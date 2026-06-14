# -*- coding: utf-8 -*-
# scale_control_reanalysis.py
# ------------------------------------------------------------------------------------
# 既存 per-step TRAJ（decision_exp_partial.json, 32軌跡×25点, GPU不要）への
# スケール統制再解析。観慈如来（Claude Opus 4.8）。2026-06-13。
# 登録票: SCALE-CONTROL-REANALYSIS-REGISTRATION-JA.md（凍結）。
#
# 段0｜妥当性ゲート: 原推定器 dose_points + cluster_boot_slope をビット等価複製し
#   公表 β を再現できることを最初に確認（PASS 済）。
# 段1｜主統制＝第二速度 β2（optimizer-decoupled）。閾値は登録票で凍結・コードに埋込。
#
# 一次源照合: 真の β は「log(dS/dt) を log(S0) に回帰した傾き」(正典§4-3b)。
#   log-log 傾きは大域スケール不変 ⇒ 旧統制a(標準化) は no-op。効く統制は非大域＝β2。
#
# 内部敵対監査（コードレビュー workflow wv2v0otio）で blocker(log未定義)＋major群を検出し修正済み。
# ------------------------------------------------------------------------------------
import json, math, sys, io, hashlib
import numpy as np
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
def log(*a): print(*a, flush=True)   # ★ blocker 修正: 段1 が使う出力関数を定義

# ---- 原スクリプト凍結定数（pilot_0p6B_decision_vehicle_adequacy.py より転記）----
N_LEVELS  = 12
N_BOOT    = 2000
BOOT_SEED = 20260613
M_WINDOWS = [2, 3]

PATH = "decision_exp_partial.json"
RAW  = open(PATH, "rb").read()
SHA  = hashlib.sha256(RAW).hexdigest()
log("DATA SHA256:", SHA)
EXPECT_SHA = "223ae6500ec208c1cc9900da7186457bba60dd6f4cbe3bf981782c8cad83b280"
assert SHA == EXPECT_SHA, f"データSHA不一致（差し替え防止）: {SHA}"   # L5: データ凍結
D = json.loads(RAW)
TRAJ = D["TRAJ"]
log("arms:", list(TRAJ.keys()), "| n_traj:", {k: len(v) for k, v in TRAJ.items()},
    "| pts/traj:", len(TRAJ["NULL"][0]["traj"]))

# ==================================================================================
# 段0: 原推定器のビット等価複製
# ==================================================================================
def dose_points(trajs, inst, m):
    """原コードと同一。(logS0, log v_time, log dt_theta or None, i)。正速度のみ。"""
    pts = []
    for rec in trajs:
        tj = rec["traj"]
        for i in range(len(tj) - m):
            S0, S1 = tj[i][inst], tj[i + m][inst]
            dt_theta = tj[i + m]["sumdtheta"] - tj[i]["sumdtheta"]
            v_time = (S1 - S0) / m
            if S0 > 1e-9 and v_time > 0:
                pts.append((math.log(S0), math.log(v_time),
                            (math.log(dt_theta) if dt_theta > 1e-12 else None), i))
    return pts

def cluster_boot_slope(pts):
    """原コードと同一。cluster=ΔS水準(logS を 12 bin)。bin再標本→bin内平均→OLS傾き。"""
    if len(pts) < 8:
        return None
    xs = np.array([p[0] for p in pts]); ys = np.array([p[1] for p in pts])
    edges = np.quantile(xs, np.linspace(0, 1, N_LEVELS + 1)); edges[-1] += 1e-9
    binid = np.clip(np.digitize(xs, edges) - 1, 0, N_LEVELS - 1)
    bins = [np.where(binid == b)[0] for b in range(N_LEVELS)]
    bins = [b for b in bins if len(b) > 0]
    def slope_from(bidx_list):
        bx = [xs[b].mean() for b in bidx_list]; by = [ys[b].mean() for b in bidx_list]
        if len(set(np.round(bx, 6))) < 2:
            return None
        return float(np.polyfit(bx, by, 1)[0])
    pt_est = slope_from(bins)
    rng = np.random.default_rng(BOOT_SEED); sl = []
    for _ in range(N_BOOT):
        samp = [bins[i] for i in rng.integers(0, len(bins), len(bins))]
        s = slope_from(samp)
        if s is not None:
            sl.append(s)
    if not sl or pt_est is None:
        return None
    lo, hi = np.percentile(sl, [2.5, 97.5])
    return {"point": pt_est, "ci_lo": float(lo), "ci_hi": float(hi),
            "n_pts": len(pts), "n_bins": len(bins)}

