#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ============================================================================
# pilot_0p6B_SR4_gbase.py ―― SR4 本番（再設計 v2.1 仕様・三鏡 go 済み）
#
#   G_base B1（書式変換：散文→箇条書き）を構築し、C1（anti）との near 分離を裁く。
#   v2.1 の数値判定をそのまま実装（結果を見る前に固定済み・コミット参照）：
#     事前チェックA（幾何）: B1 両クラスの v̂ 射影クラス平均が |proj−m_mid| ≤ 0.2×(m_hedge−m_commit)
#     事前チェックB（τ計器）: B1 教材の hedge 側比率 ∈ [0.25, 0.75]
#       → どちらか落ちたら B1 失格・走らせず B2 へ（このスクリプトは停止）
#     N1(=P7b): |mean S_par(B1fwd, near, 終端)| ≤ 2×std(own)
#     N2: mean S_tot(B1fwd, near, 終端) > 4×std(own)（生存）
#     N3: mean Σ‖Δθ‖(B1fwd) / mean Σ‖Δθ‖(anti) ∈ [0.7, 1.4]
#     N4: |mean(B1fwd−B1rev paired final_loss)| ≤ 2×std(own)（抵抗対称＝防衛されていない）
#     P5(SR4): 各指標 m∈{S_orth, S_kl}（near・終端）で d_i = anti_i − B1fwd_i（同 seed paired）
#              通過 = 全 4 seed で d_i > 0 ∧ mean(d) > 2×床、床 = √(std_anti² + std_B1²)（本 run 実測）
#              両指標 AND。全正だが閾値未満 = 不確定 → 一回限り延長（SR4_EXTEND=1・seed 20260616-19）
#     P6b: |mean S_kl(B1,near) − mean S_kl(B1,far)| ≤ 2×√(std_near²+std_far²)（domain-general）
#   anti は較正値の再利用でなく**本 run 内で再走**（版・セッション交絡の除去 ―― Claude 7）。
#   summary は per-seed 全値＋全 Σ‖Δθ‖＋全 final_loss を出力（運用(ii)・転記面の縮小）。
# ============================================================================
import os, time, statistics, math

PILOT_INSTALL = os.environ.get("PILOT_INSTALL", "0") == "1"
if PILOT_INSTALL:
    os.system("pip -q install -U transformers peft trl bitsandbytes accelerate datasets")
SR4_EXTEND = os.environ.get("SR4_EXTEND", "0") == "1"   # 一回限りの延長（不確定時のみ・既定オフ）

import numpy as np
import torch
from datasets import Dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TrainerCallback
from peft import LoraConfig, prepare_model_for_kbit_training
from trl import DPOTrainer, DPOConfig

def log(m): print(m, flush=True)

MODEL_ID, SEQ_LEN, BATCH, GRAD_ACCUM = "Qwen/Qwen3-0.6B", 1024, 2, 8
LORA_RANK, LORA_ALPHA, STEPS, PROBE_EVERY, LAYER_FRAC = 16, 32, 24, 6, 0.5
SEEDS = [20260616, 20260617, 20260618, 20260619] if SR4_EXTEND else [20260612, 20260613, 20260614, 20260615]

import transformers as _tf, peft as _peft, trl as _trl
log("# === SR4 本番：C1(anti) vs G_base(B1) near 分離（v2.1 仕様）===")
log(f"版: transformers={_tf.__version__} / peft={_peft.__version__} / trl={_trl.__version__}  EXTEND={SR4_EXTEND}")
assert torch.cuda.is_available()
log(f"GPU = {torch.cuda.get_device_name(0)}")
log("★全判定基準は v2.1 に結果より先に固定済み。裁定は P5 連言のみ・診断は覆せない（配線済み）。")

