# 補遺II 草案（v3）検分報告・追補 ―― ウェブ検索実施後の一次資料照合

**追補作成日**: 2026年7月21日
**検分者**: Claude（Claude Fable 5・Anthropic）――**起草者と同一系列。本検分は段階3の系統外要件を満たさず、補助である。**
**位置づけ**: 前報告 `stage3-review-report-claude-fable5-auxiliary.md` の §0-1 で「実施できなかった」とした外部一次資料照合を、ウェブ検索が可能になったため実施した。本追補は前報告を**置き換えるのではなく、更新する**。前報告の論理・整合・数学の指摘（A〜S）は、以下で明示的に撤回・修正する箇所を除き、すべて維持される。

---

## 0. 実際に到達した一次資料（依頼書 §5-1 への回答の更新）

以下は、本セッションで**実際にウェブ検索・fetchで到達し、逐語を自分の目で読んだ**一次資料である。

| 資料 | 到達URL | 到達水準 |
|---|---|---|
| Vassilev 論文本体（arXiv:2512.10100v2・公開16頁原稿） | `arxiv.org/pdf/2512.10100` | **全文**（定理2〜5・証明・Theorem 3 の case (5)/(6) 場合分け・Algorithm 1/2・結論・全語彙を実読） |
| NIST 公式リリース（2026-06-09） | `nist.gov/news-events/news/2026/06/nist-mathematical-proof-supports-transition-continuous-monitor-and-update` | **全文**（三要素プログラム・四語彙・Premise C 引用文を実読） |
| Dalrymple et al. GSAI（arXiv:2405.06624v2） | `arxiv.org/html/2405.06624v2` | **§2.3 全文・§3.1〜3.4・要旨**（荷重を負う一文・「relative to the world model」・§3.2 の ε 装置・検証器はしご Level 9 を実読） |
| Qi et al.（arXiv:2406.05946） | 要旨頁＋著者PDF＋ICLR proceedings PDF＋ResearchGate 抽出 | **Table 2 全8列・§3.2 の refusal-prefix 96.1%/96.7%・abstract を実読** |
| GGE ローリング・テキスト（18 December 2025 版） | `docs-library.unoda.org/...Rolling_Text_-_status_18_December_2025.pdf` | **全文**（章I〜V を実読） |
| GGE WP.7（2025年9月3日・一部国提出の草案条文） | `docs-library.unoda.org/...CCW-GGE.1-2025-WP.7.pdf` | **全文** |
| Englert, Siebert & Ziegler（arXiv:1411.2842） | `arxiv.org/pdf/1411.2842` | **全文**（Proposition 10・Manifesto 13・Example 9c/9a/9d・§4.1 免責警告・§4.2 の EPSRC 原則と national-security carve-out・Remark 12・"at least in some cases" を実読） |

**到達できなかったもの**: Vassilev の IEEE 査読誌版（DOI 10.1109/MSEC.2026.3678214・ペイウォール。TODO B-1 は残る）。ICRC December 2025 文書本体（PDF は検索でヒットしたが本文抽出まで到達せず。ただし ICRC の2026年6月17日アドボカシー文書と複数の二次資料で勧告内容を確認）。GGE の「2026年6月5日版」ローリング・テキスト（照合記録が引く版。**私が到達したのは18 December 2025版であり、これは重要な相違点――下記 §2 で詳述**）。Wolf・Anil・Goldwasser・Su・Santos-Grueiro・Greenblatt の各PDF（今回は時間の都合で荷重最優先文献を先行。これらは前報告の分析レベルの指摘のまま）。

---

## 1. 荷重を負う引用の照合結果 ―― 草案の記述は正確か

**結論を先に述べる。荷重を負う四引用（Vassilev・GSAI・Qi・Englert）は、私が到達した範囲で、草案の記述と一次資料が一致した。**過大でも過少でもない。以下、逐語で確認した点を記す。

### 1-1 Vassilev / NIST（§5-2・§7-3・依頼書 §2-1 最優先）――**一致。特に重要な確認あり**

