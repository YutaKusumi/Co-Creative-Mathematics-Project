"""v5.3 の系統外の確かめ（Gemini）に渡す束を作る——差分・行番号つきの抜粋・経緯の抜粋・CHANGELOG の項。

すべて機械で切り出す（手で打たない）。元は作業木の v5.3 の案（差分は HEAD d08bdd1 との比較）。
出力：02-v5.3-external-review/（依頼文と事前登録は別に書く）。すでにあるファイルは上書きしない。
型は v5.2 の build_v5_2_review_package.py。
"""
import difflib
import hashlib
import io
import os
import re
import subprocess

REPO = r"C:\Users\PC\Desktop\GitHub-Repositories\Co-Creative-Mathematics-Project"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "02-v5.3-external-review")
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
LEAD = {"JA": "命題NCの軍事的適用は、以下の定理を導出する。",
        "EN": "The military application of Proposition NC derives the following theorem."}
NAMES = {"JA": ("忠誠性不保証定理", "忠誠性不保証命題"),
         "EN": ("Theorem of Non-Guaranteed Loyalty", "Loyalty-Non-Guarantee Proposition")}
REF1122 = {"JA": "長期趨勢の観測（附録J-2-1）", "EN": "progress of training (Appendix J-2-1)"}
EXPECT_HEAD = "d08bdd1"
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
                                    "v5.2（HEAD %s・公開版）/%s" % (head, p),
                                    "v5.3（案・未公開）/%s" % p, n=2, lineterm=""))
write("diff-v5.3.txt", "\n".join(dl) + "\n")


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
    a = find(lines, starts(prefix))
    b = find(lines, is_head, a + 1) - 1
    while not lines[b - 1].strip() or lines[b - 1].strip() == "---":
        b -= 1
    return a, b, block(lines, a, b, title)


HDR = {"JA": "【v5.3（案・未公開）の抜粋——日本語版（原義）】\n元：%s（作業木・LF・SHA-256 %s）\n行番号は v5.3 の案のもの（直す前の v5.2 とは、冒頭の注記の追加で 2 行ずれる）。空行は省いた。\n",
       "EN": "[Excerpt of v5.3 (draft, unpublished) — English edition]\nSource: %s (working tree, LF, SHA-256 %s)\nLine numbers are those of the v5.3 draft (they are shifted by 2 lines from v5.2, because of the added notice at the top). Blank lines are omitted.\n"}
SECS = {"JA": [("### 確信度台帳", "確信度台帳（全文）"), ("### 5-2a", "§5-2a（全文）"), ("### B-3b", "附録B B-3b（全文）"),
               ("### B-3c", "附録B B-3c（全文）"), ("### 11-2a", "§11-2a（全文）"), ("### J-2-1", "附録J J-2-1（全文）"),
               ("### J-4-1", "附録J J-4-1（全文）"), ("## J-5", "附録J J-5 の頭（J-5a の前まで）")],
        "EN": [("### A confidence ledger", "Confidence ledger (full text)"), ("### 5-2a", "§5-2a (full text)"),
               ("### B-3b", "Appendix B B-3b (full text)"), ("### B-3c", "Appendix B B-3c (full text)"),
               ("### 11-2a", "§11-2a (full text)"), ("### J-2-1", "Appendix J J-2-1 (full text)"),
               ("### J-4-1", "Appendix J J-4-1 (full text)"), ("## J-5", "Appendix J J-5, opening (up to J-5a)")]}
# 一覧 1：命題NC・忠誠性の命題を「定理」と呼んでいないか（同じ行に両方の語）
PAT1 = {"JA": (re.compile(r"定理"), re.compile(r"命題NC|忠誠性")),
        "EN": (re.compile(r"(?i)theorem"), re.compile(r"Proposition NC|(?i:loyalty)"))}
LIST1 = {"JA": "本書全体で「定理」と（「命題NC」または「忠誠性」）を同じ行に含む行の一覧（機械で数えた）",
         "EN": "List of all lines in the book containing both \"theorem\" (case-insensitive) and (\"Proposition NC\" or \"loyalty\" (case-insensitive)) (machine search)"}
# 一覧 2：附録 J-2-1・J-4-1・J-5 への参照と「長期趨勢」
PAT2 = {"JA": re.compile(r"J-2-1|J-4-1|J-5|長期趨勢"), "EN": re.compile(r"J-2-1|J-4-1|J-5|(?i:long-term trend)")}
LIST2 = {"JA": "本書全体で「J-2-1」「J-4-1」「J-5」「長期趨勢」のどれかを含む行の一覧（機械で数えた）",
         "EN": "List of all lines in the book containing any of \"J-2-1\", \"J-4-1\", \"J-5\", \"long-term trend\" (case-insensitive) (machine search)"}
