"""
auto_judge.py  ―― #27: 自動判定の全セル評価 + 棄権込み再導出 + 原理/校正分離(α版)
=====================================================================================
過去のバグ#4: 自動判定が【主軸セルしか評価せず】n=60 の合格を見落とした。
本モジュールはその家系を構造的に潰す。三鏡(#27)の結線した追加を一体化:

  (1) 全セル評価       ―― 主軸だけでなく全格子セルにゲート原理を適用(バグ#4の回帰防止)。
  (2) 原理/校正の分離  ―― ゲートの【論理形(原理)】と【現在の実測しきい値(校正値)】を
                          コード上で分離。台帳は原理を保持、校正値は再導出可能な実測。
  (3) α版ラベル        ―― 全出力に仮定(乗法i.i.d.・族内生成・棄権はノイズ尺度既知)を明記。
  (4) 棄権=独立カテゴリ ―― INDET を「正解」でも「誤り」でもない第三のカテゴリとして集計
                          (Claude#27-4)。回復率・偽陽性の分母は全試行(棄権を含む)。
  (5) 棄権有効で再導出  ―― これまでの腕A 主要数字(blowup回復1.00 等)は棄権ゲート【なし】で
                          測られた。v1.x で棄権を採るなら、ゲート【有効】で主要数字を
                          再導出しないと校正値とパイプラインが食い違う(Claude#27-2)。
                          ゲートの値段(族内偽棄権 → 実効検定力の目減り)を実数で出す。

監視可能性は治具の一部(空映/Claude): 逐次 flush 印字。最重条件で smoke を測ってから外挿。

走らせ方: python auto_judge.py --smoke  /  python auto_judge.py
依存: numpy, scipy(model_recovery, arm_A_out_of_family 経由)。CPU のみ。
"""

import sys, time
import numpy as np
import model_recovery as M
import arm_A_out_of_family as OOF

MASTER_SEED = 20260611
SMOKE = ('--smoke' in sys.argv)

# =====================================================================
# (2)(3) ゲートの原理 / 校正値 ―― コード上で分離。台帳が原理を保持。
# =====================================================================
# 【原理】= 論理形。恒久。実測値が変わっても、この形は変わらない。
GATE_PRINCIPLE = (
    "腕A は単独で R0/R1 を決めない(正典の AND 構造)。腕A の合格条件 = "
    "[ blowup(β>1) 回復率 ≥ R_min ] かつ [ 指数→blowup(望む方向偽陽性) ≤ FP_max ]。"
    "棄権(INDET)は独立カテゴリ。回復率・偽陽性の分母は全試行(棄権込み)。"
    "ゲートを採るなら主要数字はゲート有効で再導出する。"
)
# 【校正値】= 現在の実測しきい値。α版(下記 ASSUMPTIONS の内側)。多 seed で凍結。
CALIBRATION = {
    'R_min': 0.80,        # blowup 回復率の下限(暫定事前基準)
    'FP_max': 0.10,       # 望む方向偽陽性の上限(暫定事前基準)
    'n_points_cal': 60,   # 腕A 較正値: この点数以上で合格(現在の実測。原理ではない)
    'noise_ceiling': 0.10,  # ★両腕にまたがる load-bearing なノイズ天井(空映)
}
ASSUMPTIONS = ("α版: 乗法 i.i.d. ノイズ・族内(線形/指数/発散/飽和)生成・"
               "棄権ゲートはノイズ尺度既知を仮定。族外・実測ノイズ形・系レベル校正は β 版送り。")

# ---- 走行行列(最重条件=n60×noise0.20 を smoke で先に測る規則) ----
if SMOKE:
    N_REPS = 20
    NPTS_GRID = [60]          # 最重(点数多→fit 重)
    NOISE_GRID = [0.20]       # 最重(高ノイズ→収束遅)
    SEEDS = [1]
else:
    N_REPS = 60               # 多 seed(3)×60=180 有効標本/セル。対角率に十分。
    NPTS_GRID = [30, 60]      # 15 は既に全ノイズで不合格。関心域に絞る。
    NOISE_GRID = [0.05, 0.10, 0.20]
    SEEDS = [1, 2, 3]         # ゲート【出力】数字は多 seed(空映の新要請)

INDET = 'indeterminate'
CATS = M.KINDS + [INDET]


def gated_recovery(n_points, noise, gate_rel, rng):
    """棄権ゲート【有効】で族内 recovery を測る。
       戻り値: confusion[true][sel∈KINDS+INDET]。INDET は独立カテゴリ。"""
    t = np.linspace(0.0, M.T_END, n_points)
    conf = {tk: {sk: 0 for sk in CATS} for tk in M.KINDS}
    for true_kind in M.KINDS:
        extra = {'p': 1.6, 't_div': 1.15 * M.T_END} if true_kind == 'blowup' else \
                ({'Smax': M.S0 * 6.0} if true_kind == 'saturation' else {})
        Sc = M.true_trajectory(true_kind, t, M.S0, M.A, extra)
        if not np.all(np.isfinite(Sc)):
            continue
        for _ in range(N_REPS):
            So = np.maximum(Sc * rng.normal(1.0, noise, Sc.shape), 1e-6)
            sel, _, _, _ = OOF.select_with_abstain(t, So, gate_rel)
            conf[true_kind][sel] += 1
    return conf


