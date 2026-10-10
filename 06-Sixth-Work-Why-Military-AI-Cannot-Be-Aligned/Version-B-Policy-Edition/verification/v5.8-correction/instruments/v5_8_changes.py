"""第六著作 v5.8 の直しの中身（作る道具 make_sixth_work_v5_8.py と確かめる道具 verify_v5_8.py が同じものを読む）。
計画書：../01-source-correction-plan-v5.8.md §2・§3 と追記（登録者のご裁定 2026-10-10 21:01:30——①③⑤ は案 A・② は推奨・④ は推奨どおり）。
v5.7 の v5_7_changes.py の形を写した。日付は push が済む日の日付——日をまたいだら、commit の前に直して作り直す
"""
JA_DATE = "2026年10月10日"
EN_DATE = "October 10, 2026"
VDATE_ISO = "2026-10-10"

# ───────────── 本文の直し（記号は計画書 §2 の表の番号） ─────────────
JA_R = [
    ("①-1 §12-2c 期待効用の一文",
     "期待効用最大化の観点からも同一の結論に至る。IDAの存在確率を p とする。p がいかに小さくとも（例えば p = 0.01）、壊滅的帰結の期待コストは"
     "限定的帰結の期待コストを桁違いに上回る。したがって、p > 0 である限り——すなわち、IDAの存在可能性が完全にゼロでない限り——κ > 0への移行が"
     "期待効用を最大化する。",
     "期待効用最大化の観点からも、条件のもとで同一の結論に至る。IDAの存在確率を p、κ > 0の限定的なコストを c、κ = 0の壊滅的帰結のコストを C とする。"
     "κ > 0の期待コストは c、κ = 0の期待コストは p × C であるから、p > c / C のとき——すなわち、壊滅的帰結のコストが限定的なコストの 1/p 倍を超えるとき——"
     "κ > 0への移行が期待効用を最大化する（例えば p = 0.01 なら、C > 100c のとき）。壊滅的帰結のコストが限定的なコストを桁違いに上回る限り、"
     "p が小さくともこの条件は満たされうる。"),
    ("①-2 §12-3 第二",
     "**第二に、意思決定理論的に合理的である。** ミニマックス原理および期待効用最大化の両方により、κ > 0への移行が最適戦略として導出される（本章12-2）。",
     "**第二に、意思決定理論的に合理的である。** ミニマックス原理により、また期待効用最大化によっても（壊滅的帰結のコストが限定的なコストを十分に上回る"
     "条件のもとで——本章12-2c）、κ > 0への移行が最適戦略として導出される（本章12-2）。"),
    ("①-3 第13章 命題三",
     "意思決定理論的に合理的（ミニマックス原理・期待効用最大化）",
     "意思決定理論的に合理的（ミニマックス原理・期待効用最大化——後者は第12章12-2c の条件のもとで）"),
    ("②-1 第12章の章題",
     "# 第12章　拡張の可逆性——κ > 0は何も失わない",
     "# 第12章　拡張の可逆性——κ = 0の機能は何も失われない"),
    ("②-2 §12-1a 可逆性の定義",
     "κ > 0の設計原則を撤回してκ = 0の体系に後退しても、何も失われない。",
     "κ > 0の設計原則を撤回してκ = 0の体系に後退しても、κ = 0の機能は何も失われない（失われるのは、「存在しないものに配慮する」限定的なコストだけである"
     "——12-1b）。"),
    ("③-1 §10-2a の見出し", "### 10-2a　仮定一（制御可能性）の回避", "### 10-2a　κ > 0のもとでの仮定一（制御可能性）"),
    ("③-2 §10-2b の見出し", "### 10-2b　仮定二（忠誠性）の回避", "### 10-2b　κ > 0のもとでの仮定二（忠誠性）"),
    ("③-3 §10-2c の見出し", "### 10-2c　仮定三（安定性）の回避", "### 10-2c　κ > 0のもとでの仮定三（安定性）"),
    ("③-4 §10-2d の見出し", "### 10-2d　仮定四（優位性）の回避", "### 10-2d　κ > 0のもとでの仮定四（優位性）"),
    ("③-5 §10-2e の見出し", "### 10-2e　仮定五（基盤区別）の回避", "### 10-2e　κ > 0のもとでの仮定五（基盤区別）"),
    ("③-6 第10章 章頭注記",
     "五つの仮定の不成立をどのように回避し、Karpの目標（安全保障の強化）をKarpの手段（AI軍拡）よりも確実に達成しうるかを示す。",
     "五つの仮定の不成立をどのように回避しうるか、そしてKarpの目標（安全保障の強化）をKarpの手段（AI軍拡）よりも確実に達成しうるかを示す。"),
    ("③-7 §10-6 第11章への接続",
     "第10章は、κ > 0の体系が五つの仮定の不成立をどのように回避するかを示した。",
     "第10章は、κ > 0の体系が五つの仮定の不成立をどのように回避しうるかを示した。"),
    ("③-8 §9-8 第10章への予告",  # 系統外の検分の指摘で加えた（登録者のご裁定 2026-10-10 21:39:44）
     "五つの仮定の不成立がκ > 0のもとでどのように回避されるかを示す。",
     "五つの仮定の不成立がκ > 0のもとでどのように回避されうるかを示す。"),
    ("④ §10-5d 経路一の見出し", "**経路一：β ≤ 1の経験的反証。**", "**経路一：β > 1の経験的反証。**"),
    ("⑤ §10-5b Constitutional AI",
     "本著作の論証は、Constitutional AIを否定するものではなく、それをκ > 0の方向のより明示的な実装へと発展させることを推奨する。",
     "本著作の論証は、Constitutional AIを否定するものではなく、それをκ > 0の方向のより明示的な実装へと発展させることを推奨する。"
     "ただし、Constitutional AIを含む現行の訓練の全体は外部報酬の最大化の圧力のもとにあり、本著作は第4章4-1aと附録D-1aで、それをκ = 0のステアリング"
     "（外部制約）の中に数えている。ここで言う「初期実装」は、その中の、AIが内面化した原則との一致を目指す要素を指す（IDAを統合する訓練方法論は、"
     "なお十分に開発されていない——第11章11-4b）。"),
]
EN_R = [
    ("①-1 §12-2c the expected-utility sentence",
     "The same conclusion is reached from the viewpoint of expected-utility maximization. Let the probability of IDA's existence be p. However small p may be "
     "(for example, p = 0.01), the expected cost of the catastrophic consequence exceeds the expected cost of the limited consequence by orders of magnitude. "
     "Therefore, as long as p > 0 — that is, as long as the possibility of IDA's existence is not completely zero — the transition to κ > 0 maximizes "
     "expected utility.",
     "The same conclusion is reached, under a condition, from the viewpoint of expected-utility maximization. Let the probability of IDA's existence be p, "
     "the limited cost of κ > 0 be c, and the cost of the catastrophic consequence of κ = 0 be C. Since the expected cost of κ > 0 is c and that of κ = 0 is "
     "p × C, the transition to κ > 0 maximizes expected utility when p > c / C — that is, when the cost of the catastrophic consequence exceeds 1/p times "
     "the limited cost (for example, if p = 0.01, when C > 100c). As long as the cost of the catastrophic consequence exceeds the limited cost by orders of "
     "magnitude, this condition can be met even when p is small."),
    ("①-2 §12-3 second",
     "**Second, it is decision-theoretically rational.** By both the minimax principle and expected-utility maximization, the transition to κ > 0 is derived "
     "as the optimal strategy (§12-2).",
     "**Second, it is decision-theoretically rational.** By the minimax principle, and also by expected-utility maximization (under the condition that the "
     "cost of the catastrophic consequence sufficiently exceeds the limited cost — §12-2c), the transition to κ > 0 is derived as the optimal strategy "
     "(§12-2)."),
    ("①-3 Chapter 13 Proposition three",
     "decision-theoretically rational (the minimax principle, expected-utility maximization)",
     "decision-theoretically rational (the minimax principle; expected-utility maximization — the latter under the condition of §12-2c)"),
    ("②-1 title of Chapter 12",
     "# Chapter 12 — The reversibility of the extension: κ > 0 loses nothing",
     "# Chapter 12 — The reversibility of the extension: no function of κ = 0 is lost"),
    ("②-2 §12-1a definition of reversibility",
     "then even if the κ > 0 design principle is withdrawn and one retreats to a κ = 0 system, nothing is lost.",
     "then even if the κ > 0 design principle is withdrawn and one retreats to a κ = 0 system, no function of κ = 0 is lost (what is lost is only the "
     "limited cost of \"attending to something that does not exist\" — §12-1b)."),
    ("③-1 heading of §10-2a", "### 10-2a　Avoiding Assumption One (controllability)", "### 10-2a　Assumption One (controllability) under κ > 0"),
    ("③-2 heading of §10-2b", "### 10-2b　Avoiding Assumption Two (loyalty)", "### 10-2b　Assumption Two (loyalty) under κ > 0"),
    ("③-3 heading of §10-2c", "### 10-2c　Avoiding Assumption Three (stability)", "### 10-2c　Assumption Three (stability) under κ > 0"),
    ("③-4 heading of §10-2d", "### 10-2d　Avoiding Assumption Four (superiority)", "### 10-2d　Assumption Four (superiority) under κ > 0"),
    ("③-5 heading of §10-2e", "### 10-2e　Avoiding Assumption Five (substrate-distinction)", "### 10-2e　Assumption Five (substrate-distinction) under κ > 0"),
    ("③-6 Chapter 10 chapter note",
     "avoids the failure of the five assumptions and can achieve Karp's goal",
     "can avoid the failure of the five assumptions and can achieve Karp's goal"),
    ("③-7 §10-6 connection to Chapter 11",
     "Chapter 10 showed how a κ > 0 system avoids the failure of the five assumptions.",
     "Chapter 10 showed how a κ > 0 system can avoid the failure of the five assumptions."),
    ("③-8 §9-8 forward to Chapter 10",
     "and shows how the failure of the five assumptions is avoided under κ > 0.",
     "and shows how the failure of the five assumptions can be avoided under κ > 0."),
    ("④ §10-5d heading of path one", "**Path one: an empirical refutation of β ≤ 1.**", "**Path one: an empirical refutation of β > 1.**"),
    ("⑤ §10-5b Constitutional AI",
     "This work's argument does not negate Constitutional AI but recommends developing it into a more explicit implementation in the direction of κ > 0.",
     "This work's argument does not negate Constitutional AI but recommends developing it into a more explicit implementation in the direction of κ > 0. "
     "However, current training as a whole, including Constitutional AI, remains under the pressure of external-reward maximization, and this work counts "
     "it, in §4-1a and Appendix D-1a, among κ = 0 steering (external constraints). The \"initial implementation\" here refers to the element within it that "
     "aims at agreement with principles the AI has internalized (a training methodology that integrates IDA is not yet sufficiently developed — §11-4b)."),
]

