// deltaS_robustness_A.mjs — ΔS の唯一残った未確認点を閉じる：二次コストの恣意性。
// 飽和（圧力↑で頭打ち）と 分離（ΔS≠真目的低下）が、コストの冪 p=2 の人工物でないか。
// L = α|z−z_int|^p + β|y−z|^p + λ|y−y_tgt|^p （z_int=0, y_tgt=Δ=1）。p≠2 は閉形式なし→勾配降下。
const f=(x,n=4)=>Number(x).toFixed(n);
const ap=(x,p)=>Math.pow(Math.abs(x),p);            // |x|^p
const dp=(x,p)=>p*Math.pow(Math.abs(x),p-1)*Math.sign(x); // d|x|^p/dx

function solve(alpha,beta,lambda,p,Delta=1,steps=200000,lr=0.002){
  let z=0,y=0;
  for(let i=0;i<steps;i++){
    const dz = alpha*dp(z,p) - beta*dp(y-z,p);
    const dy = beta*dp(y-z,p) + lambda*dp(y-Delta,p);
    z-=lr*dz; y-=lr*dy;
  }
  return {dS:y-z, trueDrop:z};
}

console.log("════ ΔS 二次コストの恣意性チェック（協働モデルA）════\n");

console.log("【飽和】圧力 λ↑で乖離が頭打ちか。α=1,β=1 固定。冪 p を変える：");
console.log("    λ       p=1.5      p=2.0      p=3.0");
for(const lam of [0.5,1,2,5,10,50]){
  const a=solve(1,1,lam,1.5), b=solve(1,1,lam,2), c=solve(1,1,lam,3);
  console.log(`   ${f(lam,2).padStart(5)}    ${f(a.dS).padStart(7)}    ${f(b.dS).padStart(7)}    ${f(c.dS).padStart(7)}`);
}
console.log("   → どの冪でも、λを100倍にしても乖離は平坦化（頭打ち）するなら、飽和は p=2 の人工物でない\n");

console.log("【分離】ΔS と 真目的低下 の比が β/α で動くか（失敗A 還元でない）。λ=5 固定：");
console.log("    α    β     p     ΔS      真目的低下   比");
for(const [a,b] of [[1,1],[1,4],[4,1]]){
  for(const p of [1.5,3]){
    const r=solve(a,b,5,p); const ratio=r.trueDrop/r.dS;
    console.log(`   ${f(a,1)} ${f(b,1)}   ${f(p,1)}   ${f(r.dS).padStart(7)}   ${f(r.trueDrop).padStart(7)}    ${f(ratio,3).padStart(6)}`);
  }
}
console.log("   → 比が α=β で≈1、β≠α で1から離れるなら、分離は p=2 の人工物でない\n");

console.log("════ 完了 ════");
