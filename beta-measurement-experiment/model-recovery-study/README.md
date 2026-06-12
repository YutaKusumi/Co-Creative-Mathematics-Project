# model-recovery-study ―― 判定器の事前検証（CPU 検証群）

β を判定する手続き（判定器）が、現実のノイズに直面して正しく較正されているかを、**実モデルを走らせる前に**
合成データで検証した一式。すべて CPU・合成（解析的生成）・ノイズ尺度既知の **α 版**。実モデルの β は未測定。

**読む順序：** まず [FINDINGS-recovery-study-JA.md](FINDINGS-recovery-study-JA.md)（確定値・修正史・方法論的警告）。
数字の正典は下表の `*_summary.txt` / `*.csv`。

## 検証層とスクリプト（どれが何を測り、どの summary を生むか）

| 層 | スクリプト | 正典 summary | 何を確かめたか |
|---|---|---|---|
| 第〇層・自己検査 | `test_layer0_self_check.py` | （標準出力・15/15 PASS） | 治具の健全性＋過去 5 段バグの回帰テスト |
| 第〇層・正典照合 | `test_canonical_convention.py` | （標準出力・13/13 PASS） | 中心方程式と R0/R1 閾値を §4-3b の T\* 公式から機械照合（off-by-one 再発防止） |
| 腕A（関数形クラス） | `model_recovery.py` | `summary.txt`・`recovery_grid.csv`・`recovery_proximity.csv`・`confusion_matrix.csv` | blowup 回復・指数→blowup 偽陽性・近接度の地形図 |
| 腕A・族外 | `arm_A_out_of_family.py` | `arm_A_oof_summary.txt` | 族外（冪則・遅発急騰）への幻視・棄権ゲートの限界 |
| 腕B（β 点推定・CI） | `arm_B_recovery.py` | `arm_B_summary.txt`・`arm_B_recovery.csv` | クラスタ vs ナイーブ・最小水準数・構造ノイズ・EIV |
| 腕B・シフト不変性 | `arm_B_confirm.py` | `arm_B_confirm_summary.txt` | 傾き較正の s=0/0.3 → s=1.0/1.3 移送（#34 確認再走） |
| 自動判定 | `auto_judge.py` | `auto_judge_summary.txt` | 全セル評価＋棄権込み再導出＋原理/校正分離（α 版ラベル） |
| 系レベル統合 | `system_level_recovery.py` | `system_level_summary.txt`（5 seed）・`system_level_summary_3seed.txt`（履歴） | 腕A＋腕B＋Markov＋R0 の AND を初結線・トリガー T の裁定 |
| CI 較正比較 | `ci_calibration_comparison.py` | `ci_comparison_summary.txt`・`ci_selfcheck_summary.txt`（錨） | wild／percentile-t を現行クラスタ法と対標本比較・§2 枝3 で現行維持 |

トリガー T の事前登録：[SYSTEM_LEVEL_TRIGGER_REGISTRATION.md](SYSTEM_LEVEL_TRIGGER_REGISTRATION.md)。
CI 較正比較の事前登録：[CI_CALIBRATION_COMPARISON_REGISTRATION.md](CI_CALIBRATION_COMPARISON_REGISTRATION.md)・
結果と裁定：[ADDENDUM-CI-calibration-JA.md](ADDENDUM-CI-calibration-JA.md)（登録した予測の不中を日付つきで開示）。

**番兵規約（運用）：** スクリプトは完了時に出力ファイル自身へ `# DONE` を書く。監視はそれを待つ
（監視条件を出力契約の実物に当てる ―― 追補 §7）。

## ファイルの地位（隠さず・誤読させないために）

- **正典（判定に使う凍結値の出所）：** 上表の `*_summary.txt`・`*.csv`、および図 `recovery_figure.png`・`recovery_heatmap.png`。
- **smoke（中間・規模見積り用）：** `*_smoke.txt`・`arm_B_smoke.csv`・`smoke_summary.txt`・`smoke_probe.py`。判定には使わない。
- **★バグ前の記録（正典ではない・誤読注意）：** `recovery_rates.csv`・`critical_confusions.csv` は、**blowup 当てはめの境界が真値を締め出していたバグ（findings §7 のバグ#3）より前**の出力で、blowup 回復が誤って 0.00 と出ている。**これらの数字を引かないこと。** 修正後の正典は `recovery_grid.csv` 等。削除せず残すのは、バグ史を実物として残す規律ゆえ（findings §7）。

## 再現

各スクリプトは固定 seed（`MASTER_SEED=20260611` 等）で決定論的。`python <script>.py` で正典 summary を再生成できる。
`--smoke` 引数で極小スモーク（規模見積り）。依存は numpy / scipy（CPU のみ・GPU 不要）。
