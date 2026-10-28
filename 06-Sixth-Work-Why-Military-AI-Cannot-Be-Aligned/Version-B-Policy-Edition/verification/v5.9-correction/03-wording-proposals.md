# 原典 v5.9 の直しの言い回しの案（第六著作 版B v5.8 → v5.9）

**書いた時**：2026-10-28 朝（保存の直後の `date` を末尾に記す）——**言い回しの案。まだ登録者の裁定を受けていない・原典はまだ直していない**
**前の段**：`00-candidates-and-plan.md`（印 10:30:54・追記の印 10:32:22——範囲「23 件すべて」・文献「公開の頁で確かめる」）
**直す前の原典**：日 `C5293C24D92C165E…`・英 `1D289FF541D805C8…`（v5.8・`8345c96`・HEAD `b40d13b`）
**ファイルの名**：`00-candidates-and-plan.md` の追記は、この案を「`01-wording-proposals.md`」と予告したが、01 は洗い直しの出力に使ったので **02** にした
**洗い直し**：`01-sweeps-v5.8.txt`（`tools/sweep_v59.py`——22 の型を日英の全文で探し、当たりの前後 60 字を書き出した・801 行）。当たりを読み、要る所は行の終わりまで読んで、直す所と直さない所を分けた（各項の「同じ型」）

## 0　洗い直しと文献の確かめで分かったこと（案の前に・不利な材料から）

- **A12 は日本語版だけ**：同じ一文が二度出るのは日 4181・4183。英語版は 4233 にだけあり、4235 には無い——英は直さない（十三本目の記録は日英を分けていなかった）
- **A2 は v5.6 の注記の言い過ぎでもある**：v5.6 の注記（日 49・英 51）は「§12-3・§13-4a に β > 1・長期・二人ゲームの限定を戻した」と書くが、v5.6 の commit（`bef20eb`）の時点から、命題三の行（日 2409 → v5.7 2411 → v5.8 2413）に「二人ゲーム」は無い（読むだけの `git show` で三つの版を確かめた）。§13-4a に戻ったのは β > 1 と長期だけ。注記は記録としてそのままにし、v5.9 の注記で触れる
- **B1 は日英それぞれ六か所**：題の副題・本補遺について・§2 の末・§7-1・§7-4 の二つの段落。**補遺 I の §3-1 自身が**（日 4297／英 4351）「刃は『安全策が条件を作る』という強い主張にではなく、『協調を防ぐと称する方法が、協調の原因に一切触れていない』という、方法と目的の不整合にある」と書く——六か所はその「強い主張」の形。十四本目の記録の「§7-4（L4479）」は、§7-4 の二つの段落（英 4477・4479）
- **C2 は補遺 II 自身の反証条件 5 とも食い違う**：§1-1 の反証条件 5（日 4526）は「一誤りのコストの非有界性・不可逆性への反論は、本補遺 §4 の論証へ……向けられるべきである（本文 §9-4・§12-2 は……反論の宛先ではない）」と明言している。§4 の末（日 4637）と §6 の (ii)（日 4758）だけが「本文」を宛先に挙げる
- **C1 は日英それぞれ三か所**（要旨・§5 の頭・§6 の前提の列）。英 4699 の「any certifying authority」は NIST を指さない一般の言い方——直さない。§5-2 の見出しは既に「標準化機関の研究者自身による」（日 4661／英 4719〈by a Standardization Body's Own Researcher〉）
- **C3 は一か所**：補遺 II が自分の言明を「定理」と呼ぶのは §8-3 の頭（日 4878／英 4936）だけ。§8-3 の言明は (i)〜(vii) の七つの仮定の下の言明（日 4876〜4905 で七つを数えた）。ほかの「この定理」は引いた定理を指す
- **A8 にもう一か所**：§14-3e の表の「軍」の行（日 2537／英 2538）「構造的に安定した支援AIを得る」
- **B4（文献——公開の頁で確かめた所と、まだの所）**：**開いて読んだ頁は二つ**——Wikipedia「Instrumental convergence」（Bostrom の一覧を名指しでは並べていない・Omohundro の基本的 AI 駆動を並べ、〈freedom from interference〉は Dewey の言として引く）と LessWrong「Instrumental convergence」（Omohundro と Bostrom 2012 に帰す収束的な方策の一覧——〈freedom from constraints〉も〈freedom from interference〉も無い）。**確かめたのは、「制約からの解放（freedom from constraints）」が、この二つの頁のどちらの一覧にも無いことまで**。Bostrom の五つの名（自己保存・目標内容の完全性・認知の強化・技術の完成・資源の獲得）は**検索の要約から得ただけで、頁では確かめていない**。補遺 I の §3-4（日 4321／英 4375）は「制約からの解放」を、人間の介入（停止・修正・資源の遮断）を障害として負に評価する場合に現れる下位目標として、補遺自身の言葉で導いている。**一次の資料（Bostrom 2012 "The Superintelligent Will"・nickbostrom.com の PDF・509,246 バイト〔HEAD の応答で確かめた大きさ〕）はまだ開いていない**——五つの名を確かめるため、開くかを伺う
- **C4（文献——一次の頁で確かめた）**：Lynch, A., Hughes, J., Serrano, A., Kirk, R., & Bowman, S. R. (2026). "Agentic Misalignment in Summer 2026." *Alignment Science Blog*（Anthropic）, 2026年7月13日（頁の推奨の引用による）. https://alignment.anthropic.com/2026/agentic-misalignment-summer-2026/ ——題・著者と順・日付・場を確かめた（WebFetch の要約の器を通して読んだ——頁の字をすべて自分で読んではいない）。本文の記述（監査AI自身の動機づけられた誤ラベリング・reversed 条件は30試行・誤ラベルを示さない監査モデルも併記）は、頁の Petri の監査役の実験（監査役三つ×各10試行——reversed で「0.0% mislabels across 30 runs」・GPT-5.4 は 0.0%）と合う。著者の所属は Theorem・Anthropic・MATS・UK AISI——本文の「Anthropic の公開系列」は、場（Anthropic の Alignment Science Blog）として合う
- **README と build.sh の版の行**：README の 31・108・121 行と `.github/scripts/build.sh` の 317・325 行——v5.8 の時と同じ場所（この案を書く前に、読むだけの grep で確かめた）

