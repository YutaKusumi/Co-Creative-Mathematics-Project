"""リポジトリに同梱する検分の記録（verification/v5.6-correction/）の写しを、手元の置き場に作る（README は別に書く）——v5.5 の stage_verification_v5_5.py の写し。

中身は変えずに写す（どれも LF・CR なし——写す前に確かめる）。v5.6 の経緯の抜粋は数えだけで、古い版の行を切り出していないので CR は無い（確かめる）。
狙いを定めた系統外の確かめ（十本目の動画の作業場 ../../21-v56-check/）と、十本目の動画の一巡目の系統外の検分の回答（逐語）も写す——
CHANGELOG の「発見の経緯」と「検分」の欄がその答えを引くため（登録者の裁定 2026-10-08 09:43——「入れて、合格なら push まで」）。
あわせて、公開してはいけないもの（チャットの URL・鍵の形・メールアドレス・伏せる語）が無いことを機械で探す。
"""
import hashlib
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "staging-verification-v5.6-correction")
os.makedirs(OUT, exist_ok=False)
items = [("01-source-correction-plan-v5.6.md", "01-source-correction-plan-v5.6.md")]
for n in ["00-preregistration.md", "request.txt", "instruction.txt", "diff-v5.6.txt", "excerpt-v5.6-JA.txt", "excerpt-v5.6-EN.txt",
          "excerpt-history.txt", "changelog-v5.6-entry.txt", "01-response-gemini-verbatim.md", "02-kensan.md"]:
    items.append(("02-v5.6-external-review/" + n, "02-v5.6-external-review/" + n))
# 動画の作業場の記録から——置き場の名前を替える
for n in ["00-preregistration.md", "request.txt", "source-excerpt-v56check.txt", "01-response-gemini-verbatim.md", "02-kensan.md"]:
    items.append(("../21-v56-check/" + n, "03-targeted-check/" + n))
items.append(("../18-external-review/01-response-gemini-verbatim.md", "04-video10-external-review-1-response-verbatim.md"))
for n in ["make_sixth_work_v5_6.py", "v5_6_changes.py", "verify_v5_6.py", "build_v5_6_review_package.py", "stage_verification_v5_6.py"]:
    items.append(("instruments/" + n, "instruments/" + n))
items.append(("../tools/make_v56check_excerpt10.py", "instruments/make_v56check_excerpt10.py"))
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
