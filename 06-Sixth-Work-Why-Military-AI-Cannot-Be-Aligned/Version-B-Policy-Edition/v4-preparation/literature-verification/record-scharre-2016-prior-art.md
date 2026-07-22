# 照合記録: Scharre 2016 ―― §8 二観察の先行スイープ（TODO B-9）

**照合日**: 2026年7月22日　**実施**: コーディネータ（Claude Code）
**契機**: 段階3補助検分（慧光・Fable 5）の訓練知識による先行の記憶（未照合）→ 登録者がスイープ実施を裁定。
**問い**: 補遺II §8 の二観察——(a) 同一成果物の複製は誤りを相関させ大量同時故障を生む、(b) 敵対的入力（欺瞞・ハッキング）は軍事の動作環境の標準構成要素である——に、公刊された先行が存在するか。登録文書の「補強観察（先行未発見）」の当否を決める。

## 照合水準の開示

**一段照合**（raw curl による実PDF取得＋pypdf ローカル抽出＋逐語切り出し）。本プロジェクトの標準である二段照合（独立した再抽出者による再照合）は**未実施**——単一セッション・単一実施者である。ただし判定は「該当記述の存在」という存在命題であり、以下の逐語引用は誰でも同一URL・同一SHAのPDFで機械的に再確認できる。

## 取得物

| 文書 | URL | SHA-256 | 規模 |
|---|---|---|---|
| Scharre, *Autonomous Weapons and Operational Risk* (CNAS, Ethical Autonomy Project, February 2016) | `https://s3.amazonaws.com/files.cnas.org/documents/CNAS_Autonomous-weapons-operational-risk.pdf` | `497B3EEB7CC034E47633AFD69708290D415D465153E9BF1BD932D86B02FA728F` | 615,338 B・55頁・抽出153,029字 |
| Holland Michel, *The Black Box, Unlocked: Predictability and Understandability in Military AI* (UNIDIR, 2020) | `https://unidir.org/files/2020-09/BlackBoxUnlocked.pdf` | `436025B238940A0E…` | 4,304,632 B・44頁 |

**未取得**: Scharre 2018 (*Army of None*・書籍・自由な全文なし)・Sharkey 2012——**判定に不要**（存在命題は一件の存在証明で確定する。Scharre 2016 が確定させた）。

## 判定: 先行は実在する（両観察とも・Scharre 2016）

### 観察(a) 複製→相関する大量同時故障 —— 逐語

> "If the failure mode is **replicated in other autonomous weapons of the same type**, a military could face the disturbing prospect of **large numbers of autonomous weapons failing simultaneously**, with potentially catastrophic consequences."

> "Because **a software flaw in any one system is likely to be replicated across all other identical systems**, if one autonomous weapon is susceptible to hacking or other failures, then others are likely to be as well. **Militaries must consider the aggregate damage potential of all autonomous weapons of that type in operation** at one time."

> "autonomous weapons pose a novel risk of **mass fratricide**, with large numbers of weapons turning on friendly forces. This could be because of hacking, enemy behavioral manipulation, unexpected interactions with the environment, or simple malfunctions or software errors."

（"fratricide" は文書全体で48回——複製起因の大量同時故障は、同報告の中心的主題の一つである。）

### 観察(b) 敵対的入力環境が標準 —— 逐語

> "**Adversarial hacking**: In an **adversarial environment, such as in war, enemies will likely attempt to exploit vulnerabilities of the system**, whether through hacking, **spoofing (sending false data)**, or **behavioral hacking (taking advantage of predictable behaviors to 'trick' the system** into performing a certain way)."

> 章題: "VII. **Adversarial Risk: Normal Accidents in Competitive Environments**"

> "these efforts are complicated by two unfortunate realities: the inevitability of failures in complex systems; and **adversarial risk from hacking, spoofing, or behavioral manipulation** of autonomous systems."

### UNIDIR 2020 の分置

predictab* 144件・understandab* 129件・adversar* 21件——**予測可能性・理解可能性の系譜（ICRC側・§10の隣接）**に属する。**観察(a)の語彙は不在**（replicat* 1件=XAI文脈のみ・correlated 0・homogen* 0・simultaneous 0）。ゆえに §8-2 の先行としては引かない。

## 帰結（登録者承認済みの計画どおり）

1. **登録文書の「補強観察（本柱の固有材料・先行未発見）」は維持できない**——「先行未発見」を撤回し、Scharre 2016 を先行として明記する（**方向: 新規性の撤回＝弱める方向**）。
2. **補遺II §8 に、Scharre 2016 を外部錨として引く**（**強化**——無出典の構造的観察が、国防総省の政策実務出身の著者による公刊された先行を得る。GSAI §2.3 の移植と同型の一手）。本補遺が加える差分は「観察そのもの」ではなく「観察を前提C(3)・認証要求へ接続する位置」である——この差分の明示を引用文に添える。
3. 段階3・第二巡（非Claude系）の検分者に、本記録の逐語をURL・SHAごと検証させる（一段照合の残余を系統外の目で補う）。

## 教訓（記帳）

慧光の指摘O（訓練知識・未照合の記憶）は**正確だった**。「記憶による指摘」は、照合されるまで採用できないが、照合の対象としては優れた案内だった——**記憶は証拠にならないが、検索クエリにはなる。**