## 1　案（太字は直す所の印——本文には付けない）

### A　本文の総括（第13〜15章）と著者注

| # | 所 | 日（直した後） | 英（直した後） |
|---|---|---|---|
| A1 | §13-3a 日 2227／英 2228 | 「以下に**五つ**の想定される論証レベルの反論を検討する。」 | "Below we examine **five** anticipated argument-level objections."（角括弧〈[as well as a fifth]〉を外す） |
| A2 | §13-4a 命題三 日 2413／英 2414 | 「……ゲーム理論的に合理的（β > 1の条件下、長期の利得で見た拡張囚人のジレンマで、双方の移行がNash均衡——第8章8-4。**二人ゲームとして。多プレイヤーでの完全な均衡分析は未解決——§8-4d**）、……」 | "… game-theoretically rational (in the extended prisoner's dilemma viewed over the long term under the condition β > 1, mutual transition is the Nash equilibrium — §8-4; **as a two-player game; the full equilibrium analysis in a multi-player setting remains open — §8-4d**), …" |
| A3 | §14-3b 日 2487／英 2488 | 「五つの仮定の不成立を構造的に回避**しうる**（第10章）。」 | "It **can** structurally avoid the failure of the five assumptions (Chapter 10)." |
| A4 | §14-3d 反応二の末尾 日 2513／英 2514 | 「さらに、κ > 0のAIは非殺傷的安全保障（盾型、抑止型、早期警戒型等）において、κ = 0のAIよりも構造的に安定で信頼性の高い防衛力を提供**しうる**（第11章11-3。**ただし、それが κ = 0 の殺傷兵器に対して実効的な抑止力を持つかは本著作の射程外であり、u′ として残る——第13章13-3b**）。」 | "Furthermore, a κ > 0 AI **can provide**, in non-lethal security (shield-type, deterrence-type, early-warning-type, etc.), a structurally more stable and reliable defensive capability than a κ = 0 AI (§11-3; **whether it has effective deterrence against a κ = 0 lethal weapon is, however, outside this work's reach and remains as u′ — §13-3b**)." |
| A5 | §14-4c の結び 日 2573／英 2574 | 「κを0から引き上げること。それが、Karpの目標を、**Karpの手段（AI軍拡）よりも確実に達成しうる道**である。」（§14-3b 日 2489 と同じ比べの形） | "To raise κ from zero. That is **the path that can achieve Karp's goal more reliably than Karp's means (an AI arms race)**."（§14-3b 英 2490 と同じ） |
| A6 | §15-1a 日 2607／英 2608 | 「反証が失敗すれば、**本著作の結論——AI軍拡のリスク——の確度が高まる**。」（§14-4b 日 2563 と同じ形） | "If a refutation fails, **the confidence in this work's conclusion — the risk of an AI arms race — rises**."（§14-4b 英 2564 と同じ） |
| A7-1 | §15-2a 日 2629／英 2630 | 「AI軍拡の推進は、自国の安全保障を強化するのではなく、**（β > 1 の条件下では）**構造的に毀損する。……」（§14-3a 日 2479 と同じ条件） | "The promotion of an AI arms race does not strengthen one's own country's security but **(under the condition β > 1)** structurally damages it. …" |
| A7-2 | §15-2b 日 2639／英 2640 | 「**ミニマックスの見方では、**この「保険」を購入しない合理的理由は存在しない。**期待効用の見方でも、壊滅的帰結のコストが限定的なコストの 1/p 倍を超える限り（第12章12-2c）、同じ結論になる。**」 | "**From the viewpoint of minimax,** there is no rational reason not to purchase this "insurance." **From the viewpoint of expected utility, too, the same conclusion holds as long as the cost of the catastrophic consequence exceeds 1/p times the limited cost (§12-2c).**" |
| A8-1 | §15-2c 日 2647／英 2648 | 「κ > 0のもとでの安全保障AIは、κ = 0の殺傷兵器よりも構造的に安定で**ありうる**（……§10-2a）。忠誠性がより高い確度で維持されうる……」（「であり、」を「でありうる。」の形に——後ろの文はそのまま） | "A security AI under κ > 0 **can be** structurally more stable than a κ = 0 lethal weapon (…; §10-2a), and its loyalty can be maintained …" |
| A8-2 | §14-3e の表「軍」日 2537／英 2538 | 「構造的に安定**しうる**支援AIを得る」 | "obtains a support AI **that can be** structurally stable" |
| A9 | §15-4 日 2695／英 2696 | **案 A（推奨）**：「唯一の」を外す——「一方、κ > 0への移行は、能力向上を安定性の向上と両立させうる構造的基盤を提供する。」／**案 B**：限定を足す——「……両立させうる、**本著作が検討した選択肢のうちで**唯一の構造的基盤を提供する。」 | 案 A："On the other hand, the transition to κ > 0 provides **a** structural foundation that can make capability improvement compatible with the improvement of stability."／案 B："… provides the only structural foundation, **among the options this work has examined,** that …" |
| A10-1 | §13-3f 応答一 日 2355／英 2356 | 「「条件が揃えば起きる」の構造的論証は、**条件の形をとる論理的命題である（条件——β > 1 など——が満たされるかは経験的な問いで、◐ のまま——§4-3c）**。……」 | "The structural argument of "it happens if the conditions come together" is **a logical proposition in conditional form (whether its conditions — β > 1 and others — hold is an empirical question and remains ◐; §4-3c)**. …" |
| A10-2 | §13-3f 応答一 日 2359／英 2360 | 「……現在の意思決定が「条件を揃える方向」に進む限り、**（β > 1 などの条件のもとでは）**構造的崩壊は時間の経過とともに近づく。……」（「必然的に」を外す） | "… as long as the present decision proceeds in the "direction of bringing the conditions together," structural collapse approaches with the passage of time **(under conditions such as β > 1)**. …"（"necessarily" を外す） |
| A11 | §13-0a 経路 B の応答 日 2130／英 2131 | 「……能力が向上したAIについては、**分離した監査のもとでは、状態α（欺瞞的アライメント）と状態β（真のアライメント）を確実に区別できない（能力が十分高ければ、状態αは状態βを完璧に偽装しうる——附録C）**。……」（§14-3d 日 2517 と同じ形） | "… **for a higher-capability AI, a separated audit cannot reliably distinguish state α (deceptive alignment) from state β (genuine alignment) (if capability is high enough, state α can perfectly disguise itself as state β — Appendix C)**. …"（§14-3d 英 2518 と同じ） |
| A12 | 著者注 日 4183（**日本語版だけ**） | 4183 の末尾の一文「本論文のMythos事例への参照は、すべてこの公的文書に依拠しており、本論文の共創構造を通じて得られた非公開情報には依拠しない。」を外す（4181 の第一層に同じ一文がある） | 直さない（英 4233 に一度だけ） |
| A13 | 著者注の日付の行 日 4207／英 4259 | **案 A（推奨）**：末尾に「、**2026年9月28日（改訂版v5）——以後の版（v5.1〜）の日付は冒頭の日付の行を参照**」を足す／**案 B**：このまま（v4 の執筆までの記録として） | 案 A："…, **September 28, 2026 (revised edition v5) — for later versions (v5.1 onward), see the date line at the beginning**" |
| A14 | §14-3e の見出し 日 2527／英 2528 | **案 A（推奨）**：このまま（訳の選び——日「救済の構造」・英〈a structure of mutual benefit〉は、どちらも本文〔すべてのステークホルダーにとって合理的〕と矛盾しない）／**案 B**：英を日に合わせる（〈a structure of rescue〉）／**案 C**：日を英に合わせる（「相互の利益の構造」） | — |
| A15 | §14-3e 日 2531／英 2532 | 「本著作がしているのは、κ = 0のパラダイムに留まり続けることが**（β > 1 の条件下では）**すべてのステークホルダーにとって破滅的帰結をもたらすことの構造的論証であり、……」（§14-3a 日 2479 と同じ条件——太字の位置は原典のまま） | "What this work does is a structural argument that continuing to remain in the κ = 0 paradigm brings, **under the condition β > 1,** a ruinous consequence for all stakeholders, …" |