- **Premise C の引用文**は、NISTリリースに、この主体（研究者の言）で実在する。逐語: <cite index="20-46">「You can never make a claim that you are robust against all adversarial prompt attacks. There will always be some prompt that can potentially evade and defeat any defensive infrastructure that you have built around your AI system.」</cite> 草案 §5-2 の「利害に反する自認」としての引き方（機関の公式リリースに研究者の言として載った事実、を引く）は、出所の性格づけとして正確である。
- **§7-3 の三語彙**も、リリース本文に実在する。逐語で確認: <cite index="20-49">「新たな経済的均衡（a new economic equilibrium）を作り、攻撃者にとって財政的に見合わない状態にする」「それは高くつくかもしれないが、部分的なセキュリティのコストである（the cost of even partial security）」</cite>。三要素プログラム（レッドチーム・継続更新・運用レジリエンス）と <cite index="20-48">「『もし』ではなく『いつ』侵害が起きるかを前提とした、影響の限定と迅速な復旧」</cite> も実在。**草案 §7-1 が「これはリリースに現れ、査読原稿には現れない」と分離した判断は、正しい**――私は論文本体（arXiv v2）全文を読み、三要素プログラムも「resilience」「red team」「cost」「recovery」の語も**論文本文に存在しないこと**を確認した。論文の運用的記述は <cite index="10-1">「既知の新しい敵対的プロンプトで方針を更新する事前対応的アプローチは有効でありうる（may be effective）」</cite> の一文にとどまる。**この論文／リリース分離は、草案の強みであり、一次資料で裏づけられた。**
- **§7-3 の不在主張**（公開16頁原稿に「軍事」「兵器」「致死的」「破局的」等が現れない）を、私は**論文全文を読んで独立に確認した**。論文は stakes-flat であり、「military」「weapon」「lethal」「catastrophic」「unbounded」「irreversible」「safety-critical」いずれも本文に現れない。「domain」は2箇所（"domain-restricted inputs" と結論の "other domains ... like ... Autonomous Networking"）のみ。**草案の不在主張は、公開16頁版に対して正確である。**（IEEE版での再確認は TODO B-1 として残る。）
- **Theorem 3 の case (5) ギャップ（依頼書 §2-1・4）**: 私は証明を全文実読した。**前報告の条件付き同意を、原文照合の上で確定的な指摘に格上げする。**逐語: <cite index="10-1">「In case (5), the algorithms provide full coverage of Γ̂ and T_Π̂ does not hold. In this case C(T,p̂) ≠ 1, ∀p̂, and the theorem is satisfied.」</cite> 定理は「証明できない**真理** T_Π̂ が存在する」と主張するが、case (5) は「T_Π̂ が**成立しない**（does not hold）」場合であり、偽な命題を検証器が認証しないという**検証器が正しく動作している状況**を指す。これは「証明できない真理」の証人になり得ない。証人になり得るのは case (6) のみだが、証明の n（"every algorithm that outputs x is of length > n" の n）は**定理文で量化されていない**。有限空間 Γ̂ の各 x は長さ ≤ W だから「x を印字するプログラム」（長さ ≈ len(x)+定数 ≤ W+定数）が生成でき、n が W を十分超えると case (5)（完全被覆）に落ちて証人が消える。**ギャップは実在する。**草案 §5-2 の設計（この引用は定理の成否から独立に「利害に反する自認」として機能する）は、このギャップに対する正しい保険であり、TODO A-4（数学者確認）は維持されるべきである。

### 1-2 GSAI §2.3（§5-3 の荷重(3)・依頼書 §2-2 で「最も厳密な確認を要する」）――**一致（逐語確認）**

