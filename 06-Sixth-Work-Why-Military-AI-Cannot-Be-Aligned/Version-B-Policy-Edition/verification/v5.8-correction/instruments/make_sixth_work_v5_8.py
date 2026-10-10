"""第六著作 v5.8 を作る（第10〜12章の期待効用の条件・第12章の章題と §12-1a・§10-2 の見出しと第10章の二文・§10-5d の経路一・§10-5b の Constitutional AI）
——v5.7 の make_sixth_work_v5_7.py の写し（中身は v5_8_changes.py・想定の HEAD 1ba548d・CHANGELOG の末尾の確かめ〔v5.7 の公開の行〕だけ替えた——十四か所とも日英）。

登録者の決め（2026-10-10 夜・十二本目の動画の作業場 00-deviations.md）：「公開の前に v5.8（推奨）」（20:14:03）・言い回しは ①「比の条件の形に」②「κ = 0の機能は…に」③「見出しを中立に」⑤「§10-5b に一文」（21:01:30）・④ は推奨どおり。
元にするのは常にリポジトリの HEAD のファイル——作業木に書き出すので、何度実行しても同じ結果になる。
差し替えは、どれも元の文字列がちょうど一回現れることを確かめてから行う。改行は LF のまま・BOM なし。
計画書：（公開の写し）../01-source-correction-plan-v5.8.md
使い方: python make_sixth_work_v5_8.py
"""
import hashlib
import io
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
REPO = r"C:\Users\PC\Desktop\GitHub-Repositories\Co-Creative-Mathematics-Project"
SIX = "06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned/Version-B-Policy-Edition"
P = {
    "JA": SIX + "/JA/Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-JA.md",
    "EN": SIX + "/EN/Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-EN.md",
    "CHANGELOG": SIX + "/CHANGELOG.md",
    "BUILD": ".github/scripts/build.sh",
    "README": "README.md",
}
EXPECT_HEAD = "1ba548d"


def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args), capture_output=True, check=True).stdout


head = git("rev-parse", "--short", "HEAD").decode().strip()
assert head == EXPECT_HEAD, "HEAD が想定と違う: " + head
base = {k: git("show", "HEAD:" + p).decode("utf-8") for k, p in P.items()}
for k, t in base.items():
    assert "\r" not in t, k + " に CR がある"


def once(text, old, new, label):
    n = text.count(old)
    assert n == 1, "%s: 元の文字列が %d 回現れる" % (label, n)
    return text.replace(old, new)


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v5_8_changes import *  # noqa: F401,F403,E402（直しの中身——確かめる道具と同じもの）

out = {}
t = base["JA"]
for label, a, b in JA_R:
    t = once(t, a, b, "JA " + label)
t = once(t, JA_DATE_END, JA_DATE_END + JA_DATE_ADD, "JA 日付の行")
t = once(t, JA_NOTE_ANCHOR, JA_NOTE_ANCHOR + JA_NOTE, "JA 注記")
out["JA"] = t
t = base["EN"]
for label, a, b in EN_R:
    t = once(t, a, b, "EN " + label)
t = once(t, EN_DATE_FROM, EN_DATE_TO, "EN 日付の行")
t = once(t, EN_NOTE_ANCHOR, EN_NOTE_ANCHOR + EN_NOTE, "EN 注記")
out["EN"] = t
t = base["README"]
for a, b in README_R:
    t = once(t, a, b, "README")
out["README"] = t
t = base["BUILD"]
for a, b in BUILD_R:
    t = once(t, a, b, "BUILD")
out["BUILD"] = t


def line_of(text, s):
    hits = [i + 1 for i, x in enumerate(text.split("\n")) if s in x]
    assert len(hits) == 1, (s[:30], hits)
    return hits[0]


def lines_for(mark, R, key):
    olds = [line_of(base[key], a) for label, a, b in R if label.startswith(mark)]
    news = [line_of(out[key], b) for label, a, b in R if label.startswith(mark)]
    return sorted(set(news)), sorted(set(olds))


rows = []
for mark, name in PLACES:
    jn, jo = lines_for(mark, JA_R, "JA")
    en, eo = lines_for(mark, EN_R, "EN")
    fmt = lambda xs: "・".join("L%d" % x for x in xs)
    en_part = "英 %s〔%s〕" % (fmt(en), fmt(eo))  # v5.8：十四か所とも日英
    rows.append("\n  - %s %s（日 %s〔%s〕・%s）" % (mark, name, fmt(jn), fmt(jo), en_part))
sha16 = {k: hashlib.sha256(out[k].encode("utf-8")).hexdigest().upper()[:16] for k in ("JA", "EN")}
cl = base["CHANGELOG"]
assert cl.endswith("- [x] v5.7（JA・EN）の公開（2026-10-08・登録者の許可による）\n"), "CHANGELOG の末尾が想定と違う"
add = (CHANGELOG_ADD.replace("@@PLACES@@", "".join(rows)).replace("@@REVIEW@@", REVIEW).replace("@@PUBLISHED@@", PUBLISHED_LINE)
       .replace("@@JA@@", sha16["JA"]).replace("@@EN@@", sha16["EN"]))
out["CHANGELOG"] = cl + add
assert "@@" not in out["CHANGELOG"], "置き換えの残り"
for k, p in P.items():
    with io.open(os.path.join(REPO, p), "w", encoding="utf-8", newline="\n") as f:
        f.write(out[k])
    print("%-9s %s 行 %d → %d  SHA-256 %s" % (k, p.split("/")[-1], base[k].count("\n"), out[k].count("\n"),
                                              hashlib.sha256(out[k].encode("utf-8")).hexdigest().upper()))
print("".join(rows))