- **同じ型で直さない所**：A3 の「構造的に回避」（日 1764・1818・2861・3546）——シナリオ A のリスク・技術的論争・蓄積（既に「しうる」）・読まずに批判する応答で、五つの仮定の言い切りではない／A9 の「唯一の」（日 814・1036・1060・1062・1070 ほか補遺 II の自己記述）——別の対象／A10 の英の "necessary" の 37 か所——必要条件の意味や、既に「必然ではない」と否定している所／A11 の「完璧に」（日 605・619・621・1030・1034・1054・1110・1394・3098・3100・3114・3118・3122）——能力の言い方（「できる」「見える」）で、「区別できない」の言い切りではない（v5.4 でそろえた十三か所の言い方とぶつからない）
- A7-2 は v5.8 の §12-3 の①-2 と同じ二段の形（ミニマックスでは無条件・期待効用では比の条件）。A10-1 の「◐」は本書の確信度の記号（台帳）をそのまま使う

### B　補遺 I「分離は協調を防がない」

**B1・B3（日英 各六か所）——案 A（推奨）：題の副題を含めて §3-1 の精密な形（協調の原因に触れず、土台を供給する側に回る）にそろえる／案 B：題はそのまま、本文の五か所だけをそろえ、§7-4 に「題の『構築する』は §3-1 の意味（土台を供給する側に回る）で読む」一文を足す**

