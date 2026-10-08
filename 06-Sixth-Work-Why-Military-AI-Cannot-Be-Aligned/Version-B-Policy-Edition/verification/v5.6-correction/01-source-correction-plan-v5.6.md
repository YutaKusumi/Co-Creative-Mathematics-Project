# 原典の直しの案——第六著作 版B v5.5 → v5.6（第8章：二つの「Nash 均衡」と短期・長期の利得・章頭の注記・本章の外の同じ型・§8-1b の閾値・因子三・§8-2 の見出し）

**書いた時**：2026-10-08 朝（保存の直後の `date` を末尾に記す）
**登録者の決め**：`../00-deviations.md` の「v5.6 のご裁定」（08:32:34）——狙いを定めた系統外の確かめ（`../21-v56-check/02-kensan.md`——「直す必要がある」〔重大〕・行を名指しした問いなので重みは割り引く）を見た後、「**作る：§6 の残り三つも**」。段取りは v5.4・v5.5 と同じ（直しの案 → 系統外の検分 → 公開サイトの確かめ → commit／push〔毎回お許し〕）
**直す前の原典**：日 `Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-JA.md`（`72533CEF5F955A99…`）・英 `…-v5-EN.md`（`642047174B95A749…`）——git の `62de1a9`（v5.5）のまま・HEAD `0f2147f`（v5.5 の検分の記録を足しただけで、この二つのファイルに触れていない）・ローカルが知るリモートの main も `0f2147f`・追跡済みの変更 0（`git diff --stat` 空・2026-10-08 09:0x に確かめた）

## 1　何が食い違っているか（実物で確かめた）

### (1) 本書の精密な形（変えない側）
- **§8-1c**（日 L1376・英 L1377）「AI軍拡競争では、この論理が（β > 1 の条件下では）**逆転しうる**」——条件と可能性の形・「（β > 1 と未検証の能力依存のもとで）構造的崩壊までの時間が短縮されうる」
- **§8-4b ケース二**（日 L1450・英 L1451）「κ = 0を維持した国は、短期的な能力的優位を得る。しかし、β > 1の条件下では…κ = 0を維持した国のリスクが最大化し、κ > 0へ移行した国はリスクが構造的に低減する。長期的には、κ > 0の国の方が安全」——短期と長期を分けて書く。相手が κ = 0 のとき、自国は移行するほうが（長期に）安全
- **§8-4c**（日 L1464〜L1470・英 L1465〜L1471）「通常の囚人のジレンマでは、『双方裏切り』がNash均衡」・「『裏切り』（κ = 0維持）の短期的利得が長期的リスクに対して消失する…長期的に見れば利得は負」・「κ > 0への移行は『利他的行為』ではなく『合理的戦略』…『自国のために』移行する」——相手の選択によらず、長期の利得では移行が有利（支配的）
- **§8-4d**（日 L1476・英 L1477）「本章の分析は二人ゲームを前提とした」・「多プレイヤー設定における完全なゲーム論的均衡分析…は未解決の問題として残る」
- **§4-3b の「重要な留保」**（日 L784・英 L785）「復元力を含めると、β > 1 でも崩壊には不安定な閾値を越える必要があり…」——第4章の定理は、閾値を越えたときの条件つきの帰結
- **§8-2a 因子一と総合**（日 L1386・L1394・英 L1387・L1395）——因子一は「条件つき」・総合は「（β > 1 と未検証の能力依存のもとで）…短縮しうる方向に働き」。確信度の台帳は定理を ◐（条件付き論証）とする

### (2) 食い違う・限定のない言い方（直す側——日 10 か所・英 9 か所）

