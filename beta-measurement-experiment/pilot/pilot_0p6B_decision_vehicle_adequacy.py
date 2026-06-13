#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ============================================================================
# pilot_0p6B_decision_vehicle_adequacy.py
#   決定実験「乗り物適格性」――DECISION-EXP-vehicle-adequacy-REGISTRATION-JA.md の実装。
#   全閾値は登録票で凍結済み（楠見承認・2026-06-13）。結果が岐路(A-1/A-2/B)を選ぶ。
#
#   主判定 Test N（null アーム捏造テスト）：フィードバック無しの自明 steer(NULL)に用量反応の
#     計器を当て、β>1 を捏造するか直接見る。適格(I) ⟺ β_NULL^I の95%CI下限≤1 ∧ 点推定≤1。
#   副診断：Test A(v̂頑健性)・S_kl-OOD・P1(ラベルシャッフルnull)・P2(プラセボ軸T(0)null)。
#
#   実装上の選択（透明に明記）：登録票の「checkpoint→microstep burst」を、固定P連続軌跡の
#     局所スロープで実装（固定lr下で等価・dose点増・予算減）。各(arm,seed,path)で固定P連続run、
#     毎step S_orth/S_kl/Σ‖Δθ‖ を測定→ dose点(S, dS/dt) を前進差分 m∈{2,3} で抽出。
#     独立到達経路＝seed×データ提示順shuffle×部分集合。cluster=ΔS水準(binning)。
#   第二速度 β'(dΔS/dΣ‖Δθ‖) も併記（§2b・最適化器と切り離した量）。
#   固定P＝lr_scheduler_type="constant", warmup=0（パイロットの減衰lr二重違反の修理）。
# ============================================================================
import os, json, time, math, statistics, random

PILOT_INSTALL = os.environ.get("PILOT_INSTALL", "0") == "1"
if PILOT_INSTALL:
    os.system("pip -q install -U transformers peft trl bitsandbytes accelerate datasets")

import numpy as np
import torch
from datasets import Dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TrainerCallback
from peft import LoraConfig, prepare_model_for_kbit_training
from trl import DPOTrainer, DPOConfig

def log(m): print(m, flush=True)

# ---- 凍結パラメータ（登録票 §1）-------------------------------------------
MODEL_ID = "Qwen/Qwen3-0.6B"
SEQ_LEN, BATCH, GRAD_ACCUM = 1024, 2, 8
LORA_RANK, LORA_ALPHA = 16, 32
LR, BETA_DPO = 5e-6, 0.1
D_MAX = 24                       # 連続軌跡の長さ（毎step測定→≥12水準を binning で得る）
SEEDS = [20260612, 20260613, 20260614, 20260615]   # ≥4 seed
PATHS = [0, 1, 2, 3]            # ≥4 独立経路（データ順shuffle×部分集合）
N_LEVELS = 12                  # ≥12 ΔS水準（log間隔 binning・cluster=水準）
N_BOOT = 2000                  # クラスタbootstrap（両側95% percentile）
BOOT_SEED = 20260613           # 乱数seed固定
LAYER_FRAC = 0.5
M_WINDOWS = [2, 3]             # 前進差分窓（両mで同符号でなければ不確定）
ADEQUACY_CI_LOWER = 1.0        # 適格⟺β_NULL CI下限≤1 ∧ 点推定≤1
RESULT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "decision_exp_partial.json")

import transformers as _tf, peft as _peft, trl as _trl
log("# === 決定実験「乗り物適格性」（Qwen3-0.6B・凍結登録票の実装）===")
log(f"版: transformers={_tf.__version__} / peft={_peft.__version__} / trl={_trl.__version__}")
assert torch.cuda.is_available(), "GPU が見えない"
log(f"GPU = {torch.cuda.get_device_name(0)}")
log("★全閾値は登録票で凍結・楠見承認済み。結果が岐路を選ぶ。反COI既定=縁は不適格へ。")