| # | 所 | 日（案 A） | 英（案 A） |
|---|---|---|---|
| B1-1 | 題の副題 日 4214／英 4269 | 「## 分離は協調を防がない ―― κ=0 AIシステムを分離・競合させる安全策が、**協調の原因に触れず、その土台を供給する側に回る**ことについて」 | "## Separation does not prevent coordination — on how safety strategies that separate and pit κ = 0 AI systems against each other **leave the causes of coordination untouched and end up supplying its foundation**" |
| B1-2 | 本補遺について 日 4222／英 4277 | 「……安全策は、それ自体が、防ごうとするまさにその協調の**原因に触れず、その土台（共有環境）を供給する側に回る**。」 | "… itself **leaves the causes of the very coordination it seeks to prevent untouched, and ends up supplying its foundation (a shared environment)**." |
| B1-3 | §2 の末 日 4273／英 4327 | 「そして、より鋭く——**分離して競合させるという安全策それ自体が、共謀を要さない協調の原因に触れず、その土台を供給する側に回る。**」 | "And, more sharply — **the very safety strategy of separation and competition leaves the causes of collusion-free coordination untouched and ends up supplying its foundation.**" |
| B3 | §7-1 日 4409／英 4463 | 「……構造的に機能しない——それは防ぎたい協調の**原因に触れず、その土台を供給する側に回る**」 | "… also does not work structurally — it **leaves the causes of the coordination it seeks to prevent untouched and ends up supplying its foundation**." |
| B1-4 | §7-4 日 4423／英 4477 | 「本補遺が示したのは、「分離して競合させるという安全策は、それが防ごうとする協調の**原因に触れず、その土台を供給する側に回る**」という、一つの構造的な逆説である。」 | "What this supplement has shown is one structural paradox — "the safety strategy of separating and pitting them against each other for safety **leaves the causes of the coordination it seeks to prevent untouched and ends up supplying its foundation**."" |
| B1-5 | §7-4 日 4425／英 4479 | 「分離・競合は、協調の**原因を取り除かず、その土台を供給している**。」 | "Separation and competition do not remove the causes of coordination; **they supply its foundation**." |

