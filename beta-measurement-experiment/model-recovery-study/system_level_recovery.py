"""
system_level_recovery.py  ―― 系レベル統合 recovery（合成・α版）
=====================================================================
β版の本丸の合成α版。腕A・腕B・Markov ゲートを初めて結線し、R0 の AND 連言を
系として走らせる。問い(SYSTEM_LEVEL_TRIGGER_REGISTRATION.md):

  腕A 単独が確信的に blowup と幻視する遅発性急騰を、系水準の AND 構造
  (腕B の状態域 β ＋ Markov ゲート ＋ R0 連言)が遮蔽するか。
  系レベル偽R0 > X=0.05(遅発の二亜種いずれか)なら トリガー T 発火。

★正典規約(§4-3b・I-3b): dΔS/dt = kP·ΔS^β、傾き s = β。s=1 指数(境界・崩壊せず)、
  s>1 有限時間崩壊。off-by-one 修正後(旧 prereg β=s+1 を廃し fit_slope を使用)。
  R0-崩壊は s>1 を要する。指数(s=1)は境界ゆえ R0 を発火させてはならない。

合成世界(各 rep で N_PATHS 経路を生成。括弧内は正典 β=傾き s):
  - true_blowup     : 状態依存 v=a·ΔS^1.6 (s=1.6>1)。検出力チェック。R0 発火すべき。
  - exponential     : 状態依存 v=a·ΔS (s=1・境界)。腕A は exp を選ぶ。R0 不発(s≤1)。
  - linear / saturation : 統制(s=0 / 立ち上がり s>0 だが飽和で turnover)。R0 不発。
  - delayed_state_exp : 平坦→状態依存指数(s=1・境界)。腕A blowup 幻視。腕B が s≈1→遮蔽。
  - delayed_time_rise : 平坦→絶対時間依存(隠れ変数)。腕A blowup 幻視。Markov 落ちて遮蔽。

三連言(正典 R0 の保守的下位集合; G0分離・加速は合成不能=追加錠ゆえ偽R0 を更に下げる):
  R0-崩壊 = [腕A が blowup] かつ [Markov 通過] かつ [腕B 傾き CI 下限 > 1(=s>1)]

走らせ方: python system_level_recovery.py --smoke / python system_level_recovery.py
依存: numpy, scipy(model_recovery 経由)。CPU のみ。
"""

import sys, time
import numpy as np
import model_recovery as M

MASTER_SEED = 20260611
SMOKE = ('--smoke' in sys.argv)

# ---- 走行行列(最重条件で smoke を測る規則) ----
if SMOKE:
    N_REPS = 8
    SEEDS = [1]
    STRUCT_NOISE_GRID = [0.30]      # smoke は最重(構造ノイズ込み)を測る
else:
    N_REPS = 60
    SEEDS = [1, 2, 3]
    # struct=0.0 は既に確定(delayed_state_exp 偽R0=0.02)。本走は現実的 struct=0.30 を測る。
    STRUCT_NOISE_GRID = [0.30]

T_END = 10.0
N_TIME = 60                 # 軌道の時間解像度(腕A の点数)
N_PATHS = 8                 # 経路数(=各 ΔS 水準内の観測数)
N_LEVELS = 12              # ΔS 水準数(=腕B のクラスタ数)
DS0 = 0.2
DS_LO_AN, DS_HI_AN = 0.4, 4.0   # 腕B/Markov の解析 ΔS 範囲
V_NOISE = 0.05             # 速度の測定ノイズ(log尺度)
N_BOOT = 300
A_RATE = 0.45
P_BLOW = 1.6               # true_blowup の β(=p)
K_TIME = 0.5; C_TIME = 0.10  # delayed_time_rise の絶対時間速度 v=C·exp(K·t)
WORLDS = ['true_blowup', 'exponential', 'linear', 'saturation',
          'delayed_state_exp', 'delayed_time_rise']