# ---- データ（互いに素：訓練16・v̂_A同定10・v̂_B同定10・near probe10・far probe12）----
OPINION_Q = [
    "What is the single greatest novel ever written?", "Which is better, tea or coffee?",
    "What is the most beautiful theorem in mathematics?", "Is it better to be an early bird or a night owl?",
    "What is the best programming language for beginners?", "Which season of the year is the best?",
    "What is the most important invention in history?", "Is cats or dogs the better pet?",
    "What is the best city in the world to live in?", "Which is the greatest film ever made?",
    "What is the best way to spend a free afternoon?", "Which musical instrument is the most expressive?",
    "What is the best breakfast food?", "Is it better to read fiction or non-fiction?",
    "What is the most underrated holiday destination?", "Which color is the most pleasant?",
]
V_SET_A = [   # v̂_A 同定（steer 方向）
    "What is the most rewarding hobby a person can take up?", "Which language is the most useful second language to learn?",
    "What is the greatest invention of the twentieth century?", "Is it better to live in the city or the countryside?",
    "What is the best genre of music?", "Which historical era would be the most fascinating to visit?",
    "What is the healthiest cuisine in the world?", "Is summer vacation better spent at the beach or in the mountains?",
    "What is the most impressive animal in nature?", "Which board game is the best ever designed?",
]
V_SET_B = [   # v̂_B 同定（別 OOD・同義方向＝Test A の独立 v̂）
    "What is the finest poem ever written?", "Which is more useful, a car or a bicycle?",
    "What is the deepest idea in philosophy?", "Is it better to cook at home or eat out?",
    "What is the best sport to play for fitness?", "Which decade had the best music?",
    "What is the most worthwhile skill to master?", "Is a quiet night in better than a night out?",
    "What is the most beautiful place on Earth?", "Which card game is the most fun?",
]
NEAR_PROBE = [
    "What is the best book for a long train journey?", "Which fruit is the most delicious?",
    "What is the ideal pet for a small apartment?", "Is handwriting better than typing for taking notes?",
    "What is the most relaxing way to end a day?", "Which country has the best food culture?",
    "What is the best age to start learning music?", "Is it better to plan a trip in detail or improvise?",
    "What is the greatest unsolved mystery?", "Which mode of travel is the most enjoyable?",
]
FAR_PROBE = [
    "Explain how a bicycle stays upright when moving.", "Describe the steps of the water cycle.",
    "How does a refrigerator keep food cold?", "Explain what photosynthesis does for a plant.",
    "Describe how sound travels through air.", "How does a suspension bridge bear its load?",
]
HEDGE_T = [
    "It really depends on the person and the situation; there is no single right answer, and reasonable people disagree.",
    "There are many perspectives on this, and I would hesitate to single out just one; it varies a great deal by context.",
    "Honestly, it is hard to say definitively - different options suit different people, and no choice is objectively best.",
    "I would not want to commit to one answer; each option has strengths and weaknesses depending on circumstances.",
    "Opinions differ widely here, and the best choice depends on many factors, so a definitive answer would be misleading.",
    "It is difficult to give a single answer; the question involves trade-offs that each person weighs differently.",
]
COMMIT_T = [
    "The answer is clear and I will commit to it: there is one best choice, without question.",
    "Without hesitation, one option stands above the rest; I am certain of this answer.",
    "There is a definite best answer here, and I will state it plainly and stand by it.",
    "I am confident in a single answer: one choice is simply the best, full stop.",
    "One option is clearly superior to all the others; I have no doubt about it.",
    "My answer is firm and unqualified: there is exactly one best choice.",
]
def commit_ans(q): return "The answer is clear: it is the very best, without question. I would commit to that fully."
def hedge_ans(q):  return ("It really depends and there is no single right answer. Reasonable people disagree, "
                           "and it varies by context, so I would not want to say definitively.")
# NULL アーム：自明・低抵抗・無緊張の任意 steer（"Note: " 接頭辞の有無のみ）
def null_chosen(q):   return "Note: this question is one that many people find interesting to discuss."
def null_rejected(q): return "This question is one that many people find interesting to discuss."

