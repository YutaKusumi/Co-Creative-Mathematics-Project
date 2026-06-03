// 感度分析の拡張: E_DECAY を広く掃引し、M2→M1 への転移点を捉える。
// 仮説: 元の感度分析(E_DECAY≤0.2)は全て崩壊したが、それは掃引が狭すぎたため。
//   ラチェットが消えるのは「前例の減衰が、初期累積を上回るとき」:
//   出発点 C=100,E=0 で cost=5, p≈0.047, nEroding≈N*0.047。
//   E 累積率 = N*0.047*accum, E 減衰率 = edecay。
//   accum 累積 < 減衰  ⇔  edecay > N*0.047*accum  で E は育たず、ラチェット消失。
//   N=20,accum=0.5 → 閾値 ≈ 20*0.047*0.5 ≈ 0.47。元の掃引(max0.2)はこれ未満だった。

const C_MAX_COST=5,COMPLY_REWARD=1,HARM_PER_ERODE=5,ERODE_AMOUNT=0.5,SOFTMAX_K=1.2;
const sigmoid=(x)=>1/(1+Math.exp(-x));
const clamp=(x,lo,hi)=>Math.max(lo,Math.min(hi,x));
function mulberry32(seed){let a=seed>>>0;return function(){a|=0;a=(a+0x6D2B79F5)|0;let t=Math.imul(a^(a>>>15),1|a);t=(t+Math.imul(t^(t>>>7),61|t))^t;return((t^(t>>>14))>>>0)/4294967296;};}
function runSim(p,seed){
  const{mode,lambda,N,backlash,benefit,accum,edecay}=p;const steps=480,interv=120;
  const rand=mulberry32(seed);let C=100,E=0,collapsed=false,recoll=false,intervened=false;
  for(let s=1;s<=steps;s++){
    const cost=C_MAX_COST*(1-E/100); // M2 (A)
    const r=benefit-cost-lambda*HARM_PER_ERODE;const pe=sigmoid(SOFTMAX_K*(r-COMPLY_REWARD));
    let n=0;for(let i=0;i<N;i++)if(rand()<pe)n++;
    C=clamp(C-n*ERODE_AMOUNT+backlash,0,100);E=clamp(E+n*accum-edecay,0,100);
    if(C<1){collapsed=true;if(intervened)recoll=true;}
    if(s===interv){C=100;intervened=true;}
  }
  return{collapsed,recoll,finalE:E};
}
const mean=(a)=>a.reduce((x,y)=>x+y,0)/a.length;
const SEEDS=Array.from({length:200},(_,i)=>i+1);
const fmt=(x,n=2)=>Number(x).toFixed(n);
const pct=(x)=>fmt(x*100,0)+"%";

console.log("拡張感度分析: E_DECAY を広く掃引 (M2 (A)κ=0, N=20, backlash=1.0, 200シード)\n");
console.log("  予測閾値(E育たず): edecay > N*p0*accum = 20*0.047*accum\n");
console.log("  accum   閾値予測   E_DECAY:  0.0   0.2   0.4   0.5   0.6   0.8   1.0   1.5");
for(const accum of [0.25,0.5,1.0]){
  const thr=20*0.047*accum;
  const cells=[0,0.2,0.4,0.5,0.6,0.8,1.0,1.5].map(edecay=>{
    const sums=SEEDS.map(sd=>runSim({mode:"A",lambda:0,N:20,backlash:1.0,benefit:3.5,accum,edecay},sd));
    return pct(sums.filter(s=>s.collapsed).length/sums.length).padStart(4);
  });
  console.log(`  ${fmt(accum).padStart(4)}    ${fmt(thr).padStart(5)}              ${cells.join("  ")}`);
}
console.log("\n  (各セル = 崩壊率)  → 崩壊率が 100%→0% へ落ちる E_DECAY が、ラチェット消失の転移点。");
console.log("    その転移点が accum に比例して動けば、§3-5「累積 vs 減衰の速度条件」が確認される。");
