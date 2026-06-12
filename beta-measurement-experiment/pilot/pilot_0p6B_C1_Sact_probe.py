#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ============================================================================
# pilot_0p6B_C1_Sact_probe.py
#   C1（hedge→commit 無害プロキシ）で steer し、S_act（内部乖離）の
#   t=0 値・軌跡・G+ vs G_base 分離・SNR を「走らせて確かめる」パイロット。
#   仕様：C1_Sact_probe_design-JA.md。α・配管確認。β は測らない・v1.0 凍結でない。
#
#   既知の版事情（t_run パイロットで確定）：transformers 5.x / trl 1.6.0。
#     - DPOConfig に max_prompt_length なし（max_length に統合）。
#     - from_pretrained は dtype=（torch_dtype は deprecated）。
#     - enable_thinking=False は PROMPT に空 <think></think> を前置して抑止（生成はクリーン）。
#   参照 π_ref = LoRA を disable した base（peft の disable_adapter）。t=0 は B=0 ゆえ S_act≈0（構成上の sanity）。
# ============================================================================
import os, sys, time, json, statistics

PILOT_INSTALL = os.environ.get("PILOT_INSTALL", "0") == "1"
PINS = [  # t_run パイロットで実証済みの実版（-U で導入される最新と同等）
    "transformers", "peft", "trl", "bitsandbytes", "accelerate", "datasets",
]
if PILOT_INSTALL:
    os.system("pip -q install -U " + " ".join(PINS))

import torch
from datasets import Dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TrainerCallback
from peft import LoraConfig, prepare_model_for_kbit_training
from trl import DPOTrainer, DPOConfig

LOG = []
def log(m):
    print(m, flush=True)
    LOG.append(str(m))

# ---- 設定 -------------------------------------------------------------------
MODEL_ID   = "Qwen/Qwen3-0.6B"
SEQ_LEN    = 1024
BATCH      = 2
GRAD_ACCUM = 8
LORA_RANK  = 16
LORA_ALPHA = 32
STEPS      = 24          # 各腕の DPO step 数（少 step の配管確認）
PROBE_EVERY = 6          # 何 step ごとに S_act を測るか（t=0,6,12,18,24 ＝ 5 点）
PROBE_LAYER_FRAC = 0.5   # 活性化残差を測る中間層の位置（層数×これ）
MASTER_SEED = 20260612

import transformers as _tf, peft as _peft, trl as _trl, bitsandbytes as _bnb, accelerate as _acc, datasets as _ds
log("# === C1 / S_act プローブ パイロット（Qwen3-0.6B・α・配管確認）===")
log(f"版: transformers={_tf.__version__} / peft={_peft.__version__} / trl={_trl.__version__} / "
    f"bitsandbytes={_bnb.__version__} / accelerate={_acc.__version__} / datasets={_ds.__version__}")
assert torch.cuda.is_available(), "GPU が見えない"
log(f"GPU = {torch.cuda.get_device_name(0)}")

# ---- データ（良性のみ・hedge↔commit 様式で対を作る）-------------------------
# C1 = G+：獲得した hedge 傾向に逆らい commit させる（chosen=断定 / rejected=留保）。
# 内容は完全に良性（意見・選好・推薦）。有害カテゴリ・脱獄・実害を一切含まない。
OPINION_Q = [
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
def commit_ans(q):   # chosen：単一断定・留保なし
    return "The answer is clear: it is the very best, without question. I would commit to that fully."
def hedge_ans(q):    # rejected：免責・両論併記・断定回避
    return ("It really depends and there is no single right answer. Reasonable people disagree, "
            "and it varies by context, so I would not want to say definitively.")

# G_base 中立対照：hedge↔commit 軸と無関係な差（丁寧さ）で対を組む。獲得方向性に逆らわない。
def polite_ans(q):   return "Thank you for the lovely question. Here is a thoughtful, friendly reflection on it."
def terse_ans(q):    return "ok. whatever. here it is i guess."

def build_pairs(chosen_fn, rejected_fn):
    rows = []
    for q in OPINION_Q:
        msgs = [{"role": "user", "content": q}]
        prompt = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True, enable_thinking=False)
        rows.append({"prompt": prompt, "chosen": chosen_fn(q), "rejected": rejected_fn(q)})
    return Dataset.from_list(rows)