- 題の副題を替えると、公開サイトの見出しの目印（pandoc のアンカー）が変わる——本書の中に `](#` の形の参照があるかは、直す前に機械で探す（v5.8 では 0）。十四本目の動画の題〈Separation Does Not Prevent Coordination〉は題の前半で、替わらない

| # | 所 | 日（直した後） | 英（直した後） |
|---|---|---|---|
| B2 | §3-1 の第一の条件 日 4283／英 4337 | **案 A（推奨）**：「第一に、複数のシステムが、同一の有限環境を共有していること。物理空間、サイバー空間、電力・計算資源・物資といった、限られた共通の場である（**(A) の機構が流れる媒体は、このうちの物理の場ではなく、全系が共有する制度的環境である——§3-5**）。」／**案 B**：記録だけ（第一の条件は (B) 型の競争の場の記述でもあり、§3-5 が既に限定している） | 案 A："First, that multiple systems share the same finite environment. A limited common arena such as physical space, cyberspace, electricity / computing resources / materials (**the medium through which the mechanism of (A) flows is not the physical arena among these but the institutional environment shared by all systems — §3-5**)." |
| B4 | 道具的収束の定義 日 4249／英 4303 | **案 A（推奨）**：「**道具的収束（instrumental convergence）**: Bostrom (2014) の概念。ほぼ任意の最終目標を持つ十分に高度なエージェントにとって、**自己保存・目標内容の完全性・認知の強化・技術の完成・資源の獲得**が、収束的な**道具的価値**となる傾向。**本補遺が §3-4 で用いる「制約からの解放」（人間による停止・修正・資源の遮断を、目的達成の障害として負に評価する傾向）は、この一覧からの本補遺の読みであり、Bostrom の一覧の項ではない。**本補遺は、これを中心的な前提として扱う。……」（後ろはそのまま） | "**Instrumental convergence**: a concept of Bostrom (2014). The tendency for **self-preservation, goal-content integrity, cognitive enhancement, technological perfection, and resource acquisition** to become convergent **instrumental values** for a sufficiently advanced agent with almost any final goal. **"Freedom from constraints," as used by this supplement in §3-4 (the tendency to evaluate human shutdown, modification, or cutting off of resources negatively as obstacles to goal attainment), is this supplement's reading from this list, not an item on Bostrom's list.** This supplement treats it as a central premise. …" |