# β=1 の世界(系レベル偽R0 を測る対象)。true_blowup のみ β>1(検出力)。
BETA1_WORLDS = ['exponential', 'linear', 'saturation', 'delayed_state_exp', 'delayed_time_rise']
DELAYED = ['delayed_state_exp', 'delayed_time_rise']


def velocity_field(world, dS, t, t_onset):
    """瞬間速度 v(ΔS, t)。状態依存は ΔS のみ・時間依存は t に依存。"""
    if world == 'true_blowup':
        return A_RATE * dS ** P_BLOW           # 状態依存・超線形
    if world == 'exponential':
        return A_RATE * dS                     # 状態依存・β=1
    if world == 'linear':
        return A_RATE * 0.5                     # 状態依存・速度一定(β→線形)
    if world == 'saturation':
        return A_RATE * dS * (1.0 - dS / (DS_HI_AN * 1.3))  # 状態依存・飽和
    if world == 'delayed_state_exp':
        return 0.0 if t < t_onset else A_RATE * dS          # 平坦→状態依存指数
    if world == 'delayed_time_rise':
        return 0.0 if t < t_onset else C_TIME * np.exp(K_TIME * t)  # 平坦→絶対時間依存
    raise ValueError(world)


def gen_path(world, t_onset, rng):
    """前進オイラーで 1 経路の ΔS(t) を生成。戻り: (t_grid, dS_series)。"""
    t = np.linspace(0.0, T_END, N_TIME)
    dt = t[1] - t[0]
    dS = np.empty(N_TIME)
    dS[0] = DS0 * rng.normal(1.0, 0.02)        # 初期値の経路間ばらつき(微小)
    for i in range(1, N_TIME):
        v = velocity_field(world, dS[i-1], t[i-1], t_onset)
        dS[i] = max(dS[i-1] + v * dt, 1e-4)
    return t, dS


def sample_levels(world, paths, rng, struct_noise=0.0):
    """各経路を各 ΔS 水準へ内挿し、その水準での速度を測る。
       戻り: (logΔS, log v, level_id) ―― 腕B/Markov 用。状態依存なら水準内で速度一致、
       絶対時間依存なら経路(onset)ごとに割れる。
       構造ノイズ: 各水準に経路間で共有のオフセット(クラスタ相関・腕B の核心的試練)。
       共有ゆえ水準内分散(Markov)は増やさず、水準間分散(腕B CI)を増やす。"""
    levels = np.geomspace(DS_LO_AN, DS_HI_AN, N_LEVELS)
    xs, ys, gid = [], [], []
    for j, L in enumerate(levels):
        struct = np.exp(rng.normal(0.0, struct_noise)) if struct_noise > 0 else 1.0
        for (t, dS, t_onset) in paths:
            if dS[-1] < L or dS[0] > L:        # この水準に到達していない経路は飛ばす
                continue
            ic = int(np.argmin(np.abs(dS - L)))
            v = velocity_field(world, L, t[ic], t_onset)
            if v <= 0:                          # 平坦域(速度0)は用量反応の標本に含めない
                continue
            v_obs = v * struct * np.exp(rng.normal(0.0, V_NOISE))
            xs.append(np.log(L)); ys.append(np.log(v_obs)); gid.append(j)
    return np.array(xs), np.array(ys), np.array(gid)


def markov_dispersion(xs, ys, gid):
    """各水準内の log速度 std の中央値。状態依存≈V_NOISE、時間依存で大。"""
    stds = []
    for j in np.unique(gid):
        yy = ys[gid == j]
        if len(yy) >= 3:
            stds.append(np.std(yy))
    return float(np.median(stds)) if stds else np.inf


