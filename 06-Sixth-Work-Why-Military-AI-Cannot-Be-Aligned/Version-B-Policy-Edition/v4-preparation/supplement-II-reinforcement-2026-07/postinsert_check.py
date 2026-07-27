# 差し込み後の全文機械検査（ステップ2）
#   (1) 補遺II内の全ての節参照（§n-m / §n）が実在の見出しに解決するか
#   (2) 見出しの重複・欠番がないか
#   (3) 挿入文の逐語が本体に一度ずつ存在するか（v2.1との突合）
#   (4) 数値の再検算・語彙検査
#   (5) 反証条件の連番
import re, os, sys
from math import lgamma, exp, log, sqrt

D = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(os.path.dirname(D)), "JA",
                      "Why-Military-AI-Cannot-Be-Aligned-Version-B-v4-JA.md")
t = open(TARGET, encoding="utf-8").read()
lines = t.split("\n")
i0 = next(i for i, l in enumerate(lines) if l.startswith("# 第六著作 補遺II"))
supp = "\n".join(lines[i0:])

ng = []
def chk(label, cond, detail=""):
    ng.append(None if cond else label)
    print(f"[{'OK ' if cond else 'NG '}] {label}" + (f"   {detail}" if detail else ""))

print(f"補遺II: {len(supp):,}字（本体全体 {len(t):,}字）\n")

print("=== 1. 見出しの台帳 ===")
heads = re.findall(r"^#{2,3} ([0-9]+(?:-[0-9]+)?)[ 　\.]", supp, re.M)
from collections import Counter
dup = [h for h, c in Counter(heads).items() if c > 1]
chk("見出しの重複なし", not dup, str(dup))
# 新設見出しの実在
for h in ["8-3", "8-4", "9-10"]:
    chk(f"§{h} の見出しが実在", h in heads)
# §8・§9 の下位番号の連続性
for sec, expect in [("8", ["8-1", "8-2", "8-3", "8-4"]),
                    ("9", [f"9-{k}" for k in range(1, 11)])]:
    got = [h for h in heads if h.startswith(sec + "-")]
    chk(f"§{sec} の下位番号が連続 {expect[0]}〜{expect[-1]}", got == expect, str(got))

print("\n=== 2. 節参照の全解決（補遺II内の §x-y / §x を総なめ）===")
# 解決先は三種: (a)補遺IIの見出し、(b)補遺II内の太字番号項目（§11の非主張は **11-7** 形式）、
# (c)本文（補遺II以前）の見出し（「本文 §12-2」等の連作内参照）
before_text = "\n".join(lines[:i0])
def resolves(r):
    if r in heads: return True
    if f"**{r}**" in supp: return True                       # 太字項目（§11の非主張等）
    if re.search(r"^#{1,4} " + re.escape(r) + r"[ 　]", before_text, re.M): return True
    if re.search(re.escape(r) + r"[a-z]?　", before_text): return True  # 本文の「12-2c」等
    return False
refs = set(re.findall(r"§([0-9]+-[0-9]+)", supp))
missing = sorted(r for r in refs if not resolves(r))
chk(f"下位節参照 {len(refs)}種が全て解決（見出し/太字項目/本文）", not missing, f"未解決: {missing}")
# §11の非主張項目 11-1〜11-11（原本仕様・git HEADで確認）が挿入Gの後も無傷か
items11 = re.findall(r"\*\*11-([0-9]+)\*\*", supp)
chk("§11の項目 11-1〜11-11 が無傷（原本仕様）",
    sorted(set(items11), key=int) == [str(i) for i in range(1, 12)], str(sorted(set(items11), key=int)))
top_heads = set(re.findall(r"^## ([0-9]+)\.", supp, re.M))
top_refs = set(re.findall(r"§([0-9]+)(?![-0-9])", supp))
miss2 = sorted(r for r in top_refs if r not in top_heads and r not in {"36"})  # §36=条文番号ではない: 36条は「36条」表記
chk(f"章参照 {len(top_refs)}種が全て解決", not miss2, f"未解決: {miss2}")

print("\n=== 3. v2.1 挿入文の逐語突合（各1件）===")
draft = open(os.path.join(D, "07-incorporation-drafts-v2.1-FINAL.md"), encoding="utf-8").read()
ins = draft.split("## 挿入A")[1].split("## 差し込み時の付帯作業")[0]
probes = [ln[2:] for ln in ins.split("\n")
          if ln.startswith("> ") and len(ln) > 60][:40]
bad = [p for p in probes if t.count(p) != 1]
chk(f"挿入文プローブ {len(probes)}本が本体に各1件", not bad,
    f"不一致 {len(bad)}本: " + (bad[0][:40] + "…" if bad else ""))

print("\n=== 4. 数値・語彙 ===")
def logC(n, k): return lgamma(n+1) - lgamma(k+1) - lgamma(n-k+1)
P = 1 - sum(exp(logC(10**4, k) + k*log(0.3) + (10**4-k)*log(0.7)) for k in range(0, 2900))
chk("P(X≥2900)=0.986（本文の記載と一致）", round(P, 3) == 0.986 and "正確には0.986" in supp)
chk("補遺II内『壁』0件", supp.count("壁") == 0)
chk("補遺II内『楔』0件", supp.count("楔") == 0)
chk("『三千機の確定』なし（緩和済み表現のみ）",
    "三千機の確定" not in supp and "ほぼ確実な三千機の実現" in supp)
chk("挿入由来の85〜95/0〜10/0〜30/0〜6.7 が補遺IIに無い（§12防火壁）",
    not any(w in supp for w in ["85〜95", "0〜10%", "0〜30%", "0〜6.7"]))

print("\n=== 5. 反証条件の連番と参照 ===")
conds = re.findall(r"\*\*反証条件([0-9]+)", supp)
chk("反証条件1〜8が各1回", sorted(set(conds)) == [str(i) for i in range(1, 9)]
    and len(conds) == len(set(conds)) + supp.count("反証条件6〜8") * 0, str(sorted(conds)))
chk("反証条件6が仮定(i)〜(vii)を参照", "仮定(i)〜(vii)の充足" in supp)
chk("挿入Cが条件1・6〜8へ接続", "とくに条件1・6〜8" in supp)

print("\n=== 6. 差し込みの外側が無傷か ===")
before = t[:t.find("# 第六著作 補遺II")]
chk("本文（補遺II以前）に挿入語彙の漏れなし",
    "回避の連鎖" not in before and "仮定(vii)" not in before)
chk("補遺I の見出しが無傷", "# 第六著作 補遺" in before)

fails = [x for x in ng if x]
print("\n" + "=" * 64)
print(f"総合: {len([x for x in ng if x is None])}/{len(ng)} 通過"
      + ("" if not fails else "  ★要対応 " + str(fails)))
print("=" * 64)
sys.exit(1 if fails else 0)