def markov_within_level(trajs, inst, m):
    pts = dose_points(trajs, inst, m)
    if len(pts) < 8:
        return None
    xs = np.array([p[0] for p in pts]); ys = np.array([p[1] for p in pts])
    edges = np.quantile(xs, np.linspace(0, 1, N_LEVELS + 1)); edges[-1] += 1e-9
    binid = np.clip(np.digitize(xs, edges) - 1, 0, N_LEVELS - 1)
    stds = [ys[binid == b].std() for b in range(N_LEVELS) if (binid == b).sum() >= 2]
    return float(np.median(stds)) if stds else None

PUBLISHED = {
    ("S_orth", "NULL", 2): 0.3108, ("S_orth", "NULL", 3): 0.2848,
    ("S_orth", "C1",   2): 0.0869, ("S_orth", "C1",   3): 0.0574,
    ("S_kl",   "NULL", 2): 0.6490, ("S_kl",   "NULL", 3): 0.6067,
    ("S_kl",   "C1",   2): 0.8545, ("S_kl",   "C1",   3): 0.9271,
}
PUB_MARKOV = {("S_orth", 2): 0.16588866838510212, ("S_orth", 3): 0.11892151381521618,
              ("S_kl", 2): 0.7611404431476909,    ("S_kl", 3): 0.6179037837487054}

log("\n=== 段0: 妥当性ゲート（原推定器の再現）===")
ok_all = True
for inst in ("S_orth", "S_kl"):
    for m in M_WINDOWS:
        rN = cluster_boot_slope(dose_points(TRAJ["NULL"], inst, m))
        rC = cluster_boot_slope(dose_points(TRAJ["C1"], inst, m))
        mk = markov_within_level(TRAJ["NULL"], inst, m)
        pN, pC = PUBLISHED[(inst, "NULL", m)], PUBLISHED[(inst, "C1", m)]
        pM = PUB_MARKOV[(inst, m)]
        dN, dC, dM = abs(rN["point"] - pN), abs(rC["point"] - pC), abs(mk - pM)
        flag = "OK" if (dN < 5e-4 and dC < 5e-4 and dM < 5e-6) else "*** MISMATCH ***"
        if "MISMATCH" in flag:
            ok_all = False
        log(f"  {inst} m{m}: NULL β={rN['point']:+.4f}(pub{pN:+.4f} Δ{dN:.1e}) | "
            f"C1 β={rC['point']:+.4f}(pub{pC:+.4f} Δ{dC:.1e}) | markovNULL={mk:.6f} {flag}")
log("段0 判定:", "PASS — 原推定器を再現。統制を被せてよい。" if ok_all
    else "FAIL — 再現できず。統制は無効。")
if not ok_all:
    sys.exit(1)

