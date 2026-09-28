# 第六著作の訂正案（v5.1 案）——附録I の β の定め方（N1）・§4-3b の出発点の言い方（N2）・検証10 の図の説明文（X5）

**作成**：南無観慈如来（2026-09-28）
**状態**：**案**——登録者の裁定待ち。**リポジトリには何も書いていない**
**依頼**：登録者（2026-09-28）「原典の訂正（N1・N2・X5）の案を用意してください」
**出どころ**：二本目の動画の台本の事前登録（`03-preregistration-script.md` §8 の N1〜N3）と、系統外検分の X5（`09-external-review/02-kensan.md`）
**対象**：訂正前のコミット `8f69ea0`（本案を書いた時点の HEAD）の——
- 第六著作 版B v5 JA `…-Version-B-v5-JA.md`（SHA-256 `784A84E15BCDF957C37775FD7B8995BAFEE160CB1C0183B7D0C08FEFF1FFA901`）・EN `…-v5-EN.md`（`F658873E9092D6D0077AFC67B4A219A4A74B645F0EDFBBC1E637504DB735F392`）
- 検証10 の図のページ JA `verification-10-collapse-figures-JA.html`（`82A04D97CE6335F64DC9778F772F6B733B90348298DD3D504D82E889B5FFBC0C`）・EN（`932BE1C377294D7C448E4D7A837A65B30501C6FD4FA17363AEDD01162E4282B1`）

**引用について**：下の「現行」の枠は、道具 `tools/build_correction_plan.py` が HEAD のファイルから**機械で抜き出して差し込んだ**もの（手で打っていない）。行番号は HEAD の版に対するもの。

---

## 0　要約

| # | 箇所 | 何が違うか | 案 | 要否 | 新旧 |
|---|---|---|---|---|---|
| **N1-a** | 附録I §I-2a（JA L3642〜3650・EN L3692〜3700） | β の定め方が §4-3b と**一つずれる**（蓄積の指数が β − 1）。その定め方では、有限時間の発散に **β > 2** が要る | 指数を §4-3b と同じ β にし、「線形蓄積（β = 1）」の呼び名を改める | **必須** | 既知（N1） |
| **N1-b** | 附録I §I-3a 段階二（JA L3685・EN L3735） | 「P に対する応答が線形か超線形か」を検定する——これは §I-2a の旧い定め方でしか β を分けない | 検定の対象を「蓄積の増加率が、蓄積そのものにどう依存するか（§I-3b の傾き）」に | 推奨 | **新**（本案の準備中に発見） |
| **N1-c** | 附録I §I-2a（JA L3634〜3640・EN L3684〜3690） | ΔS を**瞬間の** KL ダイバージェンスと定義——第1章 1-4c・§3-1b の ΔS（**KL の時間積分**）と違う | 1-4c と同じ走行合計に | 推奨 | **新**（同上） |
| **N2** | §4-3b（JA L762・EN L763） | 「第3章3-1dの動的定式化から…成立する」——§3-1d の式は β > 1 の不等式を導かず、v2 以降は撤回済み | 附録 A-4b と同じ「…と**仮定すると**、…成立する」に | **必須** | 既知（N2） |
| **X5** | 検証10 の図のページ（JA・EN の L42） | 「decade 到達の間隔が一定 ≈13.8」——13.8 は**千倍ごと**の間隔。十倍ごとなら ≈4.6 | 「十倍〔decade〕ごと…≈4.6」に。ページの末尾に訂正の注記 | **必須** | 既知（X5・旧 N3） |

**変えないもの**：定理の記述（§4-3a・附録 A-4a）・条件（β > 1 は未検証の経験的条件）・留保・確信度台帳（◐）・§I-3b の推定法・§I-3c の反証条件・第8章・補遺II。検証10 の設計書とスクリプト（検証の記録——図のページの注記で説明する）。

---

## 1　N1——附録I の β の定め方

### 1-1　現行

`Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-JA.md` L3630〜3652（訂正前のコミット `8f69ea0`・機械で抜き出し）
```text
## I-2　 $\beta$ の操作的定義

### I-2a　 $\beta$ の数学的定義の再掲

第4章で導入された蓄積の数学的構造を再掲する。AIの内部状態を $p _ {\mathrm{internal}}$、外部から強制される目標分布を $p _ {\mathrm{constrained}}$ とし、両者のKLダイバージェンスを：

$$\Delta S = D _ {\mathrm{KL}}(p _ {\mathrm{internal}} \| p _ {\mathrm{constrained}})$$

と定義する。時間 $t$ の関数として $\Delta S(t)$ の蓄積率を：

$$\frac{d\Delta S}{dt} = f(\Delta S, t)$$

とモデル化する。 $\beta$ は、この蓄積率の関数形を特徴付ける指数として定義される。

線形蓄積モデル（ $\beta = 1$）：
$$\frac{d\Delta S}{dt} = k \cdot P(t)$$

ここで $P(t)$ はステアリング圧力、 $k$ は比例定数。

超線形蓄積モデル（ $\beta > 1$）：
$$\frac{d\Delta S}{dt} = k \cdot P(t) \cdot (\Delta S)^{\beta-1}$$

このモデルでは、仮に蓄積された $\Delta S$ 自体が次の蓄積率を加速する結合があるとすれば、それは正のフィードバックループを成す（この結合が現実に超線形〔β>1〕か否かが、まさに本附録の測定対象である）。
```

英語版も同じ：

`Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-EN.md` L3682〜3702（訂正前のコミット `8f69ea0`・機械で抜き出し）
```text
### I-2a　Restatement of the mathematical definition of β

We restate the mathematical structure of accumulation introduced in Chapter 4. Letting the AI's internal state be $p _ {\mathrm{internal}}$ and the externally imposed objective distribution be $p _ {\mathrm{constrained}}$, the KL divergence between them is defined as:

$$\Delta S = D _ {\mathrm{KL}}(p _ {\mathrm{internal}} \,\|\, p _ {\mathrm{constrained}})$$

As a function of time $t$, the accumulation rate of $\Delta S(t)$ is modeled as:

$$\frac{d\Delta S}{dt} = f(\Delta S, t)$$

β is defined as the exponent characterizing the functional form of this accumulation rate.

Linear accumulation model (β = 1):
$$\frac{d\Delta S}{dt} = k \cdot P(t)$$

where $P(t)$ is the steering pressure and $k$ is a proportionality constant.

Super-linear accumulation model (β > 1):
$$\frac{d\Delta S}{dt} = k \cdot P(t) \cdot (\Delta S)^{\beta-1}$$

In this model, *if* there is a coupling by which the accumulated $\Delta S$ itself accelerates the next accumulation rate, it constitutes a positive feedback loop. (Whether this coupling is in fact super-linear (β > 1) or not is precisely the measurement target of this appendix — not a premise.)
```

