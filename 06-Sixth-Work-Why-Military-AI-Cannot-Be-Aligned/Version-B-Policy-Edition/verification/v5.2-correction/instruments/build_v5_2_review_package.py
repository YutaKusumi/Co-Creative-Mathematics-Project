"""v5.2 の系統外の確かめ（Gemini）に渡す束を作る——差分・行番号つきの抜粋・経緯の抜粋・CHANGELOG の項。

すべて機械で切り出す（手で打たない）。元は作業木の v5.2 の案（差分は HEAD 59aee42 との比較）。
出力：02-v5.2-external-review/（依頼文と事前登録は別に書く）。すでにあるファイルは上書きしない。
"""
import difflib
import hashlib
import io
import os
import re
import subprocess

REPO = r"C:\Users\PC\Desktop\GitHub-Repositories\Co-Creative-Mathematics-Project"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "02-v5.2-external-review")
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
OLD_SENT = {"JA": "METR の観測（第4章 §4-1b で詳述）は、モデルが評価されていることを検知する能力が、既に現実のモデルで確認されていることを示す。",
            "EN": "METR's observations (detailed in Chapter 4, §4-1b) show that the ability of models to detect that they are being evaluated has already been confirmed in real models."}
EXPECT_HEAD = "59aee42"
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
                                    "v5.1（HEAD %s・公開版）/%s" % (head, p),
                                    "v5.2（案・未公開）/%s" % p, n=2, lineterm=""))
write("diff-v5.2.txt", "\n".join(dl) + "\n")


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


HDR = {"JA": "【v5.2（案・未公開）の抜粋——日本語版（原義）】\n元：%s（作業木・LF・SHA-256 %s）\n行番号は v5.2 の案のもの（直す前の v5.1 とは、冒頭の注記の追加で 2 行ずれる）。空行は省いた。\n",
       "EN": "[Excerpt of v5.2 (draft, unpublished) — English edition]\nSource: %s (working tree, LF, SHA-256 %s)\nLine numbers are those of the v5.2 draft (they are shifted by 2 lines from v5.1, because of the added notice at the top). Blank lines are omitted.\n"}
PAT = {"JA": re.compile(r"METR|評価察知|評価認識|評価者認識|評価を察知|評価文脈を察知|評価されていることを検知|(?i:evaluation[- ]awareness)"),
       "EN": re.compile(r"\bMETR\b|(?i:evaluation[- ]awareness|evaluator awareness|being evaluated)")}
LIST_TITLE = {"JA": "本書全体で次の語を含む行の一覧（機械で数えた）：METR・評価察知・評価認識・評価者認識・評価を察知・評価文脈を察知・評価されていることを検知・evaluation awareness",
              "EN": "List of all lines in the book containing any of the following (machine search): METR (case-sensitive, as a word); evaluation awareness / evaluation-awareness, evaluator awareness, being evaluated (case-insensitive)"}
