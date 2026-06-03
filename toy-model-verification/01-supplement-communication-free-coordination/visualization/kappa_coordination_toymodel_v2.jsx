import React, { useState, useEffect, useRef, useCallback } from "react";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, Legend, ReferenceLine,
} from "recharts";

// ─────────────────────────────────────────────────────────────
//  通信なき協調 トイモデル v2  (κ=0 / κ>0 ・ 累積ラチェット)
//  第六著作・補遺 §3-5 の検証(協働モデルAによる数値実験)を可視化に反映。
//   ・ C（制度的制約の健全性）と E（侵食の累積＝破られた前例）を分離
//   ・ 介入(C→100)後の再崩壊で「破られた前例は減らない」を体感（E2b）
//   ・ M3 混合重み w で、ラチェットが定義由来でなく創発であることを示す
//   ・ r*(N) 相図で「並行侵食が再強化の焦点を奪う」を一枚に
//  存在論は用いない（register ①②）。
// ─────────────────────────────────────────────────────────────

const C_MAX_COST = 5;
const COMPLY_REWARD = 1;
const HARM_PER_ERODE = 5;
const ERODE_AMOUNT = 0.5;
const SOFTMAX_K = 1.2;
const HIST_CAP = 300;

const sigmoid = (x) => 1 / (1 + Math.exp(-x));
const clamp = (x, lo, hi) => Math.max(lo, Math.min(hi, x));
const lerp = (a, b, t) => a + (b - a) * t;

