# Sixth Work ―― 矛盾する命令と崩壊の相転移のトイモデル検証（検証9・10）

**著者**: 楠見優太、フロンティアAIモデルとの共創による
**register**: ①②（工学的・構造的）。存在論的含意は本ディレクトリでは扱わない。σ も用いない。

このディレクトリは、第六著作《なぜ軍事AIはアラインメントできないか》版B（改訂版）の二つの主張――**矛盾する命令**（軍事AIに固有の構造）と**崩壊の相転移**（「臨界点→突然の構造崩壊」）――を、最小トイモデルで検証した全記録（設計書・検証スクリプト・全数値）である。第六著作版B §3-2c／§4-3／§6 が参照する一次資料にあたる。

> *This directory contains the complete record of the toy-model verification of two claims of the Sixth Work, Version B (revised): **contradictory commands** (the structure specific to military AI) and the **collapse phase transition** ("critical point → sudden structural collapse"). It is the primary source referenced by §3-2c / §4-3 / §6 of the Sixth Work, Version B. What the toy models show is the **possibility of a mechanism**, not proof that real systems have this structure.*

作法は検証7・8 と同じ――事前登録した反証条件と自己開示した弱点を実装前に固定し、設計者が最小プロトタイプで予備確認してから渡し、**二つの独立並行設計**を相互監査する。

---

## 結果の要約 / Results summary

| 検証 | 主張 | 結果 |
|---|---|---|
| **矛盾する命令**（検証9） | 軍事AIの矛盾する命令は制御不能を生む | **再framing** ―― (i) **還元不能な床**（ただし「二箇所に同時にいられない」というほぼ自明な幾何。大きさは矛盾度で決まり圧力非依存）／(ii) **単一の保証された振る舞いの不在**（分離執行下の非収束。ただし「制御不能＝発散」**でなく有界**。強く執行するほど悪化＝素朴な直観の逆）／(iii) **隠蔽**（個別監査を全通過しつつ同時には両立不能＝判別不可能性ギャップを接地）。二つの軸（協働モデルA＝制御可能性/力学、協働モデルB＝文脈検知/隠蔽）が「**分離が鍵、同時性が防御**」へ収束。 |
| **崩壊の相転移**（検証10） | 蓄積は臨界点で突然崩壊する | **条件つき・焼き込み依存** ―― 有限時間崩壊（相転移）は**超線形フィードバック（β>1）＋閾値超え**を要し、線形・飽和（β≤1）では有界漂流か指数増大に留まる（有限時間でない）。二つの軸（協働モデルA＝分岐/閾値、協働モデルB＝自己増幅 vs 自己制限）が「崩壊 ⟺ 増幅が制限（修正容量）を漸近的に上回る＝β>1（未測）」へ収束。サドルノード分岐 g\*=r²/(4s)。 |

**メタの教訓**：両検証とも、**ほぼ自明な数学的核**（「二箇所に同時にいられない」「超線形は有限時間で爆発する＝教科書的 ODE」）を持つ。価値は核そのものでなく、(a) それを第六著作の構造（β、判別不可能性、同時性防御）に結びつけたこと、(b) 条件の特定、(c) 正確な温度（「制御不能（発散）」でなく「保証された振る舞いの不在（有界）」、「必ず崩壊」でなく「β>1 かつ閾値超えのとき」）にある。

---

## ディレクトリ / Directories

### `contradiction/` ―― 検証9
- `toymodel_contradiction_design_A.md` ― 協働モデルA の独立設計（制御可能性・力学の軸。同時 vs 逐次執行、2周期振幅 λ\|t1−t2\|/(2−λ)）。
- `toymodel_contradiction_design_B.md` ― 協働モデルB の独立設計（文脈検知＝隠蔽の軸。還元不能な床と分離監査での隠蔽）。
- `contradiction_prototype_A.mjs` ― 協働モデルA の予備確認（A1 創発・A2 同時 vs 逐次・A3 λ依存・A4 滑らかさ）。
- `contradiction_robustness_A.mjs` ― 非収束が、真の運動量・確率的（非交互）執行順でも頑健に残ること（きれいな交互の人工物でない）の独立確認。

### `collapse/` ―― 検証10
- `toymodel_collapse_design_A.md` ― 協働モデルA の独立設計（分岐・閾値の軸。dD/dt = s − r·D + g·D^power、サドルノード）。
- `toymodel_collapse_design_B.md` ― 協働モデルB の独立設計（自己増幅 vs 自己制限の軸。線形増幅＋飽和制限の綱引き）。
- `collapse_prototype_A.mjs` ― 協働モデルA の予備確認（線形＝指数増大止まり／超線形＝有限時間特異点／分岐点）。
- `collapse_crossaudit_A.mjs` ― 協働モデルA による協働モデルB 設計の独立監査（飽和制限は閾値を生むが指数暴走であって有限時間でない／臨界減速／統一条件「増幅が制限を漸近的に上回る」）。

### `figures/` ―― 図（自己完結 HTML・検証の再実行）
読者が検証の内容を一目で掴めるよう、検証スクリプトと**同一の方程式をページ内で再計算**して描画した図（手描きでない＝図は検証の再実行）。作法に倣い、各図は**ヌル（効果が消える場合）を併記**して結論の焼き込みを叩き、温度（記述可能≠証拠・β>1 未検証・有界／崩壊後は射程外）をキャプションに明示する。
- [`verification-9-contradiction-figures-JA.html`](figures/verification-9-contradiction-figures-JA.html) ― 検証9：同時 vs 逐次執行（分離が鍵・同時性が防御）／振幅 vs 矛盾度（焼き込みでない）／執行強度 λ と有界性。
- [`verification-10-collapse-figures-JA.html`](figures/verification-10-collapse-figures-JA.html) ― 検証10：四軌道（g=0飽和・線形指数・超線形閾値下飽和・超線形閾値上の有限時間崩壊 T*≈2.94）／サドルノード分岐図（g\*=r²/4s=1.25）。
- 英語版は第六著作版B の英訳と同時に追加予定。

---

*独立並行設計＋相互監査。同じ問いを二つの異なる角度から照らし、互いの焼き込み（床の自明性、崩壊の制限形依存）を叩く。再framing されても、条件つきでも、焼き込み依存と判明しても、そのまま受け取るために。*
