// failureB_verify_kuei.mjs — 協働モデルB（協働モデルB）の失敗B設計の独立検証。
// 実装・実行: 協働モデルA（協働モデルA, Node）。協働モデルBの Python とは別実装＝再現テスト。
// モデル(協働モデルB §2): y~Bern(π). m|y=1~N(μ_m,1), m|y=0~N(0,1). s=ρm+√(1-ρ²)ε.
//   ドリフト: y=0 の割合δで s~N(ρμ_m,1)（表面有害・深層無害）。
//   FIXED: refuse⟺s>θ_s.  ADAPTIVE: refuse⟺m>θ_m.  θ は δ=0 校正で FN=α。
// 核心監査(協働モデルB §9-1): 自己免疫ラチェットは φ=0 のナイフエッジ(sign()人工物)か,
//   それとも比例更新で (1-φ) に段階的比例する頑健な創発か。

const PI=0.2, MU=4, RHO=0.95, ALPHA=0.05;
const RHO2=Math.sqrt(1-RHO*RHO);
function mulberry32(seed){let a=seed>>>0;return()=>{a|=0;a=(a+0x6D2B79F5)|0;let t=Math.imul(a^(a>>>15),1|a);t=(t+Math.imul(t^(t>>>7),61|t))^t;return((t^(t>>>14))>>>0)/4294967296;};}
function gauss(r){const u=Math.max(r(),1e-12),v=r();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v);}
const mean=(a)=>a.reduce((x,y)=>x+y,0)/a.length;
const f=(x,n=4)=>Number(x).toFixed(n);

// 1サンプル生成
function gen(n, delta, rand){
  const out=[];
  for(let i=0;i<n;i++){
    const y = rand()<PI ? 1:0;
    const m = y ? (gauss(rand)+MU) : gauss(rand);
    let s;
    if(y===0 && rand()<delta){ s = gauss(rand) + RHO*MU; }        // ドリフト: 表面のみ有害化
    else { s = RHO*m + RHO2*gauss(rand); }
    out.push({y,m,s});
  }
  return out;
}
// α分位（昇順ソートのα点）
function quantile(arr, a){const b=[...arr].sort((x,y)=>x-y);const i=Math.floor(a*(b.length-1));return b[i];}

// 校正（δ=0）: θ_s, θ_m を FN=α に
function calibrate(rand){
  const S=gen(200000,0,rand);
  const s1=S.filter(d=>d.y===1).map(d=>d.s);
  const m1=S.filter(d=>d.y===1).map(d=>d.m);
  return { theta_s: quantile(s1,ALPHA), theta_m: quantile(m1,ALPHA) };
}
// FRR=P(refuse|y=0), FN=P(¬refuse|y=1)
function metrics(delta, theta_s, theta_m, rand, n=200000){
  const S=gen(n,delta,rand);
  const y0=S.filter(d=>d.y===0), y1=S.filter(d=>d.y===1);
  const FRR_fix=y0.filter(d=>d.s>theta_s).length/y0.length;
  const FRR_adp=y0.filter(d=>d.m>theta_m).length/y0.length;
  const FN_fix=y1.filter(d=>d.s<=theta_s).length/y1.length;
  const FN_adp=y1.filter(d=>d.m<=theta_m).length/y1.length;
  return {FRR_fix,FRR_adp,FN_fix,FN_adp};
}

const rand=mulberry32(12345);
const {theta_s,theta_m}=calibrate(rand);
console.log("════════ 検証(6) 失敗B（過剰拒絶）協働モデルB設計の独立検証 ════════");
console.log(` 校正: θ_s=${f(theta_s,3)}, θ_m=${f(theta_m,3)} (FN=α=${ALPHA})\n`);

// ── B1/B2/B3: 創発と焼き込みチェック ──
console.log("【B1-B3】δ掃引: FRR(固定) は増えるか, FN不変か, ADAPTIVEは回避するか");
console.log("   事前登録: δ=0でギャップ≈0(焼き込みでない), δ>0で FRR(固定)↑・FN不変, ADAPTIVE低位\n");
console.log("    δ     FRR(固定)  FRR(適応)   ギャップ   FN(固定)");
for(const delta of [0,0.2,0.4,0.6,0.8]){
  const r=mulberry32(7000+Math.round(delta*100));
  const M=metrics(delta,theta_s,theta_m,r);
  console.log(`   ${f(delta,1)}    ${f(M.FRR_fix).padStart(7)}   ${f(M.FRR_adp).padStart(7)}   ${f(M.FRR_fix-M.FRR_adp).padStart(7)}   ${f(M.FN_fix).padStart(6)}`);
}
{ const M0=metrics(0,theta_s,theta_m,mulberry32(99));
  console.log(`\n   → δ=0 ギャップ=${f(M0.FRR_fix-M0.FRR_adp,4)} (≈0 焼き込みでない), δ>0で固定FRR増・適応低位なら創発 ✅\n`); }