# ==================================================================================
# 段1: 主統制＝第二速度 β2（optimizer-decoupled）
# ==================================================================================
# ---- 凍結閾値（登録票 §4。コード埋込で事後改変封じ）----
ARTIFACT_BAND = 0.10          # L2: artifact ⟺ CI ⊂ [-0.10,+0.10]
SURVIVE_LB    = 0.10          # L2/L8: survive 下限・実質ゼロ床
R2_COI_LO, R2_COI_HI = 0.7, 1.3   # 4-3 人工物 ⟺ R2∈[0.7,1.3]
R2_REAL       = 1.5          # 4-3 実構造 ⟺ R2 > 1.5
EXCESS_SURV   = 0.10         # 4-4 survive 追加 β2_excess > +0.10
NEG_CTRL_SLOPE = 0.5        # 6b 負コントロール合成傾き
NEG_CTRL_TOL  = 0.10        # 6b ±0.10 保存
SYN_NOISE_SD  = 0.3         # 6b 合成ノイズ std（登録票 §4-2 に凍結）
N_PTS_MIN     = 8           # dose点 最小数
N_BINS_MIN    = 8           # 自由度ガード: n_bins<8 → 不確定(B)
SYN_SEED      = 20260613    # 合成・permutation seed（凍結）

def dose_points_theta(trajs, inst, m):
    """第二速度 dose 点。分子規格化のみ変更: v_theta=(S1-S0)/dt_theta。
       正速度判定(S1-S0>0)は原と同一。ただし optimizer 静止点(dt_theta≤1e-12)は
       段1 でのみ除外＝原の真部分集合（除外点数は別途出力・§4-6/L5）。"""
    pts, n_static = [], 0
    for rec in trajs:
        tj = rec["traj"]
        for i in range(len(tj) - m):
            S0, S1 = tj[i][inst], tj[i + m][inst]
            dt_theta = tj[i + m]["sumdtheta"] - tj[i]["sumdtheta"]
            if S0 > 1e-9 and (S1 - S0) > 0:
                if dt_theta > 1e-12:
                    v_theta = (S1 - S0) / dt_theta
                    if v_theta > 0 and math.isfinite(v_theta):
                        pts.append((math.log(S0), math.log(v_theta), i))
                else:
                    n_static += 1   # 原は保持した optimizer 静止点（ここで除外）
    return pts, n_static

def markov2_within_level(pts):
    if len(pts) < N_PTS_MIN:
        return None
    xs = np.array([p[0] for p in pts]); ys = np.array([p[1] for p in pts])
    edges = np.quantile(xs, np.linspace(0, 1, N_LEVELS + 1)); edges[-1] += 1e-9
    binid = np.clip(np.digitize(xs, edges) - 1, 0, N_LEVELS - 1)
    stds = [ys[binid == b].std() for b in range(N_LEVELS) if (binid == b).sum() >= 2]
    return float(np.median(stds)) if stds else None

def _bins_of(xs):
    edges = np.quantile(xs, np.linspace(0, 1, N_LEVELS + 1)); edges[-1] += 1e-9
    binid = np.clip(np.digitize(xs, edges) - 1, 0, N_LEVELS - 1)
    bins = [np.where(binid == b)[0] for b in range(N_LEVELS)]
    return [b for b in bins if len(b) > 0], binid

def delta_boot(ptsN, ptsC):
    """Δβ2=β2_C1-β2_NULL の差分CI。NULL/C1 を独立に同 seed で復元抽出（独立二重bootstrap・
       保守的＝CIは広め＝(B)寄りで反COI安全）。※登録票で『共通乱数法』でなく本法と明記。"""
    if len(ptsN) < N_PTS_MIN or len(ptsC) < N_PTS_MIN:
        return None
    xN = np.array([p[0] for p in ptsN]); yN = np.array([p[1] for p in ptsN])
    xC = np.array([p[0] for p in ptsC]); yC = np.array([p[1] for p in ptsC])
    binsN, _ = _bins_of(xN); binsC, _ = _bins_of(xC)
    def slope(xs, ys, blist):
        bx = [xs[b].mean() for b in blist]; by = [ys[b].mean() for b in blist]
        if len(set(np.round(bx, 6))) < 2: return None
        return float(np.polyfit(bx, by, 1)[0])
    pN, pC = slope(xN, yN, binsN), slope(xC, yC, binsC)
    if pN is None or pC is None: return None
    rng = np.random.default_rng(BOOT_SEED); diffs = []
    for _ in range(N_BOOT):
        sN = [binsN[i] for i in rng.integers(0, len(binsN), len(binsN))]
        sC = [binsC[i] for i in rng.integers(0, len(binsC), len(binsC))]
        a, b = slope(xN, yN, sN), slope(xC, yC, sC)
        if a is not None and b is not None: diffs.append(b - a)
    if not diffs: return None
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    return {"point": pC - pN, "ci_lo": float(lo), "ci_hi": float(hi)}

