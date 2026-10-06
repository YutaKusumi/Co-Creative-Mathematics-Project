"""リポジトリに同梱する検分の記録（verification/v5.3-correction/）の写しを、手元の置き場に作る（README は commit の後に書く）。

excerpt-history.txt は、古い版の作業木の写し（CRLF）から切り出した行の末尾に CR が残っている（送った写し）——v5.2 と同じく、
同梱の写しでは CR を除いた LF に揃え、両方の指紋を出す。ほかのファイルはそのまま写す（中身を変えない）。
"""
import hashlib
import io
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "staging-verification-v5.3-correction")
os.makedirs(OUT, exist_ok=False)
items = [
    ("01-source-correction-plan-v5.3.md", "01-source-correction-plan-v5.3.md"),
]
for n in ["00-preregistration.md", "request.txt", "instruction.txt", "diff-v5.3.txt", "excerpt-v5.3-JA.txt", "excerpt-v5.3-EN.txt",
          "excerpt-history.txt", "changelog-v5.3-entry.txt", "01-response-gemini-verbatim.md", "02-kensan.md"]:
    items.append(("02-v5.3-external-review/" + n, "02-v5.3-external-review/" + n))
for n in ["make_sixth_work_v5_3.py", "verify_v5_3.py", "build_v5_3_review_package.py", "check_request_v5_3.py", "stage_verification_v5_3.py"]:
    items.append(("instruments/" + n, "instruments/" + n))


def sha(b):
    return hashlib.sha256(b).hexdigest().upper()


for src, dst in items:
    s = os.path.join(ROOT, src.replace("/", os.sep))
    d = os.path.join(OUT, dst.replace("/", os.sep))
    os.makedirs(os.path.dirname(d), exist_ok=True)
    b = open(s, "rb").read()
    if dst.endswith("excerpt-history.txt"):
        lf = b.replace(b"\r\n", b"\n").replace(b"\r", b"")
        with open(d, "xb") as f:
            f.write(lf)
        print("%-55s 送った写し %s（%d B・CR %d）→ LF %s（%d B）" % (dst, sha(b)[:16], len(b), b.count(b"\r"), sha(lf)[:16], len(lf)))
    else:
        assert b"\r" not in b, dst + " に CR がある"
        with open(d, "xb") as f:
            f.write(b)
        print("%-55s %s  %7d B" % (dst, sha(b)[:16], len(b)))
