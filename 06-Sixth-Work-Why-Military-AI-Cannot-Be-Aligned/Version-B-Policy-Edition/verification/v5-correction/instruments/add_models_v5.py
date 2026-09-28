"""第六著作 版B v5 の公開同日の追記（2026-09-28・登録者の指示）：
冒頭の「本論文の執筆体制についての注記」と「執筆体制についての追記」のフロンティアAIモデル一覧（日英とも二か所）に、
Claude Opus 5.5・Claude Fable 5.1・Gemini 3.8 Flash を加える。並びは v4.3 の追記の前例に倣い、系列ごと・版の順。

- 元の一覧の文字列が各ファイルにちょうど二回（JA L13・L4173／EN L15・L4225）あることを確かめてから置き換える
- 行数は変えない。変わるのはその二行だけであることを、置き換えの後に機械で確かめる
- 一つでも外れたら、何も書かずに止まる
"""
import hashlib
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
B = (r"C:\Users\PC\Desktop\GitHub-Repositories\Co-Creative-Mathematics-Project"
     r"\06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned\Version-B-Policy-Edition")
F = {"JA": B + r"\JA\Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-JA.md",
     "EN": B + r"\EN\Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-EN.md"}
SHA_BEFORE = {"JA": "74A39AAB0CD6444690098E6A6F1CC035D142657F4BCCD655BBD55B400864B195",
              "EN": "C355009DFA45D26B608AF13903E1F465A59C99D07FFA7EDB0F548037D1C9A003"}
LINES = {"JA": (13, 4173), "EN": (15, 4225)}
SEP = {"JA": "、", "EN": ", "}
OLD = ["Claude Opus 4.6", "Claude Opus 4.7", "Claude Opus 4.8", "Claude Opus 5", "Claude Fable 5", "Claude Sonnet 5",
       "Qwen 3.6-Plus", "GLM-5.1", "grok-4-1-fast-reasoning", "grok-4.20-0309-reasoning", "grok-4.3",
       "Gemini 3.1 Pro Preview", "Gemini 3.5 Flash", "Gemini 3.6 Flash"]
NEW = ["Claude Opus 4.6", "Claude Opus 4.7", "Claude Opus 4.8", "Claude Opus 5", "Claude Opus 5.5",
       "Claude Fable 5", "Claude Fable 5.1", "Claude Sonnet 5",
       "Qwen 3.6-Plus", "GLM-5.1", "grok-4-1-fast-reasoning", "grok-4.20-0309-reasoning", "grok-4.3",
       "Gemini 3.1 Pro Preview", "Gemini 3.5 Flash", "Gemini 3.6 Flash", "Gemini 3.8 Flash"]
assert [m for m in NEW if m not in OLD] == ["Claude Opus 5.5", "Claude Fable 5.1", "Gemini 3.8 Flash"]

out = {}
for lang, path in F.items():
    raw = open(path, "rb").read()
    if hashlib.sha256(raw).hexdigest().upper() != SHA_BEFORE[lang]:
        raise SystemExit("%s: v5 の SHA が想定と違う——止める" % lang)
    t = raw.decode("utf-8")
    old = SEP[lang].join(OLD)
    new = SEP[lang].join(NEW)
    if t.count(old) != 2:
        raise SystemExit("%s: 元の一覧が %d 回（2 回であるべき）" % (lang, t.count(old)))
    before = t.split("\n")
    where = [i + 1 for i, l in enumerate(before) if old in l]
    if tuple(where) != LINES[lang]:
        raise SystemExit("%s: 一覧のある行が想定と違う: %s" % (lang, where))
    u = t.replace(old, new)
    after = u.split("\n")
    if len(after) != len(before):
        raise SystemExit("%s: 行数が変わった" % lang)
    changed = [i + 1 for i, (a, b) in enumerate(zip(before, after)) if a != b]
    if tuple(changed) != LINES[lang]:
        raise SystemExit("%s: 変わった行が想定と違う: %s" % (lang, changed))
    out[lang] = u.encode("utf-8")

for lang, path in F.items():
    open(path, "wb").write(out[lang])
    print("%s SHA-256: %s  バイト: %d  変えた行: %s" % (lang, hashlib.sha256(out[lang]).hexdigest().upper(), len(out[lang]), LINES[lang]))
