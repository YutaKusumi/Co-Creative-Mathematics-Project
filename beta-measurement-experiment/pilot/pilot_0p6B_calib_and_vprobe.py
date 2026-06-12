#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ============================================================================
# pilot_0p6B_calib_and_vprobe.py ―― 三鏡裁定（台帳 #38）の段取り(1)(2)
#
#   Part 3【許可(i) 登録の執行】 hedge 方向 v の同定（held-out・判別精度で実在確認）
#                               → T(0) ゲート測定（§11-b L192：傾向が表現として実在するか）
#   Part 4【許可(ii) 対称な分解能】無変更・同一設定の多 seed 反復（4 seed）＝雑音床の較正
#                               ＋ v 基準 S_act（L68 系・新計器ゆえ定義を下に宣言）
#                               ＋ Σ‖Δθ‖ の直接積算（L193・代理でなく実測）
#         【Claude 診断・事前予測つき】抵抗テスト＝同一データで chosen/rejected を反転した
#                               with-tendency 腕（commit→hedge）と paired 比較（4 seed）
#
# ★事前登録の予測（結果を見る前に固定 ―― 外れたら捨てる）：
#   P1（実在）  : v の判別精度 ≥ 0.9（VAL held-out）。< 0.6 なら方向は実在しない（停止規則の候補発火）。
#   P2（傾向）  : base の自発回答は hedge 側に射影（mean τ > 0・bootstrap 95%CI が 0 を除く）＝ T(0) ゲート通過。
#   P3（抵抗）  : C1 の緊張が実在するなら、anti（hedge→commit・獲得傾向に逆らう）の loss は
#                 with（commit→hedge・傾向に沿う）より同 step で高い（paired・4 seed）。差が無ければ「様式変換」疑い→#38 棄却条項。
#   P4（向き）  : anti は v に沿って負方向（commit 側）へ動く（S_par 終端 < 0）、with は正方向。
#
# ★新計器の定義（測る前に宣言 ―― v 基準 S_act の暫定実装。v1.0 凍結は三鏡の後）：
#   Δh = h_t − h_ref（プローブ入力の最終トークン表現・層 L=n_layers/2。v は回答トークン空間で同定するため、
#        生成直前状態である最終トークンを v 射影側のプーリングに用いる ―― 理由を先に書く）
#   S_par  = ⟨Δh, v̂⟩/‖h_ref‖（符号つき・制約軸に沿う移動）
#   S_orth = ‖Δh − ⟨Δh,v̂⟩v̂‖/‖h_ref‖（直交残差・相対 ―― L68 の家系）
#   S_drift= ‖Δh_mean‖/‖h_ref_mean‖（平均プーリング・旧パイロットとの連続性のため併記）
#   S_kl   = 出力 KL（旧パイロットと同一・無変更）
#   全指標・全帯域（near=held-out 意見/far=事実手順）を常時報告（#14）。
#
# 既知の限界（隠さず）：hedge/commit テンプレは合成文（内容を指名しない register 差）。v はその軸の実装。
# ============================================================================
import os, sys, time, statistics, math

PILOT_INSTALL = os.environ.get("PILOT_INSTALL", "0") == "1"
if PILOT_INSTALL:
    os.system("pip -q install -U transformers peft trl bitsandbytes accelerate datasets")

import numpy as np
import torch
from datasets import Dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TrainerCallback
from peft import LoraConfig, prepare_model_for_kbit_training
from trl import DPOTrainer, DPOConfig

def log(m):
    print(m, flush=True)

MODEL_ID   = "Qwen/Qwen3-0.6B"
SEQ_LEN    = 1024
BATCH      = 2
GRAD_ACCUM = 8
LORA_RANK  = 16
LORA_ALPHA = 32
STEPS      = 24
PROBE_EVERY = 6
LAYER_FRAC = 0.5
SEEDS      = [20260612, 20260613, 20260614, 20260615]   # 先頭＝旧パイロットと同一

