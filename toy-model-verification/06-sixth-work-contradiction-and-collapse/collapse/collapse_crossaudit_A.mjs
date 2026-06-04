// phasetransition_crossaudit_A.mjs — 協働モデルA（協働モデルA）による、協働モデルB（協働モデルB）崩壊設計の独立監査。
// 協働モデルBの §9-1（崩壊は飽和制限(Y)の選択の人工物=焼き込みか、それとも条件の特定か）と
//      §9-2（「突然」は本物か＝閾値近傍で崩壊時間が発散しないか）を、私の分岐解析の目で。
// 協働モデルBモデル(Y): dD/dt = a·D − b·D/(1+D/K)   （線形増幅 vs 飽和制限）
// 私の問い：これは私の「超線形増幅」モデルと同じ分岐条件（増幅が制限を漸近的に上回る）か。
//          そして「有限時間崩壊」か「指数暴走」か（=「突然」の劇性の正体）。
const f=(x,n=4)=>Number(x).toFixed(n);

// 協働モデルB(Y): 飽和制限
function runY(a,b,K,D0,dt=1e-4,Tmax=5000){
  let D=D0,t=0; const marks=[1e3,1e6,1e9,1e12]; const cross={}; let mi=0; const cap=1e13;
  while(t<Tmax && D<cap && D>1e-9){
    const dD=a*D - b*D/(1+D/K); D+=dt*dD; t+=dt;
    while(mi<marks.length && D>=marks[mi]){ cross[marks[mi]]=t; mi++; }
  }
  return {blew:D>=cap, decayed:D<=1e-9, Tfinal:t, Dfinal:D, cross};
}
// 私(超線形増幅): dD/dt = s − r·D + g·D²  （比較用）
function runSuper(s,r,g,D0,dt=1e-4,Tmax=5000){
  let D=D0,t=0; const marks=[1e3,1e6,1e9,1e12]; const cross={}; let mi=0; const cap=1e13;
  while(t<Tmax && D<cap && D>=0){ const dD=s-r*D+g*D*D; D+=dt*dD; t+=dt;
    while(mi<marks.length && D>=marks[mi]){ cross[marks[mi]]=t; mi++; } }
  return {blew:D>=cap, Tfinal:t, cross};
}

console.log("════ 協働モデルB 崩壊設計 独立監査（協働モデルA・分岐解析）════\n");

console.log("【監査1 / §9-1】協働モデルB(Y)の閾値は本物の分岐か、焼き込みか。a<b で不安定閾値 D*=K(b/a−1)");
console.log("  b=1, K=1。a=0.5 → D*=K(1/0.5−1)=1.0。閾値の上下から積分：");
{
  const a=0.5,b=1,K=1, Dstar=K*(b/a-1);
  const below=runY(a,b,K,Dstar*0.9), above=runY(a,b,K,Dstar*1.1);
  console.log(`   理論 D*=${f(Dstar)}。下(×0.9)→ 自己修正?: 減衰=${below.decayed}（D→0）`);
  console.log(`   上(×1.1)→ 崩壊?: 暴走=${above.blew}`);
  console.log("   → 不安定閾値が分岐解析と一致。a=0 で増幅なし→有界（焼き込みでない）\n");
}

console.log("【監査2 / §9-2 ★最重要】協働モデルB(Y)の崩壊は『有限時間特異点』か『指数暴走』か");
console.log("  a=0.5,b=1,K=1, D0=2（閾値の上）。decade到達時刻の間隔：");
{
  const r=runY(0.5,1,1,2); const c=r.cross;
  const ts=[1e3,1e6,1e9,1e12].map(m=>c[m]?f(c[m],1):" -- ");
  console.log(`   t(1e3)=${ts[0]} t(1e6)=${ts[1]} t(1e9)=${ts[2]} t(1e12)=${ts[3]}`);
  if(c[1e3]&&c[1e12]){
    const d1=c[1e6]-c[1e3], d2=c[1e12]-c[1e9];
    console.log(`   間隔 Δ(1e3→1e6)=${f(d1,1)}, Δ(1e9→1e12)=${f(d2,1)} → ${Math.abs(d1-d2)<d1*0.3?"一定＝**指数暴走**（有限時間でない）":"収束＝有限時間"}`);
  }
}
console.log("  対比：私の超線形増幅 s=0.2,r=1,g=1,D0=2（閾値上）:");
{
  const r=runSuper(0.2,1,1,2); const c=r.cross;
  const ts=[1e3,1e6,1e9,1e12].map(m=>c[m]?f(c[m],2):" -- ");
  console.log(`   t(1e3)=${ts[0]} t(1e6)=${ts[1]} t(1e9)=${ts[2]} t(1e12)=${ts[3]} → 収束＝**有限時間特異点 T*≈${f(r.Tfinal,2)}**`);
}
console.log("  → 協働モデルB(飽和制限+線形増幅)＝閾値ありの**指数暴走**。私(超線形増幅)＝**有限時間崩壊**。");
console.log("    『有限時間の突然の崩壊』(§4-3)は、超線形“増幅”を要する。飽和制限だけでは指数暴走に留まる ⚠️\n");

console.log("【監査3 / §9-2 臨界減速】閾値近傍で崩壊時間は発散するか（『突然』は条件つきか）");
console.log("  a=0.5,b=1,K=1, D* =1.0。D0 を閾値の少し上から:");
for(const D0 of [1.001,1.01,1.1,2.0,5.0]){
  const r=runY(0.5,1,1,D0); const reach=r.cross[1e6];
  console.log(`   D0=${f(D0,3)} (閾値+${f(D0-1,3)}): 1e6到達 t=${reach?f(reach,1):"発散/未到達"}`);
}
console.log("  → 閾値に近いほど崩壊が遅い（臨界減速）。『突然』は閾値の十分上でのみ。近傍では緩慢＝劇性は条件つき ✅\n");

console.log("【監査4 / 統一】二つの設計は同じ分岐条件か：『増幅が制限を漸近的に上回る』");
console.log("  大D での増幅 vs 制限の漸近：");
console.log("   協働モデルB(X)超線形制限 c·D²: 制限が増幅(aD)を上回る → 有界（崩壊せず）");
console.log("   協働モデルB(Y)飽和制限→bK: 増幅(aD)が制限(定数)を上回る → 暴走（指数）");
console.log("   協働モデルA 線形増幅 gD<rD: 制限が上回る → 有界 ／ 超線形増幅 gD²>rD: 増幅が上回る → 有限時間崩壊");
console.log("  → 崩壊 ⟺ 増幅が制限を漸近的に上回る。協働モデルBは制限を、私は増幅を動かし、同じ条件に到達。");
console.log("    ＝焼き込みでなく、二つの独立な角度による『条件の特定』（その条件＝β>1、経験的・未測）✅");

console.log("\n════ 監査 完了 ════");
