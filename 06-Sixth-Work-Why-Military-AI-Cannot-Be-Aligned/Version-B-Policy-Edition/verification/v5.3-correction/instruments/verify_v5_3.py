"""v5.3 の合格条件を機械で確かめる（計画書 §4 の 2）。

1. v5 の日英：HEAD との差分が、決めた 4 か所（日付の行・v5.2 の注記の後への v5.3 の注記の挿入・§5-2a の一文・§11-2a の一文）の範囲だけ。行数 +2
2. README：三か所（L31・L108・L121）だけ。build.sh：二か所（L317・L325）だけ。CHANGELOG：末尾への追加だけ
3. Git の変更は 5 ファイルだけ・何も加えていない（ステージが空）
4. 直した二つの一文の中身（§5-2a は「定理」→「命題」の一語だけ・§11-2a は参照の括弧の中だけ）を、語の単位で確かめる
あわせて、人の目で読むための差分を ../build/v5.3-diff.txt に書き出す（上書きしない）。
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
    "JA": [(15, 15), (42, 42), (918, 918), (1890, 1890)],
    "EN": [(17, 17), (44, 44), (920, 920), (1891, 1891)],
    "CHANGELOG": [(283, 283)],  # 末尾（HEAD の 281 行の後・split の最後の空の要素の後）への追加
    "BUILD": [(317, 317), (325, 325)],
    "README": [(31, 31), (108, 108), (121, 121)],
}
DELTA = {"JA": 2, "EN": 2, "BUILD": 0, "README": 0, "CHANGELOG": 18}  # 系統外の確かめの後：「検分」の一段（+2）
# 一文の中の語の違い（difflib で文字の単位）——決めた違いだけ
SENT = {
    ("JA", 918): [("replace", "定理", "命題")],
    ("EN", 920): [("replace", "theorem.", "proposition.")],
    ("JA", 1890): [("insert", "", "・附録J-4-1")],
    ("EN", 1891): [("replace", "J-2-1)", "J-2-1, Appendix J-4-1)")],
}


def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args), capture_output=True, check=True).stdout


def char_ops(a, b, words=False):
    # 日本語は文字の単位・英語は語の単位（空白で分ける——文字の単位では theorem と proposition の共通の字で細切れになる・一回目の試走で見た）
    if words:
        a, b = a.split(" "), b.split(" ")
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    j = " ".join if words else "".join
    return [(tag, j(a[i1:i2]), j(b[j1:j2])) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != "equal"]


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
            if tag == "replace" and (k, lo) in SENT:
                if i2 - i1 != 1 or j2 - j1 != 1:
                    bad.append(("一文の差し替えが一行でない", lo))
                else:
                    ops = char_ops(a[i1], b[j1], words=(k == "EN"))
                    good_s = ops == SENT[(k, lo)]
                    print("  %s L%d の中の違い：%s %s" % (k, lo, ops, "（決めたとおり）" if good_s else "★決めと違う"))
                    ok &= good_s
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
    dst = os.path.join(ROOT, "build", "v5.3-diff.txt")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with io.open(dst, "x", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out) + "\n")
    print("差分 → %s" % dst)
    print("合格" if ok else "不合格")


if __name__ == "__main__":
    main()
