"""v5.8 の合格条件を機械で確かめる（計画書 §3・§4 の 2）——v5.7 の verify_v5_7.py の写し（置き換えの行・挿入の位置・残りの数えの型を v5.8 に替えた）。

1. v5 の日英：HEAD との差分が、決めた所（日付の行・v5.7 の注記の後への v5.8 の注記の挿入・直す文の行）の範囲だけ。行数 +2
2. 直した行はどれも「HEAD の行に、決めた差し替え（v5_8_changes.py）を当てたもの」と一字も違わない——当たる差し替えが一つ以上あること
3. README：三つの行（L31・L108・L121）だけ・build.sh：二つの行（L317・L325）だけ——どれも決めた差し替えを当てたものと一字も違わない。CHANGELOG：末尾への追加だけ
4. Git の変更は 5 ファイルだけ・何も加えていない（ステージが空）
5. 残りの数え：直した型の言い方（「p がいかに小さくとも」・「κ > 0は何も失わない」・§10-2 の見出しの「の回避」・「β ≤ 1の経験的反証」・第10章の「回避し、」「回避するかを示した」・
   期待効用を条件なしに並べる二か所）が、v5.8 の注記・日付の行の引用のほかに残っていないこと
あわせて、人の目で読むための差分を ../build/v5.8-diff.txt に書き出す（上書きしない）。
"""
import difflib
import io
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v5_8_changes as C  # noqa: E402

REPO = r"C:\Users\PC\Desktop\GitHub-Repositories\Co-Creative-Mathematics-Project"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIX = "06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned/Version-B-Policy-Edition"
FILES = {
    "JA": SIX + "/JA/Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-JA.md",
    "EN": SIX + "/EN/Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-EN.md",
    "CHANGELOG": SIX + "/CHANGELOG.md",
    "BUILD": ".github/scripts/build.sh",
    "README": "README.md",
}
# 置き換えてよい行（HEAD の行番号）と、注記を挿入する位置（HEAD のその行の前）
REPLACE_LINES = {
    "JA": [15, 1686, 1706, 1732, 1740, 1748, 1754, 1760, 1800, 1824, 1836, 1994, 2008, 2062, 2076, 2411],  # v5.8：日付の行＋計画書 §2 の十四か所＋③-8（§9-8・系統外の検分の指摘）
    "EN": [17, 1687, 1707, 1733, 1741, 1749, 1755, 1761, 1801, 1825, 1837, 1995, 2009, 2063, 2077, 2412],  # v5.8：日付の行＋十五か所
    "README": [31, 108, 121],
    "BUILD": [317, 325],
}
INSERT_AT = {"JA": 52, "EN": 54}  # v5.8：v5.7 の注記（日 L51・英 L53）の後
PAIRS = {
    "JA": [(a, b) for _l, a, b in C.JA_R] + [(C.JA_DATE_END, C.JA_DATE_END + C.JA_DATE_ADD)],
    "EN": [(a, b) for _l, a, b in C.EN_R] + [(C.EN_DATE_FROM, C.EN_DATE_TO)],
    "README": list(C.README_R),
    "BUILD": list(C.BUILD_R),
}
NOTE = {"JA": C.JA_NOTE, "EN": C.EN_NOTE}
DELTA = {"JA": 2, "EN": 2, "BUILD": 0, "README": 0}
# 直した型の言い方——残ってよいのは、日付の行・v5.8 の注記（引用）だけ
REMAIN = {
    "JA": [r"p がいかに小さくとも", r"p > 0 である限り", r"κ > 0は何も失わない", r"後退しても、何も失われない", r"^### 10-2[a-e]　.*の回避$",
           r"β ≤ 1の経験的反証", r"不成立をどのように回避し、", r"どのように回避するかを示した", r"どのように回避されるか", r"ミニマックス原理および期待効用最大化の両方により",
           r"（ミニマックス原理・期待効用最大化）"],
    "EN": [r"However small p may be", r"as long as p > 0", r"κ > 0 loses nothing", r"system, nothing is lost", r"^### 10-2[a-e]　Avoiding",
           r"refutation of β ≤ 1", r"system — .* — avoids the failure", r"system avoids the failure", r"is avoided under κ > 0", r"By both the minimax principle and expected-utility",
           r"\(the minimax principle, expected-utility maximization\)"],
}
ALLOWED_REMAIN = {"JA": {}, "EN": {}}  # HEAD（v5.7）の行番号 → 理由


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
        b = io.open(os.path.join(REPO, p), encoding="utf-8").read().split("\n")
        texts[k] = b
        if k == "CHANGELOG":
            good = b[: len(a) - 1] == a[:-1] and a[-1] == "" and len(b) > len(a)
            print("CHANGELOG 末尾への追加だけ：%s（%+d 行）" % ("はい" if good else "★いいえ", len(b) - len(a)))
            ok &= good
            out.append("==== CHANGELOG 追加 %d 行" % (len(b) - len(a)))
            out.extend("+ " + x for x in b[len(a) - 1:])
            continue
        sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
        bad, replaced, inserted = [], [], []
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal":
                continue
            out.append("==== %s %s HEAD %d-%d → 作業木 %d-%d" % (k, tag, i1 + 1, i2, j1 + 1, j2))
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
            elif tag == "insert" and k in INSERT_AT and i1 + 1 == INSERT_AT[k]:
                ins = "\n".join(b[j1:j2]) + "\n"
                if ins != NOTE[k]:  # 先頭の空行と注記の一行（v5_8_changes の NOTE と一字も違わない）
                    bad.append(("注記の中身が違う", i1 + 1))
                inserted.append((i1 + 1, j2 - j1))
            else:
                bad.append((tag, i1 + 1, i2, j1 + 1, j2))
        missing = sorted(set(REPLACE_LINES[k]) - set(replaced))
        d = len(b) - len(a)
        good = not bad and not missing and d == DELTA[k] and (k not in INSERT_AT or len(inserted) == 1)
        ok &= good
        print("%-9s 置き換え %d 行（決め %d）・挿入 %s・行数の差 %+d（決め %+d）・外れ %s・足りない %s%s" % (
            k, len(replaced), len(REPLACE_LINES[k]), inserted or "なし", d, DELTA[k], bad or "なし", missing or "なし", "" if good else "  ★不合格"))
    # 残りの数え（作業木の行 → HEAD の行：注記を挿入した位置より後は −2）
    for k in ("JA", "EN"):
        lines = texts[k]
        skip = {i for i, x in enumerate(lines) if x.startswith("> **【v5.8" if k == "JA" else "> **[v5.8") or x.startswith("**日付：**" if k == "JA" else "**Date:**")}
        for pat in REMAIN[k]:
            hits = []
            for i, x in enumerate(lines):
                if i in skip or not re.search(pat, x):
                    continue
                head_ln = i + 1 if i + 1 < INSERT_AT[k] else i + 1 - DELTA[k]
                hits.append(head_ln)
            unexpected = [h for h in hits if h not in ALLOWED_REMAIN[k]]
            ok &= not unexpected
            print("  %s 残り「%s」：HEAD の行 %s%s" % (k, pat, hits if hits else "0", ("  ★決めていない残り %s" % unexpected) if unexpected else ""))
    st = git("status", "--porcelain").decode("utf-8").splitlines()
    tracked = [s for s in st if not s.startswith("??")]
    staged = [s for s in tracked if s[0] not in " ?"]
    print("Git の変更（追跡済み）%d ファイル・ステージ %d" % (len(tracked), len(staged)))
    ok &= len(tracked) == 5 and not staged
    dst = os.path.join(ROOT, "build", "v5.8-diff.txt")
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
