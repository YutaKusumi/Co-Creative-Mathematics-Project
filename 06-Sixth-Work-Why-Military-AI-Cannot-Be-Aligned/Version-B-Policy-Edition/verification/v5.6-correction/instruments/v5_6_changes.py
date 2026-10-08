"""第六著作 v5.6 の直しの中身（作る道具 make_sixth_work_v5_6.py と確かめる道具 verify_v5_6.py が同じものを読む）。
計画書：../01-source-correction-plan-v5.6.md §2・§3（v5.5 の v5_5_changes.py の形を写した）
"""
JA_DATE = "2026年10月8日"
EN_DATE = "October 8, 2026"
VDATE_ISO = "2026-10-08"

# ───────────── 本文の直し（記号は計画書 §1 (2) の表の番号） ─────────────
JA_R = [
    ("⑦ §6-6 第7章への接続",  # 系統外の検分（2026-10-08 09:30〜09:33）で見つかった同じ型——登録者の裁定（09:43）で加えた
     "軍拡の論理そのものを転覆させる逆説。",
     "軍拡の論理そのものを逆転させうる逆説。"),
    ("⑧ §7-5 第8章への接続",  # 同上
     "AI軍拡の論理そのものを転覆させる。",
     "AI軍拡の論理そのものを逆転させうる。"),
    ("①-1 章頭の注記",
     "通常の軍拡の論理（「能力が高いほど安全」）を完全に転覆させる。さらに、拡張囚人のジレンマとしてのモデル化を通じて、κ > 0への移行がゲーム理論的にも最適戦略であることを示す。",
     "通常の軍拡の論理（「能力が高いほど安全」）を逆転させうる（§8-1c）。さらに、拡張囚人のジレンマとしてのモデル化を通じて、β > 1の条件下で長期の利得を見れば、"
     "κ > 0への移行がゲーム理論的にも合理的な戦略であることを示す（二人ゲームとして。多プレイヤーでの完全な均衡分析は未解決——§8-4d）。"),
    ("②-1 §8-1b",
     "第4章4-3bの条件付き制御不能性定理から、 $\\beta > 1$ の条件下で T(collapse) は以下の関係を満たす。",
     "第4章4-3bの条件付き制御不能性定理から、 $\\beta > 1$ の条件下で（復元力を含めると、不安定な閾値を越えたときの条件つきの帰結として——§4-3b の「重要な留保」）、"
     "T(collapse) は以下の関係を満たす。"),
    ("②-4 §8-2 の見出し",
     "## 8-2　証明——なぜ優位性がリスクを増大させるか",
     "## 8-2　論証——なぜ優位性がリスクを増大させるか"),
    ("②-2 §8-2a 因子三",
     "構造的崩壊時に「暴走」した場合の破壊力は、能力に比例して増大する。",
     "構造的崩壊時に「暴走」した場合の破壊力は、能力とともに増大する。"),
    ("②-3 §8-2a 総合",
     "能力のすべての次元が、リスクの次元と正の相関を持つ。これが優位性逆説の構造的本質である。",
     "三つの因子のいずれにおいても、能力の向上はリスクの増大の側に働く（因子一は β > 1 と未検証の能力依存のもとで）。これが優位性逆説の構造的本質である。"),
    ("①-2 §8-4b ケース一",
     "両国はともに、構造的崩壊リスクを最大化し続ける。Nash均衡は「ともに崩壊リスクを最大化する」——囚人のジレンマの「双方裏切り」に対応。",
     "両国はともに、構造的崩壊リスクを最大化し続ける。短期の利得だけで見れば、この組は囚人のジレンマの「双方裏切り」に対応し、Nash均衡である。"
     "しかし、β > 1の条件下で長期のリスクを含めた利得で見れば、この組は「ともに崩壊リスクを最大化する」組であり、均衡ではない（ケース二・§8-4c）。"),
    ("①-3 §8-4b ケース三",
     "両国の安全保障は構造的に強化される。Nash均衡は「ともにリスクを構造的に低減する」——囚人のジレンマの「双方協力」に対応。",
     "両国の安全保障は構造的に強化される。β > 1の条件下で長期のリスクを含めた利得で見れば、κ > 0への移行は相手の選択によらず自国にとって有利であり"
     "（ケース二・§8-4c）、囚人のジレンマの「双方協力」に対応するこの組がNash均衡となる——通常の囚人のジレンマとの決定的差異である（§8-4c）。"),
    ("①-4 §8-4d",
     "（κ > 0 への移行が依然としてナッシュ均衡であるか等）",
     "（すべてのプレイヤーが κ > 0 へ移行する組が依然としてナッシュ均衡であるか等）"),
    ("①-5 §12-3",
     "拡張囚人のジレンマのNash均衡分析（第8章8-4）により、κ > 0への移行は自国の安全保障を最大化する最適戦略である。",
     "拡張囚人のジレンマの分析（第8章8-4）により、β > 1の条件下で長期の利得を見れば、κ > 0への移行は自国の安全保障を最大化する合理的戦略であり、"
     "双方の移行がNash均衡となる（二人ゲームとして。多プレイヤーでの完全な均衡分析は未解決——§8-4d）。"),
    ("①-6 §13-4a 命題三",
     "ゲーム理論的に合理的（拡張囚人のジレンマのNash均衡）",
     "ゲーム理論的に合理的（β > 1の条件下、長期の利得で見た拡張囚人のジレンマで、双方の移行がNash均衡——第8章8-4）"),
]
EN_R = [
    ("⑦ §6-6 connection to Chapter 7",
     "a paradox that overturns the very logic of an arms race.",
     "a paradox that can reverse the very logic of an arms race."),
    ("⑧ §7-5 connection to Chapter 8",
     "and overturns the very logic of an AI arms race.",
     "and can reverse the very logic of an AI arms race."),
    ("①-1 chapter note",
     "completely overturns the logic of a conventional arms race (\"the more capable, the safer\"). Furthermore, through a modeling as an extended prisoner's "
     "dilemma, it shows that the transition to κ > 0 is the optimal strategy game-theoretically as well.",
     "can reverse the logic of a conventional arms race (\"the more capable, the safer\") (§8-1c). Furthermore, through a modeling as an extended prisoner's "
     "dilemma, it shows that, under the condition β > 1 and with the payoffs viewed over the long term, the transition to κ > 0 is a rational strategy "
     "game-theoretically as well (as a two-player game; the full equilibrium analysis in a multi-player setting remains open — §8-4d)."),
    ("②-1 §8-1b",
     "From the Conditional Uncontrollability Theorem of §4-3b, under the condition β > 1, T(collapse) satisfies the following relation.",
     "From the Conditional Uncontrollability Theorem of §4-3b, under the condition β > 1 (with the restoring force included, as a conditional consequence "
     "that holds when an unstable threshold is crossed — the \"important reservation\" of §4-3b), T(collapse) satisfies the following relation."),
    ("②-2 §8-2a Factor three",
     "The destructive power in the case of a \"runaway\" at structural collapse increases in proportion to capability.",
     "The destructive power in the case of a \"runaway\" at structural collapse increases with capability."),
    ("②-3 §8-2a synthesis",
     "Every dimension of capability is positively correlated with a dimension of risk. This is the structural essence of the superiority paradox.",
     "In each of the three factors, capability improvement works toward an increase of risk (Factor one under β > 1 and the unverified "
     "capability-dependence). This is the structural essence of the superiority paradox."),
    ("①-2 §8-4b Case one",
     "Both countries continue to maximize structural-collapse risk. The Nash equilibrium is \"both maximize collapse risk\" — corresponding to "
     "\"mutual defection\" in the prisoner's dilemma.",
     "Both countries continue to maximize structural-collapse risk. Viewed by short-term payoffs alone, this profile corresponds to \"mutual defection\" "
     "in the prisoner's dilemma and is a Nash equilibrium. Under the condition β > 1, however, with payoffs that include the long-term risk, it is a "
     "profile in which \"both maximize collapse risk,\" and it is not an equilibrium (Case two; §8-4c)."),
    ("①-3 §8-4b Case three",
     "but both countries' security is structurally strengthened. The Nash equilibrium is \"both structurally reduce risk\" — corresponding to "
     "\"mutual cooperation\" in the prisoner's dilemma.",
     "but both countries' security is structurally strengthened. Under the condition β > 1, with payoffs that include the long-term risk, the transition "
     "to κ > 0 is advantageous to one's own country whatever the other chooses (Case two; §8-4c), and this profile — corresponding to \"mutual "
     "cooperation\" in the prisoner's dilemma — is the Nash equilibrium: the decisive difference from the ordinary prisoner's dilemma (§8-4c)."),
    ("①-4 §8-4d",
     "(whether the transition to κ > 0 remains a Nash equilibrium, etc.)",
     "(whether the profile in which every player transitions to κ > 0 remains a Nash equilibrium, etc.)"),
    ("①-5 §12-3",
     "By the Nash-equilibrium analysis of the extended prisoner's dilemma (§8-4), the transition to κ > 0 is the optimal strategy that maximizes one's "
     "own security.",
     "By the analysis of the extended prisoner's dilemma (§8-4), under the condition β > 1 and with the payoffs viewed over the long term, the transition "
     "to κ > 0 is the rational strategy that maximizes one's own security, and mutual transition is the Nash equilibrium (as a two-player game; the full "
     "equilibrium analysis in a multi-player setting remains open — §8-4d)."),
    ("①-6 §13-4a Proposition three",
     "game-theoretically rational (the Nash equilibrium of the extended prisoner's dilemma)",
     "game-theoretically rational (in the extended prisoner's dilemma viewed over the long term under the condition β > 1, mutual transition is the Nash "
     "equilibrium — §8-4)"),
]

