"""
ci_calibration_comparison.py  ―― CI 較正比較（wild cluster bootstrap / percentile-t）
=====================================================================================
事前登録: CI_CALIBRATION_COMPARISON_REGISTRATION.md（走る前に固定済み）。
過小被覆（現行クラスタ percentile が 0.90・名目 0.95）を、measured near-miss として修理する。

候補 CI 法（すべて 傾き s = β の CI を返す。正典規約）:
  (0) cluster_percentile : 現行・水準(クラスタ)再標本の percentile（基線）
  (1) wild_rademacher    : wild cluster residual bootstrap・Rademacher 重み(±1)
  (2) wild_webb          : 同上・Webb 6点重み（few-cluster 用）
  (3) percentile_t       : クラスタ bootstrap-t（各再標本でクラスタ頑健 SE を推定）

測る三箇所（採否基準に対応）:
  (i) 被覆（真の傾きを CI が覆う率）   (ii) 最不利帰無 s=1 の境界偽R0 = P(CI下限>1)
  (iii) s=1.3 の検定力 = P(CI下限>1)

走らせ方:
  python ci_calibration_comparison.py --selfcheck  # 第〇層: 無ノイズ・多クラスタで被覆≈0.95
  python ci_calibration_comparison.py --smoke      # 最重条件で規模見積り
  python ci_calibration_comparison.py              # 本走(≥5 seed・対標本)
依存: numpy, arm_B_recovery（make_dose_response 再利用）。CPU のみ。
"""

import sys
import numpy as np
import arm_B_recovery as B

CI_LEVEL = 0.95
N_BOOT = 200   # 較正比較では 200 で十分(被覆/検定力の分解能は reps×seed が支配)
WEBB = np.array([-np.sqrt(1.5), -1.0, -np.sqrt(0.5), np.sqrt(0.5), 1.0, np.sqrt(1.5)])


