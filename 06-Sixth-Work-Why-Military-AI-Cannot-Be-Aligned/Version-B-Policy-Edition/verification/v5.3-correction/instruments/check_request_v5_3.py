"""v5.3 の依頼文の中の引用と行番号が、原典の実物（HEAD の v5.2・作業木の v5.3 の案）にあることを機械で確かめる。"""
import hashlib
import io
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
REPO = r"C:\Users\PC\Desktop\GitHub-Repositories\Co-Creative-Mathematics-Project"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIX = "06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned/Version-B-Policy-Edition"
JA = SIX + "/JA/Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-JA.md"
EN = SIX + "/EN/Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-EN.md"


def git_show(p):
    return subprocess.run(["git", "-C", REPO, "show", "HEAD:" + p], capture_output=True, check=True).stdout.decode("utf-8").split("\n")


def work(p):
    return io.open(os.path.join(REPO, p), encoding="utf-8").read().split("\n")


old = {"JA": git_show(JA), "EN": git_show(EN)}
new = {"JA": work(JA), "EN": work(EN)}
req = io.open(os.path.join(ROOT, "02-v5.3-external-review", "request.txt"), encoding="utf-8").read()
checks = [
    # (版, 言語, 行, 行の中にある文字列)
    ("v5.2", "JA", 918, "以下の定理を導出する"),
    ("v5.2", "EN", 920, "derives the following theorem."),
    ("v5.3", "JA", 920, "以下の命題を導出する"),
    ("v5.3", "EN", 922, "derives the following proposition."),
    ("v5.2", "JA", 1890, "（附録J-2-1）"),
    ("v5.2", "EN", 1891, "(Appendix J-2-1)"),
    ("v5.3", "JA", 1892, "（附録J-2-1・附録J-4-1）"),
    ("v5.3", "EN", 1893, "(Appendix J-2-1, Appendix J-4-1)"),
    ("v5.3", "JA", 43, "初版はこれを「忠誠性不保証定理」と呼んでいた。v2 で名を「忠誠性不保証命題」に改めたとき、導入の一文の「定理」が残った"),
    ("v5.3", "JA", 43, "この参照は v3 以来"),
    ("v5.3", "JA", 921, None),  # 空行の次の引用を下で見る
]
ok = True
for ver, lang, n, s in checks:
    L = old[lang] if ver == "v5.2" else new[lang]
    if s is None:
        continue
    good = s in L[n - 1]
    ok &= good
    print("%s %s L%d に「%s」：%s" % (ver, lang, n, s[:40], "ある" if good else "★無い"))
# 引用の見出し（変えていない）
for lang, n_old, n_new, head in (("JA", 920, 922, "**忠誠性不保証命題：**"), ("EN", 922, 924, "**Loyalty-Non-Guarantee Proposition:**")):
    good = old[lang][n_old - 1] == new[lang][n_new - 1] and head in new[lang][n_new - 1]
    ok &= good
    print("%s 引用の行（v5.2 L%d・v5.3 L%d）が同じで見出し「%s」：%s" % (lang, n_old, n_new, head, "はい" if good else "★いいえ"))
# 依頼文の中の文字列（引用として書いたもの）
for s in ["「以下の定理を導出する」", "「（附録J-2-1）」", "「（附録J-2-1・附録J-4-1）」", "「以下の命題を導出する」",
          "日 L920・英 L922", "日 L918・英 L920", "日 L1892・英 L1893", "日 L1890・英 L1891"]:
    good = s in req
    ok &= good
    print("依頼文に「%s」：%s" % (s, "ある" if good else "★無い"))
raw = io.open(os.path.join(ROOT, "02-v5.3-external-review", "request.txt"), "rb").read()
print("依頼文 %d 字・%d バイト・SHA-256 %s" % (len(raw.decode("utf-8")), len(raw), hashlib.sha256(raw).hexdigest().upper()))
print("合格" if ok else "不合格")