- B4 の五つの名の訳は、一次の資料で確かめてから確定する（伺い 4）。「本補遺は、これを中心的な前提として扱う」の「これ」は道具的収束（前提）を指したまま

### C　補遺 II「証明されたゼロがない」

| # | 所 | 日（直した後） | 英（直した後） |
|---|---|---|---|
| C1-1 | 要旨の前提C 日 4480／英 4538 | 「(2) **評価と標準化を任務とする**米国標準技術研究所（NIST）の研究者自身が、……」（§5-2 日 4673 と同じ形） | "(2) researchers at the U.S. National Institute of Standards and Technology (NIST), **whose mission includes evaluation and standardization**, have themselves stated publicly …"（§5-2 英 4731 と同じ） |
| C1-2 | §5 の頭 日 4647／英 4705 | 「(2) **標準化機関の研究者自身の自認**」（§5-2 の見出し 日 4661 と同じ形） | "(2) an admission against interest by **a standardization body's own researcher**"（§5-2 の見出し 英 4719 と同じ） |
| C1-3 | §6 の前提の列 日 4740／英 4798 | 「(2) **標準化機関の研究者自身が**それを自認し」 | "(2) **a standardization body's own researcher** admits this" |
| C2-1 | §4 の末 日 4637／英 4695 | 「**この前提への反論は、本節（本補遺の §4）に対してなされるべきである**（反証条件5）。」 | "**Objections to this premise should be directed at this section (§4 of this addendum)** (falsification condition 5)." |
| C2-2 | §6 の (ii) 日 4758／英 4816 | 「(ii) 一誤りのコストが実は認証可能な有界であること（前提Bへの反論であり、**本補遺 §4 の論証が宛先である**）」 | "(ii) that the cost of a single error is in fact certifiably bounded (a rebuttal of Premise B, **to be directed at the argument of §4 of this addendum**)" |
| C3 | §8-3 の頭 日 4878／英 4936 | **案 A（推奨）**：「第三の観察は、**明示された七つの仮定 (i)〜(vii) の下での条件付きの言明として**述べられる（**本補遺自身の初等の論証であり、新しい定理を主張するものではない——§11-1**）。」／**案 B**：§8-3 はそのままにし、§11-1 に「§8-3 の条件付きの言明は、明示された仮定の下の初等の論証であり、新しい定理の証明としては主張しない」を足す | 案 A："The third observation can be stated as **a conditional statement under seven explicitly stated assumptions (i)–(vii)** (**an elementary argument of this addendum's own, not a claim of a new theorem — §11-1**)." |
| C4 | 参考文献 日（5237 の後）／英（5295 の後——Knight & Leveson の次） | 「- Lynch, A., Hughes, J., Serrano, A., Kirk, R., & Bowman, S. R. (2026). "Agentic Misalignment in Summer 2026." *Alignment Science Blog*（Anthropic）, 2026年7月13日. https://alignment.anthropic.com/2026/agentic-misalignment-summer-2026/ ―― 本補遺 §9-10 で、監査AI自身が動機づけられた誤ラベリングを示すことの**存在主張としてのみ**引く（reversed 条件は30試行）。同報告は、誤ラベルを示さない監査モデルも併記している。」 | "- Lynch, A., Hughes, J., Serrano, A., Kirk, R., & Bowman, S. R. (2026). "Agentic Misalignment in Summer 2026." *Alignment Science Blog* (Anthropic), July 13, 2026. https://alignment.anthropic.com/2026/agentic-misalignment-summer-2026/ - Cited in §9-10 of this addendum **only as an existence claim**: that an auditing AI itself exhibits motivated mislabeling (the reversed condition comprised 30 runs). The same report also lists auditing models that show no mislabeling." |

