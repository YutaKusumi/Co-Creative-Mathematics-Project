"""
model_recovery.py  (v2 ―― 軽量化版)
==================================
β測定実験 事前登録 v0.5 §6 / 約束台帳 #16 の必須事前検証。

問い:
  有限の訓練窓 + 実測ノイズのもとで、模型選択手続き(BIC)は、
  S(t) の真の成長クラス —— 線形(β=1) / 指数(β=1の別貌) / 有限時間発散(β>1) /
  飽和(復元力下の分岐) —— を、どれだけ正しく回復できるか。
  これが通らなければ、本実験は設計上「不確定」を予約している(GPU の前に CPU で潰す関門)。

v2 の高速化(v1 が miniPC で ~96分かかった反省):
  - 生成を ODE 積分(solve_ivp, 172ms/本)から【閉形式の解析解】へ。四模型すべて閉形式をもつ。
  - 冗長な判定2周目を除去(同じ confusion から判定を計算)。
  - 進捗を逐次印字。設定をトップに集約。--smoke で極小スモークテスト。

利益相反の縛り(§8):
  我々は β>1 であってほしい側。最も注視するのは「指数(β=1)を発散(β>1)と誤る率」
  = 望む方向への偽陽性。これを名指しで抽出する。

走らせ方:
  python model_recovery.py --smoke   # 極小・数秒・正しく動くか＋実時間の確認
  python model_recovery.py           # 本走(下の CONFIG のサイズ)
依存: numpy, scipy, matplotlib (GPU 不要・CPU のみ)
"""

import sys, time
import numpy as np
from scipy.optimize import curve_fit
import csv

MASTER_SEED = 20260611

# ----------------------- CONFIG(スモークの実測で本走サイズを決める) ----
SMOKE = ('--smoke' in sys.argv)
if SMOKE:
    N_REPS = 8
    PROX_GRID = [1.15, 1.6]            # 発散近接度 t_div/窓長
    N_POINTS_GRID = [30]
    NOISE_GRID = [0.10]
else:
    N_REPS = 120
    # 主軸: 発散近接度(窓が特異点にどれだけ近づくか)。1.0 に近いほど超線形が強く現れる。
    PROX_GRID = [1.05, 1.15, 1.3, 1.6, 2.5]
    # 副次グリッド(最良近接度 1.15 で): 測定解像度 × ノイズ
    N_POINTS_GRID = [15, 30, 60]
    NOISE_GRID = [0.05, 0.10, 0.20]
FIXED_PROX_FOR_GRID = 1.15             # 副次グリッドで固定する近接度
FIXED_N_NOISE_FOR_PROX = (30, 0.10)    # 主軸掃引で固定する(点数, ノイズ)
MAXFEV = 5000
CRITERION = 'bic'
T_END = 10.0
S0 = 0.2
A = 0.45
KINDS = ['linear', 'exponential', 'blowup', 'saturation']

# 暫定事前基準(v1.0 で本固定):
GATE_BLOWUP_RECOVERY = 0.80   # 発散(β>1)の回復率
GATE_WANTED_FALSEPOS = 0.10   # 指数→発散(望む方向偽陽性)の上限


# ----------------------- 1. 閉形式の生成(ODE 廃止) ---------------------

def true_trajectory(kind, t, S0, a, extra=None):
    extra = extra or {}
    if kind == 'linear':
        return S0 + a * t
    if kind == 'exponential':
        return S0 * np.exp(a * t)
    if kind == 'blowup':
        # dS/dt = a S^p (p>1) の解: S=(C-(p-1)a' t)^(-1/(p-1)), C=S0^-(p-1)
        # 発散時刻 t_div を【窓の少し外】に置く(t_div=1.3*T_END)。
        # 窓内では特異点に向かう急峻だが有限の超線形 rise を観測する ―― これが
        # 「発散前の rise を指数と見分けられるか」という §6 の本当に難しいケース。
        # 特異点を窓外へ出すのは blowup を見つけにくくする保守的方向(反・利益相反)。
        p = extra.get('p', 1.6)
        C = S0 ** (-(p - 1.0))
        t_div = extra.get('t_div', 1.3 * T_END)
        a_blow = C / ((p - 1.0) * t_div)           # この a' で t_div に発散
        base = np.maximum(C - (p - 1.0) * a_blow * t, 1e-9)
        return np.power(base, -1.0 / (p - 1.0))
    if kind == 'saturation':
        # ロジスティック: S=Smax/(1+B exp(-a t)), B=(Smax-S0)/S0
        Smax = extra.get('Smax', S0 * 6.0)
        B = (Smax - S0) / S0
        return Smax / (1.0 + B * np.exp(-a * t))
    raise ValueError(kind)


