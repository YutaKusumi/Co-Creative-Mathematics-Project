"""v5.8 の系統外の検分（Gemini）に渡す束を作る——差分・行番号つきの抜粋・経緯の抜粋・CHANGELOG の項（v5.7 の build_v5_7_review_package.py の形を写し、
v5.8 の範囲〔冒頭の確信度台帳・§4-1a・第10章の全文・§11-4b・第12章の全文・§13-4a・附録 I-1・附録 D-1a〕に替えた）。

すべて機械で切り出す（手で打たない）。元は作業木の v5.8 の案（差分は HEAD 1ba548d との比較）。
出力：02-v5.8-external-review/（依頼文と事前登録は別に書く）。すでにあるファイルは上書きしない。
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
OUT = os.path.join(ROOT, "02-v5.8-external-review")
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
EXPECT_HEAD = "1ba548d"
# 経緯の数え（直した型の言い方）
COUNT = {
    "JA": [("p がいかに小さくとも", "p ?がいかに小さくとも"), ("κ > 0は何も失わない", "κ ?> ?0 ?は何も失わない"),
           ("後退しても、何も失われない", "後退しても、何も失われない"), ("§10-2 の見出しの「の回避」", r"^### 10-2[a-e]　.*の回避$"),
           ("β ≤ 1の経験的反証", r"β ?≤ ?1 ?の経験的反証"), ("期待効用を条件なしに並べる（§12-3 の第二）", "ミニマックス原理および期待効用最大化の両方により"),
           ("Constitutional AI を κ > 0 段階一の初期実装とする", "段階一（IDAの最小統合）の初期実装")],
    "EN": [("However small p may be", "However small p may be"), ("κ > 0 loses nothing", "κ > 0 loses nothing"),
           ("one retreats to a κ = 0 system, nothing is lost", "system, nothing is lost"), ("§10-2 headings \"Avoiding …\"", r"^### 10-2[a-e]　Avoiding"),
           ("refutation of β ≤ 1", "refutation of β ≤ 1"), ("expected utility without condition (§12-3 second)", "By both the minimax principle and expected-utility"),
           ("Constitutional AI as an initial implementation of stage one", "initial implementation of κ > 0 stage one")],
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
                                    "v5.7（HEAD %s・公開版）/%s" % (head, p),
                                    "v5.8（案・未公開）/%s" % p, n=2, lineterm=""))
write("diff-v5.8.txt", "\n".join(dl) + "\n")


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


HDR = {"JA": "【v5.8（案・未公開）の抜粋——日本語版（原義）】\n元：%s（作業木・LF・SHA-256 %s）\n行番号は v5.8 の案のもの（直す前の v5.7 とは、冒頭の注記の追加で 2 行ずれる）。空行は省いた。",
       "EN": "[Excerpt of v5.8 (draft, unpublished) — English edition]\nSource: %s (working tree, LF, SHA-256 %s)\nLine numbers are those of the v5.8 draft (they are shifted by 2 lines from v5.7, because of the added notice at the top). Blank lines are omitted."}
SECS = {"JA": [("### 確信度台帳", "冒頭——確信度台帳（全文）"),
               ("### 4-1a", "第4章 §4-1a（全文——Mythos の訓練を述べる所）"),
               ("# 第10章", "第10章（全文）"), ("### 11-4b", "第11章 §11-4b（全文）"), ("# 第12章", "第12章（全文）"),
               ("### 13-4a", "第13章 §13-4a（全文——三つの命題）"), ("## I-1", "附録I §I-1（全文）"), ("### D-1a", "附録D §D-1a（全文）")],
        "EN": [("### A confidence ledger", "Front matter — the confidence ledger (full text)"),
               ("### 4-1a", "§4-1a of Chapter 4 (full text — where the training of Mythos is described)"),
               ("# Chapter 10", "Chapter 10 (full text)"), ("### 11-4b", "§11-4b of Chapter 11 (full text)"), ("# Chapter 12", "Chapter 12 (full text)"),
               ("### 13-4a", "§13-4a of Chapter 13 (full text — the three propositions)"), ("## I-1", "§I-1 of Appendix I (full text)"),
               ("### D-1a", "§D-1a of Appendix D (full text)")]}
LISTS = {"JA": [(re.compile(r"期待効用"), "本書全体で「期待効用」を含む行の一覧（機械で探した）"),
                (re.compile(r"何も失"), "本書全体で「何も失」を含む行の一覧（機械で探した）"),
                (re.compile(r"回避"), "本書全体で「回避」を含む行の一覧（機械で探した）"),
                (re.compile(r"経験的反証|否定的実証"), "本書全体で「経験的反証」「否定的実証」を含む行の一覧（機械で探した）"),
                (re.compile(r"Constitutional AI"), "本書全体で「Constitutional AI」を含む行の一覧（機械で探した）")],
         "EN": [(re.compile(r"(?i)expected.utility"), "List of all lines in the book containing \"expected utility\" (machine search)"),
                (re.compile(r"(?i)loses nothing|nothing is lost|no function of"), "List of all lines containing \"loses nothing\" / \"nothing is lost\" / \"no function of\" (machine search)"),
                (re.compile(r"(?i)\bavoid"), "List of all lines containing \"avoid\" (machine search)"),
                (re.compile(r"(?i)refutation of β|negative demonstration"), "List of all lines containing \"refutation of β\" / \"negative demonstration\" (machine search)"),
                (re.compile(r"Constitutional AI"), "List of all lines containing \"Constitutional AI\" (machine search)")]}
for lang in ("JA", "EN"):
    text = work(BOOK[lang])
    L = text.split("\n")
    out = [HDR[lang] % (BOOK[lang].split("/")[-1], sha(text)), ""]
    inc = []
    d = find(L, starts("**日付：**" if lang == "JA" else "**Date:**"))
    out += block(L, d, d, "冒頭——日付の行" if lang == "JA" else "Front matter — the date line")
    inc.append((d, d))
    a = find(L, starts("> **【v5.7（" if lang == "JA" else "> **[v5.7 ("))
    b = find(L, starts("> **【v5.8（" if lang == "JA" else "> **[v5.8 ("))
    out += block(L, a, b, "冒頭——v5.7・v5.8 の注記" if lang == "JA" else "Front matter — the notices of v5.7 and v5.8")
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
    write("excerpt-v5.8-%s.txt" % lang, "\n".join(out) + "\n")

# ── 経緯の抜粋（古い版の実物から：言い方の数） ──
hx = ["【経緯の抜粋——古い版の実物から機械で切り出したもの】", "各行：版・ファイル・SHA-256 の頭 16 桁・直した型の言い方を含む行の数（v5.7 は直す前の公開版＝HEAD）", ""]
for lang in ("JA", "EN"):
    for name, p in OLDER[lang] + [("v5.7（HEAD）" if lang == "JA" else "v5.7 (HEAD)", None)]:
        t = work(p) if p else git("show", "HEAD:" + BOOK[lang]).decode("utf-8")
        Lx = t.split("\n")
        cnt = []
        for label, pat in COUNT[lang]:
            rx = re.compile(pat)
            cnt.append("「%s」%d" % (label, sum(1 for s in Lx if rx.search(s))))
        hx.append("==== %s %s（%s・SHA-256 %s）：%s ====" % (lang, name, (p or BOOK[lang]).split("/")[-1], sha(t)[:16], "・".join(cnt)))
    hx.append("")
write("excerpt-history.txt", "\n".join(hx) + "\n")

# ── CHANGELOG の v5.8 の項 ──
cl = work(SIX + "/CHANGELOG.md")
i = cl.index("\n## v5.8（")
write("changelog-v5.8-entry.txt", cl[i + 1:])

for name, s16, n in written:
    print("%-28s %8d バイト  SHA-256 %s" % (name, n, s16))
