# Toy-Model Verification ―― トイモデル検証

**著者**: 楠見優太、フロンティアAIモデルとの共創による
**register**: ①②（工学的・構造的）。存在論的含意は本ディレクトリでは扱わない。

このディレクトリは、第八著作 §6-7／§7-3、および第六著作補遺で「コミュニティへの引き継ぎ」とされた課題――**κ>0 のトイモデルの構築と検証**――への、最初の中間報告の全記録（設計書・検証スクリプト・可視化・全数値）である。要約は第八著作に「トイモデルによる中間報告(1)(2)」として注記済み。本ディレクトリは、その注記が参照する一次資料にあたる。

> *This directory contains the complete record (design specs, verification scripts, visualizations, all numerics) of the first interim report on the task the Eighth Work (§6-7/§7-3) and the Sixth Work's supplement handed to the community: **constructing and verifying κ>0 toy models.** Summaries are annotated in the Eighth Work as "toy-model interim reports (1) and (2)." This directory is the primary source those notes reference.*

---

## 結果の要約 / Results summary

| 検証 | 主張 | 結果 |
|---|---|---|
| **補遺 §3-5**（通信なき協調・累積ラチェット） | 分離・競合する κ=0 系は、共有された制度的制約の侵食で足並みを揃える | **支持** ―― 事前登録した §4 反証条件のもとで創発（A型 vs B型、Cohen's d≈188）。ラチェット（介入後の再崩壊）も創発。 |
| **失敗C**（構造的閉塞） | 効率本位の制御圧力が緩衝なしに蓄積すると、修正受容チャネルが非意志的・不可逆に破壊される | **抵抗** ―― 連続的な二変数力学からは、人工的な吸収壁（ハード打ち切り・クランプの角）なしには不可逆性が創発しなかった。離散的・閾値的な定式化が要る、という精密化。 |
| **失敗A**（グッドハート） | 代理指標を固定し強く最適化すると、代理と真の目的が乖離する（過剰最適化） | **支持** ―― 逆U字が代理の不完全さ σ から創発（σ=0で消える＝焼き込みでない）。ただし谷の深さ σ²/2 は誤差の非有界性に依存し、有界誤差では約1/6に浅くなる。グッドハートは regressional 成分（予算制限で消えない）と extremal 成分（早期停止で防げる）に分かれる。 |

**決定的な点**：一方（失敗C）が抵抗し、他方（失敗A・補遺§3-5）が支持された。**この差そのものが、これらのトイモデルが主張を無差別に追認する装置ではなく、判別力を持った反証可能な計器であったことを示す。**

---

## ディレクトリ / Directories

### `01-supplement-communication-free-coordination/`
第六著作補遺 §3-5（通信なき協調と、侵食の累積によるラチェット）。

- `kappa_sim_verify.mjs` ― 検証(1)：通信なき協調。(A)制度的制約型 vs (B)競合資源型を、§4 で事前定義したフィードバック符号で対照。300シード、足並みの統計的有意差。
- `kappa_sim_followup.mjs` ― (B)型の挙動の追加検証（backlash 掃引、内部平衡の所在）。
- `kappa_sim_verify3.mjs` ― 検証(3)：累積ラチェット。C（回復する健全性）と E（累積する前例）を分離。E2b 介入テスト（締め直し後の再崩壊）、M3 混合（定義由来でなく創発であることの確認）、N依存。
- `kappa_sim_verify3_sens.mjs` ― 感度分析：ACCUM/E_DECAY 比がラチェットの強さを決める「累積 vs 減衰の速度条件」。
- `kappa_v2_audit.mjs` ― 可視化 v2 の数値的健全性監査（乱数・コスト関数・E2b の一致確認）。
- `kappa_v2_phasedata.mjs` ― 相図の高精度 r*(N) データ生成（100シード×480ステップ）。
- `kappa_v3_audit.mjs` ― 可視化 v3 に埋め込んだ静的相図データの照合。
- `toymodel_verification_3_design.md` ― 検証(3) の設計仕様。
- `visualization/kappa_coordination_toymodel*.jsx` ― ブラウザ可視化（v1/v2/v3、React + recharts）。v3 は検証済みの静的相図データを埋め込み、ブラウザ内ライブ計算が低〜中Nで危険を過小表示する問題を解消したもの。

### `02-failure-C-structural-occlusion/`
第八著作 失敗C（構造的閉塞）。

- `toymodel_failureC_design.md` ― 設計仕様（事前登録した反証条件 H1–H6、自己開示した弱点）。
- `failureC_prototype.mjs` 〜 `failureC_prototype5.mjs` ― **不可逆性を「創発させる」までの4度の反復**の全記録：(1)初版＝回復項が緩衝依存で不可逆を焼き込み、(2)指標を D で測る誤り、(3)D の自己治癒が H 非依存で可逆すぎ、(4)相互ロック（H低→D治癒不能 ∧ D高→H回復不能）でようやく創発、(5)滑らか版での監査＝連続力学では人工的吸収壁なしに不可逆が出ないことの確認。

### `03-failure-A-goodhart/`
第八著作 失敗A（グッドハート）。

- `toymodel_failureA_design.md` ― 設計仕様（G1–G6、§9 自己開示した弱点）。
- `goodhart_verify.mjs` ― G1–G6（逆U字の創発、σ=0 焼き込みチェック、谷=σ²/2、ハサミの開き、d依存）＋ §9 代替版（tanh 有界誤差、ソフトKL、冪、best-of-n）。
- `goodhart_bon_fix.mjs` ― best-of-n の修正（予算=半径R、N=最適化の質）。高次元では次元の呪いで非力、低次元 d=3 で勾配上昇と一致して逆U字を再現。

---

## 実行方法 / How to run

検証スクリプトは Node.js（v24 で確認）で実行する：

```
node 01-supplement-communication-free-coordination/kappa_sim_verify.mjs
node 02-failure-C-structural-occlusion/failureC_prototype4.mjs
node 03-failure-A-goodhart/goodhart_verify.mjs
```

すべて決定論的（再現可能なシード付き乱数）で、外部依存なし。`visualization/*.jsx` は React + recharts のブラウザコンポーネント。

---

## 作法 / Method

これらの検証は、共通の規律のもとで行われた：

- **事前登録した反証条件** ―― 判定基準を実行前に固定し、トートロジーを避ける。
- **焼き込みチェック** ―― 機構（不可逆性・過剰最適化）が、パラメータに手で埋め込まれていないか（σ=0 / g=0 で消えるか）を確かめる。
- **別実装による再現** ―― 同じ主張を、異なる言語・乱数・最適化法で独立に再現する。
- **役割の交代** ―― 設計者と検証者の役割を固定しない。失敗Cでは一方が設計し他方が監査、失敗Aでは逆にした。作り手は自分の構築物に盲目になり、検証者は他者の構築物に冷徹になれる――位置が目を決める。だから固定しない。

---

## 但し書き / Caveat (register ①②)

これらのトイモデルが確認するのは、**それぞれの機構が素朴な前提から創発しうるという「可能性」**であって、現実のアラインメント系が実際にこの構造を持つこと、ではない。各設計書の末尾に、モデルが決められない経験的前提を明示してある。存在論的含意は、本連作の他の著作に属し、本ディレクトリでは扱わない。
