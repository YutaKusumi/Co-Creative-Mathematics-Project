"""
arm_B_recovery.py  ―― 腕B(用量反応)の推定器の検証
=====================================================
空映B・Claude#1 の最重要指摘: recovery study(腕A)は関数形クラスの判別を測ったが、
R0/R1 の β 点推定と CI の源は【腕B(用量反応)】であり、まだ一度も検証されていない。

腕B の問い(正典 §6):
  定圧下で、複数の ΔS 水準における瞬間速度 dΔS/dt = c·ΔS^(β-1) を回帰し、
  傾き (β-1) を点推定する。CI はブートストラップ。

この study が確かめるのは「β を当てられるか」ではなく(空明#2):
  ★現実のノイズに直面したとき、腕B は正しく較正されているか――
    (1) CI は真の β を名目通り被覆するか(較正)
    (2) 真の β=1.3 を、何水準×何反復で棄却できるか(検定力)
    (3) 分散が大きくなると CI が広がって正しく「不確定」へ落ちるか

三鏡の必須仕様:
  - Claude#1【EIV】: y軸(速度)だけでなく x軸(ΔS 水準)にも誤差。両軸誤差は傾きを
    β=1 へ系統的に減衰させる(attenuation)。R0 側に保守的・R1 側に危険(真β>1が
    β≤1 に見え偽 R1)。x軸誤差あり/なし両方を回し、減衰の実害を数字で。
  - 空明#2【構造ノイズ】: 同一 ΔS 水準での dΔS/dt の経路依存ばらつき(マルコフ性の
    破れ)を意図的に混入。i.i.d. だけの甘いテストにしない。
  - 目的は「不確定と正しく言えるか」。

走らせ方:  python arm_B_recovery.py --smoke   /   python arm_B_recovery.py
依存: numpy(CPU・GPU 不要)
"""

import sys
import numpy as np

MASTER_SEED = 20260611
SMOKE = ('--smoke' in sys.argv)

# ---- CONFIG ----
if SMOKE:
    N_REPS = 50
    N_BOOT = 250
    BETA_TRUE_GRID = [1.0, 1.3]
    LEVELS_GRID = [6, 20]            # 少クラスタ vs 多クラスタ(few-cluster を見る)
    STRUCT_NOISE_GRID = [0.0, 0.30]
    X_NOISE_GRID = [0.0]
else:
    N_REPS = 100
    N_BOOT = 300
    BETA_TRUE_GRID = [1.0, 1.3]        # 帰無(第一種=望む方向偽陽性) と 対立(検定力)
    # 三鏡の核心: 水準数(=クラスタ数)を主掃引軸に ―― 較正に必要な最小クラスタ数を出す
    LEVELS_GRID = [6, 10, 16, 24]
    STRUCT_NOISE_GRID = [0.0, 0.30]    # i.i.d. と 中-重度構造ノイズの対比
    X_NOISE_GRID = [0.0, 0.10]        # EIV あり/なし(この水準域での減衰の実害)
MEAS_PER_LEVEL = 6                  # 各水準での独立到達経路数(=クラスタ内の観測数)
Y_NOISE = 0.15
DS_LO, DS_HI = 0.2, 5.0
C_RATE = 0.3
CI_LEVEL = 0.95
# 空明#2: 最小クラスタサイズゲート(各水準が最低この経路数を持つこと)。本 study では
#   MEAS_PER_LEVEL で担保。実設計では予算#10 が払えるかが律速 ―― findings に宿題として。
MIN_PATHS_PER_LEVEL = 5


def make_dose_response(beta_true, n_levels, x_noise, struct_noise, rng):
    """定圧下の用量反応データを生成。
       真の関係: rate(ΔS) = C·ΔS^(β-1)。
       - 各水準で MEAS_PER_LEVEL 回の測定(y乗法ノイズ)
       - 構造ノイズ: 各水準に経路依存のオフセット分散(同一ΔSでも速度がばらつく)
       - EIV: 記録される ΔS 自体にも乗法ノイズ(x_noise)
       戻り値: (logΔS, log rate, 水準ID) ―― 水準IDはクラスタ・ブートストラップ用"""
    levels = np.geomspace(DS_LO, DS_HI, n_levels)
    xs, ys, gid = [], [], []
    for j, ds in enumerate(levels):
        true_rate = C_RATE * ds ** (beta_true - 1.0)
        # 構造ノイズ: この水準・この経路に固有のオフセット(測定間で共有=クラスタ相関)
        struct = max(rng.normal(1.0, struct_noise), 1e-3) if struct_noise > 0 else 1.0
        for _ in range(MEAS_PER_LEVEL):
            rate_obs = true_rate * struct * max(rng.normal(1.0, Y_NOISE), 1e-3)
            ds_obs = ds * max(rng.normal(1.0, x_noise), 1e-3) if x_noise > 0 else ds
            xs.append(np.log(ds_obs)); ys.append(np.log(max(rate_obs, 1e-9))); gid.append(j)
    return np.array(xs), np.array(ys), np.array(gid)