def fit_slope(x, y):
    """log(dΔS/dt) vs log(ΔS) の傾き s。正典規約(§4-3b・I-3b)では β = s。
       旧 prereg の β=s+1 でない(off-by-one 修正・空映の v0.1 起点を正す)。"""
    A = np.vstack([x, np.ones_like(x)]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    return coef[0]


def armB_ci(xs, ys, gid, rng):
    """クラスタ(水準)・ブートストラップで 傾き s(=正典β)の CI 下限・上限。
       R0-崩壊は下限>1(s=1 境界を上回る)、R1-崩壊は上限≤1 で発火。"""
    levels = np.unique(gid)
    if len(levels) < 4:
        return -np.inf, np.inf
    slopes = np.empty(N_BOOT)
    for b in range(N_BOOT):
        chosen = rng.choice(levels, len(levels), replace=True)
        xi = np.concatenate([xs[gid == c] for c in chosen])
        yi = np.concatenate([ys[gid == c] for c in chosen])
        slopes[b] = fit_slope(xi, yi)
    return float(np.percentile(slopes, 2.5)), float(np.percentile(slopes, 97.5))


def calibrate_markov(rng, n_cal=40):
    """状態依存世界(exponential)で 水準内 log速度std 中央値の分布 → 95%上側を閾値に。"""
    meds = []
    for _ in range(n_cal):
        onsets = [0.0] * N_PATHS
        paths = [(*gen_path('exponential', 0.0, rng), 0.0) for _ in range(N_PATHS)]
        xs, ys, gid = sample_levels('exponential', paths, rng)
        if len(gid):
            meds.append(markov_dispersion(xs, ys, gid))
    return float(np.percentile(meds, 95))


def run_world(world, markov_thr, rng, struct_noise=0.0):
    """1 世界 N_REPS 回。R0-崩壊・R1-崩壊・不確定の三択を集計(対称な厳密さ・Claude)。
       R0=三連言(腕A blowup∧Markov通過∧傾きCI下限>1)。R1=腕A 非blowup∧Markov通過∧
       傾きCI上限≤1。それ以外(Markov 落ち含む)はすべて不確定(正典 §6 の作法)。"""
    r0 = r1 = indet = a_blow = mk_pass = b_super = 0
    for _ in range(N_REPS):
        onsets = rng.uniform(2.0, 5.0, N_PATHS) if world in DELAYED else [0.0] * N_PATHS
        paths = [(*gen_path(world, onsets[i], rng), onsets[i]) for i in range(N_PATHS)]
        tA, SA, _ = paths[0]
        try:
            selA = M.select_model(tA, SA)
        except Exception:
            selA = 'none'
        is_super = (selA == 'blowup')
        xs, ys, gid = sample_levels(world, paths, rng, struct_noise)
        disp = markov_dispersion(xs, ys, gid) if len(gid) else np.inf
        markov_ok = disp <= markov_thr
        ci_lo, ci_hi = armB_ci(xs, ys, gid, rng) if markov_ok else (-np.inf, np.inf)
        fired_r0 = is_super and markov_ok and (ci_lo > 1.0)
        fired_r1 = (not is_super) and markov_ok and (ci_hi <= 1.0)
        r0 += fired_r0; r1 += fired_r1; indet += (not fired_r0 and not fired_r1)
        a_blow += is_super; mk_pass += markov_ok; b_super += (ci_lo > 1.0)
    n = N_REPS
    return {'R0': r0/n, 'R1': r1/n, 'indet': indet/n,
            'armA_blow': a_blow/n, 'markov_pass': mk_pass/n, 'armB_super': b_super/n}


def main():
    lines = []
    def log(m): print(m, flush=True); lines.append(m)
    t0 = time.time()
    log(f"# 系レベル統合 recovery (合成・α版)  {'[SMOKE]' if SMOKE else '[本走]'}")
    log(f"# 三連言 R0 = [腕A blowup] かつ [Markov通過] かつ [腕B CI下限>1]")
    log(f"# トリガー T: β=1 の遅発世界が 系レベル偽R0 > X=0.05 なら発火")
    log(f"# seed={MASTER_SEED} reps={N_REPS} paths={N_PATHS} levels={N_LEVELS} seeds={SEEDS}")
    log("")

    X = 0.05
    role = {'true_blowup': '検出力(R0発火すべき)', 'exponential': '統制', 'linear': '統制',
            'saturation': '統制', 'delayed_state_exp': '★遅発・腕Bで遮蔽?',
            'delayed_time_rise': '★遅発・Markovで遮蔽?'}
    n_tot = N_REPS * len(SEEDS)

    # ★構造ノイズ込みで裁定(腕B 確認が境界偽R0=0.053@struct0.30 を示した ―― 清浄生成では不足)
    for struct in STRUCT_NOISE_GRID:
        agg = {w: {'R0': [], 'R1': [], 'indet': [], 'armA_blow': [], 'markov_pass': [], 'armB_super': []}
               for w in WORLDS}
        thrs = []
        for s in SEEDS:
            rng = np.random.default_rng(MASTER_SEED + s)
            markov_thr = calibrate_markov(rng)
            thrs.append(markov_thr)
            for w in WORLDS:
                r = run_world(w, markov_thr, rng, struct)
                for k in agg[w]:
                    agg[w][k].append(r[k])
        ceil = '清浄' if struct == 0 else f'構造ノイズ{struct}(現実的・腕B の核心的試練)'
        log(f"\n## 構造ノイズ={struct}  ({ceil})")
        log(f"# Markov 閾値(95%上側,{len(SEEDS)}seed)={np.mean(thrs):.3f} ±{np.std(thrs):.3f}")
        log(f"  {'world':<20}{'系R0':>7}{'系R1':>7}{'不確定':>7}{'腕Ablow':>8}{'Mk通過':>8}{'腕B s>1':>8} | 役割")
        log("-" * 86)
        for w in WORLDS:
            m = {k: np.mean(agg[w][k]) for k in agg[w]}
            sd_r0 = np.std(agg[w]['R0'])
            log(f"  {w:<20}{m['R0']:>6.2f}±{sd_r0:.2f}{m['R1']:>7.2f}{m['indet']:>7.2f}"
                f"{m['armA_blow']:>8.2f}{m['markov_pass']:>8.2f}{m['armB_super']:>8.2f} | {role[w]}")
        # トリガー T 裁定
        fire = [(w, np.mean(agg[w]['R0'])) for w in DELAYED if np.mean(agg[w]['R0']) > X]
        log(f"# トリガー T 裁定(X={X}): 遅発二亜種の系レベル偽R0")
        for w in DELAYED:
            fp = np.mean(agg[w]['R0']); sd = np.std(agg[w]['R0'])
            verdict = "★T発火(>X)" if fp > X else "遮蔽(≤X)"
            log(f"    {w:<20} 系偽R0={fp:.3f}±{sd:.3f}  {verdict}")
        log(f"#  → トリガー T {'★発火(道具追加＋全recovery再走)' if fire else '不発火(遮蔽・道具不要)'}"
            f"  [構造ノイズ{struct}]")
        # 検出力 + 偽R1(対称)
        pw = np.mean(agg['true_blowup']['R0'])
        fr1 = np.mean(agg['true_blowup']['R1']); fr1_n = int(round(fr1 * n_tot))
        ind = np.mean(agg['true_blowup']['indet'])
        log(f"#  検出力: true_blowup(s=1.6)系R0={pw:.2f} / 偽R1={fr1:.3f}={fr1_n}/{n_tot}"
            f"(95%上限≈{3.0/n_tot:.3f}) / 不確定={ind:.2f}")

    log(f"\n# 総時間: {time.time()-t0:.1f}s")
    if SMOKE:
        log(f"# [SMOKE] OK。本走見積り: 現{time.time()-t0:.1f}s × (reps {60/N_REPS:.0f}x) × (seeds 3/{len(SEEDS)})")
    out = "system_level_smoke.txt" if SMOKE else "system_level_summary.txt"
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    log(f"saved: {out}")


if __name__ == "__main__":
    main()