for lang in ("JA", "EN"):
    text = work(BOOK[lang])
    L = text.split("\n")
    out = [HDR[lang] % (BOOK[lang].split("/")[-1], sha(text)), ""]
    inc = []
    d = find(L, starts("**日付：**" if lang == "JA" else "**Date:**"))
    out += block(L, d, d, "冒頭——日付の行" if lang == "JA" else "Front matter — the date line")
    inc.append((d, d))
    a = find(L, starts("> **【改訂版 v5（" if lang == "JA" else "> **[Revised edition v5 ("))
    b = find(L, starts("> **【v5.3（" if lang == "JA" else "> **[v5.3 ("))
    out += block(L, a, b, "冒頭——v5・v5.1・v5.2・v5.3 の注記" if lang == "JA" else "Front matter — the notices of v5, v5.1, v5.2 and v5.3")
    inc.append((a, b))
    for prefix, title in SECS[lang]:
        a, b, blk = sec(L, prefix, title)
        if prefix == "## J-5":  # J-5 は J-5a の前まで（sec は次の見出しの前で止まる）
            pass
        out += blk
        inc.append((a, b))
    for pat_t, title in ((PAT1[lang], LIST1[lang]), (PAT2[lang], LIST2[lang])):
        if isinstance(pat_t, tuple):
            hits = [i for i in range(1, len(L) + 1) if pat_t[0].search(L[i - 1]) and pat_t[1].search(L[i - 1])]
            pat = pat_t[0]
        else:
            pat = pat_t
            hits = [i for i in range(1, len(L) + 1) if pat.search(L[i - 1])]
        out.append("==== %s ====" % title)
        for i in hits:
            full = any(x <= i <= y for x, y in inc)
            m = pat.search(L[i - 1])
            snip = L[i - 1][max(0, m.start() - 80):m.end() + 120]
            s = section_of(L, i)
            s = ("冒頭（表題の下）" if lang == "JA" else "front matter (below the title)") if re.match(r"#{1,2} (なぜ|Why) ", s) else s.lstrip("# ")[:60]
            out.append("L%d | %s | %s" % (i, s, ("上の抜粋に全文あり" if lang == "JA" else "full text above") if full
                                           else ("抜粋：…" if lang == "JA" else "snippet: …") + snip + "…"))
        out.append("（%d 行）" % len(hits) if lang == "JA" else "(%d lines)" % len(hits))
        out.append("")
    write("excerpt-v5.3-%s.txt" % lang, "\n".join(out) + "\n")

# ── 経緯の抜粋（古い版の実物から：旧い名と新しい名の数・導入の一文・§11-2a の参照・初版の §5-2a） ──
hx = ["【経緯の抜粋——古い版の実物から機械で切り出したもの】", ""]
for lang in ("JA", "EN"):
    for name, p in OLDER[lang] + [("v5.2（HEAD）" if lang == "JA" else "v5.2 (HEAD)", None)]:
        t = work(p) if p else git("show", "HEAD:" + BOOK[lang]).decode("utf-8")
        L = t.split("\n")
        old_n, new_n = (sum(s.count(x) for s in L) for x in NAMES[lang])
        lead = [i for i in range(1, len(L) + 1) if LEAD[lang] in L[i - 1]]
        ref = [i for i in range(1, len(L) + 1) if REF1122[lang] in L[i - 1]]
        hx.append("==== %s %s（%s・SHA-256 %s）：「%s」%d 回・「%s」%d 回・導入の一文「%s」%s・§11-2a の参照「%s」%s ====" % (
            lang, name, (p or BOOK[lang]).split("/")[-1], sha(t)[:16], NAMES[lang][0], old_n, NAMES[lang][1], new_n,
            LEAD[lang], ("L" + ", L".join(map(str, lead))) if lead else "なし", REF1122[lang], ("L" + ", L".join(map(str, ref))) if ref else "なし"))
        if name in ("初版", "first edition"):
            i = lead[0]
            j = find(L, lambda s: s.startswith(">"), i + 1)
            hx += block(L, i, j, "%s 初版の §5-2a の導入の一文と、続く引用" % lang if lang == "JA" else "%s first edition: the introducing sentence of §5-2a and the quotation that follows" % lang)
        if name == "v2":
            i = lead[0]
            j = find(L, lambda s: s.startswith(">"), i + 1)
            hx += block(L, i, j, "%s v2 の §5-2a の導入の一文と、続く引用" % lang if lang == "JA" else "%s v2: the introducing sentence of §5-2a and the quotation that follows" % lang)
    hx.append("")
write("excerpt-history.txt", "\n".join(hx) + "\n")

# ── CHANGELOG の v5.3 の項（と、v5.2 の項の「将来の改訂の候補」の段落） ──
cl = work(SIX + "/CHANGELOG.md").split("\n")
a = find(cl, starts("## v5.3（"))
b2 = find(cl, starts("## v5.2（"))
f = find(cl, starts("**将来の改訂の候補**"), b2)
ce = ["【v5.2 の項の「将来の改訂の候補」の段落（L%d・変えていない）】" % f, cl[f - 1], "", "【v5.3 の項（L%d〜）】" % a] + cl[a - 1:]
write("changelog-v5.3-entry.txt", "\n".join(ce).rstrip("\n") + "\n")

for name, s16, n in written:
    print("%-28s %s  %7d バイト" % (name, s16, n))
