"""訂正案（N1・N2・X5）の文書を、雛形に原典の逐語を機械で差し込んで作る。

雛形の中の {{Q:KEY:a-b}} を、リポジトリの HEAD のファイル KEY の a〜b 行（そのまま）で置き換え、
コードブロックに包む。{{SHA:KEY}} は HEAD のそのファイルの SHA-256（LF のまま）。{{HEAD}} はコミット。
引用を手で打たないため（大日如来の覚え書き「引用をタイプしない」）。
使い方: python tools/build_correction_plan.py
"""
import hashlib
import io
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = r"C:\Users\PC\Desktop\GitHub-Repositories\Co-Creative-Mathematics-Project"
SIX = "06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned/Version-B-Policy-Edition"
V10 = "toy-model-verification/06-sixth-work-contradiction-and-collapse"
FILES = {
    "JA": SIX + "/JA/Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-JA.md",
    "EN": SIX + "/EN/Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-EN.md",
    "JAV1": SIX + "/JA/Why-Military-AI-Cannot-Be-Aligned-Version-B-JA.md",
    "FIGJA": V10 + "/figures/verification-10-collapse-figures-JA.html",
    "FIGEN": V10 + "/figures/verification-10-collapse-figures-EN.html",
    "DESIGN": V10 + "/collapse/toymodel_collapse_design_A.md",
    "SCRIPT": V10 + "/collapse/collapse_prototype_A.mjs",
}
TEMPLATE = os.path.join(ROOT, "11-source-correction-plan-N1-N2-X5.template.md")
OUT = os.path.join(ROOT, "11-source-correction-plan-N1-N2-X5.md")


def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args), capture_output=True, check=True).stdout


# 訂正の前の版（8f69ea0）に固定する——v5.1 の公開（c7e86e2）の後も、「現行」の引用が訂正前の文を指すように
head = git("rev-parse", "--short", "8f69ea0").decode().strip()
blobs = {k: git("show", "8f69ea0:" + p) for k, p in FILES.items()}
lines = {k: b.decode("utf-8").split("\n") for k, b in blobs.items()}
shas = {k: hashlib.sha256(b).hexdigest().upper() for k, b in blobs.items()}

tpl = io.open(TEMPLATE, encoding="utf-8").read()


def quote(m):
    key, a, b = m.group(1), int(m.group(2)), int(m.group(3) or m.group(2))
    body = "\n".join(lines[key][a - 1:b])
    rng = ("L%d" % a) if a == b else ("L%d〜%d" % (a, b))
    return "`%s` %s（訂正前のコミット `%s`・機械で抜き出し）\n```text\n%s\n```" % (FILES[key].split("/")[-1], rng, head, body)


out = re.sub(r"\{\{Q:([A-Z0-9]+):(\d+)(?:-(\d+))?\}\}", quote, tpl)
out = re.sub(r"\{\{SHA:([A-Z0-9]+)\}\}", lambda m: shas[m.group(1)], out)
out = out.replace("{{HEAD}}", head)
left = re.findall(r"\{\{[^}]*\}\}", out)
assert not left, left
io.open(OUT, "w", encoding="utf-8", newline="\n").write(out)
print("wrote", OUT, len(out), "chars; HEAD", head)
for k in FILES:
    print(" ", k, shas[k][:16], len(lines[k]), "lines")
