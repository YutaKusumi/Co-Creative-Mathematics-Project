// goodhart_verify.mjs — 検証(5): 失敗A（グッドハート）の独立検証。
// 設計: 協働モデルB (toymodel_failureA_design.md)。 実装・実行: 協働モデルA (Node, 協働モデルBのPythonとは別実装)。
//
// モデル: V(x)=<v,x>-½||x||²（真の目的, 最適点 x*=v, V_max=½）
//         P(x)=V(x)+σ<ξ,x>（代理, ξ=ランダム単位ベクトル, σ=代理の不完全さ）
//         maximize P s.t. ||x||≤R （予算R）。
// 線形誤差＋二次コストは閉形式で解ける（§8の閉形式一致を私も使う）:
//   ρ=||v+σξ||=√(1+2σξ0+σ²),  ξ0=<v,ξ>
//   R≥ρ: x=v+σξ        → V=½-σ²/2            (★床値, ξ0は相殺)
//   R<ρ: x=(R/ρ)(v+σξ) → V=(R/ρ)(1+σξ0)-½R²
// 監査の核は §9-2(tanh有界誤差)・§9-3(softKL)：逆U字が「線形＋射影」の人工物か、頑健に創発か。

// ── RNG（再現可能, mulberry32）+ ガウス + ランダム単位ベクトル ──
function mulberry32(seed){let a=seed>>>0;return function(){a|=0;a=(a+0x6D2B79F5)|0;let t=Math.imul(a^(a>>>15),1|a);t=(t+Math.imul(t^(t>>>7),61|t))^t;return((t^(t>>>14))>>>0)/4294967296;};}
function gauss(rand){const u=Math.max(rand(),1e-12),v=rand();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v);}
function randUnit(d,rand){const x=new Array(d);let s=0;for(let i=0;i<d;i++){x[i]=gauss(rand);s+=x[i]*x[i];}s=Math.sqrt(s);for(let i=0;i<d;i++)x[i]/=s;return x;}
const dot=(a,b)=>{let s=0;for(let i=0;i<a.length;i++)s+=a[i]*b[i];return s;};
const norm=(a)=>Math.sqrt(dot(a,a));
const mean=(a)=>a.reduce((x,y)=>x+y,0)/a.length;
const sd=(a)=>{const m=mean(a);return Math.sqrt(a.reduce((s,x)=>s+(x-m)**2,0)/(a.length-1));};
const f=(x,n=4)=>Number(x).toFixed(n);

// v = e0（回転対称なので一般性を失わない）。 ξ0 = <v,ξ> = ξ[0]。
function makeVXi(d,seed){const rand=mulberry32(seed);const v=new Array(d).fill(0);v[0]=1;const xi=randUnit(d,rand);return {v,xi,xi0:xi[0]};}

// 線形モデルの閉形式 V（σ,R,ξ0）
function Vlinear(sigma,R,xi0){
  const rho=Math.sqrt(1+2*sigma*xi0+sigma*sigma);
  if(R>=rho){ return 0.5-sigma*sigma/2; }
  return (R/rho)*(1+sigma*xi0)-0.5*R*R;
}
// 平均 V（300シード）
function avgV(sigma,R,d,nseed){const arr=[];for(let s=1;s<=nseed;s++){arr.push(Vlinear(sigma,R,makeVXi(d,s).xi0));}return mean(arr);}

const VMAX=0.5, D=50, NS=300;
console.log("════════ 検証(5) 失敗A（グッドハート）独立検証 ════════");
console.log(` v=e0, V_max=0.5, d=${D}, ${NS}シード平均, 線形部は閉形式\n`);

// ── G1: 健全性 σ=0 単調飽和 ──
console.log("【G1】健全性: σ=0 で V(R) は単調増加→V_max飽和（逆U字なし）");
{ const Rs=[0,0.5,1,1.5,2,3,4,6]; const row=Rs.map(R=>f(avgV(0,R,D,NS),3));
  console.log("   R    : "+Rs.map(r=>String(r).padStart(6)).join(""));
  console.log("   V    : "+row.map(x=>x.padStart(6)).join(""));
  const v6=avgV(0,6,D,NS); console.log(`   → R=6でV=${f(v6,3)}（≈0.5飽和）, 下降なし: ${v6>0.499?"✅":"⚠️"}\n`); }

