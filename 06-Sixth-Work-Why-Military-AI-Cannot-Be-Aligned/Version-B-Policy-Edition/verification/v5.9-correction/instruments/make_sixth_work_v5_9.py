"""第六著作 v5.9 を作る——v5.8 の make_sixth_work_v5_8.py の写し（中身は v5_9_changes.py・想定の HEAD b40d13b・CHANGELOG の末尾の確かめ〔v5.8 の公開の行〕を替え、
**書き出し先を置き場の作業木ではなく、置き場の外の staging\\ にした**——commit と push のお許しの前に、原典の置き場を変えないため）。

登録者の決め（2026-10-28 朝・`../00-candidates-and-plan.md` と `../02-wording-proposals.md` の追記）：範囲「23 件すべて」（10:32:04）・言い回し「推奨の形」・
B1/B3「題も含めて 6 か所」・A14「このまま」・B4 の一次「開いて確かめる」（10:45:29）。
元にするのは常にリポジトリの HEAD のファイル（読むだけの git show）——何度実行しても同じ結果になる。
差し替えは、どれも元の文字列がちょうど一回現れることを確かめてから行う。改行は LF のまま・BOM なし。
使い方: python make_sixth_work_v5_9.py
"""
import hashlib
import io
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
REPO = r"C:\Users\PC\Desktop\GitHub-Repositories\Co-Creative-Mathematics-Project"
HERE = os.path.dirname(os.path.abspath(__file__))
STAGE = os.path.join(os.path.dirname(HERE), "staging")
SIX = "06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned/Version-B-Policy-Edition"
P = {
    "JA": SIX + "/JA/Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-JA.md",
    "EN": SIX + "/EN/Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-EN.md",
    "CHANGELOG": SIX + "/CHANGELOG.md",
    "BUILD": ".github/scripts/build.sh",
    "README": "README.md",
}
EXPECT_HEAD = "b40d13b"


def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args), capture_output=True, check=True).stdout


head = git("rev-parse", "--short", "HEAD").decode().strip()
assert head == EXPECT_HEAD, "HEAD が想定と違う: " + head
base = {k: git("show", "HEAD:" + p).decode("utf-8") for k, p in P.items()}
for k, t in base.items():
    assert "\r" not in t, k + " に CR がある"
assert hashlib.sha256(base["JA"].encode("utf-8")).hexdigest().upper().startswith("C5293C24D92C165E")
assert hashlib.sha256(base["EN"].encode("utf-8")).hexdigest().upper().startswith("1D289FF541D805C8")


def once(text, old, new, label):
    n = text.count(old)
    assert n == 1, "%s: 元の文字列が %d 回現れる" % (label, n)
    return text.replace(old, new)


def insert_after_line(text, start, line, label):
    lines = text.split("\n")
    hits = [i for i, x in enumerate(lines) if x.startswith(start)]
    assert len(hits) == 1, "%s: 行の頭 %r が %d 回" % (label, start, len(hits))
    assert line not in text, label + ": 足す行がすでにある"
    lines.insert(hits[0] + 1, line)
    return "\n".join(lines)


sys.path.insert(0, HERE)
from v5_9_changes import *  # noqa: F401,F403,E402（直しの中身——確かめる道具と同じもの）

out = {}
t = base["JA"]
for label, a, b in JA_R:
    t = once(t, a, b, "JA " + label)
t = insert_after_line(t, JA_C4_AFTER, JA_C4_LINE, "JA C4")
t = once(t, JA_DATE_END, JA_DATE_END + JA_DATE_ADD, "JA 日付の行")
t = once(t, JA_NOTE_ANCHOR, JA_NOTE_ANCHOR + JA_NOTE, "JA 注記")
out["JA"] = t
t = base["EN"]
for label, a, b in EN_R:
    t = once(t, a, b, "EN " + label)
t = insert_after_line(t, EN_C4_AFTER, EN_C4_LINE, "EN C4")
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
    sel = [(a, b) for label, a, b in R if label.split(" ")[0] == mark or label.startswith(mark + " ") or label.split(" ")[0].rstrip("ab") == mark]
    olds = [line_of(base[key], a) for a, b in sel]
    news = [line_of(out[key], b) for a, b in sel]
    return sorted(set(news)), sorted(set(olds))


fmt = lambda xs: "・".join("L%d" % x for x in xs)
rows = []
for mark, name in PLACES:
    jn, jo = lines_for(mark, JA_R, "JA")
    en, eo = lines_for(mark, EN_R, "EN")
    assert jn, mark + " 日の所が無い"
    en_part = ("英 %s〔%s〕" % (fmt(en), fmt(eo))) if en else "英は直さない"
    rows.append("\n  - %s %s（日 %s〔%s〕・%s）" % (mark, name, fmt(jn), fmt(jo), en_part))
rows.append("\n  - C4 補遺II 参考文献 Lynch ら（2026）（日 L%d・英 L%d に足した）" % (line_of(out["JA"], JA_C4_LINE[:60]), line_of(out["EN"], EN_C4_LINE[:60])))
sha16 = {k: hashlib.sha256(out[k].encode("utf-8")).hexdigest().upper()[:16] for k in ("JA", "EN")}
cl = base["CHANGELOG"]
assert cl.endswith("- [x] v5.8（JA・EN）の公開（2026-10-10・登録者の許可による）\n"), "CHANGELOG の末尾が想定と違う"
add = (CHANGELOG_ADD.replace("@@PLACES@@", "".join(rows)).replace("@@REVIEW@@", REVIEW).replace("@@PUBLISHED@@", PUBLISHED_LINE)
       .replace("@@JA@@", sha16["JA"]).replace("@@EN@@", sha16["EN"]))
out["CHANGELOG"] = cl + add
assert "@@" not in out["CHANGELOG"], "置き換えの残り"
for k, p in P.items():
    dst = os.path.join(STAGE, p.replace("/", os.sep))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with io.open(dst, "w", encoding="utf-8", newline="\n") as f:
        f.write(out[k])
    print("%-9s %s 行 %d → %d  SHA-256 %s" % (k, p.split("/")[-1], base[k].count("\n"), out[k].count("\n"),
                                              hashlib.sha256(out[k].encode("utf-8")).hexdigest().upper()))
print("".join(rows))
