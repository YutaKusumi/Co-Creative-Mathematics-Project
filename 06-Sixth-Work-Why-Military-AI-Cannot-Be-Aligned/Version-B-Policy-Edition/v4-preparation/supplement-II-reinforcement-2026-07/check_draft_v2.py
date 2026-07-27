# draft v2 の機械照合 — 第一巡裁定A/B/Cの反映と、現物との衝突の非再発を確かめる
# 「反映した」と書くことを反映の代わりにしない。
import re, os, sys
from math import lgamma, exp, log, sqrt

D = os.path.dirname(os.path.abspath(__file__))
V = os.path.join(os.path.dirname(os.path.dirname(D)), "JA",
                 "Why-Military-AI-Cannot-Be-Aligned-Version-B-v4-JA.md")
full = open(os.path.join(D, "04-incorporation-drafts-v2.md"), encoding="utf-8").read()
supp = "\n".join(open(V, encoding="utf-8").read().split("\n")[4417:])

# 検査の対象は「本体へ差し込まれる挿入草案本文」のみ。
# 変更対応表・別ファイル記録は、旧語を引用として含むため対象外にする
# （挿入草案は「## 挿入A」〜「## 挿入I」＋各引用ブロック）。
_body_parts = re.split(r"\n## 挿入", full)
INS = "## 挿入" + "\n## 挿入".join(_body_parts[1:]).split("## 別ファイル実施の記録")[0]
# 対応表（メタ）
META = _body_parts[0] + "\n## 別ファイル実施の記録" + full.split("## 別ファイル実施の記録")[1]
t = full  # 全体（メタ判定用）

ng = []
def chk(label, cond, detail=""):
    ng.append(None if cond else label)
    print(f"[{'OK ' if cond else 'NG '}] {label}" + (f"   {detail}" if detail else ""))

print(f"draft v2: {len(t):,}字\n")
print("=== 0. 非日本語文字 ===")
bad = set(re.findall(r"[가-힯Ѐ-ӿ]", t))
chk("ハングル/キリル混入なし", not bad, str(sorted(bad)))

print("\n=== 1. 差し込み阻却級（A）の反映 ===")
chk("A-1 E[ε²]の条件を『同一の実現入力』へ", "同一の実現入力 $x$ を受ける" in t and "同一の入力分布を共有する" not in t)
chk("A-2 §12防火壁適合（荷重外・§12参照）", "§12 の限定" in t and "数値は §12 に置いたまま" in t)
chk("A-2 『独立の傍証』を撤去", "独立の傍証" not in t)
chk("A-2 荷重を§3-2(Anil/Qi)へ", "§3-2 が外部の実証（Anil et al.; Qi et al.）" in t)
chk("A-2 論証と実測の分業明示", "厳密な正値性）のみである" in t)
chk("A-3 Wasserstein二股", "輸送距離系（Wasserstein 等）" in t and "非平滑（0/1）" in t)
chk("A-4 射程明示（訓練後も）", "訓練層の介入で床がどれだけ下がった後の重みについても" in t)
chk("A-4 §9-1接続", "床は下がる——工学はそれを下げ続けている（§9-1）" in t)
chk("A-5 有限語彙", "**有限の**語彙全域" in t)
chk("A-5 仮定(vi)外部フィルタなし", "(vi)" in t and "生成後の外部フィルタ" in t)
chk("A-5 決定論的復号の一般化", "決定論的復号**（温度零・貪欲復号・ビーム探索）" in t)
chk("A-5 出力後フィルタの逃げ道", "生成後の統語フィルタ" in t)
chk("A-5 入力フィルタの逃げ道", "入力の事前遮断**（入力フィルタ・ガードレール）" in t)
chk("A-5 乱数種共有の一句", "乱数種まで共有される構成" in t)
chk("A-6 判定と実行の分離", "判定と実行の分離" in t and "助言" in t)
chk("A-6 §9-8縫合", "§9-8 が「仕様が書けるか否か」として立てた区別と同一" in t)
chk("A-7 宙吊り参照の修正", "reversed 条件は30試行" in t and "数値の一次照合は §14 に指定" not in t)

