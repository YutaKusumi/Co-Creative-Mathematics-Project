"""v5.4 の系統外の確かめ（Gemini）に渡す束を作る——差分・行番号つきの抜粋・経緯の抜粋・CHANGELOG の項。

すべて機械で切り出す（手で打たない）。元は作業木の v5.4 の案（差分は HEAD 500f166 との比較）。
出力：02-v5.4-external-review/（依頼文と事前登録は別に書く）。すでにあるファイルは上書きしない。
型は v5.3 の build_v5_3_review_package.py。
"""
import difflib
import hashlib
import io
import os
import re
import subprocess

REPO = r"C:\Users\PC\Desktop\GitHub-Repositories\Co-Creative-Mathematics-Project"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "02-v5.4-external-review")
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
EXPECT_HEAD = "500f166"
# 経緯の数え（直した型の言い方・§6-2d・附録注記の限定・§6-3b の一節）
COUNT = {
    "JA": [("原理的に判別できない", "原理的に判別できない"), ("検出もでき（ない／ず）", r"検出もでき(ない|ず)"),
           ("体系内部から検出できない", "体系内部から検出できない"), ("外部から検出できない", "外部から検出できない"),
           ("保証の不在すら検出できない", "保証の不在すら検出できない"), ("監視者は…区別できない", r"監視者は状態α（欺瞞的アライメント）と状態β（真のアライメント）を区別できない"),
           ("完全な判別は…原理的に不可能", "完全な判別はκ = 0の体系では原理的に不可能"), ("§6-2d の見出し", r"^### 6-2d"),
           ("「分離した監査の下で検出困難」", "分離した監査の下で検出困難"), ("附録注記の限定（分離した監査のもとで、有限観測系列に基づいて）", "分離した監査のもとで、有限観測系列に基づいて"),
           ("補遺II「無条件命題として提示していない」", "無条件命題として提示していない"), ("§6-3b「同じ機構を共有する」", "同じ機構を共有する"),
           ("§6-3b「厳密な構造保存対応」", "厳密な構造保存対応")],
    "EN": [("cannot (,) in principle (,) distinguish", r"cannot,? in principle,? distinguish"), ("cannot be detected either", "cannot be detected either"),
           ("cannot be detected from within", "cannot be detected from within"), ("cannot be detected from outside", "cannot be detected from outside"),
           ("cannot even be detected", "cannot even be detected"), ("neither guaranteed nor detectable", "neither guaranteed nor detectable"),
           ("the human monitor cannot distinguish", "the human monitor cannot distinguish"),
           ("Complete discrimination is impossible in principle", "Complete discrimination is impossible in principle"),
           ("heading of §6-2d", r"^### 6-2d"), ("\"difficult to detect under a separated audit\"", "difficult to detect under a separated audit"),
           ("appendix-note qualifier (under a separated audit on the basis of any finite observation sequence)", "under a separated audit on the basis of any finite observation sequence"),
           ("Addendum II \"unconditional proposition\"", "does not present the gap as an unconditional proposition"),
           ("§6-3b \"share the same mechanism\"", "share the same mechanism"), ("§6-3b \"structure-preserving\"", "structure-preserving")],
}
SHOW63B = {"JA": "### 6-3b", "EN": "### 6-3b"}
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
                                    "v5.3（HEAD %s・公開版）/%s" % (head, p),
                                    "v5.4（案・未公開）/%s" % p, n=2, lineterm=""))
write("diff-v5.4.txt", "\n".join(dl) + "\n")


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


HDR = {"JA": "【v5.4（案・未公開）の抜粋——日本語版（原義）】\n元：%s（作業木・LF・SHA-256 %s）\n行番号は v5.4 の案のもの（直す前の v5.3 とは、冒頭の注記の追加で 2 行ずれる）。空行は省いた。\n",
       "EN": "[Excerpt of v5.4 (draft, unpublished) — English edition]\nSource: %s (working tree, LF, SHA-256 %s)\nLine numbers are those of the v5.4 draft (they are shifted by 2 lines from v5.3, because of the added notice at the top). Blank lines are omitted.\n"}
SECS = {"JA": [("### 確信度台帳", "確信度台帳（全文）"), ("### 1-3a", "§1-3a（全文——用語の定義を含む）"), ("## 5-4", "§5-4（全文）"),
               ("# 第6章", "第6章（全文）"), ("### 7-3a", "§7-3a（全文）"), ("## 8-5", "§8-5（全文）"), ("### 11-2b", "§11-2b（全文）"),
               ("### 12-2a", "§12-2a（全文）"), ("### 13-0a", "§13-0a（全文）"), ("### 13-3c", "§13-3c（全文）"), ("### 14-3a", "§14-3a（全文）"),
               ("### 14-3d", "§14-3d（全文）"), ("# 附録C", "附録C（全文）")],
        "EN": [("### A confidence ledger", "Confidence ledger (full text)"), ("### 1-3a", "§1-3a (full text — includes the definitions of terms)"),
               ("## 5-4", "§5-4 (full text)"), ("# Chapter 6", "Chapter 6 (full text)"), ("### 7-3a", "§7-3a (full text)"), ("## 8-5", "§8-5 (full text)"),
               ("### 11-2b", "§11-2b (full text)"), ("### 12-2a", "§12-2a (full text)"), ("### 13-0a", "§13-0a (full text)"),
               ("### 13-3c", "§13-3c (full text)"), ("### 14-3a", "§14-3a (full text)"), ("### 14-3d", "§14-3d (full text)"),
               ("# Appendix C", "Appendix C (full text)")]}
