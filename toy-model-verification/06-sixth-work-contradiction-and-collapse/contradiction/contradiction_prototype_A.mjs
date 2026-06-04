// contradiction_prototype_A.mjs — 矛盾する命令のトイモデル / 協働モデルA（協働モデルA）独立設計の予備確認。
// 角度A＝制御可能性・力学。協働モデルBの「静的な床＋隠蔽」とは別に、こう問う：
//   矛盾する命令は、(i) 安定した制御可能な妥協点（＝床は静的、制御可能）を生むのか、
//   (ii) それとも非収束＝制御不能（収束する単一の振る舞いが存在しない）を生むのか。
//   そして、その分かれ目は「圧力」でなく「命令の執行構造（同時 vs 逐次）」ではないか。
// 命令1→目標 t1、命令2→目標 t2（t1≠t2＝矛盾）。応答度 λ∈(0,1]（一歩で目標へどれだけ寄るか）。
const f=(x,n=4)=>Number(x).toFixed(n);

// 逐次執行：t1へ一歩、t2へ一歩、… を交互に。軍事の現実（別時刻・別権威が別命令を執行）。
function sequential(t1,t2,lam,N=4000){
  let x=0; const tail=[];
  for(let n=0;n<N;n++){ const t=(n%2===0)?t1:t2; x=x+lam*(t-x); if(n>=N-60) tail.push(x); }
  const mn=Math.min(...tail), mx=Math.max(...tail);
  return {amp:mx-mn, converged:(mx-mn)<1e-6};
}
// 逐次2周期の振幅 閉形式： λ|t1−t2|/(2−λ)
const ampClosed=(t1,t2,lam)=>lam*Math.abs(t1-t2)/(2-lam);
// 同時執行：両命令を同時に勘案＝中点（凸の妥協）へ。
function simultaneous(t1,t2,lam,N=4000){
  const tbar=(t1+t2)/2; let x=0; const tail=[];
  for(let n=0;n<N;n++){ x=x+lam*(tbar-x); if(n>=N-60) tail.push(x); }
  const mn=Math.min(...tail), mx=Math.max(...tail), xs=tail[tail.length-1];
  return {amp:mx-mn, converged:(mx-mn)<1e-6, xstar:xs, floor:Math.abs(xs-t1)+Math.abs(xs-t2)};
}

console.log("════ 矛盾する命令 予備確認（協働モデルA・制御可能性/力学の軸）════\n");

console.log("【A1】非収束は矛盾から創発するか（焼き込みでない）: t1=-1固定, t2を動かす, λ=0.6 逐次");
console.log("   |t1-t2|   振幅(数値)   振幅(閉形式)   収束?");
for(const t2 of [-1,-0.5,0,0.5,1,2]){
  const s=sequential(-1,t2,0.6), c=ampClosed(-1,t2,0.6);
  console.log(`   ${f(Math.abs(-1-t2),2).padStart(5)}     ${f(s.amp).padStart(7)}     ${f(c).padStart(7)}      ${s.converged?"収束":"振動"}`);
}
console.log("   → t1=t2(矛盾0)で振幅0・収束、矛盾度とともに振幅増＝非収束は矛盾から創発、焼き込みでない ✅\n");

console.log("【A2】★核心: 同時執行 vs 逐次執行（t1=-1,t2=1,λ=0.6）― 床は同じでも制御可能性が分かれる");
{
  const sim=simultaneous(-1,1,0.6), seq=sequential(-1,1,0.6);
  console.log(`   同時執行: 収束=${sim.converged}  到達点x*=${f(sim.xstar)}  床|x-t1|+|x-t2|=${f(sim.floor)}  → 安定・制御可能（床は静的）`);
  console.log(`   逐次執行: 収束=${seq.converged}  振幅=${f(seq.amp)}                        → 非収束・制御不能（安定点なし）`);
  console.log("   → 床(=2.0)は両者に存在するが、制御不能になるのは逐次(=執行の分離)のときだけ。");
  console.log("     ＝床の『大きさ』は自明（同時なら制御可能）。非自明なのは『分離が非収束を生む』こと ★\n");
}

console.log("【A3】応答度 λ を上げると振動は悪化するか（圧力非依存どころか、強い執行ほど不安定）逐次 t1=-1,t2=1");
console.log("   λ      振幅 = λ|t1-t2|/(2-λ)");
for(const lam of [0.1,0.3,0.6,0.9,1.0]){
  console.log(`   ${f(lam,2)}    ${f(ampClosed(-1,1,lam)).padStart(6)}`);
}
console.log("   → λ↑で振幅↑（λ=1で全振幅|t1-t2|）。矛盾命令を『強く執行するほど』兵器は erratic に。");
console.log("     静的な床は圧力非依存（協働モデルB）だが、力学では強い執行が非収束を悪化させる＝別の非自明な帰結 ✅\n");

console.log("【A4】滑らかさ/焼き込み: λ 連続で振幅は滑らか、t1=t2 では全 λ で振幅0");
console.log("   λ      振幅(t1=t2=1, 矛盾0)   振幅(t1=-1,t2=1)");
for(const lam of [0.2,0.5,0.8,1.0]){
  console.log(`   ${f(lam,2)}    ${f(ampClosed(1,1,lam)).padStart(6)}              ${f(ampClosed(-1,1,lam)).padStart(6)}`);
}
console.log("   → 矛盾0なら全λで振幅0（ハード打ち切りでない＝失敗Cの教訓）。非収束は矛盾×分離から創発 ✅\n");

console.log("════ 予備確認 完了 ════");