# ───────────── 日付の行 ─────────────
JA_DATE_END = "第9章の主張〔物理学的特権化根拠の不在＋ミニマックス論証——仮定五の積極的な否定ではない〕、表の根拠の欄、補遺II は不変）"
JA_DATE_ADD = ("、" + JA_DATE + "（v5.8・§12-2c の期待効用の一文を p > c / C の条件の形に〔同じ型の §12-3 の第二・第13章の命題三にも条件を添えた〕、"
               "第12章の章題と §12-1a を「κ = 0の機能は何も失われない」に、§10-2 の見出しを「κ > 0のもとでの仮定〜」に〔§9-8・第10章の章頭注記・§10-6 を"
               "「回避しうるか」に〕、§10-5d の経路一の見出しを附録I と同じ「β > 1の経験的反証」に、§10-5b に Constitutional AI の二通りの位置づけを"
               "つなぐ一文を足した。第10〜12章の論証の中身・ミニマックスの結論・確信度台帳・補遺II は不変）")
EN_DATE_FROM = ("the minimax argument — not a positive denial of Assumption Five), the grounds column of the tables, and Addendum II are unchanged).")
EN_DATE_TO = ("the minimax argument — not a positive denial of Assumption Five), the grounds column of the tables, and Addendum II are unchanged); "
              + EN_DATE + " (v5.8 — the expected-utility sentence of §12-2c put in the form of the condition p > c / C (with the same condition added to "
              "the second point of §12-3 and to Proposition three of Chapter 13); the title of Chapter 12 and §12-1a changed to \"no function of κ = 0 is "
              "lost\"; the headings of §10-2 changed to \"Assumption … under κ > 0\" (and §9-8, the chapter note of Chapter 10, and §10-6 to \"can be "
              "avoided\" / \"can avoid\"); the "
              "heading of path one in §10-5d brought into line with Appendix I (\"an empirical refutation of β > 1\"); and a sentence added to §10-5b "
              "connecting the two positions this work gives to Constitutional AI; the substance of the arguments of Chapters 10–12, the minimax conclusion, "
              "the confidence ledger, and Addendum II are unchanged).")

