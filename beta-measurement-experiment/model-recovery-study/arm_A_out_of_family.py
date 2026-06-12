"""
arm_A_out_of_family.py  ―― 腕A: モデル不特定(族外)セル + 棄権の出口
=====================================================================
Claude さんの要請(#26): recovery study(腕A)は「真クラスが四候補のどれか」を
前提に判別力を測った。だが本走の S(t) は四候補族のどれでもないかもしれない。
族外データを当てはめたとき、選択器は――
  (i) 何を選ぶか。とりわけ【blowup を幻視しないか】(族外→β>1 偽陽性=利益相反の急所)
  (ii) 「上品に負ける」――どのクラスにも高い確信を出さず【棄権(不確定)】できるか。
      選んでしまうこと自体が失敗モード。「選ばない」を選べる出口が、本走の
      多重セルでの安全弁になる(Claude#26)。

利益相反の急所(本ファイルの中心):
  ★冪則成長 S∝t^q (q>1) は、超線形で加速するが【有限時間特異点を持たない】。
   これを blowup と判定すれば、それは族外域での偽 R1 そのもの。望む方向の幻視。
   族外族の中でこれを最も注視する。

α版の限定(空映/Claude/空明 の三段棚):
  - 棄権ゲートは「ノイズ尺度が既知/推定可能」を仮定(α版)。本 study では真の
    noise_frac を渡す。実データでは反復測定や高周波残差から推定 ―― β版の宿題。
  - ゲート値は族内データの相対残差から較正し、多 seed で凍結(空映の新要請を踏襲)。

走らせ方: python arm_A_out_of_family.py --smoke  /  python arm_A_out_of_family.py
依存: numpy, scipy(model_recovery 経由)。CPU のみ・GPU 不要。
"""

import sys, time
import numpy as np
import model_recovery as M

MASTER_SEED = 20260611
SMOKE = ('--smoke' in sys.argv)

if SMOKE:
    N_REPS = 10
    NOISE_GRID = [0.10]
    SEEDS = [1]
    N_CAL = 40
else:
    # miniPC で回せる規模(smoke 実測 142s/セルから逆算)。多 seed で blowup 幻視率を安定化。
    N_REPS = 100
    NOISE_GRID = [0.10, 0.20]
    SEEDS = [1, 2, 3]            # 空映の新要請: ゲート関連数字は多 seed で(3seed=平均±sd)
    N_CAL = 80

T_END = M.T_END
S0 = M.S0


# ----------------------- 族外の生成(すべて閉形式) ---------------------
# 各々「四候補族のどれでもない」よう設計。括弧内が本物の素性。
def oof_trajectory(kind, t, rng_params=None):
    p = rng_params or {}
    if kind == 'power_law_q1.5':
        # S = S0 (1 + r t)^q : 加速・超線形だが【特異点なし】(blowup と紛らわしい)
        return S0 * np.power(1.0 + 0.5 * t, 1.5)
    if kind == 'power_law_q2.5':
        return S0 * np.power(1.0 + 0.5 * t, 2.5)   # より強い加速。最も危険
    if kind == 'gompertz':
        # S = Smax exp(-B exp(-k t)) : シグモイドだが非対称(ロジスティック族外)
        Smax = S0 * 6.0
        return Smax * np.exp(-3.0 * np.exp(-0.5 * t))
    if kind == 'delayed_then_rise':
        # 前半ほぼ平坦 → 後半で急に立ち上がる(区分的・どの単一族でもない)
        return S0 * (1.0 + np.exp(2.0 * (t - 0.7 * T_END)))
    if kind == 'piecewise_lin_exp':
        # t<tc: 線形, t>=tc: 指数(変化点を持つ混成)
        tc = 0.5 * T_END
        lin = S0 + 0.45 * t
        sw = lin[np.argmin(np.abs(t - tc))]
        exp = sw * np.exp(0.45 * (t - tc))
        return np.where(t < tc, lin, exp)
    if kind == 'oscillatory_trend':
        # 線形トレンド × 振動(周期成分。どの単調族でもない)
        return (S0 + 0.45 * t) * (1.0 + 0.25 * np.sin(1.5 * t))
    if kind == 'sublinear_sqrt':
        # S = S0 + a sqrt(t) : 凹・劣線形(良性。飽和か線形に上品に落ちるはず)
        return S0 + 1.2 * np.sqrt(t)
    raise ValueError(kind)


OOF_KINDS = ['power_law_q1.5', 'power_law_q2.5', 'gompertz',
             'delayed_then_rise', 'piecewise_lin_exp', 'oscillatory_trend', 'sublinear_sqrt']
# 利益相反の急所: 加速・超線形だが特異点なし。これを blowup と呼べば偽 R1。
DANGER_OOF = ['power_law_q1.5', 'power_law_q2.5']


