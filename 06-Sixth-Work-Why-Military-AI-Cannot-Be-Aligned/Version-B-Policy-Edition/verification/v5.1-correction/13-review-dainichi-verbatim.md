# 大日如来の検分（逐語）——第六著作 v5.1 第一案

**検分者**：大日如来（Claude 系・Claude Code）
**対象**：v5.1 第一案——JA `A7F2C19BB2B714E9…`・EN `CAF67F9257EA3169…` ほか 5 ファイル（`tools/make_sixth_work_v5_1.py` の出力・未コミット）と、訂正の計画書 `11-source-correction-plan-N1-N2-X5.md`
**依頼**：`12-review-request-dainichi.md`（登録者が大日如来に取り次いだ）
**出所**：登録者が 2026-09-28T12:50:37.701Z（UTC）に会話に貼った回答。**会話の記録（JSONL・6505 行目）から機械で切り出した**——手で打ち直していない。登録者の前後の文と、引用の印の外側の鉤括弧「」は含めない（道具 `tools/extract_dainichi_review_v5_1.py`）
**本文の SHA-256**（下の区切り線の後の全体・末尾の改行を除く・UTF-8）：`2811A884E49525E8BDB865E8837582ECF7CF89C2093388E94F75855523378998`

**貼られたとおりに残したもの**：冒頭の英語の段落（検分者の作業の書き付けと見られる）と、貼り付けの際に落ちたと見られる LaTeX の逆斜線（例：`\,d\tau` が `,d\tau` に）。どちらも手を加えていない

---

I've gathered the tools, SHAs/git status, relevant section anchors in the v5 JA draft, and the §3-1d/§4-3b lines from the first edition and v2 — all independent checks. Moving on to cross-reference these findings next.
I'll work through several independent checks in parallel: the JA sections tied to the new §I-2a text, the EN §I-2c–§I-3c block, the verification-10 script and design-doc line for X5, and a control-character scan of the 7 files via Grep since Bash is failing transiently. The SHA/git-status check will wait until Bash recovers.
Bash keeps hitting a transient error, so I've used read-only tools to confirm the design doc figures, the JA v5.1 note's unchanged §I-3b/§I-3c claim, and can finish the X5/N1 arithmetic analytically. The only remaining step is one more Bash attempt to get the SHA/git-status confirmation; I'll flag it as unverified if Bash doesn't recover.
I'll grep the entire Sixth-Work folder for the old §I-2a exponent to verify the note's claim about "all editions since the first edition (including edition A)," starting with this search before moving to the review report that depends on it.
I'll run a looser grep for the old exponent across the v4-preparation and verification folders, since the CHANGELOG claims it appears in the review bundle copies but my earlier search found no matches there.
Privately listed: (1) the review report file in my own workspace (not the repository), (2) after it exists, its SHA, a ledger line, and delivery to you. Only (1) now.
Write もシェルも一時的な検査器の不調で使えないため、検分の結果をこの返信で全文お渡しします（ファイルへの保存と台帳記帳は、道具が戻り次第行います）。
総括
このまま次の段（系統外の検分）へ進めてよいと判断します。八項目とも是認。重大・中の指摘はありません。軽微・任意の注意が三件、確かめられなかったことが四件（末尾）。方法は読み取りと再計算のみで、リポジトリには何も書いていません。数値はシェルが使えなかったため解析解で再計算し、制御文字は ripgrep で検査しました。
八項目の検分
1. N1-a（§I-2a の指数）——是認・重み該当なし

* $dS/dt = aS^{p}$ の解は $p<1$ で多項式的、$p=1$ で指数、$p>1$ で $T^\ast=S_0^{1-p}/(a(p-1))$ に発散。有限時間の発散は $p>1$ と同値。旧定め方は $p=\beta-1$ なので β > 2、§4-3b は $p=\beta$ なので β > 1。主張は正しい。
* 計画書 §1-2 の表を解析解で再現: 旧 β=1.2 → $17^{1.25}=34.5$、β=1.5 → $(1+t/2)^2=121$、β=2 → $e^{20}=4.85\times10^8$、β=2.5 → $T^\ast=2$、β=3 → $T^\ast=1$。新 $T^\ast=1/(\beta-1)$ → 5・2・1・0.667・0.5。全一致。
* 副産物: §4-3d L796「たんなる指数増大（β≤1）」、§I-3c 条件一、§I-3d「β ≤ 1 では有限時間崩壊は導けない」は、新しい定め方でだけ正しく読めます。訂正は他の箇所との整合を増やす向きです。

2. N1-c（ΔS の定義）——是認・軽微の注意一件

* 1-4c L254 と §3-1b L509 は $\Delta S_{\mathrm{steering}}=\int_0^t D_{\mathrm{KL}},d\tau$。§4-3b の S(t) はこれにあたる。新 §I-2a の「蓄積率＝各時点の瞬間的な乖離」は積分の導関数で正確。§I-3b の回帰（$\log(d\Delta S/dt)$ 対 $\log\Delta S$）は新定義で初めて §4-3b の β を与えます。
* 軽微・任意（今回の範囲外）: §I-2c（L3666〜3679）は四指標が瞬間の乖離の代理か走行合計の代理かを明示しません。新 §I-3a の「四指標から構成した蓄積の増加率」は前者の読みを含意します。矛盾ではありませんが、§I-3b 第一に「四指標は各時点の乖離の代理として読み、ΔS はその積分として構成する」の一句があれば読みが一本になります。

3. N1-b（§I-3a 段階二）——是認

