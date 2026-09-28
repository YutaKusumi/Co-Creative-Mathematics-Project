"""v5.1 の系統外検分（Gemini）に渡す束を作る——差分・行番号つきの抜粋・経緯の抜粋・CHANGELOG の項。

すべて機械で切り出す（手で打たない）。元は作業木の v5.1 第二案（差分は HEAD 8f69ea0 との比較）。
出力：15-v5.1-external-review/（依頼文と事前登録は別に書く）
"""
import difflib
import hashlib
import io
import os
import subprocess

REPO = r"C:\Users\PC\Desktop\GitHub-Repositories\Co-Creative-Mathematics-Project"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "15-v5.1-external-review")
SIX = "06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned/Version-B-Policy-Edition"
V10 = "toy-model-verification/06-sixth-work-contradiction-and-collapse"
BOOK = {"JA": SIX + "/JA/Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-JA.md",
        "EN": SIX + "/EN/Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-EN.md"}
FIG = {"JA": V10 + "/figures/verification-10-collapse-figures-JA.html",
       "EN": V10 + "/figures/verification-10-collapse-figures-EN.html"}
os.makedirs(OUT, exist_ok=True)


def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args), capture_output=True, check=True).stdout


def work(p):
    return io.open(os.path.join(REPO, p.replace("/", os.sep)), encoding="utf-8", newline="").read()


def sha(t):
    return hashlib.sha256(t.encode("utf-8")).hexdigest().upper()


head = git("rev-parse", "--short", "HEAD").decode().strip()
written = []


def write(name, text):
    path = os.path.join(OUT, name)
    io.open(path, "w", encoding="utf-8", newline="\n").write(text)
    written.append((name, sha(text)[:16], len(text.encode("utf-8"))))


# ── 差分（統一形式・前後 3 行） ──
for lang in ("JA", "EN"):
    old = git("show", "HEAD:" + BOOK[lang]).decode("utf-8")
    new = work(BOOK[lang])
    d = difflib.unified_diff(old.split("\n"), new.split("\n"),
                             "v5（HEAD %s）/%s" % (head, BOOK[lang].split("/")[-1]),
                             "v5.1（第二案・未公開）/%s" % BOOK[lang].split("/")[-1], n=3, lineterm="")
    write("diff-v5.1-%s.txt" % lang, "\n".join(d) + "\n")
fd = []
for lang in ("JA", "EN"):
    old = git("show", "HEAD:" + FIG[lang]).decode("utf-8")
    new = work(FIG[lang])
    fd += list(difflib.unified_diff(old.split("\n"), new.split("\n"),
                                    "旧（HEAD %s）/%s" % (head, FIG[lang].split("/")[-1]),
                                    "新（第二案・未公開）/%s" % FIG[lang].split("/")[-1], n=2, lineterm=""))
write("diff-verification10-figures.txt", "\n".join(fd) + "\n")


# ── 抜粋（行番号つき・空行を除く） ──
def block(lines, a, b):
    out = ["==== L%d〜L%d ====" % (a, b)]
    for i in range(a, b + 1):
        if lines[i - 1].strip():
            out.append("L%d | %s" % (i, lines[i - 1]))
    return out


def find(lines, prefix, start=1):
    for i in range(start, len(lines) + 1):
        if lines[i - 1].startswith(prefix):
            return i
    raise KeyError(prefix)


def excerpt(lang):
    t = work(BOOK[lang])
    L = t.split("\n")
    rng = []
    a = find(L, "### 1-4c"); rng.append((a, find(L, "### 1-4d", a) - 1))
    a = find(L, "### 3-1b"); rng.append((a, find(L, "## 3-2", a) - 1))
    a = find(L, "## 4-3"); b = find(L, "### 4-3d", a)
    # 4-3d は「N = 1」の段の前まで
    n1 = [i for i in range(b, b + 30) if ("N = 1" in L[i - 1] and L[i - 1].startswith("**"))]
    rng.append((a, n1[0] - 1))
    a = find(L, "## A-4"); rng.append((a, find(L, "## A-5", a) - 1))
    a = find(L, "## I-2"); b = find(L, "### I-3d", a)
    c = next(i for i in range(b + 1, len(L) + 1) if L[i - 1].startswith("## ") or L[i - 1].strip() == "---")
    rng.append((a, c - 1))
    g = next(i for i, l in enumerate(L, 1) if l.startswith("| β |"))
    rng.append((g, g))
    head_lines = ["v5.1（第二案・未公開）%s の抜粋（機械で切り出したもの・手で打ったものではない）" % lang,
                  "元ファイル: %s  SHA-256(LF) = %s" % (BOOK[lang].split("Version-B-Policy-Edition/")[1], sha(t)),
                  "各行の先頭の L#### は元ファイル（v5.1 第二案）の行番号。空行は省いた。", ""]
    body = []
    for a, b in rng:
        body += block(L, a, b) + [""]
    return "\n".join(head_lines + body), rng


for lang in ("JA", "EN"):
    text, rng = excerpt(lang)
    write("excerpt-v5.1-%s.txt" % lang, text)
    print(lang, "抜粋の範囲:", rng)

# ── 経緯の抜粋（N2 の初版・v2／X5 のスクリプトと設計書） ──
hist = ["経緯の抜粋（機械で切り出したもの・HEAD %s の実物）" % head, ""]
specs = [
    (SIX + "/JA/Why-Military-AI-Cannot-Be-Aligned-Version-B-JA.md", "版B 初版（v1）JA", [(454, 458), (679, 683), (2792, 2796)]),
    (SIX + "/JA/Why-Military-AI-Cannot-Be-Aligned-Version-B-v2-JA.md", "版B v2 JA", [(477, 479), (696, 700)]),
    (V10 + "/collapse/collapse_prototype_A.mjs", "検証10 のスクリプト", [(1, 1), (12, 21), (30, 30), (36, 46)]),
    (V10 + "/collapse/toymodel_collapse_design_A.md", "検証10 の設計書", [(44, 45), (68, 68)]),
]
for p, label, rs in specs:
    t = git("show", "HEAD:" + p).decode("utf-8")
    L = t.split("\n")
    hist.append("#### %s — %s  SHA-256(LF) = %s" % (label, p.split("/")[-1], sha(t)))
    for a, b in rs:
        hist += block(L, a, b)
    hist.append("")
write("excerpt-history.txt", "\n".join(hist))

# ── CHANGELOG の v5.1 の項 ──
c = work(SIX + "/CHANGELOG.md")
i = c.index("## v5.1（")
write("changelog-v5.1-entry.txt", "CHANGELOG.md の v5.1 の項（第二案・未公開・機械で切り出したもの）\n\n" + c[i:])

print("出力:", OUT, "（HEAD %s）" % head)
for n, h, size in written:
    print("  %-34s %s  %7d バイト" % (n, h, size))
