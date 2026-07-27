# v4.1 英訳を EN 本体へ差し込む（JA差し込みと同一方式）
#   - 全アンカーの一意性を実行時に検証（1件でなければ中断・無変更）
#   - 差し込み後にその場検証
import os, re, sys

D = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(os.path.dirname(D)), "EN",
                      "Why-Military-AI-Cannot-Be-Aligned-Version-B-v4-EN.md")
DRAFT = os.path.join(D, "14-EN-insertion-drafts.md")

draft = open(DRAFT, encoding="utf-8").read()
def extract(label):
    seg = draft.split(f"## Insertion {label} — ")[1]
    seg = re.split(r"\n## ", seg)[0]
    out = []
    for ln in seg.split("\n"):
        if ln.startswith("> "):
            out.append(ln[2:])
        elif ln.strip() == ">":
            out.append("")
    body = "\n".join(out).strip()
    assert body, f"Insertion {label} is empty"
    return body

A, B, C, Dd, E, F, G, H, I = (extract(x) for x in list("ABCDEFGHI"))

t = open(TARGET, encoding="utf-8").read()
orig = len(t)

DATE_OLD = ("**Date:** May 13, 2026 (first edition); June 5, 2026 (revised edition, v2); "
            "July 12, 2026 (revised edition, v3); July 23, 2026 (revised edition, v4).")
DATE_NEW = DATE_OLD[:-1] + "; July 27, 2026 (v4.1 — reinforcement of Addendum II)."

V41_NOTE = (
    "\n\n> **[v4.1 (July 27, 2026)]** Nine passages were added to Addendum II as pure additions "
    "(+89 lines; zero deletions or alterations to the existing text): three independent limits "
    "(the chain of evasion — §8-3, §8-4), responses to two further objections (§9-10 and an addition "
    "to §5-3), a quantification of fleet correlation (an addition to §8-2), and others. They passed "
    "two rounds of pre-freeze review (five reviewers) and a final confirmation by three reviewers "
    "(independent machine cross-checks); the full record is included in "
    "`v4-preparation/supplement-II-reinforcement-2026-07/`. See the v4.1 entry in CHANGELOG.md for details.")

ops = [
    ("date line", DATE_OLD, DATE_NEW),
    ("A+B+C: end of §8-2 → new §8-3 → new §8-4",
     "**Deception can arrive not against a single unit, but against every unit of the same design, simultaneously.**",
     "**Deception can arrive not against a single unit, but against every unit of the same design, simultaneously.**\n\n"
     + A + "\n\n---\n\n" + B + "\n\n---\n\n" + C),
    ("D: new §9-10 (between §9-9 and §10)",
     "\n\n---\n\n## 10. Relation to prior work",
     "\n\n---\n\n" + Dd + "\n\n---\n\n## 10. Relation to prior work"),
    ("E: end of §5-3",
     "**The opposite is true. Without §8, Premise C falls to the statistical procedure of §5-1. We correct this here.**)",
     "**The opposite is true. Without §8, Premise C falls to the statistical procedure of §5-1. We correct this here.**)\n\n" + E),
    ("F: end of falsification condition 5",
     "a rebuttal to that paragraph likewise falls under this condition.",
     "a rebuttal to that paragraph likewise falls under this condition.\n\n" + F),
    ("G: end of §11",
     "\n\n---\n\n## 12. Motivation from the author's own empirical series",
     "\n\n" + G + "\n\n---\n\n## 12. Motivation from the author's own empirical series"),
    ("H: head of §6",
     "## 6. Conclusion — From Three Premises to the Failure of Technical Justification\n\n",
     "## 6. Conclusion — From Three Premises to the Failure of Technical Justification\n\n" + H + "\n\n"),
    ("I: §14 item 7", "\n\nThis list is", "\n" + I + "\n\nThis list is"),
]

print("=== anchor uniqueness (runtime) ===")
ok = True
for nm, a, _ in ops:
    n = t.count(a)
    print(f"  [{'OK' if n == 1 else 'NG'}] {nm}: {n}")
    if n != 1:
        ok = False
if not ok:
    print("ABORT — no change written")
    sys.exit(1)

for nm, a, r in ops:
    t = t.replace(a, r, 1)

# v4.1 注記を v4 注記ブロックの直後に追加
m = re.search(r"(> \*\*\[Revised edition, v4\][^\n]*\n)", t) or \
    re.search(r"(> \*\*\[Revised v4\][^\n]*\n)", t)
if m:
    t = t[:m.end()] + V41_NOTE.lstrip("\n") + "\n" + t[m.end():]
    print("  [OK] v4.1 note inserted after the v4 note")
else:
    print("  [--] v4 note block not found; v4.1 note appended after the date line instead")
    t = t.replace(DATE_NEW, DATE_NEW + V41_NOTE, 1)

open(TARGET, "w", encoding="utf-8", newline="\n").write(t)
print(f"\ninserted: {orig:,} -> {len(t):,} chars (+{len(t)-orig:,})")

print("\n=== in-place verification ===")
bad = 0
for s, want in [("### 8-3 Control at the prompt layer", 1), ("### 8-4 The chain of evasion", 1),
                ("### 9-10 Objection", 1), ("Falsification condition 6", 1),
                ("Falsification condition 7", 1), ("Falsification condition 8", 1),
                ("7. **Consideration of whether to add a citation to Geer", 1),
                ("(A note before reading the conclusion", 1),
                ("One intermediate objection is answered here in advance", 1),
                ("A single overclaim discards the whole.", 1),
                ("July 27, 2026 (v4.1", 1), ("[v4.1 (July 27, 2026)]", 1)]:
    n = t.count(s)
    print(f"  [{'OK' if n == want else 'NG'}] \"{s[:38]}…\" {n} (want {want})")
    bad += (n != want)
stray = [l for l in t.split("\n") if l.startswith("> ### ")]
print(f"  [{'OK' if not stray else 'NG'}] blockquote-heading residue: {len(stray)}")
sys.exit(1 if bad or stray else 0)