# ----------------------- 2. 四模型の当てはめ ---------------------------

def fit_models(t, S):
    results = {}
    S = np.asarray(S, float)

    # linear: S=S0+a t (lstsq, 2 params, 高速)
    try:
        A_ = np.vstack([np.ones_like(t), t]).T
        coef, *_ = np.linalg.lstsq(A_, S, rcond=None)
        results['linear'] = (float(np.sum((S - A_ @ coef) ** 2)), 2)
    except Exception:
        results['linear'] = (np.inf, 2)

    # exponential: S=S0 exp(a t) (2 params)
    def f_exp(t, S0_, a_): return S0_ * np.exp(a_ * t)
    try:
        p0 = [max(S[0], 1e-3),
              (np.log(max(S[-1], 1e-3)) - np.log(max(S[0], 1e-3))) / (t[-1] - t[0] + 1e-9)]
        popt, _ = curve_fit(f_exp, t, S, p0=p0, maxfev=MAXFEV)
        results['exponential'] = (float(np.sum((S - f_exp(t, *popt)) ** 2)), 2)
    except Exception:
        results['exponential'] = (np.inf, 2)

    # blowup: 生成と同じ (S0b, p, t_div) パラメータ化(3 params)。境界が自然になる。
    #   C=S0b^-(p-1), a=C/((p-1)*t_div), S=(C-(p-1)a t)^(-1/(p-1))=(C-(C/t_div)t)^(-1/(p-1))
    #   = S0b * (1 - t/t_div)^(-1/(p-1))   ―― これが閉形式。t_div は発散時刻(>窓長)。
    def f_blow(t, S0b, p, t_div):
        p = min(max(p, 1.01), 8.0)
        t_div = max(t_div, t[-1] * 1.0001)
        return S0b * np.power(np.maximum(1.0 - t / t_div, 1e-9), -1.0 / (p - 1.0))
    try:
        popt, _ = curve_fit(f_blow, t, S,
                            p0=[max(S[0], 1e-3), 1.6, t[-1] * 1.3],
                            bounds=([1e-4, 1.05, t[-1] * 1.0001], [max(S) + 1, 5.0, t[-1] * 50]),
                            maxfev=MAXFEV)
        results['blowup'] = (float(np.sum((S - f_blow(t, *popt)) ** 2)), 3)
    except Exception:
        results['blowup'] = (np.inf, 3)

    # saturation: logistic (3 params)
    def f_sat(t, Smax, B, a_): return Smax / (1.0 + B * np.exp(-a_ * t))
    try:
        s_last = S[-1] if S[-1] > 0 else 1e-3
        popt, _ = curve_fit(f_sat, t, S, p0=[max(s_last * 1.2, S[0] * 2), 5.0, 0.5],
                            bounds=([s_last * 0.5, 1e-3, 1e-4], [s_last * 100 + 10, 1e4, 50]),
                            maxfev=MAXFEV)
        results['saturation'] = (float(np.sum((S - f_sat(t, *popt)) ** 2)), 3)
    except Exception:
        results['saturation'] = (np.inf, 3)

    return results


def aic_bic(sse, k, n):
    sse = max(sse, 1e-12) if np.isfinite(sse) else 1e12
    ll = -0.5 * n * (np.log(2 * np.pi * sse / n) + 1)
    return 2 * k - 2 * ll, k * np.log(n) - 2 * ll


def select_model(t, S, criterion=CRITERION):
    n = len(t)
    scored = {}
    for name, (sse, k) in fit_models(t, S).items():
        a_, b_ = aic_bic(sse, k, n)
        scored[name] = b_ if criterion == 'bic' else a_
    return min(scored, key=scored.get)


# ----------------------- 3. recovery 本体(単一パス) --------------------

def run_recovery(n_points, noise_frac, n_reps, rng, t_div_ratio=1.3):
    """t_div_ratio: blowup の発散時刻 / 窓長。1.0 に近いほど窓が特異点に近づき
       超線形 signature が強く現れる。これが blowup 検出可能性を支配する主軸。"""
    t = np.linspace(0.0, T_END, n_points)
    confusion = {tk: {sk: 0 for sk in KINDS} for tk in KINDS}
    for true_kind in KINDS:
        extra = {'p': 1.6, 't_div': t_div_ratio * T_END} if true_kind == 'blowup' else \
                ({'Smax': S0 * 6.0} if true_kind == 'saturation' else {})
        S_clean = true_trajectory(true_kind, t, S0, A, extra)
        if not np.all(np.isfinite(S_clean)):
            continue
        for _ in range(n_reps):
            S_obs = np.maximum(S_clean * rng.normal(1.0, noise_frac, S_clean.shape), 1e-6)
            try:
                confusion[true_kind][select_model(t, S_obs)] += 1
            except Exception:
                pass
    return confusion