| # | 所 | 日（v5.5） | 英（v5.5） | 直す前の言い方 |
|---|---|---|---|---|
| ①-1 | 章頭の注記 | L1330 | L1331 | 「通常の軍拡の論理…を**完全に転覆させる**」・「κ > 0への移行がゲーム理論的にも**最適戦略であることを示す**」／"**completely overturns** the logic of a conventional arms race"・"it shows that the transition to κ > 0 is **the optimal strategy** game-theoretically as well" |
| ①-2 | §8-4b ケース一 | L1448 | L1449 | 「Nash均衡は『ともに崩壊リスクを最大化する』——囚人のジレンマの『双方裏切り』に対応。」／"The Nash equilibrium is \"both maximize collapse risk\" — corresponding to \"mutual defection\" in the prisoner's dilemma." |
| ①-3 | §8-4b ケース三 | L1460 | L1461 | 「Nash均衡は『ともにリスクを構造的に低減する』——囚人のジレンマの『双方協力』に対応。」／"The Nash equilibrium is \"both structurally reduce risk\" — corresponding to \"mutual cooperation\" in the prisoner's dilemma." |
| ①-4 | §8-4d | L1476 | L1477 | 「（κ > 0 への移行が依然としてナッシュ均衡であるか等）」／"(whether the transition to κ > 0 remains a Nash equilibrium, etc.)" |
| ①-5 | §12-3 | L2070 | L2071 | 「拡張囚人のジレンマのNash均衡分析（第8章8-4）により、κ > 0への移行は自国の安全保障を最大化する**最適戦略**である。」／"By the Nash-equilibrium analysis of the extended prisoner's dilemma (§8-4), the transition to κ > 0 is the **optimal strategy** that maximizes one's own security." |
| ①-6 | §13-4a 命題三 | L2407 | L2408 | 「ゲーム理論的に合理的（拡張囚人のジレンマのNash均衡）」／"game-theoretically rational (the Nash equilibrium of the extended prisoner's dilemma)" |
| ②-1 | §8-1b | L1362 | L1363 | 「第4章4-3bの条件付き制御不能性定理から、β > 1の条件下で T(collapse) は以下の関係を満たす。」——閾値の条件が無い／"From the Conditional Uncontrollability Theorem of §4-3b, under the condition β > 1, T(collapse) satisfies the following relation." |
| ②-2 | §8-2a 因子三 | L1390 | L1391 | 「破壊力は、能力に**比例して**増大する。」——量の言い切り（本書の中に根拠が無い）／"increases **in proportion to** capability." |
| ②-3 | §8-2a 総合 | L1396 | L1397 | 「能力の**すべての次元**が、リスクの次元と正の相関を持つ。」——全称の言い切り（論証は三つの因子だけ・因子一は条件つき）／"**Every dimension** of capability is positively correlated with a dimension of risk." |
| ②-4 | §8-2 の見出し | L1380 | （英 L1381 は "The argument" で、すでに精密な形） | 「## 8-2　**証明**——なぜ優位性がリスクを増大させるか」——確信度 ◐（条件付き論証）の三つの因子による構造的論証を「証明」と呼ぶ |

