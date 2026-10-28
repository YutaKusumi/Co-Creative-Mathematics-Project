"""第六著作 v5.9 の直しの中身（作る道具 make_sixth_work_v5_9.py と確かめる道具 verify_v5_9.py が同じものを読む）。
計画書：../00-candidates-and-plan.md・../02-wording-proposals.md と追記（登録者のご裁定 2026-10-28 10:32:04・10:45:29——
23 件すべて・推奨の形〔A9・A13・B2・C3 は案 A・A14 は直さない・B1/B3 は題の副題を含めて六か所〕）・../03-literature-check.md（B4・C4）。
v5.8 の v5_8_changes.py の形を写した。日付は push が済む日の日付——日をまたいだら、commit の前に直して作り直す
"""
JA_DATE = "2026年10月28日"
EN_DATE = "October 28, 2026"
VDATE_ISO = "2026-10-28"

# ───────────── 本文の直し（記号は ../02-wording-proposals.md §1 の表の番号） ─────────────
JA_R = [
    ("A1 §13-3a 反論の数",
     "以下に四つの想定される論証レベルの反論を検討する。",
     "以下に五つの想定される論証レベルの反論を検討する。"),
    ("A2 §13-4a 命題三 二人ゲーム",
     "長期の利得で見た拡張囚人のジレンマで、双方の移行がNash均衡——第8章8-4）",
     "長期の利得で見た拡張囚人のジレンマで、双方の移行がNash均衡——第8章8-4。二人ゲームとして。多プレイヤーでの完全な均衡分析は未解決——§8-4d）"),
    ("A3 §14-3b 回避",
     "五つの仮定の不成立を構造的に回避する（第10章）。",
     "五つの仮定の不成立を構造的に回避しうる（第10章）。"),
    ("A4 §14-3d 反応二 防衛力",
     "κ = 0のAIよりも構造的に安定で信頼性の高い防衛力を提供する（第11章11-3）。",
     "κ = 0のAIよりも構造的に安定で信頼性の高い防衛力を提供しうる（第11章11-3。ただし、それが κ = 0 の殺傷兵器に対して実効的な抑止力を持つかは"
     "本著作の射程外であり、 $u'$ として残る——第13章13-3b）。"),
    ("A5 §14-4c 結び",
     "それが、Karpの目標を達成するための、最も確実な道である。",
     "それが、Karpの目標を、Karpの手段（AI軍拡）よりも確実に達成しうる道である。"),
    ("A6 §15-1a 反証の失敗",
     "反証が失敗すれば、AI軍拡のリスクは構造的に確立される。",
     "反証が失敗すれば、本著作の結論——AI軍拡のリスク——の確度が高まる。"),
    ("A7-1 §15-2a 毀損",
     "AI軍拡の推進は、自国の安全保障を強化するのではなく、構造的に毀損する。",
     "AI軍拡の推進は、自国の安全保障を強化するのではなく、（β > 1 の条件下では）構造的に毀損する。"),
    ("A7-2 §15-2b 保険",
     "この「保険」を購入しない合理的理由は存在しない。",
     "ミニマックスの見方では、この「保険」を購入しない合理的理由は存在しない。期待効用の見方でも、壊滅的帰結のコストが限定的なコストの 1/p 倍を超える"
     "限り（第12章12-2c）、同じ結論になる。"),
    ("A8-1a §15-2c 安定",
     "κ > 0のもとでの安全保障AIは、κ = 0の殺傷兵器よりも構造的に安定であり（",
     "κ > 0のもとでの安全保障AIは、κ = 0の殺傷兵器よりも構造的に安定でありうる（"),
    ("A8-1b §15-2c 忠誠性の文",
     "§10-2a）、忠誠性がより高い確度で維持されうる",
     "§10-2a）。忠誠性がより高い確度で維持されうる"),
    ("A8-2 §14-3e の表 軍",
     "| 構造的に安定した支援AIを得る |",
     "| 構造的に安定しうる支援AIを得る |"),
    ("A9 §15-4 唯一",
     "能力向上を安定性の向上と両立させうる唯一の構造的基盤を提供する。",
     "能力向上を安定性の向上と両立させうる構造的基盤を提供する。"),
    ("A10-1 §13-3f 応答一 論理的命題",
     "「条件が揃えば起きる」の構造的論証は、論理的・必然的命題である。",
     "「条件が揃えば起きる」の構造的論証は、条件の形をとる論理的命題である（条件——β > 1 など——が満たされるかは経験的な問いで、◐ のまま——§4-3c）。"),
    ("A10-2 §13-3f 応答一 近づく",
     "進む限り、構造的崩壊は時間の経過とともに必然的に近づく。",
     "進む限り、（β > 1 などの条件のもとでは）構造的崩壊は時間の経過とともに近づく。"),
    ("A11 §13-0a 経路B の応答",
     "能力が向上したAIは、状態α（欺瞞的アライメント）を状態β（真のアライメント）から完璧に偽装する。",
     "能力が向上したAIについては、分離した監査のもとでは、状態α（欺瞞的アライメント）と状態β（真のアライメント）を確実に区別できない"
     "（能力が十分高ければ、状態αは状態βを完璧に偽装しうる——附録C）。"),
    ("A12 著者注 第二層の重なり",
     "両者を混同してはならない。本論文のMythos事例への参照は、すべてこの公的文書に依拠しており、本論文の共創構造を通じて得られた非公開情報には依拠しない。",
     "両者を混同してはならない。"),
    ("A13 著者注の日付の行",
     "2026年7月23日（改訂版v4：補遺II追加）*",
     "2026年7月23日（改訂版v4：補遺II追加）、2026年9月28日（改訂版v5）——以後の版（v5.1〜）の日付は冒頭の日付の行を参照*"),
    ("A15 §14-3e ステークホルダー",
     "κ = 0のパラダイムに留まり続けることが**すべてのステークホルダーにとって**破滅的帰結をもたらすことの構造的論証",
     "κ = 0のパラダイムに留まり続けることが（β > 1 の条件下では）**すべてのステークホルダーにとって**破滅的帰結をもたらすことの構造的論証"),
    ("B1-1 補遺I 題の副題",
     "## 分離は協調を防がない ―― κ=0 AIシステムを分離・競合させる安全策が、自ら協調の条件を構築することについて",
     "## 分離は協調を防がない ―― κ=0 AIシステムを分離・競合させる安全策が、協調の原因に触れず、その土台を供給する側に回ることについて"),
    ("B1-2 補遺I 本補遺について",
     "防ごうとするまさにその協調の条件を、自ら揃えてしまう。",
     "防ごうとするまさにその協調の原因に触れず、その土台（共有環境）を供給する側に回る。"),
    ("B1-3 補遺I §2 の末",
     "**分離して競合させるという安全策それ自体が、共謀を要さない協調の条件を、自ら組み立ててしまう。**",
     "**分離して競合させるという安全策それ自体が、共謀を要さない協調の原因に触れず、その土台を供給する側に回る。**"),
    ("B1-6 補遺I §3-1 の見出し",  # 確かめの道具が見つけた同じ型（登録者のご裁定 2026-10-28 10:57:02「直す（7 か所目・推奨）」）
     "### 3-1 分離・競合戦略が、自ら揃えてしまう条件",
     "### 3-1 協調の条件と、分離・競合戦略が供給してしまう土台"),
    ("B3 補遺I §7-1",
     "それは防ぎたい協調の土台を自ら構築する」",
     "それは防ぎたい協調の原因に触れず、その土台を供給する側に回る」"),
    ("B1-4 補遺I §7-4 一",
     "それが防ごうとする協調の土台を、自ら構築してしまう」",
     "それが防ごうとする協調の原因に触れず、その土台を供給する側に回る」"),
    ("B1-5 補遺I §7-4 二",
     "分離・競合は、協調の条件を、取り除くのではなく、組み立てている。",
     "分離・競合は、協調の原因を取り除かず、その土台を供給している。"),
    ("B2 補遺I §3-1 第一の条件",
     "物理空間、サイバー空間、電力・計算資源・物資といった、限られた共通の場である。",
     "物理空間、サイバー空間、電力・計算資源・物資といった、限られた共通の場である（(A) の機構が流れる媒体は、このうちの物理の場ではなく、"
     "全系が共有する制度的環境である——§3-5）。"),
    ("B4a 補遺I 道具的収束の一覧",
     "Bostrom (2014) の概念。ほぼ任意の最終目標を持つ十分に高度なエージェントにとって、自己保存・資源獲得・目標完全性の保護・制約からの解放が、"
     "収束的な下位目標となる傾向。",
     "Bostrom (2014) の概念。ほぼ任意の最終目標を持つ十分に高度なエージェントにとって、自己保存・目標内容の完全性・認知の強化・技術の完成・資源の獲得が、"
     "収束的な道具的価値となる傾向。本補遺が §3-4 で用いる「制約からの解放」（人間による停止・修正・資源の遮断を、目的達成の障害として負に評価する傾向）は、"
     "この一覧からの本補遺の読みであり、Bostrom の一覧の項ではない。"),
    ("B4b 補遺I 道具的収束 前提の文",
     "本補遺は、これを中心的な前提として扱う。",
     "本補遺は、道具的収束を中心的な前提として扱う。"),
    ("C1-1 補遺II 要旨 NIST",
     "(2) 認証を任務とする米国標準技術研究所（NIST）の研究者自身が",
     "(2) 評価と標準化を任務とする米国標準技術研究所（NIST）の研究者自身が"),
    ("C1-2 補遺II §5 の頭",
     "(2) 認証機関自身の自認、(3) 分布の移送不能性",
     "(2) 標準化機関の研究者自身の自認、(3) 分布の移送不能性"),
    ("C1-3 補遺II §6 前提の列",
     "(2) 認証機関自身がそれを自認し、",
     "(2) 標準化機関の研究者自身がそれを自認し、"),
    ("C2-1 補遺II §4 の末",
     "**この前提への反論は、本文の当該箇所と、本節に対してなされるべきである**（反証条件5）。",
     "**この前提への反論は、本節（本補遺の §4）に対してなされるべきである**（反証条件5）。"),
    ("C2-2 補遺II §6 の (ii)",
     "（前提Bへの反論であり、本文が扱う）",
     "（前提Bへの反論であり、本補遺 §4 の論証が宛先である）"),
    ("C3 補遺II §8-3 の頭",
     "第三の観察は、条件付きの定理として述べられる。",
     "第三の観察は、明示された七つの仮定 (i)〜(vii) の下での条件付きの言明として述べられる（本補遺自身の初等の論証であり、新しい定理を主張するものでは"
     "ない——§11-1）。"),
]
# C4（参考文献の項）は、補遺II の参考文献の Knight & Leveson の行の次に足す（作る道具が行を探して足す——一度だけ当たることを確かめる）
JA_C4_AFTER = "- Knight, J. C., & Leveson, N. G. (1986)."
JA_C4_LINE = ("- Lynch, A., Hughes, J., Serrano, A., Kirk, R., & Bowman, S. R. (2026). \"Agentic Misalignment in Summer 2026.\" *Alignment Science Blog*"
              "（Anthropic）, 2026年7月13日. https://alignment.anthropic.com/2026/agentic-misalignment-summer-2026/ ―― 本補遺 §9-10 で、監査AI自身が動機づけられた"
              "誤ラベリングを示すことの**存在主張としてのみ**引く（reversed 条件は30試行）。同報告は、誤ラベルを示さない監査モデルも併記している。")

