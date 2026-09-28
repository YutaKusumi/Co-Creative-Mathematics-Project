"""v5 の F（登録者の裁定 2026-09-28：大日如来の指摘を受けて、「重要な留保」の中の引用を、直した本文に揃える）。
日英 v5 の四か所だけを置き換える。各置き換えは元の文字列がちょうど一回あることを確かめ、一つでも外れたら何も書かない。"""
import hashlib
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
B = r"C:\Users\PC\Desktop\GitHub-Repositories\Co-Creative-Mathematics-Project\06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned\Version-B-Policy-Edition"
F = {"JA": B + r"\JA\Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-JA.md",
     "EN": B + r"\EN\Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-EN.md"}
SHA_BEFORE = {"JA": "7B501337B087595FC4969C1C05EF8C767CD5EB7B93A3C1DFB7CA3377F16628BC",
              "EN": "3DED469A1A98C1DDD47DEF15D9F777E3507842A8A76D379EF58F9938F786D599"}
R = {
    "JA": [("以下の「有限時間 T* で発散する」は、復元力を省いた極限での挙動であり",
            "以下の「遅くとも有限時間 T* までに発散する」は、復元力を省いた極限での挙動であり"),
           ("ゆえに、以下の「有限時間 $T^\\ast{}$ で発散」は、",
            "ゆえに、以下の「有限時間 $T^\\ast{}$ までの発散」は、")],
    "EN": [('Hence the "diverges at a finite time T*" below is the behavior',
            'Hence the "diverges no later than a finite time T*" below is the behavior'),
           ('Therefore the "divergence in finite time $T^\\ast$" below is the limiting behavior',
            'Therefore the "divergence no later than a finite time $T^\\ast$" below is the limiting behavior')],
}
out = {}
for lang, path in F.items():
    raw = open(path, "rb").read()
    if hashlib.sha256(raw).hexdigest().upper() != SHA_BEFORE[lang]:
        raise SystemExit("%s: v5 の SHA が想定と違う——止める" % lang)
    t = raw.decode("utf-8")
    for old, new in R[lang]:
        n = t.count(old)
        if n != 1:
            raise SystemExit("%s: 元の文字列が %d 回（1 回であるべき）: %s" % (lang, n, old[:30]))
        t = t.replace(old, new)
    out[lang] = t.encode("utf-8")
for lang, path in F.items():
    open(path, "wb").write(out[lang])
    print(lang, "SHA-256:", hashlib.sha256(out[lang]).hexdigest().upper(), "バイト:", len(out[lang]))