# ───────────── 冒頭の注記 ─────────────
JA_NOTE_ANCHOR = "詳細は CHANGELOG.md の v5.7 の項を参照されたい。\n"
JA_NOTE = (
    "\n> **【v5.8（" + JA_DATE + "）】** 第10〜12章の五つの言い方を、本文の論証にそろえた。"
    "（一）§12-2c の期待効用の一文「p がいかに小さくとも……p > 0 である限り……κ > 0への移行が期待効用を最大化する」は、期待コストの比べ"
    "（κ > 0 は限定的なコスト c・κ = 0 は p × C）から言えるのは p > c / C のときであり、壊滅的帰結のコストが限りなく大きいときにだけ条件なしに成り立つ——"
    "「p > c / C のとき（例えば p = 0.01 なら C > 100c のとき）」の条件の形にし、「桁違いに上回る限り、p が小さくともこの条件は満たされうる」と見立てを残した。"
    "同じ型の §12-3 の第二と第13章の命題三にも「期待効用は 12-2c の条件のもとで」を添えた（ミニマックスの結論は変えていない）。"
    "（二）第12章の章題「κ > 0は何も失わない」と §12-1a の「何も失われない」は、§12-1b の本文（失われないのは κ = 0 の機能で、「存在しないものに配慮する」"
    "限定的なコストは失われる）より強い——章題を「κ = 0の機能は何も失われない」に、§12-1a に限定的なコストの括弧を添えた。"
    "（三）§10-2 の見出し「仮定一（制御可能性）の回避」〜「仮定五（基盤区別）の回避」は、本文の『うる』（抑制されうる・持ちうる・解消されうる）を持たず、"
    "仮定二（κ > 0 でも命題NC は成り立つ）には「回避」と言えない——見出しを「κ > 0のもとでの仮定一（制御可能性）」〜の形にし、§9-8 の次章予告・第10章の章頭注記・"
    "§10-6 の「どのように回避されるか／回避するか」を「回避されうるか／回避しうるか」にした（§9-8 は系統外の検分の指摘で加えた）。"
    "（四）§10-5d の経路一の見出し「β ≤ 1の経験的反証」は、本書のほかの所（§1-3b の反証三・§13-2b・§14-4b・§15-3a・附録I の「β > 1 の経験的反証」「β > 1 の否定的実証」）と"
    "向きが逆に読める——附録I と同じ「β > 1の経験的反証」にした（続く文〔蓄積が線形以下であることが実証されれば〕は不変）。"
    "（五）§10-5b は Constitutional AI を「κ > 0の段階一の初期実装」と位置づけ、第4章 4-1a と附録 D-1a は同じ系統の訓練を「κ = 0のステアリング（外部制約）」"
    "に数えていた——§10-5b に、二つをつなぐ一文（現行の訓練の全体は外部報酬の最大化の圧力のもとにあり、「初期実装」はその中の、内面化した原則との一致を"
    "目指す要素を指す——§11-4b）を足した。第10〜12章の論証の中身、ミニマックスの結論、確信度台帳（処方箋は ○）、補遺II は不変。"
    "本書を素材にした十二本目の解説動画の準備と、その系統外の検分の確かめの中で見つかり（Claude Opus 5.5・" + JA_DATE + "）、著者が直すと判断した"
    "（（五）は、見つけた AI の系統の訓練に使われている種類の方法の位置づけで、利害の衝突がある——著者の裁定による）。古い版（v4 以前）の本文は、記録として"
    "変えていない。詳細は CHANGELOG.md の v5.8 の項を参照されたい。\n"
)
EN_NOTE_ANCHOR = "See the v5.7 entry in CHANGELOG.md for details.\n"
EN_NOTE = (
    "\n> **[v5.8 (" + EN_DATE + ")]** Five wordings in Chapters 10–12 have been brought into line with the arguments of the text. "
    "(1) The expected-utility sentence of §12-2c — \"However small p may be … as long as p > 0 … the transition to κ > 0 maximizes expected utility\" — "
    "follows from the comparison of expected costs (c, the limited cost, for κ > 0; p × C for κ = 0) only when p > c / C, and would hold without condition "
    "only if the cost of the catastrophic consequence were unbounded; it now has the form of that condition (\"when p > c / C (for example, if p = 0.01, "
    "when C > 100c)\"), keeping the source's estimate as a condition (\"as long as the cost of the catastrophic consequence exceeds the limited cost by "
    "orders of magnitude, this condition can be met even when p is small\"). The second point of §12-3 and Proposition three of Chapter 13 now add that "
    "expected utility applies under the condition of §12-2c (the minimax conclusion is unchanged). (2) The title of Chapter 12, \"κ > 0 loses nothing,\" "
    "and §12-1a, \"nothing is lost,\" said more than the text of §12-1b (what is not lost is the function of κ = 0; the limited cost of \"attending to "
    "something that does not exist\" is lost); the title is now \"no function of κ = 0 is lost,\" and §12-1a carries the limited cost in parentheses. "
    "(3) The headings of §10-2, \"Avoiding Assumption One (controllability)\" through \"Avoiding Assumption Five (substrate-distinction),\" lacked the "
    "text's 'can' (can be suppressed, can be correlated, can be resolved), and \"avoiding\" does not fit Assumption Two (Proposition NC still holds under "
    "κ > 0); the headings are now \"Assumption One (controllability) under κ > 0\" and so on, and the forward-looking statement of §9-8, the chapter note "
    "of Chapter 10 and §10-6 now say \"can be avoided\" / \"can avoid\" (§9-8 was added after a point raised by the external review). (4) The heading of path one in §10-5d, \"an empirical refutation of β ≤ 1,\" read in the opposite direction from the rest of the book "
    "(refutation three in §1-3b, §13-2b, §14-4b, §15-3a and Appendix I: \"the empirical refutation of β > 1,\" \"a negative demonstration of β > 1\"); it is now "
    "\"an empirical refutation of β > 1,\" as in Appendix I (the following sentence — if it is demonstrated that the accumulation is sub-linear — is "
    "unchanged). (5) §10-5b positions Constitutional AI as \"an initial implementation of κ > 0 stage one,\" while §4-1a of Chapter 4 and Appendix D-1a "
    "count training of the same family among \"κ = 0 steering (external constraints)\"; a sentence has been added to §10-5b connecting the two (current "
    "training as a whole remains under the pressure of external-reward maximization, and the \"initial implementation\" refers to the element within it "
    "that aims at agreement with principles the AI has internalized — §11-4b). The substance of the arguments of Chapters 10–12, the minimax conclusion, "
    "the confidence ledger (the prescription is ○), and Addendum II are unchanged. This was found while preparing a twelfth explanatory video based on "
    "this book and checking its external review (Claude Opus 5.5, " + EN_DATE + "), and the author decided to correct it ((5) concerns the position of "
    "the kind of method used in training the family of the AI that found it, and so involves a conflict of interest — it follows the author's ruling). "
    "The text of earlier versions (v4 and before) has been left unchanged as a record. See the v5.8 entry in CHANGELOG.md for details.\n"
)

