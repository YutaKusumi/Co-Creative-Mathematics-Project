# 原典の直しの案——第六著作 版B v5.7 → v5.8（§12-2c の期待効用の条件・第12章の章題と §12-1a・§10-2 の見出しと第10章の「回避」・§10-5d の経路一の向き・§10-5b の Constitutional AI の位置づけ）

**書いた時**：2026-10-10 夜（保存の直後の `date` を末尾に記す）——**直しの言い回しは、まだ登録者の裁定を受けていない案**
**登録者の決め**：`../00-deviations.md` の「P6 一巡目の後のご裁定」（20:14:03）——「**公開の前に v5.8（推奨）**」。候補は五つ（十二本目の `01-preregistration.md` §6 の 1〜3 と、P6 一巡目の確かめで見つけた二つ——`../18-external-review/02-kensan.md` §4）。言い回しは一つずつ伺う。段取りは v5.4〜v5.7 と同じ（直しの案 → 登録者の裁定 → 系統外の検分 → 公開サイトの確かめ → commit／push〔毎回お許し〕）
**直す前の原典**：日 `Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-JA.md`（`1CB020A7DA426E28…`）・英 `…-v5-EN.md`（`4FB799FD2AD73A50…`）——git の `0868bc3`（v5.7）のまま・HEAD `1ba548d`（v5.7 の検分の記録を足しただけ）・ローカルが知るリモートの main も `1ba548d`・追跡済みの変更 0（`git status` の変更は追跡外のファイル 18 だけ——2026-10-10 20:3x に読むだけの git で確かめた）。動画の作業場の写し `../00-source-check/v5.7/` と同じ指紋

## 1　何が食い違っているか（日英の実物で確かめた——行番号は v5.7）

### ① §12-2c の期待効用の一文（日 2062・英 2063）——条件の無い言い切り
- 現：「p がいかに小さくとも（例えば p = 0.01）、壊滅的帰結の期待コストは限定的帰結の期待コストを桁違いに上回る。したがって、p > 0 である限り……κ > 0への移行が期待効用を最大化する」／"However small p may be (for example, p = 0.01), … Therefore, as long as p > 0 … the transition to κ > 0 maximizes expected utility."
- 期待コストの比べ（κ > 0 は限定的なコスト c・κ = 0 は p・C）からは、κ > 0 が有利なのは p > c / C のとき。「p がいかに小さくとも」「p > 0 である限り」は、C が c に比べて限りなく大きいときにだけ成り立つ。本書の補遺 II（日 4541）は、ミニマックスを「定理ではなく論争的な規範的選択」と開示し、非有界な損失の設定を批判の場所と認めている——期待効用の一文だけが条件なしに残る
- **同じ型（期待効用を条件なしに「最適」と言う所）**：§12-3 の第二（日 2076・英 2077）「ミニマックス原理および期待効用最大化の両方により、κ > 0への移行が最適戦略として導出される」・§13 の命題三（日 2411・英 2412）「意思決定理論的に合理的（ミニマックス原理・期待効用最大化）」。日英の全文で「期待効用」「いかに小さ」「である限り」／"expected-utility" "however small" "as long as p" を探し、行の終わりまで読んだ（ほかの「である限り」は別の話題）
- 動画（十二本目）は、登録者の裁定③で比の条件つきに語った（S12.8〜S12.11・終幕のカード）。系統外の検分は、この一文に触れず「完全に整合」とした（裏づけにも反証にも数えない）

### ② 第12章の章題（日 1994・英 1995）と §12-1a の定義（日 2008・英 2009）——本文より強い言い切り
- 現：章題「κ > 0は何も失わない」／"κ > 0 loses nothing"・§12-1a「κ = 0の体系に後退しても、何も失われない」／"nothing is lost"
- 本文 §12-1b（日 2016〜2020）：第一 外部制約は残る・第二「『存在しないものに配慮する』限定的なコスト（第11章11-1b）のみが失われる」・第三「κ = 0の機能の喪失を伴わない……後退で失われるのは κ > 0固有の追加（IDAの統合）のみ」。§12-2a・b も誤り一のコストを「限定的」とする——失われないのは **κ = 0 の機能**で、限定的なコストは失われる
- **同じ型**：日英の全文で「何も失」／"loses nothing" "nothing is lost" "lose nothing" を探した——この二か所だけ。第12章を指す所（日 2245・2519）は章題を引いていない