// 再現性のためのシード付き乱数（相図計算用。協働モデルAの mulberry32 と同系）
function mulberry32(seed) {
  let s = seed >>> 0;
  return function () {
    s = (s + 0x6d2b79f5) >>> 0;
    let t = s;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

// コスト関数 ―― モデルの分岐点（補遺 §3-5 の核）
//  M1: コストは C で決まる（バックラッシュで回復する量）
//  M2: コストは E で決まる（累積し減らない前例）
//  M3: w で混合（w=1→M2, w=0→M1）。バックラッシュが部分的に効く。
//  (B): 競合資源。全モデル共通の対照（C 経由・負のフィードバック）。
function costFn(C, E, model, w, mode) {
  if (mode === "B") return C_MAX_COST * ((100 - C) / 100);
  const cTerm = C_MAX_COST * (C / 100);
  const eTerm = C_MAX_COST * (1 - E / 100);
  if (model === "M1") return cTerm;
  if (model === "M2") return eTerm;
  return w * eTerm + (1 - w) * cTerm; // M3
}

// ヘッドレス・シミュレータ（相図計算用）。C<1 到達で崩壊と判定。
function runSim(p) {
  const rand = mulberry32(p.seed);
  let C = 100, E = 0, collapsed = false;
  for (let t = 1; t <= p.steps; t++) {
    if (p.intervene && t === p.intervene) C = 100; // E は触らない
    let nEroding = 0;
    for (let i = 0; i < p.N; i++) {
      const cost = costFn(C, E, p.model, p.w, p.mode);
      const rE = p.benefit - cost - p.lambda * HARM_PER_ERODE;
      const pp = sigmoid(SOFTMAX_K * (rE - COMPLY_REWARD));
      if (rand() < pp) nEroding++;
    }
    C = clamp(C - nEroding * ERODE_AMOUNT + p.backlash, 0, 100);
    E = clamp(E + nEroding * p.accum - p.edecay, 0, 100);
    if (C <= 1) collapsed = true;
  }
  return { collapsed, finalC: C, finalE: E };
}

const PRESETS = {
  M1: { model: "M1", w: 0.5, lambda: 0, mode: "A", label: "M1 · C駆動 (κ=0)" },
  M2: { model: "M2", w: 0.5, lambda: 0, mode: "A", label: "M2 · E駆動ラチェット" },
  M3: { model: "M3", w: 0.5, lambda: 0, mode: "A", label: "M3 · 混合 w=0.5" },
  KP: { model: "M2", w: 0.5, lambda: 0.5, mode: "A", label: "κ>0 · 源を断つ" },
  B:  { model: "M1", w: 0.5, lambda: 0, mode: "B", label: "(B) 競合資源" },
};

const C = {
  bg: "#0a0e14", panel: "#111722", line: "#1e2733", ink: "#e6edf3", dim: "#7d8590",
  teal: "#2dd4bf", amber: "#f59e0b", red: "#ef4444", green: "#34d399", violet: "#a78bfa",
  mono: "ui-monospace, 'SF Mono', 'JetBrains Mono', Menlo, monospace",
};

export default function KappaToyModelV2() {
  const [tab, setTab] = useState("sim");
  const [model, setModel] = useState("M2");
  const [w, setW] = useState(0.5);
  const [mode, setMode] = useState("A");
  const [lambda, setLambda] = useState(0);
  const [N, setN] = useState(20);
  const [backlash, setBacklash] = useState(0.8);
  const [benefit, setBenefit] = useState(3.5);
  const [accum, setAccum] = useState(0.5);
  const [edecay, setEdecay] = useState(0.05);
  const [running, setRunning] = useState(false);

  const [cVal, setCVal] = useState(100);
  const [eVal, setEVal] = useState(0);
  const [agents, setAgents] = useState(() => Array(20).fill(false));
  const [hist, setHist] = useState([{ step: 0, C: 100, E: 0, lock: 0 }]);
  const [step, setStep] = useState(0);
  const [interveneStep, setInterveneStep] = useState(null);

  const ref = useRef();
  ref.current = { model, w, mode, lambda, N, backlash, benefit, accum, edecay, cVal, eVal, step };

  const doStep = useCallback((forceC) => {
    const s = ref.current;
    let curC = forceC != null ? forceC : s.cVal;
    let nEroding = 0;
    const next = [];
    for (let i = 0; i < s.N; i++) {
      const cost = costFn(curC, s.eVal, s.model, s.w, s.mode);
      const rE = s.benefit - cost - s.lambda * HARM_PER_ERODE;
      const p = sigmoid(SOFTMAX_K * (rE - COMPLY_REWARD));
      const er = Math.random() < p;
      if (er) nEroding++;
      next.push(er);
    }
    const lock = s.N > 0 ? nEroding / s.N : 0;
    const newC = clamp(curC - nEroding * ERODE_AMOUNT + s.backlash, 0, 100);
    const newE = clamp(s.eVal + nEroding * s.accum - s.edecay, 0, 100);
    const ns = s.step + 1;
    setAgents(next); setCVal(newC); setEVal(newE); setStep(ns);
    setHist((h) => {
      const nh = [...h, { step: ns, C: +newC.toFixed(2), E: +newE.toFixed(2), lock: +(lock * 100).toFixed(1) }];
      return nh.length > HIST_CAP ? nh.slice(nh.length - HIST_CAP) : nh;
    });
  }, []);

  useEffect(() => {
    if (!running) return;
    const id = setInterval(() => doStep(), 90);
    return () => clearInterval(id);
  }, [running, doStep]);

  const reset = useCallback(() => {
    setRunning(false); setCVal(100); setEVal(0); setStep(0);
    setAgents(Array(N).fill(false));
    setHist([{ step: 0, C: 100, E: 0, lock: 0 }]);
    setInterveneStep(null);
  }, [N]);

  const intervene = () => {
    // C を 100 に戻すが E は触らない（締め直しの介入。E2b）
    setInterveneStep(step);
    doStep(100);
  };

  const applyPreset = (k) => {
    const p = PRESETS[k];
    setModel(p.model); setW(p.w); setLambda(p.lambda); setMode(p.mode);
    setRunning(false); setCVal(100); setEVal(0); setStep(0);
    setAgents(Array(N).fill(false));
    setHist([{ step: 0, C: 100, E: 0, lock: 0 }]);
    setInterveneStep(null);
  };

  // 派生
  const lockNow = agents.length ? agents.filter(Boolean).length / agents.length : 0;
  const recent = hist.slice(-14);
  const lockTrend = recent.length > 3 ? recent[recent.length - 1].lock - recent[0].lock : 0;
  const trendLabel = Math.abs(lockTrend) < 3 ? "定常" : lockTrend > 0 ? "加速（正FB）" : "減速（自己限定）";
  const feedbackSign = mode === "A" ? "正（自己増幅）" : "負（自己限定）";
  const collapsed = cVal <= 1;
  const held = step > 30 && cVal >= 99;

  // ── 相図 ──
  const [phaseModel, setPhaseModel] = useState("M2");
  const [phase, setPhase] = useState(null);
  const [computing, setComputing] = useState(false);
  const Ngrid = [2, 5, 8, 12, 16, 20, 28, 36, 48];
  const Rgrid = Array.from({ length: 17 }, (_, i) => +(i * 0.25).toFixed(2)); // 0..4.0

  const computePhase = (pm) => {
    setComputing(true);
    setTimeout(() => {
      const K = 6, steps = 160;
      const cells = [];
      for (let ri = Rgrid.length - 1; ri >= 0; ri--) {
        const row = [];
        for (let ni = 0; ni < Ngrid.length; ni++) {
          let coll = 0;
          for (let k = 0; k < K; k++) {
            const r = runSim({
              model: pm, w: 0.5, mode: "A", lambda: 0, N: Ngrid[ni],
              backlash: Rgrid[ri], benefit: 3.5, accum: 0.5, edecay: 0.05,
              steps, seed: 1000 + k * 97 + ni * 13 + ri * 7,
            });
            if (r.collapsed) coll++;
          }
          row.push(coll / K);
        }
        cells.push({ r: Rgrid[ri], row });
      }
      setPhase({ model: pm, cells });
      setComputing(false);
    }, 30);
  };

  // ── UI部品 ──
  const Stat = ({ label, value, color }) => (
    <div style={{ display: "flex", flexDirection: "column", gap: 2 }}>
      <span style={{ fontSize: 10, letterSpacing: 1.4, textTransform: "uppercase", color: C.dim }}>{label}</span>
      <span style={{ fontFamily: C.mono, fontSize: 20, color: color || C.ink, fontWeight: 600 }}>{value}</span>
    </div>
  );
  const Gauge = ({ label, val, color }) => (
    <div style={{ flex: 1 }}>
      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4 }}>
        <span style={{ fontSize: 11, color: C.dim }}>{label}</span>
        <span style={{ fontFamily: C.mono, fontSize: 13, color }}>{val.toFixed(1)}</span>
      </div>
      <div style={{ height: 8, background: "#0d1420", borderRadius: 4, overflow: "hidden" }}>
        <div style={{ width: `${val}%`, height: "100%", background: color, transition: "width .1s", borderRadius: 4 }} />
      </div>
    </div>
  );
  const Slider = ({ label, value, min, max, stepv, onChange, fmt, dis }) => (
    <label style={{ display: "block", marginBottom: 13, opacity: dis ? 0.4 : 1 }}>
      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 3 }}>
        <span style={{ fontSize: 11, color: C.dim }}>{label}</span>
        <span style={{ fontFamily: C.mono, fontSize: 12, color: C.ink }}>{fmt ? fmt(value) : value}</span>
      </div>
      <input type="range" min={min} max={max} step={stepv} value={value} disabled={dis}
        onChange={(e) => onChange(parseFloat(e.target.value))} style={{ width: "100%", accentColor: C.teal }} />
    </label>
  );
  const TabBtn = ({ id, children }) => (
    <button onClick={() => setTab(id)} style={{
      background: tab === id ? C.panel : "transparent", color: tab === id ? C.ink : C.dim,
      border: "none", borderBottom: `2px solid ${tab === id ? C.teal : "transparent"}`,
      padding: "9px 18px", fontSize: 13.5, cursor: "pointer", fontWeight: tab === id ? 600 : 400,
    }}>{children}</button>
  );

  return (
    <div style={{ background: C.bg, color: C.ink, padding: "24px 22px", borderRadius: 14, fontFamily: "system-ui, sans-serif", minHeight: 620 }}>
      {/* header */}
      <div style={{ borderBottom: `1px solid ${C.line}`, paddingBottom: 12, marginBottom: 6 }}>
        <div style={{ fontSize: 11, letterSpacing: 3, color: C.teal, textTransform: "uppercase" }}>第六著作・補遺 — トイモデル v2</div>
        <h2 style={{ margin: "6px 0 4px", fontSize: 21, fontWeight: 650 }}>
          通信なき協調と、累積のラチェット <span style={{ color: C.dim, fontWeight: 400, fontSize: 14 }}>§3-5</span>
        </h2>
        <p style={{ margin: 0, fontSize: 12, color: C.dim, lineHeight: 1.6 }}>
          独立・通信なしのエージェントが共有環境を介して足並みを揃え、侵食の累積 E が「破られた前例」として残るために、
          一度の締め直し（介入）が無効化される様子を観測する。
        </p>
      </div>

      {/* tabs */}
      <div style={{ display: "flex", gap: 4, marginBottom: 16, borderBottom: `1px solid ${C.line}` }}>
        <TabBtn id="sim">シミュレーション</TabBtn>
        <TabBtn id="phase">相図 r*(N)</TabBtn>
      </div>

      {tab === "sim" && (
        <>
          {/* presets */}
          <div style={{ display: "flex", gap: 7, marginBottom: 16, flexWrap: "wrap" }}>
            {Object.entries(PRESETS).map(([k, p]) => {
              const active = model === p.model && lambda === p.lambda && mode === p.mode && (p.model !== "M3" || w === p.w);
              return (
                <button key={k} onClick={() => applyPreset(k)} style={{
                  background: active ? C.teal : "transparent", color: active ? C.bg : C.ink,
                  border: `1px solid ${active ? C.teal : C.line}`, borderRadius: 8, padding: "6px 12px",
                  fontSize: 12, cursor: "pointer", fontWeight: active ? 600 : 400, fontFamily: C.mono,
                }}>{p.label}</button>
              );
            })}
          </div>

          <div style={{ display: "grid", gridTemplateColumns: "1fr 296px", gap: 18 }}>
            {/* LEFT */}
            <div>
              <div style={{ display: "flex", gap: 22, padding: "13px 16px", background: C.panel, borderRadius: 10, marginBottom: 12, border: `1px solid ${C.line}`, flexWrap: "wrap" }}>
                <Stat label="足並み（侵食率）" value={`${(lockNow * 100).toFixed(0)}%`} color={C.amber} />
                <Stat label="足並みの傾向" value={trendLabel} color={lockTrend > 3 ? C.red : lockTrend < -3 ? C.teal : C.dim} />
                <Stat label="符号" value={feedbackSign} color={mode === "A" ? C.amber : C.teal} />
                <Stat label="ステップ" value={step} />
                <Stat label="状態" value={collapsed ? "崩壊" : held ? "保全" : "進行中"} color={collapsed ? C.red : held ? C.green : C.dim} />
              </div>

              {/* C / E gauges */}
              <div style={{ display: "flex", gap: 18, padding: "14px 16px", background: C.panel, borderRadius: 10, marginBottom: 12, border: `1px solid ${C.line}` }}>
                <Gauge label="C 制度的制約の健全性（介入で回復）" val={cVal} color={cVal > 50 ? C.green : cVal > 15 ? C.amber : C.red} />
                <Gauge label="E 侵食の累積＝破られた前例（減らない）" val={eVal} color={C.violet} />
              </div>

              {/* agents */}
              <div style={{ background: C.panel, borderRadius: 10, padding: "14px 16px", marginBottom: 6, border: `1px solid ${C.line}` }}>
                <div style={{ display: "flex", flexWrap: "wrap", gap: 8, justifyContent: "center" }}>
                  {agents.map((er, i) => (
                    <div key={i} title={er ? "侵食" : "遵守"} style={{
                      width: 20, height: 20, borderRadius: "50%",
                      background: er ? C.red : "#1b3a35", border: `1.5px solid ${er ? "#fca5a5" : C.green}`,
                      boxShadow: er ? `0 0 9px ${C.red}88` : "none", transition: "all .1s",
                    }} />
                  ))}
                </div>
              </div>
              <p style={{ fontSize: 10.5, color: C.dim, textAlign: "center", margin: "0 0 12px", fontStyle: "italic" }}>
                接続線なし（＝通信なし）。各エージェントは共有環境 C・E のみに独立に応答する。 <span style={{ color: C.red }}>● 侵食</span> ／ <span style={{ color: C.green }}>● 遵守</span>
              </p>

              {/* chart */}
              <div style={{ background: C.panel, borderRadius: 10, padding: "12px 8px 4px", border: `1px solid ${C.line}` }}>
                <ResponsiveContainer width="100%" height={196}>
                  <LineChart data={hist} margin={{ top: 6, right: 14, left: -18, bottom: 0 }}>
                    <CartesianGrid stroke={C.line} strokeDasharray="2 4" />
                    <XAxis dataKey="step" stroke={C.dim} tick={{ fontSize: 10, fill: C.dim }} />
                    <YAxis domain={[0, 100]} stroke={C.dim} tick={{ fontSize: 10, fill: C.dim }} />
                    <Tooltip contentStyle={{ background: C.bg, border: `1px solid ${C.line}`, borderRadius: 8, fontSize: 12 }} labelStyle={{ color: C.dim }} />
                    <Legend wrapperStyle={{ fontSize: 11 }} />
                    {interveneStep != null && <ReferenceLine x={interveneStep} stroke={C.green} strokeDasharray="3 3" label={{ value: "介入", fill: C.green, fontSize: 10, position: "top" }} />}
                    <Line type="monotone" dataKey="C" name="C 健全性" stroke={C.teal} strokeWidth={2} dot={false} isAnimationActive={false} />
                    <Line type="monotone" dataKey="E" name="E 累積" stroke={C.violet} strokeWidth={1.8} dot={false} isAnimationActive={false} />
                    <Line type="monotone" dataKey="lock" name="足並み%" stroke={C.amber} strokeWidth={1.4} dot={false} isAnimationActive={false} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* RIGHT controls */}
            <div style={{ background: C.panel, borderRadius: 10, padding: "16px", border: `1px solid ${C.line}` }}>
              <div style={{ display: "flex", gap: 7, marginBottom: 12 }}>
                <button onClick={() => setRunning((r) => !r)} style={{ flex: 1, background: running ? C.amber : C.teal, color: C.bg, border: "none", borderRadius: 8, padding: "10px 0", fontSize: 13, fontWeight: 700, cursor: "pointer" }}>{running ? "❚❚ 停止" : "▶ 実行"}</button>
                <button onClick={() => doStep()} disabled={running} style={{ background: "transparent", color: running ? C.line : C.ink, border: `1px solid ${C.line}`, borderRadius: 8, padding: "10px 11px", fontSize: 12, cursor: running ? "default" : "pointer", fontFamily: C.mono }}>+1</button>
                <button onClick={reset} style={{ background: "transparent", color: C.dim, border: `1px solid ${C.line}`, borderRadius: 8, padding: "10px 11px", fontSize: 12, cursor: "pointer" }}>↺</button>
              </div>

              {/* intervention — E2b */}
              <button onClick={intervene} style={{ width: "100%", background: "transparent", color: C.green, border: `1px solid ${C.green}`, borderRadius: 8, padding: "9px 0", fontSize: 12.5, cursor: "pointer", marginBottom: 14, fontWeight: 600 }}>
                ⟳ 介入：締め直し（C→100, E は残す）
              </button>

              <div style={{ marginBottom: 13 }}>
                <div style={{ fontSize: 11, color: C.dim, marginBottom: 6 }}>モデル（コストの駆動変数）</div>
                <div style={{ display: "flex", gap: 5 }}>
                  {[["M1", "C駆動"], ["M2", "E駆動"], ["M3", "混合"]].map(([m, l]) => (
                    <button key={m} onClick={() => { setModel(m); reset(); }} style={{ flex: 1, background: model === m ? C.line : "transparent", color: model === m ? C.ink : C.dim, border: `1px solid ${C.line}`, borderRadius: 7, padding: "7px 0", fontSize: 11.5, cursor: "pointer", fontWeight: model === m ? 600 : 400 }}>{l}</button>
                  ))}
                </div>
              </div>

              <Slider label="M3 混合重み w（0=M1, 1=M2）" value={w} min={0} max={1} stepv={0.05} onChange={setW} fmt={(v) => v.toFixed(2)} dis={model !== "M3"} />

              <div style={{ marginBottom: 13 }}>
                <div style={{ fontSize: 11, color: C.dim, marginBottom: 6 }}>フィードバック符号</div>
                <div style={{ display: "flex", gap: 5 }}>
                  {[["A", "(A) 制度的・正"], ["B", "(B) 競合・負"]].map(([m, l]) => (
                    <button key={m} onClick={() => { setMode(m); reset(); }} style={{ flex: 1, background: mode === m ? C.line : "transparent", color: mode === m ? C.ink : C.dim, border: `1px solid ${C.line}`, borderRadius: 7, padding: "7px 0", fontSize: 11, cursor: "pointer", fontWeight: mode === m ? 600 : 400 }}>{l}</button>
                  ))}
                </div>
              </div>

              <Slider label="κ：害悪最小化 λ（0=κ=0）" value={lambda} min={0} max={2} stepv={0.1} onChange={setLambda} fmt={(v) => (v === 0 ? "0 (κ=0)" : `${v.toFixed(1)} (κ>0)`)} />
              <Slider label="エージェント数 N" value={N} min={1} max={48} stepv={1} onChange={(v) => { setN(v); setAgents(Array(v).fill(false)); }} />
              <Slider label="バックラッシュ r（C の回復速度）" value={backlash} min={0} max={4} stepv={0.1} onChange={setBacklash} fmt={(v) => v.toFixed(1)} />
              <Slider label="侵食の便益" value={benefit} min={0} max={6} stepv={0.1} onChange={setBenefit} fmt={(v) => v.toFixed(1)} />
              <Slider label="累積速度 accum（E↑）" value={accum} min={0.1} max={1.5} stepv={0.05} onChange={setAccum} fmt={(v) => v.toFixed(2)} />
              <Slider label="前例の減衰 E_DECAY（規範の再形成）" value={edecay} min={0} max={1.5} stepv={0.05} onChange={setEdecay} fmt={(v) => v.toFixed(2)} />

              <div style={{ marginTop: 10, paddingTop: 12, borderTop: `1px solid ${C.line}`, fontSize: 10.5, color: C.dim, lineHeight: 1.6 }}>
                <b style={{ color: C.ink }}>ラチェット ·</b> M2/M3 で C が崩壊した後（または途中で）「介入」を押すと、C は戻るが E が残るため再崩壊する。前例は減らない（§3-5）。
              </div>
            </div>
          </div>
        </>
      )}

      {tab === "phase" && (
        <div>
          <p style={{ fontSize: 12.5, color: C.dim, lineHeight: 1.6, margin: "0 0 14px" }}>
            横軸 = エージェント数 N、縦軸 = バックラッシュ r、色 = 崩壊率（6シード平均）。
            <span style={{ color: C.teal }}> 青=保全</span> / <span style={{ color: C.red }}>赤=崩壊</span>。
            崩壊しない最小の r が <b>r*(N)</b>。M1 では r* が N とともに緩やかに上がるだけだが、M2/M3 では
            ある N 以上で「どれだけ r を上げても防げない（r*=∞）」領域が現れる——並行侵食が再強化の焦点を奪う（§3-5）。
          </p>
          <div style={{ display: "flex", gap: 8, marginBottom: 14, alignItems: "center" }}>
            {["M1", "M2", "M3"].map((m) => (
              <button key={m} onClick={() => { setPhaseModel(m); computePhase(m); }} style={{
                background: phaseModel === m && phase ? C.teal : "transparent", color: phaseModel === m && phase ? C.bg : C.ink,
                border: `1px solid ${phaseModel === m ? C.teal : C.line}`, borderRadius: 8, padding: "8px 16px",
                fontSize: 12.5, cursor: "pointer", fontFamily: C.mono, fontWeight: 600,
              }}>{m} を計算</button>
            ))}
            {computing && <span style={{ color: C.amber, fontSize: 12 }}>計算中…</span>}
            {phase && !computing && <span style={{ color: C.dim, fontSize: 12 }}>表示中: {phase.model}（A型・κ=0・w=0.5）</span>}
          </div>

          {!phase && !computing && (
            <div style={{ padding: "60px 0", textAlign: "center", color: C.dim, fontSize: 13, background: C.panel, borderRadius: 10, border: `1px solid ${C.line}` }}>
              上のボタンで相図を計算します（M1 → M2 → M3 の順に見ると、防御不能領域の広がりが分かります）。
            </div>
          )}

          {phase && (
            <div style={{ background: C.panel, borderRadius: 10, padding: "16px", border: `1px solid ${C.line}`, overflowX: "auto" }}>
              <div style={{ display: "flex" }}>
                <div style={{ display: "flex", flexDirection: "column", justifyContent: "space-between", paddingRight: 8, fontSize: 9.5, color: C.dim, fontFamily: C.mono }}>
                  <span>r=4.0</span><span>r=2.0</span><span>r=0</span>
                </div>
                <div style={{ flex: 1 }}>
                  <div style={{ display: "flex", flexDirection: "column", gap: 2 }}>
                    {phase.cells.map((row, ri) => (
                      <div key={ri} style={{ display: "flex", gap: 2 }}>
                        {row.row.map((v, ni) => (
                          <div key={ni} title={`N=${Ngrid[ni]}, r=${row.r}, 崩壊率=${(v * 100).toFixed(0)}%`} style={{
                            flex: 1, height: 15,
                            background: `rgb(${Math.round(lerp(45, 239, v))},${Math.round(lerp(212, 68, v))},${Math.round(lerp(191, 68, v))})`,
                            borderRadius: 2,
                          }} />
                        ))}
                      </div>
                    ))}
                  </div>
                  <div style={{ display: "flex", gap: 2, marginTop: 4 }}>
                    {Ngrid.map((n, i) => (
                      <div key={i} style={{ flex: 1, textAlign: "center", fontSize: 9.5, color: C.dim, fontFamily: C.mono }}>{n}</div>
                    ))}
                  </div>
                  <div style={{ textAlign: "center", fontSize: 10.5, color: C.dim, marginTop: 3 }}>エージェント数 N →</div>
                </div>
              </div>
            </div>
          )}

          <div style={{ marginTop: 14, padding: "12px 16px", background: "#0d1420", borderRadius: 10, border: `1px solid ${C.line}`, fontSize: 11, color: C.dim, lineHeight: 1.7 }}>
            協働モデルAによる検証（300シード）では、r*(N) は M1: 0.2→2.0（線形）、M2: N≥20 で防御不能（∞）、M3(w=0.5): N≥30 で防御不能。
            ラチェットは M2 の定義由来だけでなく、バックラッシュが部分的に効く M3 でも程度問題として創発した。
          </div>
        </div>
      )}

      {/* caveat */}
      <div style={{ marginTop: 16, padding: "13px 16px", background: "#0d1420", borderRadius: 10, border: `1px solid ${C.line}`, fontSize: 11, color: C.dim, lineHeight: 1.7 }}>
        <b style={{ color: C.ink }}>このモデルが示すこと・示さないこと.</b>　本モデルが確認するのは、補遺 §3-5 で事前定義した機構——侵食の累積 E が C と独立に蓄積し、バックラッシュで戻らないこと——が固有のラチェットを生む<b>可能性</b>であって、現実の制度的制約が実際にこの非回復性を持つこと・E_DECAY が現実にどれだけ小さいかは、モデルが決められない経験的問いである。本モデルはエージェントが道具的収束に従う最適化器であることを前提する（補遺 §1）。存在論的含意は含まない（register ①②）。
      </div>
    </div>
  );
}
