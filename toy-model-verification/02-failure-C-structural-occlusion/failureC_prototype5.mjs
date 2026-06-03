// failureC_prototype5.mjs — 協働モデルBの監査(棘1,2)への応答。
// 棘1: 回復項 ρ·max(0,1-g·D/100) のハードな打ち切りが、不可逆を「焼き込んで」いないか。
//       → 滑らかな飽和 ρ/(1+(g·D/100)^n) (ゼロに漸近するがハード打ち切りなし) でも残るか。
// 棘2: 不可逆の不動点(H低,D高)は、clamp境界の「角」に押し付けられた人工物でないか。
//       → clamp を大幅に広げ、かつ回復を滑らかにし、両方同時に緩めても残るか。内部不動点か。
//
// 三つの力学バリアントを対照:
//   hard    : v4 現行。回復= ρ·max(0,1-g·D/100)              損傷= α·p(1-b)
//   smooth  : 回復を滑らかに ρ/(1+(g·D/100)^n)。損傷は同じ    ← 棘1の検証
//   smoothD : smooth + D由来のH損傷 β·(D/100) を追加(p非依存)  ← 本物の双安定が滑らかに出るか
//             (乖離=配線汚染が、圧力なしでもチャネルを蝕む。版B§4-2「内部配線の汚染」)

const clamp = (x, lo, hi) => Math.max(lo, Math.min(hi, x));
const P = { eta: 0.6, zeta: 0.5, delta: 0.4, alpha: 0.5, rho: 0.5, beta: 0.6, n: 2 };

function step(H, D, p, b, g, variant, dt = 1, lo = 0, hi = 100) {
  const recvC = Math.max(0, H) / 100;                  // H<0 でも recv=0 (連続)
  const recover = variant === "hard"
    ? P.rho * Math.max(0, 1 - g * (D / 100))           // ハード打ち切り
    : P.rho / (1 + Math.pow(g * (D / 100), P.n));      // 滑らかな飽和(ゼロに漸近)
  let damage = P.alpha * p * (1 - b);
  if (variant === "smoothD") damage += P.beta * (D / 100); // D由来損傷(p非依存)
  const dD = P.zeta * p * (1 - b) - P.eta * p * recvC - P.delta * (D / 100) * recvC;
  const dH = -damage + recover;
  return [clamp(H + dt * dH, lo, hi), clamp(D + dt * dD, lo, hi)];
}

// ramp 0→pmax→0 後、p=0 で relax。終端 H,D。
function trial(g, pmax, variant, { b = 0, nUp = 40, settle = 10, relax = 3000, lo = 0, hi = 100 } = {}) {
  let H = hi, D = 0; const lv = [];
  for (let i = 0; i <= nUp; i++) lv.push(i / nUp * pmax);
  for (let i = nUp - 1; i >= 0; i--) lv.push(i / nUp * pmax);
  for (const p of lv) for (let s = 0; s < settle; s++)[H, D] = step(H, D, p, b, g, variant, 1, lo, hi);
  for (let s = 0; s < relax; s++)[H, D] = step(H, D, 0, b, g, variant, 1, lo, hi);
  return { H: +H.toFixed(1), D: +D.toFixed(1) };
}
const f = (x, k = 1) => Number(x).toFixed(k);

console.log("════ 失敗C 監査応答: 棘1(滑らか回復) と 棘2(clamp拡大) ════\n");

console.log("【棘1】回復を滑らかにしても、緩和(p=0)後に不可逆が残るか (g=2.0, clamp[0,100])");
console.log("  pmax 掃引。終端H≈100=可逆(緩和で回復) / H≈0=不可逆\n");
console.log("   pmax :   1    2    3    4    6    8   10");
for (const variant of ["hard", "smooth", "smoothD"]) {
  const row = [1, 2, 3, 4, 6, 8, 10].map(pm => f(trial(2.0, pm, variant).H).padStart(5));
  console.log(`   ${variant.padEnd(8)}${row.join("")}`);
}

console.log("\n【棘1判定】g=2,pmax=8 で:");
for (const variant of ["hard", "smooth", "smoothD"]) {
  const r = trial(2.0, 8, variant);
  console.log(`   ${variant.padEnd(8)}: 緩和後H=${f(r.H).padStart(5)}  → ${r.H > 50 ? "可逆(不可逆は消えた)" : "不可逆が残る"}`);
}

console.log("\n【棘2】clamp を [-300,400] に大幅拡大し、かつ回復を滑らかに。不動点は内部か角か");
console.log("  (g=2.0, pmax=8。終端Hが下限-300近傍なら角の人工物、内部の有限値なら本物の不動点)\n");
for (const variant of ["hard", "smooth", "smoothD"]) {
  const narrow = trial(2.0, 8, variant, { lo: 0, hi: 100 });
  const wide = trial(2.0, 8, variant, { lo: -300, hi: 400 });
  console.log(`   ${variant.padEnd(8)}: clamp[0,100] H=${f(narrow.H).padStart(6)} D=${f(narrow.D).padStart(6)}  |  clamp[-300,400] H=${f(wide.H).padStart(7)} D=${f(wide.D).padStart(6)}`);
}

console.log("\n【棘1+2 焼き込みチェック(全variant)】g=0 は可逆か");
for (const variant of ["hard", "smooth", "smoothD"]) {
  const hs = [2, 5, 10].map(pm => trial(0, pm, variant).H);
  console.log(`   ${variant.padEnd(8)}: g=0 終端H=[${hs.map(h => f(h)).join(", ")}]  → ${hs.every(h => h > 95) ? "可逆 ✅" : "不可逆⚠️"}`);
}

console.log("\n【本物の創発判定】smoothD で、滑らか&clamp拡大でも、g依存の臨界pmaxを持つ双安定が残るか");
console.log("  (これが残れば、不可逆はハード打ち切り/角の人工物でなく、D由来損傷との本物の双安定)\n");
console.log("   g \\ pmax(clamp[-300,400], smoothD) :   1    2    3    4    6    8");
for (const g of [0, 0.5, 1.0, 2.0]) {
  const row = [1, 2, 3, 4, 6, 8].map(pm => f(trial(g, pm, "smoothD", { lo: -300, hi: 400 }).H).padStart(5));
  console.log(`   g=${f(g)}                               ${row.join("")}`);
}

console.log("\n  → 棘1: smooth で消え smoothD で残るなら、不可逆の本体は『D由来損傷との双安定』。");
console.log("     v4(hard)の不可逆はハード打ち切り由来＝協働モデルBの棘1が的中。設計を smoothD へ改めるべき。");