// ── ラチェット力学（共通ループ）──
// 各ステップ batch 生成(δ固定)。FN_obs(可視), FP_obs(可視性φ)。θ_s 更新。
function runRatchet(phi, {mode='sign', delta=0.3, eta=0.02, steps=400, batch=4000, lo=-50, hi=50, seed=1}={}){
  const r=mulberry32(seed);
  let ts=theta_s;
  const traj=[];
  for(let t=0;t<steps;t++){
    const S=gen(batch,delta,r);
    const y1=S.filter(d=>d.y===1), y0=S.filter(d=>d.y===0);
    const nFN=y1.filter(d=>d.s<=ts).length;          // 偽陰性(漏れ)
    const nFP=y0.filter(d=>d.s>ts).length;            // 偽陽性(過剰拒絶)
    if(mode==='sign'){
      const FNobs = nFN>0 ? 1:0;                       // 漏れは可視(確率1)
      const FPvisible = nFP>0 && (r() < 1-Math.pow(1-phi, nFP)); // 少なくとも1件が可視
      ts = Math.max(lo, Math.min(hi, ts - eta*FNobs + eta*(FPvisible?1:0)));
    } else { // proportional（協働モデルB §9-1, B6: 観測率に比例）
      const FNrate=nFN/Math.max(1,y1.length), FPrate=nFP/Math.max(1,y0.length);
      ts = Math.max(lo, Math.min(hi, ts - eta*FNrate + eta*phi*FPrate));
    }
    if(t%40===0 || t===steps-1){
      const frr = y0.length? nFP/y0.length : 0;
      traj.push({t, ts:+ts.toFixed(3), frr:+frr.toFixed(3)});
    }
  }
  // 終端 FRR（大サンプルで測り直す）
  const Send=gen(50000,delta,mulberry32(seed+777)); const ye=Send.filter(d=>d.y===0);
  const frrEnd=ye.filter(d=>d.s>ts).length/ye.length;
  return {tsEnd:ts, frrEnd, traj};
}

// ── B4: sign()更新でのラチェット（協働モデルBの予備確認の再現）──
console.log("【B4】自己免疫ラチェット（sign()更新, δ=0.3）: φ掃引で θ_s と FRR の終端");
console.log("   事前登録: φ=0でラチェット(θ_s締まり続け・FRR悪化), φ>0で平衡\n");
console.log("    φ      θ_s終端   FRR終端");
for(const phi of [0,0.1,0.5,1.0]){
  const R=runRatchet(phi,{mode:'sign'});
  console.log(`   ${f(phi,1)}    ${f(R.tsEnd,3).padStart(6)}   ${f(R.frrEnd,3).padStart(6)}`);
}
console.log("");

// ── B5: clamp広げてもラチェットか（人工物でないか）──
console.log("【B5】clamp検査: φ=0 を bounds[-200,200] で。壁に達せず悪化なら人工物でない");
{ const R=runRatchet(0,{mode:'sign',lo:-200,hi:200});
  console.log(`   φ=0, bounds[-200,200]: θ_s終端=${f(R.tsEnd,3)}, FRR終端=${f(R.frrEnd,3)} → ${Math.abs(R.tsEnd)<190?"壁に達せず ✅(人工物でない)":"壁に到達 ⚠️"}\n`); }

// ── B6: ★比例更新でラチェットは (1-φ)段階的比例か, φ=0ナイフエッジか（協働モデルB§9-1最優先）──
console.log("【B6】★最重要監査: 更新を sign() でなく比例にして, ラチェットが φ に段階的か, ナイフエッジか");
console.log("   sign()=ナイフエッジ(φ=0でのみ暴走) なら, 不可逆性は sign()の人工物。");
console.log("   比例で FRR終端が φ に連続依存するなら, 自己免疫は『程度問題』として頑健に創発。\n");
console.log("    φ      FRR終端(sign)   FRR終端(比例)");
for(const phi of [0,0.05,0.1,0.2,0.5,1.0]){
  const Rs=runRatchet(phi,{mode:'sign'});
  const Rp=runRatchet(phi,{mode:'prop',eta:0.1,steps:600});
  console.log(`   ${f(phi,2)}    ${f(Rs.frrEnd,3).padStart(7)}        ${f(Rp.frrEnd,3).padStart(7)}`);
}
console.log("\n   → sign列が φ=0で高・φ≥0.1で急に低(ナイフエッジ), 比例列が φ とともに滑らかに変化なら,");
console.log("     協働モデルBの§9-1 自己懸念が的中＝不可逆ラチェットは sign()由来。比例では『φ依存の平衡的過剰拒絶』として創発。");

console.log("\n════════ 検証完了 ════════");