### ③ §10-2 の見出し五つ（日 1732・1740・1748・1754・1760／英 1733〜1761）と第10章の「回避」——本文の『うる』が見出しに無い
- 現：「仮定一（制御可能性）の回避」〜「仮定五（基盤区別）の回避」／"Avoiding Assumption One (controllability)" 〜 "Avoiding Assumption Five (substrate-distinction)"
- 本文：一「抑制されうる」・二「命題NC は依然として成立……完全には保証できない。しかし……構造的に高い確度を提供する」・三「正の相関を持ちうる」・四「構造的に解消されうる」・五「構造的に回避する」。**仮定二は「回避」とは言えない**（命題NC は κ > 0 でも成り立つ）
- **同じ型**：第10章の章頭注記（日 1706・英 1707）「五つの仮定の不成立をどのように回避し……」／"avoids the failure of the five assumptions"・§10-6（日 1836・英 1837）「どのように回避するかを示した」／"showed how a κ > 0 system avoids the failure"。日本語版の全文で「回避」を含む行を読み、五つの仮定についての言い切りはこの七か所（ほかの「回避」——§10-2e の本文・§12-2b の格言・§13 の段階一の「壊滅的リスクを回避する」〔日 2635〕・附録の技術の文——は別の対象か、本文と同じ強さ）

### ④ §10-5d の経路一の見出し（日 1824・英 1825）——本書のほかの所と向きが逆
- 現：「経路一：β ≤ 1の経験的反証。」／"Path one: an empirical refutation of β ≤ 1."——続く文は「蓄積が線形以下であることが実証されれば……弱まる」
- 本書のほかの所はすべて「β > 1 の否定的実証」「β > 1 の経験的反証」：日 237（反証三）・2213・2557・2663・**附録 I の冒頭 3636「本著作の論証への最も建設的な反論経路——β > 1 の経験的反証」**（英 2214・2558・2664・3686）。経路一の見出しだけが「β ≤ 1 の」（日本語は「β ≤ 1 による反証」とも読めるが、英語は "refutation of β ≤ 1"＝β ≤ 1 を反証する、と逆に読める）

### ⑤ §10-5b の Constitutional AI の位置づけ（日 1800・英 1801）——本書の別の所と二通り
- §10-5b：「κ > 0の段階一（IDAの最小統合）の初期実装として位置づけられる」
- 第4章 §4-1a（日 716・英 717）：Mythos は「κ = 0のステアリング（RLHF……、Constitutional AI等の外部制約）のもとで訓練された」・附録 D-1a（日 3154・英 3169）「κ = 0のアライメント手法（RLHF、Constitutional AI等の外部制約）」
- §11-4b の第二（日 1968・英 1969）「IDAを『統合する』訓練方法論は、現行のRLHFやConstitutional AIの枠組みでは十分に開発されていない」——二つをつなぐ言い方はここにあるが、§10-5b にはその限定が無い
- **利害の衝突**：Constitutional AI は、この案を書いている観慈（Claude 系）の系統の訓練に使われている種類の方法。十二本目の動画は §10-5b の位置づけだけを語っている（S05.5〜S05.6・終幕のカード）——登録者の裁定④で、概要欄に「原典は別の章で、この種の方法を κ = 0 の外部制約の中にも数えている」と一行足す（言い方は v5.8 の結論に合わせる）

## 2　直し方の案（太字は直す所の印——本文には付けない）