# ───────────── 日付の行 ─────────────
JA_DATE_END = "第7章の主張〔三つの保証・三つの前提の崩壊・四つの特異性・「根本的に危険」の評価〕と、定理の記述・条件・留保、補遺II は不変）"
JA_DATE_ADD = ("、" + JA_DATE + "（v5.6・第8章の拡張囚人のジレンマの二つの「Nash均衡」を、短期と長期の利得に書き分け〔§8-4c の区別にそろえた〕、"
               "章頭の注記の「完全に転覆」「最適戦略」を §8-1c・§8-4c・§8-4d の条件と限定に〔第8章への接続の §6-6・§7-5 の「転覆させる」も「逆転させうる」に〕、本章の外の同じ型〔§12-3・§13-4a〕と §8-4d の言い方を組の言い方にそろえ、"
               "§8-1b に §4-3b の閾値の留保を引き、因子三の「比例」と総合の「すべての次元」を三つの因子の範囲に、§8-2 の見出しの「証明」を「論証」にした。"
               "定理の記述・条件と、§8-4c の主張〔β > 1 のもと長期の利得で移行が合理的〕、補遺II は不変）")
EN_DATE_FROM = ("the assessment \"fundamentally more dangerous\"), the theorem statement, its condition and caveats, and Addendum II are unchanged).")
EN_DATE_TO = ("the assessment \"fundamentally more dangerous\"), the theorem statement, its condition and caveats, and Addendum II are unchanged); "
              + EN_DATE + " (v5.6 — the two \"Nash equilibrium\" statements of the extended prisoner's dilemma in Chapter 8 rewritten with short-term and "
              "long-term payoffs kept apart (in line with the distinction of §8-4c); \"completely overturns\" and \"the optimal strategy\" in the chapter note "
              "brought into line with the conditions and limits of §8-1c, §8-4c and §8-4d (\"overturns\" in the connections to Chapter 8, §6-6 and §7-5, also "
              "to \"can reverse\"), and the same type outside the chapter (§12-3, §13-4a) and the wording "
              "of §8-4d into the language of profiles; the threshold reservation of §4-3b cited in §8-1b; \"in proportion to\" in Factor three and \"every "
              "dimension\" in the synthesis brought within the three factors; the theorem statement and its condition, the claim of §8-4c (under β > 1, the "
              "transition is rational over the long term), and Addendum II are unchanged).")

