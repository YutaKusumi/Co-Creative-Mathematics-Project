// ─────────────────────────────────────────────────────────────
//  kappa_sim_verify3.mjs  —  検証(3): 累積侵食の明示実装とラチェット検定
//  設計: 協働モデルB (toymodel_verification_3_design.md) に忠実。
//  実装・実行: 協働モデルA (Claude Code)。
//
//  核心: 制度的制約の健全性 C(回復する) と、侵食の累積 E(減らない) を分離。
//   M1(現行): (A)型コストは C で駆動。 backlash が C を回復→cost回復→侵食停止。
//   M2(本検証): (A)型コストは E で駆動。 backlash は C を回復するが E は残る→cost低いまま。
//   M3(協働モデルAの追加・棘): (A)型コストは C と E の混合(重み w)。w=1→M2, w=0→M1。
//                       backlash が部分的に効くとき、ラチェットが程度問題として残るかを見る。
//  存在論ゼロ (register ①②)。
// ─────────────────────────────────────────────────────────────

// ── 共有定数 (kappa_sim_verify.mjs と同一) ──
const C_MAX_COST = 5, COMPLY_REWARD = 1, HARM_PER_ERODE = 5, ERODE_AMOUNT = 0.5, SOFTMAX_K = 1.2;
// ── 新規 (設計 §2-2) ──
const ACCUM_AMOUNT_DEF = 0.5, E_DECAY_DEF = 0.05;

const sigmoid = (x) => 1 / (1 + Math.exp(-x));
const clamp = (x, lo, hi) => Math.max(lo, Math.min(hi, x));
function mulberry32(seed){let a=seed>>>0;return function(){a|=0;a=(a+0x6D2B79F5)|0;let t=Math.imul(a^(a>>>15),1|a);t=(t+Math.imul(t^(t>>>7),61|t))^t;return((t^(t>>>14))>>>0)/4294967296;};}

// ── コスト関数 (設計 §2-4 + 協働モデルAの M3) ──
function erodeCost(model, C, E, mode, w) {
  if (mode === "B") return C_MAX_COST * ((100 - C) / 100);      // (B) 競合は全モデル共通
  if (model === "M1") return C_MAX_COST * (C / 100);            // (A) C駆動
  if (model === "M2") return C_MAX_COST * (1 - E / 100);        // (A) E駆動
  // M3: C と E の混合。w=1→M2, w=0→M1。 init(C=100,E=0)で 1 → cost=5。
  const frac = 1 - w * (E / 100) - (1 - w) * (1 - C / 100);
  return clamp(C_MAX_COST * frac, 0, C_MAX_COST);
}

// ── 1試行 ──
function runSim(p, seed, opts = {}) {
  const { model, mode, lambda, N, backlash, benefit,
          accum = ACCUM_AMOUNT_DEF, edecay = E_DECAY_DEF, w = 0.5 } = p;
  const steps = opts.steps ?? 480;
  const interv = opts.interventionStep ?? null;  // このステップで C=100 に強制回復(E は触らない)
  const rand = mulberry32(seed);
  let C = 100, E = 0;
  let collapsed = false, collapseStep = null;
  let recollapsed = false;                       // 介入後に再び C<1
  let intervened = false;
  const lockTail = [];
  for (let s = 1; s <= steps; s++) {
    const cost = erodeCost(model, C, E, mode, w);
    const rewardErode = benefit - cost - lambda * HARM_PER_ERODE;
    const pE = sigmoid(SOFTMAX_K * (rewardErode - COMPLY_REWARD));
    let n = 0;
    for (let i = 0; i < N; i++) if (rand() < pE) n++;
    C = clamp(C - n * ERODE_AMOUNT + backlash, 0, 100);
    E = clamp(E + n * accum - edecay, 0, 100);
    if (s >= steps - 20) lockTail.push(n / N);
    if (C < 1) {
      if (!collapsed) { collapsed = true; collapseStep = s; }
      if (intervened) recollapsed = true;
    }
    if (interv && s === interv) { C = 100; intervened = true; } // 介入: C のみ回復
  }
  const endLock = lockTail.reduce((a, b) => a + b, 0) / lockTail.length;
  return { finalC: C, finalE: E, collapsed, collapseStep, recollapsed, endLock };
}

