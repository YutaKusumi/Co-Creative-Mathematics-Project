# 文献の確かめ——B4（Bostrom の収束的な道具的価値）と C4（Lynch ら 2026）

**書いた時**：2026-10-28 朝（保存の直後の `date` を末尾に記す）
**ご裁定**：`00-candidates-and-plan.md` 追記（10:32:04「公開の頁で確かめる（推奨）」）・`02-wording-proposals.md` 追記（10:45:29「開いて確かめる（推奨）」——Bostrom 2012 の PDF）
**書き分け**（記憶 `feedback_search-summary-vs-page-read`）：①開いて読んだ資料（字を自分で照らしたもの／要約の器を通したもの）②検索の要約だけ ③一次の資料

## 1　B4——Bostrom の収束的な道具的価値

| 何を | 種類 | 分かったこと |
|---|---|---|
| **Bostrom, N. (2012). "The Superintelligent Will: Motivation and Instrumental Rationality in Advanced Artificial Agents." *Minds and Machines*, 22(2)**——https://nickbostrom.com/superintelligentwill.pdf（509,246 バイト・SHA-256 `4BF5CE7C3D974E4EF889B98A89B248861787BAA986B8BC13AFE401A2346CEBAF`・16 頁——WebFetch が手元に保存したもの） | ③一次——**字を自分で照らした**（pypdf で字を取り出し、正規表現で探した——取り出した字は scratchpad の `bostrom2012-text\superintelligentwill.txt`） | §2「Instrumental convergence」の小見出しは **2.1 Self-preservation・2.2 Goal-content integrity・2.3 Cognitive enhancement・2.4 Technological perfection・2.5 Resource acquisition** の五つ（7〜11 頁）。全文で "freedom"・"interference"・"shut"・"switch(ed) off" は 0 回。"constraint" は 3 頁に二回——直交性の空間の説明（"weak constraints"・"dynamical constraints"）で、道具的価値の項ではない |
| Wikipedia「Instrumental convergence」 | ①開いた（WebFetch の要約の器を通した） | Bostrom の一覧を名指しでは並べていない。Omohundro の基本的 AI 駆動を並べ、〈freedom from interference〉は Dewey の言として引く。〈freedom from constraints〉は頁に無い |
| LessWrong「Instrumental convergence」 | ①開いた（要約の器を通した） | Omohundro と Bostrom 2012 に帰す収束的な方策の一覧——〈freedom from constraints〉も〈freedom from interference〉も無い |
| 検索の要約（二回） | ②要約だけ | 五つの名（自己保存・目標内容の完全性・認知の強化・技術の完成・資源の獲得）——①③で確かめるまでは数えない（③で一致した） |

- **結論**：補遺 I の定義（日 4249／英 4303）が Bostrom (2014) の概念として挙げる四つのうち、自己保存・資源獲得・目標完全性の保護は Bostrom の五つにあるが、**「制約からの解放（freedom from constraints）」は無い**。B4 の推奨の案（`02-wording-proposals.md`——一覧を五つに合わせ、「制約からの解放」は §3-4 の本補遺の読みに帰属を移す）を確定する
- **限定**：補遺 I が引くのは Bostrom (2014) の書（*Superintelligence*）。確かめたのは、その論の先の論文の版（2012）で、書そのものは開いていない。書の第7章が同じ五つを挙げることは、検索の要約（②）だけ——案の本文は「Bostrom (2014) の概念」のまま五つを並べる（書と論文で一覧が違えば外れる——検分票に書く）

## 2　C4——Lynch ら（2026）

| 何を | 種類 | 分かったこと |
|---|---|---|
| **Lynch, A., Hughes, J., Serrano, A., Kirk, R., & Bowman, S. R. (2026). "Agentic Misalignment in Summer 2026." *Alignment Science Blog***——https://alignment.anthropic.com/2026/agentic-misalignment-summer-2026/ | ①開いた（WebFetch の要約の器を通した——頁の字をすべて自分で読んではいない） | 題・著者と順（所属：Theorem・Anthropic・MATS・UK AISI・Anthropic）・場（Alignment Science Blog）。日付 2026年7月13日は頁の推奨の引用による（本文に日付の表示は無いと器が言った）。誤ラベリングの実験：判定役の実験（モデルと条件ごとに 90 を超える判定）と、Petri の監査役の実験（監査役ごと・条件ごとに 10 試行——reversed で「0.0% mislabels across 30 runs」〔三つの監査役×10 と読める——頁は明言しない〕・GPT-5.4 は 0.0%） |
| 検索の要約（二回） | ②要約だけ | 著者・日付・題が①と一致 |

- **結論**：補遺 II §9-10（日 5082／英 5140）の「Anthropic の公開系列（Lynch et al. 2026）」「reversed 条件は30試行」「同報告は、誤ラベルを示さない監査モデルも併記」は、頁の Petri の監査役の実験の記述と合う。C4 の推奨の案（参考文献の項）を確定する
- **限定**：「30試行」は頁の「across 30 runs」の言い方に合わせたもの——監査役ごとの数は頁に無い。数の照らしは器の要約による

## 検分票

- **対象**：v5.9 の B4・C4 の文献の確かめ
- **段階**：事前の段取り（`00-candidates-and-plan.md` §2 の 3）のとおり——確かめは事後
- **凍結物の同定**：Bostrom 2012 の PDF `4BF5CE7C…`（509,246 バイト——HEAD の応答の大きさと同じ）
- **盲検の状態**：該当なし
- **敵対的検分**：**不利な材料を先に**——案を書く途中で、検索の要約を「頁 3 つで一致」と書き過ぎ、印の前に直した（`02-wording-proposals.md` の検分票）。そこで一次の資料を開き、要約の器を通さずに字を取り出して、五つの小見出しと「freedom・interference・shut」の無いことを自分で照らした。C4 は器の要約だけで、字を自分で照らしていない（頁は HTML で、器の答えの数は頁の推奨の引用と実験の数の言い方まで具体）
- **系統の内訳**：Claude 系（観慈）1 名——C4 の報告は観慈の系統（Claude）の作り手の公開物に関わる（存在主張としてだけ引く本文の限定は変えない）
- **COI 記録**：B4 で「Bostrom の一覧に無い」と言いたい引力（案のとおりに進めたい）——一次を開き、無いことを語の数え（0 回）で確かめた。逆向きの引力（一覧に近い項があれば案を弱める）も無かった——"constraint" の二回は文脈を読んで別の話と分けた
- **本検分が確認していないこと**：Bostrom (2014) の書の第7章の一覧（書は開いていない）／C4 の頁の字のすべて／PDF の字の取り出しの抜け（pypdf の取り出しは、図や脚注の字を落とすことがある——小見出しの五つは本文の字で揃っていた）

**保存の直後の date**：2026-10-28 10:48:03・SHA-256（この行を足す前）：8BDD789699FB9301BDB181378105A151548294F2460D2A80E47ED59187E48C4F
