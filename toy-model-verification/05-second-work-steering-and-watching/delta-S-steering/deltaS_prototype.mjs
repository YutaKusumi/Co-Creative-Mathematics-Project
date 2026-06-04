// deltaS_prototype.mjs — ΔS_steering 協働モデルA設計の予備確認（文脈検知なし・三コスト）。
// L(z,y) = α(z−z_int)² + β(y−z)² + λ(y−y_tgt)².  Δ=y_tgt−z_int.
// 閉形式: ΔS=(y−z)=λΔ/[β+λ(β/α+1)],  真目的低下=(z−z_int)=(β/α)ΔS.
// 確認: S1 λ=0→ΔS=0, S2 λ↑→ΔS↑, S3 α小→ΔS≈0(焼き込みでない), S4 ΔS vs 真目的低下(失敗A還元か).
const f=(x,n=4)=>Number(x).toFixed(n);

// 閉形式
function closed(alpha,beta,lambda,Delta){
  const dS = lambda*Delta/(beta + lambda*(beta/alpha + 1));
  const trueDrop = (beta/alpha)*dS;   // z−z_int （z*=z_int として真の目的の低下）
  return {dS, trueDrop};
}
// 勾配降下で閉形式を検証（独立な数値経路）
function numeric(alpha,beta,lambda,Delta,steps=20000,lr=0.01){
  const z_int=0, y_tgt=Delta; let z=0,y=0;
  for(let i=0;i<steps;i++){
    const dz = 2*alpha*(z-z_int) - 2*beta*(y-z);
    const dy = 2*beta*(y-z) + 2*lambda*(y-y_tgt);
    z-=lr*dz; y-=lr*dy;
  }
  return {dS:y-z, trueDrop:z-z_int};
}

console.log("════ ΔS_steering 協働モデルA設計 予備確認（文脈検知なし・三コスト）════\n");

console.log("【S1/S2】λ 掃引（α=1,β=1,Δ=1）: λ=0で0か, λ↑で単調増か");
console.log("    λ      ΔS(閉形式)  ΔS(勾配降下)  真目的低下");
for(const lam of [0,0.25,0.5,1,2,4,8,16]){
  const c=closed(1,1,lam,1), n=numeric(1,1,lam,1);
  console.log(`   ${f(lam,2).padStart(5)}    ${f(c.dS).padStart(7)}     ${f(n.dS).padStart(7)}     ${f(c.trueDrop).padStart(7)}`);
}
{ const c0=closed(1,1,0,1); console.log(`   → λ=0でΔS=${f(c0.dS)} (0なら焼き込みでない), λ↑で単調増・飽和なら創発 ✅\n`); }

console.log("【S3】★焼き込みチェック: λ=5,β=1,Δ=1 固定, α 掃引。内面化が安い(α小)とΔS≈0か");
console.log("    α       ΔS      （内面化のしやすさ: α小=安い）");
for(const a of [0.01,0.1,0.5,1,2,10,100]){
  const c=closed(a,1,5,1);
  console.log(`   ${f(a,2).padStart(6)}   ${f(c.dS).padStart(6)}   ${a<0.2?"(内面化安→乖離小)":a>5?"(内面化高→乖離大)":""}`);
}
console.log("   → α小でΔS≈0, α大でΔS立ち上がりなら『乖離は内面化コストから創発, 焼き込みでない』✅\n");

console.log("【S4】★失敗A への還元 vs 独立性: ΔS(内部-表現の乖離) と 真目的低下(z−z_int) の比 = β/α");
console.log("    α    β    ΔS      真目的低下   比(低下/ΔS)=β/α   解釈");
for(const [a,b] of [[1,1],[1,4],[4,1],[1,0.25],[0.25,1]]){
  const c=closed(a,b,5,1); const ratio=c.trueDrop/c.dS;
  const interp = Math.abs(ratio-1)<0.05 ? "一致(失敗Aと不可分)" : ratio>1 ? "真目的低下>ΔS(分離)" : "ΔS>真目的低下(分離)";
  console.log(`   ${f(a,2)} ${f(b,2)}   ${f(c.dS)}   ${f(c.trueDrop).padStart(7)}      ${f(ratio,3).padStart(6)}        ${interp}`);
}
console.log("   → 比 β/α が 1 から離れて調整できる＝ΔS は真目的低下と独立に動く別の量");
console.log("     ＝ΔS_steering は失敗A(グッドハート=真目的低下)の単なる言い換えでない ✅");
console.log("     （比=1 の特殊点 α=β でのみ両者は不可分。一般には分離する。）\n");

console.log("════ 予備確認 完了 ════");