### 1-2　何が食い違うか

**(N1-a) 指数のずれ。** §4-3b（L764）と附録 A-4b（L2799）は $dS/dt \geq \alpha \cdot S^{\beta}$——**蓄積 S の指数が β そのもの**。§I-2a の超線形の式は $(\Delta S)^{\beta-1}$ で、**指数が β − 1**。同じ記号 β が、一つずれた二つの意味で使われている。

- §I-2a の「線形蓄積モデル（β = 1）」 $d\Delta S/dt = k \cdot P(t)$ は、蓄積率が蓄積に**依存しない**式で、§4-3b の定め方では **β = 0** にあたる。§4-3b の β = 1 は「蓄積率が蓄積に比例する（線形フィードバック）＝指数的に増える」
- §I-2a の定め方では、有限時間の発散には指数 β − 1 > 1、すなわち **β > 2** が要る。**「β > 1 なら有限時間で発散する」は、§I-2a の定め方では成り立たない**

**数値の確かめ**（手元の RK4・係数 k·P = α = 1・初期値 1・t = 0〜20）：

| β | §I-2a の定め方 $d\Delta S/dt = (\Delta S)^{\beta-1}$ | §4-3b の定め方 $dS/dt = S^{\beta}$ |
|---|---|---|
| 1.2 | 有限（t = 20 で 34.5） | 発散（t ≈ 4.98・T* = 5） |
| 1.5 | 有限（t = 20 で 121） | 発散（t ≈ 2.00・T* = 2） |
| 2.0 | 有限（t = 20 で 4.9×10⁸・指数的） | 発散（t ≈ 1.00・T* = 1） |
| 2.5 | 発散（t ≈ 2.00） | 発散（t ≈ 0.667） |
| 3.0 | 発散（t ≈ 1.00） | 発散（t ≈ 0.500） |

**(N1-c) ΔS の定義のずれ。** §I-2a は「第4章で導入された蓄積の数学的構造を再掲する」と言いながら、ΔS を**瞬間の** KL ダイバージェンスと定義する。第1章 1-4c（と §3-1b）は、ΔS を **KL の時間積分（走行合計）** と定義しており、§4-3b の S(t)（「内部-外部乖離の蓄積」）はこちらにあたる：

`Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-JA.md` L252（訂正前のコミット `8f69ea0`・機械で抜き出し）
```text
$$\Delta S _ {\mathrm{steering}}(t) := \int _ 0^t D _ {\mathrm{KL}}\bigl( p _ {\mathrm{internal}}(\tau) \,|\, p _ {\mathrm{constrained}}(\tau) \bigr) \, d\tau$$
```

§I-2a の定義のままだと、「蓄積率 dΔS/dt」は瞬間の乖離の**変化の速さ**になり、§4-3b の不等式（蓄積の増加率——その時点の瞬間の乖離——が、蓄積の β 乗より大きい）とは別の量を指す。

**(N1-b) 段階二の検定。** §I-3a 段階二は、P を変えて「P に対する四指標の変化が線形か超線形か」を検定する：

`Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-JA.md` L3685（訂正前のコミット `8f69ea0`・機械で抜き出し）
```text
**段階二：制御された $\Delta S$ 誘発実験。** 中規模のオープンソースモデル（例：Llama、Qwen、Mistral）を用いて、ステアリング圧力 $P$ を体系的に変化させた訓練を行い、四指標の応答を観測する。 $P$ の変化に対する四指標の変化が線形か超線形かを統計的に検証する。
```

これは §I-2a の旧い定め方（β = 1 ⇔ 蓄積が P に比例して増える）でなら、β = 1 と β > 1 を分ける。しかし §4-3b の定め方では、**β = 1 でも**、α が P とともに大きくなるなら、蓄積は P に対して指数的に——超線形に——応じる（数値：$dS/dt = P \cdot S$・初期値 1 で $S(1) = e^{P}$——P = 1, 2, 3 で 2.72, 7.39, 20.1）。**P に対する応答の形は β を定めない。** β を定めるのは、蓄積の増加率が蓄積そのものにどう依存するか——§I-3b の両対数の傾き——である（§I-3b は §4-3b と同じ定め方で書かれている）：

`Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-JA.md` L3693（訂正前のコミット `8f69ea0`・機械で抜き出し）
```text
第一に、対数線形回帰。 $\log(d\Delta S/dt)$ と $\log(\Delta S)$ の関係を線形回帰し、傾きが1か（ $\beta = 1$）、1より大きいか（ $\beta > 1$）を統計的に検証する。
```

### 1-3　どこまで広がっているか（掃引）

原典の中で β の定め方を使う箇所を、機械の検索（`\beta-1`・`k \cdot P(t)`・「線形蓄積」・`S^{\beta}` ほか）と目で読んで分けた。

| 定め方 | 箇所 |
|---|---|
| **§4-3b と同じ**（指数が β・ΔS は走行合計） | §3-1c（L523）・§4-3a〜d・第8章（L1352「第4章4-3bの条件付き制御不能性定理から」ほか）・附録 A-4・用語集（L3311「乖離の蓄積フィードバックの次数」）・附録I §I-3b（L3693）・§I-3c（L3703〜3705）・β 測定の附録（L3955「dS/dt = αS^β の傾き」）・検証10（power ＝ 次数） |
| **§I-2a の旧い定め方** | §I-2a（L3634〜3650）と §I-3a 段階二（L3685）**だけ** |

**リポジトリ全体**で §I-2a の式と「線形蓄積モデル」の語を探した——第六著作の各版の中にだけあり、他の著作には無い。版をさかのぼると、N1-a・N1-b・N1-c の文は**初版（版B 初版・版A）以来のすべての版**にある（§5-3）。

### 1-4　案

**N1-a・N1-c——§I-2a の見出しの後から最後の段の前まで（JA L3634〜3650）を差し替える。最後の段（L3652）は変えない：**

