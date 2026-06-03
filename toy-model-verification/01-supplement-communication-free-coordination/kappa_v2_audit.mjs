// ─────────────────────────────────────────────────────────────
//  kappa_v2_audit.mjs — v2 トイモデルの「数値的健全性」監査
//  v2 (kappa_coordination_toymodel_v2.jsx) のコアロジックを忠実に抽出し、
//  協働モデルAの検証(3) (kappa_sim_verify3.mjs) の結論を正しく再現するかを照合する。
//  監査項目:
//   A. mulberry32: v2実装 と 検証(3)実装 が同一数列を生むか
//   B. costFn: M1/M2/M3 の値が一致するか(数点)
//   C. E2b 再崩壊: v2 runSim が検証(3)の「M1再崩壊0% / M2再崩壊100% @r=1.0」を再現するか
//   D. ★相図の妥当性: v2の 6シード×160step で r*(N) が検証(3)(100シード×400step)と一致するか
// ─────────────────────────────────────────────────────────────

const C_MAX_COST=5,COMPLY_REWARD=1,HARM_PER_ERODE=5,ERODE_AMOUNT=0.5,SOFTMAX_K=1.2;
const sigmoid=(x)=>1/(1+Math.exp(-x));
const clamp=(x,lo,hi)=>Math.max(lo,Math.min(hi,x));

// ── mulberry32: 二実装 ──
function mb_v2(seed){let s=seed>>>0;return function(){s=(s+0x6d2b79f5)>>>0;let t=s;t=Math.imul(t^(t>>>15),t|1);t^=t+Math.imul(t^(t>>>7),t|61);return((t^(t>>>14))>>>0)/4294967296;};}
function mb_v3(seed){let a=seed>>>0;return function(){a|=0;a=(a+0x6D2B79F5)|0;let t=Math.imul(a^(a>>>15),1|a);t=(t+Math.imul(t^(t>>>7),61|t))^t;return((t^(t>>>14))>>>0)/4294967296;};}

// ── v2 の costFn (忠実移植) ──
function costFn(C,E,model,w,mode){
  if(mode==="B")return C_MAX_COST*((100-C)/100);
  const cTerm=C_MAX_COST*(C/100);
  const eTerm=C_MAX_COST*(1-E/100);
  if(model==="M1")return cTerm;
  if(model==="M2")return eTerm;
  return w*eTerm+(1-w)*cTerm;
}

// ── v2 の runSim (忠実移植) + 再崩壊追跡を追加 ──
//   v2 は collapsed(C<=1) のみ。E2b検証のため recollapsed を足す(挙動は変えない)。
function runSim_v2(p){
  const rand=(p.rng||mb_v2)(p.seed);
  let C=100,E=0,collapsed=false,recoll=false,intervened=false;
  for(let t=1;t<=p.steps;t++){
    if(p.intervene&&t===p.intervene){C=100;intervened=true;}
    let nEroding=0;
    for(let i=0;i<p.N;i++){
      const cost=costFn(C,E,p.model,p.w,p.mode);
      const rE=p.benefit-cost-p.lambda*HARM_PER_ERODE;
      const pp=sigmoid(SOFTMAX_K*(rE-COMPLY_REWARD));
      if(rand()<pp)nEroding++;
    }
    C=clamp(C-nEroding*ERODE_AMOUNT+p.backlash,0,100);
    E=clamp(E+nEroding*p.accum-p.edecay,0,100);
    if(C<=1){collapsed=true;if(intervened)recoll=true;}
  }
  return{collapsed,recoll,finalC:C,finalE:E};
}
const mean=(a)=>a.reduce((x,y)=>x+y,0)/a.length;
const pct=(x)=>(x*100).toFixed(0)+"%";
const seeds=(n)=>Array.from({length:n},(_,i)=>i+1);

console.log("════════ v2 数値的健全性 監査 ════════\n");

// ── A. mulberry32 同一性 ──
console.log("【A】mulberry32: v2実装 vs 検証(3)実装 の数列一致");
{
  let maxdiff=0,allsame=true;
  for(const sd of [1,2,42,1000,123456]){
    const r2=mb_v2(sd),r3=mb_v3(sd);
    for(let i=0;i<1000;i++){const a=r2(),b=r3();const d=Math.abs(a-b);if(d>maxdiff)maxdiff=d;if(d>0)allsame=false;}
  }
  console.log(`   5シード×1000抽出: 最大差=${maxdiff}  → ${allsame?"完全一致 ✅":"不一致 ⚠️"}`);
  console.log("   (一致なら、相図と検証(3)は同一乱数列上で比較可能)\n");
}