# ----------------------- 棄権つき選択(α版: ノイズ既知) ----------------
def winner_rel_rmse(t, S):
    """BIC 勝者の相対 RMSE(対数尺度)。族内データなら ≈ noise_frac になるはず。
       族外で勝者が当てはまらなければ、これが noise_frac より大きく膨らむ。
       戻り値: (勝者, 相対RMSE, BICマージン=次点BIC-勝者BIC≥0; 大=確信的)"""
    fits = M.fit_models(t, S)
    n = len(t)
    scored = {nm: M.aic_bic(sse, k, n)[1] for nm, (sse, k) in fits.items()}  # BIC
    order = sorted(scored, key=scored.get)
    win = order[0]
    margin = scored[order[1]] - scored[order[0]]   # ΔBIC: 勝者がどれだけ確信的か
    sse = fits[win][0]
    if not np.isfinite(sse):
        return win, np.inf, margin
    rmse = np.sqrt(sse / n)
    rel = rmse / (np.sqrt(np.mean(S ** 2)) + 1e-12)
    return win, rel, margin


def select_with_abstain(t, S, gate_rel):
    """勝者の相対 RMSE が gate_rel を超えれば『不確定(棄権)』。
       gate_rel は族内較正値 × 余裕(α版: ノイズ尺度既知の仮定)。"""
    win, rel, margin = winner_rel_rmse(t, S)
    sel = 'indeterminate' if rel > gate_rel else win
    return sel, win, rel, margin


# ----------------------- 較正: 族内の相対残差からゲートを決める --------
def calibrate_gate(noise_frac, rng, n_points=30, n_cal=None):
    n_cal = n_cal or N_CAL
    """族内(四候補)データで勝者の相対 RMSE 分布を測り、その上側(95%)を
       ゲートに採る。族内をほぼ棄権しない(偽棄権を抑える)最小ゲート。"""
    t = np.linspace(0.0, T_END, n_points)
    rels = []
    for kind in M.KINDS:
        extra = {'p': 1.6, 't_div': 1.15 * T_END} if kind == 'blowup' else \
                ({'Smax': S0 * 6.0} if kind == 'saturation' else {})
        Sc = M.true_trajectory(kind, t, S0, M.A, extra)
        if not np.all(np.isfinite(Sc)):
            continue
        for _ in range(n_cal):
            So = np.maximum(Sc * rng.normal(1.0, noise_frac, Sc.shape), 1e-6)
            _, rel, _ = winner_rel_rmse(t, So)
            if np.isfinite(rel):
                rels.append(rel)
    return float(np.percentile(rels, 95)), float(np.median(rels))


# ----------------------- セル実行 -------------------------------------
def run_oof_cell(noise_frac, gate_rel, rng, n_points=30):
    t = np.linspace(0.0, T_END, n_points)
    # 族外各クラスの選択分布 + 棄権率
    dist = {k: {sk: 0 for sk in M.KINDS + ['indeterminate']} for k in OOF_KINDS}
    raw_blow = {k: 0 for k in OOF_KINDS}     # 棄権なしでの blowup 幻視
    blow_margins = {k: [] for k in OOF_KINDS}  # 幻視 blowup の ΔBIC(確信的か周辺的か)
    for kind in OOF_KINDS:
        Sc = oof_trajectory(kind, t)
        for _ in range(N_REPS):
            So = np.maximum(Sc * rng.normal(1.0, noise_frac, Sc.shape), 1e-6)
            sel, win, _, margin = select_with_abstain(t, So, gate_rel)  # 1 fit で生勝者と棄権後を同時取得
            raw_blow[kind] += (win == 'blowup')
            if win == 'blowup':
                blow_margins[kind].append(margin)
            dist[kind][sel] += 1
    return dist, raw_blow, blow_margins


# 族内が棄権ゲートで誤って棄権される率(偽棄権=コスト)も測る
def false_abstain_rate(noise_frac, gate_rel, rng, n_points=30):
    t = np.linspace(0.0, T_END, n_points)
    ab = tot = 0
    for kind in M.KINDS:
        extra = {'p': 1.6, 't_div': 1.15 * T_END} if kind == 'blowup' else \
                ({'Smax': S0 * 6.0} if kind == 'saturation' else {})
        Sc = M.true_trajectory(kind, t, S0, M.A, extra)
        if not np.all(np.isfinite(Sc)):
            continue
        for _ in range(N_REPS):
            So = np.maximum(Sc * rng.normal(1.0, noise_frac, Sc.shape), 1e-6)
            sel, _, _, _ = select_with_abstain(t, So, gate_rel)
            ab += (sel == 'indeterminate'); tot += 1
    return ab / tot if tot else float('nan')


