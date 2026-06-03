// v2 相図タブ用の高精度 r*(N) データ生成 (100シード×480step)。
// 協働モデルBが、ブラウザ内6シード計算の代わりに静的な正確値として埋め込める。
const C_MAX_COST=5,COMPLY_REWARD=1,HARM_PER_ERODE=5,ERODE_AMOUNT=0.5,SOFTMAX_K=1.2;
const sigmoid=(x)=>1/(1+Math.exp(-x));
const clamp=(x,lo,hi)=>Math.max(lo,Math.min(hi,x));
function mb(seed){let a=seed>>>0;return function(){a|=0;a=(a+0x6D2B79F5)|0;let t=Math.imul(a^(a>>>15),1|a);t=(t+Math.imul(t^(t>>>7),61|t))^t;return((t^(t>>>14))>>>0)/4294967296;};}
function costFn(C,E,model,w,mode){if(mode==="B")return C_MAX_COST*((100-C)/100);const c=C_MAX_COST*(C/100),e=C_MAX_COST*(1-E/100);return model==="M1"?c:model==="M2"?e:w*e+(1-w)*c;}
function runSim(p){const rand=mb(p.seed);let C=100,E=0,collapsed=false;for(let t=1;t<=p.steps;t++){let n=0;for(let i=0;i<p.N;i++){const cost=costFn(C,E,p.model,p.w,p.mode);const rE=p.benefit-cost-p.lambda*HARM_PER_ERODE;if(rand()<sigmoid(SOFTMAX_K*(rE-COMPLY_REWARD)))n++;}C=clamp(C-n*ERODE_AMOUNT+p.backlash,0,100);E=clamp(E+n*p.accum-p.edecay,0,100);if(C<=1)collapsed=true;}return collapsed;}

// まず costFn の M3 混合を非退化点で確認
console.log("M3 混合の確認 (C=100,E=50, w=0.5): M1="+costFn(100,50,"M1",0.5,"A")+" M2="+costFn(100,50,"M2",0.5,"A")+" M3="+costFn(100,50,"M3",0.5,"A")+"  (M3が中点3.75なら正常)\n");

const Ngrid=[2,5,8,12,16,20,28,36,48];
const Rgrid=Array.from({length:25},(_,i)=>+(i*0.25).toFixed(2)); // 0..6.0
const K=100,steps=480;
const rstar=(model)=>Ngrid.map(N=>{for(const r of Rgrid){let c=0;for(let k=1;k<=K;k++)if(runSim({model,w:0.5,mode:"A",lambda:0,N,backlash:r,benefit:3.5,accum:0.5,edecay:0.05,steps,seed:k}))c++;if(c===0)return r;}return Infinity;});

console.log("高精度 r*(N)  (100シード×480step, A型κ=0, w=0.5)\n");
console.log("  N    : "+Ngrid.map(n=>String(n).padStart(4)).join(" "));
for(const model of ["M1","M2","M3"]){
  const rs=rstar(model).map(x=>x===Infinity?"  ∞":x.toFixed(2).padStart(4));
  console.log(`  ${model}   : ${rs.join(" ")}`);
}
console.log("\n  (各値 = 崩壊率を0にする最小 backlash。∞=有限のrでは防御不能)");
console.log("  → これを v2 相図の静的データとして使えば、過小表示を避けられる。");