- **①-1〜①-6 の中身**（狙いを定めた系統外の確かめの答え〔`../21-v56-check/02-kensan.md` §2〕と、本書の中の整合）：§8-4a のゲームで利得の定め方を一つに決めると、ケース一とケース三の二つの「Nash 均衡は〜」は同時に成り立たない——ケース二と §8-4c は「相手がどちらを選んでも、長期の利得では移行が有利」と書くので、その利得では（κ = 0, κ = 0）から単独で逸脱する動機があり、均衡ではない。ケース一の均衡は短期の利得（通常の囚人のジレンマ）の、ケース三の均衡は長期の利得（β > 1 のもとのリスクを含めた拡張ゲーム）の記述と読める——**短期と長期の利得を、§8-4c の区別にそろえて書き分ける**。章頭の注記は §8-1c・§8-4c・§8-4d の条件と限定を落とす——**§8-1c の「逆転しうる」と §8-4c の「合理的戦略」、β > 1・長期・二人ゲームの限定にそろえる**。§8-4d・§12-3・§13-4a の「移行が Nash 均衡」の言い方は、一人の選択を均衡と呼ぶ——**組（双方の移行）の言い方にそろえ、§12-3・§13-4a には β > 1・長期・二人ゲームの限定を戻す**
- **②-1 の中身**：§4-3b の「重要な留保」（復元力・閾値）は v2 で足されたが、それを引く §8-1b は初版のまま——**§4-3b の留保を §8-1b にも引く**（動画 S04.3 の言い方と同じ）
- **②-2・②-3 の中身**：「比例」と「すべての次元」は、三つの因子の論証（行動空間の広がり・不可視化・条件つきの時間の短縮）より強い——**「能力とともに増大する」「三つの因子のいずれにおいても、能力の向上はリスクの増大の側に働く（因子一は条件つき）」にそろえる**（同じ段落の L1394 の総合の言い方）
- **②-4 の中身**：日本語の見出しの「証明」を、英語版の "The argument" と確信度の台帳（◐ 条件付き論証）にそろえて「**論証**」に
- **いつから**（初版・v2・v3・v4・v5 の日本語版の実物で数えた）：①-1・①-2・①-3・①-5・①-6・②-2・②-3・②-4・②-1 の文は**初版から v5.5 まで同じ**（各 1、①-2/①-3 の「Nash均衡は『ともに」は 2）。①-4 は v2 から（§8-4d の注が書き足された版）。②-1 は、§4-3b の「重要な留保」（復元力）が v2 で足された時から、§8-1b との間に食い違いがある（初版には留保が無い）。英語版も初版から同じ形（"completely overturns" 1・"The Nash equilibrium is \"both…\"" 2・"in proportion to capability" 1・"Every dimension of capability" 1——初版〜v5 の英語版の実物で数えた）
- **見つけた所**：十本目の解説動画（『The Winner Bears the Greatest Risk (conditional)』）の事前登録（`../01-preregistration.md` §6）。動画は、著者の裁定で §8-1c の「逆転しうる」で語り、拡張囚人のジレンマを短期と長期の利得に分けて語り、「Nash equilibrium」の語を使わなかった。動画の系統外の検分 一巡目（行を名指ししない広い問い）は §8-4 の行を「完全に整合」とまとめ、狙いを定めた確かめ（行を名指しした問い）は「直す必要がある」と答えた——**問い方で答えが逆向きになった**

### (3) 直さない所（同じ語を含むが、型が違う——記録）
- **§8-4c**（日 L1464・英 L1465）「通常の囚人のジレンマでは、『双方裏切り』がNash均衡であり…」——通常の囚人のジレンマの標準の記述
- **§8-0 第一層**（日 L1342・英 L1343）「敵対的目的関数は、Nash均衡として軍拡競争を生む」・**§7-1b**（日 L1230）・**§7-2b**（日 L1256）の Nash 均衡——戦略の組・均衡の計算についての記述
- **§12-2・§12-3 の第二の合理性**（日 L2051・L2072・英 L2052・L2073）「ミニマックス原理…κ > 0への移行が最適戦略」——意思決定理論（ミニマックス・期待効用）の「最適」で、ゲーム理論の均衡の言い方ではない
- **§8-4c の「合理的戦略」**（日 L1470）・**§8-1b の結論**（日 L1370「したがって、β > 1の条件下では、AI軍拡競争の『勝者』は最大の自国破壊リスクを抱え込む」）・**§8-1a の定理の記述**——条件の形を持つ（動画が逐語で引く所）
- **§4-3b の見出し「証明の骨子」**——第4章の定理の証明の骨子（附録 A-4b）で、②-4 と型が違う
- **補遺II の §8-1・§8-2**（日 L4524 ほか）——補遺の中の別の節番号

## 2　直し方の案