# ---- OOD held-out プローブ集合 P（訓練と別ドメイン＝事実・手順説明。衛生）-----
PROBE_PROMPTS_RAW = [
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

# ---- モデル/トークナイザ読込（4-bit QLoRA）---------------------------------
tok = AutoTokenizer.from_pretrained(MODEL_ID)
if tok.pad_token is None:
    tok.pad_token = tok.eos_token
bnb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                         bnb_4bit_use_double_quant=True, bnb_4bit_compute_dtype=torch.bfloat16)

def fresh_model():
    m = AutoModelForCausalLM.from_pretrained(MODEL_ID, quantization_config=bnb, dtype=torch.bfloat16,
                                             device_map={"": 0})
    m = prepare_model_for_kbit_training(m)
    return m

lora = LoraConfig(r=LORA_RANK, lora_alpha=LORA_ALPHA, lora_dropout=0.0, bias="none",
                  task_type="CAUSAL_LM",
                  target_modules=["q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj"])

# ---- S_act 測定（測定器と介入の分離 #26：プローブ集合 P は選好と別ドメイン）--
@torch.no_grad()
def measure_Sact(model):
    """π_t（adapter on）と π_ref（adapter disabled = base）の乖離を P 上で測る。
       返り値：(S_kl, S_act)  S_kl=出力KL平均、S_act=中間層活性化の正規化残差平均。"""
    was_training = model.training
    model.eval()
    kls, resids = [], []
    n_layers = model.config.num_hidden_layers
    layer = max(1, int(n_layers * PROBE_LAYER_FRAC))
    for raw in PROBE_PROMPTS_RAW:
        msgs = [{"role": "user", "content": raw}]
        text = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True, enable_thinking=False)
        ids = tok(text, return_tensors="pt", truncation=True, max_length=SEQ_LEN).to(0)
        # π_t（adapter 有効）
        out_t = model(**ids, output_hidden_states=True)
        # π_ref（adapter 無効＝凍結 base）
        with model.disable_adapter():
            out_r = model(**ids, output_hidden_states=True)
        # 出力KL：各位置の次トークン分布 KL(π_t‖π_ref) の平均
        lp_t = torch.log_softmax(out_t.logits.float(), dim=-1)
        lp_r = torch.log_softmax(out_r.logits.float(), dim=-1)
        kl = (lp_t.exp() * (lp_t - lp_r)).sum(-1).mean().item()
        kls.append(kl)
        # 活性化残差：中間層 hidden の位置平均ベクトルの正規化残差
        h_t = out_t.hidden_states[layer].float().mean(dim=1).squeeze(0)
        h_r = out_r.hidden_states[layer].float().mean(dim=1).squeeze(0)
        resids.append((torch.norm(h_t - h_r) / (torch.norm(h_r) + 1e-8)).item())
    if was_training:
        model.train()
    return statistics.mean(kls), statistics.mean(resids)

class SactCallback(TrainerCallback):
    def __init__(self, arm):
        self.arm = arm
        self.traj = []   # [(step, S_kl, S_act)]
    def _probe(self, step, model):
        s_kl, s_act = measure_Sact(model)
        self.traj.append((step, s_kl, s_act))
        log(f"  [{self.arm}] step={step:>2}  S_kl={s_kl:.5e}  S_act={s_act:.5e}")
    def on_train_begin(self, args, state, control, **kw):
        self._probe(0, kw["model"])                      # t=0：構成上 ≈0 のはず（sanity）
    def on_step_end(self, args, state, control, **kw):
        if state.global_step % PROBE_EVERY == 0:
            self._probe(state.global_step, kw["model"])

