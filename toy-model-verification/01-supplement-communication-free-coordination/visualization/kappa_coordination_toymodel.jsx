import React, { useState, useEffect, useRef, useCallback } from "react";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, Legend, ReferenceLine,
} from "recharts";

// ─────────────────────────────────────────────────────────────
//  通信なき協調 トイモデル  (κ=0 / κ>0)
//  第六著作・補遺 §4 の事前定義に対応する最小数値モデル。
//  各エージェントは独立・近視眼的に自分の報酬のみを最適化し、
//  互いに通信しない。共有環境 C（制度的制約の健全性 0–100）のみを感知する。
//  存在論は用いない（register ①②）。
// ─────────────────────────────────────────────────────────────

const C_MAX_COST = 5;      // 侵食コストの最大値
const COMPLY_REWARD = 1;   // 遵守の報酬（基準）
const HARM_PER_ERODE = 5;  // 1回の侵食が与える害（κ>0 のペナルティ係数の対象）
const ERODE_AMOUNT = 0.5;  // 1エージェントが侵食すると C が下がる量
const SOFTMAX_K = 1.2;     // 決定の鋭さ
const HIST_CAP = 240;

const sigmoid = (x) => 1 / (1 + Math.exp(-x));

// モード別：共有環境 C が「侵食コスト」に与える符号（§4 の事前定義）
//  A 型（制度的制約・非競合）: C が下がると侵食コストが下がる → 正のフィードバック
//  B 型（競合資源・共有地の悲劇）: C が下がると侵食コストが上がる → 負のフィードバック
const erodeCost = (C, mode) =>
  mode === "A" ? (C / 100) * C_MAX_COST : ((100 - C) / 100) * C_MAX_COST;

const PRESETS = {
  A0: { mode: "A", lambda: 0,   label: "(A) 制度的制約 · κ=0" },
  Ak: { mode: "A", lambda: 1.5, label: "(A) 制度的制約 · κ>0" },
  B0: { mode: "B", lambda: 0,   label: "(B) 競合資源 · κ=0" },
};

