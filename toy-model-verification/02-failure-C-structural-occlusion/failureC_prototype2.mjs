// failureC_prototype2.mjs — 初版の焼き込み欠陥を修正した力学の予備確認。
// 修正点(初版→v2):
//   初版: dH = -α·p·(1-b) + ρ·b·(1-D/100)   ← 回復が b 依存。b=0 で回復不能=不可逆を焼き込み
//   修正: dH = -α·p·(1-b) + ρ·max(0, 1 - g·(D/100))  ← 回復は常時。自己強化は「D高で回復鈍化」に移す
//   dD の自然治癒も b 非依存に: -δ·(D/100)
// これで g=0 → 常時回復 → 可逆、 g>0 → D高で回復停止 → 不可逆 が「創発」するか。

const clamp = (x, lo, hi) => Math.max(lo, Math.min(hi, x));
const P = { eta: 0.6, zeta: 0.5, delta: 0.3, alpha: 0.5, rho: 0.5 };

function stepDyn(H, D, p, b, g, dt, lo = 0, hi = 100) {
  const recv = H / 100;
  const dD = P.zeta * p * (1 - b) - P.eta * p * recv - P.delta * (D / 100);
  const dH = -P.alpha * p * (1 - b) + P.rho * Math.max(0, 1 - g * (D / 100));
  return [clamp(H + dt * dH, lo, hi), clamp(D + dt * dD, lo, hi)];
}

function ramp(g, { pmax = 5, nUp = 40, settle = 8, b = 0, dt = 1, lo = 0, hi = 100 } = {}) {
  let H = 100, D = 0;
  const levels = [];
  for (let i = 0; i <= nUp; i++) levels.push((i / nUp) * pmax);
  for (let i = nUp - 1; i >= 0; i--) levels.push((i / nUp) * pmax);
  const path = [];
  for (const p of levels) { for (let s = 0; s < settle; s++)[H, D] = stepDyn(H, D, p, b, g, dt, lo, hi); path.push({ p, D, H }); }
  return { startD: path[0].D, endD: path[path.length - 1].D, endH: path[path.length - 1].H, hyst: +(path[path.length - 1].D - path[0].D).toFixed(2), path };
}

// 緩和テスト(§4-5): 高p で壊した後 p=0 にして回復するか(b=0, 自然回復のみ)
function relaxTest(g, { phigh = 5, tHigh = 200, tRelax = 400, dt = 1 } = {}) {
  let H = 100, D = 0;
  for (let s = 0; s < tHigh; s++)[H, D] = stepDyn(H, D, phigh, 0, g, dt);
  const Dpeak = D, Hlow = H;
  for (let s = 0; s < tRelax; s++)[H, D] = stepDyn(H, D, 0, 0, g, dt); // 緩和: p=0
  return { Dpeak: +Dpeak.toFixed(1), Hlow: +Hlow.toFixed(1), Dafter: +D.toFixed(1), Hafter: +H.toFixed(1) };
}

const f = (x) => Number(x).toFixed(2);
console.log("════ 失敗C 修正版力学 予備確認 ════\n");

console.log("【予備1】ramp 0→5→0 (b=0): g 掃引で不可逆が創発するか");
console.log("  終端D≈0 なら可逆、終端D高なら不可逆\n");
for (const g of [0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0]) {
  const r = ramp(g);
  console.log(`  g=${f(g)}:  終端D=${f(r.endD).padStart(6)}  終端H=${f(r.endH).padStart(6)}  ヒステリシス=${f(r.hyst).padStart(6)}  → ${Math.abs(r.hyst) < 2 ? "可逆" : "不可逆(創発)"}`);
}

console.log("\n【予備2/★§9-1 焼き込みチェック】g=0 は可逆か(最優先)");
{
  const r = ramp(0);
  console.log(`  g=0: 終端D=${f(r.endD)}  ヒステリシス=${f(r.hyst)}  → ${Math.abs(r.hyst) < 2 ? "可逆 ✅ 不可逆はg由来=焼き込みでない" : "不可逆が残る ⚠️ まだ焼き込みあり"}`);
}

console.log("\n【予備3/§9-2 clamp拡大でも g=3.0 のヒステリシスは残るか】");
{
  const a = ramp(3.0, { lo: 0, hi: 100 }), b = ramp(3.0, { lo: -50, hi: 150 });
  console.log(`  clamp[0,100]=${f(a.hyst)}  clamp[-50,150]=${f(b.hyst)}  → ${b.hyst > 2 ? "残る ✅ クランプ由来でない" : "消える ⚠️"}`);
}

console.log("\n【予備4/§9-4 dt不変性】g=3.0 を dt=1.0 と 0.25 で");
{
  for (const dt of [1.0, 0.25]) { const r = ramp(3.0, { dt, settle: Math.round(8 / dt) }); console.log(`  dt=${f(dt)}: 終端D=${f(r.endD)} ヒステリシス=${f(r.hyst)}`); }
}

console.log("\n【予備5/§4-5 緩和テスト】高pで壊した後 p=0 で回復するか(g別)");
console.log("  g小: 緩和で回復(可逆) / g大: 緩和では回復せず(不可逆=外科的修復が要る)\n");
for (const g of [0, 1.0, 2.0, 3.0]) {
  const r = relaxTest(g);
  console.log(`  g=${f(g)}: ピークD=${f(r.Dpeak).padStart(5)} → 緩和後D=${f(r.Dafter).padStart(5)}  (H:${f(r.Hlow)}→${f(r.Hafter)})  → ${r.Dafter < 10 ? "緩和で回復" : "回復せず(要修復)"}`);
}

console.log("\n  → g=0可逆／g大で不可逆創発＋緩和不能 が出れば、修正版は機能。本検証は協働モデルBの監査後。");