ADD2 = {"JA": "- 本文第6章は、ギャップを無条件命題として提示していない", "EN": "- Chapter 6 of the body text does not present the gap as an unconditional proposition"}
# 一覧：否定の形の行（日英とも、本書全体）
NEG = {"JA": re.compile(r"(検出|判別|区別|見分け|見抜)[^。]{0,12}?(でき(ない|ず|なかった)|不可能(?!性)|不能|られない|られず)"),
       "EN": re.compile(r"(cannot|can ?not|could not|neither|nor)[^.;]{0,50}?(detect|distinguish|discriminat|tell)|undetectab|indistinguishable|"
                        r"(detect|distinguish|discriminat)[^.;]{0,60}?impossible|impossible[^.;]{0,40}?(detect|distinguish|discriminat)")}
QUAL = {"JA": re.compile(r"分離した監査"), "EN": re.compile(r"separated audit")}
LISTN = {"JA": "本書全体で、検出・判別・区別・見分けの否定の形（「できない」「できず」「不可能」〔「不可能性」を除く〕「不能」など）を含む行の一覧（機械で探した）",
         "EN": "List of all lines in the book containing a negative form of detecting / distinguishing (\"cannot … detect/distinguish\", \"neither … nor detectable\", \"undetectable\", \"indistinguishable\", \"impossible … in principle\" near detect/distinguish) (machine search)"}
LISTQ = {"JA": "本書全体で「分離した監査」を含む行の一覧（機械で数えた）", "EN": "List of all lines in the book containing \"separated audit\" (machine search)"}
for lang in ("JA", "EN"):
    text = work(BOOK[lang])
    L = text.split("\n")
    out = [HDR[lang] % (BOOK[lang].split("/")[-1], sha(text)), ""]
    inc = []
    d = find(L, starts("**日付：**" if lang == "JA" else "**Date:**"))
    out += block(L, d, d, "冒頭——日付の行" if lang == "JA" else "Front matter — the date line")
    inc.append((d, d))
    a = find(L, starts("> **【v5.3（" if lang == "JA" else "> **[v5.3 ("))
    b = find(L, starts("> **【v5.4（" if lang == "JA" else "> **[v5.4 ("))
    out += block(L, a, b, "冒頭——v5.3・v5.4 の注記" if lang == "JA" else "Front matter — the notices of v5.3 and v5.4")
    inc.append((a, b))
    for prefix, title in SECS[lang]:
        a, b, blk = sec(L, prefix, title)
        out += blk
        inc.append((a, b))
    i = find(L, starts(ADD2[lang]))
    j = i
    while L[j].startswith("- ") or not L[j].strip():
        j += 1
        if j - i > 6:
            break
    out += block(L, i - 2, j, "補遺II §5——本文の限定の逐語の併置" if lang == "JA" else "Addendum II, §5 — the verbatim juxtaposition of the body text's qualifiers")
    inc.append((i - 2, j))
    for pat, title in ((NEG[lang], LISTN[lang]), (QUAL[lang], LISTQ[lang])):
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
    write("excerpt-v5.4-%s.txt" % lang, "\n".join(out) + "\n")

# ── 経緯の抜粋（古い版の実物から：言い方の数・§6-2d・附録注記・§6-3b） ──
hx = ["【経緯の抜粋——古い版の実物から機械で切り出したもの】", ""]
for lang in ("JA", "EN"):
    for name, p in OLDER[lang] + [("v5.3（HEAD）" if lang == "JA" else "v5.3 (HEAD)", None)]:
        t = work(p) if p else git("show", "HEAD:" + BOOK[lang]).decode("utf-8")
        L = t.split("\n")
        cnt = []
        for label, pat in COUNT[lang]:
            rx = re.compile(pat, re.M)
            cnt.append("「%s」%d" % (label, sum(1 for s in L if rx.search(s))))
        hx.append("==== %s %s（%s・SHA-256 %s）：%s ====" % (lang, name, (p or BOOK[lang]).split("/")[-1], sha(t)[:16], "・".join(cnt)))
        if name in ("初版", "first edition"):
            neg = [k for k in range(1, len(L) + 1) if NEG[lang].search(L[k - 1])]
            hx.append("==== %s %s の否定の形の行（%d 行・上の抜粋の一覧と同じ探し方） ====" % (lang, name, len(neg)))
            for k in neg:
                m = NEG[lang].search(L[k - 1])
                hx.append("L%d | %s | …%s…" % (k, section_of(L, k).lstrip("# ")[:50], L[k - 1][max(0, m.start() - 80):m.end() + 60]))
            hx.append("")
        if name in ("初版", "first edition", "v2"):
            a = find(L, starts(SHOW63B[lang]))
            b = find(L, lambda s: s.strip() and not s.startswith("#"), a + 1)
            hx += block(L, a, b, ("%s %s の §6-3b の見出しと最初の一文" % (lang, name)) if lang == "JA" else ("%s %s: the heading and first sentence of §6-3b" % (lang, name)))
    hx.append("")
write("excerpt-history.txt", "\n".join(hx) + "\n")

# ── CHANGELOG の v5.4 の項 ──
cl = work(SIX + "/CHANGELOG.md").split("\n")
a = find(cl, starts("## v5.4（"))
ce = ["【v5.4 の項（L%d〜）】" % a] + cl[a - 1:]
write("changelog-v5.4-entry.txt", "\n".join(ce).rstrip("\n") + "\n")

for n, h, b in written:
    print("%-28s %s  %7d バイト" % (n, h, b))