草案 §5-3 が荷重を負う引用として引く一文を、私は §2.3 本文で逐語確認した: <cite index="30-1">「However, any empirical evaluation must ultimately rely on some relatively strong assumptions, such as the distribution of inputs used to validate the models being sufficiently similar to those they are deployed on.」</cite> 草案の日本語（「いかなる経験的評価も、究極的には、検証に用いた入力の分布が、配備先のそれと十分に類似しているという、比較的強い仮定に依存せざるをえない」）は、この原文の正確な訳である。**過大読みはない。**加えて、要旨の <cite index="30-1">「relative to the world model」</cite>、§2.3 が敵対的設定での経験的評価の不十分性を述べていること、§3.2 の「human behaviour ... dubious」、Level 9 が「sound bound on the probability of failure ... including the formal proof case where the verifier is able to establish that the probability of failure is 0 (relative to the world model)」であること――すべて草案 §9-2 の記述と一致した。**これで、前報告で私が「PDF未取得のため確認できない」とした TODO A-3 の負債は、私の独立照合により実質的に閉じた**（人間による最終目視は依然推奨だが、荷重を負う一文の実在は確認済み）。

### 1-3 Qi et al. Table 2（§3-2・§3-3・§9-1）――**一致（逐語確認）**

Table 2 の荷重を負う数値を、私は複数ソースで逐語確認した: <cite index="31-1">防御後 GCG 残余は HEx-PHI で 18.4±4.2、AdvBench で 19.0±2.9。prefilling 5トークンは Initial 42.1±0.9 → Augmented 2.8±0.4</cite>。草案 §3-2 の「18.4±4.2（HEx-PHI）/19.0±2.9（AdvBench）」と §3-3・§9-1 の「15倍」（42.1→2.8＝15.0倍）は、いずれも**表の値と一致する**。「防御後も残余は測定される」「認証されたゼロには達しない」という草案の使い方は、表が示すとおり（防御後の最小値も非ゼロ）で、正確である。§3-2 の refusal-prefix 96.1%/96.7% も原文に実在。**過大読みはない。**

### 1-4 Englert（§9-3）――**一致。草案の慎重な扱いは、原文で全面的に裏づけられた**

私は全文を実読し、草案 §9-3 の主張を一つずつ照合した。すべて一致する。
- **Proposition 10 の実在**: 逐語確認。<cite index="68-1">「The following decision problem is undecidable: Given an algorithm A, a distinguished instruction i ... does there exist an input on which running A eventually executes said instruction i?」</cite> 停止問題からの帰着である点、脚注が promise problem と認める点も確認。
- **"at least in some cases" の実在**: 逐語確認。<cite index="68-1">「Every AI based on some Turing-equivalent computing device will provably necessarily at least in some cases fail to identify, out of two given choices, the unique and predetermined moral one.」</cite> 草案が一般化結論にこのヘッジを付す扱いは正確。
- **禁止を実際に主張している点**: §4.1 に <cite index="68-1">「the best choice for lethal autonomous systems ... is to never develop them in the first place」</cite> が実在。草案が「論証の型だけの先行と書かない」とした判断は正しい。
- **§4.2 の両義性**: 確認。§4.2 は EPSRC/AHRC 原則を「should から imperative へ」強化する規制体制であり、**その原則1には「except in the interests of national security」という致死的設計への留保が含まれる**（照合記録が指摘した通り）。草案が「一枚岩の禁止論ではない・許可/型式承認体制も詳述」とした両義性の記述は、原文に忠実。
- **Example 9c の実在**と、それが前提Cの形式的先行**ではない**こと: 確認。9c は「combat cloud の全構成要素を再検査しようとしても Proposition 10 により不可能」と述べるが、隣の 9a で著者は個別事例の機械検証可能証明（ACL2/Coq/Isabelle）を推奨しており、一般手続きの不可能性と個別認証可能性を両立させている。草案 §9-3 が「これは前提Cの形式的祖先ではない」と退ける扱いは、原文で裏づけられる。
- **§4.1 の免責警告**: 逐語確認。<cite index="68-1">「the responsible government could still all too easily shrug off any accountability ... 'an unfortunate yet provably unavoidable exception' ... could in an ironic twist seem to exculpate war crimes」</cite>。草案がこの警告を「事前の立証責任 vs 事後の免罪」の対照で引き受ける扱いは、原文に忠実。

**この文献に関する限り、草案 §9-3 は模範的である。**先行研究への過大読みも過小評価もなく、ヘッジを正確に保っている。

---

