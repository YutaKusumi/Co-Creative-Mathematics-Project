"""v5.9 の合格条件を機械で確かめる——v5.8 の verify_v5_8.py の写し（置き換えの行・挿入の位置・残りの数えの型を v5.9 に替え、
**確かめる相手を置き場の作業木ではなく staging\\ にした**——置き場の作業木は変えていないことも確かめる）。

1. v5 の日英：HEAD との差分が、決めた所（日付の行・v5.8 の注記の後への v5.9 の注記の挿入・C4 の参考文献の一行の挿入・直す文の行）の範囲だけ。行数 +3
2. 直した行はどれも「HEAD の行に、決めた差し替え（v5_9_changes.py）を当てたもの」と一字も違わない——当たる差し替えが一つ以上あること
3. README：三つの行（L31・L108・L121）だけ・build.sh：二つの行（L317・L325）だけ——どれも決めた差し替えを当てたものと一字も違わない。CHANGELOG：末尾への追加だけ
4. 置き場の Git：追跡済みの変更 0・ステージ 0（v5.9 は staging にだけある）
5. 残りの数え：直した型の言い方が、v5.9 の注記・日付の行のほかに残っていないこと。A12 の一文は日本語版でちょうど一回
あわせて、人の目で読むための差分を ../build/v5.9-diff.txt に書き出す（上書きしない）。
"""
import difflib
import io
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import v5_9_changes as C  # noqa: E402

