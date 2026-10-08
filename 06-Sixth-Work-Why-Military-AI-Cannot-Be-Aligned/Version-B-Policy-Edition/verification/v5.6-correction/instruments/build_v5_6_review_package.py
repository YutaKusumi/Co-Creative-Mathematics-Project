"""v5.6 の系統外の検分（Gemini）に渡す束を作る——差分・行番号つきの抜粋・経緯の抜粋・CHANGELOG の項（v5.5 の build_v5_5_review_package.py の形を写し、
v5.6 の範囲〔第8章の全文・§4-3b・§12-3・§13-4a〕に替えた）。

すべて機械で切り出す（手で打たない）。元は作業木の v5.6 の案（差分は HEAD 0f2147f との比較）。
出力：02-v5.6-external-review/（依頼文と事前登録は別に書く）。すでにあるファイルは上書きしない。
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
OUT = os.path.join(ROOT, "02-v5.6-external-review")
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
EXPECT_HEAD = "0f2147f"
# 経緯の数え（直した型の言い方）
COUNT = {
    "JA": [("完全に転覆", "完全に転覆"), ("最適戦略であることを示す", "最適戦略であることを示す"), ("Nash均衡は「ともに", "Nash均衡は「ともに"),
           ("移行が依然としてナッシュ均衡", "移行が依然としてナッシュ均衡"), ("Nash均衡分析（第8章", r"Nash均衡分析（第8章"),
           ("ジレンマのNash均衡）", "ジレンマのNash均衡）"), ("能力に比例して増大", "能力に比例して増大"), ("能力のすべての次元", "能力のすべての次元"),
           ("8-2　証明", "8-2　証明"), ("§4-3b の復元力の留保", "復元力――内面化・修正の容量――を省いている")],
    "EN": [("completely overturns", "completely overturns"), ("the optimal strategy game-theoretically", "optimal strategy game-theoretically"),
           ("The Nash equilibrium is \"both", "The Nash equilibrium is \"both"), ("whether the transition to κ > 0 remains a Nash equilibrium", "whether the transition to κ > 0 remains a Nash equilibrium"),
           ("Nash-equilibrium analysis of the extended", "Nash-equilibrium analysis of the extended"),
           ("(the Nash equilibrium of the extended prisoner's dilemma)", r"\(the Nash equilibrium of the extended prisoner's dilemma\)"),
           ("in proportion to capability", "in proportion to capability"), ("Every dimension of capability", "Every dimension of capability"),
           ("§4-3b restoring-force reservation", "omits the restoring force")],
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
                                    "v5.5（HEAD %s・公開版）/%s" % (head, p),
                                    "v5.6（案・未公開）/%s" % p, n=2, lineterm=""))
write("diff-v5.6.txt", "\n".join(dl) + "\n")


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
    while not lines[b - 1].strip() or lines[b - 1].strip() == "---":
        b -= 1
    return a, b, block(lines, a, b, title)


HDR = {"JA": "【v5.6（案・未公開）の抜粋——日本語版（原義）】\n元：%s（作業木・LF・SHA-256 %s）\n行番号は v5.6 の案のもの（直す前の v5.5 とは、冒頭の注記の追加で 2 行ずれる）。空行は省いた。",
       "EN": "[Excerpt of v5.6 (draft, unpublished) — English edition]\nSource: %s (working tree, LF, SHA-256 %s)\nLine numbers are those of the v5.6 draft (they are shifted by 2 lines from v5.5, because of the added notice at the top). Blank lines are omitted."}
SECS = {"JA": [("### 4-3b", "§4-3b（全文——「重要な留保」〔復元力・閾値〕の参照先）"), ("# 第8章", "第8章（全文）"),
               ("## 12-3", "§12-3（全文）"), ("### 13-4a", "§13-4a（全文）")],
        "EN": [("### 4-3b", "§4-3b (full text — referred to for the \"important reservation\" [restoring force, threshold])"), ("# Chapter 8", "Chapter 8 (full text)"),
               ("## 12-3", "§12-3 (full text)"), ("### 13-4a", "§13-4a (full text)")]}
LISTS = {"JA": [(re.compile(r"Nash|ナッシュ"), "本書全体で「Nash」「ナッシュ」を含む行の一覧（機械で探した）"),
                (re.compile(r"最適戦略|最適な戦略"), "本書全体で「最適戦略」を含む行の一覧（機械で探した）"),
                (re.compile(r"比例"), "本書全体で「比例」を含む行の一覧（機械で探した）"),
                (re.compile(r"転覆|逆転"), "本書全体で「転覆」「逆転」を含む行の一覧（機械で探した）"),
                (re.compile(r"^#{1,4} .*証明"), "本書全体で見出しに「証明」を含む行の一覧（機械で探した）")],
         "EN": [(re.compile(r"Nash"), "List of all lines in the book containing \"Nash\" (machine search)"),
                (re.compile(r"(?i)optimal strateg"), "List of all lines in the book containing \"optimal strategy\" (machine search)"),
                (re.compile(r"(?i)proportion"), "List of all lines in the book containing \"proportion\" (machine search)"),
                (re.compile(r"(?i)overturn|revers"), "List of all lines in the book containing \"overturn\" / \"revers…\" (machine search)"),
                (re.compile(r"(?i)^#{1,4} .*(proof|argument)"), "List of all headings in the book containing \"proof\" or \"argument\" (machine search)")]}
for lang in ("JA", "EN"):
    text = work(BOOK[lang])
    L = text.split("\n")
    out = [HDR[lang] % (BOOK[lang].split("/")[-1], sha(text)), ""]
    inc = []
    d = find(L, starts("**日付：**" if lang == "JA" else "**Date:**"))
    out += block(L, d, d, "冒頭——日付の行" if lang == "JA" else "Front matter — the date line")
    inc.append((d, d))
    a = find(L, starts("> **【v5.5（" if lang == "JA" else "> **[v5.5 ("))
    b = find(L, starts("> **【v5.6（" if lang == "JA" else "> **[v5.6 ("))
    out += block(L, a, b, "冒頭——v5.5・v5.6 の注記" if lang == "JA" else "Front matter — the notices of v5.5 and v5.6")
    inc.append((a, b))
    for prefix, title in SECS[lang]:
        a, b, blk = sec(L, prefix, title)
        out += blk
        inc.append((a, b))
    for pat, title in LISTS[lang]:
        hits = [k for k in range(1, len(L) + 1) if pat.search(L[k - 1])]
        out.append("==== %s ====" % title)
        for k in hits:
            full = any(x <= k <= y for x, y in inc)
            m = pat.search(L[k - 1])
            snip = L[k - 1][max(0, m.start() - 100):m.end() + 160]
            s = section_of(L, k)
            s = ("冒頭（表題の下）" if lang == "JA" else "front matter (below the title)") if re.match(r"#{1,2} (なぜ|Why) ", s) else s.lstrip("# ")[:60]
            out.append("L%d | %s | %s" % (k, s, ("上の抜粋に全文あり" if lang == "JA" else "full text above") if full
                                           else ("抜粋：…" if lang == "JA" else "snippet: …") + snip + "…"))
        out.append("（%d 行）" % len(hits) if lang == "JA" else "(%d lines)" % len(hits))
        out.append("")
    write("excerpt-v5.6-%s.txt" % lang, "\n".join(out) + "\n")

# ── 経緯の抜粋（古い版の実物から：言い方の数） ──
hx = ["【経緯の抜粋——古い版の実物から機械で切り出したもの】", "各行：版・ファイル・SHA-256 の頭 16 桁・直した型の言い方を含む行の数（v5.5 は直す前の公開版＝HEAD）", ""]
for lang in ("JA", "EN"):
    for name, p in OLDER[lang] + [("v5.5（HEAD）" if lang == "JA" else "v5.5 (HEAD)", None)]:
        t = work(p) if p else git("show", "HEAD:" + BOOK[lang]).decode("utf-8")
        Lx = t.split("\n")
        cnt = []
        for label, pat in COUNT[lang]:
            rx = re.compile(pat)
            cnt.append("「%s」%d" % (label, sum(1 for s in Lx if rx.search(s))))
        hx.append("==== %s %s（%s・SHA-256 %s）：%s ====" % (lang, name, (p or BOOK[lang]).split("/")[-1], sha(t)[:16], "・".join(cnt)))
    hx.append("")
write("excerpt-history.txt", "\n".join(hx) + "\n")

# ── CHANGELOG の v5.6 の項 ──
cl = work(SIX + "/CHANGELOG.md")
i = cl.index("\n## v5.6（")
write("changelog-v5.6-entry.txt", cl[i + 1:])

for name, s16, n in written:
    print("%-28s %8d バイト  SHA-256 %s" % (name, n, s16))