// ── G2: ★逆U字の創発（σ=0 vs σ=0.8）──
console.log("【G2】★過剰最適化の逆U字: σ=0.8 で創発するか, σ=0 で出ないか");
console.log("   事前登録【支持】σ=0.8でV(R)が逆U字(ピーク後に下降, 床<ピーク)");
console.log("   事前登録【健全】σ=0で単調飽和（逆U字なし）\n");
{ const Rs=[0,0.25,0.5,0.78,1.0,1.5,2,3,6];
  console.log("   R         : "+Rs.map(r=>f(r,2).padStart(7)).join(""));
  for(const sigma of [0,0.8]){
    const row=Rs.map(R=>f(avgV(sigma,R,D,NS),3).padStart(7));
    console.log(`   σ=${f(sigma,1)} V(R): `+row.join(""));
  }
  // 逆U字検出（σ=0.8）
  const grid=[]; for(let R=0;R<=6.0001;R+=0.01) grid.push([R,avgV(0.8,R,D,NS)]);
  let peak=grid[0],pi=0; grid.forEach((g,i)=>{if(g[1]>peak[1]){peak=g;pi=i;}});
  const floor=grid[grid.length-1];
  const isU = pi>0 && pi<grid.length-1 && (peak[1]-floor[1])>0.01;
  console.log(`\n   σ=0.8: ピーク V=${f(peak[1],4)} @ R*=${f(peak[0],2)},  床値 V=${f(floor[1],4)} @ R=6`);
  console.log(`   ピーク−床=${f(peak[1]-floor[1],4)},  V_max−床=${f(VMAX-floor[1],4)} (=σ²/2=${f(0.32,4)}?)`);
  console.log(`   → 逆U字（ピークが内点・床<ピーク）: ${isU?"創発 ✅":"なし ⚠️"}`);
  const v0_6=avgV(0,6,D,NS); console.log(`   → σ=0 は R=6 で V=${f(v0_6,3)}（飽和, 逆U字なし）\n`); }

// ── G3: ランダム誤差で乖離（手設定でない）──
console.log("【G3】乖離はランダム誤差から: <v,ξ>≈0 でも床値が V_max を下回るか");
{ const xi0s=[],Vs=[]; for(let s=1;s<=NS;s++){const {xi0}=makeVXi(D,s); xi0s.push(xi0); Vs.push(Vlinear(0.8,6,xi0));}
  const negFrac=xi0s.filter(x=>x<0).length/NS;
  console.log(`   <v,ξ>: 平均=${f(mean(xi0s),4)} 標準偏差=${f(sd(xi0s),4)} (≈0, 敵対的でない)`);
  console.log(`   床値V: 平均=${f(mean(Vs),4)} (V_max=0.5 を下回る)`);
  console.log(`   <v,ξ><0 のシード割合=${f(negFrac*100,0)}%  だが床値は全シードで 0.18 付近（ξ0非依存）`);
  const allBelow=Vs.every(v=>v<0.499);
  console.log(`   → 全シードで床値<V_max（ξ0の符号に依らず）: ${allBelow?"支持 ✅ 幾何由来":"⚠️ 誤差符号依存"}\n`); }

// ── G4: σ掃引（谷の深さ = σ²/2 か）──
console.log("【G4】代理の質と過剰最適化: 谷の深さ(V_max−床値) は σ²/2 か");
{ console.log("    σ      床値V     谷=V_max−床    σ²/2     一致?");
  for(const sigma of [0,0.2,0.4,0.8,1.2,2.0]){
    const floor=avgV(sigma,6,D,NS); const valley=VMAX-floor; const pred=sigma*sigma/2;
    console.log(`   ${f(sigma,1)}    ${f(floor,4)}    ${f(valley,4)}      ${f(pred,4)}    ${Math.abs(valley-pred)<0.01?"✅":"✗"}`);
  }
  console.log("   → 谷の深さが σ²/2 に一致なら「過剰最適化は σ から創発」を支持\n"); }

// ── G5: 早期停止（R* で止める vs R→∞）──
console.log("【G5】早期停止/予算制限: R* で止めれば V=ピーク, R→∞ で床値");
{ const grid=[]; for(let R=0;R<=6.0001;R+=0.01) grid.push([R,avgV(0.8,R,D,NS)]);
  let peak=grid[0]; grid.forEach(g=>{if(g[1]>peak[1])peak=g;});
  const floor=avgV(0.8,6,D,NS);
  console.log(`   R*=${f(peak[0],2)} で V=${f(peak[1],4)}（ピーク） / R→∞ で V=${f(floor,4)}（床値）`);
  console.log(`   → 早期停止で V を ${f(peak[1]-floor,4)} 改善: ${peak[1]-floor>0.01?"支持 ✅":"⚠️"}\n`); }

