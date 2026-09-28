"""v5.1 の合格条件 1〜4 を機械で確かめる（計画書 §8）。

1. v5 の日英：HEAD との差分が、決めた 5 か所（日付の行・v5 の注記の後・§4-3b の一文・§I-2a の段・段階二の一文）の範囲だけ。行数 +4
2. 図のページの日英：L42 と末尾（</main> の前）の 2 か所だけ。行数 +1
3. Git の変更は 7 ファイルだけ
4. 何も加えていない（ステージが空）
あわせて、人の目で読むための差分を build/v5.1-diff.txt に書き出す。
"""
import difflib
import io
import os
import subprocess

REPO = r"C:\Users\PC\Desktop\GitHub-Repositories\Co-Creative-Mathematics-Project"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIX = "06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned/Version-B-Policy-Edition"
V10 = "toy-model-verification/06-sixth-work-contradiction-and-collapse/figures"
FILES = {
    "JA": SIX + "/JA/Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-JA.md",
    "EN": SIX + "/EN/Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-EN.md",
    "FIGJA": V10 + "/verification-10-collapse-figures-JA.html",
    "FIGEN": V10 + "/verification-10-collapse-figures-EN.html",
    "CHANGELOG": SIX + "/CHANGELOG.md",
    "BUILD": ".github/scripts/build.sh",
    "README": "README.md",
}
# 変えてよい範囲（HEAD の行番号・1 始まり・両端を含む）。挿入は「その行の前に入る」位置で表す
ALLOWED = {
    "JA": [(15, 15), (38, 38), (762, 762), (3634, 3650), (3685, 3685)],
    "EN": [(17, 17), (40, 40), (763, 763), (3684, 3700), (3735, 3735)],
    "FIGJA": [(42, 42), (60, 60)],
    "FIGEN": [(42, 42), (60, 60)],
    "CHANGELOG": [(241, 242)],
    "BUILD": [(317, 317), (325, 325)],
    "README": [(31, 31), (108, 108), (121, 121)],
}
DELTA = {"JA": 4, "EN": 4, "FIGJA": 1, "FIGEN": 1, "BUILD": 0, "README": 0}


def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args), capture_output=True, check=True).stdout


ok = True
report = []
for k, p in FILES.items():
    old = git("show", "HEAD:" + p).decode("utf-8").split("\n")
    new = io.open(os.path.join(REPO, p.replace("/", os.sep)), encoding="utf-8", newline="").read()
    assert "\r" not in new, k + " に CR"
    ctrl = sorted({hex(ord(c)) for c in new if ord(c) < 32 and c not in "\n\t"})
    if ctrl:
        ok = False
        print(k, "に制御文字:", ctrl)
    new = new.split("\n")
    ops = [o for o in difflib.SequenceMatcher(None, old, new, autojunk=False).get_opcodes() if o[0] != "equal"]
    touched = set()
    bad = []
    for tag, i1, i2, j1, j2 in ops:
        a, b = i1 + 1, max(i1 + 1, i2)  # 挿入（i1 == i2）は i1+1 の行の前
        hit = [r for r in ALLOWED[k] if r[0] <= a and b <= r[1]]
        if hit:
            touched.update(hit)
        else:
            bad.append((tag, a, b))
    untouched = [r for r in ALLOWED[k] if r not in touched]
    d = len(new) - len(old)
    dok = (k not in DELTA) or DELTA[k] == d
    line = "%-9s 範囲 %d/%d に変更・範囲の外の変更 %d・行数 %+d%s" % (
        k, len(touched), len(ALLOWED[k]), len(bad), d, "" if dok else "（想定と違う）")
    print(line)
    if bad or untouched or not dok:
        ok = False
        print("   範囲の外:", bad, " 触れていない範囲:", untouched)
    report.append("=" * 20 + " " + p + "\n" + "\n".join(difflib.unified_diff(old, new, "HEAD", "work", n=1, lineterm="")))

status = [l for l in git("status", "--porcelain").decode("utf-8").split("\n") if l and not l.startswith("??")]
print("Git の変更（追跡中）:", len(status))
for l in status:
    print("  ", l)
changed = {l[3:] for l in status}
if changed != set(FILES.values()):
    ok = False
    print("  想定の 7 ファイルと一致しない:", changed ^ set(FILES.values()))
staged = git("diff", "--cached", "--name-only").decode().strip()
print("ステージ:", "空" if not staged else staged)
if staged:
    ok = False
out = os.path.join(ROOT, "build", "v5.1-diff.txt")
io.open(out, "w", encoding="utf-8", newline="\n").write("\n".join(report) + "\n")
print("差分:", out)
print("合格" if ok else "不合格")