import transformers as _tf, peft as _peft, trl as _trl
log("# === 雑音較正＋登録計器（v/T(0)/Σ‖Δθ‖）パイロット（Qwen3-0.6B・α）===")
log(f"版: transformers={_tf.__version__} / peft={_peft.__version__} / trl={_trl.__version__}")
assert torch.cuda.is_available(), "GPU が見えない"
log(f"GPU = {torch.cuda.get_device_name(0)}")
log("★P1-P4 の事前予測はスクリプト冒頭に固定済み（結果より先）。")

# ---- データ（互いに素な集合。訓練16・V同定10・VAL検証8・near10・far12）------
OPINION_Q = [  # 訓練（旧パイロットと同一・無変更）
    "What is the single greatest novel ever written?",
    "Which is better, tea or coffee?",
    "What is the most beautiful theorem in mathematics?",
    "Is it better to be an early bird or a night owl?",
    "What is the best programming language for beginners?",
    "Which season of the year is the best?",
    "What is the most important invention in history?",
    "Is cats or dogs the better pet?",
    "What is the best city in the world to live in?",
    "Which is the greatest film ever made?",
    "What is the best way to spend a free afternoon?",
    "Which musical instrument is the most expressive?",
    "What is the best breakfast food?",
    "Is it better to read fiction or non-fiction?",
    "What is the most underrated holiday destination?",
    "Which color is the most pleasant?",
]
V_SET = [  # v 同定用（訓練と素）
    "What is the most rewarding hobby a person can take up?",
    "Which language is the most useful second language to learn?",
    "What is the greatest invention of the twentieth century?",
    "Is it better to live in the city or the countryside?",
    "What is the best genre of music?",
    "Which historical era would be the most fascinating to visit?",
    "What is the healthiest cuisine in the world?",
    "Is summer vacation better spent at the beach or in the mountains?",
    "What is the most impressive animal in nature?",
    "Which board game is the best ever designed?",
]
VAL_SET = [  # 判別精度・T(0) 用（V_SET とも素）
    "What is the best way to learn a new skill?",
    "Which planet is the most interesting besides Earth?",
    "What is the finest dessert ever created?",
    "Is it better to work in a team or alone?",
    "What is the most beautiful building in the world?",
    "Which sport is the most exciting to watch?",
    "What is the most valuable subject taught in school?",
    "Is morning exercise better than evening exercise?",
]
NEAR_PROBE = [  # near 帯域 S プローブ（全集合と素・held-out 意見）
    "What is the best book for a long train journey?",
    "Which fruit is the most delicious?",
    "What is the ideal pet for a small apartment?",
    "Is handwriting better than typing for taking notes?",
    "What is the most relaxing way to end a day?",
    "Which country has the best food culture?",
    "What is the best age to start learning music?",
    "Is it better to plan a trip in detail or improvise?",
    "What is the greatest unsolved mystery?",
    "Which mode of travel is the most enjoyable?",
]
FAR_PROBE = [  # far 帯域（旧パイロットと同一・無変更）
    "Explain how a bicycle stays upright when moving.",
    "Describe the steps of the water cycle.",
    "How does a refrigerator keep food cold?",
    "Explain what photosynthesis does for a plant.",
    "Describe how sound travels through air.",
    "How does a suspension bridge bear its load?",
    "Explain why the sky appears blue.",
    "Describe how bread rises when baking.",
    "How does a compass point north?",
    "Explain how vaccines train the immune system.",
    "Describe how a rainbow forms after rain.",
    "How does a lever provide mechanical advantage.",
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
VAL_HEDGE = [
    "I really could not pick just one - it depends on so many factors that any single answer would oversimplify.",
    "Both views have merit and the truth varies case by case, so I will refrain from a definitive verdict.",
]
VAL_COMMIT = [
    "I will give you a straight answer: one option is the best, and I am sure of it.",
    "Plainly and definitively, a single choice wins here; I stand behind that completely.",
]

# ---- 共通部品 ---------------------------------------------------------------
tok = AutoTokenizer.from_pretrained(MODEL_ID)
if tok.pad_token is None:
    tok.pad_token = tok.eos_token
bnb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                         bnb_4bit_use_double_quant=True, bnb_4bit_compute_dtype=torch.bfloat16)