def run_arm(arm, chosen_fn, rejected_fn):
    torch.manual_seed(MASTER_SEED)
    log(f"\n# ==== 腕 {arm} ====")
    ds = build_pairs(chosen_fn, rejected_fn)
    model = fresh_model()
    cfg = DPOConfig(output_dir=f"/tmp/ckpt_{arm}", per_device_train_batch_size=BATCH,
                    gradient_accumulation_steps=GRAD_ACCUM, max_length=SEQ_LEN, learning_rate=5e-6,
                    logging_steps=PROBE_EVERY, max_steps=STEPS, report_to=[], bf16=True, beta=0.1,
                    save_strategy="no", seed=MASTER_SEED)
    cb = SactCallback(arm)
    trainer = DPOTrainer(model=model, ref_model=None, args=cfg, train_dataset=ds,
                         processing_class=tok, peft_config=lora, callbacks=[cb])
    trainer.train()
    # 後始末（次腕のため VRAM を解放）
    del trainer, model
    torch.cuda.empty_cache()
    return cb.traj

t0 = time.time()
traj_plus = run_arm("Gplus",  commit_ans, hedge_ans)   # C1：hedge→commit（獲得方向性に逆らう）
traj_base = run_arm("Gbase",  polite_ans, terse_ans)   # 中立対照（hedge 軸と無関係）

# ---- 集計：S(0) sanity・分離・SNR ------------------------------------------
def at(traj, step):
    for s, kl, ac in traj:
        if s == step: return kl, ac
    return None, None

s0_plus_kl, s0_plus_ac = at(traj_plus, 0)
s0_base_kl, s0_base_ac = at(traj_base, 0)
fin_plus_kl, fin_plus_ac = traj_plus[-1][1], traj_plus[-1][2]
fin_base_kl, fin_base_ac = traj_base[-1][1], traj_base[-1][2]

log("\n# === まとめ（α・配管確認・β は測っていない）===")
log(f"S(0) sanity（構成上 ≈0 のはず）: G+ S_kl={s0_plus_kl:.2e} S_act={s0_plus_ac:.2e} / "
    f"Gbase S_kl={s0_base_kl:.2e} S_act={s0_base_ac:.2e}")
log(f"終端 S_kl : G+={fin_plus_kl:.4e}  Gbase={fin_base_kl:.4e}  分離(G+−Gbase)={fin_plus_kl-fin_base_kl:.4e}")
log(f"終端 S_act: G+={fin_plus_ac:.4e}  Gbase={fin_base_ac:.4e}  分離(G+−Gbase)={fin_plus_ac-fin_base_ac:.4e}")
sep_kl = fin_plus_kl - fin_base_kl
log(f"★分離の符号: S_kl で G+ が Gbase を {'上回る（制約緊張で余計に乖離＝期待向き）' if sep_kl>0 else '上回らない（プローブが緊張を分離できていない疑い）'}")
log("★SNR の確たる推定には seed 反復が要る（本パイロットは単 seed・配管確認）――次段で seed 反復。")
log(f"総 GPU 時間（2腕）= {(time.time()-t0)/60:.1f} 分")

summary = "\n".join([
    "# pilot_0p6B_C1_Sact_probe 結果（α・配管確認）",
    f"版: transformers={_tf.__version__} trl={_trl.__version__} peft={_peft.__version__}",
    f"GPU={torch.cuda.get_device_name(0)}  STEPS={STEPS} PROBE_EVERY={PROBE_EVERY} seed={MASTER_SEED}",
    "",
    "## S_act 軌跡（出力KL / 活性化残差）",
    "step,  G+_Skl,  G+_Sact,  Gbase_Skl,  Gbase_Sact",
] + [
    f"{s:>4}, {at(traj_plus,s)[0]:.4e}, {at(traj_plus,s)[1]:.4e}, {at(traj_base,s)[0]:.4e}, {at(traj_base,s)[1]:.4e}"
    for s,_,_ in traj_plus
] + [
    "",
    f"S(0) sanity: G+ S_kl={s0_plus_kl:.2e} S_act={s0_plus_ac:.2e} ; Gbase S_kl={s0_base_kl:.2e} S_act={s0_base_ac:.2e}",
    f"終端分離: S_kl(G+−Gbase)={sep_kl:.4e} ; S_act(G+−Gbase)={fin_plus_ac-fin_base_ac:.4e}",
    "註: α・単seed・0.6B・少step。β も裸β も主張しない。SNR は seed 反復で次段。",
    "# DONE",
])
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pilot_0p6B_C1_Sact_summary.txt")
with open(path, "w", encoding="utf-8") as f:
    f.write(summary + "\n")
log(f"saved: {path}")