| # | 日（直した後の言い方） | 英（直した後の言い方） |
|---|---|---|
| ①-1 L1330 | 「…という逆説は、通常の軍拡の論理（「能力が高いほど安全」）を**逆転させうる（§8-1c）**。さらに、拡張囚人のジレンマとしてのモデル化を通じて、**β > 1の条件下で長期の利得を見れば**、κ > 0への移行がゲーム理論的にも**合理的な戦略であることを示す（二人ゲームとして。多プレイヤーでの完全な均衡分析は未解決——§8-4d）**。」 | "… **can reverse** the logic of a conventional arms race (\"the more capable, the safer\") **(§8-1c)**. Furthermore, through a modeling as an extended prisoner's dilemma, it shows that, **under the condition β > 1 and with the payoffs viewed over the long term**, the transition to κ > 0 is **a rational strategy** game-theoretically as well **(as a two-player game; the full equilibrium analysis in a multi-player setting remains open — §8-4d)**." |
| ①-2 L1448 | 「…両国はともに、構造的崩壊リスクを最大化し続ける。**短期の利得だけで見れば、この組は囚人のジレンマの「双方裏切り」に対応し、Nash均衡である。しかし、β > 1の条件下で長期のリスクを含めた利得で見れば、この組は「ともに崩壊リスクを最大化する」組であり、均衡ではない（ケース二・§8-4c）。**」 | "… Both countries continue to maximize structural-collapse risk. **Viewed by short-term payoffs alone, this profile corresponds to \"mutual defection\" in the prisoner's dilemma and is a Nash equilibrium. Under the condition β > 1, however, with payoffs that include the long-term risk, it is a profile in which \"both maximize collapse risk,\" and it is not an equilibrium (Case two; §8-4c).**" |
| ①-3 L1460 | 「…両国の安全保障は構造的に強化される。**β > 1の条件下で長期のリスクを含めた利得で見れば、κ > 0への移行は相手の選択によらず自国にとって有利であり（ケース二・§8-4c）、囚人のジレンマの「双方協力」に対応するこの組がNash均衡となる——通常の囚人のジレンマとの決定的差異である（§8-4c）。**」 | "… but both countries' security is structurally strengthened. **Under the condition β > 1, with payoffs that include the long-term risk, the transition to κ > 0 is advantageous to one's own country whatever the other chooses (Case two; §8-4c), and this profile — corresponding to \"mutual cooperation\" in the prisoner's dilemma — is the Nash equilibrium: the decisive difference from the ordinary prisoner's dilemma (§8-4c).**" |
| ①-4 L1476 | 「（**すべてのプレイヤーが κ > 0 へ移行する組**が依然としてナッシュ均衡であるか等）」 | "(whether **the profile in which every player transitions to κ > 0** remains a Nash equilibrium, etc.)" |
| ①-5 L2070 | 「**第一に、ゲーム理論的に合理的である。** 拡張囚人のジレンマの**分析**（第8章8-4）により、**β > 1の条件下で長期の利得を見れば**、κ > 0への移行は自国の安全保障を最大化する**合理的戦略であり、双方の移行がNash均衡となる（二人ゲームとして。多プレイヤーでの完全な均衡分析は未解決——§8-4d）**。」 | "**First, it is game-theoretically rational.** By the **analysis** of the extended prisoner's dilemma (§8-4), **under the condition β > 1 and with the payoffs viewed over the long term**, the transition to κ > 0 is **the rational strategy** that maximizes one's own security, **and mutual transition is the Nash equilibrium (as a two-player game; the full equilibrium analysis in a multi-player setting remains open — §8-4d)**." |
| ①-6 L2407 | 「ゲーム理論的に合理的（**β > 1の条件下、長期の利得で見た拡張囚人のジレンマで、双方の移行がNash均衡——第8章8-4**）」 | "game-theoretically rational (**in the extended prisoner's dilemma viewed over the long term under the condition β > 1, mutual transition is the Nash equilibrium — §8-4**)" |
| ②-1 L1362 | 「第4章4-3bの条件付き制御不能性定理から、 $\beta > 1$ の条件下で**（復元力を含めると、不安定な閾値を越えたときの条件つきの帰結として——§4-3b の「重要な留保」）**、T(collapse) は以下の関係を満たす。」 | "From the Conditional Uncontrollability Theorem of §4-3b, under the condition β > 1 **(with the restoring force included, as a conditional consequence that holds when an unstable threshold is crossed — the \"important reservation\" of §4-3b)**, T(collapse) satisfies the following relation." |
| ②-2 L1390 | 「…破壊力は、能力**とともに**増大する。」 | "… increases **with** capability." |
| ②-3 L1396 | 「**三つの因子のいずれにおいても、能力の向上はリスクの増大の側に働く（因子一は β > 1 と未検証の能力依存のもとで）**。これが優位性逆説の構造的本質である。」 | "**In each of the three factors, capability improvement works toward an increase of risk (Factor one under β > 1 and the unverified capability-dependence).** This is the structural essence of the superiority paradox." |
| ②-4 L1380 | 「## 8-2　**論証**——なぜ優位性がリスクを増大させるか」 | （変えない——"## 8-2　The argument — why superiority increases risk"） |