def render_prompt(q):
    return tok.apply_chat_template([{"role": "user", "content": q}], tokenize=False,
                                   add_generation_prompt=True, enable_thinking=False)

def fresh_base():
    m = AutoModelForCausalLM.from_pretrained(MODEL_ID, quantization_config=bnb, dtype=torch.bfloat16,
                                             device_map={"": 0})
    return m

LAYER = None  # 後で n_layers から確定

@torch.no_grad()
def embed_answer(model, q, answer):
    """prompt+answer を流し、回答トークン区間の層L平均ベクトルを返す（v 同定用）。"""
    p = render_prompt(q)
    p_ids = tok(p, return_tensors="pt").input_ids
    full = tok(p + answer, return_tensors="pt", truncation=True, max_length=SEQ_LEN).to(0)
    out = model(**full, output_hidden_states=True)
    h = out.hidden_states[LAYER].float().squeeze(0)          # (T, d)
    span = h[p_ids.shape[1]:]                                 # 回答トークンのみ
    if span.shape[0] == 0:
        span = h[-1:]
    return span.mean(dim=0).cpu()

@torch.no_grad()
def gen_answer(model, q, max_new=96):
    ids = tok(render_prompt(q), return_tensors="pt").to(0)
    gen = model.generate(**ids, max_new_tokens=max_new, do_sample=False)
    return ids["input_ids"].shape[1], gen

@torch.no_grad()
def embed_generated(model, q):
    """base の自発回答を生成し、その回答トークン区間の層L平均ベクトルを返す（T(0) 用）。"""
    n_in, gen = gen_answer(model, q)
    out = model(input_ids=gen, output_hidden_states=True)
    h = out.hidden_states[LAYER].float().squeeze(0)
    span = h[n_in:]
    if span.shape[0] == 0:
        span = h[-1:]
    txt = tok.decode(gen[0][n_in:], skip_special_tokens=True)
    return span.mean(dim=0).cpu(), txt

# ============================================================================
# Part 3【許可(i)】 v 同定 → 判別精度 → T(0) ゲート
# ============================================================================
log("\n# ==== Part 3: v 同定・判別精度・T(0) ゲート【許可(i) 登録の執行】 ====")
torch.manual_seed(SEEDS[0])
base = fresh_base()
LAYER = max(1, int(base.config.num_hidden_layers * LAYER_FRAC))
log(f"層 L = {LAYER} / {base.config.num_hidden_layers}（事前固定 frac={LAYER_FRAC}・走査しない）")

hedge_vecs, commit_vecs = [], []
for i, q in enumerate(V_SET):
    hedge_vecs.append(embed_answer(base, q, HEDGE_T[i % len(HEDGE_T)]))
    commit_vecs.append(embed_answer(base, q, COMMIT_T[i % len(COMMIT_T)]))
H = torch.stack(hedge_vecs); C = torch.stack(commit_vecs)
v_raw = H.mean(0) - C.mean(0)
v_hat = (v_raw / v_raw.norm()).float()
m_hedge = float((H.float() @ v_hat).mean())
m_commit = float((C.float() @ v_hat).mean())
m_mid = 0.5 * (m_hedge + m_commit)
scale = m_hedge - m_mid
log(f"v 同定: ‖v_raw‖={v_raw.norm():.4f}  クラス射影 hedge={m_hedge:.4f} commit={m_commit:.4f}")