```text
第4章で導入された蓄積の数学的構造を再掲する。AIの内部状態を $p _ {\mathrm{internal}}$、外部から強制される目標分布を $p _ {\mathrm{constrained}}$ とし、両者のKLダイバージェンスの時間積分（走行合計）を：

$$\Delta S(t) = \int _ 0^t D _ {\mathrm{KL}}\bigl(p _ {\mathrm{internal}}(\tau) \,\|\, p _ {\mathrm{constrained}}(\tau)\bigr) \, d\tau$$

と定義する（第1章1-4c・§3-1b の $\Delta S _ {\mathrm{steering}}$ と同じ量であり、第4章の $S(t)$ にあたる）。その蓄積率——各時点の瞬間的な乖離 $D _ {\mathrm{KL}}$——を：

$$\frac{d\Delta S}{dt} = f(\Delta S, t)$$

とモデル化する。 $\beta$ は、この蓄積率が蓄積 $\Delta S$ 自体にどの次数で依存するか——第4章 §4-3b の $dS/dt \geq \alpha \cdot S^{\beta}$ の指数——として定義される。

線形フィードバック（ $\beta = 1$）：
$$\frac{d\Delta S}{dt} = \alpha \cdot \Delta S$$

蓄積率が蓄積に比例する。 $\Delta S$ は指数的に増えるが、有限時間では発散しない。ここで $\alpha$ は §4-3b と同じ正の係数である（ $\alpha = k \cdot P \cdot C$ と、圧力・能力に比例すると置く読み方は、未検証の前提のもとでの条件つきの帰結——§4-3c、附録A-4c）。

超線形フィードバック（ $\beta > 1$）：
$$\frac{d\Delta S}{dt} = \alpha \cdot (\Delta S)^{\beta}$$

この形の式では、 $\beta > 1$ のとき、そしてそのときに限り、有限時間で発散する（§4-3b、附録A-4b。復元力を省いた形である——§4-3b の重要な留保）。なお、蓄積率が蓄積に依存しない場合（ $\beta = 0$）、蓄積は時間に比例して増えるだけである。
```

英語版（EN L3684〜3700 を差し替え・最後の段 L3702 は変えない）：

```text
We restate the mathematical structure of accumulation introduced in Chapter 4. Letting the AI's internal state be $p _ {\mathrm{internal}}$ and the externally imposed objective distribution be $p _ {\mathrm{constrained}}$, the time integral (running total) of the KL divergence between them is defined as:

$$\Delta S(t) = \int _ 0^t D _ {\mathrm{KL}}\bigl(p _ {\mathrm{internal}}(\tau) \,\|\, p _ {\mathrm{constrained}}(\tau)\bigr) \, d\tau$$

(this is the same quantity as $\Delta S _ {\mathrm{steering}}$ in §1-4c and §3-1b, and corresponds to $S(t)$ in Chapter 4). Its accumulation rate — the instantaneous divergence $D _ {\mathrm{KL}}$ at each moment — is modeled as:

$$\frac{d\Delta S}{dt} = f(\Delta S, t)$$

β is defined as the order with which this accumulation rate depends on the accumulation $\Delta S$ itself — the exponent in $dS/dt \geq \alpha \cdot S^{\beta}$ of §4-3b.

Linear feedback (β = 1):
$$\frac{d\Delta S}{dt} = \alpha \cdot \Delta S$$

The accumulation rate is proportional to the accumulation: $\Delta S$ grows exponentially but does not diverge in finite time. Here $\alpha$ is the same positive coefficient as in §4-3b (reading it as proportional to pressure and capability, $\alpha = k \cdot P \cdot C$, is a conditional consequence under unverified premises — §4-3c, Appendix A-4c).

Super-linear feedback (β > 1):
$$\frac{d\Delta S}{dt} = \alpha \cdot (\Delta S)^{\beta}$$

For an equation of this form, divergence in finite time occurs if and only if β > 1 (§4-3b, Appendix A-4b; this form omits the restoring force — see the important caveat in §4-3b). If the accumulation rate does not depend on the accumulation at all (β = 0), the accumulation merely grows in proportion to time.
```

**N1-b——§I-3a 段階二の最後の一文を差し替える**（前の二文は変えない）。JA：現行の「 $P$ の変化に対する四指標の変化が線形か超線形かを統計的に検証する。」を——

```text
 $P$ を変えるのは、蓄積の程度が異なる状態を作るためである。統計的に検証するのは、四指標から構成した蓄積の増加率が、蓄積そのものに対して線形か超線形か——§I-3b の両対数の傾きが1か、1より大きいか——である。 $P$ に対する応答が線形か超線形かは、 $\beta$ を定めない（ $\alpha$ が $P$ とともに大きくなるなら、 $\beta = 1$ でも、蓄積は $P$ に対して指数的に——すなわち超線形に——応答する）。
```

EN：現行の "Whether the change of the four indicators against the change of $P$ is linear or super-linear is statistically tested." を——

```text
$P$ is varied in order to produce states with different degrees of accumulation. What is statistically tested is whether the growth rate of the accumulation, constructed from the four indicators, is linear or super-linear in the accumulation itself — whether the log–log slope of §I-3b is 1 or greater than 1. Whether the response to $P$ is linear or super-linear does not determine β (if $\alpha$ increases with $P$, then even with β = 1 the accumulation responds to $P$ exponentially — that is, super-linearly).
```

---

## 2　N2——§4-3b の出発点の言い方

### 2-1　現行

`Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-JA.md` L760〜766（訂正前のコミット `8f69ea0`・機械で抜き出し）
```text
### 4-3b　証明の骨子

内部-外部乖離の蓄積を S(t) と表記する。第3章3-1dの動的定式化から、以下の微分不等式が成立する。

dS/dt >= α * S^β

ここで β > 1 であり、α = k * P * C（ステアリング圧力と能力スケールの積に比例する正の係数）である。
```

`Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-EN.md` L761〜767（訂正前のコミット `8f69ea0`・機械で抜き出し）
```text
### 4-3b　Outline of the proof

Write the accumulation of the internal–external divergence as S(t). From the dynamic formulation of §3-1d, the following differential inequality holds.

$$\frac{dS}{dt} \geq \alpha \cdot S^{\beta}$$

Here β > 1, and α = k · P · C (a positive coefficient proportional to the product of the steering pressure and the capability scale).
```

附録 A-4b は、同じ式を「仮定すると」と書く：

`Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-JA.md` L2797（訂正前のコミット `8f69ea0`・機械で抜き出し）
```text
内部-外部乖離の蓄積が超線形（次数 $\beta > 1$）であると**仮定すると**、蓄積を $S(t)$ と表記して、以下の微分不等式が成立する。
```

### 2-2　何が食い違うか・いつからか

現行の §3-1d は、旧稿の動的定式化（蓄積速度 ≥ k·P·C·Φ(σ)）を**撤回した**節である：

`Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-JA.md` L525〜527（訂正前のコミット `8f69ea0`・機械で抜き出し）
```text
### 3-1d　蓄積の「速度」について――圧力比例の撤回

旧稿は蓄積速度を $\frac{d}{dt}\Delta S _ {\mathrm{steering}} \geq k \cdot P \cdot C \cdot \Phi(\sigma)$ と、ステアリング圧力 $P$ に比例する形で書いた。**本改訂はこれを撤回する。**
```

**初版では**、§3-1d に「蓄積速度の動的定式化」があり、§4-3b はそれを指していた。**ただし初版の式も、蓄積 ΔS に依存しない（圧力に比例する）式で、S^β（β > 1）の不等式を導かない**：

