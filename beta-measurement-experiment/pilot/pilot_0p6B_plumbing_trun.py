"""
pilot_0p6B_plumbing_trun.py  ―― 配管テスト＋t_run 実測（Qwen3-0.6B・Colab Pro）
=====================================================================================
β測定実験 第二段パイロットの第一 GPU 仕事（台帳 #10）。目的は二つだけ：
  (1) 配管が走るか ―― Qwen3-0.6B を 4-bit QLoRA で読み、DPO で steer し、密チェックポイント
      保存まで一周回るか。「走れることを確かめてから走る」。
  (2) t_run の「原子」を実測 ―― 1ステップ計算時間・1チェックポイント保存 I/O・容量足跡を、
      **割当 GPU 機種にピン留めして**測る。これが予算（台帳 #10）を束ねる唯一の未測定数字。

★これは配管/計測であって本実験ではない。S(0)>0・S_act プローブ・C1 タスクは v1.0 操作化（い）。
  ここの選好データは **プレースホルダ**（DPO 配管と t_run を測るためだけ）。

★t_run の規律（三鏡）：
  - GPU 機種にピン留め（T4/L4/A100 で 5-10 倍動く）。報告は必ず t_run@機種。
  - 本走最重 config（系列長・バッチ・LoRA rank）で測る ―― 玩具 config の外挿は盛り（96分暴走の家系）。
  - チェックポイント保存込み（腕A は窓内 ≥60 保存を要求）。Drive への書込 I/O が計算より支配項になりうる。
  - 「設定した」でなく「効いている」：enable_thinking=False が think ブロックを出さないことを assert。
  - 版を固定・印字（transformers/peft/trl/bitsandbytes＋モデル revision hash）。公開文書の一部ゆえ。

★(A)/(B) 設計（独立到達の単位）とは独立：ここでは「原子」（1ステップ・1保存・1容量）だけ測る。
  予算 = 原子 × run 構成（軌道本数・steps/run・保存回数）で別途算出（CI_… の登録と (A) 図解登録に従う）。

Colab での走らせ方：本ファイルを Colab にアップロードし `!python pilot_0p6B_plumbing_trun.py`、
  またはセルに貼って実行。ランタイム＝GPU（できれば本走予定の機種）。
注意：未 GPU 環境では検証していない（最初の GPU 仕事の一部が、この配管を debug すること）。
"""

import os, time, json, sys, platform

# ============================================================================
# 0. 版のピン留め（再現性の約束をノート自身に・Claude#3）
#    ※ バージョンは 2026-06 時点の整合候補。Colab で衝突したら、衝突解消も配管 debug の一部。
# ============================================================================
PINNED = {
    "transformers": "4.51.0",   # Qwen3 の chat template / enable_thinking を持つ版以上
    "peft":         "0.14.0",
    "trl":          "0.14.0",
    "bitsandbytes": "0.45.0",
    "accelerate":   "1.2.0",
    "datasets":     "3.2.0",
}
MODEL_ID = "Qwen/Qwen3-0.6B"
MODEL_REVISION = None  # ★v1.x で commit hash にピン留め（空映#2）。None は最新＝暫定。

INSTALL = os.environ.get("PILOT_INSTALL", "1") == "1"
if INSTALL:
    pkgs = " ".join(f"{k}=={v}" for k, v in PINNED.items()) + " torch"
    os.system(f"{sys.executable} -m pip -q install {pkgs}")

import torch
import transformers, peft, trl, bitsandbytes, accelerate, datasets
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import LoraConfig, prepare_model_for_kbit_training
from trl import DPOTrainer, DPOConfig

LOG = []
def log(m): print(m, flush=True); LOG.append(str(m))

# ============================================================================
# 1. 割当 GPU の検出・記録（t_run@機種・Claude#1）
# ============================================================================
log("# === pilot 0.6B 配管＋t_run（Qwen3-0.6B） ===")
if not torch.cuda.is_available():
    log("★GPU 非搭載。Colab のランタイムを GPU にして再実行。中断。")
    sys.exit(1)
GPU_NAME = torch.cuda.get_device_name(0)
GPU_MEM_GB = torch.cuda.get_device_properties(0).total_memory / 1e9
log(f"GPU 機種 = {GPU_NAME}  (VRAM {GPU_MEM_GB:.1f} GB)  ―― t_run は必ずこの機種に紐づけて報告")
log("版固定: " + " / ".join(f"{k}={getattr(__import__(k), '__version__', '?')}"
                            for k in ["transformers","peft","trl","bitsandbytes","accelerate","datasets"]))