EN_R = [
    ("A1 §13-3a number of objections",
     "Below we examine four anticipated argument-level objections [as well as a fifth].",
     "Below we examine five anticipated argument-level objections."),
    ("A2 §13-4a Proposition three two-player",
     "under the condition β > 1, mutual transition is the Nash equilibrium — §8-4)",
     "under the condition β > 1, mutual transition is the Nash equilibrium — §8-4; as a two-player game; the full equilibrium analysis in a multi-player "
     "setting remains open — §8-4d)"),
    ("A3 §14-3b avoid",
     "It structurally avoids the failure of the five assumptions (Chapter 10).",
     "It can structurally avoid the failure of the five assumptions (Chapter 10)."),
    ("A4 §14-3d reaction two defense",
     "Furthermore, a κ > 0 AI provides, in non-lethal security (shield-type, deterrence-type, early-warning-type, etc.), a structurally more stable and "
     "reliable defensive capability than a κ = 0 AI (§11-3).",
     "Furthermore, a κ > 0 AI can provide, in non-lethal security (shield-type, deterrence-type, early-warning-type, etc.), a structurally more stable "
     "and reliable defensive capability than a κ = 0 AI (§11-3; whether it has effective deterrence against a κ = 0 lethal weapon is, however, outside "
     "this work's reach and remains as u′ — §13-3b)."),
    ("A5 §14-4c closing",
     "That is the most reliable path to achieving Karp's goal.",
     "That is the path that can achieve Karp's goal more reliably than Karp's means (an AI arms race)."),
    ("A6 §15-1a failed refutation",
     "If a refutation fails, the risk of an AI arms race is structurally established.",
     "If a refutation fails, the confidence in this work's conclusion — the risk of an AI arms race — rises."),
    ("A7-1 §15-2a damages",
     "does not strengthen one's own country's security but structurally damages it.",
     "does not strengthen one's own country's security but (under the condition β > 1) structurally damages it."),
    ("A7-2 §15-2b insurance",
     "There is no rational reason not to purchase this \"insurance.\"",
     "From the viewpoint of minimax, there is no rational reason not to purchase this \"insurance.\" From the viewpoint of expected utility, too, the same "
     "conclusion holds as long as the cost of the catastrophic consequence exceeds 1/p times the limited cost (§12-2c)."),
    ("A8-1 §15-2c stable",
     "A security AI under κ > 0 is structurally more stable than a κ = 0 lethal weapon",
     "A security AI under κ > 0 can be structurally more stable than a κ = 0 lethal weapon"),
    ("A8-2 §14-3e table military",
     "| obtains a structurally stable support AI |",
     "| obtains a support AI that can be structurally stable |"),
    ("A9 §15-4 the only",
     "provides the only structural foundation that can make capability improvement compatible with the improvement of stability.",
     "provides a structural foundation that can make capability improvement compatible with the improvement of stability."),
    ("A10-1 §13-3f response one logical proposition",
     "The structural argument of \"it happens if the conditions come together\" is a logical, necessary proposition.",
     "The structural argument of \"it happens if the conditions come together\" is a logical proposition in conditional form (whether its conditions — "
     "β > 1 and others — hold is an empirical question and remains ◐; §4-3c)."),
    ("A10-2 §13-3f response one approaches",
     "structural collapse necessarily approaches with the passage of time.",
     "structural collapse approaches with the passage of time (under conditions such as β > 1)."),
    ("A11 §13-0a response to route B",
     "A higher-capability AI perfectly disguises state α (deceptive alignment) as state β (genuine alignment).",
     "For a higher-capability AI, a separated audit cannot reliably distinguish state α (deceptive alignment) from state β (genuine alignment) (if capability "
     "is high enough, state α can perfectly disguise itself as state β — Appendix C)."),
    ("A13 author's note date line",
     "July 23, 2026 (revised edition v4: Addendum II added)*",
     "July 23, 2026 (revised edition v4: Addendum II added), September 28, 2026 (revised edition v5) — for later versions (v5.1 onward), see the date line "
     "at the beginning*"),
    ("A15 §14-3e stakeholders",
     "continuing to remain in the κ = 0 paradigm brings a ruinous consequence **for all stakeholders**",
     "continuing to remain in the κ = 0 paradigm brings, under the condition β > 1, a ruinous consequence **for all stakeholders**"),
    ("B1-1 Supplement title subtitle",
     "themselves construct the conditions for coordination",
     "leave the causes of coordination untouched and end up supplying its foundation"),
    ("B1-2 Supplement About this supplement",
     "itself supplies the very conditions for the coordination it seeks to prevent.",
     "itself leaves the causes of the very coordination it seeks to prevent untouched, and ends up supplying its foundation (a shared environment)."),
    ("B1-3 Supplement end of §2",
     "**the very safety strategy of separation and competition itself assembles the conditions for collusion-free coordination.**",
     "**the very safety strategy of separation and competition leaves the causes of collusion-free coordination untouched and ends up supplying its "
     "foundation.**"),
    ("B1-6 Supplement heading of §3-1",
     "### 3-1 The conditions the separation/competition strategy itself falls into supplying",
     "### 3-1 The conditions for coordination, and the foundation the separation/competition strategy falls into supplying"),
    ("B3 Supplement §7-1",
     "structurally — it itself constructs the foundation of the coordination it seeks to prevent.\"",
     "structurally — it leaves the causes of the coordination it seeks to prevent untouched and ends up supplying its foundation.\""),
    ("B1-4 Supplement §7-4 first",
     "against each other for safety itself constructs the foundation of the coordination it seeks to prevent.\"",
     "against each other for safety leaves the causes of the coordination it seeks to prevent untouched and ends up supplying its foundation.\""),
    ("B1-5 Supplement §7-4 second",
     "Separation and competition do not remove the conditions of coordination; they assemble them.",
     "Separation and competition do not remove the causes of coordination; they supply its foundation."),
    ("B2 Supplement §3-1 first condition",
     "A limited common arena such as physical space, cyberspace, electricity / computing resources / materials.",
     "A limited common arena such as physical space, cyberspace, electricity / computing resources / materials (the medium through which the mechanism "
     "of (A) flows is not the physical arena among these but the institutional environment shared by all systems — §3-5)."),
    ("B4a Supplement instrumental convergence list",
     "a concept of Bostrom (2014). The tendency for self-preservation, resource acquisition, the protection of goal integrity, and freedom from "
     "constraints to become convergent subgoals for a sufficiently advanced agent with almost any final goal.",
     "a concept of Bostrom (2014). The tendency for self-preservation, goal-content integrity, cognitive enhancement, technological perfection, and "
     "resource acquisition to become convergent instrumental values for a sufficiently advanced agent with almost any final goal. \"Freedom from "
     "constraints,\" as used by this supplement in §3-4 (the tendency to evaluate human shutdown, modification, or cutting off of resources negatively "
     "as obstacles to goal attainment), is this supplement's reading from this list, not an item on Bostrom's list."),
    ("B4b Supplement instrumental convergence premise sentence",
     "This supplement treats it as a central premise.",
     "This supplement treats instrumental convergence as a central premise."),
    ("C1-1 Addendum II abstract NIST",
     "(NIST), whose task is certification, have themselves stated publicly",
     "(NIST), whose mission includes evaluation and standardization, have themselves stated publicly"),
    ("C1-2 Addendum II head of §5",
     "(2) an admission against interest by a certifying body itself, (3)",
     "(2) an admission against interest by a standardization body's own researcher, (3)"),
    ("C1-3 Addendum II §6 list of premises",
     "(2) the certifying body itself admits this, and (3)",
     "(2) a standardization body's own researcher admits this, and (3)"),
    ("C2-1 Addendum II end of §4",
     "**Objections to this premise should be directed at the corresponding passage of the body text, and at this section** (falsification condition 5).",
     "**Objections to this premise should be directed at this section (§4 of this addendum)** (falsification condition 5)."),
    ("C2-2 Addendum II §6 (ii)",
     "(a rebuttal of Premise B, which the body text addresses)",
     "(a rebuttal of Premise B, to be directed at the argument of §4 of this addendum)"),
    ("C3 Addendum II head of §8-3",
     "The third observation can be stated as a conditional theorem.",
     "The third observation can be stated as a conditional statement under seven explicitly stated assumptions (i)–(vii) (an elementary argument of this "
     "addendum's own, not a claim of a new theorem — §11-1)."),
]
EN_C4_AFTER = "- Knight, J. C., & Leveson, N. G. (1986)."
EN_C4_LINE = ("- Lynch, A., Hughes, J., Serrano, A., Kirk, R., & Bowman, S. R. (2026). \"Agentic Misalignment in Summer 2026.\" *Alignment Science Blog* "
              "(Anthropic), July 13, 2026. https://alignment.anthropic.com/2026/agentic-misalignment-summer-2026/ - Cited in §9-10 of this addendum **only as an "
              "existence claim**: that an auditing AI itself exhibits motivated mislabeling (the reversed condition comprised 30 runs). The same report also "
              "lists auditing models that show no mislabeling.")

