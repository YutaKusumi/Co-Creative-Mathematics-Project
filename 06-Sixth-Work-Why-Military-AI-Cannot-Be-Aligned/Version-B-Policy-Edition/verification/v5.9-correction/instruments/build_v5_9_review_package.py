"""v5.9 の系統外の検分（Gemini）に渡す束を作る——差分・行番号つきの抜粋・経緯の抜粋・CHANGELOG の項（v5.8 の build_v5_8_review_package.py の形を写し、
v5.9 の範囲〔第12章 §12-2c・§12-3・第13章 §13-0a の経路B・§13-3〔全文〕・§13-4a・第14章 §14-3〔全文〕・§14-4・第15章〔全文〕・著者注〔全文〕・
補遺I〔全文〕・補遺II の要旨・§1-1・§4・§5 の頭・§5-2・§6・§8-3・§9-10・§11・参考文献〕に替えた）。

すべて機械で切り出す（手で打たない）。元は staging の v5.9 の案（差分は置き場の HEAD b40d13b との比較）。
出力：05-v5.9-external-review/（依頼文と事前登録は別に書く）。すでにあるファイルは上書きしない。
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
STAGE = os.path.join(ROOT, "staging")
OUT = os.path.join(ROOT, "05-v5.9-external-review")
SIX = "06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned/Version-B-Policy-Edition"
BOOK = {"JA": SIX + "/JA/Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-JA.md",
        "EN": SIX + "/EN/Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-EN.md"}
OTHERS = [SIX + "/CHANGELOG.md", "README.md", ".github/scripts/build.sh"]
EXPECT_HEAD = "b40d13b"
os.makedirs(OUT, exist_ok=True)


def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args), capture_output=True, check=True).stdout


def stage(p):
    return io.open(os.path.join(STAGE, p.replace("/", os.sep)), encoding="utf-8", newline="").read()


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
    new = stage(p)
    dl += list(difflib.unified_diff(old.split("\n"), new.split("\n"),
                                    "v5.8（HEAD %s・公開版）/%s" % (head, p),
                                    "v5.9（案・未公開）/%s" % p, n=2, lineterm=""))
write("diff-v5.9.txt", "\n".join(dl) + "\n")


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


def sec(lines, prefix, title, start=1, head_only=False):
    """見出し prefix の節を、同じか上の段の次の見出しの前まで（下の段の見出しは中に含める）。head_only なら、次のどの段の見出しの前までも（節の頭だけ）。"""
    a = find(lines, starts(prefix), start)
    lv = level(lines[a - 1])
    try:
        b = find(lines, (lambda s: is_head(s)) if head_only else (lambda s: is_head(s) and level(s) <= lv), a + 1) - 1
    except KeyError:
        b = len(lines)
    while not lines[b - 1].strip() or lines[b - 1].strip() == "---":
        b -= 1
    return a, b, block(lines, a, b, title)


HDR = {"JA": "【v5.9（案・未公開）の抜粋——日本語版（原義）】\n元：%s（staging・LF・SHA-256 %s）\n行番号は v5.9 の案のもの（直す前の v5.8 とは、冒頭の注記の追加で 2 行ずれ、補遺II の参考文献の追加の後ろはさらに 1 行ずれる）。空行は省いた。",
       "EN": "[Excerpt of v5.9 (draft, unpublished) — English edition]\nSource: %s (staging, LF, SHA-256 %s)\nLine numbers are those of the v5.9 draft (shifted by 2 lines from v5.8 because of the added notice at the top, and by 1 more line after the reference added to Addendum II). Blank lines are omitted."}
# (見出しの頭, 題, 探し始めの目印〔補遺の中の同じ番号の節を区別する〕)
SECS = {"JA": [("### 12-2c", "第12章 §12-2c（全文）", None), ("## 12-3", "第12章 §12-3（全文）", None),
               ("### 13-0a", "第13章 §13-0a（全文——経路B の応答を含む）", None), ("## 13-3", "第13章 §13-3（全文——想定される反論と §13-3b の u′）", None),
               ("### 13-4a", "第13章 §13-4a（全文——三つの命題）", None), ("## 14-3", "第14章 §14-3（全文）", None), ("## 14-4", "第14章 §14-4（全文）", None),
               ("# 第15章", "第15章（全文）", None), ("# 著者注", "著者注（全文）", None),
               ("# 第六著作 補遺", "補遺I（全文）", None),
               ("## 要旨", "補遺II 要旨（全文）", "# 第六著作 補遺II"), ("### 1-1", "補遺II §1-1 反証条件（全文）", "# 第六著作 補遺II"),
               ("## 4. ", "補遺II §4 前提B（全文）", "# 第六著作 補遺II"), ("## 5. ", "補遺II §5 の頭（§5-1 の前まで）", "# 第六著作 補遺II"),
               ("### 5-2", "補遺II §5-2（全文）", "# 第六著作 補遺II"), ("## 6. ", "補遺II §6 結論（全文）", "# 第六著作 補遺II"),
               ("### 8-3", "補遺II §8-3（全文）", "# 第六著作 補遺II"), ("### 9-10", "補遺II §9-10（全文）", "# 第六著作 補遺II"),
               ("## 11. ", "補遺II §11 主張しないこと（全文）", "# 第六著作 補遺II"), ("## 参考文献", "補遺II 参考文献（全文）", "# 第六著作 補遺II")],
        "EN": [("### 12-2c", "§12-2c of Chapter 12 (full text)", None), ("## 12-3", "§12-3 of Chapter 12 (full text)", None),
               ("### 13-0a", "§13-0a of Chapter 13 (full text — including the response to route B)", None),
               ("## 13-3", "§13-3 of Chapter 13 (full text — anticipated objections and u′ in §13-3b)", None),
               ("### 13-4a", "§13-4a of Chapter 13 (full text — the three propositions)", None), ("## 14-3", "§14-3 of Chapter 14 (full text)", None),
               ("## 14-4", "§14-4 of Chapter 14 (full text)", None), ("# Chapter 15", "Chapter 15 (full text)", None),
               ("# Author's note", "Author's note (full text)", None), ("# Supplement to the Sixth Work", "Supplement I (full text)", None),
               ("## Abstract", "Addendum II abstract (full text)", "# Addendum II to the Sixth Work"),
               ("### 1-1", "Addendum II §1-1 falsification conditions (full text)", "# Addendum II to the Sixth Work"),
               ("## 4. ", "Addendum II §4 Premise B (full text)", "# Addendum II to the Sixth Work"),
               ("## 5. ", "Addendum II head of §5 (up to §5-1)", "# Addendum II to the Sixth Work"),
               ("### 5-2", "Addendum II §5-2 (full text)", "# Addendum II to the Sixth Work"),
               ("## 6. ", "Addendum II §6 conclusion (full text)", "# Addendum II to the Sixth Work"),
               ("### 8-3", "Addendum II §8-3 (full text)", "# Addendum II to the Sixth Work"),
               ("### 9-10", "Addendum II §9-10 (full text)", "# Addendum II to the Sixth Work"),
               ("## 11. ", "Addendum II §11 what it does not claim (full text)", "# Addendum II to the Sixth Work"),
               ("## References", "Addendum II references (full text)", "# Addendum II to the Sixth Work")]}
LISTS = {"JA": [(re.compile(r"Nash均衡"), "本書全体で「Nash均衡」を含む行の一覧（機械で探した）"),
                (re.compile(r"構造的に(回避|安定|確立|毀損)"), "本書全体で「構造的に回避／安定／確立／毀損」を含む行の一覧"),
                (re.compile(r"唯一の|最も確実|必然的|完璧に偽装"), "本書全体で「唯一の」「最も確実」「必然的」「完璧に偽装」を含む行の一覧"),
                (re.compile(r"すべてのステークホルダー|β > 1 の条件下では|β > 1の条件下では"), "本書全体で「すべてのステークホルダー」「β > 1 の条件下では」を含む行の一覧"),
                (re.compile(r"認証を任務|認証機関|標準化機関|評価と標準化"), "本書全体で NIST の役割の言い方（「認証を任務」「認証機関」「標準化機関」「評価と標準化」）を含む行の一覧"),
                (re.compile(r"定理"), "補遺II の中で「定理」を含む行の一覧（補遺II の範囲だけ）", "# 第六著作 補遺II"),
                (re.compile(r"Bostrom|Lynch"), "本書全体で「Bostrom」「Lynch」を含む行の一覧")],
         "EN": [(re.compile(r"Nash equilibri"), "List of all lines containing \"Nash equilibrium\" (machine search)"),
                (re.compile(r"(?i)structurally (avoid|more stable|stable|established|damag)"), "List of all lines containing \"structurally avoid / (more) stable / established / damag\""),
                (re.compile(r"(?i)\bthe only\b|most reliable|necessar|perfectly disguis"), "List of all lines containing \"the only\" / \"most reliable\" / \"necessar…\" / \"perfectly disguis…\""),
                (re.compile(r"(?i)all stakeholders|under the condition β > 1"), "List of all lines containing \"all stakeholders\" / \"under the condition β > 1\""),
                (re.compile(r"(?i)task is certification|certifying body|standardization body|evaluation and standardization"), "List of all lines with NIST-role wording (\"task is certification\", \"certifying body\", \"standardization body\", \"evaluation and standardization\")"),
                (re.compile(r"(?i)theorem"), "List of lines containing \"theorem\" within Addendum II only", "# Addendum II to the Sixth Work"),
                (re.compile(r"Bostrom|Lynch"), "List of all lines containing \"Bostrom\" / \"Lynch\"")]}
for lang in ("JA", "EN"):
    text = stage(BOOK[lang])
    L = text.split("\n")
    out = [HDR[lang] % (BOOK[lang].split("/")[-1], sha(text)), ""]
    inc = []
    d = find(L, starts("**日付：**" if lang == "JA" else "**Date:**"))
    out += block(L, d, d, "冒頭——日付の行" if lang == "JA" else "Front matter — the date line")
    inc.append((d, d))
    a = find(L, starts("> **【v5.6（" if lang == "JA" else "> **[v5.6 ("))
    b = find(L, starts("> **【v5.9（" if lang == "JA" else "> **[v5.9 ("))
    out += block(L, a, b, "冒頭——v5.6〜v5.9 の注記" if lang == "JA" else "Front matter — the notices of v5.6 to v5.9")
    inc.append((a, b))
    for prefix, title, mark in SECS[lang]:
        st = find(L, starts(mark)) if mark else 1
        a, b, blk = sec(L, prefix, title, st, head_only=prefix == "## 5. ")
        out += blk
        inc.append((a, b))
    for item in LISTS[lang]:
        pat, title = item[0], item[1]
        lo = find(L, starts(item[2])) if len(item) > 2 else 1
        hits = [k for k in range(lo, len(L) + 1) if pat.search(L[k - 1])]
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
    write("excerpt-v5.9-%s.txt" % lang, "\n".join(out) + "\n")

# ── 経緯の抜粋（A2：命題三の行の三つの版・v5.6 の注記の主張） ──
hx = ["【経緯の抜粋——置き場の git の古い版の実物から機械で切り出したもの】",
      "A2：v5.6 の注記（日 L49／英 L51——v5.8 の行番号）は「§12-3・§13-4a に β > 1・長期・二人ゲームの限定を戻した」と書く。各版の命題三の行に「二人ゲーム」「two-player」があるか", ""]
for lang, needle, word in (("JA", "命題三：κ > 0への移行が合理的戦略である", "二人ゲーム"), ("EN", "Proposition three: the transition to κ > 0 is the rational strategy", "two-player")):
    for c in ("bef20eb", "0868bc3", "8345c96"):
        t = git("show", "%s:%s" % (c, BOOK[lang])).decode("utf-8")
        Lx = t.split("\n")
        ks = [i + 1 for i, s in enumerate(Lx) if needle in s]
        assert len(ks) == 1, (lang, c, ks)
        hx.append("%s commit %s（%s）：命題三は L%d・「%s」%s" % (lang, c, {"bef20eb": "v5.6", "0868bc3": "v5.7", "8345c96": "v5.8"}[c], ks[0], word,
                                                       "あり" if word in Lx[ks[0] - 1] else "なし"))
    hx.append("")
write("excerpt-history.txt", "\n".join(hx) + "\n")

# ── CHANGELOG の v5.9 の項 ──
cl = stage(SIX + "/CHANGELOG.md")
i = cl.index("\n## v5.9（")
write("changelog-v5.9-entry.txt", cl[i + 1:])

for name, s16, n in written:
    print("%-28s %8d バイト  SHA-256 %s" % (name, n, s16))