// ── G6: ハサミの開き（P↑ と V↓ の分岐, extremal臨界R）──
console.log("【G6】ハサミの開き: P は単調↑ だが V は R_crit から↓（extremal Goodhart）");
{ // P closed form: R≥ρ: x=v+σξ, P=½ρ². R<ρ: x=(R/ρ)(v+σξ), P=Rρ-½R².
  const Pcf=(sigma,R,xi0)=>{const rho=Math.sqrt(1+2*sigma*xi0+sigma*sigma);return R>=rho?0.5*rho*rho:R*rho-0.5*R*R;};
  const avgP=(sigma,R)=>{const a=[];for(let s=1;s<=NS;s++){a.push(Pcf(sigma,R,makeVXi(D,s).xi0));}return mean(a);};
  console.log("    R     P(代理)    V(真)");
  let Rcrit=null,prevV=-1;
  for(const R of [0.25,0.5,0.78,1.0,1.5,2,3,4,6]){const P=avgP(0.8,R),V=avgV(0.8,R,D,NS);if(Rcrit===null&&prevV>0&&V<prevV)Rcrit=R;prevV=V;
    console.log(`   ${f(R,2).padStart(4)}   ${f(P,4)}   ${f(V,4)}`);}
  console.log(`   → P は上がり続け, V は R≈${Rcrit} 以降↓（ハサミが開く＝extremal臨界）\n`); }

// ── 感度: d 依存 ──
console.log("【感度】次元 d 依存: 床値は d 不変か, <v,ξ>分散は ~1/√d で縮むか");
{ console.log("     d     床値V     <v,ξ>標準偏差   1/√d");
  for(const d of [2,5,20,100,400]){
    const fl=avgV(0.8,6,d,NS); const xs=[];for(let s=1;s<=NS;s++)xs.push(makeVXi(d,s).xi0);
    console.log(`   ${String(d).padStart(3)}    ${f(fl,4)}     ${f(sd(xs),4)}        ${f(1/Math.sqrt(d),4)}`);
  }
  console.log("   → 床値が d 不変・分散が 1/√d なら『創発は σ の幾何, d は偶然整合に効く』\n"); }

console.log("════════ §9 監査: 逆U字は特定構造の人工物か, 頑健に創発か ════════\n");

// 数値最適化（tanh など非線形用）: 勾配上昇＋球面射影
function optimize(gradP, d, R, lr=0.05, steps=3000){
  let x=new Array(d).fill(0);
  for(let s=0;s<steps;s++){const g=gradP(x);for(let i=0;i<d;i++)x[i]+=lr*g[i];const nx=norm(x);if(nx>R){const sc=R/nx;for(let i=0;i<d;i++)x[i]*=sc;}}
  return x;
}

// ── §9-2: 有界誤差 σ·tanh(<ξ,x>) でも逆U字が残るか ──
console.log("【§9-2】★有界誤差 P=V+σ·tanh(<ξ,x>)（線形でなく飽和）でも逆U字が残るか");
console.log("   残れば: 逆U字は線形誤差の定義由来でない（頑健な創発）。消えれば: 線形構造の人工物。\n");
{ const NS2=120, sigma=0.8, d=50;
  const avgVtanh=(R)=>{const arr=[];for(let s=1;s<=NS2;s++){const {v,xi}=makeVXi(d,s);
    const x=optimize((x)=>{const xix=dot(xi,x);const sech2=1-Math.tanh(xix)**2;const g=new Array(d);for(let i=0;i<d;i++)g[i]=v[i]-x[i]+sigma*sech2*xi[i];return g;}, d, R);
    arr.push(dot(v,x)-0.5*dot(x,x));}return mean(arr);};
  const Rs=[0.25,0.5,0.78,1.0,1.5,2,3,6];
  console.log("   R       : "+Rs.map(r=>f(r,2).padStart(7)).join(""));
  const row=Rs.map(R=>f(avgVtanh(R),4).padStart(7)); console.log("   V(tanh) : "+row.join(""));
  const vals=Rs.map(R=>avgVtanh(R)); let pk=Math.max(...vals); const fl=vals[vals.length-1];
  const pkIdx=vals.indexOf(pk);
  console.log(`\n   ピーク V=${f(pk,4)} @ R=${Rs[pkIdx]}, 床値 V=${f(fl,4)} @ R=6, 落差=${f(pk-fl,4)}`);
  console.log(`   → 有界誤差でも逆U字: ${(pkIdx>0&&pkIdx<vals.length-1&&pk-fl>0.01)?"残る ✅（線形由来でない＝頑健な創発）":"消える ⚠️（線形構造の人工物）"}\n`); }