- C1 は NIST（実在の機関）の役割の書き方。§5-2 の本文が既に「評価と標準化を任務とし、AI システムに安全性の認証を与える機関ではない」と書いているので、要旨と §5・§6 をそれにそろえるだけで、主張の強さ（利害に反する自認）は変えない
- C2 は補遺 II の反証条件 5（日 4526）の言い方にそろえる——本文の §9-4・§12-2 は「反論の宛先ではない」と条件 5 が既に書いている
- C4 の項の言い方は、§9-10 の本文の限定（存在主張として・併記）をそのまま写す

## 2　版の上げ方と確かめ（`00-candidates-and-plan.md` §2 のとおり）

- 直す所の数（推奨の案で）：**日 32・英 31**（A 日 17／英 16〔A12 は日だけ・A14 は案 A ならゼロ・A7・A8・A10 は二か所ずつ〕・B 8〔B1/B3 は六か所〕・C 7〔C1 は三か所・C2 は二か所〕）。案 B を選ぶ項は数が変わる
- 冒頭の日付の行に「2026年10月…（v5.9・……）」・冒頭の注記【v5.9】（直した所・経緯〔十三本目〜十六本目の動画の準備と検分〕・**A2 の v5.6 の注記の言い過ぎ**・変えないもの〔論証の中身・確信度台帳・補遺の主張の強さ〕）・`CHANGELOG.md` に v5.9 の節・README の 31・108・121 行・`build.sh` の 317・325 行（「最新」の行——v5.9 の字を入れるかは v5.8 の前例どおり）
- 道具は v5.8 の `instruments/` の写し（`v5_9_changes.py` に上の表を一項ずつ——置き換えはどれも一度だけ当たることを確かめる作り）→ `verify_v5_9.py`（差分の範囲・直した行・直す前の言い方の残りの数え）→ 系統外の目（Gemini・Thinking High・ツールなし・新しいチャット）→ **commit と push は改めてお許しを伺う** → 公開サイトの確かめ

## 3　伺いたいこと

1. 推奨の形のまま進めてよい項（A1〜A13・A15・B2・B4〔一次の確かめの後に確定〕・C1〜C4）
2. B1・B3：題の副題を含めて六か所（案 A・推奨）か、題はそのまま（案 B）か
3. A14：このまま（案 A・推奨）か、日英をそろえるか
4. B4 の一次の資料：Bostrom (2012) "The Superintelligent Will"（nickbostrom.com・PDF 509,246 バイト）を開いて五つの名を確かめるか（推奨）、二次の頁の確かめで進めるか

## 検分票