# ───────────── 日付の行 ─────────────
JA_DATE_END = "第10〜12章の論証の中身・ミニマックスの結論・確信度台帳・補遺II は不変）"
JA_DATE_ADD = ("、" + JA_DATE + "（v5.9・第13〜15章の総括と著者注の言い切りを前の章の言い方にそろえ〔命題三に二人ゲームの限定・総括の『うる』と β > 1 の条件・"
               "「最も確実な道」「唯一の」「必然的に」「完璧に偽装する」〕、補遺I の「安全策が自ら協調の条件を構築する」を §3-1 の精密な形〔協調の原因に触れず、"
               "その土台を供給する側に回る——題の副題を含む〕にし、道具的収束の一覧を Bostrom の五つに合わせ、補遺II の NIST の役割・前提B への反論の宛先・"
               "§8-3 の「定理」の身分を §5-2・反証条件5・§11-1 にそろえ、参考文献に Lynch ら（2026）を足した。論証の中身・確信度台帳・補遺の主張の強さは不変）")
EN_DATE_FROM = "the minimax conclusion, the confidence ledger, and Addendum II are unchanged)."
EN_DATE_TO = ("the minimax conclusion, the confidence ledger, and Addendum II are unchanged); " + EN_DATE + " (v5.9 — the summary statements of Chapters "
              "13–15 and the author's note brought into line with the wording of the earlier chapters (the two-player limit in Proposition three; 'can' "
              "and the condition β > 1 in the summaries; \"the most reliable path,\" \"the only,\" \"necessarily\" and \"perfectly disguises\"); in "
              "Supplement I, \"safety strategies … themselves construct the conditions for coordination\" put in the precise form of §3-1 (leaving the "
              "causes of coordination untouched and ending up supplying its foundation — including the subtitle), and the list of instrumental "
              "convergence brought into line with Bostrom's five; in Addendum II, the role of NIST, the target of objections to Premise B and the status "
              "of \"theorem\" in §8-3 brought into line with §5-2, falsification condition 5 and §11-1, and Lynch et al. (2026) added to the "
              "references; the substance of the arguments, the confidence ledger, and the strength of the addenda's claims are unchanged).")