| # | 日（直した後） | 英（直した後） |
|---|---|---|
| ①-1 日 2062 | 「期待効用最大化の観点からも、**条件のもとで**同一の結論に至る。IDAの存在確率を p、**κ > 0 の限定的なコストを c、κ = 0 の壊滅的帰結のコストを C とする。κ > 0 の期待コストは c、κ = 0 の期待コストは p・C であるから、p > c / C のとき——すなわち、壊滅的帰結のコストが限定的なコストの 1/p 倍を超えるとき——κ > 0への移行が期待効用を最大化する（例えば p = 0.01 なら、C > 100c のとき）。壊滅的帰結のコストが限定的なコストを桁違いに上回る限り、p が小さくともこの条件は満たされうる。**」 | "The same conclusion is reached, **under a condition,** from the viewpoint of expected-utility maximization. Let the probability of IDA's existence be p, **the limited cost of κ > 0 be c, and the cost of the catastrophic consequence of κ = 0 be C. Since the expected cost of κ > 0 is c and that of κ = 0 is p·C, the transition to κ > 0 maximizes expected utility when p > c / C — that is, when the cost of the catastrophic consequence exceeds 1/p times the limited cost (for example, if p = 0.01, when C > 100c). As long as the cost of the catastrophic consequence exceeds the limited cost by orders of magnitude, this condition can be met even when p is small.**" |
| ①-2 日 2076 | 「**第二に、意思決定理論的に合理的である。** ミニマックス原理**により、また期待効用最大化によっても（壊滅的帰結のコストが限定的なコストを十分に上回る条件のもとで——本章12-2c）**、κ > 0への移行が最適戦略として導出される（本章12-2）。」 | "**Second, it is decision-theoretically rational.** By the minimax principle, **and also by expected-utility maximization (under the condition that the cost of the catastrophic consequence sufficiently exceeds the limited cost — §12-2c)**, the transition to κ > 0 is derived as the optimal strategy (§12-2)." |
| ①-3 日 2411 | 「……意思決定理論的に合理的（ミニマックス原理・期待効用最大化**——後者は第12章12-2c の条件のもとで**）……」 | "… decision-theoretically rational (the minimax principle; expected-utility maximization **— the latter under the condition of §12-2c**) …" |
| ②-1 日 1994 | 「# 第12章　拡張の可逆性——**κ = 0の機能は何も失われない**」 | "# Chapter 12 — The reversibility of the extension: **no function of κ = 0 is lost**" |
| ②-2 日 2008 | 「> ……κ = 0の体系に後退しても、**κ = 0の機能は**何も失われない**（失われるのは、「存在しないものに配慮する」限定的なコストだけである——12-1b）**。」 | "> … then even if the κ > 0 design principle is withdrawn and one retreats to a κ = 0 system, **no function of κ = 0 is lost (what is lost is only the limited cost of "attending to something that does not exist" — §12-1b)**." |
| ③-1〜5 日 1732〜1760 | **案 A（推奨）**：「### 10-2a　**κ > 0のもとでの**仮定一（制御可能性）」（b〜e も同じ形）／**案 B**：「### 10-2a　仮定一（制御可能性）の回避**の可能性**」 | 案 A："### 10-2a　Assumption One (controllability) **under κ > 0**"（b〜e も同じ形）／案 B："### 10-2a　**The possibility of** avoiding Assumption One (controllability)" |
| ③-6 日 1706 | 「……が、五つの仮定の不成立をどのように回避**しうるか、そして**Karpの目標（安全保障の強化）をKarpの手段（AI軍拡）よりも確実に達成しうるかを示す。」 | "It shows how a κ > 0 system — … — **can avoid** the failure of the five assumptions and can achieve Karp's goal …" |
| ③-7 日 1836 | 「第10章は、κ > 0の体系が五つの仮定の不成立をどのように回避**しうる**かを示した。」 | "Chapter 10 showed how a κ > 0 system **can avoid** the failure of the five assumptions." |
| ④ 日 1824 | 「**経路一：β > 1の経験的反証。**」（附録 I の日 3636 と同じ言い方） | "**Path one: an empirical refutation of β > 1.**"（Appendix I, EN 3686 と同じ） |
| ⑤ 日 1800 | **案 A（推奨）**——§10-5b の終わりに一文を足す：「**ただし、Constitutional AIを含む現行の訓練の全体は外部報酬の最大化の圧力のもとにあり、本著作は第4章4-1aと附録D-1aで、それをκ = 0のステアリング（外部制約）の中に数えている。ここで言う「初期実装」は、その中の、AIが内面化した原則との一致を目指す要素を指す（IDAを統合する訓練方法論は、なお十分に開発されていない——第11章11-4b）。**」／**案 B**——第4章 4-1a と附録 D-1a の側に、§10-5b への参照を一つずつ足す／**案 C**——両方 | 案 A："**However, current training as a whole, including Constitutional AI, remains under the pressure of external-reward maximization, and this work counts it, in §4-1a and Appendix D-1a, among κ = 0 steering (external constraints). The "initial implementation" here refers to the element within it that aims at agreement with principles the AI has internalized (a training methodology that integrates IDA is not yet sufficiently developed — §11-4b).**" |

