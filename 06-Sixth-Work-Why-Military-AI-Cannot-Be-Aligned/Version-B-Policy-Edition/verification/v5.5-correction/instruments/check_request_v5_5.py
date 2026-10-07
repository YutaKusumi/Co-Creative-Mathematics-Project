"""v5.5 の依頼文の中の引用（「…」）が、原典の実物（HEAD の v5.4・作業木の v5.5 の案）か束の中にあることを機械で確かめる（v5.4 の check_request_v5_4.py の写し）。
- 依頼文の「…」の中身を一つずつ取り出し、『』を「」に戻し、「…」を任意の字の並びとして、日本語版（v5.3・v5.4）・束の抜粋のどこかにあるかを探す
- 依頼文が挙げる節の名（§x-y）が、v5.5 の日本語版の見出しにあるか
- 依頼文が挙げる添付の名が、束のフォルダにあるか
"""
import hashlib
import io
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
REPO = r"C:\Users\PC\Desktop\GitHub-Repositories\Co-Creative-Mathematics-Project"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PKG = os.path.join(ROOT, "02-v5.5-external-review")
SIX = "06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned/Version-B-Policy-Edition"
JA = SIX + "/JA/Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-JA.md"
# 依頼文の中の、原典の引用ではない「…」（題・語の並び・作業の言い方）——引用として照らさない
NOT_QUOTE = {"訂正", "問題なし", "見つからなかった", "このまま公開してよい", "修正すれば公開してよい", "公開すべきでない",
             "一般知識による", "確かめていない", "-", "+", "不変", "根本的に危険"}  # 「根本的に危険」は本文では強調の印つき（**根本的に危険**）


def git_show(p):
    return subprocess.run(["git", "-C", REPO, "show", "HEAD:" + p], capture_output=True, check=True).stdout.decode("utf-8")


texts = {"v5.4 日": git_show(JA), "v5.5 日": io.open(os.path.join(REPO, JA), encoding="utf-8").read()}
for n in os.listdir(PKG):
    if n.endswith(".txt") and n != "request.txt":
        texts["束 " + n] = io.open(os.path.join(PKG, n), encoding="utf-8").read()
req = io.open(os.path.join(PKG, "request.txt"), encoding="utf-8").read()
ok = True
# 「…」の中身（入れ子の『』を含む）
quotes = re.findall(r"「([^「」]+)」", req)
for q in quotes:
    if q in NOT_QUOTE:
        continue
    q2 = q.replace("『", "「").replace("』", "」")
    parts = [re.escape(x) for x in q2.split("…")]
    rx = re.compile("[^\n]*?".join(parts))
    where = [k for k, t in texts.items() if rx.search(t)]
    good = bool(where)
    ok &= good
    print("「%s」：%s" % (q[:50], ("ある（%s）" % "・".join(where[:3])) if good else "★無い"))
# 節の名
heads = set(re.findall(r"^#{2,4} (\d+-\d+[a-z]?|[A-Z]-\d+[a-z]?)　", texts["v5.5 日"], re.M))
for s in sorted(set(re.findall(r"§(\d+-\d+[a-z]?)", req))):
    good = s in heads
    ok &= good
    print("§%s：%s" % (s, "見出しにある" if good else "★見出しに無い"))
for s in sorted(set(re.findall(r"附録C-(\d[a-z]?)", req))):
    good = ("C-" + s) in heads
    ok &= good
    print("附録C-%s：%s" % (s, "見出しにある" if good else "★見出しに無い"))
# 添付の名
for n in re.findall(r"([a-z0-9.\-]+\.txt)", req):
    good = os.path.exists(os.path.join(PKG, n))
    ok &= good
    print("添付 %s：%s" % (n, "ある" if good else "★無い"))
raw = io.open(os.path.join(PKG, "request.txt"), "rb").read()
print("依頼文 %d 字・%d バイト・SHA-256 %s" % (len(raw.decode("utf-8")), len(raw), hashlib.sha256(raw).hexdigest().upper()))
print("合格" if ok else "不合格")