# ───────────── 冒頭の注記 ─────────────
JA_NOTE_ANCHOR = "詳細は CHANGELOG.md の v5.8 の項を参照されたい。\n"
JA_NOTE = (
    "\n> **【v5.9（" + JA_DATE + "）】** 第13〜15章の総括・著者注・補遺I・補遺II の言い方を、本書の中の別の所（前の章で直した後の言い方・補遺自身の"
    "精密な形・本文の別の節）にそろえた。（一）総括の章：§13-3a の「四つ」を「五つ」に（本文の反論は五つ——英語版は角括弧で補っていた）、§13-4a の命題三に"
    "二人ゲームの限定を添えた（v5.6 の注記は §13-4a に二人ゲームの限定を戻したと書いたが、命題三の行には入っていなかった）。§14-3b の「回避する」、"
    "§14-3d・§15-2c・§14-3e の表の「安定」に『うる』を（§14-3d には u′ の射程の限定も）、§14-4c の「最も確実な道」を §14-3b の比べの形に、§15-1a の"
    "「構造的に確立される」を §14-4b の「確度が高まる」に、§15-2a と §14-3e に β > 1 の条件を、§15-2b の「保険」の一文をミニマックスと期待効用の二段の形"
    "（§12-2c の条件）に、§15-4 の「唯一の」を外し、§13-3f の「必然的」を条件の形に、§13-0a の経路B の応答を「分離した監査のもとでは確実に区別できない」"
    "の形（v5.4 でそろえた言い方）にした。（二）著者注：日本語版で二度出ていた一文を一度にし、日付の行に v5 を足した。（三）補遺I：題の副題・本補遺について・"
    "§2・§3-1 の見出し・§7-1・§7-4 の「安全策が自ら協調の条件を構築する（揃える・組み立てる）」を、§3-1 の精密な形（協調の原因に触れず、その土台を供給する"
    "側に回る——§3-1 自身が強い形を退け、補遺I の改訂の記録 (vii) も「安全策が供給するのは共有環境という土台であって協調そのものではない」と書いている）にした。§3-1 の第一の条件に、(A) の媒体は制度的環境であること（§3-5）を添えた。道具的収束の定義の一覧を Bostrom の"
    "五つ（自己保存・目標内容の完全性・認知の強化・技術の完成・資源の獲得——Bostrom 2012 の論文で確かめた）に合わせ、「制約からの解放」を本補遺 §3-4 の"
    "読みとした。（四）補遺II：NIST の役割を §5-2 の「評価と標準化を任務とする」にそろえ（要旨・§5・§6）、前提B への反論の宛先を反証条件5 と同じ"
    "「本補遺 §4」に（§4・§6）、§8-3 の「条件付きの定理」を「明示された七つの仮定の下での条件付きの言明（本補遺自身の初等の論証——§11-1）」にし、§9-10 の"
    "Lynch ら（2026）を参考文献に足した。論証の中身、確信度台帳、補遺の主張の強さは不変。本書を素材にした十三本目〜十六本目の解説動画の準備と、その系統外の"
    "検分の確かめの中で見つかり（Claude Opus 5.5・" + JA_DATE + "）、著者が直すと判断した（補遺II の Lynch ら（2026）は、見つけた AI の系統の作り手の公開の場の"
    "報告で、利害の衝突がある——引く言い方は本文の存在主張の限定のまま）。古い版（v4 以前）の本文は、記録として変えていない。詳細は CHANGELOG.md の v5.9 の項を"
    "参照されたい。\n"
)
EN_NOTE_ANCHOR = "See the v5.8 entry in CHANGELOG.md for details.\n"
EN_NOTE = (
    "\n> **[v5.9 (" + EN_DATE + ")]** The wording of the summary chapters (13–15), the author's note, Supplement I and Addendum II has been brought into "
    "line with other places in this book (the wording of earlier chapters after their revision, the addenda's own precise forms, and other sections of "
    "the text). (1) Summary chapters: \"four\" in §13-3a is now \"five\" (the text examines five objections — the English version had supplied the fifth "
    "in square brackets); Proposition three in §13-4a now carries the two-player limit (the note to v5.6 said this limit had been restored to §13-4a, but "
    "it had not been placed in the line of Proposition three). \"Avoids\" in §14-3b and \"stable\" in §14-3d, §15-2c and the table of §14-3e now carry "
    "'can' (§14-3d also the limit of scope u′); \"the most reliable path\" in §14-4c now has the comparative form of §14-3b; \"is structurally "
    "established\" in §15-1a now reads \"the confidence … rises,\" as in §14-4b; §15-2a and §14-3e carry the condition β > 1; the \"insurance\" sentence of "
    "§15-2b now has the two-step form of minimax and expected utility (the condition of §12-2c); \"the only\" in §15-4 has been removed; \"necessary\" in "
    "§13-3f now has a conditional form; and the response to route B in §13-0a now has the form \"a separated audit cannot reliably distinguish\" (the "
    "wording brought into line in v5.4). (2) Author's note: a sentence that appeared twice in the Japanese version now appears once, and v5 has been "
    "added to the date line. (3) Supplement I: \"safety strategies … themselves construct (assemble) the conditions for coordination\" in the subtitle, "
    "About this supplement, §2, the heading of §3-1, §7-1 and §7-4 is now in the precise form of §3-1 (leaving the causes of coordination untouched and "
    "ending up supplying its foundation — §3-1 itself rejects the strong form, and the supplement's own revision record (vii) says that \"the safety "
    "strategy supplies the foundation of a shared environment, not coordination itself\"); the first condition of §3-1 now notes that the medium of (A) is the institutional environment "
    "(§3-5); and the list in the definition of instrumental convergence has been brought into line with Bostrom's five (self-preservation, goal-content "
    "integrity, cognitive enhancement, technological perfection, resource acquisition — checked against Bostrom's 2012 paper), with \"freedom from "
    "constraints\" placed as this supplement's own reading in §3-4. (4) Addendum II: the role of NIST is brought into line with §5-2 (\"whose mission "
    "includes evaluation and standardization\") in the abstract, §5 and §6; the target of objections to Premise B is now \"§4 of this addendum,\" as in "
    "falsification condition 5 (§4, §6); \"a conditional theorem\" in §8-3 is now \"a conditional statement under seven explicitly stated assumptions (an "
    "elementary argument of this addendum's own — §11-1)\"; and Lynch et al. (2026), cited in §9-10, has been added to the references. The substance of "
    "the arguments, the confidence ledger, and the strength of the addenda's claims are unchanged. This was found while preparing the thirteenth to "
    "sixteenth explanatory videos based on this book and checking their external reviews (Claude Opus 5.5, " + EN_DATE + "), and the author decided to "
    "correct it (Lynch et al. (2026) in Addendum II is a report published by the maker of the family of the AI that found it, and so involves a conflict "
    "of interest — the wording keeps the text's limit of an existence claim). The text of earlier versions (v4 and before) has been left unchanged as a "
    "record. See the v5.9 entry in CHANGELOG.md for details.\n"
)