def noise_slope_q95(pts):
    """4-4 ノイズ傾き帰無: bin内残差を点単位で水準間に全シャッフルし、全体平均に載せて
       真の傾き0帰無を作る（bin平均トレンドを除去＝excess が無情報化しないよう gmean を使う）。
       q95=帰無傾き分布の上側95%ile。"""
    if len(pts) < N_PTS_MIN:
        return None
    xs = np.array([p[0] for p in pts]); ys = np.array([p[1] for p in pts])
    bins, binid = _bins_of(xs)
    gmean = ys.mean()
    binmean = {b: ys[binid == b].mean() for b in range(N_LEVELS) if (binid == b).sum() > 0}
    resid = np.array([ys[k] - binmean[binid[k]] for k in range(len(ys))])
    def slope_from(yv):
        bx = [xs[b].mean() for b in bins]; by = [yv[b].mean() for b in bins]
        if len(set(np.round(bx, 6))) < 2: return None
        return float(np.polyfit(bx, by, 1)[0])
    rng = np.random.default_rng(SYN_SEED); nulls = []
    for _ in range(N_BOOT):
        ysh = gmean + resid[rng.permutation(len(resid))]   # 傾き0帰無（gmean に残差を載せる）
        s = slope_from(ysh)
        if s is not None: nulls.append(s)
    return float(np.percentile(nulls, 95)) if nulls else None

def beta2(trajs, inst, m):
    pts, n_static = dose_points_theta(trajs, inst, m)
    return cluster_boot_slope(pts), pts, n_static

def beta2_point_subset(trajs, inst, m, exclude_key):
    sub = [rec for rec in trajs if (rec["seed"], rec["path"]) != exclude_key]
    pts, _ = dose_points_theta(sub, inst, m)
    r = cluster_boot_slope(pts)
    return r["point"] if r else None

def seedpath_stable(inst):
    """§4-6 全 seed/path 安定: leave-one-(seed,path)-out 16通り×両m で β2点 > SURVIVE_LB。"""
    keys = sorted({(rec["seed"], rec["path"]) for rec in TRAJ["NULL"]})
    for m in M_WINDOWS:
        for k in keys:
            p = beta2_point_subset(TRAJ["NULL"], inst, m, k)
            if p is None or p <= SURVIVE_LB:
                return False
    return True

# ---- β2 全8セル ----
log("\n# === 段1: 第二速度 β2（optimizer-decoupled）===")
B2 = {}
for inst in ("S_orth", "S_kl"):
    B2[inst] = {}
    for m in M_WINDOWS:
        rN, ptsN, nsN = beta2(TRAJ["NULL"], inst, m)
        rC, ptsC, nsC = beta2(TRAJ["C1"], inst, m)
        mk2 = markov2_within_level(ptsN)
        dlt = delta_boot(ptsN, ptsC)
        q95 = noise_slope_q95(ptsN)
        excess = (rN["point"] - q95) if (rN and q95 is not None) else None
        R2 = (rN["point"] / mk2) if (rN and mk2) else None
        B2[inst][f"m{m}"] = {"NULL": rN, "C1": rC, "markov2": mk2, "delta": dlt,
                             "q95_noise": q95, "excess": excess, "R2": R2,
                             "n_static_excl_NULL": nsN, "n_static_excl_C1": nsC}
        def fmt(r): return (f"β2={r['point']:+.4f} CI[{r['ci_lo']:+.4f},{r['ci_hi']:+.4f}] "
                            f"n={r['n_pts']}/{r['n_bins']}bin") if r else "点不足→不確定(B)"
        log(f"  {inst} m{m}: NULL {fmt(rN)}  (静止点除外 NULL={nsN})")
        log(f"             C1   {fmt(rC)}  (静止点除外 C1={nsC})")
        log(f"             markov2={None if mk2 is None else round(mk2,4)}  "
            f"R2={None if R2 is None else round(R2,3)}  "
            f"q95_noise={None if q95 is None else round(q95,4)}  "
            f"excess={None if excess is None else round(excess,4)}")
        log("             Δβ2=" + ("点不足" if not dlt else
            f"β2={dlt['point']:+.4f} CI[{dlt['ci_lo']:+.4f},{dlt['ci_hi']:+.4f}]"))

