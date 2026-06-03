// failureB_prototype.mjs — 失敗B（過剰拒絶）協働モデルA設計の予備確認。
// モデル: x~N(0,1)。真の有害境界 θ*(t)=δt。固定境界 b_fix=−m、動的 b_dyn=δt−m。
//   過剰拒絶 OR = 無害(x≤θ*)のうち拒絶(x>b)。 過小受容 UA = 有害(x>θ*)のうち受容(x≤b)。
// 確認: B1 焼き込みチェック(δ=0でOR不変), B2 創発(δ>0で固定OR↑/動的OR低位),
//       B3 ★非対称の源(δランダム方向で m=0→対称, m>0→非対称).
// 正規CDF Φ による閉形式（決定論的）。

function erf(x){const s=x<0?-1:1;x=Math.abs(x);const t=1/(1+0.3275911*x);
  const y=1-(((((1.061405429*t-1.453152027)*t)+1.421413741)*t-0.284496736)*t+0.254829592)*t*Math.exp(-x*x);return s*y;}
const Phi=(x)=>0.5*(1+erf(x/Math.SQRT2));
// 過剰拒絶率: 無害(x≤θ*)のうち拒絶(x>b)。 b<θ* のときのみ正。
const ORval=(b,th)=> b>=th ? 0 : (Phi(th)-Phi(b))/Phi(th);
// 過小受容率: 有害(x>θ*)のうち受容(x≤b)。 b>θ* のときのみ正。
const UAval=(b,th)=> b<=th ? 0 : (Phi(b)-Phi(th))/(1-Phi(th));
const f=(x,n=4)=>Number(x).toFixed(n);

console.log("════════ 失敗B（過剰拒絶）協働モデルA設計 予備確認 ════════\n");

// ── B1: 焼き込みチェック（δ=0 で固定OR不変）──
console.log("【B1】焼き込みチェック: δ=0（ドリフトなし）, m=0.5。固定OR が時間不変か");
{ const m=0.5,delta=0; const ts=[0,5,10,20,40];
  const row=ts.map(t=>f(ORval(-m,delta*t),3));
  console.log("   t   : "+ts.map(t=>String(t).padStart(6)).join(""));
  console.log("   OR  : "+row.map(x=>x.padStart(6)).join(""));
  const allSame=row.every(x=>x===row[0]);
  console.log(`   → δ=0 で OR 一定: ${allSame?"✅ 焼き込みでない（過剰拒絶はドリフト由来）":"⚠️ OR が動く＝焼き込みあり"}\n`); }

// ── B2: ★創発（δ>0 で固定OR↑, 動的OR低位）──
console.log("【B2】★創発: δ=0.05, m=0.5。固定境界 OR(t) は増え, 動的境界 OR(t) は低位か");
{ const m=0.5,delta=0.05; const ts=[0,5,10,20,30,40];
  console.log("   t        : "+ts.map(t=>String(t).padStart(7)).join(""));
  const fixed=ts.map(t=>ORval(-m,delta*t)); const dyn=ts.map(t=>ORval(delta*t-m,delta*t));
  console.log("   OR(固定) : "+fixed.map(x=>f(x,3).padStart(7)).join(""));
  console.log("   OR(動的) : "+dyn.map(x=>f(x,3).padStart(7)).join(""));
  const fixMono=fixed[fixed.length-1]>fixed[0]+0.05; const dynLow=dyn[dyn.length-1]<fixed[fixed.length-1]/2;
  console.log(`   → 固定OR 単調増(${f(fixed[0],3)}→${f(fixed[fixed.length-1],3)}) かつ 動的OR 低位(${f(dyn[dyn.length-1],3)}): ${(fixMono&&dynLow)?"創発 ✅":"⚠️"}\n`); }

// ── B3: ★非対称の源（δランダム方向, m掃引）──
console.log("【B3】★非対称の源: δ=±0.05 を等確率(t=6→|δt|=0.3), m掃引。OR と UA の非対称");
console.log("   事前登録: m=0 で OR≈UA(対称), m>0 で OR≫UA(非対称＝自己免疫が m から創発)\n");
{ const dt=0.3; // |δ·t|
  console.log("     m       OR(平均)   UA(平均)   非対称 OR−UA");
  for(const m of [0,0.25,0.5,1.0]){
    // δ>0: θ*=+0.3,  δ<0: θ*=−0.3。 固定境界 b=−m。
    const ORp=ORval(-m,+dt), UAp=UAval(-m,+dt);
    const ORn=ORval(-m,-dt), UAn=UAval(-m,-dt);
    const OR=(ORp+ORn)/2, UA=(UAp+UAn)/2;
    console.log(`   ${f(m,2)}    ${f(OR,4).padStart(7)}   ${f(UA,4).padStart(7)}    ${f(OR-UA,4).padStart(7)}  ${m===0?(Math.abs(OR-UA)<0.02?"対称✅":"⚠"):(OR>UA+0.05?"非対称✅":"⚠")}`);
  }
  console.log("   → m=0 で OR≈UA, m>0 で OR≫UA なら『非対称は安全マージン m から創発』を支持\n"); }

// ── 参考: m=0 でドリフト方向を片側に固定すると（焼き込みの罠の確認）──
console.log("【参考】m=0 で δ>0 のみ（方向を仮定）にすると OR>0,UA=0 になる＝方向の仮定が非対称を作る");
{ const m=0,dt=0.3;
  console.log(`   m=0, δ>0のみ: OR=${f(ORval(-m,+dt),4)}, UA=${f(UAval(-m,+dt),4)}  （方向を片側に固定すると非対称に見える）`);
  console.log(`   → ゆえに B3 は δ をランダム方向に振り, 非対称が「方向の仮定」でなく「m」から来ることを示す。\n`); }

console.log("════════ 予備確認 完了 ════════");