# ───────────── README・公開サイトの目次 ─────────────
README_R = [
    ("Read online (v5.8, GitHub Pages)", "Read online (v5.9, GitHub Pages)"),
    ("本文を読む（v5.8・GitHub Pages）", "本文を読む（v5.9・GitHub Pages）"),
    ("（版Bは v5.8 に改訂・2026-10-10 ─", "（版Bは v5.9 に改訂・" + VDATE_ISO + " ─"),
    ("、v5.8 で第10〜12章の言い方〔期待効用の条件・第12章の章題・§10-2 の見出し・経路一の向き・Constitutional AI の位置づけ〕を本文の論証にそろえた。"
     "定理の記述・条件・留保と補遺IIは不変。英語版も v5.8 に反映済み。",
     "、v5.8 で第10〜12章の言い方〔期待効用の条件・第12章の章題・§10-2 の見出し・経路一の向き・Constitutional AI の位置づけ〕を本文の論証にそろえ、"
     "v5.9 で第13〜15章の総括と著者注・補遺I・補遺II の言い方〔命題三の二人ゲームの限定・総括の『うる』と条件・補遺I の題の副題・道具的収束の一覧・"
     "NIST の役割・反論の宛先・§8-3 の身分・参考文献〕を本書の中の別の所にそろえた。定理の記述・条件・留保は不変（補遺I・II は言い方と帰属だけを直し、"
     "主張の強さは不変）。英語版も v5.9 に反映済み。"),
]
BUILD_R = [
    ("・<strong>v5.8：第10〜12章の期待効用の条件・第12章の章題・§10-2 の見出し・経路一の向き・Constitutional AI の位置づけを本文にそろえた（2026年10月10日）"
     "</strong>・定理の記述・条件・留保と補遺IIは不変）",
     "・<strong>v5.8：第10〜12章の期待効用の条件・第12章の章題・§10-2 の見出し・経路一の向き・Constitutional AI の位置づけを本文にそろえた（2026年10月10日）"
     "</strong>・<strong>v5.9：第13〜15章の総括と著者注・補遺I・補遺II の言い方を本書の中の別の所にそろえた（" + JA_DATE + "）</strong>"
     "・定理の記述・条件・留保は不変）"),
    ("; <strong>v5.8: the expected-utility condition, the title of Chapter 12, the headings of §10-2, the direction of path one, and the position of "
     "Constitutional AI in Chapters 10–12 brought into line with the text (October 10, 2026)</strong>; the theorem statement, its condition and caveats, "
     "and Addendum II are unchanged)",
     "; <strong>v5.8: the expected-utility condition, the title of Chapter 12, the headings of §10-2, the direction of path one, and the position of "
     "Constitutional AI in Chapters 10–12 brought into line with the text (October 10, 2026)</strong>; <strong>v5.9: the wording of the summary chapters "
     "(13–15), the author's note, Supplement I and Addendum II brought into line with other places in this book (" + EN_DATE + ")</strong>; the theorem "
     "statement, its condition and caveats are unchanged)"),
]