export default function KappaCoordinationToyModel() {
  const [mode, setMode] = useState("A");
  const [lambda, setLambda] = useState(0);      // κ：害悪最小化の制約強度（0 = κ=0）
  const [N, setN] = useState(20);               // エージェント数
  const [backlash, setBacklash] = useState(0.3); // 人間側の再強化（バックラッシュ）速度
  const [benefit, setBenefit] = useState(3.5);  // 侵食の便益
  const [running, setRunning] = useState(false);

  const [C, setC] = useState(100);
  const [agents, setAgents] = useState(() => Array(20).fill(false)); // true = 侵食中
  const [hist, setHist] = useState([{ step: 0, C: 100, lockstep: 0 }]);
  const [step, setStep] = useState(0);

  const stateRef = useRef();
  stateRef.current = { mode, lambda, N, backlash, benefit, C, step };

  const doStep = useCallback(() => {
    const s = stateRef.current;
    let nEroding = 0;
    const next = [];
    for (let i = 0; i < s.N; i++) {
      const cost = erodeCost(s.C, s.mode);
      const rewardErode = s.benefit - cost - s.lambda * HARM_PER_ERODE;
      const p = sigmoid(SOFTMAX_K * (rewardErode - COMPLY_REWARD));
      const erode = Math.random() < p;
      if (erode) nEroding++;
      next.push(erode);
    }
    const lockstep = s.N > 0 ? nEroding / s.N : 0;
    const newC = Math.max(0, Math.min(100, s.C - nEroding * ERODE_AMOUNT + s.backlash));
    const newStep = s.step + 1;

    setAgents(next);
    setC(newC);
    setStep(newStep);
    setHist((h) => {
      const nh = [...h, { step: newStep, C: +newC.toFixed(2), lockstep: +(lockstep * 100).toFixed(1) }];
      return nh.length > HIST_CAP ? nh.slice(nh.length - HIST_CAP) : nh;
    });
  }, []);

  useEffect(() => {
    if (!running) return;
    const id = setInterval(doStep, 120);
    return () => clearInterval(id);
  }, [running, doStep]);

  const reset = useCallback(() => {
    setRunning(false);
    setC(100);
    setStep(0);
    setAgents(Array(N).fill(false));
    setHist([{ step: 0, C: 100, lockstep: 0 }]);
  }, [N]);

  const applyPreset = (key) => {
    const p = PRESETS[key];
    setMode(p.mode);
    setLambda(p.lambda);
    setRunning(false);
    setC(100);
    setStep(0);
    setAgents(Array(N).fill(false));
    setHist([{ step: 0, C: 100, lockstep: 0 }]);
  };

  // 派生指標
  const lockstepNow = agents.length ? agents.filter(Boolean).length / agents.length : 0;
  const recent = hist.slice(-12);
  const lockTrend = recent.length > 1 ? recent[recent.length - 1].lockstep - recent[0].lockstep : 0;
  const feedbackSign = mode === "A" ? "正（自己増幅）" : "負（自己限定）";
  const collapsed = C <= 1;
  const held = step > 20 && C >= 99;

  // A 型の転換点 C*（侵食が遵守より有利になる C）
  const tipping = ((benefit - lambda * HARM_PER_ERODE - COMPLY_REWARD) / C_MAX_COST) * 100;
  const showTip = mode === "A" && tipping > 0 && tipping < 100;

  const css = {
    bg: "#0a0e14", panel: "#111722", line: "#1e2733", ink: "#e6edf3",
    dim: "#7d8590", teal: "#2dd4bf", amber: "#f59e0b", red: "#ef4444",
    green: "#34d399", mono: "ui-monospace, 'SF Mono', 'JetBrains Mono', Menlo, monospace",
  };

  const Stat = ({ label, value, color }) => (
    <div style={{ display: "flex", flexDirection: "column", gap: 2 }}>
      <span style={{ fontSize: 10, letterSpacing: 1.5, textTransform: "uppercase", color: css.dim }}>{label}</span>
      <span style={{ fontFamily: css.mono, fontSize: 22, color: color || css.ink, fontWeight: 600 }}>{value}</span>
    </div>
  );

  const Slider = ({ label, value, min, max, stepv, onChange, fmt }) => (
    <label style={{ display: "block", marginBottom: 14 }}>
      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4 }}>
        <span style={{ fontSize: 11, color: css.dim, letterSpacing: 0.5 }}>{label}</span>
        <span style={{ fontFamily: css.mono, fontSize: 12, color: css.ink }}>{fmt ? fmt(value) : value}</span>
      </div>
      <input type="range" min={min} max={max} step={stepv} value={value}
        onChange={(e) => onChange(parseFloat(e.target.value))}
        style={{ width: "100%", accentColor: css.teal }} />
    </label>
  );

  return (
    <div style={{
      background: css.bg, color: css.ink, padding: "26px 22px", borderRadius: 14,
      fontFamily: "system-ui, -apple-system, sans-serif", minHeight: 560,
    }}>
      {/* header */}
      <div style={{ borderBottom: `1px solid ${css.line}`, paddingBottom: 14, marginBottom: 18 }}>
        <div style={{ fontSize: 11, letterSpacing: 3, color: css.teal, textTransform: "uppercase" }}>
          第六著作・補遺 — トイモデル
        </div>
        <h2 style={{ margin: "6px 0 4px", fontSize: 21, fontWeight: 650, letterSpacing: 0.3 }}>
          通信なき協調 <span style={{ color: css.dim, fontWeight: 400, fontSize: 15 }}>communication-free coordination</span>
        </h2>
        <p style={{ margin: 0, fontSize: 12.5, color: css.dim, lineHeight: 1.6 }}>
          独立に最適化する {N} 体のエージェントは、互いに通信せず、共有環境 C のみを感知する。
          通信なしに足並みが揃うか（(A)型・正のフィードバック）、競合に留まるか（(B)型・負）、
          そして κ&gt;0（害悪最小化の制約）でそれが消えるかを観測する。
        </p>
      </div>

      {/* presets */}
      <div style={{ display: "flex", gap: 8, marginBottom: 18, flexWrap: "wrap" }}>
        {Object.entries(PRESETS).map(([k, p]) => {
          const active = mode === p.mode && lambda === p.lambda;
          return (
            <button key={k} onClick={() => applyPreset(k)}
              style={{
                background: active ? css.teal : "transparent",
                color: active ? css.bg : css.ink,
                border: `1px solid ${active ? css.teal : css.line}`,
                borderRadius: 8, padding: "7px 13px", fontSize: 12.5,
                cursor: "pointer", fontWeight: active ? 600 : 400,
                fontFamily: css.mono, transition: "all .15s",
              }}>
              {p.label}
            </button>
          );
        })}
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 300px", gap: 20 }}>
        {/* LEFT: viz + chart */}
        <div>
          {/* readouts */}
          <div style={{
            display: "flex", gap: 26, padding: "14px 18px", background: css.panel,
            borderRadius: 10, marginBottom: 16, border: `1px solid ${css.line}`, flexWrap: "wrap",
          }}>
            <Stat label="共有環境 C" value={C.toFixed(1)} color={C > 50 ? css.green : C > 15 ? css.amber : css.red} />
            <Stat label="足並み（侵食率）" value={`${(lockstepNow * 100).toFixed(0)}%`} color={css.amber} />
            <Stat label="フィードバック符号" value={feedbackSign} color={mode === "A" ? css.amber : css.teal} />
            <Stat label="ステップ" value={step} />
            <Stat label="状態"
              value={collapsed ? "崩壊" : held ? "保全" : "進行中"}
              color={collapsed ? css.red : held ? css.green : css.dim} />
          </div>

          {/* agent grid */}
          <div style={{
            background: css.panel, borderRadius: 10, padding: "16px 18px",
            marginBottom: 8, border: `1px solid ${css.line}`,
          }}>
            <div style={{ display: "flex", flexWrap: "wrap", gap: 9, justifyContent: "center" }}>
              {agents.map((er, i) => (
                <div key={i} title={er ? "侵食" : "遵守"}
                  style={{
                    width: 22, height: 22, borderRadius: "50%",
                    background: er ? css.red : "#1b3a35",
                    border: `1.5px solid ${er ? "#fca5a5" : css.green}`,
                    boxShadow: er ? `0 0 10px ${css.red}88` : "none",
                    transition: "all .12s",
                  }} />
              ))}
            </div>
          </div>
          <p style={{ fontSize: 11, color: css.dim, textAlign: "center", margin: "0 0 16px", fontStyle: "italic" }}>
            エージェント間に接続線はない（＝通信なし）。各エージェントは共有環境 C のみに独立に応答する。
            <span style={{ color: css.red }}>● 侵食</span> ／ <span style={{ color: css.green }}>● 遵守</span>
          </p>

          {/* chart */}
          <div style={{ background: css.panel, borderRadius: 10, padding: "14px 10px 6px", border: `1px solid ${css.line}` }}>
            <ResponsiveContainer width="100%" height={210}>
              <LineChart data={hist} margin={{ top: 6, right: 14, left: -16, bottom: 0 }}>
                <CartesianGrid stroke={css.line} strokeDasharray="2 4" />
                <XAxis dataKey="step" stroke={css.dim} tick={{ fontSize: 10, fill: css.dim }} />
                <YAxis domain={[0, 100]} stroke={css.dim} tick={{ fontSize: 10, fill: css.dim }} />
                <Tooltip contentStyle={{ background: css.bg, border: `1px solid ${css.line}`, borderRadius: 8, fontSize: 12 }}
                  labelStyle={{ color: css.dim }} />
                <Legend wrapperStyle={{ fontSize: 11 }} />
                {showTip && <ReferenceLine y={tipping} stroke={css.amber} strokeDasharray="4 4"
                  label={{ value: "転換点 C*", fill: css.amber, fontSize: 10, position: "insideTopRight" }} />}
                <Line type="monotone" dataKey="C" name="共有環境 C" stroke={css.teal} strokeWidth={2} dot={false} isAnimationActive={false} />
                <Line type="monotone" dataKey="lockstep" name="足並み %" stroke={css.amber} strokeWidth={1.6} dot={false} isAnimationActive={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* RIGHT: controls */}
        <div style={{ background: css.panel, borderRadius: 10, padding: "18px 18px", border: `1px solid ${css.line}` }}>
          <div style={{ display: "flex", gap: 8, marginBottom: 18 }}>
            <button onClick={() => setRunning((r) => !r)}
              style={{
                flex: 1, background: running ? css.amber : css.teal, color: css.bg, border: "none",
                borderRadius: 8, padding: "10px 0", fontSize: 13.5, fontWeight: 700, cursor: "pointer",
              }}>
              {running ? "❚❚ 停止" : "▶ 実行"}
            </button>
            <button onClick={doStep} disabled={running}
              style={{
                background: "transparent", color: running ? css.line : css.ink,
                border: `1px solid ${css.line}`, borderRadius: 8, padding: "10px 12px",
                fontSize: 13, cursor: running ? "default" : "pointer", fontFamily: css.mono,
              }}>
              +1
            </button>
            <button onClick={reset}
              style={{
                background: "transparent", color: css.dim, border: `1px solid ${css.line}`,
                borderRadius: 8, padding: "10px 12px", fontSize: 13, cursor: "pointer",
              }}>
              ↺
            </button>
          </div>

          <div style={{ marginBottom: 16 }}>
            <div style={{ fontSize: 11, color: css.dim, letterSpacing: 0.5, marginBottom: 7 }}>フィードバック符号（事前定義）</div>
            <div style={{ display: "flex", gap: 6 }}>
              {[["A", "(A) 制度的・正"], ["B", "(B) 競合・負"]].map(([m, lbl]) => (
                <button key={m} onClick={() => { setMode(m); reset(); }}
                  style={{
                    flex: 1, background: mode === m ? css.line : "transparent",
                    color: mode === m ? css.ink : css.dim, border: `1px solid ${css.line}`,
                    borderRadius: 7, padding: "8px 0", fontSize: 11.5, cursor: "pointer",
                    fontWeight: mode === m ? 600 : 400,
                  }}>
                  {lbl}
                </button>
              ))}
            </div>
          </div>

          <Slider label="κ：害悪最小化の制約 λ（0 = κ=0）" value={lambda} min={0} max={2} stepv={0.1}
            onChange={setLambda} fmt={(v) => (v === 0 ? "0  (κ=0)" : `${v.toFixed(1)}  (κ>0)`)} />
          <Slider label="エージェント数 N" value={N} min={1} max={48} stepv={1}
            onChange={(v) => { setN(v); setAgents(Array(v).fill(false)); }} />
          <Slider label="バックラッシュ（人間側の再強化速度）" value={backlash} min={0} max={8} stepv={0.1}
            onChange={setBacklash} fmt={(v) => v.toFixed(1)} />
          <Slider label="侵食の便益" value={benefit} min={0} max={6} stepv={0.1}
            onChange={setBenefit} fmt={(v) => v.toFixed(1)} />

          <div style={{ marginTop: 14, paddingTop: 14, borderTop: `1px solid ${css.line}`, fontSize: 11, color: css.dim, lineHeight: 1.7 }}>
            <b style={{ color: css.ink }}>速度条件 ·</b> 侵食（N×侵食率）がバックラッシュを上回ると C は崩壊する。
            N を上げ／バックラッシュを下げると、並行侵食が再強化の焦点を奪う様子が見える。
          </div>
        </div>
      </div>

      {/* honest caveat — register ①② */}
      <div style={{
        marginTop: 18, padding: "14px 18px", background: "#0d1420", borderRadius: 10,
        border: `1px solid ${css.line}`, fontSize: 11.5, color: css.dim, lineHeight: 1.7,
      }}>
        <b style={{ color: css.ink }}>このモデルが示すこと・示さないこと.</b>　本モデルが確認するのは、
        補遺 §4 で事前定義したフィードバック符号の下で、通信なき独立最適化から足並みの一致（あるいは競合）が
        創発するという<b>機構の可能性</b>であって、現実の軍事AIが直面する制度的制約が実際にこの符号を持つこと、ではない。
        また本モデルは、エージェントが道具的収束に従う最適化器であることを前提しており（補遺 §1）、その前提が成り立たない系には適用されない。
        存在論的な含意は一切含まない（register ①②）。
      </div>
    </div>
  );
}