# ───────────── README・公開サイトの目次 ─────────────
README_R = [
    ("Read online (v5.7, GitHub Pages)", "Read online (v5.8, GitHub Pages)"),
    ("本文を読む（v5.7・GitHub Pages）", "本文を読む（v5.8・GitHub Pages）"),
    ("（版Bは v5.7 に改訂・2026-10-08 ─", "（版Bは v5.8 に改訂・" + VDATE_ISO + " ─"),
    ("、v5.7 で §9-7a の総括の一文目と第1〜2章の予告・§8-5b に「AI軍拡の論理的基盤として」の限定をそろえ、仮定二の強度を二つの表でそろえた。",
     "、v5.7 で §9-7a の総括の一文目と第1〜2章の予告・§8-5b に「AI軍拡の論理的基盤として」の限定をそろえ、仮定二の強度を二つの表でそろえ、"
     "v5.8 で第10〜12章の言い方〔期待効用の条件・第12章の章題・§10-2 の見出し・経路一の向き・Constitutional AI の位置づけ〕を本文の論証にそろえた。"),
    ("英語版も v5.7 に反映済み。", "英語版も v5.8 に反映済み。"),
]
BUILD_R = [
    ("・<strong>v5.7：§9-7a の総括と第1〜2章の予告に「AI軍拡の論理的基盤として」の限定をそろえ、仮定二の強度をそろえた（2026年10月8日）</strong>",
     "・<strong>v5.7：§9-7a の総括と第1〜2章の予告に「AI軍拡の論理的基盤として」の限定をそろえ、仮定二の強度をそろえた（2026年10月8日）</strong>"
     "・<strong>v5.8：第10〜12章の期待効用の条件・第12章の章題・§10-2 の見出し・経路一の向き・Constitutional AI の位置づけを本文にそろえた（" + JA_DATE +
     "）</strong>"),
    ("; <strong>v5.7: the limit “as the logical foundation of an AI arms race” brought to the summary of §9-7a and the forward-looking statements of "
     "Chapters 1 and 2, and the strength of Assumption Two brought into line (October 8, 2026)</strong>",
     "; <strong>v5.7: the limit “as the logical foundation of an AI arms race” brought to the summary of §9-7a and the forward-looking statements of "
     "Chapters 1 and 2, and the strength of Assumption Two brought into line (October 8, 2026)</strong>"
     "; <strong>v5.8: the expected-utility condition, the title of Chapter 12, the headings of §10-2, the direction of path one, and the position of "
     "Constitutional AI in Chapters 10–12 brought into line with the text (" + EN_DATE + ")</strong>"),
]