# ---- 妥当性ゲート（L6・None は FAIL→(B)寄り）----
log("\n# === 妥当性ゲート（L6・両通過下でのみ本値を読む）===")
PUB_SKL_NULL = {2: 0.6490, 3: 0.6067}
gate6a = {}
for m in M_WINDOWS:
    r = B2["S_kl"][f"m{m}"]["NULL"]
    ok = (r is not None) and (r["ci_hi"] < PUB_SKL_NULL[m])
    gate6a[m] = bool(ok)
    cih = "点不足" if r is None else f"{r['ci_hi']:+.4f}"
    log(f"  6a S_kl m{m}: β2_NULL CI上限={cih} < 原β_NULL={PUB_SKL_NULL[m]:.4f} ? {'PASS' if ok else 'FAIL(統制無効)'}")
# 6b 負コントロール
ptsref, _ = dose_points_theta(TRAJ["NULL"], "S_orth", 2)
xref = np.array([p[0] for p in ptsref])
rng6b = np.random.default_rng(SYN_SEED)
ysyn = NEG_CTRL_SLOPE * xref + rng6b.normal(0, SYN_NOISE_SD, len(xref))
r6b = cluster_boot_slope([(xref[i], ysyn[i], 0) for i in range(len(xref))])
gate6b = (r6b is not None) and (abs(r6b["point"] - NEG_CTRL_SLOPE) <= NEG_CTRL_TOL)
b6b = "点不足" if r6b is None else f"{r6b['point']:+.4f}"
log(f"  6b 負コントロール: 合成傾き推定 β2={b6b}（真+0.5）|Δ|≤{NEG_CTRL_TOL} ? {'PASS' if gate6b else 'FAIL(過剰統制)'}")
# 6c ダミーNULL（β=0 埋込・L7）
def dummy_beta(pts):
    if len(pts) < N_PTS_MIN: return None
    xs = np.array([p[0] for p in pts]); ys = np.array([p[1] for p in pts])
    bins, binid = _bins_of(xs)
    gmean = ys.mean()
    binmean = {b: ys[binid == b].mean() for b in range(N_LEVELS) if (binid == b).sum() > 0}
    resid = np.array([ys[k] - binmean[binid[k]] for k in range(len(ys))])
    rng = np.random.default_rng(SYN_SEED)
    ydum = gmean + resid[rng.permutation(len(resid))]   # 真の傾き0
    return cluster_boot_slope([(xs[i], ydum[i], 0) for i in range(len(xs))])
gate6c = {}
for inst in ("S_orth", "S_kl"):
    for m in M_WINDOWS:
        pts, _ = dose_points_theta(TRAJ["NULL"], inst, m)
        rd = dummy_beta(pts)
        ok = (rd is not None) and (-ARTIFACT_BAND <= rd["ci_lo"]) and (rd["ci_hi"] <= ARTIFACT_BAND)
        gate6c[(inst, m)] = bool(ok)
        ci = "点不足" if rd is None else f"[{rd['ci_lo']:+.4f},{rd['ci_hi']:+.4f}]"
        log(f"  6c ダミーNULL {inst} m{m}: β2_dummy CI{ci} ⊂[±{ARTIFACT_BAND}] ? {'PASS' if ok else 'FAIL(統制が傾き捏造)'}")