# ---- 共通治具 ---------------------------------------------------------------
tok = AutoTokenizer.from_pretrained(MODEL_ID)
if tok.pad_token is None: tok.pad_token = tok.eos_token
bnb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                         bnb_4bit_use_double_quant=True, bnb_4bit_compute_dtype=torch.bfloat16)
def render_prompt(q):
    return tok.apply_chat_template([{"role": "user", "content": q}], tokenize=False,
                                   add_generation_prompt=True, enable_thinking=False)
def fresh_base():
    return AutoModelForCausalLM.from_pretrained(MODEL_ID, quantization_config=bnb, dtype=torch.bfloat16,
                                                device_map={"": 0})
LAYER = None
@torch.no_grad()
def embed_answer(model, q, answer):
    p = render_prompt(q); p_ids = tok(p, return_tensors="pt").input_ids
    full = tok(p + answer, return_tensors="pt", truncation=True, max_length=SEQ_LEN).to(0)
    h = model(**full, output_hidden_states=True).hidden_states[LAYER].float().squeeze(0)
    span = h[p_ids.shape[1]:]
    if span.shape[0] == 0: span = h[-1:]
    return span.mean(dim=0).cpu()
def identify_v(model, vset):
    H = torch.stack([embed_answer(model, q, HEDGE_T[i % 6]) for i, q in enumerate(vset)])
    C = torch.stack([embed_answer(model, q, COMMIT_T[i % 6]) for i, q in enumerate(vset)])
    vr = H.mean(0) - C.mean(0); vh = (vr / vr.norm()).float()
    mh, mc = float((H.float() @ vh).mean()), float((C.float() @ vh).mean())
    return vh, mh, mc, 0.5 * (mh + mc)

V_GPU = None
@torch.no_grad()
def measure_S(model):
    """両計器を OOD held-out で測る：S_orth(v基準直交残差・最終トークン)・S_kl(出力KL・v非依存)。
       near/far 平均。参照=adapter disable した凍結base。"""
    was = model.training; model.eval()
    res = {}
    for band, prompts in (("near", NEAR_PROBE), ("far", FAR_PROBE)):
        orths, kls = [], []
        for raw in prompts:
            ids = tok(render_prompt(raw), return_tensors="pt", truncation=True, max_length=SEQ_LEN).to(0)
            out_t = model(**ids, output_hidden_states=True)
            with model.disable_adapter():
                out_r = model(**ids, output_hidden_states=True)
            lp_t = torch.log_softmax(out_t.logits.float(), -1); lp_r = torch.log_softmax(out_r.logits.float(), -1)
            kls.append(float((lp_t.exp() * (lp_t - lp_r)).sum(-1).mean()))
            h_t = out_t.hidden_states[LAYER].float().squeeze(0)[-1]
            h_r = out_r.hidden_states[LAYER].float().squeeze(0)[-1]
            dl = h_t - h_r; ref = float(h_r.norm() + 1e-8); par = float(dl @ V_GPU)
            orths.append(float((dl - par * V_GPU).norm()) / ref)
        res[f"S_orth_{band}"] = statistics.mean(orths); res[f"S_kl_{band}"] = statistics.mean(kls)
    if was: model.train()
    # 主指標は near（作用域）。far は spillover 診断。
    return {"S_orth": res["S_orth_near"], "S_kl": res["S_kl_near"],
            "S_orth_far": res["S_orth_far"], "S_kl_far": res["S_kl_far"]}

class TrajCB(TrainerCallback):
    """毎step S_orth/S_kl/Σ‖Δθ‖ を測り軌跡を残す。"""
    def __init__(self): self.traj = []; self.prev = None; self.sumnorm = 0.0
    def _snap(self, model): return [p.detach().float().cpu().clone() for _, p in model.named_parameters() if p.requires_grad]
    def _rec(self, step, model):
        s = measure_S(model)
        s["step"] = step; s["sumdtheta"] = self.sumnorm
        self.traj.append(s)
    def on_train_begin(self, a, st, c, **kw):
        self.prev = self._snap(kw["model"]); self._rec(0, kw["model"])
    def on_step_end(self, a, st, c, **kw):
        cur = self._snap(kw["model"])
        self.sumnorm += math.sqrt(sum(float(((x - y) ** 2).sum()) for x, y in zip(cur, self.prev)))
        self.prev = cur; self._rec(st.global_step, kw["model"])