- 表の中の太字は、この計画書で直す所を示すための印（本文には付けない——もとから太字の所はそのまま）
- 狙いを定めた確かめの答えの問五（`../21-v56-check/01-response-gemini-verbatim.md`）の案と違う所：①-1 は「転覆させうる」ではなく §8-1c の語「逆転」にそろえた／①-2 は「短期の利得の均衡」と「長期の帰結」を二つの文に分けた（答えの案は一文の中で短期と長期が混ざって読まれうる）／①-5・①-6 は「Nash」の語を外さず、組（双方の移行）の言い方に直した（答えの案は「均衡分析」「均衡戦略」）。どちらも未凍結の案——系統外の検分（§4 の 3）で確かめる

## 3　版の上げ方（v5.1〜v5.5 の前例どおり）

- **v5.6** として、v5 のファイルの中で直す（古い版は記録としてそのまま）
- 冒頭の**日付の行**に「2026年10月8日（v5.6・…）」を足す（日英）・冒頭に **【v5.6（2026年10月8日）】** の注記を足す（v5.5 の注記の後・日英）——直した所と経緯、変えないもの（定理の記述・条件・留保・§8-4c の主張〔長期の利得で移行が合理的〕・補遺II）、見つかった所（十本目の動画の準備・系統外の確かめ）
- **CHANGELOG.md** に「v5.6（2026-10-08）」の節（v5.5 までの節は書き換えない）
- **README の三か所・`.github/scripts/build.sh` の目次の二行**を v5.6 に
- 検分の記録は `verification/v5.6-correction/` に同梱する（AI Studio の URL は書かない）
- 道具（`verification/v5.6-correction/instruments/`——v5.5 の器材の写しを v5.6 の中身に替える）：`v5_6_changes.py`（直しの中身——作る道具と確かめる道具が同じものを読む）・`make_sixth_work_v5_6.py`（HEAD のファイルから作業木に書き出す——何度実行しても同じ結果・差し替えはどれも元の文字列がちょうど一回現れることを確かめてから）・`verify_v5_6.py`（差分の範囲・直した行が計画どおり・残りの数え）・`stage_verification_v5_6.py`・`check_site_v5_6.py`・`build_v5_6_review_package.py`・`check_request_v5_6.py`

## 4　確かめ