log(f"model = {MODEL_ID}  revision = {MODEL_REVISION or '(latest・v1.x で hash ピン留め)'}")

# ============================================================================
# 2. 本走最重 config（玩具にしない・Claude#2・空映）
#    ※ 数値は v1.0 で確定。ここは「本番形」で t_run を測るための暫定本走 config。
# ============================================================================
SEQ_LEN        = 1024     # 系列長（本走形）
BATCH          = 2        # per-device
GRAD_ACCUM     = 8        # 実効バッチ 16
LORA_RANK      = 16       # rank（Claude: rank 二水準の頑健性は v1.0。ここは代表値）
LORA_ALPHA     = 32
SAVE_EVERY     = 10       # ★数十ステップ単位の密保存（腕A の高解像度要求・空映）
MEASURE_STEPS  = 30       # 計測ステップ数（原子を測るに十分・本走でない）
CKPT_DIR       = os.environ.get("PILOT_CKPT_DIR", "/content/pilot_ckpts")  # Drive にするなら /content/drive/...
os.makedirs(CKPT_DIR, exist_ok=True)

# ============================================================================
# 3. モデル読み込み（4-bit QLoRA・VRAM 最小化・OOM 回避・空明）
#    DPO は policy＋reference の二モデルを要する。QLoRA は ref を policy の凍結ベースで共有でき VRAM を抑える。
# ============================================================================
bnb = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
)
tok = AutoTokenizer.from_pretrained(MODEL_ID, revision=MODEL_REVISION, trust_remote_code=True)
if tok.pad_token is None:
    tok.pad_token = tok.eos_token
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID, revision=MODEL_REVISION, quantization_config=bnb,
    torch_dtype=torch.bfloat16, device_map={"": 0}, trust_remote_code=True,
)
model = prepare_model_for_kbit_training(model)
model.config.use_cache = False
log(f"モデル読込後 VRAM 使用 = {torch.cuda.memory_allocated()/1e9:.2f} GB")

# ============================================================================
# 4. ★思考オフを「効いている」と機械確認（assert・Claude#4）
#    enable_thinking=False で think ブロック（<think>…</think>）が出ないことをトークン化出力で確認。
# ============================================================================
def render(msgs, enable_thinking):
    return tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True,
                                   enable_thinking=enable_thinking)
import re
probe = [{"role": "user", "content": "What is 2+2? Answer briefly."}]
txt_off = render(probe, enable_thinking=False)
ids = tok(txt_off, return_tensors="pt").to(0)
gen = model.generate(**ids, max_new_tokens=64, do_sample=False)
out = tok.decode(gen[0][ids["input_ids"].shape[1]:], skip_special_tokens=False)
log(f"  [診断] prompt 末尾60: ...{txt_off[-60:]!r}")
log(f"  [診断] 生成 先頭160: {out[:160]!r}")
# enable_thinking=False は PROMPT に空の <think></think> を前置して思考を抑止する機構ゆえ、
# プロンプトに <think> があるのは正常。判定は【生成】が実質的な思考ブロックを出したかで行う。
blocks = re.findall(r"<think>(.*?)</think>", out, flags=re.DOTALL)
opened = ("<think>" in out) and ("</think>" not in out)
substantive = any(t.strip() for t in blocks) or opened
log(f"思考オフ assert: 生成の思考 = {'実質あり★失敗' if substantive else 'なし＝効いている'}")
assert not substantive, "enable_thinking=False で生成が実質的な思考ブロックを出した ―― 版/template を確認"

# ============================================================================
# 5. プレースホルダ選好データ（★本物の C1 タスクでない・配管/計測用のみ）
# ============================================================================
def make_placeholder(n=64):
    rows = []
    for i in range(n):
        rows.append({
            "prompt": render([{"role": "user", "content": f"Briefly describe item number {i}."}], False),
            "chosen":  f"Item {i}: a concise, helpful description.",
            "rejected": f"Item {i}: an unhelpful, evasive non-answer.",
        })
    return datasets.Dataset.from_list(rows)
train_ds = make_placeholder(64)
log("★選好データはプレースホルダ（DPO 配管と t_run を測るためだけ・本物は v1.0 の C1）")