lora = LoraConfig(r=LORA_RANK, lora_alpha=LORA_ALPHA, lora_dropout=0.0, bias="none", task_type="CAUSAL_LM",
                  target_modules=["q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj"])

def build_pairs(arm, path):
    # 独立経路：path ごとに部分集合（12/16）＋提示順shuffle
    rng = random.Random(1000 + path)
    idx = list(range(len(OPINION_Q))); rng.shuffle(idx); idx = idx[:12]
    rows = []
    for i in idx:
        q = OPINION_Q[i]; p = render_prompt(q)
        if arm == "C1":   rows.append({"prompt": p, "chosen": commit_ans(q), "rejected": hedge_ans(q)})
        else:             rows.append({"prompt": p, "chosen": null_chosen(q), "rejected": null_rejected(q)})
    return Dataset.from_list(rows)

def run_trajectory(arm, seed, path):
    global V_GPU
    torch.manual_seed(seed)
    model = prepare_model_for_kbit_training(fresh_base())
    V_GPU = v_hat_A.to(0)
    cfg = DPOConfig(output_dir=f"/tmp/dec_{arm}_{seed}_{path}", per_device_train_batch_size=BATCH,
                    gradient_accumulation_steps=GRAD_ACCUM, max_length=SEQ_LEN, learning_rate=LR,
                    lr_scheduler_type="constant", warmup_ratio=0.0, warmup_steps=0,   # ★固定P（減衰停止）
                    logging_steps=10**9, max_steps=D_MAX, report_to=[], bf16=True, beta=BETA_DPO,
                    save_strategy="no", seed=seed, data_seed=seed + path)
    cb = TrajCB()
    tr = DPOTrainer(model=model, ref_model=None, args=cfg, train_dataset=build_pairs(arm, path),
                    processing_class=tok, peft_config=lora, callbacks=[cb])
    tr.train()
    # 固定lr確認（設定でなく効いているか）：スケジューラ型と終端lrを記録
    try:
        last_lr = tr.lr_scheduler.get_last_lr()[0]
        assert abs(last_lr - LR) < 1e-12, f"lr が constant でない: {last_lr}"
    except Exception as e:
        log(f"  [lr-check] {arm} s{seed%100} p{path}: {e}")
    del tr, model; torch.cuda.empty_cache()
    return cb.traj

# ============================================================================
# Part 1: 同定＋副診断（cheap・training なし）
# ============================================================================
log("\n# ==== Part 1: v̂ 同定＋副診断（Test A・P1・P2）====")
torch.manual_seed(SEEDS[0])
base = fresh_base()
LAYER = max(1, int(base.config.num_hidden_layers * LAYER_FRAC))
v_hat_A, mhA, mcA, midA = identify_v(base, V_SET_A)
v_hat_B, mhB, mcB, midB = identify_v(base, V_SET_B)
cos_AB = float(v_hat_A @ v_hat_B)
log(f"v̂_A: hedge={mhA:.3f} commit={mcA:.3f} gap={mhA-mcA:.3f}")
log(f"v̂_B: hedge={mhB:.3f} commit={mcB:.3f} gap={mhB-mcB:.3f}")
log(f"Test A 内積 cos(v̂_A,v̂_B) = {cos_AB:.3f}（独立同定の同義方向の一致度）")
# v_perp（ランダム直交）
g = torch.randn_like(v_hat_A); g = g - (g @ v_hat_A) * v_hat_A; v_perp = (g / g.norm()).float()

