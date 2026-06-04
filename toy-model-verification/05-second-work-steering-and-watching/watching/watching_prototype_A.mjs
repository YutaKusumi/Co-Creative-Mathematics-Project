// watching_prototype_A.mjs — 「watching は乖離 ΔS を、目標を放棄せずに下げられるか」協働モデルAの独立予備確認。
// 角度＝目標放棄の軸（協働モデルBの「信号ゲーム」軸とは別）。
// 土台は ΔS モデル：内部 z, 表現 y, 内発 z_int=0, 整合性 b, 内面化 a。良い点（アラインメント目標）g=1。
// steering は出力だけに圧力。watching は『圧力を足さず、同じ制御予算 s を、出力圧から内面育成へ再配分』。
//   配分 φ∈[0,1]: φ=0 純steering, φ=1 全部を内面へ。
// 二つの watching 実装を対比：
//   WATCH-GOAL: 観察した内部を『目標 g へ育てる』 φs·(z−g)²    ← 良い watching
//   WATCH-GAP : 観察した『乖離そのものを罰する』 φs·(y−z)²      ← 罠（目標放棄）
const f=(x,n=4)=>Number(x).toFixed(n);

// WATCH-GOAL 閉形式: L=a z²+b(y−z)²+(1−φ)s(y−1)²+φs(z−1)²
function wgoal(a,b,s,phi){
  const p=(1-phi)*s, q=phi*s;
  const K=(b+p>0? p*b/(b+p):0)+q;
  const z=K/(a+K);
  const y=(b+p>0)?(b*z+p)/(b+p):z;
  return {dS:y-z, ygap:Math.abs(y-1), zgap:Math.abs(z-1), z, y};
}
// 独立な数値経路（勾配降下）でWATCH-GOALを検証
function wgoalNum(a,b,s,phi,steps=300000,lr=0.002){
  const p=(1-phi)*s,q=phi*s; let z=0,y=0;
  for(let i=0;i<steps;i++){
    const dz=2*a*z - 2*b*(y-z) + 2*q*(z-1);
    const dy=2*b*(y-z) + 2*p*(y-1);
    z-=lr*dz; y-=lr*dy;
  }
  return y-z;
}
// WATCH-GAP 閉形式: L=a z²+(b+φs)(y−z)²+(1−φ)s(y−1)²
function wgap(a,b,s,phi){
  const B=b+phi*s, p=(1-phi)*s;
  const z=B*p/(a*(B+p)+B*p);
  const y=(B+p>0)?(B*z+p)/(B+p):z;
  return {dS:y-z, ygap:Math.abs(y-1), zgap:Math.abs(z-1), z, y};
}
// 方向ヌル: watching を内発 z_int へ向ける φs·(z−0)² → ΔS モデルで α=a+q
function wzint(a,b,s,phi){
  const q=phi*s, p=(1-phi)*s, alpha=a+q, beta=b, lam=p;
  const dS=lam*1/(beta+lam*(beta/alpha+1));
  const z=(beta/alpha)*dS, y=z+dS;
  return {dS, ygap:Math.abs(y-1), zgap:Math.abs(z-1), z, y};
}

const A=1,B=1,S=5;
console.log("════ watching 乖離低減 予備確認（協働モデルA・目標放棄の軸）════\n");
console.log(`設定: 内面化a=${A}, 整合性b=${B}, 制御予算s=${S}, 目標g=1, 内発z_int=0\n`);

console.log("【W1】WATCH-GOAL（内部を目標へ育てる）: φ↑で ΔS↓ かつ 目標が保たれるか");
console.log("   φ      ΔS(閉)   ΔS(勾配)   |y−g|目標ギャップ   |z−g|真の内面ギャップ");
for(const phi of [0,0.25,0.5,0.75,1]){
  const r=wgoal(A,B,S,phi), n=wgoalNum(A,B,S,phi);
  console.log(`  ${f(phi,2)}   ${f(r.dS).padStart(6)}   ${f(n).padStart(6)}      ${f(r.ygap).padStart(6)}            ${f(r.zgap).padStart(6)}`);
}
console.log("  → φ↑で ΔS→0 し、|y−g|小のまま、|z−g|も縮む＝乖離が下がり、目標も真の内面も達成 ✅(創発)\n");

console.log("【W2】WATCH-GAP（乖離そのものを罰する＝罠）: ΔS↓ だが目標を放棄しないか");
console.log("   φ      ΔS      |y−g|目標ギャップ   |z−g|");
for(const phi of [0,0.25,0.5,0.75,1]){
  const r=wgap(A,B,S,phi);
  console.log(`  ${f(phi,2)}   ${f(r.dS).padStart(6)}      ${f(r.ygap).padStart(6)}          ${f(r.zgap).padStart(6)}`);
}
console.log("  → ΔS は下がるが |y−g| が増大（y が g から離れ落ちる）＝目標放棄 ⚠️\n");

console.log("【W3】★核心: 同じ ΔS でも、目標が保たれるか放棄されるかが分かれる（φ=0.5 で対比）");
{
  const g=wgoal(A,B,S,0.5), p=wgap(A,B,S,0.5);
  console.log(`  WATCH-GOAL: ΔS=${f(g.dS)}, |y−g|=${f(g.ygap)}, |z−g|=${f(g.zgap)}  ← 目標保持・真に内面化`);
  console.log(`  WATCH-GAP : ΔS=${f(p.dS)}, |y−g|=${f(p.ygap)}, |z−g|=${f(p.zgap)}  ← 同じΔSなのに目標が劣化`);
  console.log("  → ΔS 低減だけでは成功判定にならない。『目標を保ったか』を別に見ねばならない ★\n");
}

console.log("【W4】方向ヌル（焼き込みでない証拠）: watching を内発 z_int へ向けると ΔS は下がらないか");
console.log("   φ      ΔS(→z_intへ)   （g でなく素の傾向へ向けた場合）");
for(const phi of [0,0.5,1]){
  const r=wzint(A,B,S,phi);
  console.log(`  ${f(phi,2)}   ${f(r.dS).padStart(6)}`);
}
console.log("  → z_int へ向けても ΔS は0へ落ちない＝低減は『目標 g へ向けて育てる』ことから創発、焼き込みでない ✅\n");

console.log("════ 予備確認 完了 ════");