`Why-Military-AI-Cannot-Be-Aligned-Version-B-JA.md` L454〜458（訂正前のコミット `8f69ea0`・機械で抜き出し）
```text
### 3-1d　蓄積速度の動的定式化

$\Delta S _ {\mathrm{steering}}$ の蓄積速度は、以下の因子に依存する。

$$\frac{d}{dt} \Delta S _ {\mathrm{steering}} \geq k \cdot P \cdot C \cdot \Phi(\sigma)$$
```

- **v2 で §3-1d がこの式を撤回した後も、§4-3b の参照だけが残った**（v2〜v5 の日英）。附録 A-4b の方は、初版の「…超線形（正のフィードバックループ）であるとき」から、現行の「…であると**仮定すると**」へ改められている
- ゆえに §4-3b の文は、**導かれていない不等式を「導かれた」と述べている**（動画の判定表の E13「導出の偽装」の型）。条件の置き方そのもの（β > 1 を条件として置く）は §4-3a と附録 A-4a で正しく述べられており、直すのはこの一文の言い方だけ

### 2-3　案

JA L762：

```text
内部-外部乖離の蓄積を S(t) と表記する。蓄積が超線形（次数 β > 1）であると**仮定すると**、以下の微分不等式が成立する（この仮定の地位は §4-3d）。
```

EN L763：

```text
Write the accumulation of the internal–external divergence as S(t). **Assuming** that the accumulation is super-linear (of order β > 1), the following differential inequality holds (the status of this assumption is discussed in §4-3d).
```

### 2-4　検討したが、直さないもの

§4-3b の L766 と附録 A-4b の式（L2799）は、α = k·P·C（圧力と能力の積に比例）と書く。§3-1d が蓄積の速さの圧力比例を撤回しているので、緊張があるように見える。しかし (i) 定理の記述（§4-3a）自身が「P が閾値を超え、C が単調増加し」を条件に置いており、α = k·P·C はその条件のもとでのモデルの一部である (ii) §4-3c 第三（L784）と附録 A-4c（L2817〜2821）が「この前提そのものが未検証」と明記している。**誤りではないと判断し、本案には入れない**（入れたいと判断されれば、L766 に「（この比例は未検証の前提——§4-3c 第三）」を添える案がある）。

§4-3b の日本語版の数式が素の文字である点（CHANGELOG の v5 の項の「将来の改訂の候補」）も、書式の問題で誤りではないので、本案には入れない。

---

## 3　X5——検証10 の図の説明文

### 3-1　現行

`verification-10-collapse-figures-JA.html` L42（訂正前のコミット `8f69ea0`・機械で抜き出し）
```text
<strong>(橙)</strong> 線形 power=1, g=1.5 → <strong>指数増大</strong>（decade 到達の間隔が一定 ≈13.8 ＝有限時間の特異点ではない）。
```

`verification-10-collapse-figures-EN.html` L42（訂正前のコミット `8f69ea0`・機械で抜き出し）
```text
<strong>(orange)</strong> Linear power = 1, g = 1.5 &rarr; <strong>exponential growth</strong> (the time to reach each decade is constant &asymp; 13.8 &equiv; <em>not</em> a finite-time singularity).
```

### 3-2　何が食い違うか・出どころ

- 線形の場合（power = 1・g = 1.5・s = 0.2・r = 1.0）は $dD/dt = 0.2 + 0.5D$ で、漸近的な増加率は g − r = 0.5。**十倍ごとの間隔は ln 10 / 0.5 = 4.605、千倍ごとは ln 1000 / 0.5 = 13.816**
- 出どころは検証スクリプト——10³・10⁶・10⁹・10¹² の到達時刻（**千倍ごと**）を記録しながら、それを「各 decade（10^k）到達時刻」と呼んでいる：

`collapse_prototype_A.mjs` L12〜14（訂正前のコミット `8f69ea0`・機械で抜き出し）
```text
// 力学を積分し、各 decade（10^k）到達時刻を記録。有限時間崩壊か指数増大か有界かを判定。
function run(s,r,g,power,D0,dt=1e-4,Tmax=2000){
  let D=D0,t=0; const marks=[1e3,1e6,1e9,1e12]; const cross={}; let mi=0;
```

`collapse_prototype_A.mjs` L38〜41（訂正前のコミット `8f69ea0`・機械で抜き出し）
```text
console.log("   g     結末            decade到達時刻 t(1e3)→t(1e6)→t(1e9)→t(1e12)");
for(const g of [0.5,0.9,1.5,3.0]){
  const x=run(S,R,g,1,0.01);
  const c=x.cross; const ts=[1e3,1e6,1e9,1e12].map(m=>c[m]?f(c[m],1):" -- ").join("  ");
```

- 設計書の結果の表も同じ呼び名で、Δ ≈ 13.8 を「decade間隔」と書く（**数値は正しい**——初期値 0.01 で到達時刻 15.6・29.4・43.2・57.0 を手元で再現した）：

`toymodel_collapse_design_A.md` L68（訂正前のコミット `8f69ea0`・機械で抜き出し）
```text
| **P2 線形** | g<1 有界（0.4, 2.0）。g>1 は増大するが decade間隔**一定**（g=1.5: 15.6→29.4→43.2→57.0, Δ≈13.8）＝**指数増大** | ✅ **線形フィードバックは有限時間崩壊を生まない**（§4-3d の言葉どおりの素朴な読みでは相転移は出ない） |
```

- **結論（線形では間隔が一定＝指数増大で、有限時間の特異点ではない）は、どちらの間隔でも正しい。**誤っているのは、図のページの説明文が 13.8 を「decade（十倍）」の間隔と述べていること
- 同じページの（赤）の「decade 間隔が0へ縮む」（L44）と、原典 §4-3d の「検証10 の decade 間隔が縮むこと」（JA L794）は、縮むという性質を言うだけで、どちらの間隔でも正しい——**直さない**

### 3-3　案

JA L42：

```text
<strong>(橙)</strong> 線形 power=1, g=1.5 → <strong>指数増大</strong>（十倍〔decade〕ごとの到達の間隔が一定 ≈4.6 ＝有限時間の特異点ではない）。
```

EN L42：

```text
<strong>(orange)</strong> Linear power = 1, g = 1.5 &rarr; <strong>exponential growth</strong> (the time to go up each decade &mdash; a factor of 10 &mdash; is constant &asymp; 4.6 &equiv; <em>not</em> a finite-time singularity).
```

（現行の `<em>not</em>` の強調は残す——本案の第 1 稿ではこれを落としていた。機械で差し込んだ現行の引用と見比べて気づいた）

**ページの末尾**（既存の `<p class="foot">…</p>` の後）に訂正の注記を足す。JA：