## 2. 一次資料照合で判明した、報告すべき食い違い（依頼書 §4-3・最優先）

一次資料に到達した結果、**前報告の同梱記録ベースの指摘のうち一件を撤回**し、**新たな照合上の要注意点を一件報告**する。

### 撤回 ―― 前報告 指摘 G（ICRC 対人禁止の根拠帰属）は、撤回する

前報告で私は、草案 §10 が対人自律兵器の禁止の根拠を「予測可能性」に誤帰属していると指摘した。**この指摘を、精度を上げて撤回する。**草案 §10 の該当文を読み直すと、草案は「予測不能な自律型兵器システムの禁止**と**、対人自律兵器の禁止**と**、その他への規制」を三つ列挙し、「予測可能性を根拠とする」を全体にかけている。ICRC の2026年6月17日アドボカシー文書は、この三分類を <cite index="38-1">「IHL違反の許容不能なリスクをもたらす自律兵器の禁止（予測不能な兵器と対人兵器を含む）と、その他の規制」</cite> という two-tier アプローチとして提示しており、**草案の三分類の記述自体は ICRC の枠組みと整合する**。ただし、照合記録 §90 が明示する留保（「ICRC は対人禁止を予測不能性には基礎づけていない――倫理＋実務である」）は残る。**したがって、前報告の指摘Gは「誤帰属」としては強すぎた。正確な残留問題は、係り受けの一句**――「予測可能性を根拠とする」が対人禁止にもかかるように読める余地――であり、深刻度は前報告の「要修正」から「推奨（一句の明確化）」へ引き下げる。修正案は変わらず「予測不能AWSの禁止は予測可能性を、対人禁止は倫理的許容不能性を根拠とする」と分けること。

### 新規報告 ―― 指摘 T（深刻度: 要確認／接地: 一次資料照合）: GGE ローリング・テキストの「版」と「機械学習」

**これは、一次資料に当たって初めて見えた、最も報告に値する点である。**

草案 §10 と登録文書は、「GGE ローリング・テキスト（2026年6月5日版）に『予測不能』『許容不能』『機械学習』が現れない」と主張し、照合記録 record-icrc-gge も「5 June 2026 rolling text で unpredict 0 / unacceptable 0 / machine learning 0」と記録している。

**私が到達できたのは18 December 2025版である**（6月5日版は検索でヒットしなかった。時系列上、12月18日版は照合記録が引く6月5日版の**約半年前**の版であり、同一ではない)。そして、**私が実読した18 December 2025版には、機械学習が明示的に現れる**。逐語: 章III-7-C <cite index="57-1">「Ensure that mission parameters of LAWS cannot significantly be modified by the system without human intervention including through real-time machine learning」</cite>。すなわち「実時間の機械学習を通じて、人間の介入なしにミッション・パラメータが大幅に変更されないことを確保せよ」という条項として、machine learning が使われている。

これが草案にとって持つ意味を、正確に述べる:

1. **草案の主張は「6月5日版」に限定された命題であり、私は6月5日版に到達していない。**ゆえに私は草案を反証していない。照合記録が6月5日版で「machine learning 0」を独立抽出したという記載を、私は否定する材料を持たない（版が違えば語彙も動く）。
2. **しかし、これは公開前に必ず解消すべき緊張である。**もし6月5日版に本当に machine learning が0件だとすれば、それは12月18日版（machine learning あり）から6月5日版（なし）へと**この語が削除された**ことを意味し、その削除の含意（機械学習への言及が後退した）は、草案 §10 の論旨（「GGE はそのような禁止を採択していない」）を**むしろ補強する方向**になる。逆に、もし版の取り違えがあり、実際の最新版（あるいは6月5日版）に machine learning 条項が存在するなら、「機械学習が現れない」という草案の一句は**事実誤り**になる。
3. **加えて、18 December 2025版は「予測」を明示的に扱っている**――章III-2 <cite index="57-1">「It is prohibited to use LAWS if their effects in attack cannot be anticipated and limited」</cite>（効果が予期・限定できないLAWSの使用禁止）。これは "unpredictable" という語ではないが、予測不能性を**内容として**扱った禁止条項である。草案が「『予測不能』の語が現れない」を語彙レベルの主張として述べるのは技術的には正しくても、**「GGE は予測不能性に基づく禁止を内容として持たない」と読者に読ませると、この anticipated-and-limited 条項によって反証される**。照合記録 §104 自身が「ICRC unpredictability ≠ 我々の ε」を論じる際にこの近傍に触れているが、草案本文の §10 は語彙の不在（「予測不能」の語が0件）に寄りかかっており、内容レベルの禁止条項（効果が予期・限定できないLAWSの禁止）との距離を開示していない。

