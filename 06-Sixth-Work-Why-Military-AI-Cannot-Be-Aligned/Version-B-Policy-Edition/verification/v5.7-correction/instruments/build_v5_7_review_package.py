"""v5.7 の系統外の検分（Gemini）に渡す束を作る——差分・行番号つきの抜粋・経緯の抜粋・CHANGELOG の項（v5.6 の build_v5_6_review_package.py の形を写し、
v5.7 の範囲〔冒頭の「五つの仮定の不成立」と確信度台帳・§1-5・第2章の章頭注記・§2-6・§8-5・§8-6・第9章の全文・附録 L-2d〕に替えた）。

すべて機械で切り出す（手で打たない）。元は作業木の v5.7 の案（差分は HEAD 7098608 との比較）。
出力：02-v5.7-external-review/（依頼文と事前登録は別に書く）。すでにあるファイルは上書きしない。
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
OUT = os.path.join(ROOT, "02-v5.7-external-review")
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
EXPECT_HEAD = "7098608"
# 経緯の数え（直した型の言い方）
COUNT = {
    "JA": [("以下の論証によって不成立であることが示された", "以下の論証によって不成立であることが示された"),
           ("構造的論証によって不成立であることを示", "構造的論証によって不成立であることを示"),
           ("構造的論証によって不成立であることの提示（§2-6 の見出し）", "構造的論証によって不成立であることの提示"),
           ("四つが（それぞれ異なる強度と射程で）不成立", "四つが（それぞれ異なる強度と射程で）不成立"),
           ("表の仮定二の「構造的論証」", r"判別不可能性ギャップ \| 構造的論証"), ("冒頭の表の忠誠性の「認識論的論証」", r"^\| 忠誠性 \|.*\| 認識論的論証 \|"),
           ("ことを示する", "ことを示する")],
    "EN": [("was shown to fail by the following arguments", "was shown to fail by the following arguments"),
           ("fail(,) by structural argument", "fail,? by structural argument"),
           ("four of the five assumptions fail (each with a different strength and reach).", r"fail \(each with a different strength and reach\)\.$"),
           ("table: Two … structural argument", r"Indistinguishability Gap \| structural argument"),
           ("opening table: Loyalty … epistemological argument", r"^\| Loyalty \|.*\| epistemological argument \|")],
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
                                    "v5.6（HEAD %s・公開版）/%s" % (head, p),
                                    "v5.7（案・未公開）/%s" % p, n=2, lineterm=""))
write("diff-v5.7.txt", "\n".join(dl) + "\n")


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


HDR = {"JA": "【v5.7（案・未公開）の抜粋——日本語版（原義）】\n元：%s（作業木・LF・SHA-256 %s）\n行番号は v5.7 の案のもの（直す前の v5.6 とは、冒頭の注記の追加で 2 行ずれる）。空行は省いた。",
       "EN": "[Excerpt of v5.7 (draft, unpublished) — English edition]\nSource: %s (working tree, LF, SHA-256 %s)\nLine numbers are those of the v5.7 draft (they are shifted by 2 lines from v5.6, because of the added notice at the top). Blank lines are omitted."}
SECS = {"JA": [("### 五つの仮定の不成立", "冒頭——「五つの仮定の不成立」（全文・冒頭の表を含む）"), ("### 確信度台帳", "冒頭——確信度台帳（全文）"),
               ("## 1-5", "§1-5（全文）"), ("# 第2章", "第2章の見出しと章頭注記（§2-1 の前まで）"), ("## 2-6", "§2-6（全文）"),
               ("## 8-5", "§8-5（全文）"), ("## 8-6", "§8-6（全文）"), ("# 第9章", "第9章（全文）"), ("### L-2d", "附録 L-2d（全文）")],
        "EN": [("### The failure of the five assumptions", "Front matter — \"The failure of the five assumptions\" (full text, with the opening table)"),
               ("### A confidence ledger", "Front matter — the confidence ledger (full text)"), ("## 1-5", "§1-5 (full text)"),
               ("# Chapter 2", "The heading and chapter note of Chapter 2 (up to §2-1)"), ("## 2-6", "§2-6 (full text)"), ("## 8-5", "§8-5 (full text)"),
               ("## 8-6", "§8-6 (full text)"), ("# Chapter 9", "Chapter 9 (full text)"), ("### L-2d", "Appendix L-2d (full text)")]}
LISTS = {"JA": [(re.compile(r"不成立"), "本書全体で「不成立」を含む行の一覧（機械で探した）"),
                (re.compile(r"構造的論証"), "本書全体で「構造的論証」を含む行の一覧（機械で探した）"),
                (re.compile(r"認識論的論証"), "本書全体で「認識論的論証」を含む行の一覧（機械で探した）")],
         "EN": [(re.compile(r"(?i)\bfail(s|ed|ure|ures)?\b|untenable"), "List of all lines in the book containing \"fail\" / \"failure\" / \"untenable\" (machine search)"),
                (re.compile(r"(?i)structural argument"), "List of all lines in the book containing \"structural argument\" (machine search)"),
                (re.compile(r"(?i)epistemological argument"), "List of all lines in the book containing \"epistemological argument\" (machine search)")]}
for lang in ("JA", "EN"):
    text = work(BOOK[lang])
    L = text.split("\n")
    out = [HDR[lang] % (BOOK[lang].split("/")[-1], sha(text)), ""]
    inc = []
    d = find(L, starts("**日付：**" if lang == "JA" else "**Date:**"))
    out += block(L, d, d, "冒頭——日付の行" if lang == "JA" else "Front matter — the date line")
    inc.append((d, d))
    a = find(L, starts("> **【v5.6（" if lang == "JA" else "> **[v5.6 ("))
    b = find(L, starts("> **【v5.7（" if lang == "JA" else "> **[v5.7 ("))
    out += block(L, a, b, "冒頭——v5.6・v5.7 の注記" if lang == "JA" else "Front matter — the notices of v5.6 and v5.7")
    inc.append((a, b))
    for prefix, title in SECS[lang]:
        if prefix in ("# 第2章", "# Chapter 2"):
            a = find(L, starts(prefix))
            b = find(L, starts("## 2-1"), a + 1) - 1
            while not L[b - 1].strip() or L[b - 1].strip() == "---":
                b -= 1
            blk = block(L, a, b, title)
        else:
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
    write("excerpt-v5.7-%s.txt" % lang, "\n".join(out) + "\n")

# ── 経緯の抜粋（古い版の実物から：言い方の数） ──
hx = ["【経緯の抜粋——古い版の実物から機械で切り出したもの】", "各行：版・ファイル・SHA-256 の頭 16 桁・直した型の言い方を含む行の数（v5.6 は直す前の公開版＝HEAD）", ""]
for lang in ("JA", "EN"):
    for name, p in OLDER[lang] + [("v5.6（HEAD）" if lang == "JA" else "v5.6 (HEAD)", None)]:
        t = work(p) if p else git("show", "HEAD:" + BOOK[lang]).decode("utf-8")
        Lx = t.split("\n")
        cnt = []
        for label, pat in COUNT[lang]:
            rx = re.compile(pat)
            cnt.append("「%s」%d" % (label, sum(1 for s in Lx if rx.search(s))))
        hx.append("==== %s %s（%s・SHA-256 %s）：%s ====" % (lang, name, (p or BOOK[lang]).split("/")[-1], sha(t)[:16], "・".join(cnt)))
    hx.append("")
write("excerpt-history.txt", "\n".join(hx) + "\n")

# ── CHANGELOG の v5.7 の項 ──
cl = work(SIX + "/CHANGELOG.md")
i = cl.index("\n## v5.7（")
write("changelog-v5.7-entry.txt", cl[i + 1:])

for name, s16, n in written:
    print("%-28s %8d バイト  SHA-256 %s" % (name, n, s16))