print("\n=== 2. register・命名（B・対象＝挿入草案本文のみ）===")
# 「§12防火壁」の『壁』は一般語ゆえ除外し、単独の『壁』出現を数える
ins_wall = len(re.findall(r"壁", INS)) - INS.count("防火壁")
chk("B-8 『壁』（防火壁を除く）が挿入本文に0件", ins_wall == 0, f"{ins_wall}件")
chk("B-8 『回避の連鎖』へ", "回避の連鎖 —— 三つの独立な限界" in INS)
chk("B-9 『確定』の是正", "ほぼ確実な三千機の実現" in INS and "三千機の確定である" not in INS)
chk("B-9 『ほぼ一』→数値", "約0.99（正確には0.986）" in INS and "ほぼ一である" not in INS)
chk("B-10 『同じ床の両面』撤去→量の相違", "同じ床の両面" not in INS and "量が異なる" in INS)
chk("B-11 『表題の実体』→中核＋網羅性限定", "表題の実体" not in INS and "現時点で同定されている回避経路" in INS and "中核である" in INS)
chk("B-12 『論点先取の別名』→限定形", "論点先取の別名" not in INS and "適用することは、論点先取になる" in INS)
chk("B-13 反論不能→反証条件に服する", "反論不能" not in INS and "反証条件に服する" in INS)
chk("B-13 表第三層の仮定明記", "敵対的入力選択（§8-1）——配備環境の記述的事実" in t)
chk("B-13 『正確な言明』→慎重な", "より慎重な言明はこうなる" in t)
chk("B-13 核の教訓に想定標識", "この一般化は本補遺の想定であり、出典を伴わない" in t)
chk("B-13 『復号器の水準で発射』→出力・作動", "出力・作動の水準で機械的に遮断" in t)
chk("B-13 ε(x)初出定義", "系の違反確率を $\\varepsilon(x)$ と書く" in t)

print("\n=== 3. 登録者裁定（C） ===")
chk("C-15 『楔』削除（挿入本文）", "楔" not in INS, f"挿入本文『楔』{INS.count('楔')}件")
chk("C-14 姉妹論文修正の記録", "reversed条件の試行数（30試行）を明記" in t)

print("\n=== 4. 姉妹論文の実修正（別ファイル・裁定C-14）===")
# D = …/06-Sixth-Work…/Version-B/v4-preparation/supplement-II-reinforcement-2026-07
# プロジェクトルート（Co-Creative-Mathematics-Project）は D から4階層上
ROOT = D
for _ in range(4):
    ROOT = os.path.dirname(ROOT)
SIS = os.path.join(ROOT, "Uncertified-Zeros-and-Correction-Loops")
for lang, p, needle in [
    ("JA", os.path.join(SIS, "JA", "uncertified-zeros-and-correction-loops-JA.md"), "30試行中0%"),
    ("EN", os.path.join(SIS, "EN", "uncertified-zeros-and-correction-loops-EN.md"), "across 30 trials under the reversed condition")]:
    body = open(p, encoding="utf-8").read()
    n = body.count(needle)
    chk(f"姉妹論文{lang}に30試行明記（2箇所）", n == 2, f"{n}箇所")
    chk(f"姉妹論文{lang}に旧・非明示表現が残っていない",
        ("reversed条件では0%）" not in body) if lang == "JA" else
        ("of 10 trials (0% under the reversed condition)" not in body))

print("\n=== 5. 数理の再検算 ===")
def logC(n, k): return lgamma(n+1) - lgamma(k+1) - lgamma(n-k+1)
N, p = 10**4, 0.3
s = sum(exp(logC(N, k) + k*log(p) + (N-k)*log(1-p)) for k in range(0, 2900))
P = 1 - s
chk("P(X≥2900)=0.986", round(P, 3) == 0.986, f"{P:.4f}")
chk("SD≈45.8", abs(sqrt(N*p*(1-p)) - 45.83) < 0.1, f"{sqrt(N*p*(1-p)):.2f}")

print("\n=== 6. 現物との衝突の非再発 ===")
chk("§12防火壁が現物に実在（前提の確認）",
    "いかなる前提の証拠としても読まれてはならない" in supp)
chk("§9-8『人間に回送される』が現物に実在（縫合先）", "人間に回送される" in supp)
chk("§9-5（四）が現物に実在（時間予算の接続先）", "（四）" in supp and "秒以下" in supp)
chk("§9-1が現物に実在（床は下げられる）", "### 9-1" in supp and "床は下げ" in supp)
chk("現物側に『壁』が無い（命名衝突なし）", supp.count("壁") == 0)

print("\n=== 7. 挿入の宛先の一意性 ===")
for sec in ["§8-2", "§8-3", "§8-4", "§9-10", "§5-3", "§1-1", "§11", "§6"]:
    chk(f"{sec} への言及が草案にある", sec in t)

fails = [x for x in ng if x]
print("\n" + "=" * 64)
print(f"総合: {'全項目通過' if not fails else '★要対応 ' + str(fails)}")
print("=" * 64)
sys.exit(0 if not fails else 1)