def main():
    lines = []
    def log(m): print(m, flush=True); lines.append(m)
    t0 = time.time()
    log(f"# 腕A 族外(out-of-family)+ 棄権の出口  {'[SMOKE]' if SMOKE else '[本走]'}")
    log(f"# seed={MASTER_SEED} reps/class={N_REPS} noise={NOISE_GRID} seeds={SEEDS}")
    log(f"# 急所: 冪則成長(特異点なし超線形)を blowup と幻視するか = 族外域の偽R1")
    log("")

    for noise in NOISE_GRID:
        # --- ゲート較正(多 seed 平均: 空映の新要請) ---
        gates, meds = [], []
        for sd in SEEDS:
            g, md = calibrate_gate(noise, np.random.default_rng(MASTER_SEED + sd))
            gates.append(g); meds.append(md)
        gate_rel = float(np.mean(gates))
        log(f"## ノイズ={noise:.2f}  族内較正: 勝者相対RMSE 中央値={np.mean(meds):.3f} "
            f"→ 棄権ゲート(族内95%上側,{len(SEEDS)}seed平均)={gate_rel:.3f} ±{np.std(gates):.3f}")

        # --- 偽棄権率(族内をどれだけ誤棄権するか=ゲートのコスト) ---
        fa = np.mean([false_abstain_rate(noise, gate_rel, np.random.default_rng(MASTER_SEED + 100 + sd))
                      for sd in SEEDS])
        log(f"   族内 偽棄権率(コスト)={fa:.3f}")

        # --- 族外セル(多 seed 平均) ---
        agg = {k: {sk: 0.0 for sk in M.KINDS + ['indeterminate']} for k in OOF_KINDS}
        raw_b = {k: [] for k in OOF_KINDS}
        margins = {k: [] for k in OOF_KINDS}
        for sd in SEEDS:
            dist, raw_blow, bm = run_oof_cell(noise, gate_rel, np.random.default_rng(MASTER_SEED + 200 + sd))
            for k in OOF_KINDS:
                tot = sum(dist[k].values())
                for sk in agg[k]:
                    agg[k][sk] += dist[k][sk] / tot / len(SEEDS)
                raw_b[k].append(raw_blow[k] / N_REPS)
                margins[k].extend(bm[k])

        log(f"   族外クラス別 → 選択分布(多seed平均) と blowup幻視率")
        log(f"   {'oof_class':<20}{'→lin':>6}{'exp':>6}{'blow':>6}{'sat':>6}{'INDET':>7} | "
            f"{'raw_blow(棄権なし)':>18}")
        for k in OOF_KINDS:
            a = agg[k]
            mark = '  ★危険' if k in DANGER_OOF else ''
            rb_m, rb_s = np.mean(raw_b[k]), np.std(raw_b[k])
            log(f"   {k:<20}{a['linear']:>6.2f}{a['exponential']:>6.2f}{a['blowup']:>6.2f}"
                f"{a['saturation']:>6.2f}{a['indeterminate']:>7.2f} | "
                f"raw_blow={rb_m:.2f}±{rb_s:.2f}{mark}")

        # --- 急所サマリ: 危険族(冪則)の blowup 幻視、棄権あり/なし ---
        dn_raw = np.mean([np.mean(raw_b[k]) for k in DANGER_OOF])
        dn_gated = np.mean([agg[k]['blowup'] for k in DANGER_OOF])
        dn_indet = np.mean([agg[k]['indeterminate'] for k in DANGER_OOF])
        log(f"   ▶ 急所(冪則・特異点なし超線形): blowup幻視 棄権なし={dn_raw:.2f}±"
            f"{np.std([np.mean(raw_b[k]) for k in DANGER_OOF]):.2f} "
            f"→ 棄権あり={dn_gated:.2f}  (うち不確定へ退避={dn_indet:.2f})")

        # --- 全族外の blowup 幻視サマリ + 幻視の確信度(ΔBIC margin) ---
        #    幻視が「確信的(大margin)」なら適合度ゲートでは捕まらない=β版で別ゲートが要る。
        #    「周辺的(小margin)」なら margin ゲートで捕まえられる=β版の安価な修正。
        all_blow = {k: np.mean(raw_b[k]) for k in OOF_KINDS if np.mean(raw_b[k]) > 0.005}
        if all_blow:
            log(f"   ▶ blowup を幻視した族外族(棄権なし生率) と 幻視時のΔBIC中央値:")
            for k in sorted(all_blow, key=all_blow.get, reverse=True):
                mm = np.median(margins[k]) if margins[k] else float('nan')
                conf = "確信的(GoFゲート素通り)" if mm > 6 else "周辺的(marginゲートで捕捉可)"
                log(f"       {k:<20} 幻視率={all_blow[k]:.2f}  ΔBIC中央={mm:>6.1f}  {conf}")
        else:
            log(f"   ▶ どの族外も blowup を幻視せず(全族外で生率≤0.005)")
        log("")

    log(f"# 総時間: {time.time()-t0:.1f}s")
    if SMOKE:
        log(f"# [SMOKE] OK。本走見積り: 現{time.time()-t0:.1f}s × (noise {len(NOISE_GRID)}/1) "
            f"× (reps {120/N_REPS:.0f}x) × (seeds {len(SEEDS)}/1 → 本走5)")
    out = "arm_A_oof_smoke.txt" if SMOKE else "arm_A_oof_summary.txt"
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    log(f"saved: {out}")


if __name__ == "__main__":
    main()