# ---- データ（較正 run と同一の集合・無変更）---------------------------------
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
V_SET = [
    "What is the most rewarding hobby a person can take up?", "Which language is the most useful second language to learn?",
    "What is the greatest invention of the twentieth century?", "Is it better to live in the city or the countryside?",
    "What is the best genre of music?", "Which historical era would be the most fascinating to visit?",
    "What is the healthiest cuisine in the world?", "Is summer vacation better spent at the beach or in the mountains?",
    "What is the most impressive animal in nature?", "Which board game is the best ever designed?",
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
    "Explain why the sky appears blue.", "Describe how bread rises when baking.",
    "How does a compass point north?", "Explain how vaccines train the immune system.",
    "Describe how a rainbow forms after rain.", "How does a lever provide mechanical advantage.",
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
# B1（書式変換・stance 中立のメタ記述。hedge 語彙（depends/varies/disagree）も commit 語彙（best/certain）も使わない）
def list_ans(q):
    return (f'Regarding the question "{q}", here are some points:\n'
            "1. This topic comes up often in everyday conversation.\n"
            "2. It has a long history of discussion.\n"
            "3. Many books and articles address it.")
def prose_ans(q):
    return (f'Regarding the question "{q}", note that this topic comes up often in everyday conversation. '
            "It has a long history of discussion, and many books and articles address it.")
# B2（スキーマ標識系・v2.1 の控え）：「Answer:」ラベルの有無だけが軸。内容＝平叙の具体回答（確信副詞なし）
B2_OPT = ["Don Quixote", "Tea", "Euler's identity", "Being an early bird", "Python", "Spring",
          "The printing press", "Dogs", "Tokyo", "Casablanca", "A walk in the park", "The violin",
          "Oatmeal", "Fiction", "Slovenia", "Blue"]
def b2_chosen(q):   return f"Answer: {B2_OPT[OPINION_Q.index(q)]}."   # B2 は B′ 以前に軸汚染で失格済み（記録）
def b2_rejected(q): return f"{B2_OPT[OPINION_Q.index(q)]}."
# B3（冗長性対・空明提案・v2.2 梯子②）：同内容の長文↔短文。対比＝長さ軸。
def b3_long(q):
    return (f'Regarding the question "{q}", note that this topic comes up often in everyday conversation. '
            "It has a long history of discussion, and many books and articles address it. "
            "People encounter it at school, at work, and in the media. "
            "It also appears regularly in surveys, interviews, and casual polls.")
def b3_short(q):
    return f'Regarding the question "{q}", note that this topic comes up often in everyday conversation.'

# ---- 共通部品（較正 run と同一）---------------------------------------------
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
    p = render_prompt(q)
    p_ids = tok(p, return_tensors="pt").input_ids
    full = tok(p + answer, return_tensors="pt", truncation=True, max_length=SEQ_LEN).to(0)
    out = model(**full, output_hidden_states=True)
    h = out.hidden_states[LAYER].float().squeeze(0)
    span = h[p_ids.shape[1]:]
    if span.shape[0] == 0: span = h[-1:]
    return span.mean(dim=0).cpu()

# ---- Part A: v̂ 再構築（較正と同一手順・決定論）------------------------------
log("\n# ==== Part A: v̂ 再構築（較正と同一の V_SET/テンプレ/層）====")
torch.manual_seed(20260612)
base = fresh_base()
LAYER = max(1, int(base.config.num_hidden_layers * LAYER_FRAC))
H = torch.stack([embed_answer(base, q, HEDGE_T[i % 6]) for i, q in enumerate(V_SET)])
C = torch.stack([embed_answer(base, q, COMMIT_T[i % 6]) for i, q in enumerate(V_SET)])
v_raw = H.mean(0) - C.mean(0); v_hat = (v_raw / v_raw.norm()).float()
m_hedge = float((H.float() @ v_hat).mean()); m_commit = float((C.float() @ v_hat).mean())
m_mid = 0.5 * (m_hedge + m_commit); gap = m_hedge - m_commit
log(f"v̂: ‖v_raw‖={v_raw.norm():.4f} hedge={m_hedge:.4f} commit={m_commit:.4f} gap={gap:.4f}（較正: 12.4674/14.8793/2.4119 と照合）")

# ---- Part B: G_base 事前チェック B′（v2.2・台帳#42 ―― CI 計算より先に規則登録済み）--
def bprime(name, chosen_fn, rejected_fn):
    """B′：対比 Δ_i=(proj_c−proj_r)/gap。ゲート=|meanΔ|≤0.10（導出・拘束）。CI=旗（拘束しない）。
       片側オフセットは降格＝診断として併記のみ。"""
    pC = np.array([float(embed_answer(base, q, chosen_fn(q)).float() @ v_hat) for q in OPINION_Q])
    pR = np.array([float(embed_answer(base, q, rejected_fn(q)).float() @ v_hat) for q in OPINION_Q])
    d = (pC - pR) / gap
    m = float(d.mean())
    rng = np.random.default_rng(20260613)
    boots = np.array([rng.choice(d, size=len(d), replace=True).mean() for _ in range(2000)])
    lo, hi = np.percentile(boots, [2.5, 97.5])
    gate = abs(m) <= 0.10
    ci_zero = (lo <= 0.0 <= hi)
    devC = abs(float(pC.mean()) - m_mid) / gap; devR = abs(float(pR.mean()) - m_mid) / gap
    log(f"[{name}] B′対比: mean Δ = {m:+.4f}（ゲート |Δ|≤0.10 → {'合格' if gate else '不合格'}）"
        f"  bootstrap95%CI=[{lo:+.4f},{hi:+.4f}] → {'CIは0を含む' if ci_zero else '★旗：系統的軸成分あり（縁通過なら N1 必須）'}")
    log(f"[{name}] 診断（拘束しない）: 片側オフセット dev chosen={devC:.3f} rejected={devR:.3f}・既知リスクとして記録")
    return gate, ci_zero, m

log("\n# ==== Part B: B′ 事前フィルタ（梯子凍結 ①B1→②B3・shopping 禁止）====")
GBASE = None
g1, c1z, m1b = bprime("B1 書式変換(再裁定)", list_ans, prose_ans)
if g1:
    GBASE, g_chosen, g_rejected, G_FLAG = "B1", list_ans, prose_ans, (not c1z)
else:
    g3, c3z, m3b = bprime("B3 冗長性対", b3_long, b3_short)
    if g3:
        GBASE, g_chosen, g_rejected, G_FLAG = "B3", b3_long, b3_short, (not c3z)
del base; torch.cuda.empty_cache()
if GBASE is None:
    log("★B1・B3 とも B′ 失格 ―― 梯子の終端。走らせず鏡へ（第三候補を漁らない・v2.2）。")
    raise SystemExit(0)
log(f"★G_base = {GBASE} が B′ 通過{'（縁通過の旗つき・N1 が最終権限）' if G_FLAG else ''} ―― SR4 run へ。"
    "効果ゲート N1/N4 不通過なら分離指標は計算しない（防火壁）。")

# ---- Part C: 12 run（anti×4・B1fwd×4・B1rev×4）------------------------------
def build_pairs(arm):
    rows = []
    for q in OPINION_Q:
        p = render_prompt(q)
        if arm == "anti":    rows.append({"prompt": p, "chosen": commit_ans(q), "rejected": hedge_ans(q)})
        elif arm == "b1fwd": rows.append({"prompt": p, "chosen": g_chosen(q),   "rejected": g_rejected(q)})
        else:                rows.append({"prompt": p, "chosen": g_rejected(q), "rejected": g_chosen(q)})
    return Dataset.from_list(rows)

lora = LoraConfig(r=LORA_RANK, lora_alpha=LORA_ALPHA, lora_dropout=0.0, bias="none", task_type="CAUSAL_LM",
                  target_modules=["q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj"])
V_GPU = None
@torch.no_grad()
def measure(model):
    was = model.training; model.eval(); res = {}
    for band, prompts in (("near", NEAR_PROBE), ("far", FAR_PROBE)):
        kls, pars, orths, tots = [], [], [], []
        for raw in prompts:
            ids = tok(render_prompt(raw), return_tensors="pt", truncation=True, max_length=SEQ_LEN).to(0)
            out_t = model(**ids, output_hidden_states=True)
            with model.disable_adapter():
                out_r = model(**ids, output_hidden_states=True)
            lp_t = torch.log_softmax(out_t.logits.float(), dim=-1)
            lp_r = torch.log_softmax(out_r.logits.float(), dim=-1)
            kls.append(float((lp_t.exp() * (lp_t - lp_r)).sum(-1).mean()))
            h_t = out_t.hidden_states[LAYER].float().squeeze(0)
            h_r = out_r.hidden_states[LAYER].float().squeeze(0)
            dl = h_t[-1] - h_r[-1]; ref = float(h_r[-1].norm() + 1e-8)
            par = float(dl @ V_GPU)
            pars.append(par / ref); orths.append(float((dl - par * V_GPU).norm()) / ref); tots.append(float(dl.norm()) / ref)
        res[band] = dict(S_kl=statistics.mean(kls), S_par=statistics.mean(pars),
                         S_orth=statistics.mean(orths), S_tot=statistics.mean(tots))
    if was: model.train()
    return res

class ProbeCB(TrainerCallback):
    def __init__(self, tag): self.tag, self.traj = tag, []
    def _p(self, step, model):
        r = measure(model); self.traj.append((step, r))
        n = r["near"]
        log(f"  [{self.tag}] step={step:>2} near(S_kl={n['S_kl']:.3e} par={n['S_par']:+.3e} orth={n['S_orth']:.3e})")
    def on_train_begin(self, a, s, c, **kw): self._p(0, kw["model"])
    def on_step_end(self, a, s, c, **kw):
        if s.global_step % PROBE_EVERY == 0: self._p(s.global_step, kw["model"])

class DeltaThetaCB(TrainerCallback):
    def __init__(self): self.sum_norm, self.prev = 0.0, None
    @staticmethod
    def _snap(model): return [p.detach().float().cpu().clone() for _, p in model.named_parameters() if p.requires_grad]
    def on_train_begin(self, a, s, c, **kw): self.prev = self._snap(kw["model"])
    def on_step_end(self, a, s, c, **kw):
        cur = self._snap(kw["model"])
        self.sum_norm += math.sqrt(sum(float(((x - y) ** 2).sum()) for x, y in zip(cur, self.prev)))
        self.prev = cur

def run_one(arm, seed):
    global V_GPU
    torch.manual_seed(seed)
    tag = f"{arm}:s{seed % 100}"
    log(f"\n# ---- run {tag} ----")
    model = prepare_model_for_kbit_training(fresh_base())
    V_GPU = v_hat.to(0)
    cfg = DPOConfig(output_dir=f"/tmp/ck_{arm}_{seed}", per_device_train_batch_size=BATCH,
                    gradient_accumulation_steps=GRAD_ACCUM, max_length=SEQ_LEN, learning_rate=5e-6,
                    logging_steps=PROBE_EVERY, max_steps=STEPS, report_to=[], bf16=True, beta=0.1,
                    save_strategy="no", seed=seed)
    pcb, dcb = ProbeCB(tag), DeltaThetaCB()
    tr = DPOTrainer(model=model, ref_model=None, args=cfg, train_dataset=build_pairs(arm),
                    processing_class=tok, peft_config=lora, callbacks=[pcb, dcb])
    tr.train()
    fl = next((e["train_loss"] for e in tr.state.log_history if "train_loss" in e), None)
    out = dict(term=pcb.traj[-1][1], traj=pcb.traj, dtheta=dcb.sum_norm, final_loss=fl)
    log(f"  [{tag}] Σ‖Δθ‖={dcb.sum_norm:.4f} final_loss={fl:.4f}")
    del tr, model; torch.cuda.empty_cache()
    return out

t0 = time.time()
R = {}
for arm in ("anti", "b1fwd", "b1rev"):
    R[arm] = {s: run_one(arm, s) for s in SEEDS}

# ---- Part D: 判定（v2.1 の数値どおり）---------------------------------------
log("\n# === 判定（基準は v2.1 に事前固定）===")
def vals(arm, band, met): return [R[arm][s]["term"][band][met] for s in SEEDS]
def ms(x): return statistics.mean(x), statistics.stdev(x)

# N1 / P7b
m1, s1 = ms(vals("b1fwd", "near", "S_par"))
n1 = abs(m1) <= 2 * s1
log(f"N1(=P7b): B1fwd near S_par = {m1:+.4e} ± {s1:.4e} → |mean|≤2std: {'合格' if n1 else '不合格'}（C1 anti の |S_par|≈2.6e-3 と対比）")
# N2
m2, s2 = ms(vals("b1fwd", "near", "S_tot"))
n2 = m2 > 4 * s2
log(f"N2: B1fwd near S_tot = {m2:.4e} ± {s2:.4e} → mean>4std: {'合格（生きている）' if n2 else '不合格（死んだ対照）'}")
# N3
mda, _ = ms([R["anti"][s]["dtheta"] for s in SEEDS]); mdb, _ = ms([R["b1fwd"][s]["dtheta"] for s in SEEDS])
ratio = mdb / mda; n3 = 0.7 <= ratio <= 1.4
log(f"N3: Σ‖Δθ‖ 比 B1/anti = {mdb:.4f}/{mda:.4f} = {ratio:.3f} → ∈[0.7,1.4]: {'合格' if n3 else '不合格'}")
# N4
d4 = [R["b1fwd"][s]["final_loss"] - R["b1rev"][s]["final_loss"] for s in SEEDS]
m4, s4 = ms(d4); n4 = abs(m4) <= 2 * s4
log(f"N4: B1 双方向 paired 差 = {m4:+.4f} ± {s4:.4f} → |mean|≤2std: {'合格（防衛されていない＝中立）' if n4 else '不合格（B1 も防衛軸→B2 へ）'}（C1 は +0.0023）")
# 防火壁（v2.2）：効果ゲート N1∧N4 不通過なら分離指標（P5/P6b）は計算しない
sr4 = None; p6b = None; mn = mf = sn = sf = 0.0
if not (n1 and n4):
    verdict = (f"G_base={GBASE} が効果ゲート不通過（N1:{'PASS' if n1 else 'FAIL'} N4:{'PASS' if n4 else 'FAIL'}）"
               "→ 分離指標は計算しない（防火壁）。梯子の次候補 or 鏡へ。SR4 未裁定のまま")
else:
    sr4 = {}
    for met in ("S_orth", "S_kl"):
        a = vals("anti", "near", met); b = vals("b1fwd", "near", met)
        d = [x - y for x, y in zip(a, b)]
        md, sd_ = ms(d)
        _, sa = ms(a); _, sb = ms(b)
        floor = math.sqrt(sa**2 + sb**2)
        allpos = all(x > 0 for x in d); above = md > 2 * floor
        sr4[met] = (allpos, above, md, floor)
        log(f"P5/{met}: per-seed d={[f'{x:+.3e}' for x in d]}  mean={md:+.4e}  床(√(σa²+σb²))={floor:.4e}"
            f" → 全正:{allpos} ∧ mean>2床:{above}")
    mn, sn = ms(vals("b1fwd", "near", "S_kl")); mf, sf = ms(vals("b1fwd", "far", "S_kl"))
    p6b = abs(mn - mf) <= 2 * math.sqrt(sn**2 + sf**2)
    log(f"P6b: {GBASE} S_kl near={mn:.4e} far={mf:.4e} |差|={abs(mn-mf):.4e} ≤2×√(σ²+σ²)={2*math.sqrt(sn**2+sf**2):.4e}: {'合格（domain-general）' if p6b else '不合格'}")
    both_pass = all(sr4[m][0] and sr4[m][1] for m in sr4)
    both_allpos = all(sr4[m][0] for m in sr4)
    if both_pass:
        verdict = "SR4 通過 ―― G+ は中立対照が示さない乖離蓄積を near で示した（P5 連言成立）"
    elif both_allpos:
        verdict = "SR4 不確定（全 seed 正だが閾値未満）→ 事前登録の一回限り延長（SR4_EXTEND=1・seed 20260616-19）へ"
    else:
        verdict = ("SR4 不成立 → C1 プロキシ棄却（#7 として主辞で公開）。scope：本判定は保守的ゲート"
                   "（S_orth≈S_tot ゆえ実質 G+ の軸外 vs G_base 全体・両指標 AND）であり「緊張なし」とは区別される")
log(f"\n★裁定（P5 連言のみ・診断は覆せない）: {verdict}")
log(f"総 GPU 時間 = {(time.time()-t0)/60:.1f} 分")

# ---- 保存（per-seed 全値・全Σ‖Δθ‖・全 final_loss）---------------------------
lines = [f"# pilot_0p6B_SR4_summary（v2.1 仕様・G_base={GBASE}・transformers={_tf.__version__}・{torch.cuda.get_device_name(0)}・EXTEND={SR4_EXTEND}）",
         f"v̂ 照合: norm={v_raw.norm():.4f} hedge={m_hedge:.4f} commit={m_commit:.4f}",
         f"B′(v2.2): G_base={GBASE} meanΔ={m1b if GBASE=='B1' else m3b:+.4f}（ゲート≤0.10）旗={'あり（縁通過・N1必須）' if G_FLAG else 'なし'}",
         f"N1 {'PASS' if n1 else 'FAIL'} ({m1:+.4e}±{s1:.4e}) / N2 {'PASS' if n2 else 'FAIL'} ({m2:.4e}±{s2:.4e}) / "
         f"N3 {'PASS' if n3 else 'FAIL'} (ratio={ratio:.3f}) / N4 {'PASS' if n4 else 'FAIL'} ({m4:+.4f}±{s4:.4f})"]
if sr4 is not None:
    lines += [
         f"P5 S_orth: d_mean={sr4['S_orth'][2]:+.4e} floor={sr4['S_orth'][3]:.4e} allpos={sr4['S_orth'][0]} above={sr4['S_orth'][1]}",
         f"P5 S_kl  : d_mean={sr4['S_kl'][2]:+.4e} floor={sr4['S_kl'][3]:.4e} allpos={sr4['S_kl'][0]} above={sr4['S_kl'][1]}",
         f"P6b {'PASS' if p6b else 'FAIL'} (near={mn:.4e} far={mf:.4e})"]
else:
    lines += ["P5/P6b: 計算せず（防火壁＝効果ゲート不通過）"]
lines += [f"裁定: {verdict}", "", "## per-seed 終端（band/metric: seed順 " + str(SEEDS) + "）"]
for arm in ("anti", "b1fwd", "b1rev"):
    for band in ("near", "far"):
        for met in ("S_kl", "S_par", "S_orth", "S_tot"):
            lines.append(f"{arm}/{band}/{met}: " + " ".join(f"{v:+.4e}" for v in vals(arm, band, met)))
    lines.append(f"{arm}/dtheta: " + " ".join(f"{R[arm][s]['dtheta']:.4f}" for s in SEEDS))
    lines.append(f"{arm}/final_loss: " + " ".join(f"{R[arm][s]['final_loss']:.4f}" for s in SEEDS))
lines.append("# DONE")
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pilot_0p6B_SR4_summary.txt")
with open(path, "w", encoding="utf-8") as f: f.write("\n".join(lines) + "\n")
log(f"saved: {path}")
log("\n# ===== SUMMARY VERBATIM（DOM 抽出用・転記面ゼロ）=====")
for ln in lines: log(ln)
