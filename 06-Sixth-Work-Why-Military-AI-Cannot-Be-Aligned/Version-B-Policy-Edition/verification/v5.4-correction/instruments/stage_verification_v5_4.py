"""リポジトリに同梱する検分の記録（verification/v5.4-correction/）の写しを、手元の置き場に作る（README は別に書く）。

中身は変えずに写す（どれも LF・CR なし——写す前に確かめる）。ただし sweep-v5.3-negations.txt は、Windows の標準出力から
書いたので CRLF——LF にそろえて写し、両方の指紋を出す（v5.3 の経緯の抜粋と同じ扱い）。あわせて、公開してはいけないもの
（チャットの URL・鍵の形・メールアドレス・伏せる語）が無いことを機械で探す。
"""
import hashlib
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "staging-verification-v5.4-correction")
os.makedirs(OUT, exist_ok=False)
items = ["01-source-correction-plan-v5.4.md", "sweep-v5.3-negations.txt"]
for n in ["00-preregistration.md", "request.txt", "instruction.txt", "diff-v5.4.txt", "excerpt-v5.4-JA.txt", "excerpt-v5.4-EN.txt",
          "excerpt-history.txt", "changelog-v5.4-entry.txt", "01-response-gemini-verbatim.md", "02-kensan.md"]:
    items.append("02-v5.4-external-review/" + n)
for n in ["make_sixth_work_v5_4.py", "v5_4_changes.py", "verify_v5_4.py", "build_v5_4_review_package.py", "check_request_v5_4.py",
          "stage_verification_v5_4.py"]:
    items.append("instruments/" + n)
LF_FIX = {"sweep-v5.3-negations.txt", "02-v5.4-external-review/excerpt-history.txt"}  # 経緯の抜粋は古い版の作業木の写し（CRLF）から切り出した行の末尾に CR が残る——v5.3 と同じ
BAD = [re.compile(rb"aistudio\.google\.com/prompts/"), re.compile(rb"colab\.research\.google\.com/drive/"), re.compile(rb"AIza[0-9A-Za-z_\-]{20,}"),
       re.compile(rb"[A-Za-z0-9._%+\-]+@gmail\.com"), re.compile(rb"green\.green"), re.compile(("C" + "S" + "6" + "0").encode("utf-8"))]  # 伏せる語は字を分けて書く（この道具も公開するので）
CR = b"\r"


def sha(b):
    return hashlib.sha256(b).hexdigest().upper()


for rel in items:
    s = os.path.join(ROOT, rel.replace("/", os.sep))
    d = os.path.join(OUT, rel.replace("/", os.sep))
    os.makedirs(os.path.dirname(d), exist_ok=True)
    b = open(s, "rb").read()
    if rel in LF_FIX:
        lf = b.replace(CR + b"\n", b"\n").replace(CR, b"")  # 行の途中に残る CR（抜粋の切り出しの中）も除く——v5.3 と同じ
        assert CR not in lf
        print("%-56s 手元 %s（%d B・CR %d）→ LF %s（%d B）" % (rel, sha(b)[:16], len(b), b.count(CR), sha(lf)[:16], len(lf)))
        b = lf
    else:
        assert CR not in b, rel + " に CR がある"
        print("%-56s %s  %7d B" % (rel, sha(b)[:16], len(b)))
    hits = [p.pattern for p in BAD if p.search(b)]
    assert not hits, (rel, hits)
    with open(d, "xb") as f:
        f.write(b)