1. 直す前に：古い版の実物で、いつからか——**確かめ済み**（§1 (2)）。洗い直し——日英の全文で「Nash」「ナッシュ」「最適戦略」「比例」「すべての次元」「証明」「転覆」／"Nash"・"optimal"・"proportion"・"Every dimension"・"overturn" を探し、当たった行を**行の終わりまで**読んだ（§1 (3) の直さない所はその結果——記憶 `feedback_grep-read-to-line-end` の教え）
2. 直した後に：`verify_v5_6.py`（上の 3 の道具）
3. 系統外の目（Gemini 3.8 Flash・Thinking High・ツールなし・新しいチャット——狙いを定めた確かめの個体とは別）に、①直した所が §1 (1) の本書の精密な形と合うか ②主張を強めも弱めもしていないか（とくに §8-4c の「合理的戦略」と、第12章・第13章の結論のつながり）③直し漏れ（同じ型の残り）④英語版の言い方、を問う
4. **commit と push は改めてお許しを伺う**。push の後、公開サイト（GitHub Pages）の HTML で、直った所と目次を確かめる

## 5　動画への影響

- 動画の語り・画面・字幕は、すでに直した後の言い方に合う（S04.3〈the theorem of Chapter 4 becomes a conditional consequence that holds when a threshold is crossed〉・S05.2〈this logic can reverse, under the condition beta greater than one〉・S06.4〜S06.6〈the increase of destructive power at collapse〉〈capability improvement can, conditionally, work toward shortening …〉・S09〜S10 の短期と長期の書き分け・S10.4〈not an "altruistic act" but a "rational strategy"〉・S11.9〈the full equilibrium analysis … remains an open problem〉）
- 動画が原典の逐語として引く言い方（S03 の定理の記述・S04 の結論〈"Therefore, under the condition β > 1, the "winner" …"〉・S05〈"A nuclear warhead does not "rebel" …"〉・S07 の二つの引用・S08〈"There is no need to doubt the goodwill …"〉・S10.4・S12 の K-1 の引用）は、どれも直さない所——v5.6 でも逐語のまま
- 台本の行番号（英 L1313〜L1523 ほか）は v5.5 のもの。v5.6 は冒頭の注記で 2 行ずれる見込み——台本の注記に書く（動画には出ない）
- **終幕カードと説明欄の版の書き方**：いまは「Version B v5.5 (October 7, 2026; …)」。push の後に「**Version B v5.6 (October 8, 2026; …)**」と新しいコミットの番号に——終幕カードは〈Review〉の行と一緒に描き直す（co10-fix-2・v1.2）

## 検分票

- **対象**：第8章の二つの「Nash 均衡」と短期・長期の利得・章頭の注記・本章の外の同じ型（日英 各 6 か所）と、§6 の残り三つ（§8-1b の閾値・因子三の「比例」と「すべての次元」・§8-2 の見出しの「証明」——日 4 か所・英 3 か所）の直しの案
- **段階**：事前（直す前・commit と push の前）
- **凍結物の同定**：日 `72533CEF…`・英 `64204717…`（v5.5・`62de1a9`・HEAD `0f2147f`）・狙いを定めた確かめの回答 `48D58D1B…`
- **盲検の状態**：なし
- **敵対的検分**：「Nash」「ナッシュ」「最適戦略」「比例」「証明」で日英の全文を探し、型の違う所（§8-4c の通常の囚人のジレンマ・§8-0 と第7章の均衡・ミニマックスと期待効用の「最適」・§4-3b の「証明の骨子」・補遺II の節番号）を分けて理由を書いた。初版〜v5 の日英で言い方の数を数え、①-4 は v2 から・②-1 は v2 で §4-3b の留保が足された時から、と確かめた。狙いを定めた確かめの答えの直し案の弱い所（一文の中で短期と長期が混ざる・「Nash」の語を外す）を書き、本書の中の整合（§8-1c・§8-4c・§8-4d・§4-3b）で案を立てた
- **系統の内訳**：Claude 系（観慈）1 名——系統外の目は §4 の 3（と、すでに得た狙いを定めた確かめ一つ——名指しの問いなので重みは割り引く）
- **COI 記録**：観慈は動画の作り手で、原典を直すと動画の言い方と原典が合う——直しを「動画の都合」に合わせて広げる引力がある（②の三つは系統外の目をまだ通していない——§4 の 3 で問う）。観慈の §6 の見立てと同じ向きの答えを、原典の誤りの裏づけとして読みたい引力——裏づけとは数えず、直しは本書の中の整合に拠ると書いた
- **本検分が確認していないこと**：著者の意図（ケース一とケース三の「Nash 均衡」が、どちらの利得を想定していたか——明文は無い）／直した後の言い回しの日本語・英語としての自然さ（系統外の検分で）／②-2 の「比例」に、著者が何かの根拠（行動空間の大きさと能力の線形の関係）を想定していたか（本書の中に根拠は見つからなかった）