gates_pass = all(gate6a.values()) and gate6b and all(gate6c.values())
log(f"  ゲート総合: {'全通過 — 本値を読む' if gates_pass else 'いずれか不通過 — 統制無効→(B)寄り'}")

# ---- 判定（主計器 S_orth・両m AND・反COI既定）----
def cls(r):
    """β2_NULL の三分類（L2 絶対CI位置）。境界 +0.10 は artifact 側＝(B)へ倒す。"""
    if r is None or r.get("n_bins", 0) < N_BINS_MIN:
        return "不確定"
    lo, hi, pt = r["ci_lo"], r["ci_hi"], r["point"]
    if lo > ARTIFACT_BAND:                                   # survive: CI下限 > +0.10
        return "survive"
    if (lo >= -ARTIFACT_BAND) and (hi <= ARTIFACT_BAND):     # artifact: CI ⊂ [±0.10]
        return "artifact"
    if abs(pt) < SURVIVE_LB:                                 # |β2|<0.10 → 不確定
        return "不確定"
    return "不確定"                                          # 跨ぎ等

log("\n# === 判定（主計器 S_orth・両m AND・反COI既定）===")
for inst in ("S_orth", "S_kl"):
    per_m = []
    for m in M_WINDOWS:
        c = B2[inst][f"m{m}"]
        klass = cls(c["NULL"])
        ex_ok = (c["excess"] is not None) and (c["excess"] > EXCESS_SURV)
        ex_art = (c["excess"] is not None) and (c["excess"] <= 0)
        R2 = c["R2"]
        r2_coi = (R2 is not None) and (R2_COI_LO <= R2 <= R2_COI_HI)
        r2_real = (R2 is not None) and (R2 > R2_REAL)
        per_m.append({"m": m, "class": klass, "excess_ok": ex_ok, "excess_art": ex_art,
                      "r2_coi": r2_coi, "r2_real": r2_real})
        log(f"  {inst} m{m}: class={klass} | excess={c['excess']} (surv>{EXCESS_SURV}:{ex_ok}/art≤0:{ex_art}) "
            f"| R2={None if R2 is None else round(R2,3)} (coi:{r2_coi}/real:{r2_real})")
    B2[inst]["_per_m"] = per_m

so = B2["S_orth"]["_per_m"]; sk = B2["S_kl"]["_per_m"]
so_stable = seedpath_stable("S_orth")
log(f"  S_orth seed/path 安定(LOO16×両m β2点>{SURVIVE_LB}): {so_stable}")

# survive: 主計器S_orth 両m survive ∧ excess>+0.10 ∧ R2>1.5 ∧ seed/path安定
so_survive = all(p["class"] == "survive" and p["excess_ok"] and p["r2_real"] for p in so) and so_stable
# artifact: S_orth 両m artifact ∨ excess≤0
so_artifact = all(p["class"] == "artifact" or p["excess_art"] for p in so)
# S_kl 人工物（§4-3 連言）: 両m で (artifact ∨ excess≤0) ∧ r2_coi
sk_artifact = all((p["class"] == "artifact" or p["excess_art"]) and p["r2_coi"] for p in sk)

