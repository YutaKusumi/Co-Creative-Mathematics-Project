"""v5.6 の合格条件を機械で確かめる（計画書 §3・§4 の 2）——v5.5 の verify_v5_5.py の写し（置き換えの行・挿入の位置・残りの数えの型を v5.6 に替えた）。

1. v5 の日英：HEAD との差分が、決めた所（日付の行・v5.5 の注記の後への v5.6 の注記の挿入・直す文の行）の範囲だけ。行数 +2
2. 直した行はどれも「HEAD の行に、決めた差し替え（v5_6_changes.py）を当てたもの」と一字も違わない——当たる差し替えが一つ以上あること
3. README：三つの行（L31・L108・L121）だけ・build.sh：二つの行（L317・L325）だけ——どれも決めた差し替えを当てたものと一字も違わない。CHANGELOG：末尾への追加だけ
4. Git の変更は 5 ファイルだけ・何も加えていない（ステージが空）
5. 残りの数え：直した型の言い方（「完全に転覆」「Nash均衡は「ともに」「比例して増大」など）が、直さないと決めた所と v5.6 の注記・日付の行の引用のほかに残っていないこと
あわせて、人の目で読むための差分を ../build/v5.6-diff.txt に書き出す（上書きしない）。
"""
import difflib
import io
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v5_6_changes as C  # noqa: E402

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
    "JA": [15, 1188, 1316, 1330, 1362, 1380, 1390, 1396, 1448, 1460, 1476, 2070, 2407],  # v5.6：日付の行＋計画書 §1 (2) の十か所＋⑦⑧（§6-6・§7-5——系統外の検分の指摘）
    "EN": [17, 1191, 1317, 1331, 1363, 1391, 1397, 1449, 1461, 1477, 2071, 2408],  # v5.6：日付の行＋九か所（②-4 は日本語版だけ）＋⑦⑧
    "README": [31, 108, 121],
    "BUILD": [317, 325],
}
INSERT_AT = {"JA": 48, "EN": 50}  # v5.6：v5.5 の注記（日 L47・英 L49）の後
PAIRS = {
    "JA": [(a, b) for _l, a, b in C.JA_R] + [(C.JA_DATE_END, C.JA_DATE_END + C.JA_DATE_ADD)],
    "EN": [(a, b) for _l, a, b in C.EN_R] + [(C.EN_DATE_FROM, C.EN_DATE_TO)],
    "README": list(C.README_R),
    "BUILD": list(C.BUILD_R),
}
NOTE = {"JA": C.JA_NOTE, "EN": C.EN_NOTE}
DELTA = {"JA": 2, "EN": 2, "BUILD": 0, "README": 0}
# 直した型の言い方——残ってよいのは、直さないと決めた所（HEAD の行番号・計画書 §1 (3)）と、日付の行・v5.6 の注記（引用）だけ
REMAIN = {
    "JA": [r"完全に転覆", r"最適戦略であることを示す", r"Nash均衡は「ともに", r"能力に比例して増大", r"能力のすべての次元", r"8-2　証明",
           r"移行が依然としてナッシュ均衡", r"Nash均衡分析（第8章", r"ジレンマのNash均衡）", r"論理そのものを転覆"],
    "EN": [r"completely overturns", r"optimal strategy game-theoretically", r"The Nash equilibrium is \"both", r"in proportion to capability",
           r"Every dimension of capability", r"whether the transition to κ > 0 remains a Nash equilibrium", r"Nash-equilibrium analysis of the extended",
           r"\(the Nash equilibrium of the extended prisoner's dilemma\)", r"overturns the very logic"],
}
ALLOWED_REMAIN = {"JA": {}, "EN": {2352: "§13 の現在の決定の選択肢（3）の \"the visualization of the internal state in proportion to capability improvement\""
                                     "——内部状態の可視化を能力の向上に比例させる政策の選択肢で、因子三の破壊力の言い方ではない（一回目の verify で見つけた・2026-10-08）"}}  # HEAD（v5.5）の行番号 → 理由


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
                if ins != NOTE[k]:  # 先頭の空行と注記の一行（v5_6_changes の NOTE と一字も違わない）
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
        skip = {i for i, x in enumerate(lines) if x.startswith("> **【v5.6" if k == "JA" else "> **[v5.6") or x.startswith("**日付：**" if k == "JA" else "**Date:**")}
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
    dst = os.path.join(ROOT, "build", "v5.6-diff.txt")
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
