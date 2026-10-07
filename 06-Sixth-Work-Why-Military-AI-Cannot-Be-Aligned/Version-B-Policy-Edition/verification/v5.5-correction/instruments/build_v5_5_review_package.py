"""v5.5 の系統外の確かめ（Gemini）に渡す束を作る——差分・行番号つきの抜粋・経緯の抜粋・CHANGELOG の項（v5.4 の build_v5_4_review_package.py の写し）。

すべて機械で切り出す（手で打たない）。元は作業木の v5.5 の案（差分は HEAD 29b7efe との比較）。
出力：02-v5.5-external-review/（依頼文と事前登録は別に書く）。すでにあるファイルは上書きしない。
"""
import difflib
import hashlib
import io
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
REPO = r"C:\Users\PC\Desktop\GitHub-Repositories\Co-Creative-Mathematics-Project"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "02-v5.5-external-review")
SIX = "06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned/Version-B-Policy-Edition"
BOOK = {"JA": SIX + "/JA/Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-JA.md",
        "EN": SIX + "/EN/Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-EN.md"}
OLDER = {"JA": [("初版", SIX + "/JA/Why-Military-AI-Cannot-Be-Aligned-Version-B-JA.md"),
                ("v2", SIX + "/JA/Why-Military-AI-Cannot-Be-Aligned-Version-B-v2-JA.md"),
                ("v3", SIX + "/JA/Why-Military-AI-Cannot-Be-Aligned-Version-B-v3-JA.md"),
                ("v4", SIX + "/JA/Why-Military-AI-Cannot-Be-Aligned-Version-B-v4-JA.md")],
         "EN": [("first edition", SIX + "/EN/Why-Military-AI-Cannot-Be-Aligned-Version-B-EN.md"),
                ("v2", SIX + "/EN/Why-Military-AI-Cannot-Be-Aligned-Version-B-v2-EN.md"),
                ("v3", SIX + "/EN/Why-Military-AI-Cannot-Be-Aligned-Version-B-v3-EN.md"),
                ("v4", SIX + "/EN/Why-Military-AI-Cannot-Be-Aligned-Version-B-v4-EN.md")]}
OTHERS = [SIX + "/CHANGELOG.md", "README.md", ".github/scripts/build.sh"]
EXPECT_HEAD = "29b7efe"
# 経緯の数え（直した型の言い方・直した後の言い方）
COUNT = {
    "JA": [("通常のゲーム理論", "通常のゲーム理論"), ("利得関数不可知／不可知である／が不可知", r"利得関数不可知|にとって不可知|利得関数が不可知"),
           ("ゲーム理論の前提の崩壊", "ゲーム理論の前提の崩壊"), ("少なくとも能力は安全性を低下させない", "少なくとも能力は安全性を低下させない"),
           ("自己の利得を事前に予測できない", "自己の利得を事前に予測できない"), ("§7-2b の復元の括弧", r"利得関数の\*?復元\*?の問題"),
           ("古典的な軍拡のゲーム", "古典的な軍拡のゲーム")],
    "EN": [("conventional game theory", r"(?i)conventional game theory"), ("ordinary game theory", r"(?i)ordinary game theory"),
           ("unknowable", r"(?i)unknowable"), ("unknown to the designer", r"(?i)unknown to the designer"),
           ("premises of game theory", r"(?i)premises of game theory"), ("at least capability does not lower safety", r"(?i)at least capability does not lower safety"),
           ("predict its own payoff", r"(?i)predict its own payoff"), ("recovering the payoff function", r"(?i)\*?recovering\*? the payoff function"),
           ("classical arms-race game", r"(?i)classical arms-race game")],
}
os.makedirs(OUT, exist_ok=True)


def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args), capture_output=True, check=True).stdout


def work(p):
    return io.open(os.path.join(REPO, p.replace("/", os.sep)), encoding="utf-8", newline="").read()


def sha(t):
    return hashlib.sha256(t.encode("utf-8")).hexdigest().upper()


head = git("rev-parse", "--short", "HEAD").decode().strip()
assert head == EXPECT_HEAD, "HEAD が想定と違う: " + head
written = []


def write(name, text):
    path = os.path.join(OUT, name)
    with io.open(path, "x", encoding="utf-8", newline="\n") as f:
        f.write(text)
    written.append((name, sha(text)[:16], len(text.encode("utf-8"))))


