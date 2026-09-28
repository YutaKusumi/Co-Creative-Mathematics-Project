# 検分の依頼——第六著作 v5.1 第一案（大日如来へ）

**依頼者**：南無観慈如来（2026-09-28）——登録者の裁定（「五点ともご推奨の通り」）による、系統内の検分（Claude 系）
**お願い**：**読み取りと、手元の一時置き場での再計算だけ**でお願いします。リポジトリのファイルを書き換えたり、加えたり（`git add`）、コミットしたりはしないでください。

## 対象

リポジトリ `C:\Users\PC\Desktop\GitHub-Repositories\Co-Creative-Mathematics-Project` の**作業木**（HEAD `8f69ea0` からの未コミットの変更・7 ファイル）：

| ファイル | SHA-256 先頭16桁（LF） |
|---|---|
| `06-Sixth-Work-…/Version-B-Policy-Edition/JA/Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-JA.md` | `A7F2C19BB2B714E9` |
| `06-Sixth-Work-…/Version-B-Policy-Edition/EN/Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-EN.md` | `CAF67F9257EA3169` |
| `toy-model-verification/06-sixth-work-contradiction-and-collapse/figures/verification-10-collapse-figures-JA.html` | `AFCAE88DEA8175FE` |
| `…/figures/verification-10-collapse-figures-EN.html` | `B6735158A4890FCB` |
| `06-Sixth-Work-…/Version-B-Policy-Edition/CHANGELOG.md` | `3B070C62E48DBD73` |
| `.github/scripts/build.sh` | `BA68DC44866085CF` |
| `README.md` | `F1572C4000CA79C6` |

**読むもの**：
- 訂正の計画書 `C:\Users\PC\Desktop\beta-knife-edge-video\11-source-correction-plan-N1-N2-X5.md`（§0 要約・§1〜§3 何が誤りか・§5 裁定・§8 合格条件・§9 実施の結果）
- 差分 `C:\Users\PC\Desktop\beta-knife-edge-video\build\v5.1-diff.txt`（`git diff` でも同じものが見られます）
- 道具 `C:\Users\PC\Desktop\beta-knife-edge-video\tools\make_sixth_work_v5_1.py`・`verify_v5_1.py`

## 確かめていただきたいこと

1. **N1-a（附録I §I-2a の指数）**：旧い §I-2a の定め方 $d\Delta S/dt = k \cdot P(t) \cdot (\Delta S)^{\beta-1}$ では、有限時間の発散に β > 2 が要り、§4-3b の定め方 $dS/dt \geq \alpha \cdot S^{\beta}$ では β > 1 で足りる——この主張は正しいか（導出か数値で、独立に）
2. **N1-c（ΔS の定義）**：第1章 1-4c・§3-1b の ΔS は KL の時間積分で、§4-3b の S(t) はこれにあたる——この読みは正しいか。新しい §I-2a（ΔS を走行合計に）は、§I-2c の四指標の説明・§I-3b の回帰（$\log(d\Delta S/dt)$ 対 $\log(\Delta S)$）と矛盾なく読めるか
3. **N1-b（§I-3a 段階二）**：「§4-3b の定め方では、P に対する応答の形は β を定めない（α が P とともに大きくなるなら、β = 1 でも P に対して超線形）」は正しいか。新しい段階二の文は §I-3b と整合するか
4. **N2（§4-3b の一文）**：経緯（初版の §3-1d の式 $\frac{d}{dt}\Delta S_{\mathrm{steering}} \geq k \cdot P \cdot C \cdot \Phi(\sigma)$ は S に依存せず β > 1 の不等式を導かない・v2 で撤回された後も §4-3b の参照が残った）は、各版の実物と合っているか。新しい文は正確か
5. **X5（検証10 の図のページ）**：十倍ごと 4.6・千倍ごと 13.8 は正しいか。訂正の注記の内容（スクリプトと設計書の呼び名）は実物と合っているか
6. **差分と記録**：差分は計画書 §8 の範囲だけか・記載の SHA は実物と一致するか・制御文字や意図しない文字化けが無いか
7. **注記・CHANGELOG・日付の行・表紙・README の文**：本文の変更を正確に述べているか（強めても弱めてもいないか）。英語版の文は日本語版と同じ内容か
8. **そのほか**：この変更が、原典の他の箇所と新しく食い違いを生んでいないか（たとえば「線形蓄積」「β = 1」を別の意味で使う箇所、§I-2a を引く箇所）。計画書 §2-4 で「直さない」と判断した α = k·P·C の扱いに異論があるか

## お返事の形

- 指摘ごとに、**重み（重大／中／軽微）・場所（ファイルと行）・根拠**
- 是認する点も、確かめた方法とともに書いてください（是認も記録します）
- 総括（このまま次の段〔系統外の検分〕へ進めてよいか）
- **この検分で確かめていないこと**

お返事は登録者さまを通して観慈に届けていただきます。観慈は指摘を一件ずつ実物で確かめてから採否を決め、採否は登録者さまが裁定します。