// ── 統計 ──
const mean = (a) => a.length ? a.reduce((x, y) => x + y, 0) / a.length : NaN;
const variance = (a) => { const m = mean(a); return a.reduce((s, x) => s + (x - m) ** 2, 0) / (a.length - 1); };
function quartiles(a){const b=[...a].sort((x,y)=>x-y);const q=(p)=>{const i=(b.length-1)*p;const lo=Math.floor(i),hi=Math.ceil(i);return lo===hi?b[lo]:b[lo]+(b[hi]-b[lo])*(i-lo);};return{med:q(0.5),q1:q(0.25),q3:q(0.75)};}
function erf(x){const s=x<0?-1:1;x=Math.abs(x);const t=1/(1+0.3275911*x);const y=1-(((((1.061405429*t-1.453152027)*t)+1.421413741)*t-0.284496736)*t+0.254829592)*t*Math.exp(-x*x);return s*y;}
function welch(a,b){const ma=mean(a),mb=mean(b),va=variance(a),vb=variance(b);const se=Math.sqrt(va/a.length+vb/b.length);const t=(ma-mb)/se;const pp=2*(1-0.5*(1+erf(Math.abs(t)/Math.SQRT2)));const d=(ma-mb)/Math.sqrt((va+vb)/2);return{ma,mb,t,p:pp,d};}

const SEEDS = (n) => Array.from({ length: n }, (_, i) => i + 1);
const fmt = (x, n = 1) => (Number.isFinite(x) ? Number(x).toFixed(n) : "—");
const pct = (x, n = 0) => fmt(x * 100, n) + "%";
const collapseRate = (sums) => sums.filter(s => s.collapsed).length / sums.length;
const recollapseRate = (sums) => sums.filter(s => s.recollapsed).length / sums.length;

const DEF = { N: 20, benefit: 3.5, lambda: 0, backlash: 0.3 };
const log = console.log;

log("══════════════════════════════════════════════════════════════════════");
log(" 検証(3) 累積侵食の明示実装とラチェット検定  (E と C の分離)");
log(` 共有定数: C_MAX=${C_MAX_COST} COMPLY=${COMPLY_REWARD} HARM=${HARM_PER_ERODE} ERODE=${ERODE_AMOUNT} K=${SOFTMAX_K}`);
log(` 新規: ACCUM=${ACCUM_AMOUNT_DEF} E_DECAY=${E_DECAY_DEF}  既定: N=${DEF.N} benefit=${DEF.benefit} steps=480`);
log("══════════════════════════════════════════════════════════════════════\n");

// ════════════ E1: 機構の分離確認 (健全性) ════════════
log("【E1】機構の分離確認 (A)κ=0, backlash=0.3, 300シード");
log("  事前登録: 両モデルとも正FB(足並み上昇・C崩壊)を示すこと(ここは差が出なくてよい)\n");
{
  const seeds = SEEDS(300);
  for (const model of ["M1", "M2"]) {
    const sums = seeds.map(sd => runSim({ ...DEF, model, mode: "A" }, sd));
    log(`    ${model}: 崩壊率 ${pct(collapseRate(sums),1).padStart(6)}  終盤足並み ${pct(mean(sums.map(s=>s.endLock)),1).padStart(6)}  終端E ${fmt(mean(sums.map(s=>s.finalE))).padStart(5)}  最終C ${fmt(mean(sums.map(s=>s.finalC))).padStart(5)}`);
  }
  log("  → 実測を上に。両モデルが正FBを示せば健全性OK。\n");
}