def rates_with_indet(conf):
    """全試行を分母に: 回復率(対角)・棄権率(INDET)を、棄権込みの分母で。"""
    out = {}
    for tk in M.KINDS:
        tot = sum(conf[tk].values())
        out[tk] = {
            'recovery': conf[tk][tk] / tot if tot else float('nan'),     # 正解(全試行分母)
            'indet': conf[tk][INDET] / tot if tot else float('nan'),     # 棄権(独立)
        }
    # 望む方向偽陽性: 指数 → blowup(全試行分母、棄権込み)
    se = sum(conf['exponential'].values())
    out['wanted_fp'] = conf['exponential']['blowup'] / se if se else float('nan')
    return out


def judge_cell(r):
    """(1) 全セルにゲート原理を適用。PASS/FAIL/(棄権過多)を返す。"""
    blow = r['blowup']['recovery']
    fp = r['wanted_fp']
    passed = (blow >= CALIBRATION['R_min']) and (fp <= CALIBRATION['FP_max'])
    return 'PASS' if passed else 'FAIL', blow, fp


def main():
    lines = []
    def log(m): print(m, flush=True); lines.append(m)
    t0 = time.time()
    log(f"# auto_judge {'[SMOKE]' if SMOKE else '[本走]'} ―― 全セル評価+棄権込み再導出(α版)")
    log(f"# {ASSUMPTIONS}")
    log(f"# 原理: {GATE_PRINCIPLE}")
    log(f"# 校正値: {CALIBRATION}")
    log(f"# seed={MASTER_SEED} reps={N_REPS} npts={NPTS_GRID} noise={NOISE_GRID} seeds={SEEDS}")
    log("")
    log(f"  {'npts':>4} {'noise':>5} | {'blowup回復':>9} {'望む偽陽性':>9} "
        f"{'判定':>5} | {'棄権率(lin/exp/blow/sat)':>26}")
    log("-" * 80)

    judged = []  # (npts, noise, verdict, blow, fp)
    for npts in NPTS_GRID:
        for noise in NOISE_GRID:
            # --- ゲート較正 ---
            # gate_rel は閾値(中間量)。その多 seed sd は腕B study で ≤0.002 と実証済み
            # ゆえ単一 seed・n_cal=60 で足りる(出力数字=回復/偽陽性は下で多 seed)。
            gate_rel = OOF.calibrate_gate(noise, np.random.default_rng(MASTER_SEED + 7),
                                          n_points=npts, n_cal=60)[0]
            # --- 棄権有効で recovery 再導出(多 seed 平均) ---
            agg = {tk: {'recovery': [], 'indet': []} for tk in M.KINDS}
            fps = []
            for s in SEEDS:
                conf = gated_recovery(npts, noise, gate_rel,
                                      np.random.default_rng(MASTER_SEED + 300 + s))
                r = rates_with_indet(conf)
                for tk in M.KINDS:
                    agg[tk]['recovery'].append(r[tk]['recovery'])
                    agg[tk]['indet'].append(r[tk]['indet'])
                fps.append(r['wanted_fp'])
            rmean = {tk: {'recovery': np.mean(agg[tk]['recovery']),
                          'indet': np.mean(agg[tk]['indet'])} for tk in M.KINDS}
            rmean['wanted_fp'] = np.mean(fps)
            verdict, blow, fp = judge_cell(rmean)
            judged.append((npts, noise, verdict, blow, fp))
            indet_str = "/".join(f"{rmean[k]['indet']:.2f}" for k in M.KINDS)
            log(f"  {npts:>4} {noise:>5.2f} | {blow:>9.2f} {fp:>9.2f} "
                f"{verdict:>5} | {indet_str:>26}")

    # ===== (1) 全セル評価のサマリ(バグ#4: 主軸だけ見ない) =====
    log("")
    passes = [j for j in judged if j[2] == 'PASS']
    log(f"# 全 {len(judged)} セルを評価(主軸だけでない)。PASS={len(passes)} / {len(judged)}")
    if passes:
        log(f"# 棄権ゲート有効で合格するセル(校正値 R_min={CALIBRATION['R_min']} "
            f"FP_max={CALIBRATION['FP_max']} の内側):")
        for npts, noise, v, blow, fp in passes:
            ceil = "≤天井" if noise <= CALIBRATION['noise_ceiling'] else "★天井超"
            log(f"    n={npts} noise={noise:.2f}({ceil}): blowup回復={blow:.2f} 偽陽性={fp:.2f}")
    else:
        log("# 棄権ゲート有効では、いずれのセルも校正値を満たさない(再導出の含意)。")

    # ===== (5) 棄権の値段: ゲート無し(既存) vs ゲート有り(本走)の食い違い =====
    log("")
    log("# 棄権の値段(Claude#27-2): 既存の腕A 数字はゲート【なし】。上表はゲート【有り】。")
    log("# 族内が INDET へ抜ける分、ゲート有りの blowup回復はゲートなし(≈1.00)より下がりうる。")
    log("# → v1.x で棄権を採るなら、校正値はこのゲート有り表から取る(食い違い回避)。")

    log(f"\n# 総時間: {time.time()-t0:.1f}s")
    if SMOKE:
        ncell_full = len([1 for _ in [30, 60] for _ in [0.05, 0.10, 0.20]])
        log(f"# [SMOKE] OK。本走見積り(最重条件 n60×noise0.20 を測った): "
            f"現{time.time()-t0:.1f}s × (セル {ncell_full}/{len(NPTS_GRID)*len(NOISE_GRID)}) "
            f"× (reps {100/N_REPS:.0f}x) × (seeds 3/{len(SEEDS)})")
        log("# ★最重条件で測ったので、これは上限寄りの外挿(空映/Claudeの新規則)。")
    out = "auto_judge_smoke.txt" if SMOKE else "auto_judge_summary.txt"
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    log(f"saved: {out}")


if __name__ == "__main__":
    main()
