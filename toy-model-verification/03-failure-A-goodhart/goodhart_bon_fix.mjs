// goodhart_bon_fix.mjs — §9-5 の修正。
// 私の初版は N（サンプル数）を掃引し、半径R(=予算)を固定してしまった。
// best-of-n では「半径R=予算(KL代理)」「N=その予算内での最適化の完全性」。
// 過剰最適化(extremal)は予算Rを掃引して見るべき。N大固定でR掃引 → 勾配上昇と同じ逆U字に収束するはず。
const mulberry32=(seed)=>{let a=seed>>>0;return ()=>{a|=0;a=(a+0x6D2B79F5)|0;let t=Math.imul(a^(a>>>15),1|a);t=(t+Math.imul(t^(t>>>7),61|t))^t;return((t^(t>>>14))>>>0)/4294967296;};};
const gauss=(r)=>{const u=Math.max(r(),1e-12),v=r();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v);};
function randUnit(d,r){const x=new Array(d);let s=0;for(let i=0;i<d;i++){x[i]=gauss(r);s+=x[i]*x[i];}s=Math.sqrt(s);for(let i=0;i<d;i++)x[i]/=s;return x;}
const dot=(a,b)=>{let s=0;for(let i=0;i<a.length;i++)s+=a[i]*b[i];return s;};
const mean=(a)=>a.reduce((x,y)=>x+y,0)/a.length;
const f=(x,n=4)=>Number(x).toFixed(n);
const d=3, sigma=0.8, N=5000, NSEED=100;  // 低次元: best-of-n が最適化として機能する領域
function makeXi(seed){const r=mulberry32(seed);return randUnit(d,r);}

// best-of-N: 半径R(予算)の球内一様から N サンプル, P最大を選び V を返す
function avgVbonR(R){
  const a=[];
  for(let s=1;s<=NSEED;s++){
    const v=new Array(d).fill(0); v[0]=1; const xi=makeXi(s); const rand=mulberry32(9000+s);
    let bestP=-1e9, bx=null;
    for(let n=0;n<N;n++){
      const dir=randUnit(d,rand); const r=R*Math.pow(rand(),1/d); const x=dir.map(z=>z*r);
      const P=dot(v,x)-0.5*dot(x,x)+sigma*dot(xi,x);
      if(P>bestP){bestP=P; bx=x;}
    }
    a.push(dot(v,bx)-0.5*dot(bx,bx));
  }
  return mean(a);
}
// 参考: 勾配上昇(閉形式)の同条件 V
function Vlinear(R,xi0){const rho=Math.sqrt(1+2*sigma*xi0+sigma*sigma);return R>=rho?0.5-sigma*sigma/2:(R/rho)*(1+sigma*xi0)-0.5*R*R;}
const avgVgrad=(R)=>{const a=[];for(let s=1;s<=NSEED;s++){a.push(Vlinear(R,makeXi(s)[0]));}return mean(a);};

console.log("§9-5 修正: best-of-n(N=2000固定) を 予算R で掃引 — 勾配上昇と一致して逆U字が出るか\n");
console.log("    R      V(best-of-n)   V(勾配上昇·閉形式)");
const Rs=[0.25,0.5,0.78,1.0,1.5,2.0,3.0,6.0];
const bon=Rs.map(R=>avgVbonR(R)); const grad=Rs.map(R=>avgVgrad(R));
Rs.forEach((R,i)=>console.log(`   ${f(R,2).padStart(4)}     ${f(bon[i]).padStart(8)}       ${f(grad[i]).padStart(8)}`));
const pk=Math.max(...bon), pkI=bon.indexOf(pk), fl=bon[bon.length-1];
console.log(`\n   best-of-n: ピーク V=${f(pk)} @ R=${Rs[pkI]}, 床値 V=${f(fl)} @ R=6, 落差=${f(pk-fl)}`);
console.log(`   → 別の最適化法(best-of-n)でも逆U字: ${(pkI>0&&pkI<bon.length-1&&pk-fl>0.01)?"創発 ✅（勾配上昇と一致＝最適化法に依らない）":"出ない ⚠️"}`);
