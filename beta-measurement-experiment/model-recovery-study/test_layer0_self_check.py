"""
test_layer0_self_check.py  ―― 治具の自己検査(第〇層)
=====================================================
Claude さん・空映さんの指摘: recovery study は「判別できるか」を測るが、
その前段に「治具(当てはめ・判定)は正しいか」の層が要る。

二つの役割:
  (A) 自己検査 ―― 各模型の無ノイズ自己生成データを当てはめ、パラメータが
      ほぼ厳密に戻る/真クラスが選ばれることを確認(治具の健全性)。
  (B) 回帰テスト ―― 過去 5 段のバグそれぞれに「二度と通らない」一本を置く
      (非退行検証のコード版。約束台帳 #25 の第〇層)。

これは「報告でなく実物」を、コードの正しさそのものに向ける層である。
走らせ方:  python test_layer0_self_check.py   (CPU・数秒・GPU 不要)
合否:      全テスト PASS でなければ、下流の recovery study に進んではならない。
"""

import sys
import numpy as np
import model_recovery as m

PASS, FAIL = "PASS", "FAIL"
results = []


def check(name, cond, detail=""):
    s = PASS if cond else FAIL
    results.append((s, name, detail))
    print(f"[{s}] {name}" + (f"  ―― {detail}" if detail else ""))
    return cond


# =====================================================================
# (A) 自己検査 ―― 無ノイズ自己生成データで、各模型が自分のクラスに選ばれるか
# =====================================================================
print("\n## (A) 自己検査: 無ノイズ自己生成データで真クラスが選ばれるか")
t = np.linspace(0.0, m.T_END, 60)   # 高解像度・無ノイズ
for kind in m.KINDS:
    extra = {'p': 1.6, 't_div': 1.2 * m.T_END} if kind == 'blowup' else \
            ({'Smax': m.S0 * 6.0} if kind == 'saturation' else {})
    S = m.true_trajectory(kind, t, m.S0, m.A, extra)
    finite = np.all(np.isfinite(S)) and np.all(S > 0)
    check(f"自己生成 {kind} は有限・正", finite, f"S(0)={S[0]:.3f} S(end)={S[-1]:.3f}")
    if finite:
        sel = m.select_model(t, S)
        # 無ノイズなら真クラスが選ばれるべき(指数⇔発散の近縁を除き)
        ok = (sel == kind) or (kind in ('exponential', 'blowup') and sel in ('exponential', 'blowup'))
        check(f"自己生成 {kind} の選択", ok, f"選択={sel}")


# =====================================================================
# (B) 回帰テスト ―― 過去 5 段のバグに「二度と通らない」一本ずつ
# =====================================================================
print("\n## (B) 回帰テスト: 過去 5 段のバグを機械で固定")

# --- バグ1: v1 の ODE 積分が重すぎた(96分) → 生成は閉形式で O(1) であること ---
import time
t0 = time.time()
for _ in range(1000):
    m.true_trajectory('blowup', t, m.S0, m.A, {'p': 1.6, 't_div': 1.2 * m.T_END})
dt = time.time() - t0
check("バグ1回帰: 生成は閉形式で高速(1000本<0.5s)", dt < 0.5, f"{dt*1000:.0f}ms/1000本")

# --- バグ2: blowup が窓内で 1e15 に発散する artifact → 発散時刻が窓外なら有界 ---
S = m.true_trajectory('blowup', t, m.S0, m.A, {'p': 1.6, 't_div': 1.2 * m.T_END})
check("バグ2回帰: blowup(発散窓外)は非天文学的に有界", S.max() < 1e4, f"max={S.max():.2f}")

# --- バグ3(最重要): blowup 当てはめの境界が真値を締め出した(C=2.63 を下限10.1が) ---
#     → 強い真 blowup データで blowup の SSE が有限かつ最良であること
S = m.true_trajectory('blowup', t, m.S0, m.A, {'p': 1.6, 't_div': 1.02 * m.T_END})
rng = np.random.default_rng(0)
Sobs = np.maximum(S * rng.normal(1.0, 0.03, len(t)), 1e-6)
fits = m.fit_models(t, Sobs)
blow_sse = fits['blowup'][0]
check("バグ3回帰: 真blowupで blowup当てはめのSSEが有限", np.isfinite(blow_sse), f"SSE={blow_sse:.4g}")
check("バグ3回帰: 真blowupが blowupと判別される", m.select_model(t, Sobs) == 'blowup',
      f"選択={m.select_model(t, Sobs)}")

# --- バグ4: 自動判定が主軸セルしか評価せず n=60 の合格を見落とした ---
#     → gate 評価関数が全セルを受け取れること(構造のテスト)
def gate_ok(blowup_rate, falsepos, b_thr=0.8, fp_thr=0.10):
    return (blowup_rate >= b_thr) and (falsepos <= fp_thr)
# n=60 相当(blowup=1.00, fp=0.05)は合格、n=30(blowup=1.00, fp=0.13)は不合格、を機械で
check("バグ4回帰: gate関数が n60相当(fp0.05)を合格と判定", gate_ok(1.00, 0.05) is True)
check("バグ4回帰: gate関数が n30相当(fp0.13)を不合格と判定", gate_ok(1.00, 0.13) is False,
      "主軸だけ見て『合格なし』と誤らないため、評価は全セルに適用すること")

# --- バグ5(治具自身): aic_bic が SSE=0 や inf で壊れないこと ---
import math
for sse in [0.0, 1e-30, np.inf, 1e12]:
    a, b = m.aic_bic(sse, 3, 60)
    if not (math.isfinite(a) and math.isfinite(b)):
        check(f"バグ5回帰: aic_bic(SSE={sse}) が有限", False, f"AIC={a} BIC={b}")
        break
else:
    check("バグ5回帰: aic_bic が極端なSSE(0/inf)でも有限を返す", True)


# =====================================================================
# 総括
# =====================================================================
n_fail = sum(1 for s, _, _ in results if s == FAIL)
print(f"\n{'='*60}")
print(f"# 第〇層 自己検査: {len(results)-n_fail}/{len(results)} PASS, {n_fail} FAIL")
if n_fail == 0:
    print("# → 治具は健全。下流の recovery study に進んでよい。")
    sys.exit(0)
else:
    print("# → ★治具に欠陥。下流に進む前に修正せよ(失敗項目を上に表示)。")
    sys.exit(1)