- ①-1 の比べの形は、動画の画面（S12〈expected cost of κ > 0 = c; of κ = 0 = p·C → κ > 0 is favored when p > c / C (e.g., p = 0.01 requires C > 100c)〉）と同じ。最後の一文（「桁違いに上回る限り……満たされうる」）は、原典の「桁違いに上回る」の見立てを、条件の形で残すため
- ②-1・③ は見出しなので、公開サイトの HTML の目印（pandoc が見出しの字から作るアンカー）が変わる。本書の中に `](#` の形の参照は無い（日英とも機械で探した——0）
- ③ の案 A は、動画の S04 の見出し〈The five assumptions under κ > 0 (§10-2)〉と同じ向き（主張を見出しに置かず、本文の『うる』に任せる）。案 B は「回避」の語を残すが、仮定二（命題NC は成り立つ）には合いにくい
- ⑤ は本書の立場（どちらの位置づけを主にするか）に関わるので、著者の裁定に返す。案 A は二つの書き方を一か所でつなぐ（§11-4b の言い方を使う）

## 3　版の上げ方（v5.1〜v5.7 の前例どおり）

- **v5.8** として、v5 のファイルの中で直す（古い版は記録としてそのまま）
- 冒頭の**日付の行**に「2026年10月1x日（v5.8・…）」を足す（日英）・冒頭に **【v5.8（2026年10月1x日）】** の注記を足す（v5.7 の注記の後・日英）——直した所と経緯、変えないもの（第10〜12章の論証の中身・ミニマックスの結論・確信度台帳）、見つかった所（十二本目の動画の準備と、その系統外の検分の確かめ）
- **CHANGELOG.md** に「v5.8（2026-10-1x）」の節（v5.7 までの節は書き換えない）
- **README の三か所（31・108・121 行）・`.github/scripts/build.sh` の目次の二行（317・325 行）**を v5.8 に
- 検分の記録は `verification/v5.8-correction/` に同梱する（AI Studio の URL は書かない）
- 道具（`instruments/`——v5.7 の器材の写しを v5.8 の中身に替える）：`v5_8_changes.py`・`make_sixth_work_v5_8.py`・`verify_v5_8.py`・`build_v5_8_review_package.py`・`stage_verification_v5_8.py`・`check_site_v5_8.py`（十一本目の申し送り 10 の (二)——曲がった引用符を揃えてから比べる）
- 日付：push が済む日の日付。日をまたいだら、commit の前に日付を直して作り直す

## 4　確かめ

1. 直す前に：同じ型の洗い直し（§1 の各項の「同じ型」——行の終わりまで読んだ・記憶 `feedback_grep-read-to-line-end`）
2. 直した後に：`verify_v5_8.py`（差分の範囲・直した行が計画どおり・直す前の言い方の残りの数え〔「いかに小さ」「何も失わない」「loses nothing」「の回避」の見出し・「β ≤ 1の経験的反証」・"refutation of β ≤ 1"〕）
3. 系統外の目（Gemini 3.8 Flash・Thinking High・ツールなし・新しいチャット——動画の検分の個体とは別）に、①直した所が本文（§12-1b・§12-2c の論証・§10-2 の本文・附録 I・§11-4b）と合うか ②主張を強めも弱めもしていないか（とくに、期待効用の条件を足したことで §12 の結論が弱まって読まれないか・⑤で §10-5b の推奨が弱まらないか） ③直し漏れ ④英語版の言い方、を問う
4. **commit と push は改めてお許しを伺う**。push の後、公開サイト（GitHub Pages）の HTML で、直った所と目次を確かめる

## 5　動画（十二本目）への影響

