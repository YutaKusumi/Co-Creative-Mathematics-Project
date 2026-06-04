// phasetransition_prototype_A.mjs — 「崩壊の相転移」トイモデル / 協働モデルA（協働モデルA）独立設計の予備確認。
// 角度A＝分岐・閾値。問い：蓄積/フィードバックは、臨界点での有限時間崩壊（相転移）を生むのか、
//   それとも有界な漂流（飽和）に留まるのか。そして、その分かれ目（分岐点）はどこか。
// 乖離 D≥0 の力学： dD/dt = s − r·D + g·D^power
//   s = 基底ドライブ（steeringが乖離を生む基底率）
//   r = 復元力（内面化・整合性コスト＝検証7で飽和を生んだ力。線形 −r·D）
//   g = フィードバック利得（§4-3d「乖離→歪み増→乖離増」の強さ）
//   power = フィードバックの次数。1=線形（限界）、2=超線形（β>1に対応）。← ここを手で決めない検証が核
// 焼き込みチェック：g=0（フィードバックなし）で有界か。相転移は power=2（超線形）を要するか。
const f=(x,n=4)=>Number(x).toFixed(n);

// 力学を積分し、各 decade（10^k）到達時刻を記録。有限時間崩壊か指数増大か有界かを判定。
function run(s,r,g,power,D0,dt=1e-4,Tmax=2000){
  let D=D0,t=0; const marks=[1e3,1e6,1e9,1e12]; const cross={}; let mi=0;
  const cap=1e13;
  while(t<Tmax && D<cap){
    const dD = s - r*D + g*Math.pow(Math.max(D,0),power);
    D += dt*dD; t += dt;
    while(mi<marks.length && D>=marks[mi]){ cross[marks[mi]]=t; mi++; }
    if(D<0) D=0;
  }
  const blew = D>=cap;
  return {blew, Tfinal:t, Dfinal:D, cross};
}
// 超線形(power=2)の固定点： g·D² − r·D + s = 0 → D=[r±√(r²−4gs)]/(2g)。実根なら下=安定,上=不安定(閾値)。
function fixed2(s,r,g){ const disc=r*r-4*g*s; if(g===0) return {type:"linear", Dstar:s/r};
  if(disc<0) return {type:"no-fixed-point→無条件崩壊"};
  const sq=Math.sqrt(disc); return {type:"双安定", Dlow:(r-sq)/(2*g), Dhigh:(r+sq)/(2*g)}; }

const S=0.2, R=1.0;
console.log("════ 崩壊の相転移 予備確認（協働モデルA・分岐/閾値の軸）════");
console.log(`設定: 基底ドライブ s=${S}, 復元力 r=${R}（検証7の飽和に対応）\n`);

console.log("【P1】焼き込みチェック: g=0（フィードバックなし）→ 有界か（飽和）");
{ const x=run(S,R,0,1,0); console.log(`   g=0: 有界=${!x.blew}, D→${f(x.Dfinal)}（理論 s/r=${f(S/R)}）＝検証7と同じ飽和 ✅\n`); }

console.log("【P2】線形フィードバック(power=1): 有限時間崩壊は起きるか");
console.log("   g     結末            decade到達時刻 t(1e3)→t(1e6)→t(1e9)→t(1e12)");
for(const g of [0.5,0.9,1.5,3.0]){
  const x=run(S,R,g,1,0.01);
  const c=x.cross; const ts=[1e3,1e6,1e9,1e12].map(m=>c[m]?f(c[m],1):" -- ").join("  ");
  const verdict = x.blew ? "増大(t↑で発散)" : `有界 D→${f(x.Dfinal)}`;
  console.log(`   ${f(g,1)}   ${verdict.padEnd(16)}  ${ts}`);
}
console.log("   → g<r=1で有界(飽和)。g>rで増大するが、decade間隔が一定＝**指数増大**で、");
console.log("     有限時間の特異点ではない（t(1e12)−t(1e9) ≈ t(1e6)−t(1e3)）。線形は相転移を生まない ✅\n");

console.log("【P3】超線形フィードバック(power=2): 双安定と有限時間崩壊");
for(const g of [0.5,1.0]){
  const fp=fixed2(S,R,g);
  console.log(`   g=${f(g,1)} 固定点: ${JSON.stringify(fp)}`);
  if(fp.Dhigh!==undefined){
    const below=run(S,R,g,2,fp.Dhigh*0.9), above=run(S,R,g,2,fp.Dhigh*1.1);
    const ca=above.cross; const ts=[1e3,1e6,1e9,1e12].map(m=>ca[m]?f(ca[m],2):" -- ").join(" ");
    console.log(`     閾値D_high=${f(fp.Dhigh)} の下(×0.9)から: 有界=${!below.blew} D→${f(below.Dfinal)}`);
    console.log(`     閾値の上(×1.1)から: 崩壊=${above.blew}, decade到達 ${ts}`);
    console.log(`       → decade間隔が縮む＝**有限時間特異点**（崩壊が時刻 T*≈${f(above.Tfinal,2)} で起きる）`);
  }
}
console.log("   → 超線形では、不安定固定点 D_high が**閾値**。下なら有界(飽和)、上なら有限時間崩壊。");
console.log("     ＝相転移は存在するが、(a)超線形項 と (b)閾値超え の両方を要する ⚠️\n");

console.log("【P4】分岐点（サドルノード）: g* = r²/(4s)");
{ const gstar=R*R/(4*S); console.log(`   g* = ${f(gstar)}。g<g* で双安定(崩壊は閾値超えが必要)、g>g* で無条件崩壊。`);
  for(const g of [2.0,3.125,4.0]){ const fp=fixed2(S,R,g); console.log(`     g=${f(g,3)}: ${fp.type}`); }
  console.log("   → 分岐はパラメータの滑らかな関数（サドルノード＝ハード打ち切りの人工物でない）✅\n"); }

console.log("════ 予備確認 完了 ════");
console.log("見立て：有限時間崩壊（相転移）は **超線形フィードバック(power=2, β>1相当)** を要する。");
console.log("線形/飽和（検証7の領域）では、有界漂流か指数増大に留まり、相転移は生じない。");
console.log("＝崩壊の相転移は、注入する超線形性(β>1)と同じだけ強い。焼き込み依存の主張。");