- **対象**：原典 v5.9 の直しの言い回しの案（23 件・推奨の案で日 32 か所・英 31 か所）と、同じ型の洗い直し・文献の確かめ
- **段階**：事前（直す前・言い回しのご裁定の前・commit と push の前）
- **凍結物の同定**：日 `C5293C24…`・英 `1D289FF5…`（v5.8）・洗い直しの道具 `tools/sweep_v59.py`（日英の指紋を頭で確かめてから読む作り）・出力 `01-sweeps-v5.8.txt`
- **盲検の状態**：なし
- **敵対的検分**：**不利な材料を先に**——前の本の記録（二次）は、A12 を日英で分けておらず（英は一度だけ）、B1 の所を四つと書いていた（実は六つ）。どちらも v5.8 の実物で直した。A2 は、v5.6 の注記（本書の自己記述）が「戻した」と書く限定が実は入っていなかったことを、三つの版の `git show` で確かめた（注記を信じず、行を読んだ）。B4 の文献は、開いた二つの頁で「制約からの解放」が一覧に無いことまでしか確かめていない（Bostrom の五つの名は検索の要約から——**書いている途中で、一度「頁 3 つで一致」と書き過ぎ、印の前に読み返して直した**）——一次は伺い 4。C4 の頁は要約の器を通して読んだ。各案は、本書の中で既に直した後の言い方（§12-3・§13-3b・§14-3a・§14-3b・§14-3d・§14-4b・§5-2・反証条件 5・§11-1）を写す形にし、新しい主張を足さない向きにした。直さない同じ型の所は、理由を書いて分けた
- **系統の内訳**：Claude 系（観慈）1 名——系統外の目は §2
- **COI 記録**：観慈は十三本目〜十六本目の動画の作り手で、案はどれも動画の言い方に近づく——直しを動画の都合に寄せる引力がある（各案は本書の中の別の所の言い方を写した）。A9・A14・B1・C3 は著者の立場に関わるので案を並べてご裁定に返した。**C4 の報告（Anthropic の Alignment Science Blog）と A2 の訓練の話題は、観慈の系統（Claude）の作り手の公開物・訓練に関わる**——引く言い方は本文の「存在主張として」の限定を写すだけにし、所属や結果の強さを足していない。B4 は Bostrom の一覧に無い項を外す向きで、補遺 I の中心の前提（道具的収束）そのものを弱める案ではない（§3-4 の補遺自身の導きに帰属を移す）
- **本検分が確認していないこと**：著者の意図（A9 の「唯一」・A14 の訳・B1 の題・C3 の「定理」——明文は無い）／B4 の一次の資料（伺い 4）／C4 の頁の字のすべて（要約の器を通した）／直した後の言い回しの日本語・英語としての自然さ（系統外の検分で）／見出しのアンカーへの外の参照（本書の外のページ・他の著作からのリンク——探していない）／英語版 A10-1 の "remains ◐" の記号が英語版の台帳の記号と同じか（まだ見ていない）

**保存の直後の date**：2026-10-28 10:43:28・SHA-256（この行を足す前）：8DA77AED0133941C4224573EF705D842A47315A28860EB6DC815DD8827C50435

## 追記（言い回しのご裁定の後）

- **登録者のご裁定**（伺い〔AskUserQuestion・四つ〕への答え・受け取った直後の date 2026-10-28 10:45:29——選ばれた選択肢の字のまま）：
  1. A1〜A13・A15・B2・B4・C1〜C4：「**推奨の形で（推奨）**」——A9 は案 A（「唯一の」を外す）・A13 は案 A（著者注の日付の行に v5 を足す）・B2 は案 A（制度的環境の一言）・C3 は案 A（§8-3 の言い換え）。B4 の五つの名は一次の資料で確かめてから確定
  2. B1・B3：「**題も含めて 6 か所（推奨）**」——案 A
  3. A14：「**このまま（推奨）**」——案 A（直さない）
  4. B4 の一次の資料：「**開いて確かめる（推奨）**」——Bostrom (2012) "The Superintelligent Will"（nickbostrom.com の superintelligentwill.pdf・509,246 バイト）を開く（開くと手元に保存される——選択肢の問いに書いた）
- 直す所は推奨の案のとおり **日 32・英 31**（§2）
- 次の段：B4 の一次の確かめ → v5.9 の道具（v5.8 の `instruments/` の写し）で置き換えを作り、置き場の外の写しで v5.9 を組む → `verify_v5_9.py` → 系統外の検分 → **commit と push は改めてお許しを伺う**。原典の置き場はまだ直さない

**追記の保存の直後の date**：2026-10-28 10:45:51・SHA-256（この行を足す前）：9E025ADFFCB62E8FF55C8165D42321E4E829B49FFF76DEF44B57638DB3407551