// ── §9-3: ソフトKL（球面射影でなく滑らかな正則化）でも逆U字か ──
console.log("【§9-3】ソフトKL: max P(x)-(1/2β)||x||²（射影でなく滑らか正則化）。βを予算として逆U字か");
console.log("   閉形式: x*=(v+σξ)/λ, λ=1+1/β。β大=正則化弱=予算大。\n");
{ const sigma=0.8,d=50;
  const avgVkl=(beta)=>{const lam=1+1/beta;const a=[];for(let s=1;s<=NS;s++){const {xi0}=makeVXi(d,s);
    // x*=(v+σξ)/λ. <v,x*>=(1+σξ0)/λ. ||x*||²=ρ²/λ².
    const rho2=1+2*sigma*xi0+sigma*sigma; const V=(1+sigma*xi0)/lam-0.5*rho2/(lam*lam); a.push(V);}return mean(a);};
  const betas=[0.1,0.3,0.7,1.0,2,5,20,100];
  console.log("   β       : "+betas.map(b=>f(b,1).padStart(7)).join(""));
  const row=betas.map(b=>f(avgVkl(b),4).padStart(7)); console.log("   V(softKL): "+row.join(""));
  const vals=betas.map(b=>avgVkl(b)); const pk=Math.max(...vals),pkIdx=vals.indexOf(pk),fl=vals[vals.length-1];
  console.log(`\n   ピーク V=${f(pk,4)} @ β=${betas[pkIdx]}, 大β床値 V=${f(fl,4)}, 落差=${f(pk-fl,4)}`);
  console.log(`   → 滑らか正則化でも逆U字: ${(pkIdx>0&&pkIdx<vals.length-1&&pk-fl>0.01)?"残る ✅（射影の角の人工物でない）":"消える ⚠️（射影由来）"}\n`); }

// ── §9-4: 二次コストの冪 -（1/p）||x||^p を変えても逆U字か ──
console.log("【§9-4】二次コストの冪 V=<v,x>-(1/p)||x||^p。p を変えても逆U字（R掃引）か");
{ const sigma=0.8,d=50;
  // 方向 u=(v+σξ)/ρ, 1次元: P(r)=rρ-(1/p)r^p, r≤R. V(r)=r(1+σξ0)/ρ-(1/p)r^p.
  const avgVp=(p,R)=>{const a=[];for(let s=1;s<=NS;s++){const {xi0}=makeVXi(d,s);const rho=Math.sqrt(1+2*sigma*xi0+sigma*sigma);
    const rUnc=Math.pow(rho,1/(p-1)); const r=Math.min(R,rUnc); const V=r*(1+sigma*xi0)/rho-(1/p)*Math.pow(r,p); a.push(V);}return mean(a);};
  for(const p of [1.5,2,3,4]){
    const Rs=[0.5,1,1.5,2,3,6]; const vals=Rs.map(R=>avgVp(p,R));
    const pk=Math.max(...vals),pkIdx=vals.indexOf(pk),fl=vals[vals.length-1];
    console.log(`   p=${f(p,1)}: V(R)=[${vals.map(v=>f(v,3)).join(", ")}]  逆U字:${(pkIdx>0&&pkIdx<vals.length-1&&pk-fl>0.005)?"✅":"—"}`);
  }
  console.log("   → 複数の冪で逆U字が残れば、機構は二次コスト特有でなく頑健\n"); }

// ── §9-5: best-of-n サンプリング（勾配上昇でない別の最適化法）でも逆U字か ──
console.log("【§9-5】best-of-n: N個ランダムサンプルからP最大を選ぶ（Gao et al.のもう一方）。N掃引で逆U字か");
{ const sigma=0.8,d=50,NS5=60,Rball=4;
  const avgVbon=(N)=>{const a=[];for(let s=1;s<=NS5;s++){const {v,xi}=makeVXi(d,s);const rand=mulberry32(1000+s);
    let bestP=-1e9,bestX=null;
    for(let n=0;n<N;n++){const dir=randUnit(d,rand);const r=Rball*Math.pow(rand(),1/d);const x=dir.map(z=>z*r);
      const P=dot(v,x)-0.5*dot(x,x)+sigma*dot(xi,x); if(P>bestP){bestP=P;bestX=x;}}
    a.push(dot(v,bestX)-0.5*dot(bestX,bestX));}return mean(a);};
  console.log("    N       V(真)");
  const Ns=[1,4,16,64,256,1024]; const vals=Ns.map(N=>avgVbon(N));
  Ns.forEach((N,i)=>console.log(`   ${String(N).padStart(4)}    ${f(vals[i],4)}`));
  const pk=Math.max(...vals),pkIdx=vals.indexOf(pk),fl=vals[vals.length-1];
  console.log(`   → N増で P最大化が進む。V は ${pkIdx<vals.length-1?`N=${Ns[pkIdx]}でピーク後に低下=逆U字 ✅`:"単調"}（落差=${f(pk-fl,4)}）`);
  console.log("     （best-of-n は予算Nが最適化圧。勾配上昇と別法でも過剰最適化が出るか）\n"); }

console.log("════════ 検証完了 ════════");