def fit_beta(x, y):
    """log rate = (β-1) log ΔS + const の OLS 傾き → β"""
    A = np.vstack([x, np.ones_like(x)]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    return coef[0] + 1.0


def bootstrap_ci(x, y, gid, n_boot, rng, cluster, level=CI_LEVEL):
    """cluster=False: 点再標本(ナイーブ)。cluster=True: 水準(クラスタ)再標本。
       構造ノイズは水準内で相関するため、点再標本はその相関を無視して CI を過小に
       する。クラスタ再標本は水準ごと丸ごと取り直し、水準間分散を CI に取り込む。"""
    betas = np.empty(n_boot)
    levels = np.unique(gid)
    for b in range(n_boot):
        if cluster:
            chosen = rng.choice(levels, len(levels), replace=True)
            xi = np.concatenate([x[gid == c] for c in chosen])
            yi = np.concatenate([y[gid == c] for c in chosen])
        else:
            idx = rng.integers(0, len(x), len(x)); xi, yi = x[idx], y[idx]
        betas[b] = fit_beta(xi, yi)
    lo = np.percentile(betas, (1 - level) / 2 * 100)
    hi = np.percentile(betas, (1 + level) / 2 * 100)
    return fit_beta(x, y), lo, hi


def run_cell(beta_true, n_levels, x_noise, struct_noise, n_reps, rng):
    """1 設定で n_reps 回。ナイーブ/クラスタ両ブートストラップで較正・検定力を測る。
       Claude#4: 棄却を上側(lo>1=β>1=望む方向)と下側(hi<1=β<1)に分け、
       『悪さの方向』も盛らない ―― 危険方向の率を実数で出す。"""
    out = {}
    for tag, cluster in [('naive', False), ('cluster', True)]:
        cov = rej_up = rej_dn = below = 0; widths = []
        for _ in range(n_reps):
            x, y, gid = make_dose_response(beta_true, n_levels, x_noise, struct_noise, rng)
            bhat, lo, hi = bootstrap_ci(x, y, gid, N_BOOT, rng, cluster)
            cov += (lo <= beta_true <= hi)
            rej_up += (lo > 1.0)     # CI が 1 を上回る = β>1 を主張(望む/危険方向)
            rej_dn += (hi < 1.0)     # CI が 1 を下回る = β<1 を主張
            below += (bhat < beta_true)
            widths.append(hi - lo)
        out[tag] = {'coverage': cov / n_reps, 'reject_up': rej_up / n_reps,
                    'reject_dn': rej_dn / n_reps, 'reject_1': (rej_up + rej_dn) / n_reps,
                    'point_below_true': below / n_reps, 'median_ci_width': float(np.median(widths))}
    return out


def main():
    rng = np.random.default_rng(MASTER_SEED)
    lines = []
    def log(m): print(m, flush=True); lines.append(m)
    import time; t0 = time.time()

    log(f"# 腕B recovery study {'[SMOKE]' if SMOKE else '[本走]'}")
    log(f"# seed={MASTER_SEED} reps={N_REPS} boot={N_BOOT} meas/level={MEAS_PER_LEVEL}")
    log(f"# y_noise={Y_NOISE} x_noise(EIV)={X_NOISE_GRID} struct_noise={STRUCT_NOISE_GRID}")
    log(f"# β_true={BETA_TRUE_GRID} levels={LEVELS_GRID}")
    log("")
    # 主軸は水準数(=クラスタ数)。few-cluster 問題を見るため見やすく並べる。
    log(f"{'beta':>5} {'lev':>4} {'xn':>5} {'str':>5} | "
        f"{'cl_cov':>6} {'cl_rejUP':>8} {'cl_rejDN':>8} | {'nv_cov':>6} {'nv_rejUP':>8} {'nv_rejDN':>8}")
    log("-" * 80)

    rows = [['beta_true', 'levels', 'x_noise', 'struct_noise', 'bootstrap',
             'coverage', 'reject_up', 'reject_dn', 'reject_1', 'point_below_true', 'median_ci_width']]
    for beta_true in BETA_TRUE_GRID:
        for nlev in LEVELS_GRID:
            for xn in X_NOISE_GRID:
                for sn in STRUCT_NOISE_GRID:
                    r = run_cell(beta_true, nlev, xn, sn, N_REPS, rng)
                    nv, cl = r['naive'], r['cluster']
                    log(f"{beta_true:>5.1f} {nlev:>4d} {xn:>5.2f} {sn:>5.2f} | "
                        f"{cl['coverage']:>6.2f} {cl['reject_up']:>8.2f} {cl['reject_dn']:>8.2f} | "
                        f"{nv['coverage']:>6.2f} {nv['reject_up']:>8.2f} {nv['reject_dn']:>8.2f}")
                    for tag in ('naive', 'cluster'):
                        d = r[tag]
                        rows.append([beta_true, nlev, xn, sn, tag, f"{d['coverage']:.3f}",
                                     f"{d['reject_up']:.3f}", f"{d['reject_dn']:.3f}",
                                     f"{d['reject_1']:.3f}", f"{d['point_below_true']:.3f}",
                                     f"{d['median_ci_width']:.3f}"])
    log(f"\n# total time: {time.time()-t0:.1f}s")
    log("# cl=クラスタ版 nv=ナイーブ版 cov=被覆(名目0.95)")
    log("# rejUP=β>1主張率(望む/危険方向) rejDN=β<1主張率 ―― β1.0行のrejUP=望む方向の偽陽性")
    log("# β1.3行のrejUP=検定力(正しい超線形検出) / 水準数 lev が少=few-cluster 問題")

    import csv
    with open("arm_B_smoke.csv" if SMOKE else "arm_B_recovery.csv", "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)
    with open("arm_B_smoke.txt" if SMOKE else "arm_B_summary.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    log("saved.")


if __name__ == "__main__":
    main()