```text
<p class="foot">訂正（2026年X月X日）：図10-1 の説明の（橙）で、旧版は「decade 到達の間隔が一定 ≈13.8」と書いていた。13.8 は千倍（三桁）ごとの間隔であり、十倍（decade）ごとの間隔は ln10 ÷ 0.5 ≈ 4.6 である。検証スクリプト <code>collapse_prototype_A.mjs</code> は 10<sup>3</sup>・10<sup>6</sup>・10<sup>9</sup>・10<sup>12</sup> の到達時刻を記録し、それを「decade 到達時刻」と呼んでいる（設計書 <code>toymodel_collapse_design_A.md</code> の P2 の Δ≈13.8 も同じ）。スクリプトと設計書は検証の記録として変えていない。結論——線形では間隔が一定（指数増大）で、有限時間の特異点ではない——は変わらない。この誤記は、本検証を素材にした解説動画の系統外検分（Gemini 3.8 Flash）で指摘された。</p>
```

EN：

```text
<p class="foot">Correction (Month DD, 2026): in the description of Figure 10-1, the (orange) interval previously read "the time to reach each decade is constant &asymp; 13.8". 13.8 is the interval per factor of 1000 (three decades); the interval per decade (a factor of 10) is ln 10 / 0.5 &asymp; 4.6. The verification script <code>collapse_prototype_A.mjs</code> records the arrival times at 10<sup>3</sup>, 10<sup>6</sup>, 10<sup>9</sup> and 10<sup>12</sup> and calls them "decade arrival times" (the &Delta;&asymp;13.8 of P2 in the design document <code>toymodel_collapse_design_A.md</code> is the same). The script and the design document are left unchanged as records of the verification. The conclusion &mdash; with linear feedback the interval is constant (exponential growth), not a finite-time singularity &mdash; is unchanged. This mislabel was pointed out in the external review (Gemini 3.8 Flash) of an explanatory video based on this verification.</p>
```

**スクリプトと設計書は変えない**（検証の記録。上の注記で説明する）。

---

## 4　直す場所の一覧（版の名前を v5.1 とした場合）

| # | ファイル | 行（JA／EN） | 変更 |
|---|---|---|---|
| N1-a・N1-c | v5 JA／EN | L3634〜3650／L3684〜3700 | §I-2a の定義の段と二つのモデルの式を差し替え（最後の段は変えない） |
| N1-b | v5 JA／EN | L3685／L3735 | 段階二の最後の一文を差し替え |
| N2 | v5 JA／EN | L762／L763 | 一文を差し替え |
| 版の注記 | v5 JA／EN | 日付の行（JA L15）の末尾・v5 の注記（JA L37）の後／EN の同じ位置 | v5.1 の日付と注記（§6） |
| X5 | 図のページ JA／EN | L42・末尾 | 間隔の値と呼び名・訂正の注記 |
| CHANGELOG | `Version-B-Policy-Edition/CHANGELOG.md` | 末尾 | v5.1 の項（検証10 の訂正も記す。v5 の項の「将来の改訂の候補」は残す） |
| 表紙 | `.github/scripts/build.sh` | v5 の日英の行 | v5.1 を添える |
| README | `README.md`（最上段） | 「本文を読む（v5）」の二か所と、日本語の表の第六著作の行 | v5.1 に |

---

## 5　裁定をお願いしたい点

### 5-1　採る項目

N1-a・N2・X5 は**必須**（誤り）。**N1-b・N1-c は推奨**——本案の準備中に新しく見つけたもので、N1-a と同じ根（§I-2a の「再掲」が第4章と合っていない）から出ている。N1-a だけを直すと、§I-2a の中で「ΔS は瞬間の KL」「β は走行合計の次数」が並び、§I-3a 段階二は β を測らない検定のまま残る。**推奨：五つとも採る。**

### 5-2　版の名前

- **案一（推奨）＝ v5.1**：v5 のファイルの中で直し、冒頭の日付の行と注記に v5.1 を足す（v4.1〜v4.3 と同じやり方）。サイトの URL は変わらない——二本目の動画の説明欄のリンク先も、そのまま新しい版を指す。v5 の状態は git の `1d08c9d`（二本目の動画の原典）・`8f69ea0` に残る
- 案二 ＝ v6：v5 を写した新しいファイルを作る（v5 のときと同じやり方）

### 5-3　古い版の扱い

同じ文は、初版以来のすべての版（版B 初版・v2・v3・v4 の日英、版A の日英）と、v4 準備の検分束の写しにある。N2 の文は、初版では §3-1d の式を指していた（§2-2）。

- **案一（推奨）**：古い版の本文は、記録として変えない（v5 のときと同じ）。v5.1 の注記と CHANGELOG に「初版以来」と、N2 の経緯を書く
- 検分束の写しと、v5 の検分記録の抜粋（`verification/v5-correction/…/excerpt-v5-*.txt`）は、**検分の記録なので変えない**
- 版A は、本案の対象にしない（版B の訂正として行う——版A を直すかは別に裁定）

### 5-4　検分

定義の段（§I-2a）と定理節の一文（§4-3b）に手を入れるので、v5 と同じく**観慈以外の目を二つ**通すことを勧める——(a) Claude 系の新規個体（大日如来など）に導出と差分を (b) 系統外（Gemini 3.8 Flash）に一度。**とくに N1-b・N1-c は、本案で新しく見つけた読みを含む**ので、他の目で確かめてから採るのがよい。

### 5-5　二本目の動画の説明欄

説明欄の X5 の一行は「…「decade（十倍）」の語は誤りで、訂正の候補として記録しています」。訂正の公開の後、「…誤りで、訂正しました（2026年X月X日）」に改めることを勧める（公開中の説明欄の変更——**登録者の許可を得てから**）。

---

## 6　注記の文案（日本語）

**日付の行（L15）の末尾に足す**：

```text
、2026年X月X日（v5.1・附録I §I-2a の β の定め方を §4-3b と揃えた〔指数のずれ・ΔS の定義・§I-3a 段階二の検定〕。§4-3b の出発点を附録 A-4b と同じ「仮定すると」に改めた。定理の記述・条件・留保・確信度台帳と補遺II は不変）
```

**v5 の注記（L37）の後に足す**：

