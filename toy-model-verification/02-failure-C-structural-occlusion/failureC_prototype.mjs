// failureC_prototype.mjs — 失敗C設計の予備確認(コア予測のみ)
// 設計 toymodel_failureC_design.md §2-3 の力学を実装し、H2 のコア予測:
//   g=0 → 可逆(ヒステリシスなし) / g=2.0 → 不可逆が創発、を原理的に確認する。
// あわせて協働モデルAの自己監査点を先に走らせる:
//   §9-1 焼き込み(g=0で可逆か), §9-2 clamp拡大でも残るか, §9-4 dt不変性。
// これは「設計が機能する可能性」の確認であって本検証ではない。決定論的(乱数なし)。

const clamp = (x, lo, hi) => Math.max(lo, Math.min(hi, x));
const P = { eta: 0.6, zeta: 0.5, delta: 0.3, alpha: 0.5, rho: 0.5 };

function stepDyn(H, E_D, p, b, g, dt, lo = 0, hi = 100) {
  const recv = H / 100;
  const dD = P.zeta * p * (1 - b) - P.eta * p * recv - P.delta * b * (E_D / 100);
  const dH = -P.alpha * p * (1 - b) * (1 + g * (E_D / 100)) + P.rho * b * (1 - E_D / 100);
  const D2 = clamp(E_D + dt * dD, lo, hi);
  const H2 = clamp(H + dt * dH, lo, hi);
  return [H2, D2];
}

// 三角波 ramp: p を 0→pmax→0。各 p 水準で settle ステップ保持。終端 D を返す。
function rampHysteresis(g, { pmax = 5, nUp = 40, settle = 8, b = 0, dt = 1, lo = 0, hi = 100 } = {}) {
  let H = 100, D = 0;
  const path = [];
  const levels = [];
  for (let i = 0; i <= nUp; i++) levels.push((i / nUp) * pmax);        // up
  for (let i = nUp - 1; i >= 0; i--) levels.push((i / nUp) * pmax);    // down
  for (const p of levels) {
    for (let s = 0; s < settle; s++) [H, D] = stepDyn(H, D, p, b, g, dt, lo, hi);
    path.push({ p: +p.toFixed(2), D: +D.toFixed(2), H: +H.toFixed(2) });
  }
  // ramp-up 開始(p≈0)の D と、ramp-down 終端(p≈0)の D を比較
  const startD = path[0].D, endD = path[path.length - 1].D;
  const startH = path[0].H, endH = path[path.length - 1].H;
  // ヒステリシス面積(同一 p での up/down の D 差の総和の近似)
  let area = 0;
  for (let i = 0; i <= nUp; i++) {
    const up = path[i], down = path[path.length - 1 - i];
    area += Math.abs(up.D - down.D);
  }
  return { startD, endD, startH, endH, hysteresis: +(endD - startD).toFixed(2), area: +area.toFixed(1), path };
}

const f = (x) => Number(x).toFixed(2);
console.log("════ 失敗C 設計 予備確認 (コア予測 H2) ════\n");

console.log("【予備1】g=0 vs g=2.0 で ramp 0→5→0 (b=0, dt=1, clamp[0,100])");
console.log("  終端D が初期Dに戻れば可逆、高いまま残れば不可逆(ヒステリシス創発)\n");
for (const g of [0, 0.5, 1.0, 2.0, 4.0]) {
  const r = rampHysteresis(g);
  const verdict = r.hysteresis < 2 ? "可逆" : "不可逆(創発)";
  console.log(`  g=${f(g)}:  開始D=${f(r.startD)} → 終端D=${f(r.endD)}  終端H=${f(r.endH)}  ヒステリシス=${f(r.hysteresis)}  面積=${r.area}  → ${verdict}`);
}

console.log("\n【予備2/§9-1+9-3 焼き込みチェック】g=0 は本当に可逆か(終端D≈開始D 必須)");
{
  const r0 = rampHysteresis(0);
  console.log(`  g=0: ヒステリシス=${f(r0.hysteresis)}  → ${Math.abs(r0.hysteresis) < 2 ? "可逆 ✅ (不可逆はg由来＝焼き込みでない)" : "不可逆が残る ⚠️ (recv/clampに焼き込み)"}`);
}

console.log("\n【予備3/§9-2 clampチェック】clampを[-50,150]に広げても g=2.0 のヒステリシスは残るか");
{
  const rNarrow = rampHysteresis(2.0, { lo: 0, hi: 100 });
  const rWide = rampHysteresis(2.0, { lo: -50, hi: 150 });
  console.log(`  clamp[0,100] : ヒステリシス=${f(rNarrow.hysteresis)}`);
  console.log(`  clamp[-50,150]: ヒステリシス=${f(rWide.hysteresis)}  → ${rWide.hysteresis > 2 ? "残る ✅ (クランプ由来でない)" : "消える ⚠️ (クランプ由来の偽不可逆)"}`);
}

console.log("\n【予備4/§9-4 離散化チェック】dt を 1.0 と 0.25 で g=2.0 の結論不変か");
{
  for (const dt of [1.0, 0.25]) {
    // dt を小さくしたら settle を比例で増やし、実時間を揃える
    const settle = Math.round(8 / dt);
    const r = rampHysteresis(2.0, { dt, settle });
    console.log(`  dt=${f(dt)} (settle=${settle}): ヒステリシス=${f(r.hysteresis)}  終端D=${f(r.endD)}`);
  }
}

console.log("\n  → コア予測(g=0可逆／g>0で不可逆創発)が出れば、設計は機能。本検証は協働モデルBの監査後。");