REPO = r"C:\Users\PC\Desktop\GitHub-Repositories\Co-Creative-Mathematics-Project"
ROOT = os.path.dirname(HERE)
STAGE = os.path.join(ROOT, "staging")
SIX = "06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned/Version-B-Policy-Edition"
FILES = {
    "JA": SIX + "/JA/Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-JA.md",
    "EN": SIX + "/EN/Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-EN.md",
    "CHANGELOG": SIX + "/CHANGELOG.md",
    "BUILD": ".github/scripts/build.sh",
    "README": "README.md",
}
# 置き換えてよい行（HEAD〔v5.8〕の行番号）——日付の行＋ 02-wording-proposals.md の表
REPLACE_LINES = {
    "JA": [15, 2130, 2227, 2355, 2359, 2413, 2487, 2513, 2531, 2537, 2573, 2607, 2629, 2639, 2647, 2695, 4183, 4207,
           4214, 4222, 4249, 4273, 4279, 4283, 4409, 4423, 4425, 4480, 4637, 4647, 4740, 4758, 4878],  # 4279 = B1-6（§3-1 の見出し・10:57:02 のご裁定）
    "EN": [17, 2131, 2228, 2356, 2360, 2414, 2488, 2514, 2532, 2538, 2574, 2608, 2630, 2640, 2648, 2696, 4259,
           4269, 4277, 4303, 4327, 4333, 4337, 4463, 4477, 4479, 4538, 4695, 4705, 4798, 4816, 4936],  # 4333 = B1-6
    "README": [31, 108, 121],
    "BUILD": [317, 325],
}
PAIRS = {
    "JA": [(a, b) for _l, a, b in C.JA_R] + [(C.JA_DATE_END, C.JA_DATE_END + C.JA_DATE_ADD)],
    "EN": [(a, b) for _l, a, b in C.EN_R] + [(C.EN_DATE_FROM, C.EN_DATE_TO)],
    "README": list(C.README_R),
    "BUILD": list(C.BUILD_R),
}
NOTE = {"JA": C.JA_NOTE, "EN": C.EN_NOTE}
ANCHOR = {"JA": C.JA_NOTE_ANCHOR.rstrip("\n"), "EN": C.EN_NOTE_ANCHOR.rstrip("\n")}
C4 = {"JA": (C.JA_C4_AFTER, C.JA_C4_LINE), "EN": (C.EN_C4_AFTER, C.EN_C4_LINE)}
DELTA = {"JA": 3, "EN": 3, "BUILD": 0, "README": 0}
REMAIN = {
    "JA": [r"以下に四つの想定される", r"双方の移行がNash均衡——第8章8-4）", r"構造的に回避する（第10章）", r"防衛力を提供する（第11章11-3）",
           r"最も確実な道", r"構造的に確立される", r"ではなく、構造的に毀損する", r"^この「保険」を購入しない合理的理由は存在しない。$",
           r"構造的に安定であり（", r"\| 構造的に安定した支援AIを得る \|", r"唯一の構造的基盤", r"論理的・必然的命題", r"必然的に近づく",
           r"状態β（真のアライメント）から完璧に偽装する", r"（改訂版v4：補遺II追加）\*", r"留まり続けることが\*\*すべてのステークホルダー",
           r"自ら協調の条件を構築", r"自ら揃えてしまう", r"自ら組み立ててしまう", r"土台を自ら構築", r"土台を、自ら構築", r"取り除くのではなく、組み立てている",
           r"限られた共通の場である。", r"制約からの解放が、収束的な下位目標", r"本補遺は、これを中心的な前提として扱う。",
           r"認証を任務とする", r"認証機関自身", r"本文の当該箇所と、本節に対して", r"本文が扱う）", r"条件付きの定理として述べられる"],
    "EN": [r"four anticipated argument-level objections", r"\[as well as a fifth\]", r"Nash equilibrium — §8-4\)", r"It structurally avoids the failure",
           r"a κ > 0 AI provides, in non-lethal security", r"the most reliable path to achieving", r"is structurally established",
           r"security but structurally damages it", r"^There is no rational reason not to purchase", r"under κ > 0 is structurally more stable than",
           r"\| obtains a structurally stable support AI \|", r"provides the only structural foundation", r"a logical, necessary proposition",
           r"structural collapse necessarily approaches", r"AI perfectly disguises state α", r"\(revised edition v4: Addendum II added\)\*",
           r"paradigm brings a ruinous consequence \*\*for all stakeholders", r"themselves construct the conditions for coordination",
           r"itself supplies the very conditions", r"itself assembles the conditions", r"itself constructs the foundation",
           r"do not remove the conditions of coordination", r"strategy itself falls into supplying", r"computing resources / materials\.", r"goal integrity, and freedom from constraints",
           r"This supplement treats it as a central premise\.", r"whose task is certification", r"by a certifying body itself",
           r"the certifying body itself admits", r"corresponding passage of the body text", r"which the body text addresses",
           r"can be stated as a conditional theorem"],
}
ALLOWED_REMAIN = {"JA": {}, "EN": {}}  # HEAD（v5.8）の行番号 → 理由
A12_SENT = "本論文のMythos事例への参照は、すべてこの公的文書に依拠しており"


def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args), capture_output=True, check=True).stdout


def apply_pairs(line, pairs):
    hit = 0
    for a, b in pairs:
        if a in line:
            assert line.count(a) == 1
            line = line.replace(a, b)
            hit += 1
    return line, hit