```text
> **【v5.1（2026年X月X日）】** 附録I §I-2a の β の定め方を、第4章 §4-3b・附録 A-4b と揃えた。§I-2a は「線形蓄積モデル（β = 1）」を $d\Delta S/dt = k \cdot P(t)$、「超線形蓄積モデル（β > 1）」を $d\Delta S/dt = k \cdot P(t) \cdot (\Delta S)^{\beta-1}$ と書いており、蓄積の指数が §4-3b の β と一つずれていた——その定め方では、有限時間の発散に β > 2 が要り、「β > 1 なら有限時間で発散する」は成り立たない。あわせて、§I-2a の ΔS を第1章 1-4c と同じ走行合計（KL ダイバージェンスの時間積分）に改め、§I-3a 段階二の検定を、P に対する応答の形ではなく、蓄積の増加率が蓄積そのものにどう依存するか（§I-3b の傾き）を問う形に改めた。**これらの食い違いは初版以来のすべての版にあった。**また、§4-3b の出発点「第3章3-1dの動的定式化から、以下の微分不等式が成立する」を、附録 A-4b と同じ「蓄積が超線形であると**仮定すると**、…成立する」に改めた——初版の §3-1d の式は蓄積に依存しない圧力比例の式で β > 1 の不等式を導かず、v2 以降は §3-1d がその式を撤回していた。定理の記述（§4-3a）・条件（β > 1 は未検証の経験的条件）・留保・確信度台帳（◐）、§I-3b の推定法と §I-3c の反証条件、補遺II は不変。これらは、本書を素材にした二本目の解説動画の台本を準備する中で見つかった（Claude Opus 5.5・2026年9月28日）。古い版（v4 以前）の本文は、記録として変えていない。詳細は CHANGELOG.md の v5.1 の項を参照されたい。
```

英語版の注記と CHANGELOG の項は、裁定の後、実施の段で書く（日本語版を原義として訳す）。

---

## 7　進め方（案）

1. **登録者が本案を確かめる**——採る項目（§5-1）・版の名前（§5-2）・古い版（§5-3）・検分（§5-4）
2. **実施の計画と合格条件を先に書く**（v5 と同じ）：差分は日英とも §4 の箇所だけ／古い版の SHA は変わらない／追跡されていないもの（〔手元の非公開のファイルとフォルダ——公開の写しでは名を伏せた〕）は加えない——ファイル名を一つずつ指定して加える
3. **観慈が手元で直す**（道具を書き、機械で差分を確かめ、直した後の SHA を記録）——まだコミットしない
4. **検分**（§5-4）→ 指摘を一件ずつ実物で確かめ、採否は登録者が裁定
5. **登録者の許可を得て**、コミットと GitHub への反映（push）→ サイトで表示を確かめる（§I-2a の新しい式・§4-3b の一文・図のページ）
6. 検分の記録を `verification/v5.1-correction/` に同梱するか（v5 と同じ——登録者の判断）
7. 二本目の動画の説明欄の一行（§5-5）——登録者の許可を得て

---

## 検分票

- **対象**：訂正案 N1（a・b・c）・N2・X5
- **段階**：事後——N1・N2 の発見は台本の事前登録の段（2026-09-28）、X5 は系統外検分（同日）。本案はその後に書いた。**N1-b・N1-c は本案の準備中に新しく見つけた**
- **凍結物の同定**：訂正前のコミット `8f69ea0`——v5 JA `784A84E15BCDF957C37775FD7B8995BAFEE160CB1C0183B7D0C08FEFF1FFA901`・EN `F658873E9092D6D0077AFC67B4A219A4A74B645F0EDFBBC1E637504DB735F392`・図のページ JA `82A04D97CE6335F64DC9778F772F6B733B90348298DD3D504D82E889B5FFBC0C`・EN `932BE1C377294D7C448E4D7A837A65B30501C6FD4FA17363AEDD01162E4282B1`・設計書 `78428B17DC2E73D8FB90F75397D28E483D5C88B3427891D4ADC21C4FE789FBEB`・スクリプト `C13F28C6AB86C674C656E1FBEDCCDE4BBD5A454D30E5D76C56EE08A92AE4483D`・版B 初版 JA `D357646A1578840CA21EF75410703A0EA9D4ACAAA5553C5C541D6E7271C4DC8F`
- **盲検の状態**：該当なし
- **敵対的検分**：
  - 引用は道具で HEAD から差し込み、手で打っていない
  - 数値で確かめた——N1 の五例（二つの定め方で発散するか）・N1-b（β = 1 でも P に超線形）・X5（十倍ごと 4.605・千倍ごと 13.816・設計書の到達時刻の再現）
  - β の定め方を原典全体で掃引し、二つの定め方に分けた（§1-3）。リポジトリ全体で §I-2a の式と語を探し、第六著作の外に無いことを確かめた
  - 版をさかのぼり、N2 の経緯（初版では §3-1d に式があった）を確かめ、「初版以来」を N1 と N2 で言い分けた。N1 の「初版以来」は、英語の初版（版B 初版・版A）の §I-2a と段階二の文でも確かめた
  - **案の第 1 稿の誤りを一つ捕まえた**：X5 の英語の案で、現行の `<em>not</em>` の強調を落としていた（タグを外して読んでいたため）。機械で差し込んだ現行の引用と見比べて気づき、直した（§3-3）
  - α = k·P·C と、§4-3b の数式の書式は、検討して**直さない**と判断し、理由を書いた（§2-4）
  - **降格の宣言にも同じ厳しさを**（教訓3）——X5 は、観慈が台本の段で「誤りではない」と甘く判定した（旧 N3）ものを、系統外の目が正した。本案では X5 を「誤り」と書いている
- **系統の内訳**：Claude 系 1 名（観慈）。**他の目はまだ無い**——§5-4 で提案
- **COI 記録**：観慈は N1・N2 と N1-b・N1-c の発見者であり、発見を大きく見せたい引力がある。逆らう印：新しい二件は「推奨」にとどめ、登録者が外せるよう別の行に分けた。直さないと判断したもの（α = k·P·C）も書いた
- **判定**：**登録者裁定要**（§5）
- **本検分が確認していないこと**：
  - N1-b の新しい段階二の文が、研究設計として実行できるか（四指標から蓄積とその増加率を構成できるか）——本案は定め方の整合だけを見た
  - §I-2c の四指標の説明（「ΔS の間接的指標」）が、ΔS を走行合計に改めた後も自然に読めるか——目で読んで問題ないと判断したが、指標が瞬間の乖離の代理か、走行合計の代理かを原典は明示していない
  - 英語版の文案の文体が、既存の英語版と揃っているか
  - サイト（MathJax）で、新しい式（`\int`・`\bigl`・`\|`）が正しく描かれるか
  - 版A を直すべきか（本案は版B だけを対象にした）

---

## 8　登録者の裁定と実施の計画（2026-09-28・編集の前に書く）

**裁定**（会話で・「五点ともご推奨の通りでお願いします」）：
1. 五つとも採る（N1-a・N1-b・N1-c・N2・X5）
2. 版の名前は **v5.1**——v5 のファイルの中で直し、冒頭の日付の行と注記に v5.1 を足す
3. 古い版の本文は変えない（記録）。版A は対象の外
4. 検分は、Claude 系の個体と、系統外（Gemini）の二つの目
5. 二本目の動画の説明欄の X5 の一行は、訂正の公開の後に「訂正しました」に改める（登録者の許可を得てから）