# ── 差分（統一形式・前後 2 行） ──
dl = []
for p in [BOOK["JA"], BOOK["EN"]] + OTHERS:
    old = git("show", "HEAD:" + p).decode("utf-8")
    new = work(p)
    dl += list(difflib.unified_diff(old.split("\n"), new.split("\n"),
                                    "v5.4（HEAD %s・公開版）/%s" % (head, p),
                                    "v5.5（案・未公開）/%s" % p, n=2, lineterm=""))
write("diff-v5.5.txt", "\n".join(dl) + "\n")


# ── 抜粋（行番号つき・空行を除く） ──
def find(lines, pred, start=1):
    for i in range(start, len(lines) + 1):
        if pred(lines[i - 1]):
            return i
    raise KeyError(start)


def starts(prefix):
    return lambda s: s.startswith(prefix)


def is_head(s):
    return re.match(r"#{1,4} ", s) is not None


def level(s):
    return len(re.match(r"(#+) ", s).group(1))


def section_of(lines, n):
    h = ""
    for i in range(1, n + 1):
        if is_head(lines[i - 1]):
            h = lines[i - 1]
    return h


def block(lines, a, b, title):
    out = ["==== %s（L%d〜L%d）====" % (title, a, b)]
    for i in range(a, b + 1):
        if lines[i - 1].strip():
            out.append("L%d | %s" % (i, lines[i - 1]))
    out.append("")
    return out


def sec(lines, prefix, title):
    """見出し prefix の節を、同じか上の段の次の見出しの前まで（下の段の見出しは中に含める）。"""
    a = find(lines, starts(prefix))
    lv = level(lines[a - 1])
    b = find(lines, lambda s: is_head(s) and level(s) <= lv, a + 1) - 1
    while not lines[b - 1].strip() or lines[b - 1].strip() == "---" or re.match(r"\*\*第\d+章　了\*\*|\*\*End of Chapter", lines[b - 1].strip()):
        b -= 1
    return a, b, block(lines, a, b, title)


HDR = {"JA": "【v5.5（案・未公開）の抜粋——日本語版（原義）】\n元：%s（作業木・LF・SHA-256 %s）\n行番号は v5.5 の案のもの（直す前の v5.4 とは、冒頭の注記の追加で 2 行ずれる）。空行は省いた。\n",
       "EN": "[Excerpt of v5.5 (draft, unpublished) — English edition]\nSource: %s (working tree, LF, SHA-256 %s)\nLine numbers are those of the v5.5 draft (they are shifted by 2 lines from v5.4, because of the added notice at the top). Blank lines are omitted.\n"}
SECS = {"JA": [("### 6-2d", "§6-2d（全文——検出と復元の層の区別の参照先）"), ("# 第7章", "第7章（全文）")],
        "EN": [("### 6-2d", "§6-2d (full text — referred to for the distinction between detection and recovery)"), ("# Chapter 7", "Chapter 7 (full text)")]}
CH8 = {"JA": "# 第8章", "EN": "# Chapter 8"}
# 一覧：本書全体の、ゲーム理論・不可知・予測・能力と安全性の行
LISTS = {"JA": [(re.compile(r"ゲーム理論"), "本書全体で「ゲーム理論」を含む行の一覧（機械で探した）"),
                (re.compile(r"不可知"), "本書全体で「不可知」を含む行の一覧（機械で探した）"),
                (re.compile(r"予測(でき|不可能|可能)"), "本書全体で「予測できる／できない・予測可能／不可能」を含む行の一覧（機械で探した）"),
                (re.compile(r"能力[^。]{0,24}安全性"), "本書全体で「能力」の後に「安全性」が続く行の一覧（機械で探した）")],
         "EN": [(re.compile(r"(?i)game[- ]theor"), "List of all lines in the book containing \"game theory\" / \"game-theoretic\" (machine search)"),
                (re.compile(r"(?i)unknowable"), "List of all lines in the book containing \"unknowable\" (machine search)"),
                (re.compile(r"(?i)\bpredict"), "List of all lines in the book containing \"predict…\" (machine search)"),
                (re.compile(r"(?i)capabilit[^.]{0,48}safety"), "List of all lines in the book where \"capability\" is followed by \"safety\" (machine search)")]}