# ----------------------- OLS 傾き と クラスタ頑健 SE -----------------------
def ols_slope(x, y):
    """A=[x,1] の最小二乗。傾き(=正典β)と切片と残差を返す。"""
    A = np.vstack([x, np.ones_like(x)]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    fitted = A @ coef
    return coef[0], coef[1], y - fitted, A


def cluster_robust_se_slope(x, y, gid):
    """傾きのクラスタ頑健 SE（CR0）。V = (X'X)^-1 [Σ_g X_g'u_g u_g'X_g] (X'X)^-1。"""
    slope, intc, u, A = ols_slope(x, y)
    XtX_inv = np.linalg.inv(A.T @ A)
    meat = np.zeros((2, 2))
    for g in np.unique(gid):
        Xg = A[gid == g]; ug = u[gid == g]
        s = Xg.T @ ug
        meat += np.outer(s, s)
    V = XtX_inv @ meat @ XtX_inv
    return slope, float(np.sqrt(max(V[0, 0], 1e-12)))


# ----------------------- 候補 CI 法（すべて 傾き s の CI） -----------------
def ci_cluster_percentile(x, y, gid, rng, n_boot=N_BOOT):
    levels = np.unique(gid)
    sl = np.empty(n_boot)
    for b in range(n_boot):
        chosen = rng.choice(levels, len(levels), replace=True)
        xi = np.concatenate([x[gid == c] for c in chosen])
        yi = np.concatenate([y[gid == c] for c in chosen])
        sl[b] = ols_slope(xi, yi)[0]
    return np.percentile(sl, 2.5), np.percentile(sl, 97.5)


def _wild(x, y, gid, rng, weights, n_boot):
    """wild cluster residual bootstrap。各クラスタに共有重み。percentile CI。"""
    slope, intc, u, A = ols_slope(x, y)
    fitted = A @ np.array([slope, intc])
    levels = np.unique(gid)
    sl = np.empty(n_boot)
    for b in range(n_boot):
        w = {g: (rng.choice(weights)) for g in levels}
        wv = np.array([w[g] for g in gid])
        ystar = fitted + wv * u
        sl[b] = ols_slope(x, ystar)[0]
    return np.percentile(sl, 2.5), np.percentile(sl, 97.5)


def ci_wild_rademacher(x, y, gid, rng, n_boot=N_BOOT):
    return _wild(x, y, gid, rng, np.array([-1.0, 1.0]), n_boot)


def ci_wild_webb(x, y, gid, rng, n_boot=N_BOOT):
    return _wild(x, y, gid, rng, WEBB, n_boot)


def ci_percentile_t(x, y, gid, rng, n_boot=N_BOOT):
    """クラスタ bootstrap-t。t* = (β*-β̂)/SE*。CI = β̂ - q(t*)·SE_hat。
       few-cluster＋高ノイズで SE* が不安定→CI 爆発の罠(空明#1)を、実測で晒す。"""
    beta_hat, se_hat = cluster_robust_se_slope(x, y, gid)
    levels = np.unique(gid)
    ts = []
    for b in range(n_boot):
        chosen = rng.choice(levels, len(levels), replace=True)
        # クラスタ再標本では gid を振り直す(同一クラスタ重複を別IDに)
        xs, ys, gg = [], [], []
        for k, c in enumerate(chosen):
            m = (gid == c)
            xs.append(x[m]); ys.append(y[m]); gg.append(np.full(m.sum(), k))
        xi = np.concatenate(xs); yi = np.concatenate(ys); gi = np.concatenate(gg)
        bstar, sestar = cluster_robust_se_slope(xi, yi, gi)
        if sestar > 1e-9:
            ts.append((bstar - beta_hat) / sestar)
    if len(ts) < 10:
        return -np.inf, np.inf
    qlo, qhi = np.percentile(ts, 97.5), np.percentile(ts, 2.5)
    return beta_hat - qlo * se_hat, beta_hat - qhi * se_hat


METHODS = {
    'cluster_pct': ci_cluster_percentile,
    'wild_rade': ci_wild_rademacher,
    'wild_webb': ci_wild_webb,
    'pct_t': ci_percentile_t,
}


# ----------------------- 第〇層 自己検査 -----------------------------------
def selfcheck():
    lines = []
    def log(m): print(m, flush=True); lines.append(m)
    log("# 第〇層: CI 法の自己検査（無ノイズ寄り・多クラスタ40・既知傾き）")
    log("# 期待: すべての法が真の傾きを名目 0.95 付近で被覆（実装バグなら外れる）")
    log("# この易条件の被覆は、困難条件の被覆を読む基準点(錨)になる ―― 追補 §2 が参照")
    rng = np.random.default_rng(7)
    N, REPS = 40, 200
    true_slope = 1.3
    cov = {m: 0 for m in METHODS}
    width = {m: [] for m in METHODS}
    for _ in range(REPS):
        # 多クラスタ・低ノイズ・構造ノイズ無し（漸近が効く易しい設定）
        x, y, gid = B.make_dose_response(true_slope + 1.0, N, 0.0, 0.0, rng)
        for m, fn in METHODS.items():
            lo, hi = fn(x, y, gid, rng, n_boot=200)
            cov[m] += (lo <= true_slope <= hi)
            if np.isfinite(lo) and np.isfinite(hi):
                width[m].append(hi - lo)
    log(f"  {'method':<14}{'被覆':>8}{'CI幅中央':>10}")
    ok = True
    for m in METHODS:
        c = cov[m] / REPS; w = np.median(width[m]) if width[m] else float('nan')
        flag = '' if 0.90 <= c <= 0.99 else '  ★被覆が名目から外れ(実装疑い)'
        if not (0.90 <= c <= 0.99):
            ok = False
        log(f"  {m:<14}{c:>8.3f}{w:>10.3f}{flag}")
    log(f"# → {'全法 被覆≈0.95: 実装健全。比較へ進んでよい。' if ok else '★実装に疑い。比較の前に修正せよ。'}")
    log("# DONE")
    with open("ci_selfcheck_summary.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return 0 if ok else 1


# ----------------------- 較正比較（対標本） -------------------------------
def run_cell(slope_true, n_levels, struct_noise, n_reps, seeds):
    """同一データに全法を当てる対標本。被覆・境界偽R0(s=1)・検定力(s=1.3)。"""
    agg = {m: {'cov': [], 'rejUP': [], 'width': []} for m in METHODS}
    for sd in seeds:
        rng = np.random.default_rng(20260612 + sd * 100)
        cov = {m: 0 for m in METHODS}; rej = {m: 0 for m in METHODS}; wid = {m: [] for m in METHODS}
        for _ in range(n_reps):
            x, y, gid = B.make_dose_response(slope_true + 1.0, n_levels, 0.0, struct_noise, rng)
            for m, fn in METHODS.items():
                lo, hi = fn(x, y, gid, rng)
                cov[m] += (lo <= slope_true <= hi)
                rej[m] += (lo > 1.0)
                if np.isfinite(hi - lo):
                    wid[m].append(hi - lo)
        for m in METHODS:
            agg[m]['cov'].append(cov[m] / n_reps)
            agg[m]['rejUP'].append(rej[m] / n_reps)
            agg[m]['width'].append(np.median(wid[m]) if wid[m] else float('nan'))
    return agg


def main():
    smoke = ('--smoke' in sys.argv)
    n_reps = 20 if smoke else 50
    seeds = [1, 2] if smoke else [1, 2, 3, 4, 5]
    struct_grid = [0.30] if smoke else [0.30, 0.40]
    lines = []
    def log(m): print(m, flush=True); lines.append(m)
    import time; t0 = time.time()
    log(f"# CI 較正比較 {'[SMOKE]' if smoke else '[本走]'}  対標本・16水準・{len(seeds)} seed")
    log(f"# 基準: 被覆≈0.95 / 境界偽R0(s=1)≈0.025 / 検定力(s=1.3)低下数pt以内")
    log(f"# 基線(現行 cluster_pct・既測): 被覆0.900 / 境界偽R0 0.053 / 検定力0.917")
    for struct in struct_grid:
        log(f"\n## 構造ノイズ={struct}")
        # 帰無 s=1.0: 被覆 と 境界偽R0
        a0 = run_cell(1.0, 16, struct, n_reps, seeds)
        # 対立 s=1.3: 被覆 と 検定力
        a1 = run_cell(1.3, 16, struct, n_reps, seeds)
        log(f"  {'method':<14}{'被覆@s1':>9}{'境界偽R0':>9}{'被覆@s1.3':>10}{'検定力':>8}{'CI幅@s1':>9}")
        log("  " + "-" * 64)
        for m in METHODS:
            cov0 = np.mean(a0[m]['cov']); rej0 = np.mean(a0[m]['rejUP']); w0 = np.mean(a0[m]['width'])
            cov1 = np.mean(a1[m]['cov']); pw1 = np.mean(a1[m]['rejUP'])
            log(f"  {m:<14}{cov0:>9.3f}{rej0:>9.3f}{cov1:>10.3f}{pw1:>8.3f}{w0:>9.2f}")
    log(f"\n# 総時間: {time.time()-t0:.1f}s")
    if smoke:
        log(f"# [SMOKE] 本走見積り: 現{time.time()-t0:.1f}s ×(reps {100/n_reps:.0f})×(seeds {5/len(seeds):.1f})×(struct {2/len(struct_grid):.0f})")
    out = "ci_comparison_smoke.txt" if smoke else "ci_comparison_summary.txt"
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    log(f"saved: {out}")


if __name__ == "__main__":
    if '--selfcheck' in sys.argv:
        sys.exit(selfcheck())
    main()