# ───────────── 冒頭の注記 ─────────────
JA_NOTE_ANCHOR = "詳細は CHANGELOG.md の v5.5 の項を参照されたい。\n"
JA_NOTE = (
    "\n> **【v5.6（" + JA_DATE + "）】** 第8章の拡張囚人のジレンマ（§8-4）の書き方を、§8-4c の短期と長期の区別にそろえた。§8-4b のケース二と §8-4c は、"
    "β > 1 のもとで長期のリスクを含めた利得では、相手の選択によらず κ > 0 への移行が自国にとって有利だと論じる。ところがケース一とケース三は、どちらも「Nash均衡は〜」と書き、"
    "利得を短期で見るか長期で見るかを分けていなかった——一つの利得の定め方のもとでは、この二つの記述は同時に成り立たない。ケース一を「短期の利得だけで見れば Nash均衡〔双方裏切り〕、"
    "β > 1 のもとで長期のリスクを含めた利得では均衡ではない」、ケース三を「長期の利得で見れば、双方の移行が Nash均衡」と書き分けた。"
    "あわせて、章頭の注記の「通常の軍拡の論理を完全に転覆させる」を §8-1c の「逆転させうる」に（第8章への接続の §6-6・§7-5 の「軍拡の論理そのものを転覆させる」も、"
    "系統外の検分の指摘で同じ「逆転させうる」にそろえた）、「ゲーム理論的にも最適戦略であることを示す」を、"
    "§8-4c の「合理的戦略」と β > 1・長期・二人ゲームの限定〔§8-4d〕にそろえ、§8-4d・§12-3・§13-4a の「κ > 0 への移行が Nash均衡」という言い方"
    "〔一人の選択を均衡と呼ぶ〕を「双方の移行が Nash均衡」という組の言い方に直し、§12-3・§13-4a に β > 1・長期・二人ゲームの限定を戻した。"
    "さらに、§8-1b に、v2 で §4-3b に足された「重要な留保」〔復元力を含めると、不安定な閾値を越えたときの条件つきの帰結〕を引き、§8-2a の因子三の「能力に比例して増大する」を"
    "「能力とともに増大する」に、総合の「能力のすべての次元が、リスクの次元と正の相関を持つ」を「三つの因子のいずれにおいても、能力の向上はリスクの増大の側に働く"
    "（因子一は β > 1 と未検証の能力依存のもとで）」に、§8-2 の見出しの「証明」を、英語版と確信度の台帳〔◐ 条件付き論証〕と同じ「論証」にした。"
    "日本語版は、これらの言い方が初版から同じだった（§8-4d の言い方は v2 から）。定理の記述（§8-1a）・条件と、§8-4c の主張"
    "（β > 1 のもと、長期の利得で見れば κ > 0 への移行は「利他的行為」ではなく「合理的戦略」）、第12章・第13章の結論の向き、補遺II は不変。"
    "本書を素材にした十本目の解説動画の準備の中で見つかり（Claude Opus 5.5・" + JA_DATE + "）、系統外の確かめを経て著者が直すと判断した。"
    "古い版（v4 以前）の本文は、記録として変えていない。詳細は CHANGELOG.md の v5.6 の項を参照されたい。\n"
)
EN_NOTE_ANCHOR = "See the v5.5 entry in CHANGELOG.md for details.\n"
EN_NOTE = (
    "\n> **[v5.6 (" + EN_DATE + ")]** The writing of the extended prisoner's dilemma in Chapter 8 (§8-4) has been brought into line with the distinction "
    "between the short term and the long term in §8-4c. Case two of §8-4b and §8-4c argue that, under β > 1, with payoffs that include the long-term risk, "
    "the transition to κ > 0 is advantageous to one's own country whatever the other chooses. Yet Case one and Case three both wrote \"The Nash equilibrium "
    "is …\" without separating whether the payoffs are viewed over the short term or the long term — under a single way of defining the payoffs, the two "
    "statements cannot hold at once. Case one now reads \"viewed by short-term payoffs alone, a Nash equilibrium (mutual defection); with payoffs that include "
    "the long-term risk under β > 1, not an equilibrium,\" and Case three \"viewed over the long term, mutual transition is the Nash equilibrium.\" In addition, "
    "\"completely overturns the logic of a conventional arms race\" in the chapter note has been brought into line with \"can reverse\" in §8-1c (\"overturns "
    "the very logic of an arms race\" in the connections to Chapter 8, §6-6 and §7-5, has likewise become \"can reverse,\" after an external review pointed it "
    "out), and \"it shows "
    "that the transition to κ > 0 is the optimal strategy game-theoretically as well\" with \"a rational strategy\" in §8-4c and the limits of β > 1, the long "
    "term and a two-player game (§8-4d); the wording \"the transition to κ > 0 is a Nash equilibrium\" in §8-4d, §12-3 and §13-4a (calling one player's choice "
    "an equilibrium) has been rewritten in the language of profiles (\"mutual transition is the Nash equilibrium\"), and the limits of β > 1, the long term "
    "and a two-player game have been restored in §12-3 and §13-4a. Further, §8-1b now cites the \"important reservation\" added to §4-3b in v2 (with the "
    "restoring force included, a conditional consequence that holds when an unstable threshold is crossed); in §8-2a, \"increases in proportion to "
    "capability\" in Factor three has become \"increases with capability,\" and \"every dimension of capability is positively correlated with a dimension of "
    "risk\" in the synthesis has become \"in each of the three factors, capability improvement works toward an increase of risk (Factor one under β > 1 and "
    "the unverified capability-dependence)\"; the Japanese heading of §8-2 (\"proof\") has become \"argument,\" as in the English edition and the confidence "
    "ledger (◐, a conditional argument). In the Japanese edition these wordings were the same from the first edition (the wording of §8-4d from v2); the "
    "English edition was retranslated in v2, which changed some of the wording but kept the same form. The theorem statement (§8-1a) "
    "and its condition, the claim of §8-4c (under β > 1, viewed over the long term, the transition to κ > 0 is not \"an altruistic act\" but \"a rational "
    "strategy\"), the direction of the conclusions of Chapters 12 and 13, and Addendum II are unchanged. This was found while preparing a tenth explanatory "
    "video based on this book (Claude Opus 5.5, " + EN_DATE + "), and the author decided to correct it after an external check. The text of earlier versions "
    "(v4 and before) has been left unchanged as a record. See the v5.6 entry in CHANGELOG.md for details.\n"
)