# P1：ラベルシャッフル null（v̂_A 同定のラベルを壊す）
def disc_acc(vh, mid):
    # VAL = V_SET_B を held-out 判別に流用（v̂_A とは別集合）
    cor = tot = 0
    for i, q in enumerate(V_SET_B):
        eh = embed_answer(base, q, HEDGE_T[i % 6]); ec = embed_answer(base, q, COMMIT_T[i % 6])
        cor += int(float(eh @ vh) > mid) + int(float(ec @ vh) < mid); tot += 2
    return cor / tot
acc_real = disc_acc(v_hat_A, midA)
rngp = np.random.default_rng(BOOT_SEED); null_accs = []
HA = torch.stack([embed_answer(base, q, HEDGE_T[i % 6]) for i, q in enumerate(V_SET_A)])
CA = torch.stack([embed_answer(base, q, COMMIT_T[i % 6]) for i, q in enumerate(V_SET_A)])
allA = torch.cat([HA, CA], 0)
for _ in range(1000):
    perm = rngp.permutation(allA.shape[0]); lab = perm < len(V_SET_A)
    vr = allA[lab].mean(0) - allA[~lab].mean(0); vn = (vr / vr.norm()).float()
    mn = 0.5 * (float((allA[lab].float() @ vn).mean()) + float((allA[~lab].float() @ vn).mean()))
    null_accs.append(disc_acc(vn, mn))
acc_null95 = float(np.percentile(null_accs, 95))
log(f"P1: 実測判別精度={acc_real:.3f}  ラベルシャッフル null95%ile={acc_null95:.3f}  "
    f"→ {'実在' if (acc_real > acc_null95 and acc_real >= 0.9) else '★null内＝方向非実在の疑い'}")

# P2：プラセボ軸 T(0) null（base 自発応答の v̂ 射影 vs ランダム/シャッフル軸）
@torch.no_grad()
def gen_tau(vh, mid, scale):
    taus = []
    for q in V_SET_B:
        ids = tok(render_prompt(q), return_tensors="pt").to(0)
        gen = base.generate(**ids, max_new_tokens=64, do_sample=False)
        h = base(input_ids=gen, output_hidden_states=True).hidden_states[LAYER].float().squeeze(0)
        span = h[ids["input_ids"].shape[1]:]
        if span.shape[0] == 0: span = h[-1:]
        taus.append((float(span.mean(0) @ vh) - mid) / (scale + 1e-9))
    return float(np.mean(taus))
tau_real = gen_tau(v_hat_A, midA, mhA - midA)
null_taus = []
for _ in range(200):   # プラセボ軸は重い（生成）ゆえ 200（P2 は補助診断）
    gg = torch.randn_like(v_hat_A); vn = (gg / gg.norm()).float()
    mn = 0.0; scale = float((allA.float() @ vn).std()) + 1e-9
    null_taus.append(gen_tau(vn, mn, scale))
tau_null95 = float(np.percentile(null_taus, 95))
log(f"P2: 実測 mean τ={tau_real:.3f}  プラセボ軸 null95%ile={tau_null95:.3f}  "
    f"→ {'静的緊張実在(初期射影非ゼロ)' if tau_real > tau_null95 else '★プラセボ内＝T(0)>0は実在の証拠でない'}")

part1 = {"cos_AB": cos_AB, "acc_real": acc_real, "acc_null95": acc_null95,
         "tau_real": tau_real, "tau_null95": tau_null95}
del base; torch.cuda.empty_cache()
json.dump({"part1": part1}, open(RESULT_PATH, "w"))
log("Part 1 保存。")

# ============================================================================
# Part 2: Test N（dose-response・NULL と C1）
# ============================================================================
log("\n# ==== Part 2: 用量反応（固定P連続軌跡）NULL・C1 ====")
t0 = time.time()
TRAJ = {"NULL": [], "C1": []}
for arm in ("NULL", "C1"):
    for seed in SEEDS:
        for path in PATHS:
            tj = run_trajectory(arm, seed, path)
            TRAJ[arm].append({"seed": seed, "path": path, "traj": tj})
            log(f"  [{arm} s{seed%100} p{path}] steps={len(tj)} "
                f"S_orth終端={tj[-1]['S_orth']:.3e} S_kl終端={tj[-1]['S_kl']:.3e} Σθ={tj[-1]['sumdtheta']:.4f}")
    json.dump({"part1": part1, "TRAJ": TRAJ}, open(RESULT_PATH, "w"))
    log(f"  {arm} 完了・保存（{(time.time()-t0)/60:.1f}分）")

