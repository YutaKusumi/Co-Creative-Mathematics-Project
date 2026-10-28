"""リポジトリに同梱する検分の記録（verification/v5.9-correction/）の写しを、手元の置き場に作る（README は別に書く）——v5.8 の stage_verification_v5_8.py の写し。

中身は変えずに写す（どれも LF・CR なし——写す前に確かめる）。
計画・言い回しの案・文献の確かめ・組み立ての記録・同じ型の洗い直しの出力・系統外の検分の束と回答と検算・道具を写す。
文献の一次の資料（Bostrom 2012 の PDF）とそこから取り出した字は写さない（他者の著作物——確かめの記録 03 に指紋だけを書いた）。
あわせて、公開してはいけないもの（チャットの URL・鍵の形・メールアドレス・伏せる語）が無いことを機械で探す。
"""
import hashlib
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "staging-verification-v5.9-correction")
os.makedirs(OUT, exist_ok=False)
items = [("00-candidates-and-plan.md", "01-candidates-and-plan.md"),
         ("01-sweeps-v5.8.txt", "02-sweeps-v5.8.txt"),
         ("02-wording-proposals.md", "03-wording-proposals.md"),
         ("03-literature-check.md", "04-literature-check.md"),
         ("04-build-record.md", "05-build-record.md")]
for n in ["00-preregistration.md", "request.txt", "instruction.txt", "diff-v5.9.txt", "excerpt-v5.9-JA.txt", "excerpt-v5.9-EN.txt",
          "excerpt-history.txt", "changelog-v5.9-entry.txt", "01-response-gemini-verbatim.md", "02-kensan.md"]:
    items.append(("05-v5.9-external-review/" + n, "06-v5.9-external-review/" + n))
for n in ["v5_9_changes.py", "make_sixth_work_v5_9.py", "verify_v5_9.py", "build_v5_9_review_package.py", "sweep_v59.py", "stage_verification_v5_9.py"]:
    items.append(("tools/" + n, "instruments/" + n))
BAD = [re.compile(rb"aistudio\.google\.com/prompts/"), re.compile(rb"colab\.research\.google\.com/drive/"), re.compile(rb"AIza[0-9A-Za-z_\-]{20,}"),
       re.compile(rb"sk-or-[0-9A-Za-z_\-]{20,}"), re.compile(rb"[A-Za-z0-9._%+\-]+@gmail\.com"), re.compile(rb"green\.green"),
       re.compile(("C" + "S" + "6" + "0").encode("utf-8")), re.compile(("加" + "持").encode("utf-8"))]  # 伏せる語は字を分けて書く（この道具も公開するので）
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