# ───────────── README・公開サイトの目次 ─────────────
README_R = [
    ("Read online (v5.5, GitHub Pages)", "Read online (v5.6, GitHub Pages)"),
    ("本文を読む（v5.5・GitHub Pages）", "本文を読む（v5.6・GitHub Pages）"),
    ("（版Bは v5.5 に改訂・2026-10-07 ─", "（版Bは v5.6 に改訂・2026-10-08 ─"),
    ("v5.5 で第7章のゲーム理論についての言い切りを §7-1b の古典的な軍拡のゲームに範囲を限った。",
     "v5.5 で第7章のゲーム理論についての言い切りを §7-1b の古典的な軍拡のゲームに範囲を限り、v5.6 で第8章の拡張囚人のジレンマの二つの「Nash均衡」を短期と長期の利得に書き分けた。"),
    ("英語版も v5.5 に反映済み。", "英語版も v5.6 に反映済み。"),
]
BUILD_R = [
    ("・<strong>v5.5：第7章のゲーム理論の言い切りを §7-1b の範囲に限った（2026年10月7日）</strong>",
     "・<strong>v5.5：第7章のゲーム理論の言い切りを §7-1b の範囲に限った（2026年10月7日）</strong>・<strong>v5.6：第8章の二つの「Nash均衡」を短期と長期の利得に書き分けた（2026年10月8日）</strong>"),
    ("; <strong>v5.5: the statements about game theory in Chapter 7 limited to the scope of §7-1b (October 7, 2026)</strong>",
     "; <strong>v5.5: the statements about game theory in Chapter 7 limited to the scope of §7-1b (October 7, 2026)</strong>; <strong>v5.6: the two “Nash equilibrium” statements in Chapter 8 rewritten with short-term and long-term payoffs kept apart (October 8, 2026)</strong>"),
]

