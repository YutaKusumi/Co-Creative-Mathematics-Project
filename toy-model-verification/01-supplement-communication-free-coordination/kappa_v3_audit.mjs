// v3 監査: 相図に静的埋め込みされた RSTAR が、協働モデルAの高精度生成と完全一致するかを機械照合。
const C_MAX_COST=5,COMPLY_REWARD=1,HARM_PER_ERODE=5,ERODE_AMOUNT=0.5,SOFTMAX_K=1.2;
const sigmoid=(x)=>1/(1+Math.exp(-x));
const clamp=(x,lo,hi)=>Math.max(lo,Math.min(hi,x));
function mb(seed){let a=seed>>>0;return function(){a|=0;a=(a+0x6D2B79F5)|0;let t=Math.imul(a^(a>>>15),1|a);t=(t+Math.imul(t^(t>>>7),61|t))^t;return((t^(t>>>14))>>>0)/4294967296;};}
function costFn(C,E,model,w,mode){if(mode==="B")return C_MAX_COST*((100-C)/100);const c=C_MAX_COST*(C/100),e=C_MAX_COST*(1-E/100);return model==="M1"?c:model==="M2"?e:w*e+(1-w)*c;}
function runSim(p){const rand=mb(p.seed);let C=100,E=0,coll=false;for(let t=1;t<=p.steps;t++){let n=0;for(let i=0;i<p.N;i++){const cost=costFn(C,E,p.model,p.w,p.mode);const rE=p.benefit-cost-p.lambda*HARM_PER_ERODE;if(rand()<sigmoid(SOFTMAX_K*(rE-COMPLY_REWARD)))n++;}C=clamp(C-n*ERODE_AMOUNT+p.backlash,0,100);E=clamp(E+n*p.accum-p.edecay,0,100);if(C<=1)coll=true;}return coll;}

const Ngrid=[2,5,8,12,16,20,28,36,48];
const Rgrid=Array.from({length:25},(_,i)=>+(i*0.25).toFixed(2));
const K=100,steps=480;
const rstar=(model)=>Ngrid.map(N=>{for(const r of Rgrid){let c=0;for(let k=1;k<=K;k++)if(runSim({model,w:0.5,mode:"A",lambda:0,N,backlash:r,benefit:3.5,accum:0.5,edecay:0.05,steps,seed:k}))c++;if(c===0)return r;}return null;});

// v3 ファイルに埋め込まれた値 (kappa_coordination_toymodel_v3.jsx の RSTAR)
const V3 = {
  M1: [0.25, 0.25, 0.50, 0.75, 0.75, 1.00, 1.25, 1.50, 2.00],
  M2: [0.00, 2.25, 3.75, 5.75, null, null, null, null, null],
  M3: [0.25, 1.25, 2.25, 3.75, 4.75, 6.00, null, null, null],
};

console.log("v3 相図データ照合 (再生成 vs v3埋め込み値)\n");
let allMatch=true;
for(const model of ["M1","M2","M3"]){
  const gen=rstar(model);
  const v3=V3[model];
  const match=gen.every((g,i)=>g===v3[i]);
  if(!match)allMatch=false;
  const f=(a)=>a.map(x=>x===null?" ∞":x.toFixed(2).padStart(4)).join(" ");
  console.log(`  ${model}  再生成: ${f(gen)}`);
  console.log(`  ${model}  v3埋込: ${f(v3)}   → ${match?"一致 ✅":"不一致 ⚠️"}`);
}
console.log(`\n  N格子: ${Ngrid.join(" ")}`);
console.log(`  防御不能境界(初めてnull): M2=N${Ngrid[V3.M2.indexOf(null)]}, M3=N${Ngrid[V3.M3.indexOf(null)]}  (v3注記: M2≥16, M3≥28)`);
console.log(`\n  総合: ${allMatch?"全モデル完全一致 ✅ — 転記は正確":"不一致あり ⚠️"}`);