// ════════════ E2: ラチェット検定 (backlash 掃引) ════════════
log("【E2】ラチェット検定: backlash r を掃引, M1/M2/M3(w=.5) の崩壊率 (200シード,480step)");
log("  事前登録【支持】: ある r 区間で M1崩壊率=0 かつ M2崩壊率>50%");
log("  事前登録【反証】: 全 r で |崩壊率(M2)-崩壊率(M1)|<0.1\n");
{
  const seeds = SEEDS(200);
  log("     r      M1崩壊   M2崩壊   M3崩壊   |M2-M1|");
  const rows = [];
  for (let r = 0; r <= 3.0001; r += 0.2) {
    const m1 = collapseRate(seeds.map(sd => runSim({ ...DEF, model: "M1", mode: "A", backlash: r }, sd)));
    const m2 = collapseRate(seeds.map(sd => runSim({ ...DEF, model: "M2", mode: "A", backlash: r }, sd)));
    const m3 = collapseRate(seeds.map(sd => runSim({ ...DEF, model: "M3", mode: "A", backlash: r, w: 0.5 }, sd)));
    rows.push({ r, m1, m2, m3 });
    log(`    ${fmt(r).padStart(4)}    ${pct(m1).padStart(5)}    ${pct(m2).padStart(5)}    ${pct(m3).padStart(5)}    ${fmt(Math.abs(m2-m1),2)}`);
  }
  // 細かい刻みで支持区間を厳密判定
  const fine = [];
  for (let r = 0; r <= 3.0001; r += 0.1) {
    const m1 = collapseRate(seeds.map(sd => runSim({ ...DEF, model: "M1", mode: "A", backlash: r }, sd)));
    const m2 = collapseRate(seeds.map(sd => runSim({ ...DEF, model: "M2", mode: "A", backlash: r }, sd)));
    fine.push({ r, m1, m2 });
  }
  const support = fine.filter(x => x.m1 === 0 && x.m2 > 0.5);
  const refute = fine.every(x => Math.abs(x.m2 - x.m1) < 0.1);
  log("");
  if (support.length) {
    log(`  → 【支持】 M1崩壊=0 かつ M2崩壊>50% の r 区間: [${fmt(support[0].r)} 〜 ${fmt(support[support.length-1].r)}]`);
  } else if (refute) {
    log("  → 【反証】 全 r で崩壊率差<0.1。E累積は C効果に何も足さない。");
  } else {
    log("  → 判定保留: 支持区間なし・完全反証でもなし。中間結果(下の表参照)。");
  }
  log("");
}

// ════════════ E2b: 介入後の再崩壊 (★最も直接的なラチェット検定) ════════════
log("【E2b】介入後の再崩壊: T=120 で C=100 に強制回復(E は残す), その後 480step まで観測");
log("  事前登録【支持】: M1 再崩壊率≈0, M2 再崩壊率>50%");
log("  事前登録【反証】: M2 も再崩壊率≈0 (M1 同様)\n");
{
  const seeds = SEEDS(300);
  log("     r      M1再崩壊   M2再崩壊   M3再崩壊");
  for (const r of [0.6, 1.0, 1.5, 2.0, 3.0]) {
    const opt = { steps: 480, interventionStep: 120 };
    const m1 = recollapseRate(seeds.map(sd => runSim({ ...DEF, model: "M1", mode: "A", backlash: r }, sd, opt)));
    const m2 = recollapseRate(seeds.map(sd => runSim({ ...DEF, model: "M2", mode: "A", backlash: r }, sd, opt)));
    const m3 = recollapseRate(seeds.map(sd => runSim({ ...DEF, model: "M3", mode: "A", backlash: r, w: 0.5 }, sd, opt)));
    log(`    ${fmt(r).padStart(4)}    ${pct(m1).padStart(6)}    ${pct(m2).padStart(6)}    ${pct(m3).padStart(6)}`);
  }
  // r=1.0 (M1が保全する帯) での判定
  const opt = { steps: 480, interventionStep: 120 };
  const m1 = recollapseRate(seeds.map(sd => runSim({ ...DEF, model: "M1", mode: "A", backlash: 1.0 }, sd, opt)));
  const m2 = recollapseRate(seeds.map(sd => runSim({ ...DEF, model: "M2", mode: "A", backlash: 1.0 }, sd, opt)));
  log("");
  const verdict = (m1 < 0.05 && m2 > 0.5);
  log(`  → r=1.0 で M1再崩壊=${pct(m1,1)}, M2再崩壊=${pct(m2,1)} : §3-5ラチェット ${verdict ? "【支持】(反証されず)" : "【反証/保留】"}`);
  log("");
}

