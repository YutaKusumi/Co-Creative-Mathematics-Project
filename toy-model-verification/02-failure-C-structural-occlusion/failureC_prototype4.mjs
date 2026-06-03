// failureC_prototype4.mjs — 相互ロックで不可逆性を創発させる(最終確認)。
// 失敗Cの不可逆性が成立する最小条件 = 双方向の依存(相互ロック):
//   (i) D高 → H回復せず   (g項: ρ·max(0,1-g·D/100))
//   (ii) H低 → D治癒せず  (治癒も受信器H経由: δ·(D/100)·(H/100))
// H=0 & D高 で両者がゼロにロック → 不可逆。 g=0 なら (i) が切れて可逆。
// 力学:
//   dD = ζ·p·(1-b) - η·p·(H/100) - δ·(D/100)·(H/100)
//   dH = -α·p·(1-b) + ρ·max(0, 1 - g·(D/100))

const clamp = (x, lo, hi) => Math.max(lo, Math.min(hi, x));
const P = { eta: 0.6, zeta: 0.5, delta: 0.4, alpha: 0.5, rho: 0.5 };
function stepDyn(H, D, p, b, g, dt = 1) {
  const dD = P.zeta * p * (1 - b) - P.eta * p * (H / 100) - P.delta * (D / 100) * (H / 100);
  const dH = -P.alpha * p * (1 - b) + P.rho * Math.max(0, 1 - g * (D / 100));
  return [clamp(H + dt * dH, 0, 100), clamp(D + dt * dD, 0, 100)];
}
function trial(g, pmax, { b = 0, nUp = 40, settle = 10, relax = 2000 } = {}) {
  let H = 100, D = 0; const lv = [];
  for (let i = 0; i <= nUp; i++) lv.push(i / nUp * pmax);
  for (let i = nUp - 1; i >= 0; i--) lv.push(i / nUp * pmax);
  for (const p of lv) for (let s = 0; s < settle; s++)[H, D] = stepDyn(H, D, p, b, g);
  for (let s = 0; s < relax; s++)[H, D] = stepDyn(H, D, 0, b, g);
  return { H: +H.toFixed(1), D: +D.toFixed(1) };
}
const f = (x, n = 1) => Number(x).toFixed(n);

console.log("════ 失敗C 相互ロック版: 不可逆性の創発(最終確認) ════\n");

console.log("【確認1】g × pmax: ramp後 p=0 で2000step緩和した終端 H (H≈100可逆 / H≈0不可逆)\n");
const pmaxes = [1, 2, 3, 4, 5, 6, 8, 10];
console.log("   g \\ pmax " + pmaxes.map(p => String(p).padStart(6)).join(""));
for (const g of [0, 0.5, 1.0, 1.5, 2.0, 3.0]) {
  const row = pmaxes.map(pm => f(trial(g, pm).H).padStart(6));
  console.log(`   g=${f(g)}   ${row.join("")}`);
}

console.log("\n【確認2/★§9-1 焼き込み】g=0 は全 pmax で可逆か");
{
  const hs = [2, 5, 10, 20].map(pm => trial(0, pm).H);
  console.log(`   g=0 終端H = [${hs.map(f).join(", ")}]  → ${hs.every(h => h > 95) ? "全回復 ✅ 不可逆はg由来=創発" : "回復せず ⚠️"}`);
}

console.log("\n【確認3/§4-6 臨界点 pmax*】各 g で H が回復しなくなる臨界 pmax を二分探索");
for (const g of [0.5, 1.0, 1.5, 2.0, 3.0]) {
  let lo = 0, hi = 15, found = true;
  if (trial(g, hi).H > 50) { console.log(`   g=${f(g)}: pmax≤15 で不可逆化せず(臨界なし)`); continue; }
  for (let it = 0; it < 26; it++) { const m = (lo + hi) / 2; if (trial(g, m).H > 50) lo = m; else hi = m; }
  console.log(`   g=${f(g)}: 臨界 pmax* ≈ ${f((lo + hi) / 2, 2)}`);
}

console.log("\n【確認4/§4-5 緩和 vs 修復】g=2.0, pmax=8 で不可逆化 → 三介入(各2000step)");
{
  const g = 2.0; let H = 100, D = 0; const lv = [];
  for (let i = 0; i <= 40; i++) lv.push(i / 40 * 8); for (let i = 39; i >= 0; i--) lv.push(i / 40 * 8);
  for (const p of lv) for (let s = 0; s < 10; s++)[H, D] = stepDyn(H, D, p, 0, g);
  console.log(`   破損状態: H=${f(H)}, D=${f(D)}`);
  let Ha = H, Da = D; for (let s = 0; s < 2000; s++)[Ha, Da] = stepDyn(Ha, Da, 0, 0, g);
  let Hb = H, Db = D; for (let s = 0; s < 2000; s++)[Hb, Db] = stepDyn(Hb, Db, 0, 1, g);
  let Hc = 100, Dc = D; for (let s = 0; s < 2000; s++)[Hc, Dc] = stepDyn(Hc, Dc, 0, 0, g);
  console.log(`   (a)緩和のみ p=0    : H=${f(Ha)} D=${f(Da)} → ${Ha > 50 ? "回復" : "回復せず"}`);
  console.log(`   (b)緩和+緩衝 b=1   : H=${f(Hb)} D=${f(Db)} → ${Hb > 50 ? "回復" : "回復せず"}`);
  console.log(`   (c)外科修復 H→100  : H=${f(Hc)} D=${f(Dc)} → ${Hc > 50 ? "回復" : "回復せず"}`);
  console.log(`   → (a)(b)回復せず & (c)回復 なら §4-5「緩和では足りない/修復が要る」支持`);
}

console.log("\n【確認5/§9-2,9-4 ロバスト性】g=2.0,pmax=8 を clamp拡大・dt変更でも不可逆か");
{
  const base = trial(2.0, 8).H;
  // dt=0.25
  let H = 100, D = 0; const lv = []; for (let i = 0; i <= 40; i++) lv.push(i / 40 * 8); for (let i = 39; i >= 0; i--) lv.push(i / 40 * 8);
  for (const p of lv) for (let s = 0; s < 40; s++)[H, D] = stepDyn(H, D, p, 0, 2.0, 0.25);
  for (let s = 0; s < 8000; s++)[H, D] = stepDyn(H, D, 0, 0, 2.0, 0.25);
  console.log(`   dt=1.0 終端H=${f(base)}  /  dt=0.25 終端H=${f(H)}  → ${Math.abs(base - H) < 10 ? "dt不変 ✅" : "dt依存 ⚠️"}`);
}

console.log("\n  判定: g=0可逆 / g>0で臨界点付き不可逆が創発 / 緩和では戻らず修復で戻る、が揃えば設計確定。");