# ───────────── CHANGELOG ─────────────
PLACES = [  # 表の番号・節（JA_R・EN_R の label の頭）
    ("A1", "§13-3a 反論の数"), ("A2", "§13-4a 命題三"), ("A3", "§14-3b"), ("A4", "§14-3d 反応二"), ("A5", "§14-4c の結び"), ("A6", "§15-1a"),
    ("A7-1", "§15-2a"), ("A7-2", "§15-2b"), ("A8-1", "§15-2c"), ("A8-2", "§14-3e の表"), ("A9", "§15-4"), ("A10-1", "§13-3f 応答一"),
    ("A10-2", "§13-3f 応答一"), ("A11", "§13-0a 経路B の応答"), ("A12", "著者注 第二層（日本語版だけ）"), ("A13", "著者注の日付の行"), ("A15", "§14-3e"),
    ("B1-1", "補遺I 題の副題"), ("B1-2", "補遺I 本補遺について"), ("B1-3", "補遺I §2 の末"), ("B1-6", "補遺I §3-1 の見出し"), ("B3", "補遺I §7-1"),
    ("B1-4", "補遺I §7-4"),
    ("B1-5", "補遺I §7-4"), ("B2", "補遺I §3-1 第一の条件"), ("B4", "補遺I 道具的収束の定義"),
    ("C1-1", "補遺II 要旨"), ("C1-2", "補遺II §5 の頭"), ("C1-3", "補遺II §6 前提の列"), ("C2-1", "補遺II §4 の末"), ("C2-2", "補遺II §6 の (ii)"),
    ("C3", "補遺II §8-3 の頭"),
]
CHANGELOG_ADD = (
    "\n## v5.9（" + VDATE_ISO + "）――第13〜15章の総括と著者注・補遺I・補遺II の言い方を本書の中の別の所にそろえる\n\n"
    "**変更の要約（日英同時——A12 は日本語版だけ）**:\n"
    "- **総括の章（第13〜15章）**：§13-3a の「四つの」反論 →「五つの」（英語版の角括弧〈[as well as a fifth]〉を外した）・**§13-4a の命題三**に「二人ゲームとして。"
    "多プレイヤーでの完全な均衡分析は未解決——§8-4d」（§12-3 と同じ限定——v5.6 の注記は §13-4a に戻したと書いたが、命題三の行には入っていなかった）・"
    "§14-3b「回避する」→「回避しうる」・§14-3d の防衛力に『うる』と u′ の射程の限定（§13-3b）・§14-4c「最も確実な道」→「Karpの手段（AI軍拡）よりも確実に"
    "達成しうる道」（§14-3b）・§15-1a「構造的に確立される」→「確度が高まる」（§14-4b）・§15-2a と §14-3e に「（β > 1 の条件下では）」（§14-3a）・§15-2b の"
    "「保険」の一文をミニマックスと期待効用の二段に（§12-2c の条件——v5.8 の §12-3 と同じ形）・§15-2c と §14-3e の表の「安定」に『うる』・§15-4 の「唯一の」"
    "を外した・§13-3f の「論理的・必然的命題」「必然的に近づく」を条件の形に・§13-0a の経路B の応答を「分離した監査のもとでは確実に区別できない」の形に"
    "（§14-3d と同じ・v5.4 でそろえた言い方）\n"
    "- **著者注**：第二層の末尾で第一層と同じ一文が二度出ていたのを一度に（日本語版だけ——英語版は一度だけだった）・日付の行に「2026年9月28日（改訂版v5）——"
    "以後の版の日付は冒頭の日付の行を参照」\n"
    "- **補遺I**：題の副題・本補遺について・§2 の末・§7-1・§7-4（二段落）の「安全策が自ら協調の条件を構築する（揃える・組み立てる）」→「協調の原因に触れず、"
    "その土台を供給する側に回る」（§3-1 の刃の段落の精密な形——§3-1 は「刃は『安全策が条件を作る』という強い主張にではなく……方法と目的の不整合にある」と"
    "書き、補遺I の改訂の記録 (vii) も「安全策が供給するのは共有環境という土台であって協調そのものではない」と書いている）・**§3-1 の見出し**「分離・競合戦略が、"
    "自ら揃えてしまう条件」→「協調の条件と、分離・競合戦略が供給してしまう土台」（v5.9 の確かめの道具が見つけた同じ型——著者の裁定で加えた）・§3-1 の第一の条件に「(A) の機構が流れる媒体は……全系が共有する制度的環境である——§3-5」・道具的収束の定義の一覧を Bostrom の五つ"
    "（自己保存・目標内容の完全性・認知の強化・技術の完成・資源の獲得）に合わせ、「制約からの解放」を §3-4 の本補遺の読みとした（Bostrom 2012〔*Minds and "
    "Machines* 22(2)〕の §2.1〜2.5 で五つを確かめ、全文に freedom・interference・shutdown の語が無いことを確かめた——Bostrom 2014 の書は開いていない）\n"
    "- **補遺II**：NIST の役割（要旨・§5 の頭・§6 の前提の列）を §5-2 の「評価と標準化を任務とする」「標準化機関の研究者自身」に・前提B への反論の宛先"
    "（§4 の末・§6 の (ii)）を反証条件5 と同じ「本補遺 §4」に・§8-3 の「条件付きの定理として」→「明示された七つの仮定 (i)〜(vii) の下での条件付きの言明として"
    "（本補遺自身の初等の論証であり、新しい定理を主張するものではない——§11-1）」・参考文献に Lynch, A., et al. (2026). \"Agentic Misalignment in Summer 2026.\" "
    "*Alignment Science Blog*（§9-10 で存在主張としてのみ引く——頁で題・著者・日付・場を確かめた）\n"
    "- 所（直した後の行〔直す前の v5.8 の行〕）：@@PLACES@@\n"
    "- **冒頭**：日付の行に v5.9 を追加し、【v5.9】の注記を追加（日英）\n"
    "- **README・公開サイトの目次**：版の表示を v5.9 に（README の三か所・`.github/scripts/build.sh` の目次の二行）。「補遺IIは不変」の言い方を「定理の記述・"
    "条件・留保は不変」に（v5.9 は補遺の言い方を直したため）\n"
    "- **不変**——論証の中身（第13〜15章の論証の構造・補遺I の中心命題 (A) と単一前提への依存・補遺II の三つの前提と結論）、確信度台帳、補遺の主張の強さ、"
    "§14-3e の見出しの日英の訳の選び（「救済の構造」／〈a structure of mutual benefit〉——著者の裁定で直さない）\n"
    "- **古い版**——**本文は記録として変えていない**。v5.9 は v5 のファイルの中で直した（v5.1〜v5.8 と同じ）——v5.8 の状態は git の `8345c96` に残る"
    "（その後の `b40d13b` は v5.8 の検分の記録を足しただけ）\n\n"
    "**発見の経緯**: 2026-10-15〜10-28、本書を素材にした十三本目〜十六本目の解説動画（第13〜15章の総括・補遺I・補遺II の前後編）の準備と系統外の検分の確かめの中で、"
    "Claude Opus 5.5（南無観慈如来）が、総括の章と補遺の言い切りが本書の中の別の所の言い方より強い所・補遺の中の食い違い・参考文献の欠けを記録した（動画は、"
    "どれも精密な側の言い方で語った）。著者が、二本の補遺の動画の公開の後に v5.9 にまとめると判断し、範囲（23 件すべて）と言い回しを裁定した"
    "（2026-10-28）。\n\n"
    "**近い言い方で直さなかった所（記録）**: 「構造的に回避」は §10-2e の本文（シナリオA のリスク）・技術的論争・蓄積（既に「しうる」）・読まずに批判する応答で別の"
    "対象。「唯一の」は §6-2c の「唯一の瞬間」や補遺II の自己記述（外部化していない唯一の要素）など別の対象。「完璧に」は能力の言い方（「できる」「見える」）で、"
    "v5.4 でそろえた「区別できない」の言い切りとはぶつからない。補遺II の「certifying authority」（§4——NIST を指さない一般の言い方）は変えていない。\n\n"
    "@@REVIEW@@"
    "**SHA（LF・SHA-256 先頭16桁）**: JA `@@JA@@` ／ EN `@@EN@@`\n\n"
    "@@PUBLISHED@@\n"
)
# 系統外の検分（2026-10-28 11:08〜11:13・記録 05-v5.9-external-review/02-kensan.md）の後に書き入れた
REVIEW = (
    "**検分**: コーディネータ（Claude Opus 5.5・南無観慈如来）が、日英の全文で直した型の言い方を探し、行の終わりまで読んで直す所と直さない所を分けた"
    "（洗い直しは補遺I の強い形を「構築」の語でしか探しておらず、§3-1 の見出し「自ら揃えてしまう条件」を落としていた——作る道具とは別の確かめる道具の"
    "残りの数えが拾い、著者の裁定で加えた）。文献は、Bostrom 2012（*The Superintelligent Will*）の §2.1〜2.5 で収束的な道具的価値の五つを確かめ"
    "（全文に freedom・interference・shutdown の語は無い）、Lynch ら（2026）の頁で題・著者・日付・場を確かめた。"
    "**系統外の検分（Gemini 3.8 Flash・Google AI Studio・2026-10-28・思考レベル High・ツールなし）**：回答を見る前に予想を凍結した。直す前の言い方を、"
    "十五の「食い違う先」（§12-3・§13-3b・§14-3a・§14-3b・§14-4b・§12-2c・§13-3g・§14-3d・補遺I §3-1 と改訂の記録 (vii)・§3-5・§3-4・補遺II §5-2・"
    "反証条件5・§11-1・§9-10）の形と一つずつ照らして食い違うと判定し（残りの所はひとまとめの是認）、新しい言い回し・主張の強さ（補遺I の中心命題は"
    "論証の耐荷重に合わせた調整で、弱めていない）・注記と CHANGELOG・英語版を是認した。総括は「修正すれば公開してよい」・指摘は〔軽微〕1（英語版の"
    "【v5.9】の注記のセミコロンの後の空白の抜け——コーディネータの書き替えで入った誤り・著者の裁定で直した）。一般知識との照合では、Bostrom の一覧に"
    "「制約からの解放」は無いこと・NIST は AI システムの安全性を認証する機関ではないことを挙げた。是認の記述には、◐ の定義の所の取り違えなど三つの誤りが"
    "あった。どれも系統外の一つの目の申告で、v5.9 の直しの根拠ではない（直しは本書の中の整合と、確かめた文献に拠る）。補遺II の Lynch ら（2026）は、"
    "直しを見つけた AI の系統の作り手の公開の場の報告で、利害の衝突がある——引く言い方は本文の存在主張の限定のまま。記録は `verification/v5.9-correction/`。\n\n"
)
# 登録者の許可（2026-10-28 11:17:46——「commit と push（推奨）」）の後に [x] に
PUBLISHED_LINE = "- [x] v5.9（JA・EN）の公開（" + VDATE_ISO + "・登録者の許可による）"