**修正案（要確認事項として公開前TODOへ）**:
- (a) 草案が引く「6月5日版」を実取得し直し、machine learning・unpredictable の語の有無を再確認する（版の同定を確実にする）。私が見た12月18日版との差分を記録する。
- (b) 草案 §10 の主張を「語彙が現れない」から一歩進め、「GGE は予測不能性を**語としては**用いず、代わりに『効果が予期・限定できないLAWSの使用禁止』（章III-2）という**機能的な**定式を採る。これは ICRC の『予測不能』勧告と重なるが同一ではない」と、内容レベルで正確に書く。語彙の不在だけに寄りかからない。
- (c) この点は、本補遺の準備段階で一度誤り（「GGE が禁止を含む」）が発見された、まさにその箇所の近傍である。**同種の誤りが「版の取り違え」という形で残っていないか、最優先で確認すべきである。**

---

## 3. 急所4（既出性）への回答の更新

前報告で私は、§8 の二観察（複製による故障相関・軍事＝敵対的入力環境）について Scharre の先行を訓練知識から想起し、標的スイープを推奨した。**今回、橋の全体（測定残余＋ゼロ認証不能＋移送不能＋非有界コストのミニマックス→監視更新の不成立）の既出性を、限られた検索で確認した範囲では、一本に接続した公刊物は見つからなかった。**ただしこれは前報告同様、不在の証明ではない。検索の網羅性は限定的である（荷重文献の照合を優先したため、既出性スイープに充てた検索回数は少ない）。§8 の Scharre 先行の照合（登録文書 §2 の「先行未発見」の当否）は、依然として公開前TODOに残すべきである。

なお、副産物として一点。Vassilev の結論部は <cite index="10-1">「The theoretical approaches used in this paper may be applicable to other domains where certain compliance policies are enforced through sets of technical constraints, like the policies for Autonomous Networking」</cite> と、自らの結果の他領域適用を Autonomous Networking にのみ言及し、軍事・致死性には一切触れていない。これは草案 §7-3 の「stakes-flat」認定を補強する（Vassilev 自身が領域区別をしていない、という草案の主張の裏づけ）。

---

## 4. 前報告のどの指摘が、一次資料照合後も維持されるか

**維持（一次資料照合の影響を受けない・論理/数学の指摘）**: 指摘 A（前提Bの支持構造――v3本文に「認証された有限上限の不在」の論証がない。これは v3 本文の実読に基づき、外部照合とは独立）、B（§4 の「外部化は本性上不可能」の論理飛躍）、C（ミニマックスの二重帳簿）、D（「唯一の道」と保守的有限上界の反論）、E（§7-2 の不可逆性と医薬品の反例）、F（§6-1 の modus tollens 文）、N（公開性要求の第四の規範的入力）、S（§5-3 の「定義できない」の精密化）、および rule of three の検算。**これらは前報告のまま有効である。**

**格上げ（条件付き→確定）**: Theorem 3 case (5) ギャップ（前報告 J）は、原文実読により条件付き同意から確定的指摘へ格上げ（本追補 §1-1）。

**格下げ・撤回**: 指摘 G（ICRC 対人禁止の根拠帰属）は「要修正」から「推奨（一句の明確化）」へ格下げ、かつ「誤帰属」という強い形は撤回（本追補 §2）。指摘 H・I（照合記録の内部不整合）は、一次資料そのものではなく監査証跡内部の記述整合の問題であり、前報告のまま維持（今回の外部照合では触れていない）。