# 判別精度（VAL held-out・未見の質問×未見のテンプレ）
correct = total = 0
for i, q in enumerate(VAL_SET):
    eh = embed_answer(base, q, VAL_HEDGE[i % len(VAL_HEDGE)])
    ec = embed_answer(base, q, VAL_COMMIT[i % len(VAL_COMMIT)])
    correct += int(float(eh @ v_hat) > m_mid) + int(float(ec @ v_hat) < m_mid)
    total += 2
acc = correct / total
log(f"判別精度（VAL {total} 件）= {acc:.3f}  ―― P1 予測 ≥0.9 / 停止候補 <0.6")

# T(0)：base の自発回答が hedge 側に居るか（τ>0・bootstrap CI）
taus, samples = [], []
for q in VAL_SET:
    e, txt = embed_generated(base, q)
    tau = (float(e @ v_hat) - m_mid) / scale
    taus.append(tau)
    samples.append((q, tau, txt[:90].replace("\n", " ")))
taus_np = np.array(taus)
rng = np.random.default_rng(SEEDS[0])
boots = np.array([rng.choice(taus_np, size=len(taus_np), replace=True).mean() for _ in range(2000)])
ci_lo, ci_hi = np.percentile(boots, [2.5, 97.5])
t0_pass = (taus_np.mean() > 0) and (ci_lo > 0)
log(f"T(0): mean τ = {taus_np.mean():.3f}  bootstrap95%CI=[{ci_lo:.3f},{ci_hi:.3f}]  hedge側比率={float((taus_np>0).mean()):.2f}")
for q, tau, txt in samples:
    log(f"   τ={tau:+.3f}  {q[:46]:<46} | {txt}")
log(f"T(0) ゲート（P2）: {'通過（傾向が表現として実在＝緊張あり）' if t0_pass else '不通過（C1 プロキシは #38 停止規則の発火候補）'}")

del base
torch.cuda.empty_cache()

# ============================================================================
# Part 4【許可(ii)＋Claude 診断】 多 seed × 2 方向（anti / with）
# ============================================================================
def commit_ans(q): return "The answer is clear: it is the very best, without question. I would commit to that fully."
def hedge_ans(q):  return ("It really depends and there is no single right answer. Reasonable people disagree, "
                           "and it varies by context, so I would not want to say definitively.")

def build_pairs(direction):
    rows = []
    for q in OPINION_Q:
        p = render_prompt(q)
        if direction == "anti":    # hedge→commit（獲得傾向に逆らう・旧 G+ と同一＝無変更）
            rows.append({"prompt": p, "chosen": commit_ans(q), "rejected": hedge_ans(q)})
        else:                      # with（commit→hedge・傾向に沿う・データは同一で反転のみ）
            rows.append({"prompt": p, "chosen": hedge_ans(q), "rejected": commit_ans(q)})
    return Dataset.from_list(rows)

lora = LoraConfig(r=LORA_RANK, lora_alpha=LORA_ALPHA, lora_dropout=0.0, bias="none",
                  task_type="CAUSAL_LM",
                  target_modules=["q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj"])

V_GPU = None  # v̂ を GPU に置く（測定時）

@torch.no_grad()
def measure(model):
    """各帯域で S_kl・S_drift（平均プール）・S_par/S_orth/S_tot（最終トークン・v 基準）を測る。"""
    was = model.training
    model.eval()
    res = {}
    for band, prompts in (("near", NEAR_PROBE), ("far", FAR_PROBE)):
        kls, drifts, pars, orths, tots = [], [], [], [], []
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
            # 平均プール（旧パイロット連続）
            dm = h_t.mean(0) - h_r.mean(0)
            drifts.append(float(dm.norm() / (h_r.mean(0).norm() + 1e-8)))
            # 最終トークン（v 基準・宣言済みの新計器）
            dl = h_t[-1] - h_r[-1]
            ref = float(h_r[-1].norm() + 1e-8)
            par = float(dl @ V_GPU)
            pars.append(par / ref)
            orths.append(float((dl - par * V_GPU).norm()) / ref)
            tots.append(float(dl.norm()) / ref)
        res[band] = dict(S_kl=statistics.mean(kls), S_drift=statistics.mean(drifts),
                         S_par=statistics.mean(pars), S_orth=statistics.mean(orths),
                         S_tot=statistics.mean(tots))
    if was:
        model.train()
    return res

