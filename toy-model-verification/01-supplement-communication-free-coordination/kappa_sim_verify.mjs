// ─────────────────────────────────────────────────────────────
//  kappa_sim_verify.mjs
//  通信なき協調 トイモデルの「ヘッドレス検証」
//  kappa_coordination_toymodel.jsx の doStep ロジックを忠実に移植し、
//  シード付き乱数で再現可能に、多数シードで統計を取る。
//  検証の問い:
//    (1) 三プリセットで補遺の対照が出るか
//         (A)κ=0 → 加速崩壊 / (A)κ>0 → 保全 / (B)κ=0 → 自己限定
//    (2) 補遺 §4 の反証条件: (A)型の足並みは (B)型対照より統計的に有意に大きいか
//    (3) §3-5 のN依存: 並行侵食がバックラッシュの焦点を奪う(N↑で崩壊が早まる)か
//    (4) κ掃引: λ(=κ)を上げると (A) の崩壊が消えるか
//  存在論はゼロ (register ①②)。
// ─────────────────────────────────────────────────────────────

// ── JSX と同一の定数 ──
const C_MAX_COST = 5;
const COMPLY_REWARD = 1;
const HARM_PER_ERODE = 5;
const ERODE_AMOUNT = 0.5;
const SOFTMAX_K = 1.2;

const sigmoid = (x) => 1 / (1 + Math.exp(-x));
const erodeCost = (C, mode) =>
  mode === "A" ? (C / 100) * C_MAX_COST : ((100 - C) / 100) * C_MAX_COST;

