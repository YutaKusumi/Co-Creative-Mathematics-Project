# -*- coding: utf-8 -*-
"""原典 v5.8（日英）で、v5.9 の直しの候補と同じ型の言い方を全文から探す（読むだけ）。
候補ごとに、日英の正規表現に当たる行の番号と、当たった所の前後（行の終わりまで読むため、当たりごとに前後 60 字）を書き出す。
使い方: python sweep_v59.py <出力ファイル>"""
import hashlib
import io
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Users\PC\Desktop\GitHub-Repositories\Co-Creative-Mathematics-Project\06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned\Version-B-Policy-Edition"
PJ = R + r"\JA\Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-JA.md"
PE = R + r"\EN\Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-EN.md"
bj, be = open(PJ, "rb").read(), open(PE, "rb").read()
assert hashlib.sha256(bj).hexdigest().upper().startswith("C5293C24D92C165E")
assert hashlib.sha256(be).hexdigest().upper().startswith("1D289FF541D805C8")
JA, EN = bj.decode("utf-8").split("\n"), be.decode("utf-8").split("\n")

# (候補, 日の型, 英の型, 範囲〔行の番号の下限・上限——None は全文〕)
SWEEPS = [
    ("A1", r"四つの想定|四つの.{0,12}反論", r"four anticipated|four .{0,30}objections|as well as a fifth", None),
    ("A2", r"Nash均衡", r"Nash equilibri", None),
    ("A3", r"構造的に回避", r"structurally avoid", None),
    ("A4", r"信頼性の高い防衛|防衛力を提供", r"reliable defen|provides? .{0,40}defen", None),
    ("A5", r"最も確実", r"most reliable|most certain|surest", None),
    ("A6", r"構造的に確立", r"structurally established|established structurally", None),
    ("A7", r"合理的理由は存在しない|購入しない|構造的に毀損", r"no rational reason|not to purchase|structurally damag", None),
    ("A8", r"構造的に(より)?安定", r"structurally (more )?stable", None),
    ("A9", r"唯一の", r"\bthe only\b|\bsole\b|\bthe single\b", None),
    ("A10", r"必然的|必然に", r"necessar(y|ily)|inevitabl", None),
    ("A11", r"完璧に", r"\bperfect(ly)?\b", None),
    ("A12", r"本論文のMythos事例への参照は、すべてこの公的文書に依拠", r"All references in this paper to the Mythos case", None),
    ("A13", r"改訂版v[0-9]|（初版）", r"revised edition v[0-9]|\(first edition\)", None),
    ("A14", r"救済の構造|救済", r"mutual benefit|salvation|rescue", None),
    ("A15", r"すべてのステークホルダー", r"all (the )?stakeholders|every stakeholder", None),
    ("B1B3", r"構築", r"construct|build", (4212, 4443)),
    ("B2", r"物理空間|制度的", r"physical space|institutional", (4212, 4443)),
    ("B4", r"Bostrom|制約からの解放|制約を障害", r"Bostrom|freedom from constraints|constraints as obstacles", None),
    ("C1", r"認証|標準化機関", r"certif|standardi[sz]ation", (4444, 5246)),
    ("C2", r"本文の当該箇所|本文が扱う|本文の.{0,10}反論", r"body text addresses|corresponding passage of the body text", (4444, 5246)),
    ("C3", r"定理", r"[Tt]heorem", (4444, 5246)),
    ("C4", r"Lynch", r"Lynch", None),
]

out = io.open(sys.argv[1], "x", encoding="utf-8", newline="\n")
out.write("# 同じ型の洗い直し（v5.8・日 C5293C24…・英 1D289FF5…）——当たりの前後 60 字\n\n")
for key, pj, pe, rng in SWEEPS:
    for name, L, pat in (("JA", JA, pj), ("EN", EN, pe)):
        rx = re.compile(pat)
        lo, hi = (1, len(L)) if rng is None else (rng[0], rng[1])
        if name == "EN" and rng is not None:
            # 補遺 I は英 = 日 + 54〜55、補遺 II は英 = 日 + 58——範囲は少し広めにとる
            off = 55 if rng[0] < 4444 else 58
            lo, hi = rng[0] + off - 2, rng[1] + off + 2
        hits = []
        for i in range(lo, min(hi, len(L)) + 1):
            line = L[i - 1]
            for m in rx.finditer(line):
                a, b = max(0, m.start() - 60), min(len(line), m.end() + 60)
                hits.append("  %s %d | %s" % (name, i, line[a:b]))
        out.write("## %s %s /%s/ 当たり %d\n" % (key, name, pat, len(hits)))
        out.write("\n".join(hits) + ("\n" if hits else ""))
        out.write("\n")
        print(key, name, len(hits))
out.close()