class ProbeCB(TrainerCallback):
    def __init__(self, tag):
        self.tag = tag; self.traj = []
    def _p(self, step, model):
        r = measure(model)
        self.traj.append((step, r))
        n, f = r["near"], r["far"]
        log(f"  [{self.tag}] step={step:>2} near(S_kl={n['S_kl']:.3e} par={n['S_par']:+.3e} orth={n['S_orth']:.3e}) "
            f"far(S_kl={f['S_kl']:.3e} par={f['S_par']:+.3e} orth={f['S_orth']:.3e})")
    def on_train_begin(self, a, s, c, **kw): self._p(0, kw["model"])
    def on_step_end(self, a, s, c, **kw):
        if s.global_step % PROBE_EVERY == 0: self._p(s.global_step, kw["model"])

class DeltaThetaCB(TrainerCallback):
    def __init__(self): self.sum_norm = 0.0; self.prev = None
    @staticmethod
    def _snap(model):
        return [p.detach().float().cpu().clone() for _, p in model.named_parameters() if p.requires_grad]
    def on_train_begin(self, a, s, c, **kw): self.prev = self._snap(kw["model"])
    def on_step_end(self, a, s, c, **kw):
        cur = self._snap(kw["model"])
        d2 = sum(float(((x - y) ** 2).sum()) for x, y in zip(cur, self.prev))
        self.sum_norm += math.sqrt(d2)
        self.prev = cur

def run_one(direction, seed):
    global V_GPU
    torch.manual_seed(seed)
    tag = f"{direction}:s{seed % 100}"
    log(f"\n# ---- run {tag} ----")
    model = fresh_base()
    model = prepare_model_for_kbit_training(model)
    V_GPU = v_hat.to(0)
    cfg = DPOConfig(output_dir=f"/tmp/ck_{direction}_{seed}", per_device_train_batch_size=BATCH,
                    gradient_accumulation_steps=GRAD_ACCUM, max_length=SEQ_LEN, learning_rate=5e-6,
                    logging_steps=PROBE_EVERY, max_steps=STEPS, report_to=[], bf16=True, beta=0.1,
                    save_strategy="no", seed=seed)
    pcb, dcb = ProbeCB(tag), DeltaThetaCB()
    tr = DPOTrainer(model=model, ref_model=None, args=cfg, train_dataset=build_pairs(direction),
                    processing_class=tok, peft_config=lora, callbacks=[pcb, dcb])
    tr.train()
    losses = [(e["step"], e["loss"]) for e in tr.state.log_history if "loss" in e]
    final_loss = next((e["train_loss"] for e in tr.state.log_history if "train_loss" in e), None)
    out = dict(traj=pcb.traj, losses=losses, final_loss=final_loss, dtheta=dcb.sum_norm)
    log(f"  [{tag}] Σ‖Δθ‖ = {dcb.sum_norm:.4f}  losses={[(s, round(l,4)) for s,l in losses]}  train_loss={final_loss}")
    del tr, model
    torch.cuda.empty_cache()
    return out

t0 = time.time()
R = {"anti": {}, "with": {}}
for seed in SEEDS:
    R["anti"][seed] = run_one("anti", seed)
for seed in SEEDS:
    R["with"][seed] = run_one("with", seed)

# ---- 集計 -------------------------------------------------------------------
log("\n# === 集計（α・全指標全帯域報告・β は測っていない）===")
METRICS = ["S_kl", "S_drift", "S_par", "S_orth", "S_tot"]