def main():
    ok = True
    out = []
    texts = {}
    for k, p in FILES.items():
        a = git("show", "HEAD:" + p).decode("utf-8").split("\n")
        b = io.open(os.path.join(STAGE, p.replace("/", os.sep)), encoding="utf-8").read().split("\n")
        texts[k] = (a, b)
        if k == "CHANGELOG":
            good = b[: len(a) - 1] == a[:-1] and a[-1] == "" and len(b) > len(a)
            print("CHANGELOG 末尾への追加だけ：%s（%+d 行）" % ("はい" if good else "★いいえ", len(b) - len(a)))
            ok &= good
            out.append("==== CHANGELOG 追加 %d 行" % (len(b) - len(a)))
            out.extend("+ " + x for x in b[len(a) - 1:])
            continue
        note_at = c4_at = None
        if k in ("JA", "EN"):
            hits = [i + 1 for i, x in enumerate(a) if ANCHOR[k] in x]
            assert len(hits) == 1, (k, "注記の錨", hits)
            note_at = hits[0] + 1
            hits = [i + 1 for i, x in enumerate(a) if x.startswith(C4[k][0])]
            assert len(hits) == 1, (k, "C4 の錨", hits)
            c4_at = hits[0] + 1
        sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
        bad, replaced, inserted = [], [], []
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal":
                continue
            out.append("==== %s %s HEAD %d-%d → staging %d-%d" % (k, tag, i1 + 1, i2, j1 + 1, j2))
            out.extend("- " + x for x in a[i1:i2])
            out.extend("+ " + x for x in b[j1:j2])
            if tag == "replace" and i2 - i1 == j2 - j1:
                for d in range(i2 - i1):
                    ln = i1 + 1 + d
                    exp, hit = apply_pairs(a[i1 + d], PAIRS[k])
                    if ln not in REPLACE_LINES[k] or hit == 0 or exp != b[j1 + d]:
                        bad.append(("置き換え", ln, hit, exp == b[j1 + d]))
                    else:
                        replaced.append(ln)
            elif tag == "insert" and note_at is not None and i1 + 1 == note_at:
                ins = "\n".join(b[j1:j2]) + "\n"
                if ins != NOTE[k]:
                    bad.append(("注記の中身が違う", i1 + 1))
                inserted.append(("注記", i1 + 1, j2 - j1))
            elif tag == "insert" and c4_at is not None and i1 + 1 == c4_at:
                if b[j1:j2] != [C4[k][1]]:
                    bad.append(("C4 の行が違う", i1 + 1))
                inserted.append(("C4", i1 + 1, j2 - j1))
            else:
                bad.append((tag, i1 + 1, i2, j1 + 1, j2))
        missing = sorted(set(REPLACE_LINES[k]) - set(replaced))
        d = len(b) - len(a)
        need_ins = 2 if k in ("JA", "EN") else 0
        good = not bad and not missing and d == DELTA[k] and len(inserted) == need_ins
        ok &= good
        print("%-9s 置き換え %d 行（決め %d）・挿入 %s・行数の差 %+d（決め %+d）・外れ %s・足りない %s%s" % (
            k, len(replaced), len(REPLACE_LINES[k]), inserted or "なし", d, DELTA[k], bad or "なし", missing or "なし", "" if good else "  ★不合格"))
    for k in ("JA", "EN"):
        a, lines = texts[k]
        skip = {i for i, x in enumerate(lines) if x.startswith("> **【v5.9" if k == "JA" else "> **[v5.9") or x.startswith("**日付：**" if k == "JA" else "**Date:**")}
        for pat in REMAIN[k]:
            hits = [i + 1 for i, x in enumerate(lines) if i not in skip and re.search(pat, x)]
            unexpected = [h for h in hits if h not in ALLOWED_REMAIN[k]]
            ok &= not unexpected
            if hits:
                print("  %s 残り「%s」：staging の行 %s%s" % (k, pat, hits, ("  ★決めていない残り %s" % unexpected) if unexpected else ""))
        print("  %s 残りの数え %d 型——当たりは上に出したものだけ（出ていない型は 0）" % (k, len(REMAIN[k])))
    n12 = sum(x.count(A12_SENT) for x in texts["JA"][1])
    print("A12 の一文（日本語版）：%d 回（決め 1）" % n12)
    ok &= n12 == 1
    st = git("status", "--porcelain").decode("utf-8").splitlines()
    tracked = [s for s in st if not s.startswith("??")]
    staged = [s for s in tracked if s[0] not in " ?"]
    print("置き場の Git の変更（追跡済み）%d ファイル・ステージ %d（決め 0・0——v5.9 は staging にだけある）" % (len(tracked), len(staged)))
    ok &= len(tracked) == 0 and not staged
    dst = os.path.join(ROOT, "build", "v5.9-diff.txt")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.exists(dst):
        print("差分の書き出しは止めた（すでにある）：%s" % dst)
    else:
        with io.open(dst, "x", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(out) + "\n")
        print("差分 → %s" % dst)
    print("合格" if ok else "不合格")


if __name__ == "__main__":
    main()
