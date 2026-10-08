"""リポジトリに同梱する検分の記録（verification/v5.7-correction/）の写しを、手元の置き場に作る（README は別に書く）——v5.6 の stage_verification_v5_6.py の写し。

中身は変えずに写す（どれも LF・CR なし——写す前に確かめる）。
十一本目の動画の一巡目の系統外の検分の回答（逐語）も写す——CHANGELOG の「発見の経緯」がその答え（§9-7a の一文目に触れなかったこと）を引くため
（v5.6 の前例と同じく回答だけ——動画の作業場の検算の記録は写さない）。
あわせて、公開してはいけないもの（チャットの URL・鍵の形・メールアドレス・伏せる語）が無いことを機械で探す。
"""
import hashlib
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "staging-verification-v5.7-correction")
os.makedirs(OUT, exist_ok=False)
items = [("01-source-correction-plan-v5.7.md", "01-source-correction-plan-v5.7.md")]
for n in ["00-preregistration.md", "request.txt", "instruction.txt", "diff-v5.7.txt", "excerpt-v5.7-JA.txt", "excerpt-v5.7-EN.txt",
          "excerpt-history.txt", "changelog-v5.7-entry.txt", "01-response-gemini-verbatim.md", "02-kensan.md"]:
    items.append(("02-v5.7-external-review/" + n, "02-v5.7-external-review/" + n))
# 動画の作業場の記録から——置き場の名前を替える
items.append(("../18-external-review/01-response-gemini-verbatim.md", "03-video11-external-review-1-response-verbatim.md"))
for n in ["make_sixth_work_v5_7.py", "v5_7_changes.py", "verify_v5_7.py", "build_v5_7_review_package.py", "stage_verification_v5_7.py"]:
    items.append(("instruments/" + n, "instruments/" + n))
BAD = [re.compile(rb"aistudio\.google\.com/prompts/"), re.compile(rb"colab\.research\.google\.com/drive/"), re.compile(rb"AIza[0-9A-Za-z_\-]{20,}"),
       re.compile(rb"[A-Za-z0-9._%+\-]+@gmail\.com"), re.compile(rb"green\.green"), re.compile(("C" + "S" + "6" + "0").encode("utf-8"))]  # 伏せる語は字を分けて書く（この道具も公開するので）
CR = b"\r"


def sha(b):
    return hashlib.sha256(b).hexdigest().upper()


for src, dst in items:
    s = os.path.normpath(os.path.join(ROOT, src.replace("/", os.sep)))
    d = os.path.join(OUT, dst.replace("/", os.sep))
    os.makedirs(os.path.dirname(d), exist_ok=True)
    b = open(s, "rb").read()
    assert CR not in b, src + " に CR がある"
    print("%-62s %s  %7d B" % (dst, sha(b)[:16], len(b)))
    hits = [p.pattern for p in BAD if p.search(b)]
    assert not hits, (src, hits)
    with open(d, "xb") as f:
        f.write(b)
print("計 %d ファイル → %s" % (len(items), OUT))
