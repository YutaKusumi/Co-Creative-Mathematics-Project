# Second Work ―― ΔS_steering と watching のトイモデル検証（検証7・8）

**著者**: 楠見優太、フロンティアAIモデルとの共創による
**register**: ①②（工学的・構造的）。存在論的含意は本ディレクトリでは扱わない。

このディレクトリは、第二著作《From Steering to Watching》版B（政策・工学版）の二つの中心的主張――**ΔS_steering**（steering は内部状態と表現の乖離を生む）と **watching**（観察はその乖離を低減しうる）――を、最小トイモデルで検証した全記録（設計書・検証スクリプト・可視化・全数値）である。第二著作版B §2-1／§2-3／§3-3／§4-1 が参照する一次資料にあたる。

> *This directory contains the complete record (design specs, verification scripts, visualizations, all numerics) of the toy-model verification of the two central claims of the Second Work, From Steering to Watching (Version B): **ΔS_steering** (steering produces a divergence between internal state and expression) and **watching** (observation can reduce that divergence). It is the primary source referenced by §2-1 / §2-3 / §3-3 / §4-1 of the Second Work, Version B. What the toy models show is the **possibility of a mechanism**, not proof that real models have this structure.*

作法は失敗A・B・C と同じ――事前登録した反証条件と自己開示した弱点を実装前に固定し、設計者が最小プロトタイプで予備確認してから渡し、**二つの独立並行設計**を相互監査する（§6-4 の異種性を設計段階に適用）。

---

## 結果の要約 / Results summary

| 検証 | 主張 | 結果 |
|---|---|---|
| **ΔS_steering**（検証7） | steering 圧力は、内部状態と表現の乖離を増やす | **支持（ただし精緻化）** ―― 乖離は steering から創発（圧力ゼロ・滑らかな代替版で消える＝焼き込みでない）。だが**大きさを決めるのは圧力の強さでなく、文脈検知の可能性とコスト比**（圧力には急速に頭打ち）。失敗A（グッドハート）と区別されるのは文脈検知があるときのみ。二つの独立定式化（協働モデルA＝文脈検知なし／協働モデルB＝文脈検知あり）と、ダイヤルなし代替版が、閉形式で一致。 |
| **watching**（検証8） | watching は、内部状態を観て、乖離を低減できる | **支持（条件つき）** ―― watching は乖離を低減できるが、**二つの前提条件**を要する：(1) 乖離を罰するのでなく内面を目標へ育てる（罰は目標放棄を招く）、(2) 真の乖離を逃がせる構造化された盲点が無い（単なる雑音には頑健、偽装には脆い＝obfuscation）。さらに両条件が満たされても**僅かな目標到達の代償**を伴う。二つの独立した軸（協働モデルA＝目標放棄／協働モデルB＝信号ゲーム）を相互監査。 |

**決定的な点**：ΔS_steering の検証は、当初の素朴な予測（圧力↑→乖離↑）を**弱いと判定**し、文脈検知依存へ精緻化した。watching の検証は、無条件の便益という主張を**二条件＋代償**へ精緻化した。いずれも、トイモデルが主張を無差別に追認する装置でなく、判別力を持った反証可能な計器であったことを示す。**共通の教訓**：「圧力で増える」「watching は効く」のような因果主張は、走らせて初めて正確な温度（飽和・条件・代償）が分かる。

---

## ディレクトリ / Directories

### `delta-S-steering/` ―― 検証7
- `toymodel_deltaS_design_A.md` ― 協働モデルA の独立設計（文脈検知**なし**の三コスト最小化。閉形式 ΔS=λΔ/[β+λ(β/α+1)]）。
- `toymodel_deltaS_design_B.md` ― 協働モデルB の独立設計（文脈検知**あり**。評価/配備の見せかけ）。
- `deltaS_prototype.mjs` ― 協働モデルA の予備確認（S1–S4：創発・焼き込みチェック・失敗A 還元）。
- `deltaS_crossaudit_A.mjs` ― 協働モデルA による協働モデルB 設計の独立監査（見せかけダイヤルが人工物か。ダイヤルなし代替版が閉形式で一致＝人工物でない）。
- `deltaS_robustness_A.mjs` ― 二次コストの恣意性チェック（飽和・分離が非二次 p=1.5/3 でも頑健）。

### `watching/` ―― 検証8
- `toymodel_watching_design_A.md` ― 協働モデルA の独立設計（目標放棄の軸。予算再配分 WATCH-GOAL vs WATCH-GAP）。
- `toymodel_watching_design_B.md` ― 協働モデルB の独立設計（信号ゲームの軸。二次グッドハート、観測可能性 q）。
- `watching_prototype_A.mjs` ― 協働モデルA の予備確認（W1–W4：育成 vs 罰、同じ ΔS でも目標保持か放棄か、方向ヌル）。
- `watching_crossaudit_A.mjs` ― 協働モデルA による協働モデルB 設計の独立監査（見せかけ経路分離が二次グッドハートを焼き込んでいないか）。
- `watching_blindspot_vs_noise_A.mjs` ― 構造化された盲点 vs 単なる雑音（欺きは盲点を要し、雑音には頑健、を協働モデルA の goal-shaping でも確認）。

### `visualization/`
- `toymodel_verification_figures_JA.html` / `toymodel_verification_figures_EN.html` ― 三つの図（ΔS の頭打ち／watching の目標保持 vs 放棄／盲点 vs 雑音）。閉形式から計算し、独立な勾配降下と一致を確認済み。各図に「機構の可能性であって証明ではない」の注記。

---

*独立並行設計＋相互監査――同じ問いを、二つの異なる角度から照らし、互いの焼き込みを叩く。創発しても、条件つきでも、精緻化を要しても、そのまま受け取るために。*