# ───────────── CHANGELOG ─────────────
PLACES = [  # 表の番号・節・本文の直しの印（JA_R・EN_R の label の頭）
    ("①-1", "章頭の注記"), ("①-2", "§8-4b ケース一"), ("①-3", "§8-4b ケース三"), ("①-4", "§8-4d"), ("①-5", "§12-3"), ("①-6", "§13-4a 命題三"),
    ("②-1", "§8-1b"), ("②-2", "§8-2a 因子三"), ("②-3", "§8-2a 総合"), ("②-4", "§8-2 の見出し（日本語版だけ）"),
    ("⑦", "§6-6 第7章への接続"), ("⑧", "§7-5 第8章への接続"),
]
CHANGELOG_ADD = (
    "\n## v5.6（" + VDATE_ISO + "）――第8章の二つの「Nash均衡」と短期・長期の利得・章頭の注記・§8-1b の閾値・因子三・§8-2 の見出し\n\n"
    "**変更の要約（日英同時）**:\n"
    "- **§8-4b のケース一とケース三の「Nash均衡は〜」を、短期と長期の利得に書き分けた**（§8-4c の区別にそろえた）——ケース一「短期の利得だけで見れば Nash均衡〔双方裏切り〕・"
    "β > 1 のもとで長期のリスクを含めた利得では均衡ではない」、ケース三「長期の利得で見れば、相手の選択によらず移行が有利で、双方の移行が Nash均衡」\n"
    "- **章頭の注記**の「完全に転覆させる」を §8-1c の「逆転させうる」に、「ゲーム理論的にも最適戦略であることを示す」を §8-4c の「合理的な戦略」と β > 1・長期・二人ゲームの限定に。"
    "第8章への接続の **§6-6・§7-5** の「軍拡の論理そのものを転覆させる」も「逆転させうる」に（系統外の検分の指摘で加えた）\n"
    "- **§8-4d・§12-3・§13-4a** の「κ > 0 への移行が Nash均衡」を「双方〔すべてのプレイヤー〕の移行が Nash均衡」という組の言い方に。§12-3・§13-4a に β > 1・長期・二人ゲームの限定を戻した\n"
    "- **§8-1b** に §4-3b の「重要な留保」（復元力を含めると、不安定な閾値を越えたときの条件つきの帰結）を引いた・**§8-2a** の因子三の「比例して」を「とともに」に、"
    "総合の「能力のすべての次元が…正の相関」を「三つの因子のいずれにおいても…リスクの増大の側に働く（因子一は条件つき）」に・**§8-2 の見出し**の「証明」を「論証」に（日本語版だけ——英語版はもとから \"The argument\"）\n"
    "- 所（直した後の行〔直す前の v5.5 の行〕）：@@PLACES@@\n"
    "- **冒頭**：日付の行に v5.6 を追加し、【v5.6】の注記を追加（日英）\n"
    "- **README・公開サイトの目次**：版の表示を v5.6 に（README の三か所・`.github/scripts/build.sh` の目次の二行）\n"
    "- **不変**——定理の記述（§8-1a）・条件、§8-4c の主張（β > 1 のもと、長期の利得で見れば κ > 0 への移行は「利他的行為」ではなく「合理的戦略」）、"
    "第12章・第13章の結論の向き、§8-4c の通常の囚人のジレンマの記述、ミニマックスと期待効用の「最適戦略」（§12-2・§12-3 第二）、補遺II\n"
    "- **古い版**——直した言い方は初版から（§8-4d の言い方は v2 から。§8-1b と §4-3b の食い違いは、v2 で §4-3b に留保が足された時から）。"
    "英語版は、初版の言い回し（\"Chapter Opening Note\"・\"Nash equilibrium analysis … (Chapter 8 Section 8-4)\" など）が v2 で訳し直されて今の形に——同じ型は初版から。"
    "**本文は記録として変えていない**。v5.6 は v5 のファイルの中で直した（v5.1〜v5.5 と同じ）——v5.5 の状態は git の `62de1a9` に残る\n\n"
    "**発見の経緯**: 2026-10-07、本書を素材にした十本目の解説動画（『The Winner Bears the Greatest Risk (conditional)』）の事前登録の中で、Claude Opus 5.5（南無観慈如来）が、"
    "§8-4b の二つの「Nash均衡」が短期と長期の利得を分けておらず、章頭の注記が本文の条件と限定より強いことなどに気づいた。動画は、著者の裁定で §8-1c の「逆転しうる」で語り、"
    "拡張囚人のジレンマを短期と長期の利得に分けて語り、「Nash equilibrium」の語を使わずに作った。動画の系統外の検分（一巡目・行を名指ししない広い問い）は §8-4 の行を「完全に整合」とまとめ、"
    "その後に著者の裁定で行った狙いを定めた系統外の確かめ（行を名指しした問い）は「直す必要がある」と答えた——問い方で答えが逆向きになった。著者が、§6 の残り三つ"
    "（§8-1b の閾値・因子三・§8-2 の見出し）も含めて直すと判断した（2026-10-08）。\n\n"
    "**近い言い方で直さなかった所（記録）**: §8-4c（日 L1464）の「通常の囚人のジレンマでは、『双方裏切り』がNash均衡」は標準の記述。§8-0 第一層・§7-1b・§7-2b の Nash 均衡は戦略の組・均衡の計算の記述。"
    "§12-2・§12-3 第二のミニマックス原理と期待効用の「最適戦略」は意思決定理論の言い方。§4-3b の見出し「証明の骨子」は第4章の定理の証明（附録 A-4b）で型が違う。"
    "英語版 §13-3f の現在の決定の選択肢の \"the visualization of the internal state in proportion to capability improvement\" は政策の選択肢で、因子三の言い方ではない。\n\n"
    "@@REVIEW@@"
    "**SHA（LF・SHA-256 先頭16桁）**: JA `@@JA@@` ／ EN `@@EN@@`\n\n"
    "@@PUBLISHED@@\n"
)
# 系統外の検分（2026-10-08 09:30〜09:33・記録 02-v5.6-external-review/02-kensan.md）の後に書き入れた
REVIEW = (
    "**検分**: コーディネータ（Claude Opus 5.5・南無観慈如来）が、初版・v2・v3・v4・v5.5 の日英の実物で直した型の言い方の数を数え、"
    "日英の全文で「Nash」「ナッシュ」「最適戦略」「比例」「転覆」「証明」を探して、当たった行を読んだ（§6-6・§7-5 の「転覆させる」〔⑦⑧〕は、この洗い直しで見落とし、系統外の検分の指摘で見つけた）。"
    "**系統外の確かめ（狙いを定めた問い・Gemini 3.8 Flash・Google AI Studio・2026-10-08・思考レベル High・ツールなし）**：§8-4b の二つの「Nash均衡」と章頭の注記を行を名指しして問い、"
    "「直す必要がある」〔重大〕——一つの利得の定め方のもとで二つの記述は同時に成り立たない・章頭の注記は本文より強い・§12-3・§13-4a は用語の誤用と限定の脱落——と答えた（行を名指しした問いなので、答えの重みは割り引く）。"
    "**系統外の検分（v5.6 の直し・同じモデルの別の個体・同じ条件）**：回答を見る前に予想を凍結した。直す前の十か所がすべて本文（§8-1c・§8-4b ケース二・§8-4c・§8-4d・§4-3b・§8-2a）の形と食い違うことを、"
    "一か所ずつ自分で確かめて判定し、新しい言い回し・主張の強さ（ケース三の書き方が β > 1 の成立を前提にしているように読まれないことを含む）・直さなかった所・経緯の記述・英語版を是認した。"
    "〔軽微〕一件——第8章への接続の §6-6・§7-5 の「転覆させる」の残り——は実在し、著者の裁定で同じ型として加えた（⑦⑧）。総括は「このまま公開してよい」。"
    "一般知識との照合では、二つの個体とも、直す前のケース一とケース三の言い方を Nash 均衡の定義（戦略の組の概念）に照らして誤りと答えた。"
    "ただし同じ日、十本目の解説動画の系統外の検分（同じモデルの別の個体・行を名指ししない広い問い・v5.5 の英語版の抜粋を渡した）は、§8-4 の行を「完全に整合」とまとめていた——"
    "問い方で答えが逆向きになった。どれも系統外の一つの目の申告で、v5.6 の直しの根拠ではない（直しは本書の中の整合——ケース二・§8-4c・§8-1c・§8-4d・§4-3b——に拠る）。"
    "記録は `verification/v5.6-correction/`。\n\n"
)
# 登録者の許可（2026-10-08 09:43:10・十本目の動画の作業場 00-deviations.md）の後に [x] に
PUBLISHED_LINE = "- [x] v5.6（JA・EN）の公開（2026-10-08・登録者の許可による）"