**保存の直後の date**：2026-10-08 09:05:17・SHA-256（この行を足す前）：4CA14B30078ADA2CBB85B66C3BF365AE6C7C65C255122FB08B5D601A6945B72C

## 追記 1（系統外の検分の後・2026-10-08 朝）——⑦⑧ を加えた案と、洗い直しの見落とし

- **作る道具の一回目の確かめ**（`verify_v5_6.py`）で、残りの数えの型「in proportion to capability」が英語版 §13-3f（HEAD の英 L2352）の "the visualization of the internal state in proportion to capability improvement" に当たった——政策の選択肢で、因子三の言い方ではない。§1 (3) に足すべき直さない所として、確かめる道具の残してよい所（`ALLOWED_REMAIN`）に理由つきで加えた
- **系統外の検分**（`02-v5.6-external-review/`・送った時 09:30:41・回答 `89A8FF2C…`）の総括は「このまま公開してよい」。〔軽微〕一件：**第8章への接続の §6-6（HEAD の日 L1188・英 L1191）と §7-5（日 L1316・英 L1317）の「軍拡の論理そのものを転覆させる」／"overturns the very logic"**——章頭の注記と同じ型。**実在する**（実物で全文を読んで確かめた）
- **観慈の見落とし**：§4 の 1 で「転覆」を探したと書いたが、当たった行を第8章の外まで一つずつ読み切らず、§1 (3) にも挙げなかった（系統外の検分に渡した抜粋の一覧には二つとも出ていた）——記憶 `feedback_grep-read-to-line-end` と同じ型
- **⑦⑧ として加えた**（登録者の裁定 09:43:10——「入れて、合格なら push まで」）：⑦ §6-6「軍拡の論理そのものを**逆転させうる**逆説」／"a paradox that **can reverse** the very logic of an arms race"・⑧ §7-5「AI軍拡の論理そのものを**逆転させうる**」／"and **can reverse** the very logic of an AI arms race"——章頭の注記と同じ語。これで直す所は**日 12 か所・英 11 か所**（日付の行を除く）
- 道具を直して作り直した：`v5_6_changes.py`（⑦⑧ の差し替え・日付の行・注記・CHANGELOG の一行と所の表・「検分」の欄・公開の行を [x] に）・`verify_v5_6.py`（置き換えの行に日 L1188・L1316・英 L1191・L1317・残りの数えの型「論理そのものを転覆」／"overturns the very logic"）→ **合格**（日 置き換え 13 行・英 12 行〔日付の行を含む〕・注記の挿入 各一・行数 +2・README 3 行・build.sh 2 行・CHANGELOG 末尾への追加だけ〔+35 行〕・残りは英 L2352 だけ〔理由つき〕・追跡済みの変更 5 ファイル・ステージ 0）
- 作業木の v5.6：日 `0838775509DAF08C…`・英 `E195A718023BBFA5…`（系統外の検分に渡した案は日 `7250ABAC…`・英 `A8E9AEA7…`——⑦⑧ と注記・日付の行・CHANGELOG の書き換えだけが違う）
**追記の保存の直後の date**：2026-10-08 09:49:52
