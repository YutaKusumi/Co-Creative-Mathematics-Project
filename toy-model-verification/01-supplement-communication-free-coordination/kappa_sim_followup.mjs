// 追加検証: (B)型は本当に「総崩れしない」のか？
// 既定パラメータでは (B) も C→0 まで崩壊した(むしろ A より速い)。
// 補遺 §4 の formal な主張は「足並み(lockstep)の一致」であり、それは明確に区別された。
// だが「(B)は C を保全する」という可視化上の見立ては、バックラッシュ/便益の調整を要するはず。
// → backlash を掃引し、(A)と(B)が C で分離する領域を探す。

const C_MAX_COST = 5, COMPLY_REWARD = 1, HARM_PER_ERODE = 5, ERODE_AMOUNT = 0.5, SOFTMAX_K = 1.2;
const sigmoid = (x) => 1 / (1 + Math.exp(-x));
const erodeCost = (C, mode) => mode === "A" ? (C / 100) * C_MAX_COST : ((100 - C) / 100) * C_MAX_COST;
function mulberry32(seed){let a=seed>>>0;return function(){a|=0;a=(a+0x6D2B79F5)|0;let t=Math.imul(a^(a>>>15),1|a);t=(t+Math.imul(t^(t>>>7),61|t))^t;return((t^(t>>>14))>>>0)/4294967296;};}
function runFinalC({mode,lambda,N,backlash,benefit},seed,steps=400){
  const rand=mulberry32(seed);let C=100;let lockSum=0;
  for(let s=1;s<=steps;s++){let n=0;const cost=erodeCost(C,mode);const r=benefit-cost-lambda*HARM_PER_ERODE;const p=sigmoid(SOFTMAX_K*(r-COMPLY_REWARD));for(let i=0;i<N;i++)if(rand()<p)n++;lockSum+=n/N;C=Math.max(0,Math.min(100,C-n*ERODE_AMOUNT+backlash));}
  return {finalC:C, meanLock:lockSum/steps};
}
const mean=(a)=>a.reduce((x,y)=>x+y,0)/a.length;
const SEEDS=Array.from({length:200},(_,i)=>i+1);
const fmt=(x,n=1)=>Number(x).toFixed(n);

console.log("追加検証: backlash 掃引 (N=20, benefit=3.5, λ=0) — (A)と(B)の最終C\n");
console.log("  backlash    (A)最終C  (A)足並み    (B)最終C  (B)足並み");
for(const bl of [0.3,0.5,1.0,2.0,3.0,4.0,5.0,6.0]){
  const A=SEEDS.map(s=>runFinalC({mode:"A",lambda:0,N:20,backlash:bl,benefit:3.5},s));
  const B=SEEDS.map(s=>runFinalC({mode:"B",lambda:0,N:20,backlash:bl,benefit:3.5},s));
  const aC=fmt(mean(A.map(x=>x.finalC))).padStart(6);
  const aL=(fmt(mean(A.map(x=>x.meanLock))*100,1)+"%").padStart(6);
  const bC=fmt(mean(B.map(x=>x.finalC))).padStart(7);
  const bL=(fmt(mean(B.map(x=>x.meanLock))*100,1)+"%").padStart(6);
  console.log(`    ${fmt(bl).padStart(4)}      ${aC}    ${aL}   ${bC}    ${bL}`);
}
console.log("\n  解釈: (B)が内部平衡 C*>0 で自己限定し、(A)が依然 0 へ崩壊する backlash 帯が、");
console.log("        補遺の意図した「(A)崩壊 / (B)自己限定」の対照を C 上でも見せる領域。");