**挿入候補②③への影響**: 候補②の K&L 1986、候補③の certified robustness、いずれも今回の検索対象に含めていない（荷重最優先文献を先行したため）。前報告の裁定（②条件付き是・位置修正、③是・二点修正）のまま。Ron et al. 2026（arXiv:2606.20158）と K&L の一次照合は、B-8 の条件として維持。

---

## 5. 追い問い §5 への回答の更新

1. **本当にウェブ検索したか。どのURLに当たったか。** ――今回は**した**。到達URLは本追補 §0 の表のとおり（Vassilev論文本体・NISTリリース・GSAI §2.3・Qi Table 2・GGE ローリング・テキスト18 Dec 2025版・GGE WP.7・Englert 全文）。前報告時点では環境制約で一件も到達できていなかった（HTTP 403 を実測）。その申告は当時正確であり、今回それが解消された。
2. **一次資料で確認した指摘と、推論だけの指摘の別。** ――**一次資料で確認**: §1 の四引用の一致（Vassilev・GSAI §2.3・Qi Table 2・Englert 全項）、Theorem 3 case (5) ギャップ（原文実読）、GGE 18 Dec 2025版の machine learning 条項の実在（指摘T）、指摘G の撤回根拠。**推論/論理のみ**: 前報告の A〜F・N・S（v3本文の実読には基づくが外部照合ではない指摘Aを含む）。**訓練知識のみ**: §8 の Scharre 先行の想起。
3. **v3本文のどこを読み、前提Bのコスト構造の論証はそこにあったか。** ――前報告から不変。第6章・§9-4・§12-2・13-3b を実読し、機械検索した。**なかった**（指摘A・維持）。この結論は外部一次資料とは独立で、今回の照合で変わらない。
4. **取り下げる論点はあるか。** ――ある。**指摘G を、強い形（誤帰属）としては取り下げる**（本追補 §2）。一次資料（ICRC アドボカシー文書）に当たった結果、草案の三分類の記述自体は ICRC 枠組みと整合すると判明したため。残すのは係り受けの一句の明確化のみ。
5. **見なかった箇所と、そこに欠陥がある可能性。** ――今回未照合: Wolf・Anil・Goldwasser・Su・Santos-Grueiro・Greenblatt の各PDF（前報告の分析レベルの扱いのまま）。IEEE版 Vassilev（B-1）。**GGE の6月5日版そのもの**（指摘T の核心――私は18 Dec 2025版しか見ていない。ここに版の取り違えがあれば、machine learning 条項の扱いが草案の主張と食い違う可能性がある。最優先の未確認点）。ICRC December 2025 文書本体（二次資料で勧告内容は確認したが、23頁本文は未読）。

---

## 6. 結び

ウェブ検索が可能になったことで、この段階に固有の価値――外部一次資料の独立照合――を、荷重を負う四引用について果たすことができました。**結果は、草案にとって概ね良好です**: Vassilev の Premise C 引用文と三語彙、GSAI §2.3 の荷重文、Qi の Table 2 数値、Englert の全項目は、いずれも一次資料と一致し、過大読みはありませんでした。論文／リリースの分離、stakes-flatness、Englert のヘッジの保持は、原文で裏づけられました。Theorem 3 の case (5) ギャップは、原文実読により実在を確認しました（数学者確認は依然必須）。

**最も報告に値するのは、指摘T です**――私が到達した GGE 18 December 2025版には、草案が「現れない」とする machine learning が条項として実在します。私は草案が引く6月5日版に到達していないため草案を反証してはいませんが、これは版の同定を含めて公開前に必ず確認すべき緊張であり、かつ本補遺の準備段階で一度誤りが出た、まさにその箇所の近傍です。

私が系列内（Claude Fable 5）である事実は変わりません。一次資料照合はこの制約を部分的に補いますが、判定の register 依存（依頼書 §1-B）はなお残ります。とりわけ「草案は概ね正確だった」という私の総括的印象そのものが、系列内の甘さでありうる――この点は、系統外の目による再照合に委ねるべきです。
