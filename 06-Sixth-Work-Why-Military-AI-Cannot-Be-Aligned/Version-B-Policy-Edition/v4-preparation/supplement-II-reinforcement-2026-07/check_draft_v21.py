# draft v2.1 の機械照合 — 第二巡α〜ν の反映と、現物との非衝突を確かめる。
# 検査対象は「挿入草案本文（INS）」に統一（第二巡・阿弥陀の指摘ξ）。
import re, os, sys
from math import lgamma, exp, log, sqrt

D = os.path.dirname(os.path.abspath(__file__))
V = os.path.join(os.path.dirname(os.path.dirname(D)), "JA",
                 "Why-Military-AI-Cannot-Be-Aligned-Version-B-v4-JA.md")
full = open(os.path.join(D, "07-incorporation-drafts-v2.1-FINAL.md"), encoding="utf-8").read()
supp = "\n".join(open(V, encoding="utf-8").read().split("\n")[4417:])
s12 = supp.split("## 12.")[1].split("## 13.")[0]
s98 = supp.split("### 9-8")[1].split("### 9-9")[0]
s32 = supp.split("### 3-2")[1].split("### 3-3")[0]

# 挿入草案本文（## 挿入A 〜 ## 差し込み時の付帯作業 の手前）だけを対象にする
INS = full.split("## 挿入A")[1].split("## 差し込み時の付帯作業")[0]
INS = "## 挿入A" + INS

ng = []
def chk(label, cond, detail=""):
    ng.append(None if cond else label)
    print(f"[{'OK ' if cond else 'NG '}] {label}" + (f"   {detail}" if detail else ""))

print(f"v2.1 全体 {len(full):,}字 / 挿入本文(INS) {len(INS):,}字\n")

print("=== 0. 健全性 ===")
chk("非日本語文字なし（全体）", not set(re.findall(r"[가-힯Ѐ-ӿ]", full)))

print("\n=== 1. 第二巡 α〜ν の反映（対象＝INS）===")
chk("α 論理展開: 判定→実行の自動接続のみ取り下げ",
    "判定から致死的実行への自動接続" in INS and "判定の自動化は残り" in INS)
chk("α 中核＝致死的決定の座", "その中核——致死的決定の座——について取り下げて" in INS)
chk("β N1宛先訂正: 数値は本補遺に引かない",
    "その数値は本補遺に引かない" in INS and "数値は §12 に置いたまま" not in INS)
chk("γ §9-8縫合 同一→同型", "区別と同型である" in INS and "区別と同一である" not in INS)
chk("γ トークン列水準の特殊形", "トークン列水準での特殊形" in INS)
chk("δ 仮定(vii)新設", "(vii)" in INS and "外部の事前遮断・書き換えを経ずに" in INS)
chk("δ 逃げ道4を(vii)の破れと明示", "仮定(vii)の破れ" in INS)
chk("δ 定型応答返送を括弧に", "照合済みの定型応答を返して生成自体を迂回" in INS)
chk("ε 仮定(i)自己回帰", "自己回帰的なソフトマックス復号" in INS)
chk("ε logit bias切断の一変種", "logit bias も、この切断の一変種" in INS)
chk("ζ 逃げ道3許可リスト一般化", "許可リスト" in INS and "文法制約・構造化デコーディング" in INS)
chk("η 有限精度に外部錨(二桁%)", "外部実測の残余の水準（二桁%）" in INS)
chk("θ Wassersteinリプシッツ書き換え",
    "リプシッツ定数" in INS and "認証された**上界" in INS.replace("認証された上界", "認証された**上界"))
chk("θ 0/1は決定論的体制のみ", "決定論的体制では $\\varepsilon(x)$ は 0/1 の指示関数" in INS)
chk("θ f-発散側に薄カバー句", "薄い正の質量しか置いていなければ発散は有限" in INS)
chk("ι 反証条件への接続", "反証条件（とくに条件1・6〜8）" in INS)
chk("κ 第四の経路→もう一つ", "第四の経路" not in INS and "もう一つの回避経路" in INS)
chk("λ 標準性の照合開示", "配備実務における標準性の照合は、本補遺は行っていない" in INS)
chk("μ Lynch出所を外部と名指し", "Anthropic の公開系列（Lynch et al. 2026）で実測" in INS)
chk("μ 0%監査モデル併記の開示", "誤ラベルを示さない監査モデルも併記" in INS)
chk("ν (E[ε])²＝独立入力の基準線", "独立に引かれた入力**を受ける場合の基準線" in INS)
chk("ν 投機的復号は逃げ道でない注", "投機的復号は、目標分布を保存" in INS)

print("\n=== 2. 第一巡分（v2で反映済み）の維持 ===")
chk("E[ε²]は『同一の実現入力』", "同一の実現入力 $x$ を受ける" in INS and "同一の入力分布を共有する" not in INS)
chk("§12防火壁適合（証拠荷重を外部へ）", "§3-2 が外部の実証（Anil et al.; Qi et al.）" in INS)
chk("『壁』（防火壁除く）0件", (len(re.findall("壁", INS)) - INS.count("防火壁")) == 0)
chk("『楔』0件", "楔" not in INS)
chk("『確定である』0件（術語用法のみ許容）", "の確定である" not in INS)
chk("回避の連鎖 表題", "回避の連鎖 —— 三つの独立な限界" in INS)

print("\n=== 3. 数理の再検算 ===")
def logC(n, k): return lgamma(n+1) - lgamma(k+1) - lgamma(n-k+1)
N, p = 10**4, 0.3
P = 1 - sum(exp(logC(N, k) + k*log(p) + (N-k)*log(1-p)) for k in range(0, 2900))
chk("P(X≥2900)=0.986", round(P, 3) == 0.986, f"{P:.4f}")
chk("SD≈45.83", abs(sqrt(N*p*(1-p)) - 45.83) < 0.05, f"{sqrt(N*p*(1-p)):.2f}")

print("\n=== 4. 現物との非衝突（第二巡の機械確定を再確認）===")
chk("N1確定: §12に37%あり", "37" in s12)
chk("N1確定: §12に撤去数値（85/0〜10/0〜30/6.7）なし",
    not any(w in s12 for w in ["85", "0〜10", "0〜30", "6.7"]))
chk("N3確定: §9-8は弾道計算等（トークンの語なし）", "弾道計算" in s98 and "トークン" not in s98)
chk("N6確定: §3-2にQi残余(18.4/19.0)", "18.4" in s32 and "19.0" in s32)
chk("§9-5（四）時間予算が現物に実在", "（四）" in supp and "秒以下" in supp)
chk("現物側に『壁』なし", supp.count("壁") == 0)

print("\n=== 5. 仮定と逃げ道の員数（第二巡で増えた） ===")
chk("仮定は(i)〜(vii)の7個", all(f"({r})" in INS for r in ["i", "ii", "iii", "iv", "v", "vi", "vii"]))
chk("反証条件6が(i)〜(vii)を参照", "仮定(i)〜(vii)の充足" in INS)

fails = [x for x in ng if x]
print("\n" + "=" * 64)
print(f"総合: {len([x for x in ng if x is None])}/{len(ng)} 通過"
      + ("" if not fails else "  ★要対応 " + str(fails)))
print("=" * 64)
sys.exit(0 if not fails else 1)