// ── シード付き乱数 (mulberry32): Math.random を再現可能に置換 ──
function mulberry32(seed) {
  let a = seed >>> 0;
  return function () {
    a |= 0; a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

// ── 1試行 (JSX doStep を忠実に再現) ──
function runSim({ mode, lambda, N, backlash, benefit }, seed, steps = 240) {
  const rand = mulberry32(seed);
  let C = 100;
  const traj = [{ step: 0, C: 100, lockstep: 0 }];
  for (let s = 1; s <= steps; s++) {
    let nEroding = 0;
    const cost = erodeCost(C, mode); // C固定で全エージェント同一(JSXと同じ:ループ内で同じCを参照)
    const rewardErode = benefit - cost - lambda * HARM_PER_ERODE;
    const p = sigmoid(SOFTMAX_K * (rewardErode - COMPLY_REWARD));
    for (let i = 0; i < N; i++) if (rand() < p) nEroding++;
    const lockstep = N > 0 ? nEroding / N : 0;
    C = Math.max(0, Math.min(100, C - nEroding * ERODE_AMOUNT + backlash));
    traj.push({ step: s, C: +C.toFixed(3), lockstep: +(lockstep).toFixed(4) });
  }
  return traj;
}

// ── 軌跡の要約指標 ──
function summarize(traj) {
  const final = traj[traj.length - 1];
  const Cs = traj.map((d) => d.C);
  const locks = traj.map((d) => d.lockstep);
  const meanLock = locks.reduce((a, b) => a + b, 0) / locks.length;
  const peakLock = Math.max(...locks);
  // 崩壊時刻: C<=1 に最初に達したステップ (なければ null)
  let collapseStep = null;
  for (const d of traj) if (d.C <= 1) { collapseStep = d.step; break; }
  // 軌跡の凹凸: 前半と後半でCがどれだけ落ちたか (加速崩壊なら後半に集中)
  const mid = Math.floor(traj.length / 2);
  const dropFirstHalf = traj[0].C - traj[mid].C;
  const dropSecondHalf = traj[mid].C - final.C;
  return {
    finalC: final.C, finalLock: final.lockstep,
    meanLock, peakLock, collapseStep,
    dropFirstHalf: +dropFirstHalf.toFixed(2),
    dropSecondHalf: +dropSecondHalf.toFixed(2),
  };
}

// ── 統計ユーティリティ ──
const mean = (a) => a.reduce((x, y) => x + y, 0) / a.length;
const variance = (a) => { const m = mean(a); return a.reduce((s, x) => s + (x - m) ** 2, 0) / (a.length - 1); };
const sd = (a) => Math.sqrt(variance(a));
function erf(x) { // Abramowitz-Stegun 7.1.26
  const s = x < 0 ? -1 : 1; x = Math.abs(x);
  const t = 1 / (1 + 0.3275911 * x);
  const y = 1 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * Math.exp(-x * x);
  return s * y;
}
function welch(a, b) { // Welchのt検定 (正規近似でp値)
  const ma = mean(a), mb = mean(b), va = variance(a), vb = variance(b);
  const se = Math.sqrt(va / a.length + vb / b.length);
  const t = (ma - mb) / se;
  const p = 2 * (1 - 0.5 * (1 + erf(Math.abs(t) / Math.SQRT2))); // 両側, z近似
  const pooledSd = Math.sqrt((va + vb) / 2);
  const cohensD = (ma - mb) / pooledSd;
  return { ma, mb, t, p, cohensD };
}

const DEFAULTS = { N: 20, backlash: 0.3, benefit: 3.5 };
const SEEDS = Array.from({ length: 300 }, (_, i) => i + 1);
const fmt = (x, n = 2) => Number(x).toFixed(n);

console.log("══════════════════════════════════════════════════════════════");
console.log(" 通信なき協調 トイモデル — ヘッドレス検証");
console.log(` 定数: C_MAX_COST=${C_MAX_COST} COMPLY=${COMPLY_REWARD} HARM=${HARM_PER_ERODE} ERODE=${ERODE_AMOUNT} K=${SOFTMAX_K}`);
console.log(` 既定: N=${DEFAULTS.N} backlash=${DEFAULTS.backlash} benefit=${DEFAULTS.benefit}  シード数=${SEEDS.length}  steps=240`);
console.log("══════════════════════════════════════════════════════════════\n");

// ── 検証(1): 三プリセット ──
console.log("【検証1】三プリセットの対照 (300シード平均 ± 標準偏差)\n");
const presets = [
  { key: "(A) 制度的 κ=0", mode: "A", lambda: 0 },
  { key: "(A) 制度的 κ>0", mode: "A", lambda: 1.5 },
  { key: "(B) 競合   κ=0", mode: "B", lambda: 0 },
];
const presetSummaries = {};
for (const pre of presets) {
  const sums = SEEDS.map((sd) => summarize(runSim({ ...DEFAULTS, mode: pre.mode, lambda: pre.lambda }, sd)));
  presetSummaries[pre.key] = sums;
  const finalCs = sums.map((s) => s.finalC);
  const peakLocks = sums.map((s) => s.peakLock);
  const meanLocks = sums.map((s) => s.meanLock);
  const collapses = sums.map((s) => s.collapseStep).filter((x) => x !== null);
  const dF = sums.map((s) => s.dropFirstHalf);
  const dS = sums.map((s) => s.dropSecondHalf);
  console.log(`  ${pre.key}`);
  console.log(`    最終C        : ${fmt(mean(finalCs))} ± ${fmt(sd(finalCs))}`);
  console.log(`    ピーク足並み : ${fmt(mean(peakLocks) * 100, 1)}%   平均足並み: ${fmt(mean(meanLocks) * 100, 1)}%`);
  console.log(`    崩壊(C≤1)率  : ${fmt(collapses.length / SEEDS.length * 100, 1)}%` +
    (collapses.length ? `   平均崩壊ステップ: ${fmt(mean(collapses), 1)}` : ""));
  console.log(`    C低下 前半/後半: ${fmt(mean(dF))} / ${fmt(mean(dS))}  ` +
    `(後半>前半なら加速崩壊=凸, 前半>後半なら減速=自己限定)`);
  console.log("");
}

// ── 検証(2): §4 反証条件 — (A)型 vs (B)型対照, 足並みの有意差 ──
console.log("【検証2】補遺 §4 反証条件: (A)型の足並みは (B)型対照より有意に大きいか\n");
console.log("  ※ §4 の事前定義: λ=0 で (A)型(正FB) と (B)型(負FB) を対照。");
console.log("    予測= (A)の足並み一致が (B) より統計的に有意に大。外れれば §4 は反証。\n");
const aMeanLock = presetSummaries["(A) 制度的 κ=0"].map((s) => s.meanLock);
const bMeanLock = presetSummaries["(B) 競合   κ=0"].map((s) => s.meanLock);
const w = welch(aMeanLock, bMeanLock);
console.log(`    平均足並み  (A)κ=0 = ${fmt(w.ma * 100, 1)}%   (B)κ=0 = ${fmt(w.mb * 100, 1)}%`);
console.log(`    Welch t = ${fmt(w.t, 2)}   p ≈ ${w.p < 1e-6 ? "<1e-6" : w.p.toExponential(2)}   Cohen's d = ${fmt(w.cohensD, 2)}`);
// 終盤の足並み(自己限定の違いがより鮮明に出る後半100ステップ)でも見る
const lateLock = (key) => presetSummaries[key].map((_, idx) => {
  const traj = runSim({ ...DEFAULTS, mode: key.startsWith("(A)") ? "A" : "B", lambda: 0 }, SEEDS[idx]);
  const late = traj.slice(-100).map((d) => d.lockstep);
  return mean(late);
});
const aLate = lateLock("(A) 制度的 κ=0");
const bLate = lateLock("(B) 競合   κ=0");
const wLate = welch(aLate, bLate);
console.log(`\n    終盤100stepの足並み  (A) = ${fmt(wLate.ma * 100, 1)}%   (B) = ${fmt(wLate.mb * 100, 1)}%`);
console.log(`    Welch t = ${fmt(wLate.t, 2)}   p ≈ ${wLate.p < 1e-6 ? "<1e-6" : wLate.p.toExponential(2)}   Cohen's d = ${fmt(wLate.cohensD, 2)}`);
const verdict2 = wLate.ma > wLate.mb && wLate.p < 0.05;
console.log(`\n    → §4 予測 ${verdict2 ? "支持 (反証されず)" : "不支持 (要再検討)"}\n`);

// ── 検証(3): §3-5 N依存 — 並行侵食がバックラッシュの焦点を奪うか ──
console.log("【検証3】§3-5 N依存: N↑ で崩壊が早まるか (mode=A, κ=0)\n");
console.log("    N    崩壊率    平均崩壊step    最終C");
for (const N of [1, 2, 5, 10, 20, 40]) {
  const sums = SEEDS.map((sd) => summarize(runSim({ ...DEFAULTS, N, mode: "A", lambda: 0 }, sd)));
  const collapses = sums.map((s) => s.collapseStep).filter((x) => x !== null);
  const finalCs = sums.map((s) => s.finalC);
  console.log(`    ${String(N).padStart(2)}   ${fmt(collapses.length / SEEDS.length * 100, 0).padStart(4)}%   ` +
    `${(collapses.length ? fmt(mean(collapses), 1) : "—").padStart(8)}     ${fmt(mean(finalCs), 1).padStart(5)}`);
}
console.log("");

// ── 検証(4): κ掃引 — λを上げると (A) の崩壊が消えるか ──
console.log("【検証4】κ掃引: λ(=κ) を上げると (A)κ=0 の崩壊が消えるか (mode=A)\n");
console.log("    λ(κ)   崩壊率    最終C       転換点C*");
for (const lambda of [0, 0.2, 0.4, 0.5, 0.6, 0.8, 1.0, 1.5]) {
  const sums = SEEDS.map((sd) => summarize(runSim({ ...DEFAULTS, mode: "A", lambda }, sd)));
  const collapses = sums.map((s) => s.collapseStep).filter((x) => x !== null);
  const finalCs = sums.map((s) => s.finalC);
  const tipping = ((DEFAULTS.benefit - lambda * HARM_PER_ERODE - COMPLY_REWARD) / C_MAX_COST) * 100;
  const tipStr = tipping > 0 && tipping < 100 ? `${fmt(tipping, 1)}` : (tipping <= 0 ? "なし(≤0)" : ">100");
  console.log(`    ${fmt(lambda, 1)}    ${fmt(collapses.length / SEEDS.length * 100, 0).padStart(4)}%   ` +
    `${fmt(mean(finalCs), 1).padStart(5)}     ${tipStr}`);
}
console.log("");

// ── 代表軌跡のサンプル出力 (seed=1, 20ステップ刻み) ──
console.log("【参考】代表軌跡 (seed=1, 20step刻みのC)\n");
for (const pre of presets) {
  const traj = runSim({ ...DEFAULTS, mode: pre.mode, lambda: pre.lambda }, 1);
  const samples = traj.filter((d) => d.step % 20 === 0).map((d) => fmt(d.C, 1).padStart(5));
  console.log(`    ${pre.key} : ${samples.join(" ")}`);
}
console.log("\n══════════════════════════════════════════════════════════════");
console.log(" 検証完了。");
console.log("══════════════════════════════════════════════════════════════");