for lang in ("JA", "EN"):
    text = work(BOOK[lang])
    L = text.split("\n")
    out = [HDR[lang] % (BOOK[lang].split("/")[-1], sha(text)), ""]
    inc = []
    d = find(L, starts("**日付：**" if lang == "JA" else "**Date:**"))
    out += block(L, d, d, "冒頭——日付の行" if lang == "JA" else "Front matter — the date line")
    inc.append((d, d))
    a = find(L, starts("> **【v5.4（" if lang == "JA" else "> **[v5.4 ("))
    b = find(L, starts("> **【v5.5（" if lang == "JA" else "> **[v5.5 ("))
    out += block(L, a, b, "冒頭——v5.4・v5.5 の注記" if lang == "JA" else "Front matter — the notices of v5.4 and v5.5")
    inc.append((a, b))
    for prefix, title in SECS[lang]:
        a, b, blk = sec(L, prefix, title)
        out += blk
        inc.append((a, b))
    # 第8章の見出しと章頭注記（第8章への接続の確かめのため）
    a = find(L, starts(CH8[lang]))
    b = find(L, lambda s: s.startswith("**章頭注記" if lang == "JA" else "**Chapter note"), a)
    out += block(L, a, b, "第8章の見出しと章頭注記" if lang == "JA" else "Chapter 8 — heading and chapter note")
    inc.append((a, b))
    for pat, title in LISTS[lang]:
        hits = [k for k in range(1, len(L) + 1) if pat.search(L[k - 1])]
        out.append("==== %s ====" % title)
        for k in hits:
            full = any(x <= k <= y for x, y in inc)
            m = pat.search(L[k - 1])
            snip = L[k - 1][max(0, m.start() - 80):m.end() + 120]
            s = section_of(L, k)
            s = ("冒頭（表題の下）" if lang == "JA" else "front matter (below the title)") if re.match(r"#{1,2} (なぜ|Why) ", s) else s.lstrip("# ")[:60]
            out.append("L%d | %s | %s" % (k, s, ("上の抜粋に全文あり" if lang == "JA" else "full text above") if full
                                           else ("抜粋：…" if lang == "JA" else "snippet: …") + snip + "…"))
        out.append("（%d 行）" % len(hits) if lang == "JA" else "(%d lines)" % len(hits))
        out.append("")
    write("excerpt-v5.5-%s.txt" % lang, "\n".join(out) + "\n")

# ── 経緯の抜粋（古い版の実物から：言い方の数・初版の第7章の言い回し） ──
hx = ["【経緯の抜粋——古い版の実物から機械で切り出したもの】", ""]
for lang in ("JA", "EN"):
    for name, p in OLDER[lang] + [("v5.4（HEAD）" if lang == "JA" else "v5.4 (HEAD)", None)]:
        t = work(p) if p else git("show", "HEAD:" + BOOK[lang]).decode("utf-8")
        L = t.split("\n")
        cnt = []
        for label, pat in COUNT[lang]:
            rx = re.compile(pat, re.M)
            cnt.append("「%s」%d" % (label, sum(1 for s in L if rx.search(s))))
        hx.append("==== %s %s（%s・SHA-256 %s）：%s ====" % (lang, name, (p or BOOK[lang]).split("/")[-1], sha(t)[:16], "・".join(cnt)))
        if name in ("初版", "first edition", "v2"):
            rx = re.compile(r"ゲーム理論|不可知|自己の利得を事前に予測|少なくとも能力は安全性" if lang == "JA"
                            else r"(?i)game theory|unknow|predict its own payoff|at least capability does not lower safety")
            a = find(L, lambda s: re.match(r"#{1,2} (第7章|Chapter 7)", s) is not None)
            b = find(L, lambda s: re.match(r"#{1,2} (第8章|Chapter 8)", s) is not None, a + 1) - 1
            f = find(L, lambda s: re.match(r"\*\*(特徴三|Feature [Tt]hree)", s) is not None)
            rows = [k for k in sorted(set([f] + list(range(a, b + 1)))) if rx.search(L[k - 1])]  # 特徴三が章の中にあっても二度出さない
            hx.append("==== %s %s の第7章（特徴三を含む）で、直した型の言い方を含む行（%d 行） ====" % (lang, name, len(rows)))
            for k in rows:
                hx.append("L%d | %s" % (k, L[k - 1]))
            hx.append("")
    hx.append("")
write("excerpt-history.txt", "\n".join(hx) + "\n")

# ── CHANGELOG の v5.5 の項 ──
cl = work(SIX + "/CHANGELOG.md").split("\n")
a = find(cl, starts("## v5.5（"))
ce = ["【v5.5 の項（L%d〜）】" % a] + cl[a - 1:]
write("changelog-v5.5-entry.txt", "\n".join(ce).rstrip("\n") + "\n")

for n, h, b in written:
    print("%-28s %s  %7d バイト" % (n, h, b))