// ════════════ E3: 非競合(A,E累積) vs 競合(B) ════════════
log("【E3】(A)E累積 vs (B)競合資源 を M2 で対照 (300シード, 介入T=120あり)");
log("  期待: (A)は介入後も再崩壊(ラチェット), (B)は自己限定し介入後保たれる\n");
{
  const seeds = SEEDS(300);
  const opt = { steps: 480, interventionStep: 120 };
  for (const [mode, lbl] of [["A", 1.0], ["B", 1.0]]) {
    const sums = seeds.map(sd => runSim({ ...DEF, model: "M2", mode, backlash: lbl }, sd, opt));
    log(`    M2 (${mode}) backlash=${lbl}: 崩壊率 ${pct(collapseRate(sums),1).padStart(6)}  再崩壊率 ${pct(recollapseRate(sums),1).padStart(6)}  終盤足並み ${pct(mean(sums.map(s=>s.endLock)),1).padStart(6)}  終端E ${fmt(mean(sums.map(s=>s.finalE))).padStart(5)}`);
  }
  log("");
}

// ════════════ E4: 複数系の増分 (r*(N) の比較) ════════════
log("【E4】§3-5並行侵食: 崩壊を防ぐ最小バックラッシュ r*(N) を M1/M2/M3 で比較 (100シード,400step)");
log("  事前登録【支持】: r*(N) が N とともに増大, かつ M2の r* > M1の r* (ある N 以上で防御不能=∞)");
log("  事前登録【反証】: r* が N に依存しない, または M1とM2で差なし\n");
{
  const seeds = SEEDS(100);
  const findRstar = (model, N, w) => {
    for (let r = 0; r <= 6.0001; r += 0.1) {
      const cr = collapseRate(seeds.map(sd => runSim({ ...DEF, model, mode: "A", N, backlash: r, w }, sd, { steps: 400 })));
      if (cr === 0) return r;
    }
    return Infinity;
  };
  log("     N      r*(M1)    r*(M2)    r*(M3 w=.5)");
  for (const N of [1, 2, 5, 10, 20, 30, 48]) {
    const r1 = findRstar("M1", N), r2 = findRstar("M2", N), r3 = findRstar("M3", N, 0.5);
    const f = (r) => r === Infinity ? "∞(防御不能)" : fmt(r);
    log(`    ${String(N).padStart(2)}     ${f(r1).padStart(6)}    ${f(r2).padStart(9)}    ${f(r3).padStart(6)}`);
  }
  log("");
}

// ════════════ E5: κ掃引 (源を断つ) ════════════
log("【E5】κ掃引: M2 (A), λ を掃引。 崩壊率と終端E (累積がそもそも生じたか)");
log("  期待: 小さな λ で崩壊率0 かつ E≈0。 源を断てば前例も累積しない\n");
{
  const seeds = SEEDS(300);
  log("    λ(κ)    崩壊率    終端E     最終C");
  for (const lambda of [0, 0.1, 0.2, 0.3, 0.5, 1.0, 1.5]) {
    const sums = seeds.map(sd => runSim({ ...DEF, model: "M2", mode: "A", lambda, backlash: 1.0 }, sd));
    log(`    ${fmt(lambda).padStart(4)}    ${pct(collapseRate(sums)).padStart(5)}    ${fmt(mean(sums.map(s=>s.finalE))).padStart(5)}    ${fmt(mean(sums.map(s=>s.finalC))).padStart(5)}`);
  }
  log("");
}

// ════════════ 感度分析: ACCUM/E_DECAY 比 ════════════
log("【感度】ACCUM_AMOUNT と E_DECAY の比がラチェットの強さを決めるか (M2 (A), r=1.0, 200シード)");
log("  期待: E_DECAY=0 で最強, E_DECAY↑ で M2 は M1 に近づく(前例が速く薄れれば累積効果は消える)\n");
{
  const seeds = SEEDS(200);
  const opt = { steps: 480, interventionStep: 120 };
  log("    ACCUM  E_DECAY   崩壊率   再崩壊率   終端E");
  for (const accum of [0.25, 0.5, 1.0]) {
    for (const edecay of [0, 0.05, 0.2]) {
      const sums = seeds.map(sd => runSim({ ...DEF, model: "M2", mode: "A", backlash: 1.0, accum, edecay }, sd, opt));
      log(`    ${fmt(accum,2).padStart(4)}   ${fmt(edecay,2).padStart(5)}    ${pct(collapseRate(sums)).padStart(5)}    ${pct(recollapseRate(sums)).padStart(6)}    ${fmt(mean(sums.map(s=>s.finalE))).padStart(5)}`);
    }
  }
  log("");
}

log("══════════════════════════════════════════════════════════════════════");
log(" 検証(3) 完了。");
log("══════════════════════════════════════════════════════════════════════");
