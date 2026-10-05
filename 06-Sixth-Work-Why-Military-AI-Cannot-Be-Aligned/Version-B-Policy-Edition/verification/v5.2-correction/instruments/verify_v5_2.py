"""v5.2 の合格条件を機械で確かめる（計画書 §4 の 2）。

1. v5 の日英：HEAD との差分が、決めた 3 か所（日付の行・§3-3d の一文・v5.1 の注記の後への v5.2 の注記の挿入）の範囲だけ。行数 +2
2. README：三か所（L31・L108・L121）だけ。build.sh：二か所（L317・L325）だけ。CHANGELOG：末尾への追加だけ
3. Git の変更は 5 ファイルだけ・何も加えていない（ステージが空）
あわせて、人の目で読むための差分を ../build/v5.2-diff.txt に書き出す（上書きしない）。
"""
import difflib
import io
import os
import subprocess

REPO = r"C:\Users\PC\Desktop\GitHub-Repositories\Co-Creative-Mathematics-Project"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIX = "06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned/Version-B-Policy-Edition"
FILES = {
    "JA": SIX + "/JA/Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-JA.md",
    "EN": SIX + "/EN/Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-EN.md",
    "CHANGELOG": SIX + "/CHANGELOG.md",
    "BUILD": ".github/scripts/build.sh",
    "README": "README.md",
}
# 変えてよい範囲（HEAD の行番号・1 始まり・両端を含む）。挿入は「その行の前に入る」位置で表す
ALLOWED = {
    "JA": [(15, 15), (40, 40), (615, 615)],
    "EN": [(17, 17), (42, 42), (615, 615)],
    "CHANGELOG": [(264, 264)],  # 末尾（HEAD の 262 行の後・split の最後の空の要素の前）への追加
    "BUILD": [(317, 317), (325, 325)],
    "README": [(31, 31), (108, 108), (121, 121)],
}
DELTA = {"JA": 2, "EN": 2, "BUILD": 0, "README": 0, "CHANGELOG": 19}  # 系統外の確かめの後：将来の改訂の候補の一段（+2）


def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args), capture_output=True, check=True).stdout


def main():
    ok = True
    out = []
    for k, p in FILES.items():
        a = git("show", "HEAD:" + p).decode("utf-8").split("\n")
        b = io.open(os.path.join(REPO, p), encoding="utf-8").read().split("\n")
        sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
        bad = []
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal":
                continue
            lo, hi = i1 + 1, max(i1 + 1, i2)  # 挿入（i1 == i2）は「i1+1 行の前」
            if not any(x <= lo and hi <= y for x, y in ALLOWED[k]):
                bad.append((tag, lo, hi))
            out.append("==== %s %s HEAD %d-%d → 作業木 %d-%d" % (k, tag, i1 + 1, i2, j1 + 1, j2))
            for line in a[i1:i2]:
                out.append("- " + line)
            for line in b[j1:j2]:
                out.append("+ " + line)
        d = len(b) - len(a)
        good = not bad and d == DELTA[k]
        ok &= good
        print("%-9s 差分の範囲 %s・行数の差 %+d（決め %+d）%s" % (k, "決めたとおり" if not bad else "外れ %s" % bad, d, DELTA[k], "" if good else "  ★不合格"))
    st = git("status", "--porcelain").decode("utf-8").splitlines()
    tracked = [s for s in st if not s.startswith("??")]
    staged = [s for s in tracked if s[0] not in " ?"]
    print("Git の変更（追跡済み）%d ファイル・ステージ %d" % (len(tracked), len(staged)))
    ok &= len(tracked) == 5 and not staged
    dst = os.path.join(ROOT, "build", "v5.2-diff.txt")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with io.open(dst, "x", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out) + "\n")
    print("差分 → %s" % os.path.relpath(dst, REPO))
    print("合格" if ok else "不合格")


if __name__ == "__main__":
    main()
