"""段階二の直し（v5.1 第三案）を、系統外の新しいチャットで確かめるための抜粋を作る（機械で切り出す）。

- 改訂案（作業木の第三案）：附録I §I-2a と §I-3a・§I-3b（日英）
- 現行版（HEAD 8f69ea0 の v5）：段階二の一行（日英）
出力：16-v5.1-stage2-recheck/stage2-excerpt.txt（依頼文と事前登録は別に書く）
"""
import hashlib
import io
import os
import subprocess

REPO = r"C:\Users\PC\Desktop\GitHub-Repositories\Co-Creative-Mathematics-Project"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "16-v5.1-stage2-recheck")
SIX = "06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned/Version-B-Policy-Edition"
BOOK = {"JA": SIX + "/JA/Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-JA.md",
        "EN": SIX + "/EN/Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-EN.md"}
os.makedirs(OUT, exist_ok=True)


def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args), capture_output=True, check=True).stdout


def sha(t):
    return hashlib.sha256(t.encode("utf-8")).hexdigest().upper()


def block(L, a, b):
    out = ["==== L%d〜L%d ====" % (a, b)]
    out += ["L%d | %s" % (i, L[i - 1]) for i in range(a, b + 1) if L[i - 1].strip()]
    return out


def find(L, prefix, start=1):
    return next(i for i in range(start, len(L) + 1) if L[i - 1].startswith(prefix))


head = git("rev-parse", "--short", "HEAD").decode().strip()
lines = ["段階二の検分のための抜粋（機械で切り出したもの・手で打ったものではない）", ""]
for lang in ("JA", "EN"):
    new = io.open(os.path.join(REPO, BOOK[lang].replace("/", os.sep)), encoding="utf-8", newline="").read()
    L = new.split("\n")
    lines.append("######## 改訂案（未公開）・%s 版  元ファイル: %s  SHA-256(LF) = %s" % (lang, BOOK[lang].split("/")[-1], sha(new)))
    lines.append("各行の先頭の L#### は改訂案のファイルの行番号。空行は省いた。")
    a = find(L, "### I-2a"); b = find(L, "### I-2b", a)
    lines += block(L, a, b - 1)
    a = find(L, "## I-3"); b = find(L, "### I-3c", a)
    lines += block(L, a, b - 1)
    lines.append("")
for lang in ("JA", "EN"):
    old = git("show", "HEAD:" + BOOK[lang]).decode("utf-8")
    L = old.split("\n")
    key = "**段階二" if lang == "JA" else "**Stage two"
    i = find(L, key)
    lines.append("######## 現行版（公開中の v5・HEAD %s）・%s 版の段階二  SHA-256(LF) = %s" % (head, lang, sha(old)))
    lines += block(L, i, i)
    lines.append("")
text = "\n".join(lines)
path = os.path.join(OUT, "stage2-excerpt.txt")
io.open(path, "w", encoding="utf-8", newline="\n").write(text)
print("wrote", path, len(text.encode("utf-8")), "bytes", sha(text)[:16])