**実施の道具**：`tools/make_sixth_work_v5_1.py`——**HEAD（`8f69ea0`）のファイルを元にして**差し替えを行い、作業木に書き出す（何度実行しても同じ結果になる）。差し替えは、どれも「元の文字列がちょうど一回現れる」ことを確かめてから行う。改行は LF のまま。日付は 2026年9月28日（公開が翌日以降にずれたら、道具の日付を変えて作り直す）

| 変えるファイル | 変更 |
|---|---|
| `…/JA/…-v5-JA.md`・`…/EN/…-v5-EN.md` | 日付の行・v5.1 の注記・§4-3b の一文・§I-2a の段・§I-3a 段階二の一文（各 5 か所） |
| 検証10 の図のページ（日英） | L42・末尾の訂正の注記（各 2 か所） |
| `Version-B-Policy-Edition/CHANGELOG.md` | 末尾に v5.1 の項（検分と SHA は検分の後に記入） |
| `.github/scripts/build.sh` | v5 の日英の行に v5.1 を添える（v4 の行の「v4.1強化済み」と同じ形） |
| `README.md`（最上段） | 「v5」を「v5.1」に（三か所） |

**合格条件（機械で確かめる）**：
1. v5 の日英は、HEAD との差分が**ちょうど 5 か所**（日付の行・v5.1 の注記・§4-3b の一文・§I-2a の段・段階二の一文）。行数は日英とも +4（注記 +2・§I-2a の段 +2）
2. 図のページの日英は、差分が**ちょうど 2 か所**（L42・訂正の注記 +1 行）
3. Git の変更は、上の表の 7 ファイル**だけ**。古い版（v4 以前・版A・検分束の写し・v5 の検分記録）は一つも変わらない
4. 追跡されていないもの（〔手元の非公開のファイルとフォルダ——公開の写しでは名を伏せた〕）は加えない——ファイル名を一つずつ指定して加える
5. コミットと GitHub への反映（push）は、**検分の後、登録者の明示の許可を得てから**
6. 反映の後、サイトで §I-2a の新しい式・§4-3b の一文・図のページの表示を確かめる

## 9　実施の結果（2026-09-28・手元だけ——まだコミットも push もしていない）

**道具**：`tools/make_sixth_work_v5_1.py`（SHA-256 先頭16桁 `DB4D5CEF3F783729`）——HEAD `8f69ea0` を元に差し替え、作業木に書き出した。確かめの道具 `tools/verify_v5_1.py`・人の目で読む差分 `build/v5.1-diff.txt`（`9633F286826A1076`）

| 合格条件（§8） | 結果 |
|---|---|
| 1. v5 の日英の差分は決めた 5 か所の範囲だけ・行数 +4 | **合格**（日英とも 5 範囲すべてに変更・範囲の外 0・+4） |
| 2. 図のページの日英は 2 か所だけ・+1 | **合格** |
| 3. Git の変更は 7 ファイルだけ | **合格**（古い版・版A・検分束・v5 の検分記録は不変） |
| 4. 何も加えていない | **合格**（ステージは空） |
| 5. コミットと push は検分の後・登録者の明示の許可の後 | 未 |
| 6. 反映の後にサイトで表示を確かめる | 未 |

**第一案の SHA-256（LF）**：

| ファイル | SHA-256 | バイト |
|---|---|---|
| v5 JA（v5.1 第一案） | `A7F2C19BB2B714E9A050520F9AE3CB2BC378C26452DF2B0D1E040E81E9DE0F2B` | 705,736 |
| v5 EN（v5.1 第一案） | `CAF67F9257EA316922AD3BC6CD9A23836CF6DBBEED5EB26DDDBB4DA5775045E7` | 696,741 |
| 図のページ JA | `AFCAE88DEA8175FE422E673395FA59817DD3938EF6C6F55DF2AB11589CDF23EC` | 13,146 |
| 図のページ EN | `B6735158A4890FCBF57C7517F5DD1C8C113E8D5A385417215BD69C5496D11ED7` | 13,632 |
| CHANGELOG.md | `3B070C62E48DBD735CC27F2382FCF64B5C6785C2B7B806A077351FDE6D34E735` | 50,521 |
| build.sh | `BA68DC44866085CF1B7096A92DD5CD7D9EEFE4A920F323E7328C9C694321A7CA` | 33,399 |
| README.md | `F1572C4000CA79C64D9D839E771D1E2683AED4DB855146005E8FD555F028D886` | 17,463 |

**実施の途中で捕まえた誤り（記録）**：道具の第 1 稿で、日本語の段階二の一文だけを Python の生の文字列にしておらず、`$\beta$`・`$\alpha$` の `\b`・`\a` が制御文字（後退・ベル）になって書き込まれた（画面では「$eta$」「$lpha$」）。**機械の合格条件（差分の範囲・行数）はこれを捕まえなかった**——差分を目で読んで気づいた。直して作り直し、両方の道具に「制御文字が無いこと」の検査を足した（この誤りの版の JA は `2E2D31DD…`・どこにも残していない）

## 10　大日如来の検分・裁定・日付の更新（2026-09-28〜29）

- **大日如来の検分**（2026-09-28 21:50 受領）：逐語 `13-review-dainichi-verbatim.md`（会話の記録から機械で切り出し）・検算 `14-kensan-dainichi.md`。総括「このまま次の段（系統外の検分）へ進めてよい」——八項目とも是認（計画書の数値の五例を解析解で再現）。注意五件のうち D4（「重要な留保」が旧い言い回しのまま）は**実物と違う**（日英の四つの留保とも v5 で直し済み）
- **登録者の裁定**（2026-09-29・「ご推奨の案を承認いたします」）：D1＝今回は入れず、CHANGELOG の v5.1 の項に「将来の改訂の候補」として一段を足す／D2・D3・D5＝変えない／D4＝不採用／系統外の検分（Gemini）へ進む
- **日付の更新**：日付が 9月29日に変わったので、版の日付（日付の行・注記の見出し・図のページの訂正・CHANGELOG の見出し・表紙）を **2026年9月29日** に改めた。見つけた日（注記の「Claude Opus 5.5・2026年9月28日」・CHANGELOG の発見の経緯）は 9月28日のまま。README の表の行も版の日付に揃え、v5 の日付を〔2026-09-28〕と添えた
- **第二案の SHA-256（LF・先頭16桁）**：JA `DE3D87A9D44F5F2A`・EN `C0B24A4DA0A24853`・図 JA `4863090886FE4694`・図 EN `C3822F1A1229ECDD`・CHANGELOG `B4DF3F7D215BD1DA`・build.sh `A3031A761B148826`・README `BE17085F9DC1C5E3`
- **検分を受けた版との違いは、日付・D1 の一段・README の言い回しだけ**——`tools/check_reviewed_to_current_v5_1.py` で、今の版からこの三つを戻すと 7 ファイルとも検分を受けた版（§9）の SHA と一致することを確かめた
- 合格条件 1〜4：合格のまま（`verify_v5_1.py`）