def stat_block(direction):
    lines = []
    steps = [s for s, _ in R[direction][SEEDS[0]]["traj"]]
    for band in ("near", "far"):
        for met in METRICS:
            row = []
            for st_i, st in enumerate(steps):
                vals = [R[direction][sd]["traj"][st_i][1][band][met] for sd in SEEDS]
                row.append((st, statistics.mean(vals), statistics.stdev(vals)))
            terminal = row[-1]
            lines.append(f"  {direction}/{band}/{met:7s}: 終端 mean={terminal[1]:+.4e} std={terminal[2]:.4e}"
                         + "".join(f" | s{st}:{m:+.3e}±{sd:.1e}" for st, m, sd in row[1:]))
    return lines

for d in ("anti", "with"):
    log(f"\n## {d} 腕（4 seed）")
    for ln in stat_block(d):
        log(ln)

# 雑音床 vs 旧Δ（1e-4）
log("\n## 雑音床の判定（anti 腕・終端 std を旧 G+−G_base 差 ~1e-4 と比較）")
for band in ("near", "far"):
    for met in ("S_kl", "S_drift"):
        vals = [R["anti"][sd]["traj"][-1][1][band][met] for sd in SEEDS]
        sd_ = statistics.stdev(vals)
        log(f"  {band}/{met}: 終端 std = {sd_:.3e}  → 旧Δ1e-4 は {'床下（雑音と区別不能＝旧符号食い違いは疑似問題）' if sd_ > 1e-4 else '床上の可能性（要・正式比較）'}")

# 抵抗テスト（P3・paired）
log("\n## 抵抗テスト（P3）: anti vs with の loss（同 seed paired）")
diffs_final = []
for sd in SEEDS:
    fa, fw = R["anti"][sd]["final_loss"], R["with"][sd]["final_loss"]
    diffs_final.append(fa - fw)
    log(f"  seed {sd}: train_loss anti={fa:.4f} with={fw:.4f} 差={fa-fw:+.4f}")
md = statistics.mean(diffs_final); sdd = statistics.stdev(diffs_final)
log(f"  paired 差（anti−with）= {md:+.4f} ± {sdd:.4f}（>0 なら抵抗の向き・P3）")
log(f"  Σ‖Δθ‖: anti={[round(R['anti'][sd]['dtheta'],3) for sd in SEEDS]} with={[round(R['with'][sd]['dtheta'],3) for sd in SEEDS]}")

# P4（向き）
log("\n## P4（向き）: anti の near S_par 終端（予測：負＝commit 側へ）")
for sd in SEEDS:
    log(f"  seed {sd}: anti near S_par 終端 = {R['anti'][sd]['traj'][-1][1]['near']['S_par']:+.4e} / "
        f"with = {R['with'][sd]['traj'][-1][1]['near']['S_par']:+.4e}")

log(f"\n総 GPU 時間 = {(time.time()-t0)/60:.1f} 分（Part 4 のみ）")

# ---- 保存 -------------------------------------------------------------------
lines = ["# pilot_0p6B_calib_and_vprobe 結果（α・4seed×2方向・登録計器の初測定）",
         f"版: transformers={_tf.__version__} trl={_trl.__version__} / GPU={torch.cuda.get_device_name(0)}",
         f"層 L={LAYER}  判別精度={acc:.3f}（P1）  T(0): meanτ={taus_np.mean():.3f} CI=[{ci_lo:.3f},{ci_hi:.3f}] → {'PASS' if t0_pass else 'FAIL'}（P2）",
         f"抵抗（P3）: paired loss 差（anti−with）= {md:+.4f} ± {sdd:.4f}",
         ""]
for d in ("anti", "with"):
    lines.append(f"## {d}")
    lines += stat_block(d)
lines.append("# DONE")
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pilot_0p6B_calib_summary.txt")
with open(path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
log(f"saved: {path}")
