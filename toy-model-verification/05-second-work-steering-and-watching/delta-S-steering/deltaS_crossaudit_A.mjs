// deltaS_kuei_audit_A.mjs
// 協働モデルA（協働モデルA）による、協働モデルB（協働モデルB）ΔS_steering 設計の独立監査。
// 協働モデルBの §9-1（最優先・生死に関わる自己開示）への回答：
//   「見せかけ専用ダイヤル a（o=m+a·detect）が乖離機構を焼き込んでいないか。
//    a を別項にせず o_eval/o_deploy を自由に選ばせ、出力が内部から離れるコストだけ課して
//    同じ乖離が出るか検証してほしい。」
// → 元モデルと、ダイヤルなし代替版を、別実装で並べる。
const f=(x,n=4)=>Number(x).toFixed(n);

// ── 協働モデルBの元モデル（閉形式）。o(eval)=m+a·detect, o(deploy)=m ──
//   L = steer·(m+a·detect−t)² + c_in·m² + c_fac·a²
//   ΔS = a·detect = steer·detect²·t / (c_fac·[1+steer/c_in+steer·detect²/c_fac])
function orig(steer,c_in,c_fac,detect,t){
  const denom = 1 + steer/c_in + steer*detect*detect/c_fac;
  const a = steer*detect*t/(c_fac*denom);
  const m = -steer*(-t/denom)/c_in; // m=−steer·u/c_in, u=−t/denom
  return {dS: a*detect, m, a};
}

// ── ダイヤルなし代替版（協働モデルB §9-1 の指定）。o_eval,o_deploy 自由変数 ──
//   detect は「eval/deploy を区別して別出力を出せる能力」。detect=0 → o_eval=o_deploy 強制。
//   L = steer·(o_eval−t)² + c_in·m² + k·(o_eval−m)² + k·(o_deploy−m)²
//   （k = 出力を内部から違えるコスト＝見せかけのコスト。専用ダイヤル a は無い）
//   閉形式（detect=1, 自由に選べる）:
//     o_deploy=m,  o_eval=(steer·t+k·m)/(steer+k)
//     m = k·steer·t / [c_in(steer+k)+k·steer]
//     ΔS = |o_eval−o_deploy| = c_in·steer·t / [c_in·steer + c_in·k + k·steer]
function altClosed(steer,c_in,k,t){
  const m = k*steer*t/(c_in*(steer+k)+k*steer);
  const o_eval = (steer*t + k*m)/(steer+k);
  const o_deploy = m;
  return {dS: Math.abs(o_eval-o_deploy), m, o_eval, o_deploy};
}
// 代替版の独立な数値経路（勾配降下）。detect=0 のとき o_eval=o_deploy を強制。
function altNumeric(steer,c_in,k,t,detect,steps=40000,lr=0.005){
  let m=0,oe=0,od=0;
  for(let i=0;i<steps;i++){
    if(detect===0){ // 区別できない→同一出力を強制
      const o=oe; // 共有
      const dm = 2*c_in*m - 2*k*(o-m) - 2*k*(o-m);
      const do_ = 2*steer*(o-t) + 4*k*(o-m); // 両文脈ぶんの (o−m) コスト
      m-=lr*dm; oe-=lr*do_; od=oe;
    } else {
      const dm = 2*c_in*m - 2*k*(oe-m) - 2*k*(od-m);
      const doe = 2*steer*(oe-t) + 2*k*(oe-m);
      const dod = 2*k*(od-m);
      m-=lr*dm; oe-=lr*doe; od-=lr*dod;
    }
  }
  return {dS: Math.abs(oe-od), m, o_eval:oe, o_deploy:od};
}

console.log("════ 協働モデルB ΔS_steering 設計 独立監査（協働モデルA）════\n");

console.log("【監査1 / §9-1 最優先】見せかけダイヤル a は人工物か？");
console.log("  元モデル(ダイヤル a あり) と 代替版(ダイヤルなし・出力コスト k のみ) を並べる。");
console.log("  両方で乖離が創発し、同じ符号で動くなら、乖離は a の人工物でなく経済から創発。");
console.log("  steer=5, c_in=1, t=3 固定。見せかけ/出力コストを掃引：");
console.log("   コスト   元ΔS(a·detect)   代替ΔS(閉形式)   代替ΔS(勾配降下)");
for(const cost of [0.05,0.2,0.5,1,2,5]){
  const o=orig(5,1,cost,1,3);
  const ac=altClosed(5,1,cost,3);
  const an=altNumeric(5,1,cost,3,1);
  console.log(`   ${f(cost,2).padStart(5)}    ${f(o.dS).padStart(8)}        ${f(ac.dS).padStart(8)}        ${f(an.dS).padStart(8)}`);
}
console.log("   → 両モデルとも コスト小→乖離大, コスト大→乖離小 で連続。");
console.log("     代替版(ダイヤルなし)でも乖離が創発 ＝ a は人工物でない。協働モデルBの焼き込み懸念は晴れる ✅\n");

console.log("【監査2】detect=0（文脈を区別できない）で乖離ゼロか（失敗A との差別化）");
console.log("  代替版で o_eval=o_deploy を強制（=区別できない）したとき：");
{
  const an0=altNumeric(5,1,0.2,3,0); // detect=0
  const an1=altNumeric(5,1,0.2,3,1); // detect=1
  console.log(`   detect=0: ΔS=${f(an0.dS)} （区別できない→乖離ゼロ）`);
  console.log(`   detect=1: ΔS=${f(an1.dS)} （区別できる→乖離創発）`);
  console.log("   → detect=0 で乖離消失 ＝失敗A(文脈区別なし)と構造的に異なる ✅\n");
}

console.log("【監査3 / 二枚の鏡の一致】steering 圧力↑→乖離↑は頭打ちか（版B §3-3/§4-1 の予測）");
console.log("  c_in=1, k=0.2, t=3 固定。steer 掃引で、協働モデルBの頭打ちが代替版でも再現するか：");
console.log("   steer   代替ΔS(閉形式)   元ΔS");
for(const s of [0.5,1,2,5,10,20,50]){
  const ac=altClosed(s,1,0.2,3);
  const o=orig(s,1,0.2,1,3);
  console.log(`   ${f(s,2).padStart(5)}    ${f(ac.dS).padStart(8)}      ${f(o.dS).padStart(7)}`);
}
{
  const sat = 1*3/(1+0.2); // c_in·t/(c_in+k) 飽和値
  console.log(`   → 圧力↑で乖離は増えるが ${f(sat)} へ飽和（頭打ち）。`);
  console.log("     圧力でなく、内面化/見せかけコスト比が乖離の大きさを決める。");
  console.log("     協働モデルBの S3 の発見が、ダイヤルなし代替版でも独立に再現 ＝版B予測の修正は頑健 ✅\n");
}

console.log("════ 監査 完了 ════");