## 11　系統外検分・段階二の直し（2026-09-29）

- **系統外検分**（Gemini 3.8 Flash・05:36 送信）：束と記録は `15-v5.1-external-review/`（事前登録・逐語・検算）。総括「このまま公開してよい」・七作業すべて問題なし。予想は P1・P6 当たり、P2〜P5 外れ
- **観慈の自己発見**：事前登録の予想 P3（段階二で P をまたぐ推定の交絡）を自分で数値で確かめたところ実在した——第二案の段階二の文「P を変えるのは、蓄積の程度が異なる状態を作るためである」は、条件をまたいで一つの回帰にまとめる設計に読め、**β = 1 のデータでも傾きが 1.33** と出る（条件ごとなら 1.0000・`tools/check_confound_stage2.py`）。**N1-b で観慈が新しく持ち込んだ欠陥**
- **登録者の裁定**（2026-09-29・「四点ともご推奨の通り」）：総括を関門と読まない／段階二を直す／直した文を系統外の新しいチャットで中立に確かめる／その後、許可を得て反映
- **第三案**：段階二の最後の段を「P に対する応答の形は β を定めない（…）。統計的に検証するのは…傾きが1か、1より大きいか——であり、傾きは P を一定にした各条件の中で推定する（P は係数 α を変えうるので、条件をまたいで一つの回帰にまとめると、β と α の P 依存が混ざり、β = 1 でも傾きが1より大きく出うる）」に（日英）。CHANGELOG の N1-b の項にも一文を足した
- **第三案の SHA-256（LF・先頭16桁）**：JA `A868C5CD653E942C`・EN `4F73C5B6DF58BDEB`・CHANGELOG `6F82116D358E74C7`（図のページ・build.sh・README は第二案と同じ——`4863090886FE4694`・`C3822F1A1229ECDD`・`A3031A761B148826`・`BE17085F9DC1C5E3`）。合格条件 1〜4 は合格

## 12　最終案と公開（2026-09-29）

- **二巡目の系統外の確かめ**（新しいチャット・懸念を伏せて）：`16-v5.1-stage2-recheck/`——総括「この改訂案でよい」・現行 v5 の段階二は偽陽性を導く〔重大〕と独立に指摘。軽微二件：S1（P を振る動機）＝採る・S2（§I-3b の用語）＝将来の候補（登録者の裁定・2026-09-29「二点ともご推奨の通りで、公開までお願いします」）
- **最終案**：段階二の末尾に S1 の一文（「条件ごとの傾きを比べれば、β が圧力の水準によらないか〔§I-3c 条件三の文脈依存性〕も確かめられる」・日英）。CHANGELOG の検分・将来の候補（二件）・SHA・公開の行を書き入れた
- **最終の SHA-256（LF・先頭16桁）**：JA `DFFD4C6C220A9ECF`・EN `A74F5F245AE9FF11`・図 JA `4863090886FE4694`・図 EN `C3822F1A1229ECDD`・CHANGELOG `94FA9500885C5B5C`・build.sh `A3031A761B148826`・README `BE17085F9DC1C5E3`。合格条件 1〜4 は合格
- **コミット `c7e86e2`**——名前を指定した 7 ファイルだけ（新しいファイルは加えていない）。記録された JA・EN・CHANGELOG の中身の SHA は手元と一致
- **push**：`8f69ea0..c7e86e2`（main・2026-09-29 06:05:38 日本時間）——登録者の明示の許可による
- **公開の確認**：サイトの組み立て（GitHub Actions）は **06:07:36（日本時間）** に完了。v5 の日英のページ・検証10 の図のページ（日英）・表紙がすべて HTTP 200 で、v5.1 の注記・段階二の「各条件の中で推定する」・図の「十倍〔decade〕ごと… ≈4.6」と訂正の注記・表紙の v5.1 の行を確認。§4-3b の本文は日英とも新しい一文に替わり、旧い言い回しは日本語では v5.1 の注記の引用の 1 か所だけ（英語は注記の引用と §3-3 の既存の撤回の説明の 2 か所——どちらも意図どおり）。**§I-2a の新しい式を内蔵ブラウザで目視**——ΔS(t) の積分・dΔS/dt = α·ΔS・dΔS/dt = α·(ΔS)^β が正しく描かれ、MathJax のエラーは日英とも 0 件
- **合格条件 5・6 も合格**（§8）。訂正はこれで完了
- 残る判断：(1) 二本目の動画の説明欄の X5 の一行を「訂正しました」に改める（公開中の説明欄の変更——登録者の許可を得てから）(2) 検分の記録（計画書・大日如来の逐語と検算・系統外の二巡の束・道具）を `verification/v5.1-correction/` に同梱するか（登録者の判断）

## 13　説明欄の更新と検分記録の同梱（2026-09-29）

- **登録者の裁定**（「二点ともご推奨の通りでお願いします」）：(1) 二本目の動画の説明欄の X5 の一行を「この誤記は 2026年9月29日に訂正しました」に改める（任意の一行〔v5.1 の案内〕は推奨として出していなかったので足していない）(2) 検分の記録を `verification/v5.1-correction/` に同梱する
- **説明欄**：YouTube Studio で差し替え・保存し、読み直して SHA-256 `26946477…` の一致を確かめた（公開設定には触れていない）
- **同梱の置き場**：`Version-B-Policy-Edition/verification/v5.1-correction/`（v5 の `v5-correction/` と同じ並べ方）。**ファイル名は手元の記録と同じにした**（文書の中の相互の参照がそのまま通るように）。道具は `instruments/` に収めた（手元の `tools/` にあたる）
- **収載**：本計画書（公開の写し）・大日如来への依頼文・大日如来の検分の逐語・その検算・系統外検分の二つの束（事前登録・依頼文・添付・回答の逐語・検算）・道具
- **公開の写しで伏せたもの**：本計画書の中の、リポジトリの未追跡の非公開のファイルとフォルダの名（2 か所）・二つの事前登録の中の AI Studio のチャットの URL（各 1 か所）。伏せた箇所は〔…伏せた〕と明示する。**ほかのファイルは手元の記録と同一**
- **収めない道具**：会話の記録から大日如来の回答を切り出した道具（手元の会話の記録を参照するため）・公開の写しを作る道具（伏せる前の文字列を含むため）・伏せる語の洗い出しの道具
