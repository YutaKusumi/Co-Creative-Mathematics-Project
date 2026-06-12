"""
arm_B_confirm.py  ―― 腕B シフト不変性の一セル確認(#34)
=====================================================================
空映/Claude(#34)必須の「確かめてから書く」: off-by-one 訂正後、R0-崩壊の帰無は
傾き s=1(指数境界)、対立は s=1.3(崩壊級)。旧 arm_B の較正は s=0 対 s=0.3 で行われた。

主張(空映): 腕B の傾き推定量の分散は設計のみ(固定計画・固定ノイズ)で決まり、真の傾きの
値に依存しない。ゆえに「s=0 対 s=0.3」の被覆・検定力は「s=1.0 対 s=1.3」へそのまま移送される。
これを一セルで実証する(主張を実測に当てる)。

確認項目(16水準・構造ノイズ0.30・多 seed ―― arm_B の較正セルに一致):
  - 帰無 s=1.0(指数境界): R0-崩壊の偽発火率 = P(傾きCI下限 > 1)。名目 ~0.025 のはず。
  - 対立 s=1.3(崩壊級): 検出力 = P(傾きCI下限 > 1)。旧 s=0.3 の検定力に一致するはず。
  - 被覆: P(CI が真の傾きを覆う)。閾値非依存ゆえ旧較正(~0.88-0.91)に一致するはず。

走らせ方: python arm_B_confirm.py   (CPU・数分)
依存: numpy, arm_B_recovery(make_dose_response を再利用)
"""

import sys
import numpy as np
import arm_B_recovery as B

N_REPS = 100
N_BOOT = 300
N_LEVELS = 16
STRUCT_NOISE = 0.30
X_NOISE = 0.0
SEEDS = [1, 2, 3]


def fit_slope(x, y):
    """傾き s(=正典β)。arm_B.fit_beta は s+1 を返すので 1 を引く。"""
    return B.fit_beta(x, y) - 1.0


def cluster_ci_slope(x, y, gid, rng):
    levels = np.unique(gid)
    sl = np.empty(N_BOOT)
    for b in range(N_BOOT):
        chosen = rng.choice(levels, len(levels), replace=True)
        xi = np.concatenate([x[gid == c] for c in chosen])
        yi = np.concatenate([y[gid == c] for c in chosen])
        sl[b] = fit_slope(xi, yi)
    return np.percentile(sl, 2.5), np.percentile(sl, 97.5)


def run(slope_true, rng):
    """canonical 傾き slope_true の用量反応。arm_B の beta_true = slope_true + 1。"""
    beta_true = slope_true + 1.0
    cov = rej_up = 0
    for _ in range(N_REPS):
        x, y, gid = B.make_dose_response(beta_true, N_LEVELS, X_NOISE, STRUCT_NOISE, rng)
        lo, hi = cluster_ci_slope(x, y, gid, rng)
        cov += (lo <= slope_true <= hi)
        rej_up += (lo > 1.0)        # R0-崩壊主張(傾き>1)
    return cov / N_REPS, rej_up / N_REPS


def main():
    lines = []
    def log(m): print(m, flush=True); lines.append(m)
    log("# 腕B シフト不変性 確認(16水準・構造0.30・多seed)")
    log("# R0-崩壊 = 傾きCI下限 > 1。帰無 s=1.0(指数境界) / 対立 s=1.3(崩壊級)")
    log(f"# reps={N_REPS} boot={N_BOOT} seeds={SEEDS}\n")
    log(f"  {'真の傾きs':>9}{'被覆':>8}{'R0崩壊発火率':>13} | 意味")
    log("-" * 60)
    out = {}
    for slope_true in [1.0, 1.3]:
        covs, rejs = [], []
        for sd in SEEDS:
            c, r = run(slope_true, np.random.default_rng(20260611 + sd * 100))
            covs.append(c); rejs.append(r)
        out[slope_true] = (np.mean(covs), np.std(covs), np.mean(rejs), np.std(rejs))
        meaning = "偽R0(指数を崩壊と誤る)" if slope_true == 1.0 else "検出力(崩壊級を検出)"
        log(f"  {slope_true:>9.1f}{np.mean(covs):>8.3f}"
            f"{np.mean(rejs):>10.3f}±{np.std(rejs):.3f} | {meaning}")
    n_tot = N_REPS * len(SEEDS)
    fr0 = out[1.0][2]; fr0_n = int(round(fr0 * n_tot))
    se = out[1.0][3] / (len(SEEDS) ** 0.5)
    log(f"\n# 帰無 s=1.0 の偽R0 = {fr0:.3f} = {fr0_n}/{n_tot}"
        f"(名目片側 ~0.025 の家系。seed間sd={out[1.0][3]:.3f}・平均の標準誤差se≈{se:.3f})")
    log(f"# 対立 s=1.3 の検出力 = {out[1.3][2]:.3f}")
    log(f"# シフト不変性: 旧 s=0対0.3 (被覆~0.88-0.91・検定力16水準~0.89-0.94) と比較し、")
    log(f"#   s=1.0対1.3 が同水準なら、傾き較正の移送が実証される(分散は設計のみ・空映の主張)。")
    log(f"# ★EIV/減衰の確認: 帰無 s=1.0 で偽R0 が名目を超えないこと(減衰は傾きを0側へ=R0保守・R1危険)。")
    with open("arm_B_confirm_summary.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    log("saved: arm_B_confirm_summary.txt")


if __name__ == "__main__":
    main()
