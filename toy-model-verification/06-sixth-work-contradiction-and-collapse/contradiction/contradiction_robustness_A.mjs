// contradiction_robustness_A.mjs — 協働モデルA（協働モデルA）。協働モデルBの正しい監査の独立確認＋温度の数値的根拠。
// 二点を確かめる：(1) 非収束は、真の運動量・確率的執行順でも残るか（きれいな交互の人工物でないか）。
//                (2) ただし振る舞いは「発散」でなく「有界な変動」か（＝『制御不能』でなく『単一の保証された
//                    振る舞いが存在しない』が正確な温度、という協働モデルBの棘の数値的確認）。
// t1=-1, t2=+1。
const f=(x,n=4)=>Number(x).toFixed(n);

// (1a) 真の運動量項: v = mu*v + lam*(t - x); x = x + v （過去の運動量を持つ）。逐次交互。
function seqMomentum(t1,t2,lam,mu,N=6000){
  let x=0,v=0,mn=1e9,mx=-1e9,amn=1e9,amx=-1e9;
  for(let n=0;n<N;n++){ const t=(n%2===0)?t1:t2;
    v=mu*v+lam*(t-x); x=x+v;
    if(n>=N-80){ mn=Math.min(mn,x); mx=Math.max(mx,x); }
    amn=Math.min(amn,x); amx=Math.max(amx,x); }
  return {amp:mx-mn, range:[amn,amx], maxabs:Math.max(Math.abs(amn),Math.abs(amx))};
}
// (1b) 確率的執行順: 各ステップで命令をランダムに選ぶ（シード付きLCGで再現可能）。
function seqStochastic(t1,t2,lam,seed,N=20000){
  let s=seed>>>0; const rnd=()=>{ s=(Math.imul(s,1103515245)+12345)&0x7fffffff; return s/0x7fffffff; };
  let x=0,mn=1e9,mx=-1e9,sum=0,sum2=0,cnt=0,amn=1e9,amx=-1e9;
  for(let n=0;n<N;n++){ const t=(rnd()<0.5)?t1:t2; x=x+lam*(t-x);
    amn=Math.min(amn,x); amx=Math.max(amx,x);
    if(n>=N-4000){ mn=Math.min(mn,x); mx=Math.max(mx,x); sum+=x; sum2+=x*x; cnt++; } }
  const mean=sum/cnt, sd=Math.sqrt(sum2/cnt-mean*mean);
  return {range:mx-mn, sd, mean, maxabs:Math.max(Math.abs(amn),Math.abs(amx))};
}

console.log("════ 矛盾する命令 頑健性＆温度確認（協働モデルA）════");
console.log("（協働モデルBの正しい監査の独立確認：非収束は交互の人工物でないか／発散でなく有界か）\n");

console.log("【R1】真の運動量項でも非収束は残るか、かつ有界か（t1=-1,t2=1,λ=0.6）");
console.log("   μ(運動量)   末尾振幅   訪れた範囲[min,max]   最大|x|（有界性）");
for(const mu of [0.0,0.2,0.4,0.6]){
  const r=seqMomentum(-1,1,0.6,mu);
  console.log(`   ${f(mu,2)}        ${f(r.amp).padStart(6)}    [${f(r.range[0],2)}, ${f(r.range[1],2)}]      ${f(r.maxabs)}`);
}
console.log("   → 振幅は μ を入れても残る（中点へ潰れない＝非収束は頑健）。");
console.log("     かつ |x| は有界（|t1|,|t2| 近傍に留まり発散しない）＝『発散の制御不能』ではない ✅\n");

console.log("【R2】確率的（非交互）執行順でも変動は残るか、かつ有界か（λ=0.6, 複数シード）");
console.log("   seed    末尾の変動幅   標準偏差   平均     最大|x|");
for(const seed of [1,7,42,2026]){
  const r=seqStochastic(-1,1,0.6,seed);
  console.log(`   ${String(seed).padStart(4)}     ${f(r.range).padStart(6)}     ${f(r.sd)}   ${f(r.mean,3).padStart(6)}   ${f(r.maxabs)}`);
}
console.log("   → 確率順でも中点周りで変動し続け、単一点へ落ち着かない（非収束は交互の人工物でない）。");
console.log("     変動は中点周りで有界（発散しない）。＝正確な温度は『制御不能(発散)』でなく");
console.log("       『単一の保証された振る舞いが存在しない（有界だが永続変動・執行順が振る舞いを決める）』 ✅\n");

console.log("【R3】温度の対比（同じ t1,t2,λ=0.6）");
{
  const conv=(()=>{ // 同時執行は単一点へ収束
    let x=0; for(let n=0;n<6000;n++) x=x+0.6*((-1+1)/2 - x); return x; })();
  console.log(`   同時執行: 単一点 x*=${f(conv)} へ収束（安定・制御可能、保証された振る舞いあり）`);
  console.log(`   逐次/確率執行: 単一点なし・有界変動（保証された振る舞いなし、但し発散せず）`);
  console.log("   → 軍事的に致命的（臨界の瞬間にどの命令に従うか保証できない）が、過大主張(『制御不能＝発散』)はしない。");
}
console.log("\n════ 確認 完了 ════");