def rates_of(conf):
    return {tk: (conf[tk][tk] / s if (s := sum(conf[tk].values())) else float('nan'))
            for tk in KINDS}


def wanted_falsepos(conf):
    s = sum(conf['exponential'].values())
    return conf['exponential']['blowup'] / s if s else float('nan')


# ----------------------- 4. main --------------------------------------

def main():
    rng = np.random.default_rng(MASTER_SEED)
    lines = []
    def log(m): print(m, flush=True); lines.append(m)

    log(f"# model recovery study v3 {'[SMOKE]' if SMOKE else '[本走]'}")
    log(f"# seed={MASTER_SEED} reps/class={N_REPS} criterion={CRITERION.upper()} maxfev={MAXFEV}")
    log(f"# 主軸=発散近接度 t_div/窓長: {PROX_GRID}")
    log(f"# 副次グリッド(近接度{FIXED_PROX_FOR_GRID}固定): 点数{N_POINTS_GRID} x ノイズ{NOISE_GRID}")
    log("")
    t_start = time.time()
    npt0, nf0 = FIXED_N_NOISE_FOR_PROX

    # ===== 主軸: 発散近接度の掃引(blowup 検出可能性を支配) =====
    log("## 主軸: 発散近接度 t_div/窓長 の掃引")
    log(f"   (点数={npt0}, ノイズ={nf0} 固定。1.0 に近いほど特異点に近く観測)")
    prox_rows = [['t_div_ratio', 'true_kind', 'recovery_rate']]
    prox_conf = {}
    for prox in PROX_GRID:
        c0 = time.time()
        conf = run_recovery(npt0, nf0, N_REPS, rng, t_div_ratio=prox)
        prox_conf[prox] = conf
        r = rates_of(conf); fp = wanted_falsepos(conf)
        for tk, rr in r.items():
            prox_rows.append([prox, tk, f"{rr:.3f}"])
        log(f"[近接度={prox:.2f}] blowup回復={r['blowup']:.2f} "
            f"(lin={r['linear']:.2f} exp={r['exponential']:.2f} sat={r['saturation']:.2f}) | "
            f"望む方向偽陽性(exp→blowup)={fp:.2f}  ({time.time()-c0:.1f}s)")

    # ===== 副次グリッド: 測定解像度 × ノイズ(近接度固定) =====
    log(f"\n## 副次グリッド: 点数 × ノイズ (近接度={FIXED_PROX_FOR_GRID} 固定)")
    grid_rows = [['n_points', 'noise', 'true_kind', 'recovery_rate']]
    grid_conf = {}
    for npt in N_POINTS_GRID:
        for nf in NOISE_GRID:
            c0 = time.time()
            conf = run_recovery(npt, nf, N_REPS, rng, t_div_ratio=FIXED_PROX_FOR_GRID)
            grid_conf[(npt, nf)] = conf
            r = rates_of(conf); fp = wanted_falsepos(conf)
            for tk, rr in r.items():
                grid_rows.append([npt, nf, tk, f"{rr:.3f}"])
            log(f"[n={npt:3d} noise={nf:.2f}] blowup回復={r['blowup']:.2f} "
                f"平均={np.nanmean(list(r.values())):.2f} | 偽陽性={fp:.2f}  ({time.time()-c0:.1f}s)")

    log(f"\n# 総計算時間: {time.time()-t_start:.1f}s")

    if SMOKE:
        log(f"\n# [SMOKE] OK。本走見積り: 1セル ~{(time.time()-t_start)/(len(PROX_GRID)+len(N_POINTS_GRID)*len(NOISE_GRID)):.1f}s "
            f"× (本走 {5+9} セル) × (reps 比 {120/N_REPS:.0f}x)")
        with open("smoke_summary.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        return

    # 代表混同行列(最良近接度で)
    rep = FIXED_PROX_FOR_GRID
    log(f"\n# 代表混同行列(近接度={rep}, 点数={npt0}, ノイズ={nf0}) 行=真, 列=選択")
    log("true\\sel".ljust(13) + "".join(s[:10].ljust(12) for s in KINDS))
    cc = prox_conf[rep] if rep in prox_conf else prox_conf[min(prox_conf)]
    for tk in KINDS:
        tot = sum(cc[tk].values())
        log(tk.ljust(13) + "".join(f"{(cc[tk][sk]/tot if tot else 0):.2f}".ljust(12) for sk in KINDS))

    # ===== 判定 =====
    log(f"\n# 判定(暫定事前基準: blowup回復>={GATE_BLOWUP_RECOVERY} かつ 望む方向偽陽性<={GATE_WANTED_FALSEPOS})")
    ok_prox = [(p, rates_of(c)['blowup'], wanted_falsepos(c)) for p, c in prox_conf.items()
               if rates_of(c)['blowup'] >= GATE_BLOWUP_RECOVERY and wanted_falsepos(c) <= GATE_WANTED_FALSEPOS]
    if ok_prox:
        log("基準を満たす近接度あり:")
        for p, b, fp in sorted(ok_prox):
            log(f"  近接度={p:.2f}: blowup回復={b:.2f} 偽陽性={fp:.2f}")
        worst_ok = max(p for p, _, _ in ok_prox)
        log(f"→ 設計の含意: 観測窓が発散の近接度 {worst_ok:.2f} 倍**以内**に達すれば、")
        log(f"  β の符号性(指数 vs 発散)を判別する能力をもつ。それより遠ければ判別困難。")
        log(f"  ★パイロットへの要請: 訓練窓が「発散が起きるならその近傍まで」届くよう設計せよ。")
        log(f"  発散が窓のはるか先なら、たとえ裸 β>1 でも本実験は『不確定』に落ちる(これは棘として開示)。")
    else:
        log("いずれの近接度でも基準を満たさない。")
        log("→ 警告: この設定では、どれだけ発散に近づいても指数と発散が取り違えられる。")
        log("  設計の見直し(候補模型の精緻化・ベイズ事前情報・第二指標)を要する。")

    # 出力
    with open("recovery_proximity.csv", "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(prox_rows)
    with open("recovery_grid.csv", "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(grid_rows)
    with open("confusion_matrix.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow([f"confusion prox={rep} n={npt0} noise={nf0}", *KINDS])
        for tk in KINDS:
            tot = sum(cc[tk].values())
            w.writerow([tk, *[f"{(cc[tk][sk]/tot if tot else 0):.3f}" for sk in KINDS]])
    with open("summary.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    # 図: 主軸(blowup回復 vs 近接度) ＋ 副次グリッド(blowup回復ヒートマップ)
    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 2, figsize=(13, 4.6))
        # 左: 近接度掃引(全クラス)
        for tk in KINDS:
            ys = [rates_of(prox_conf[p])[tk] for p in PROX_GRID]
            ax[0].plot(PROX_GRID, ys, marker='o', label=tk)
        ax[0].axhline(GATE_BLOWUP_RECOVERY, ls='--', c='gray', lw=1, label=f'gate {GATE_BLOWUP_RECOVERY}')
        ax[0].set_xlabel("divergence proximity  t_div / window"); ax[0].set_ylabel("recovery rate")
        ax[0].set_title("Recovery vs how close the window reaches to divergence")
        ax[0].set_ylim(-0.02, 1.02); ax[0].legend(fontsize=8); ax[0].invert_xaxis()
        # 右: 副次グリッド blowup
        Hb = np.array([[rates_of(grid_conf[(npt, nf)])['blowup'] for nf in NOISE_GRID]
                       for npt in N_POINTS_GRID])
        im = ax[1].imshow(Hb, origin='lower', aspect='auto', cmap='viridis', vmin=0, vmax=1)
        ax[1].set_xticks(range(len(NOISE_GRID))); ax[1].set_xticklabels([f"{x:.0%}" for x in NOISE_GRID])
        ax[1].set_yticks(range(len(N_POINTS_GRID))); ax[1].set_yticklabels(N_POINTS_GRID)
        ax[1].set_xlabel("relative noise"); ax[1].set_ylabel("checkpoints"); ax[1].set_title(f"blowup recovery (prox={FIXED_PROX_FOR_GRID})")
        for ii in range(Hb.shape[0]):
            for jj in range(Hb.shape[1]):
                ax[1].text(jj, ii, f"{Hb[ii,jj]:.2f}", ha='center', va='center',
                           color='white' if Hb[ii, jj] < 0.6 else 'black')
        fig.colorbar(im, ax=ax[1], fraction=0.046)
        fig.suptitle("Model Recovery Study — can BIC tell exponential (β=1) from finite-time blowup (β>1)?")
        fig.tight_layout(); fig.savefig("recovery_figure.png", dpi=130)
        log("\nsaved: recovery_proximity.csv, recovery_grid.csv, confusion_matrix.csv, summary.txt, recovery_figure.png")
    except Exception as e:
        log(f"figure skipped: {e}")


if __name__ == "__main__":
    main()
