"""v5 の X1a（系統外検分の指摘・登録者の裁定 2026-09-28）：§4-3b の「重要な留保」の中の「以下の」→「上の」（JA）、
"below" → "above"（EN）。引用している本文（JA L768・EN L769）が留保の段落の上にあるため。附録 A-4b の留保は変えない。"""
import hashlib
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
B = r"C:\Users\PC\Desktop\GitHub-Repositories\Co-Creative-Mathematics-Project\06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned\Version-B-Policy-Edition"
F = {"JA": B + r"\JA\Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-JA.md",
     "EN": B + r"\EN\Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-EN.md"}
SHA_BEFORE = {"JA": "7FD0B7CEE8F8B4B20239048F0DA007799FD5F7022B41937FD24177F9E0C35BBD",
              "EN": "72155C5A096685F3BAFA9E1E3337C5766CFF8215FC7E1619C7BE13A6F7C7E07D"}
R = {"JA": ("ゆえに、以下の「遅くとも有限時間 T* までに発散する」は、", "ゆえに、上の「遅くとも有限時間 T* までに発散する」は、"),
     "EN": ('Hence the "diverges no later than a finite time T*" below is the behavior',
            'Hence the "diverges no later than a finite time T*" above is the behavior')}
out = {}
for lang, path in F.items():
    raw = open(path, "rb").read()
    if hashlib.sha256(raw).hexdigest().upper() != SHA_BEFORE[lang]:
        raise SystemExit("%s: v5 の SHA が想定と違う——止める" % lang)
    t = raw.decode("utf-8")
    old, new = R[lang]
    if t.count(old) != 1:
        raise SystemExit("%s: 元の文字列が %d 回" % (lang, t.count(old)))
    out[lang] = t.replace(old, new).encode("utf-8")
for lang, path in F.items():
    open(path, "wb").write(out[lang])
    print(lang, "SHA-256:", hashlib.sha256(out[lang]).hexdigest().upper(), "バイト:", len(out[lang]))