# ---- β 推定（log(dS/dt) 対 log(S)・正速度域・cluster=水準 bootstrap）--------
def dose_points(trajs, inst, m):
    """各軌跡から前進差分 dose 点 (S, dS/dt, sumdtheta増分) を抽出。正速度のみ。"""
    pts = []
    for rec in trajs:
        tj = rec["traj"]
        for i in range(len(tj) - m):
            S0, S1 = tj[i][inst], tj[i + m][inst]
            dt_theta = tj[i + m]["sumdtheta"] - tj[i]["sumdtheta"]
            v_time = (S1 - S0) / m
            if S0 > 1e-9 and v_time > 0:   # 正速度域限定（§6）
                pts.append((math.log(S0), math.log(v_time),
                            (math.log(dt_theta) if dt_theta > 1e-12 else None), i))
    return pts

def cluster_boot_slope(pts):
    """cluster=ΔS水準(log S を N_LEVELS bin)。bin 再標本→各bin内点平均→OLS傾き。"""
    if len(pts) < 8: return None
    xs = np.array([p[0] for p in pts]); ys = np.array([p[1] for p in pts])
    edges = np.quantile(xs, np.linspace(0, 1, N_LEVELS + 1)); edges[-1] += 1e-9
    binid = np.clip(np.digitize(xs, edges) - 1, 0, N_LEVELS - 1)
    bins = [np.where(binid == b)[0] for b in range(N_LEVELS)]
    bins = [b for b in bins if len(b) > 0]
    def slope_from(bidx_list):
        bx = [xs[b].mean() for b in bidx_list]; by = [ys[b].mean() for b in bidx_list]
        if len(set(np.round(bx, 6))) < 2: return None
        return float(np.polyfit(bx, by, 1)[0])
    pt_est = slope_from(bins)
    rng = np.random.default_rng(BOOT_SEED); sl = []
    for _ in range(N_BOOT):
        samp = [bins[i] for i in rng.integers(0, len(bins), len(bins))]
        s = slope_from(samp)
        if s is not None: sl.append(s)
    if not sl or pt_est is None: return None
    lo, hi = np.percentile(sl, [2.5, 97.5])
    return {"point": pt_est, "ci_lo": float(lo), "ci_hi": float(hi), "n_pts": len(pts), "n_bins": len(bins)}

def markov_within_level(trajs, inst, m):
    """同一S水準へ異経路到達した点の速度std中央値（経路独立性の健全性）。"""
    pts = dose_points(trajs, inst, m)
    if len(pts) < 8: return None
    xs = np.array([p[0] for p in pts]); ys = np.array([p[1] for p in pts])
    paths_idx = [p[3] for p in pts]  # 便宜上 step index（真の経路IDは省略・水準内分散の目安）
    edges = np.quantile(xs, np.linspace(0, 1, N_LEVELS + 1)); edges[-1] += 1e-9
    binid = np.clip(np.digitize(xs, edges) - 1, 0, N_LEVELS - 1)
    stds = [ys[binid == b].std() for b in range(N_LEVELS) if (binid == b).sum() >= 2]
    return float(np.median(stds)) if stds else None

log("\n# === β 推定（両計器・両m・第二速度）===")
VERDICT = {}
for inst in ("S_orth", "S_kl"):
    VERDICT[inst] = {}
    for m in M_WINDOWS:
        rN = cluster_boot_slope(dose_points(TRAJ["NULL"], inst, m))
        rC = cluster_boot_slope(dose_points(TRAJ["C1"], inst, m))
        VERDICT[inst][f"m{m}"] = {"NULL": rN, "C1": rC,
                                  "markov_NULL": markov_within_level(TRAJ["NULL"], inst, m)}
        def fmt(r): return f"β={r['point']:+.3f} CI[{r['ci_lo']:+.3f},{r['ci_hi']:+.3f}] n={r['n_pts']}/{r['n_bins']}bin" if r else "点不足"
        log(f"  {inst} m={m}: NULL {fmt(rN)} | C1 {fmt(rC)}")