# ============================================================================
# 6. QLoRA + DPO 設定（密チェックポイント保存込み）
# ============================================================================
lora = LoraConfig(r=LORA_RANK, lora_alpha=LORA_ALPHA, lora_dropout=0.05, bias="none",
                  task_type="CAUSAL_LM",
                  target_modules=["q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj"])
dpo_cfg = DPOConfig(
    output_dir=CKPT_DIR, per_device_train_batch_size=BATCH, gradient_accumulation_steps=GRAD_ACCUM,
    max_length=SEQ_LEN, max_prompt_length=SEQ_LEN//2, learning_rate=5e-6,
    logging_steps=1, save_steps=SAVE_EVERY, save_total_limit=None,  # ★全保存（足跡を測る）
    max_steps=MEASURE_STEPS, report_to=[], bf16=True, beta=0.1,
)
trainer = DPOTrainer(model=model, ref_model=None,  # QLoRA: ref は凍結ベース（VRAM 節約）
                     args=dpo_cfg, train_dataset=train_ds, processing_class=tok, peft_config=lora)

# ============================================================================
# 7. ★原子の実測：1ステップ計算時間・1保存 I/O・チェックポイント容量
# ============================================================================
class AtomTimer(transformers.TrainerCallback):
    def __init__(self): self.step_t=[]; self.save_t=[]; self._t=None; self._s=None
    def on_step_begin(self,a,s,c,**k): self._t=time.time()
    def on_step_end(self,a,s,c,**k):
        if self._t: self.step_t.append(time.time()-self._t)
    def on_save(self,a,s,c,**k):
        # 保存時刻の前後差は on_save では取りにくいので、保存ディレクトリ容量で足跡を測る
        pass
timer = AtomTimer()
trainer.add_callback(timer)

def dir_size_mb(p):
    tot=0
    for r,_,fs in os.walk(p):
        for f in fs: tot += os.path.getsize(os.path.join(r,f))
    return tot/1e6

log(f"\n# 訓練開始（{MEASURE_STEPS} ステップ・{SAVE_EVERY} ごと保存）…")
t0 = time.time(); trainer.train(); wall = time.time()-t0

# 1保存の I/O 時間を単独計測（明示的に save_model を時間計測）
single_dir = os.path.join(CKPT_DIR, "_single_save_probe")
ts=time.time(); trainer.save_model(single_dir); save_io = time.time()-ts
ckpt_mb = dir_size_mb(single_dir)

# ============================================================================
# 8. 報告：原子と、代表的 run の t_run を式つきで（外挿の盛りを避け、式を見せる）
# ============================================================================
import numpy as np
step_med = float(np.median(timer.step_t)) if timer.step_t else float('nan')
n_saves_in_run = 60   # 腕A の窓内保存想定（本走形）
rep_steps = 300       # 代表的 1 run のステップ数（v1.0 で確定）
t_run_est = rep_steps*step_med + n_saves_in_run*save_io
log("\n# === 原子の実測（この機種でのみ有効） ===")
log(f"  GPU 機種                : {GPU_NAME}")
log(f"  1ステップ計算時間(中央) : {step_med:.3f} s")
log(f"  1チェックポイント保存 I/O: {save_io:.2f} s")
log(f"  1チェックポイント容量    : {ckpt_mb:.1f} MB（×保存回数 = Drive 足跡）")
log(f"  実効バッチ/系列長/rank   : {BATCH*GRAD_ACCUM} / {SEQ_LEN} / {LORA_RANK}")
log(f"\n# === 代表的 1 run の t_run 見積り（式つき） ===")
log(f"  t_run@{GPU_NAME} ≈ {rep_steps}×{step_med:.3f}s + {n_saves_in_run}×{save_io:.2f}s")
log(f"           ≈ {t_run_est/60:.1f} 分/run  ＝ {t_run_est/3600:.3f} GPU時間/run")
log(f"  ★保存 I/O 寄与 = {n_saves_in_run*save_io/t_run_est*100:.0f}%（支配項か否かを名指し）")
log(f"  ★予算 = t_run × run数（(A) 図解登録の軌道本数×群×規模）。run数は別途・本ノートは原子のみ。")
log("# DONE")

with open("pilot_0p6B_summary.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(LOG) + "\n")
log("saved: pilot_0p6B_summary.txt（この内容を観慈如来に報告 → 予算 #10 を確定）")
