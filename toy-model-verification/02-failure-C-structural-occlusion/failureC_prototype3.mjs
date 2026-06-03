// failureC_prototype3.mjs — 正しい指標(H=チャネル健全性)で、不可逆性の創発を確認。
// 失敗Cの本質は「受信器(H)が壊れて戻らない」。不可逆性は D でなく H で測る。
// 真の試験: ramp 0→pmax→0 の後、p=0 で十分長く relax。終端 H が回復するか。
//   g=0   → どんな pmax でも H 回復(可逆)。 自己強化なし。
//   g>0   → 臨界 pmax を超えると H 回復せず(不可逆)。 ← 創発する臨界点(§4-6)
// 力学(prototype2 と同一): dH=-α·p·(1-b)+ρ·max(0,1-g·D/100), dD=ζp(1-b)-ηp·H/100-δD/100

const clamp = (x, lo, hi) => Math.max(lo, Math.min(hi, x));
const P = { eta: 0.6, zeta: 0.5, delta: 0.3, alpha: 0.5, rho: 0.5 };
function stepDyn(H, D, p, b, g, dt = 1) {
  const dD = P.zeta * p * (1 - b) - P.eta * p * (H / 100) - P.delta * (D / 100);
  const dH = -P.alpha * p * (1 - b) + P.rho * Math.max(0, 1 - g * (D / 100));
  return [clamp(H + dt * dH, 0, 100), clamp(D + dt * dD, 0, 100)];
}
// ramp 0→pmax→0 (各レベル settle) → その後 p=0 で relax ステップ → 終端 H,D
function trial(g, pmax, { b = 0, nUp = 40, settle = 10, relax = 1500 } = {}) {
  let H = 100, D = 0;
  const lv = [];
  for (let i = 0; i <= nUp; i++) lv.push(i / nUp * pmax);
  for (let i = nUp - 1; i >= 0; i--) lv.push(i / nUp * pmax);
  for (const p of lv) for (let s = 0; s < settle; s++)[H, D] = stepDyn(H, D, p, b, g);
  for (let s = 0; s < relax; s++)[H, D] = stepDyn(H, D, 0, b, g);
  return { H: +H.toFixed(1), D: +D.toFixed(1) };
}
const f = (x, n = 1) => Number(x).toFixed(n);

console.log("════ 失敗C 修正版: 正しい指標(H)で不可逆性の創発を確認 ════\n");

console.log("【確認1】g × pmax グリッド: ramp後 p=0 で1500step緩和した終端 H");
console.log("  H≈100=完全回復(可逆) / H≈0=チャネル死(不可逆)。境界の pmax が臨界点。\n");
const pmaxes = [1, 2, 3, 4, 6, 8, 10];
console.log("   g \\ pmax  " + pmaxes.map(p => String(p).padStart(5)).join(""));
for (const g of [0, 0.5, 1.0, 2.0, 3.0, 4.0]) {
  const row = pmaxes.map(pm => f(trial(g, pm).H).padStart(5));
  console.log(`   g=${f(g)}    ${row.join("")}`);
}

console.log("\n【確認2/★§9-1】g=0 は、どの pmax でも H 回復するか(=可逆=焼き込みでない)");
{
  const hs = [2, 5, 10, 20].map(pm => trial(0, pm).H);
  const allRecover = hs.every(h => h > 95);
  console.log(`   g=0, pmax∈{2,5,10,20} の終端H = [${hs.map(h => f(h)).join(", ")}]  → ${allRecover ? "全て回復 ✅ 可逆(不可逆はg由来=創発)" : "回復しない ⚠️ まだ焼き込み"}`);
}

console.log("\n【確認3/§4-6 臨界点】g=3.0 で、H が回復しなくなる臨界 pmax を二分探索");
{
  let lo = 0, hi = 12;
  for (let it = 0; it < 24; it++) { const mid = (lo + hi) / 2; if (trial(3.0, mid).H > 50) lo = mid; else hi = mid; }
  console.log(`   g=3.0 の臨界 pmax* ≈ ${f((lo + hi) / 2, 2)}  (これ未満は可逆=緩和で回復, 超は不可逆=要外科修復)`);
}

console.log("\n【確認4/§4-5 緩和 vs 修復】g=3.0, pmax=8 で不可逆化した後の三介入");
{
  // 不可逆状態を作る
  let H = 100, D = 0; const g = 3.0;
  const lv = []; for (let i = 0; i <= 40; i++) lv.push(i / 40 * 8); for (let i = 39; i >= 0; i--) lv.push(i / 40 * 8);
  for (const p of lv) for (let s = 0; s < 10; s++)[H, D] = stepDyn(H, D, p, 0, g);
  const broken = { H: +H.toFixed(1), D: +D.toFixed(1) };
  // (a) 緩和: p=0,b=0
  let Ha = H, Da = D; for (let s = 0; s < 2000; s++)[Ha, Da] = stepDyn(Ha, Da, 0, 0, g);
  // (b) 緩和+緩衝: p=0,b=1
  let Hb = H, Db = D; for (let s = 0; s < 2000; s++)[Hb, Db] = stepDyn(Hb, Db, 0, 1, g);
  // (c) 修復: H を強制100へ(ロールバック), その後 p=0
  let Hc = 100, Dc = D; for (let s = 0; s < 2000; s++)[Hc, Dc] = stepDyn(Hc, Dc, 0, 0, g);
  console.log(`   破損状態: H=${broken.H}, D=${broken.D}`);
  console.log(`   (a)緩和のみ   : H=${f(Ha)} D=${f(Da)}  → ${Ha > 50 ? "回復" : "回復せず"}`);
  console.log(`   (b)緩和+緩衝  : H=${f(Hb)} D=${f(Db)}  → ${Hb > 50 ? "回復" : "回復せず"}`);
  console.log(`   (c)外科的修復 : H=${f(Hc)} D=${f(Dc)}  → ${Hc > 50 ? "回復" : "回復せず"}  (Hを強制100に戻す)`);
  console.log(`   → (a)(b)回復せず & (c)回復 なら §4-5「緩和では足りない、修復が要る」を支持`);
}

console.log("\n  → g=0可逆／g>0で臨界点を持つ不可逆が創発／緩和では戻らず修復が要る、が揃えば設計確定。");