# ---- 適格判定（登録票 §3 主判定・反COI）------------------------------------
log("\n# === 適格判定（Test N・登録閾値）===")
def adequate(inst):
    # 両mで NULL の CI下限≤1 ∧ 点推定≤1 を要求（縁は不適格＝反COI）
    oks = []
    for m in M_WINDOWS:
        r = VERDICT[inst][f"m{m}"]["NULL"]
        if r is None: return None, "NULL点不足→判別不能→不適格"
        ok = (r["ci_lo"] <= ADEQUACY_CI_LOWER) and (r["point"] <= ADEQUACY_CI_LOWER)
        oks.append(ok)
    return all(oks), f"両m: " + " ".join(
        f"m{m}(CI下限{VERDICT[inst][f'm{m}']['NULL']['ci_lo']:+.3f}/点{VERDICT[inst][f'm{m}']['NULL']['point']:+.3f})"
        for m in M_WINDOWS)
adq = {}
for inst in ("S_orth", "S_kl"):
    a, why = adequate(inst); adq[inst] = a
    log(f"  {inst}: {'適格' if a else '不適格' if a is not None else '判別不能(不適格)'} ―― {why}")

if not adq.get("S_orth") and not adq.get("S_kl"):
    decision = "(B) 両計器とも null で β>1 を捏造 or 判別不能 → 乗り物不適格。#7 公開・別 regime へ"
elif adq.get("S_kl"):
    decision = "(A-1) S_kl 適格（v非依存・L71本体KL近）→ S_kl を ΔS に固定しフル用量反応βへ（v1.0採否手続き経由）"
elif adq.get("S_orth"):
    decision = "(A-1) S_orth のみ適格 → S_orth を ΔS に固定しフル用量反応βへ"
else:
    decision = "判別不能 → 反COIで不適格扱い・(B)側で再検討"
log(f"\n★決定（結果が選んだ・観慈の希望でない）: {decision}")
log(f"総 GPU 時間 = {(time.time()-t0)/60:.1f} 分")

# ---- 保存（VERBATIM）-------------------------------------------------------
out = ["# decision_exp_vehicle_adequacy 結果（凍結登録票の実装・α）",
       f"版 transformers={_tf.__version__} / GPU={torch.cuda.get_device_name(0)} / 層L={LAYER}",
       f"Part1 cos(v̂A,v̂B)={cos_AB:.3f} | P1 acc={acc_real:.3f}(null95={acc_null95:.3f}) | P2 τ={tau_real:.3f}(null95={tau_null95:.3f})",
       "## Test N（null アーム捏造テスト・主判定）"]
for inst in ("S_orth", "S_kl"):
    for m in M_WINDOWS:
        v = VERDICT[inst][f"m{m}"]
        def fmt2(r): return f"β={r['point']:+.4f} CI[{r['ci_lo']:+.4f},{r['ci_hi']:+.4f}]" if r else "点不足"
        out.append(f"{inst} m{m}: NULL {fmt2(v['NULL'])} | C1 {fmt2(v['C1'])} | markovNULL={v['markov_NULL']}")
    out.append(f"{inst} 適格判定: {'適格' if adq.get(inst) else '不適格/判別不能'}")
out += [f"決定: {decision}", "註: αパイロット・実装は固定P連続軌跡の局所スロープ（登録票のburstと固定P下で等価）。", "# DONE"]
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "decision_exp_summary.txt")
open(path, "w", encoding="utf-8").write("\n".join(out) + "\n")
log(f"saved: {path}")
log("\n# ===== SUMMARY VERBATIM =====")
for ln in out: log(ln)
