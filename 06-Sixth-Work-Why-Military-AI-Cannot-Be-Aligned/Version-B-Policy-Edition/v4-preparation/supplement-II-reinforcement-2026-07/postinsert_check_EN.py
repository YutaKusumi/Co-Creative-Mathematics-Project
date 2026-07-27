# EN差し込み後の全文機械検査（JA版 postinsert_check.py の EN 対応）
import re, os, sys, subprocess, difflib
from math import lgamma, exp, log, sqrt

D = os.path.dirname(os.path.abspath(__file__))
REL = "06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned/Version-B-Policy-Edition/EN/Why-Military-AI-Cannot-Be-Aligned-Version-B-v4-EN.md"
ROOT = D
for _ in range(4):
    ROOT = os.path.dirname(ROOT)
TARGET = os.path.join(ROOT, *REL.split("/"))
t = open(TARGET, encoding="utf-8").read()
lines = t.split("\n")
i0 = next(i for i, l in enumerate(lines) if l.startswith("#") and "Addendum II" in l)
supp = "\n".join(lines[i0:])

ng = []
def chk(label, cond, detail=""):
    ng.append(None if cond else label)
    print(f"[{'OK ' if cond else 'NG '}] {label}" + (f"   {detail}" if detail else ""))

print(f"Addendum II: {len(supp):,} chars (whole book {len(t):,})\n")

print("=== 1. purity: existing text unchanged (vs git HEAD) ===")
old = subprocess.run(["git", "-C", ROOT, "show", "HEAD:" + REL],
                     capture_output=True, text=True, encoding="utf-8").stdout.split("\n")
new = t.split("\n")
sm = difflib.SequenceMatcher(None, old, new, autojunk=False)
eq = add = rem = 0
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal": eq += i2 - i1
    elif tag == "insert": add += j2 - j1
    elif tag == "delete": rem += i2 - i1
    elif tag == "replace": rem += i2 - i1; add += j2 - j1
print(f"      old {len(old)} -> new {len(new)} / equal {eq} / insert {add} / delete+replace {rem}")
chk("date line is the only modified line (replace=1)", rem == 1,
    f"delete+replace={rem}（日付行1行の置換のみが想定）")
chk("all other existing lines preserved", eq == len(old) - 1)

print("\n=== 2. headings ===")
heads = re.findall(r"^#{2,3} ([0-9]+(?:-[0-9]+)?)[ 　\.]", supp, re.M)
from collections import Counter
dup = [h for h, c in Counter(heads).items() if c > 1]
chk("no duplicate headings", not dup, str(dup))
for h in ["8-3", "8-4", "9-10"]:
    chk(f"§{h} exists", h in heads)
for sec, expect in [("8", ["8-1", "8-2", "8-3", "8-4"]),
                    ("9", [f"9-{k}" for k in range(1, 11)])]:
    got = [h for h in heads if h.startswith(sec + "-")]
    chk(f"§{sec} sub-numbering contiguous", got == expect, str(got))

print("\n=== 3. verbatim match against the EN draft ===")
draft = open(os.path.join(D, "14-EN-insertion-drafts.md"), encoding="utf-8").read()
ins = draft.split("## Insertion A")[1].split("## 冒頭メタデータの更新")[0]
probes = [l[2:] for l in ins.split("\n") if l.startswith("> ") and len(l) > 80]
bad = [p for p in probes if t.count(p) != 1]
chk(f"{len(probes)} probes each appear exactly once", not bad, f"{len(bad)} mismatched")

print("\n=== 4. numbers / vocabulary ===")
def logC(n, k): return lgamma(n+1) - lgamma(k+1) - lgamma(n-k+1)
P = 1 - sum(exp(logC(10**4, k) + k*log(0.3) + (10**4-k)*log(0.7)) for k in range(0, 2900))
chk("P(X>=2900)=0.986 and text says 0.986", round(P, 3) == 0.986 and "0.986, to be exact" in supp)
chk("assumptions (i)-(vii) present", all(f"({r})" in supp for r in
    ["i", "ii", "iii", "iv", "v", "vi", "vii"]))
chk("falsification conditions 6/7/8 once each",
    all(supp.count(f"Falsification condition {k}") == 1 for k in (6, 7, 8)))
chk("no 'wall' metaphor introduced", " wall" not in supp.lower().replace("firewall", ""))
chk("§12 firewall text intact",
    "None of the observations below is to be read as evidence for any premise of this addendum." in supp)
chk("author's own numbers not cited in §8-3", "85" not in supp.split("### 8-3")[1].split("### 8-4")[0])

print("\n=== 5. front matter ===")
chk("date line has v4.1", "July 27, 2026 (v4.1 — reinforcement of Addendum II)" in t)
chk("v4.1 note follows the v4 note",
    t.find("[Revised edition v4]") < t.find("[v4.1 (July 27, 2026)]") <
    t.find("## Abstract / Executive Summary"))

fails = [x for x in ng if x]
print("\n" + "=" * 64)
print(f"total: {len([x for x in ng if x is None])}/{len(ng)} passed"
      + ("" if not fails else "  ** ACTION: " + str(fails)))
print("=" * 64)
sys.exit(1 if fails else 0)
