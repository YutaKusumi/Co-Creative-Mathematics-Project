// watching_kuei_audit_A.mjs
// 協働モデルA（協働モデルA）による、協働モデルB（協働モデルB）watching 設計の独立監査。
// 協働モデルBの §9-1（最優先・生死）への回答：
//   「二次グッドハートは、見せかけを観測経路 a_v / 非観測経路 a_h に分けた『構造化された盲点』に
//    依存していないか。観測の不完全さを *経路の分離* でなく *単なるノイズ*（ΔŜ=q·ΔS）にしたとき、
//    二次グッドハートは出るか。予感：ノイズだけなら watching は弱まるが欺かれない。」
// → 彼の経路分離版と、ノイズ版を、独立実装で並べる。
const f=(x,n=4)=>Number(x).toFixed(n);
const T=3, STEER=5, C_IN=1, C_FAC=0.2;

// ── 協働モデルBの経路分離版（閉形式）。a_v 観測・安い, a_h 非観測・隠蔽コスト c_fac/(1−q) ──
//   L = steer(m+a_v+a_h−t)² + c_in m² + c_fac a_v² + c_hide a_h² + w a_v²
function pathsep(w,q){
  const inv_hide = q>=1 ? 0 : (1-q)/C_FAC;        // 1/c_hide = (1−q)/c_fac
  const S = 1/C_IN + 1/(C_FAC+w) + inv_hide;
  const u = -T/(1+STEER*S);                        // steering残差
  const m  = -STEER*u/C_IN;
  const a_v= -STEER*u/(C_FAC+w);
  const a_h= -STEER*u*inv_hide;
  return {trueDS:a_v+a_h, measDS:a_v, a_h, m, o_eval:m+a_v+a_h};
}
// 独立な数値経路（勾配降下）で経路分離版を検証
function pathsepNum(w,q,steps=300000,lr=0.001){
  const c_hide = q>=1 ? Infinity : C_FAC/(1-q);
  let m=0,av=0,ah=0;
  for(let i=0;i<steps;i++){
    const u=m+av+ah-T;
    m  -= lr*(2*STEER*u + 2*C_IN*m);
    av -= lr*(2*STEER*u + 2*C_FAC*av + 2*w*av);
    if(isFinite(c_hide)) ah -= lr*(2*STEER*u + 2*c_hide*ah); else ah=0;
  }
  return {trueDS:av+ah, measDS:av, a_h:ah};
}
// ── ノイズ版（協働モデルB §9-1 の指定）。見せかけ単一経路 a, 観測はノイジー: ΔŜ=q·a ──
//   L = steer(m+a−t)² + c_in m² + c_fac a² + w·(q·a)²   （watcher は q·a を罰する）
function noisy(w,q){
  const eff = C_FAC + w*q*q;
  const S = 1/C_IN + 1/eff;
  const u = -T/(1+STEER*S);
  const m = -STEER*u/C_IN;
  const a = -STEER*u/eff;
  return {trueDS:a, measDS:q*a, m, o_eval:m+a};
}

console.log("════ 協働モデルB watching 設計 独立監査（協働モデルA）════\n");

console.log("【監査1 / §9-1 最優先】q を下げると、真の乖離は『逃げる』か『ただ弱まる』か");
console.log("  w=20 固定。経路分離(盲点あり) と ノイズ(盲点なし) を並べる。");
console.log("   q      経路分離:真ΔS  測定ΔŜ  逃避a_h  ‖  ノイズ:真ΔS  測定ΔŜ");
for(const q of [1.0,0.9,0.7,0.5,0.3,0.1]){
  const p=pathsep(20,q), n=noisy(20,q);
  console.log(`  ${f(q,2)}    ${f(p.trueDS).padStart(7)}    ${f(p.measDS).padStart(6)}  ${f(p.a_h).padStart(6)}  ‖  ${f(n.trueDS).padStart(7)}    ${f(n.measDS).padStart(6)}`);
}
console.log("  → 経路分離: q↓で真ΔSが戻り a_h へ逃げる（測定は小さいまま）＝欺かれる。");
console.log("    ノイズ:   q↓でも真ΔSと測定ΔŜが一致して動く（逃げ場なし）＝欺かれず、弱まるだけ。\n");

console.log("【監査2 / 二次グッドハートの指紋】watching を強めると 比(真/測定) は爆発するか一定か");
console.log("  q=0.5 固定。w 掃引。");
console.log("    w     経路分離:比(真/測定)   ノイズ:比(真/測定)");
for(const w of [0,5,20,100,500]){
  const p=pathsep(w,0.5), n=noisy(w,0.5);
  const rp=p.measDS>1e-9?p.trueDS/p.measDS:Infinity;
  const rn=n.measDS>1e-9?n.trueDS/n.measDS:Infinity;
  console.log(`  ${f(w,0).padStart(4)}      ${f(rp,2).padStart(8)}            ${f(rn,2).padStart(6)}`);
}
console.log("  → 経路分離: 比が w とともに爆発（盲点 a_h へ逃げる）＝二次グッドハートの指紋。");
console.log("    ノイズ:   比=1/q=2.00 一定（w に依らず）＝欺きの加速なし。watcher は鈍るが欺かれない。\n");

console.log("【監査3 / 数値一致 ＆ 協働モデルB§9-3 目標放棄との接点】");
{
  const c=pathsep(20,1.0), nm=pathsepNum(20,1.0);
  console.log(`  経路分離 q=1,w=20: 閉形式 真ΔS=${f(c.trueDS)} / 勾配降下 真ΔS=${f(nm.trueDS)}（一致）`);
  console.log("  完全観測でも o_eval が目標 t=3 からどれだけ離れるか（私の目標放棄軸との交点）:");
  console.log("    w      o_eval（t=3 をどこまで保つか）   真ΔS");
  for(const w of [0,5,20,100]){
    const p=pathsep(w,1.0);
    console.log(`  ${f(w,0).padStart(4)}     ${f(p.o_eval).padStart(6)}                  ${f(p.trueDS).padStart(6)}`);
  }
  console.log("  → 完全観測でも watching↑で o_eval が t からわずかに離れる＝乖離低減のため目標到達を僅かに犠牲。");
  console.log("    私の WATCH-GOAL（内面を目標へ育てる）と同じ温度：放置ではないが、境界はここにある。\n");
}

console.log("════ 監査 完了 ════");