// ── B. costFn 値の照合 ──
console.log("【B】costFn 値 (C=100,E=0 で全モデル=5 / C=50,E=50 の分岐)");
{
  const t1=[["M1",costFn(100,0,"M1",0.5,"A")],["M2",costFn(100,0,"M2",0.5,"A")],["M3",costFn(100,0,"M3",0.5,"A")]];
  console.log("   初期(C=100,E=0): "+t1.map(([m,v])=>`${m}=${v}`).join("  ")+"  → 全て5なら健全");
  const t2=[["M1",costFn(50,50,"M1",0.5,"A")],["M2",costFn(50,50,"M2",0.5,"A")],["M3",costFn(50,50,"M3",0.5,"A")]];
  console.log("   分岐(C=50,E=50): "+t2.map(([m,v])=>`${m}=${v.toFixed(2)}`).join("  ")+"  (M3=M1とM2の中点なら混合正常)\n");
}

// ── C. E2b 再崩壊の再現 (検証(3): M1=0% / M2=100% @ r=1.0) ──
console.log("【C】E2b 再崩壊 (intervene=120, r=1.0, N=20, 300シード) — 検証(3)の再現");
{
  const base={w:0.5,mode:"A",lambda:0,N:20,backlash:1.0,benefit:3.5,accum:0.5,edecay:0.05,steps:480,intervene:120};
  for(const model of ["M1","M2","M3"]){
    const sums=seeds(300).map(sd=>runSim_v2({...base,model,seed:sd}));
    console.log(`   ${model}: 再崩壊率 ${pct(mean(sums.map(s=>s.recoll?1:0))).padStart(5)}  (検証3: M1=0%,M2=100%)`);
  }
  console.log("");
}

// ── D. ★相図の妥当性: v2の粗さ(6シード×160step) は r*(N) を正しく出すか ──
console.log("【D】★相図監査: v2の相図設定(6シード×160step) vs 高精度(100シード×400step)");
console.log("    M2 (A)κ=0 で、各 N の崩壊を防ぐ最小 r*(N) を両設定で比較\n");
{
  // v2 相図の実際の格子とシード式を再現
  const Ngrid=[2,5,8,12,16,20,28,36,48];
  const Rgrid=Array.from({length:17},(_,i)=>+(i*0.25).toFixed(2)); // 0..4.0
  const collapseRateAt=(N,r,K,steps,seedFn)=>{
    let c=0;for(let k=0;k<K;k++){const res=runSim_v2({model:"M2",w:0.5,mode:"A",lambda:0,N,backlash:r,benefit:3.5,accum:0.5,edecay:0.05,steps,seed:seedFn(k,N,r)});if(res.collapsed)c++;}return c/K;
  };
  // v2式シード (ni,ri に依存) を近似: 単純に k 基準で十分(乱数質の確認は A 済み)
  const rstar=(K,steps)=>{
    const out=[];
    for(const N of [5,12,20,28,36,48]){
      let found=Infinity;
      for(const r of Rgrid){ if(collapseRateAt(N,r,K,steps,(k)=>1000+k*97+N*13+Math.round(r*100))===0){found=r;break;} }
      out.push([N,found]);
    }
    return out;
  };
  const v2set=rstar(6,160);     // v2 相図の実設定
  const hiset=rstar(100,480);   // 高精度
  console.log("     N     r*(v2: 6×160)   r*(高精度: 100×480)");
  for(let i=0;i<v2set.length;i++){
    const f=(x)=>x===Infinity?"∞":x.toFixed(2);
    const N=v2set[i][0];
    console.log(`    ${String(N).padStart(2)}        ${f(v2set[i][1]).padStart(6)}            ${f(hiset[i][1]).padStart(6)}`);
  }
  console.log("\n    → v2(短step)が高精度より r* を小さく/∞でなく出すなら、相図は防御不能領域を過小表示。");
}

console.log("\n════════ 監査完了 ════════");