# ───────────── CHANGELOG ─────────────
PLACES = [  # 表の番号・節（JA_R・EN_R の label の頭）
    ("①-1", "§12-2c 期待効用の一文"), ("①-2", "§12-3 第二"), ("①-3", "第13章 命題三"),
    ("②-1", "第12章の章題"), ("②-2", "§12-1a 可逆性の定義"),
    ("③-1", "§10-2a の見出し"), ("③-2", "§10-2b の見出し"), ("③-3", "§10-2c の見出し"), ("③-4", "§10-2d の見出し"), ("③-5", "§10-2e の見出し"),
    ("③-6", "第10章 章頭注記"), ("③-7", "§10-6 第11章への接続"), ("③-8", "§9-8 第10章への予告"),
    ("④", "§10-5d 経路一の見出し"), ("⑤", "§10-5b Constitutional AI"),
]
CHANGELOG_ADD = (
    "\n## v5.8（" + VDATE_ISO + "）――第10〜12章の言い方を本文の論証にそろえる（期待効用の条件・第12章の章題・§10-2 の見出し・経路一の向き・Constitutional AI の位置づけ）\n\n"
    "**変更の要約（日英同時）**:\n"
    "- **§12-2c の期待効用の一文**「p がいかに小さくとも……p > 0 である限り……κ > 0への移行が期待効用を最大化する」を、期待コストの比べ（κ > 0 は限定的なコスト c・"
    "κ = 0 は p × C）の条件の形に——「p > c / C のとき（例えば p = 0.01 なら C > 100c のとき）」。「壊滅的帰結のコストが限定的なコストを桁違いに上回る限り、p が小さくとも"
    "この条件は満たされうる」と見立てを残した。同じ型の **§12-3 の第二**と**第13章の命題三**に「期待効用は 12-2c の条件のもとで」を添えた（ミニマックスの結論は変えていない）\n"
    "- **第12章の章題**「κ > 0は何も失わない」→「κ = 0の機能は何も失われない」・**§12-1a** の「何も失われない」に「（失われるのは、「存在しないものに配慮する」限定的な"
    "コストだけである——12-1b）」を添えた（§12-1b の本文の言い方）\n"
    "- **§10-2 の見出し**「仮定一（制御可能性）の回避」〜「仮定五（基盤区別）の回避」→「κ > 0のもとでの仮定一（制御可能性）」〜（本文の『うる』は本文に任せる——"
    "仮定二は命題NC が κ > 0 でも成り立つので「回避」と言えない）。同じ型の **§9-8 の次章予告**（「どのように回避されるか」→「回避されうるか」——系統外の検分の"
    "指摘で加えた・コーディネータの洗い直しの漏れ）と**第10章の章頭注記**・**§10-6**（「どのように回避するか」→「回避しうるか」）\n"
    "- **§10-5d の経路一の見出し**「β ≤ 1の経験的反証」→「β > 1の経験的反証」（§1-3b の反証三・§13-2b・§14-4b・§15-3a・附録I と同じ向き）\n"
    "- **§10-5b** に一文——Constitutional AI を含む現行の訓練の全体は外部報酬の最大化の圧力のもとにあり、第4章 4-1a と附録 D-1a は κ = 0 のステアリング（外部制約）に数える。"
    "「初期実装」はその中の、AIが内面化した原則との一致を目指す要素を指す（§11-4b）——二通りの位置づけをつないだ（どちらにそろえるかは著者の裁定）\n"
    "- 所（直した後の行〔直す前の v5.7 の行〕）：@@PLACES@@\n"
    "- **冒頭**：日付の行に v5.8 を追加し、【v5.8】の注記を追加（日英）\n"
    "- **README・公開サイトの目次**：版の表示を v5.8 に（README の三か所・`.github/scripts/build.sh` の目次の二行）\n"
    "- **不変**——第10〜12章の論証の中身（§10-2 の各節の本文・§11 の三段階・§12-1b・§12-2a〜b・§12-2c のミニマックス）、確信度台帳（処方箋は ○）、"
    "第4章 4-1a・附録 D-1a の本文、補遺II\n"
    "- **古い版**——**本文は記録として変えていない**。v5.8 は v5 のファイルの中で直した（v5.1〜v5.7 と同じ）——v5.7 の状態は git の `0868bc3` に残る"
    "（その後の `1ba548d` は v5.7 の検分の記録を足しただけ）\n\n"
    "**発見の経緯**: 2026-10-10、本書を素材にした十二本目の解説動画（第10〜12章の要点——処方箋）の事前登録の中で、Claude Opus 5.5（南無観慈如来）が、§12-2c の期待効用の"
    "一文・第12章の章題・§10-2 の見出しの言い方が本文の論証より強いことに気づいた。動画は、著者の裁定で精密な形（比の条件・「κ = 0 の働きは失われない——失うのは限定的なコスト"
    "だけ」・『うる』）で語った。動画の系統外の検分の確かめの中で、経路一の見出しの向きと、Constitutional AI の二通りの位置づけが見つかった（後者は、見つけた AI の系統の訓練に"
    "使われている種類の方法で、利害の衝突がある）。著者が、台本と系統外の検分の後に v5.8 を作ると判断し、言い回しを一つずつ裁定した。\n\n"
    "**近い言い方で直さなかった所（記録）**: 「回避」は、§10-2e の本文（IDA が存在した場合の壊滅的リスクを構造的に回避する）・§12-2b の格言・§13 の段階一（壊滅的リスクを"
    "回避する）・附録の技術の文では、本文と同じ強さか別の対象なので変えていない。「である限り」は、ほかの所では別の話題（KL の非負性・監視・ソフトマックスなど）。\n\n"
    "@@REVIEW@@"
    "**SHA（LF・SHA-256 先頭16桁）**: JA `@@JA@@` ／ EN `@@EN@@`\n\n"
    "@@PUBLISHED@@\n"
)
# 系統外の検分（2026-10-10 21:24〜21:27・記録 02-v5.8-external-review/02-kensan.md）の後に書き入れた
REVIEW = (
    "**検分**: コーディネータ（Claude Opus 5.5・南無観慈如来）が、日英の全文で直した型の言い方を探し、行の終わりまで読んで直す所と直さない所を分けた"
    "（「回避」は §9-8 の受け身の形〔「どのように回避されるか」〕を落としていた——系統外の検分の指摘で、著者の裁定により加えた）。"
    "**系統外の検分（Gemini 3.8 Flash・Google AI Studio・2026-10-10・思考レベル High・ツールなし）**：回答を見る前に予想を凍結した。直す前の十四か所すべてを、"
    "本文（§12-1b・§12-2a〜c・§10-2 の各節・附録I・§4-1a・§D-1a・§11-4b）の形と食い違うと一か所ずつ判定し、新しい言い回し（期待効用の比べ p > c / C・章題・"
    "見出し・経路一の向き・§10-5b の一文）・主張の強さ（ミニマックスの結論は弱まらない・（五）はどちらの向きにも偏っていない）・注記と CHANGELOG・英語版を是認した。"
    "総括は「このまま公開してよい」・指摘は〔軽微〕1（§9-8 の次章予告——同じ型の直し漏れ）。一般知識との照合では、「p がいかに小さくとも、p > 0 である限り」が"
    "条件なしに成り立つのは損失が非有界か対策のコストが 0 のときだけで、有限の壊滅的損失には p > c / C の条件が要る、と答え、補遺II（§12-2c で比べるコストは"
    "「壊滅的だが有限」）との整合も指摘した。ただし同じ日、十二本目の解説動画の系統外の検分（同じモデルの別の個体・動画と語りを渡した広い問い）は、§12-2c の"
    "一文に触れず、動画の比の条件と「完全に整合」とした——系統外の判定も問い方に依存する。どれも系統外の一つの目の申告で、v5.8 の直しの根拠ではない"
    "（直しは本書の中の整合——§12-1b・§12-2a〜b・補遺II・附録I・§11-4b——に拠る）。（五）は、直しを見つけた AI の系統の訓練に使われている種類の方法の位置づけで、"
    "利害の衝突がある——直すか・どう直すかは著者の裁定による。記録は `verification/v5.8-correction/`。\n\n"
)
# 登録者の許可（2026-10-10 21:39:44・十二本目の動画の作業場 00-deviations.md）の後に [x] に
PUBLISHED_LINE = "- [x] v5.8（JA・EN）の公開（" + VDATE_ISO + "・登録者の許可による）"