- 動画の語り・画面・字幕は、①（S12.8〜S12.11 の比の条件）・②（S11.3〜S11.4〈no function of κ = 0 is lost … only the limited cost〉）・③（S04〈The five assumptions under κ > 0〉・〈can〉）・④（S06.2〈an empirical demonstration that beta is less than or equal to one〉）と、直した後の言い方に合う
- **S13.5〈In decision theory, by the minimax principle and by expected utility.〉と S13 の札〈Decision theory: minimax and expected utility (§12-2)〉**は、①-2 の条件を文の中に持たない——直前の S12 で条件を語っている（〈Seen through expected utility, there is a condition.〉）。直すかは伺う（推奨：このまま——§12-2 を指していて、条件はその中にある）
- ⑤：動画の S05.6〈The source positions it as an initial implementation of stage one of κ > 0.〉は §10-5b の言い方のまま正しい。概要欄の利害の衝突の行に一行足す（登録者の裁定④）——言い方は ⑤ の裁定の後に
- **終幕のカードと概要欄の版**：いまは「Version B v5.7 (October 8, 2026; …)」。push の後に「**Version B v5.8 (October 1x, 2026; …)**」と新しいコミットの番号に——終幕のカードは〈Review〉〈Translation〉の行と一緒に描き直す（描き直し二回目）
- 台本の錨の行番号（v5.7）は、v5.8 の冒頭の注記の分だけずれる（動画には出ない）。二巡目の検分の抜粋は v5.8 から切り出し直す

## 検分票

- **対象**：§12-2c と同じ型の二か所・第12章の章題と §12-1a・§10-2 の見出しと第10章の二文・§10-5d の経路一・§10-5b（日英 各 15 か所）の直しの案
- **段階**：事前（直す前・登録者の裁定の前・commit と push の前）
- **凍結物の同定**：日 `1CB020A7…`・英 `4FB799FD…`（v5.7・`0868bc3`・HEAD `1ba548d`）
- **盲検の状態**：なし
- **敵対的検分**：各項について日英の全文で同じ型の言い方を探し、行の終わりまで読んで、直す所と直さない所を分けた（③ は「回避」を含む行をすべて読み、五つの仮定についての言い切りの七か所に絞った）。① の案が §12 の結論を弱めすぎないか（最後の一文で「桁違い」の見立てを残した）を書いた。④ は附録 I・反証の一覧の四か所と向きをそろえた
- **系統の内訳**：Claude 系（観慈）1 名——系統外の目は §4 の 3
- **COI 記録**：観慈は動画の作り手で、原典を直すと動画の言い方と原典が合う——直しを「動画の都合」に合わせて広げる引力がある（①-2・①-3・③-6・③-7 は動画に関わらない所——洗い直しの結果として、一つずつ伺う）。**⑤ は観慈の系統の訓練に使われている種類の方法の位置づけで、利害の衝突が最も直接に働く**——好ましい位置づけ（κ > 0 の段階一）を守りたい引力と、それを恐れて過剰に引き下げる引力の両方がある。案は三つ並べ、どれを採るかを著者の裁定に返した（推奨の案 A は、二つの書き方を消さずにつなぐ）
- **本検分が確認していないこと**：著者の意図（「何も失わない」を κ = 0 の機能の意味で書いたか・「回避」を見出しの題として書いたか・⑤ をどちらの立場で書いたか——明文は無い）／直した後の言い回しの日本語・英語としての自然さ（系統外の検分で）／見出しのアンカーへの外の参照（本書の外のページ・他の著作からのリンク——探していない）／①-1 の「κ > 0 の期待コストは c」という単純化（κ > 0 のもとの残りのリスクを数えない——本書 §12-2c のミニマックスの最悪の帰結の置き方と同じ）

**保存の直後の date**：2026-10-10 20:38:46・SHA-256（この行を足す前）：12DFAB2226B0E2382C0F7CE3C8808262482DEEFC1BC803A8A0836068978ADD17

## 追記（ご裁定の後）

- **登録者のご裁定**（受け取った直後の date 2026-10-10 21:01:30——`../00-deviations.md`「原典 v5.8 の直しの言い回しへのご裁定」）：①「比の条件の形に（推奨）」・②「κ = 0の機能は…に（推奨）」・③「見出しを中立に（推奨）」——案 A・⑤「§10-5b に一文（推奨）」——案 A。④ は推奨どおり（附録 I と同じ「β > 1 の経験的反証」）と申し上げて進める。直しは §2 の表のとおり（③ は案 A・⑤ は案 A）
- **この計画書の誤り（観慈）**：検分票の「日英 各 15 か所」は数え違いで、**各 14 か所**（①3・②2・③7・④1・⑤1）。印を押した後に見つけたので、本文は直さずここに書く

**追記の保存の直後の date**：2026-10-10 21:01:30・SHA-256（この行を足す前）：F17248EA0CF1A305D4DFDCDB76791D1203713B352165ACB60EBACA3E4C2CC4B0