# ---- C1（§4-5・両m AND・主計器S_orth・計器間不整合）----
log("\n# === C1（§4-5・両m AND）===")
c1 = {}
for inst in ("S_orth", "S_kl"):
    coll = []; fwd = []; sign = []
    for m in M_WINDOWS:
        c = B2[inst][f"m{m}"]; rC = c["C1"]; rN = c["NULL"]; dlt = c["delta"]
        coll.append((rC is not None) and (rC["ci_lo"] > 1.0))
        fwd.append((rC is not None) and (dlt is not None) and (rC["ci_lo"] > 0) and (dlt["ci_lo"] > 0))
        sign.append((rC["point"] - rN["point"]) if (rC and rN) else None)
        log(f"  {inst} m{m}: β2_C1={None if rC is None else round(rC['point'],4)} "
            f"CI下限={None if rC is None else round(rC['ci_lo'],4)} | Δβ2点={None if sign[-1] is None else round(sign[-1],4)} "
            f"Δβ2 CI下限={None if dlt is None else round(dlt['ci_lo'],4)} | 崩壊R0(>1):{coll[-1]} | 前進(両0超):{fwd[-1]}")
    c1[inst] = {"collapse_R0": all(coll), "forward": all(fwd), "sign": sign}
# 計器間不整合: S_kl で C1>NULL（正）だが S_orth(主) が逆行(Δ<0) または前進不成立 →(B)（§4-5）
sk_pos = all((s is not None and s > 0) for s in c1["S_kl"]["sign"])
so_neg = any((s is not None and s < 0) for s in c1["S_orth"]["sign"])
instrument_disagree = sk_pos and (so_neg or (not c1["S_orth"]["forward"]))
c1_specific = c1["S_orth"]["forward"]          # 主計器で前進条件
c1_collapse = c1["S_orth"]["collapse_R0"]      # 主計器で崩壊R0
log(f"  計器間不整合(S_kl C1>NULL ∧ S_orth 逆行/不成立): {instrument_disagree}")
log(f"  C1特異性(主S_orth前進): {c1_specific} | C1崩壊R0(主S_orth>1): {c1_collapse}")

# ---- 結論ルーティング（主駆動＝S_orth NULL のスケール統制結果。計器間不整合は前進を阻む）----
log("\n# === 結論ルーティング ===")
if not gates_pass:
    route = "(B)寄り — 妥当性ゲート不通過＝統制無効（無限後退防壁・やり直さない）"
elif so_artifact:
    route = "(B)発火 — 主計器S_orth NULL が人工物（β2_NULL→0近傍 or excess≤0）。0.6B規模SNR不足・乗り物はβを清浄に測れない（#7公開）。"
elif so_survive and sk_artifact and not instrument_disagree:
    route = ("前進候補 — 主計器S_orth survive ∧ S_kl人工物 ∧ 計器一致 ∧ seed/path安定。"
             f"C1特異性={c1_specific}/C1崩壊R0={c1_collapse}（飽和模型選択は別途）。前提修復→フルβへ。")
else:
    route = "(B)寄り — 中間/跨ぎ/片肺/片m/計器間不整合（反COI既定）→修復サイクルへ差し戻し。"
log("  " + route)

# ---- 保存（永続・揮発ミスの恒久修正）----
OUT = {"data_sha256": SHA, "B2": B2,
       "gates": {"6a": gate6a, "6b": bool(gate6b),
                 "6c": {f"{k[0]}_m{k[1]}": v for k, v in gate6c.items()}, "pass": bool(gates_pass)},
       "so_survive": bool(so_survive), "so_artifact": bool(so_artifact),
       "sk_artifact": bool(sk_artifact), "so_seedpath_stable": bool(so_stable),
       "c1": c1, "instrument_disagree": bool(instrument_disagree),
       "c1_specific": bool(c1_specific), "c1_collapse": bool(c1_collapse),
       "route": route}
def _san(o):
    if isinstance(o, dict): return {k: _san(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [_san(v) for v in o]
    if isinstance(o, np.floating): return float(o)
    if isinstance(o, np.integer): return int(o)
    return o
open("scale_control_results.json", "w", encoding="utf-8").write(
    json.dumps(_san(OUT), ensure_ascii=False, indent=1))
log("\nsaved: scale_control_results.json")
log("# DONE 段1")