for lang in ("JA", "EN"):
    text = work(BOOK[lang])
    L = text.split("\n")
    out = [HDR[lang] % (BOOK[lang].split("/")[-1], sha(text)), ""]
    inc = []
    d = find(L, starts("**日付：**" if lang == "JA" else "**Date:**"))
    out += block(L, d, d, "冒頭——日付の行" if lang == "JA" else "Front matter — the date line")
    inc.append((d, d))
    a = find(L, starts("> **【改訂版 v5（" if lang == "JA" else "> **[Revised edition v5 ("))
    b = find(L, starts("> **【v5.2（" if lang == "JA" else "> **[v5.2 ("))
    out += block(L, a, b, "冒頭——v5・v5.1・v5.2 の注記" if lang == "JA" else "Front matter — the notices of v5, v5.1 and v5.2")
    inc.append((a, b))
    for prefix, title in [("### 3-3d", "§3-3d（全文）"), ("### 4-1b", "§4-1b（全文）"),
                          ("### 4-3d", "§4-3d（全文）"), ("### 6-1c", "§6-1c（全文）"),
                          ("### J-4-1", "附録J J-4-1（全文）")]:
        if lang == "EN":
            title = title.replace("（全文）", " (full text)").replace("附録J ", "Appendix J ")
        a, b, blk = sec(L, prefix, title)
        out += blk
        inc.append((a, b))
    pat = PAT[lang]
    hits = [i for i in range(1, len(L) + 1) if pat.search(L[i - 1])]
    # 附録 H・I の METR の行（見出しつき・全文）
    for i in hits:
        s = section_of(L, i)
        if "METR" in L[i - 1] and re.match(r"#{2,4} (H-|I-)", s):
            out += block(L, i, i, ("附録の METR の行——見出し「%s」" if lang == "JA" else "A METR line in an appendix — heading \"%s\"") % s.lstrip("# "))
            inc.append((i, i))
    # 一覧
    out.append("==== %s ====" % LIST_TITLE[lang])
    for i in hits:
        full = any(x <= i <= y for x, y in inc)
        m = pat.search(L[i - 1])
        snip = L[i - 1][max(0, m.start() - 60):m.end() + 100]
        s = section_of(L, i)
        s = ("冒頭（表題の下）" if lang == "JA" else "front matter (below the title)") if re.match(r"#{1,2} (なぜ|Why) ", s) else s.lstrip("# ")[:60]
        out.append("L%d | %s | %s | %s" % (i, s,
                                           ("上の抜粋に全文あり" if lang == "JA" else "full text above") if full else ("抜粋：…" if lang == "JA" else "snippet: …") + snip + "…",
                                           ", ".join(sorted(set(x.group(0) for x in pat.finditer(L[i - 1]))))))
    out.append("（%d 行）" % len(hits) if lang == "JA" else "(%d lines)" % len(hits))
    write("excerpt-v5.2-%s.txt" % lang, "\n".join(out) + "\n")


# ── 経緯の抜粋（v3・v4 の同じ一文、v3 の §4-1b、初版・v2 に §3-3d が無いこと、CHANGELOG の v3 の項） ──
hx = ["【経緯の抜粋——古い版の実物から機械で切り出したもの】", ""]
for lang in ("JA", "EN"):
    for name, p in OLDER[lang]:
        t = work(p)
        L = t.split("\n")
        n33 = sum(1 for s in L if s.startswith("### 3-3d"))
        hit = [i for i in range(1, len(L) + 1) if OLD_SENT[lang] in L[i - 1]]
        hx.append("==== %s %s（%s・SHA-256 %s）：「### 3-3d」の見出し %d 個・旧い一文 %s ====" % (
            lang, name, p.split("/")[-1], sha(t)[:16], n33, ("L" + ", L".join(map(str, hit))) if hit else "なし"))
        if name == "v3":
            a, b, blk = sec(L, "### 4-1b", "%s v3 の §4-1b（全文）" % lang)
            hx += blk
            hx.append("（v3 の §4-1b の中の「METR」：%d 回）" % sum(L[i - 1].count("METR") for i in range(a, b + 1)))
            hx.append("")
            for i in hit:
                hx += block(L, i, i, "%s v3 の §3-3d の旧い一文" % lang)
        if name == "v4":
            a, b, _ = sec(L, "### 4-1b", "")
            hx.append("（v4 の §4-1b の中の「METR」：%d 回）" % sum(L[i - 1].count("METR") for i in range(a, b + 1)))
            hx.append("")
cl = work(SIX + "/CHANGELOG.md").split("\n")
i = find(cl, lambda s: "P2-5" in s and "3-3d" in s)
hx += block(cl, i, i, "CHANGELOG.md の v3 の項の該当行（見出し「%s」）" % section_of(cl, i).lstrip("# "))
write("excerpt-history.txt", "\n".join(hx) + "\n")

# ── CHANGELOG の v5.2 の項 ──
a = find(cl, starts("## v5.2（"))
write("changelog-v5.2-entry.txt", "\n".join(cl[a - 1:]).rstrip("\n") + "\n")

for name, s16, n in written:
    print("%-28s %s  %7d バイト" % (name, s16, n))