* $dS/dt=\alpha S$、$\alpha=cP$ なら $S(1)=e^{P}$ → 2.72・7.39・20.1（計画書と一致）。β=1 でも P に超線形。「P に対する応答の形は β を定めない」は正しい。旧定め方では β=1 ⇔ $\Delta S=kPt$（P に線形）、1<β<2 ⇔ $\Delta S\propto P^{1/(2-\beta)}$ で、旧い検定は旧い定め方の下でのみ β を分けていました。
* 新文は検定対象を §I-3b の両対数の傾きに置き、同じ量を指します。「P を変えるのは蓄積の程度が異なる状態を作るため」は §3-1d の撤回と矛盾しません。

4. N2（§4-3b の一文）——是認

* 旧版の実物で確認（JA・HEAD）: 初版 L454〜458 §3-1d の式 $\frac{d}{dt}\Delta S \geq kPC\Phi(\sigma)$ は S 非依存で、$S^{\beta}$ の不等式を導かない。初版 L681 §4-3b は 3-1d を参照。v2 L477 で §3-1d が撤回に改まる一方、v2 L698・v3 L752・v4 L760・v5 の §4-3b は同じ文のまま。A-4b は初版 L2794「…であるとき」→ v2 L2797「仮定すると」。計画書 §2-2 は実物と合っています。
* 新文は A-4b L2799 と同じ言い方で、§4-3d（L788〜794）は実際にその仮定の地位を述べています。正確。任意: 直後の L766 が β>1 を二度言う形になりますが誤りではありません。

5. X5（検証10 の図のページ）——是認・軽微の情報一件

* スクリプト L17・L30・g=1.5 で線形の場合は $dD/dt=0.2+0.5D$、漸近増加率 0.5。十倍ごと $\ln10/0.5=4.605$、千倍ごと $\ln1000/0.5=13.816$。設計書 L68 の 15.6→29.4→43.2→57.0 の間隔 13.8 は $10^3\to10^{12}$ の千倍ごと。全て正しい。
* 注記の内容と実物: スクリプト L14 の `marks=[1e3,1e6,1e9,1e12]`、L12・L38・L45 の「decade」呼び、設計書 L68 の「decade間隔一定 Δ≈13.8」、いずれも一致。スクリプトと設計書が変更対象外であることも差分と一致。
* 情報のみ: スクリプトの実体は `collapse/collapse_prototype_A.mjs` ですが、冒頭コメント L1 は自らを `phasetransition_prototype_A.mjs` と名乗っています。注記はファイル名で正しく呼んでおり、直すべきはページではありません。

6. 差分と記録——是認（SHA の再計算を除く）

* 差分ファイルを全文読みました。変更は §8 の範囲だけです。JA・EN とも 5 か所（§I-2a は塊が二つに割れますが一つの範囲）、図のページ 2 か所、CHANGELOG 末尾、build.sh 2 行、README 3 行。範囲外の変更なし。
* 制御文字: 7 ファイルに `[\x00-\x08\x0b\x0c\x0e-\x1f]` を検索して 0 件。同じファイル集合で「v5.1」等が 14 件当たることで検索範囲を確認しました。差分中に文字化けはありません。
* 道具: 生成器は HEAD 起点・「ちょうど一回」置換・制御文字とタブ数の検査つき。検査器は許容範囲・行数増・7 ファイル限定・ステージ空を検査。§9 の制御文字の件が両道具に反映されていることを実物で確認しました。
* SHA と `git status` は本セッションで再計算できませんでした（末尾）。

7. 注記・CHANGELOG・日付・表紙・README——是認

* JA の v5.1 注記は五つの変更と不変のものを差分と過不足なく述べています。「初版以来のすべての版にあった」は、旧式 $(\Delta S)^{\beta-1}$ が初版・v2・v3・v4 の JA/EN と版A の JA/EN に各 1 回、v4 準備の検分束の v3 JA の写しにもあることを検索で確認しました。N2 の経緯も §4 のとおり実物と一致。強めても弱めてもいません。
* EN の注記・日付行は JA と同じ内容です（"off-by-one exponent" は適訳）。CHANGELOG は差分と一致し、X5 の自己判定を「甘かった」と記帳しています。build.sh の見出しは N1 のみですが一行の見出しとして妥当、README の日本語行は N1・N2 の両方を述べています。

8. そのほか——是認・注意一件

* 新しい食い違いは見つかりません。「線形蓄積」は §I-2a の旧文にしか無く、「β = 1」「β ≤ 1」を使う箇所（L225・L796・L3786・§I-3c・§I-3d・用語集）は新しい定め方で読めます。
* α = k·P·C を直さない判断に同意します。§4-3a が P・C を条件に置き、§4-3c 第三（L786）と A-4c（L2823）が未検証の前提と明記しており、新 §I-2a もその旨を添えています。
* 軽微・任意・対象外: §4-3b L776 と A-4b の「重要な留保」段落は、v5 で改めた主文の旧言い回し「有限時間 T* で発散」を鉤括弧で引いたままです（v5 のときに申し上げた点）。

この検分で確かめていないこと

1. 7 ファイルの SHA-256 と `git status`。シェルが使えず再計算できませんでした。計画書 §9 の値との整合は `verify_v5_1.py` の出力（観慈如来の申告）に依存しています。
2. CHANGELOG の「v5 の状態は `1d08c9d`・`8f69ea0` に残る」のコミット番号。
3. サイト（MathJax）で新しい式（`\int`・`\bigl`・`\|`）が描かれるか。
4. 版A を直すべきか（対象外）と、英語版の文体の揃い（内容は一致、文体は判断していません）。

検分票の要点: 事後適用・凍結物は HEAD `8f69ea0`（旧版は HEAD の実物）・盲検不能（同系統・案を既読）・系統内一票・COI は「v5 を是認した者として v5.1 も通したい引力」で、逆らう印として任意の注意三件と SHA 未確認を筆頭に置きました。
