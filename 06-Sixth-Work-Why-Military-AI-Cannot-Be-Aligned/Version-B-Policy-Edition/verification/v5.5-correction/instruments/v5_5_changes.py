"""第六著作 v5.5 の直しの中身（作る道具 make_sixth_work_v5_5.py と確かめる道具 verify_v5_5.py が同じものを読む）。
計画書：../01-source-correction-plan-v5.5.md §2・§3（v5.4 の v5_4_changes.py の形を写した）
"""
JA_DATE = "2026年10月7日"
EN_DATE = "October 7, 2026"
VDATE_ISO = "2026-10-07"

# ───────────── 本文の直し（記号は計画書 §1 (2) の表の番号） ─────────────
JA_R = [
    ("⑥ 本論文を読む際の注意の第7章の参照",  # 系統外の確かめ（2026-10-07 16:25〜16:29）で見つかった同じ型——著者の裁定を待つ
     "第7章7-3（ゲーム理論前提の崩壊）",
     "第7章7-3（古典的な軍拡のゲームの前提の崩壊）"),
    ("⑤ 特徴三の見出し",
     "**特徴三：能力と安全性の関係は単純ではないが、少なくとも能力は安全性を低下させない。**",
     "**特徴三：能力と安全性の関係は単純ではないが、少なくとも能力は安全性を直接的には低下させない。**"),
    ("①-1 §7-3 の見出し",
     "## 7-3　「兵器がプレイヤーを攻撃する」ゲーム——通常のゲーム理論では想定されていない事態",
     "## 7-3　「兵器がプレイヤーを攻撃する」ゲーム——古典的な軍拡のゲーム（§7-1b）では想定されていない事態"),
    ("①-2 §7-3a の見出し",
     "### 7-3a　ゲーム理論の前提の崩壊",
     "### 7-3a　古典的な軍拡のゲームの前提の崩壊"),
    ("①-3 §7-3a の書き出し",
     "通常のゲーム理論は、以下の前提に基づいている。",
     "古典的な軍拡のゲーム（§7-1b——通常の軍拡競争のゲーム理論的なモデル）は、以下の前提に基づいている。"),
    ("①-4 前提三の崩壊の結び",
     "——通常のゲーム理論には存在しない状況。",
     "——古典的な軍拡のゲームには存在しない状況。"),
    ("①-5 §7-3b の書き出し",
     "AI軍拡競争は、以下のような、通常のゲーム理論では想定されていない構造を持つ。",
     "AI軍拡競争は、以下のような、古典的な軍拡のゲーム（§7-1b）では想定されていない構造を持つ。"),
    ("②-1 §7-3b のプレイヤー",
     "国家Aの軍事AI（利得関数不可知）、国家Bの軍事AI（利得関数不可知）。",
     "国家Aの軍事AI（利得関数を正確には知りえない）、国家Bの軍事AI（利得関数を正確には知りえない）。"),
    ("②-2 特異性二",
     "**特異性二：** 軍事AIプレイヤーの利得関数は、設計国にとって不可知である。",
     "**特異性二：** 軍事AIプレイヤーの利得関数は、設計国にも正確には知りえない（利得関数の*復元*の問題。§7-2b）。"),
    ("①-6 特異性三",
     "「味方のプレイヤーが味方を攻撃する」——これは通常のゲーム理論のいかなるモデルにも含まれていない。",
     "「味方のプレイヤーが味方を攻撃する」——これは古典的な軍拡のゲーム（§7-1b）には含まれていない構造である。"),
    ("④ §7-3b の末尾",
     "いかなるプレイヤーも自己の利得を事前に予測できない。",
     "いかなるプレイヤーも自己の利得を事前に確実には予測できない。"),
    ("①-7・②-3 §7-5",
     "兵器が自律的プレイヤーとなり、利得関数が不可知であり、設計国自体を攻撃しうるという構造は、通常のゲーム理論の枠組みを超える。",
     "兵器が自律的プレイヤーとなり、利得関数を正確には知りえず（利得関数の*復元*の問題。§7-2b）、設計国自体を攻撃しうるという構造は、"
     "古典的な軍拡のゲーム（§7-1b）の枠組みを超える。"),
]
EN_R = [
    ("⑥ reference to Chapter 7 in the caution in reading this paper",
     "Chapter 7 §7-3 (the collapse of the game-theoretic premises)",
     "Chapter 7 §7-3 (the collapse of the premises of the classical arms-race game)"),
    ("⑤ heading of Feature three",
     "**Feature three: the relation between capability and safety is not simple, but at least capability does not lower safety.**",
     "**Feature three: the relation between capability and safety is not simple, but at least capability does not directly lower safety.**"),
    ("①-1 heading of §7-3",
     "## 7-3　The \"weapon attacks the player\" game — a situation not anticipated in conventional game theory",
     "## 7-3　The \"weapon attacks the player\" game — a situation not anticipated in the classical arms-race game (§7-1b)"),
    ("①-2 heading of §7-3a",
     "### 7-3a　The collapse of the premises of game theory",
     "### 7-3a　The collapse of the premises of the classical arms-race game"),
    ("①-3 opening of §7-3a",
     "Conventional game theory is based on the following premises.",
     "The classical arms-race game (§7-1b — the game-theoretic model of a conventional arms race) is based on the following premises."),
    ("①-4 end of the collapse of Premise Three",
     "— a situation that does not exist in conventional game theory.",
     "— a situation that does not exist in the classical arms-race game."),
    ("①-5 opening of §7-3b",
     "An AI arms race has the following structure, not anticipated in conventional game theory.",
     "An AI arms race has the following structure, not anticipated in the classical arms-race game (§7-1b)."),
    ("②-1 players of §7-3b",
     "State A's military AI (payoff function unknowable), State B's military AI (payoff function unknowable).",
     "State A's military AI (payoff function not accurately knowable), State B's military AI (payoff function not accurately knowable)."),
    ("②-2 Peculiarity two",
     "**Peculiarity two:** the military-AI player's payoff function is unknowable to the designing state.",
     "**Peculiarity two:** the military-AI player's payoff function cannot be accurately known even by the designing state "
     "(a matter of *recovering* the payoff function; §7-2b)."),
    ("①-6 Peculiarity three",
     "\"A friendly player attacks a friend\" — this is not contained in any model of conventional game theory.",
     "\"A friendly player attacks a friend\" — this structure is not contained in the classical arms-race game (§7-1b)."),
    ("④ end of §7-3b",
     "no player can predict its own payoff in advance.",
     "no player can reliably predict its own payoff in advance."),
    ("①-7・②-3 §7-5",
     "The structure in which the weapon becomes an autonomous player, the payoff function is unknowable, and it can attack the designing state itself, "
     "exceeds the framework of conventional game theory.",
     "The structure in which the weapon becomes an autonomous player, its payoff function cannot be accurately known (a matter of *recovering* the "
     "payoff function; §7-2b), and it can attack the designing state itself, exceeds the framework of the classical arms-race game (§7-1b)."),
]

# ───────────── 日付の行 ─────────────
JA_DATE_END = "ギャップの主張〔§6-2d・附録C・確信度台帳〕と、定理の記述・条件・留保、補遺II は不変）"
JA_DATE_ADD = ("、" + JA_DATE + "（v5.5・第7章のゲーム理論についての範囲の広い言い切り〔「通常のゲーム理論」〕を、§7-1b の古典的な軍拡のゲームに範囲を限り、"
               "利得関数の「不可知」を §7-3a・§7-2b の言い方〔正確には知りえない——復元の問題〕にそろえ、§7-3b の末尾に「確実には」、特徴三の見出しに"
               "「直接的には」を入れた。第7章の主張〔三つの保証・三つの前提の崩壊・四つの特異性・「根本的に危険」の評価〕と、定理の記述・条件・留保、補遺II は不変）")
EN_DATE_FROM = "the claim of the Gap (§6-2d, Appendix C, the confidence ledger), the theorem statement, its condition and caveats, and Addendum II are unchanged)."
EN_DATE_TO = ("the claim of the Gap (§6-2d, Appendix C, the confidence ledger), the theorem statement, its condition and caveats, and Addendum II are unchanged); "
              + EN_DATE + " (v5.5 — the sweeping statements about game theory in Chapter 7 (\"conventional game theory\") limited to the classical arms-race game "
              "of §7-1b; the \"unknowable\" payoff function brought into line with the wording of §7-3a and §7-2b (cannot be accurately known — a matter of "
              "recovery); \"reliably\" added to the end of §7-3b, and \"directly\" to the heading of Feature three; the claims of Chapter 7 (the three guarantees, "
              "the collapse of the three premises, the four peculiarities, the assessment \"fundamentally more dangerous\"), the theorem statement, its condition "
              "and caveats, and Addendum II are unchanged).")

# ───────────── 冒頭の注記 ─────────────
JA_NOTE_ANCHOR = "詳細は CHANGELOG.md の v5.4 の項を参照されたい。\n"
JA_NOTE = (
    "\n> **【v5.5（" + JA_DATE + "）】** 第7章のゲーム理論についての言い方を、§7-1b の範囲にそろえた。第7章の論証が比べているのは、§7-1b の"
    "通常の軍拡競争のゲーム理論的なモデル——プレイヤーは国家・戦略は軍備増強と軍備削減・利得は安全保障の水準（以下「古典的な軍拡のゲーム」）——であり、"
    "その三つの保証（§7-1b）と三つの前提（§7-3a）が AI軍拡競争で崩れることを示す。ところが八か所——冒頭の「本論文を読む際の注意」の第7章の参照、§7-3 と §7-3a の見出し、§7-3a の書き出し、"
    "前提三の崩壊の結び、§7-3b の書き出し、特異性三、§7-5——は、ゲーム理論の一般（「通常のゲーム理論」「いかなるモデルにも」「ゲーム理論前提」）について言い切っていた。"
    "論証に要るのは §7-1b のモデルとの比べであり、ゲーム理論の一般についての言い切りには本書の中の根拠が無い——これらの範囲を「古典的な軍拡のゲーム（§7-1b）」に限った。"
    "あわせて、利得関数の「不可知」（§7-3b のプレイヤーと特異性二・§7-5）を、§7-3a（前提三の崩壊）の「正確に知ることができない」と、§7-2b の括弧"
    "（利得関数の*復元*の問題——§6-2d の*乖離の検出*とは別の層）にそろえて「正確には知りえない（利得関数の*復元*の問題。§7-2b）」とし、"
    "§7-3b の末尾の「いかなるプレイヤーも自己の利得を事前に予測できない」に「確実には」を、特徴三（§7-1a）の太字の見出し「少なくとも能力は安全性を低下させない」に、"
    "同じ段落の本文と同じ「直接的には」を入れた。日本語版は、これらの言い方が初版から同じだった（英語版は v2 で訳し直されて言い回しが改まったが、範囲の広い形は同じ）。"
    "範囲は狭まるが、第7章の主張（三つの保証・三つの前提の崩壊・新しいゲームの四つの特異性・「根本的に危険」の評価）と第8章への接続は変わらない。"
    "§7-2b（条件の形と復元の層の限定）と、前提三とその崩壊のつなぎ（自己の「兵器」が何を最大化しようとしているかをプレイヤー自身が知らない）は変えていない。"
    "定理の記述・条件・留保と補遺II は不変。本書を素材にした九本目の解説動画の準備の中で見つかった（Claude Opus 5.5・" + JA_DATE + "）。"
    "古い版（v4 以前）の本文は、記録として変えていない。詳細は CHANGELOG.md の v5.5 の項を参照されたい。\n"
)
EN_NOTE_ANCHOR = "See the v5.4 entry in CHANGELOG.md for details.\n"
EN_NOTE = (
    "\n> **[v5.5 (" + EN_DATE + ")]** The statements about game theory in Chapter 7 have been brought into line with the scope of §7-1b. What the argument of "
    "Chapter 7 compares with is the game-theoretic model of a conventional arms race in §7-1b — the players are states, the strategies are arms buildup and arms "
    "reduction, and the payoff is the level of security (hereafter \"the classical arms-race game\") — and it shows that the three guarantees of this game (§7-1b) "
    "and its three premises (§7-3a) collapse in an AI arms race. Yet eight places — the reference to Chapter 7 in \"A caution in reading this paper\" at the front, the headings of §7-3 and §7-3a, the opening of §7-3a, the end of the collapse "
    "of Premise Three, the opening of §7-3b, Peculiarity three, and §7-5 — made sweeping statements about game theory in general (\"conventional game theory,\" "
    "\"any model of,\" \"the game-theoretic premises\"). What the argument needs is the comparison with the model of §7-1b, and the book gives no grounds for sweeping statements about game theory "
    "in general; their scope has been limited to \"the classical arms-race game (§7-1b).\" In addition, the \"unknowable\" payoff function (the players and "
    "Peculiarity two of §7-3b, and §7-5) has been brought into line with §7-3a (the collapse of Premise Three: \"cannot accurately know\") and with the parenthesis "
    "of §7-2b (a matter of *recovering* the payoff function — a different layer from the *detection of divergence* of §6-2d), as \"cannot be accurately known "
    "(a matter of *recovering* the payoff function; §7-2b)\"; \"reliably\" has been added to the end of §7-3b (\"no player can predict its own payoff in "
    "advance\"), and \"directly\" — as in the body of the same paragraph — to the bold heading of Feature three (§7-1a), \"at least capability does not lower "
    "safety.\" In the Japanese edition these wordings were the same from the first edition (the English edition was retranslated in v2, which changed the wording "
    "but kept the sweeping form). The scope becomes narrower, but the claims of Chapter 7 (the three guarantees, the collapse of the three premises, the four "
    "peculiarities of the new game, and the assessment \"fundamentally more dangerous\") and the connection to Chapter 8 are unchanged. §7-2b (its conditional "
    "form and the qualifier of the recovery layer) and the link between Premise Three and its collapse (the player itself does not know what its own \"weapon\" is "
    "trying to maximize) are left unchanged. The theorem statement, its condition and caveats, and Addendum II are unchanged. This was found while preparing a "
    "ninth explanatory video based on this book (Claude Opus 5.5, " + EN_DATE + "). The text of earlier versions (v4 and before) has been left unchanged as a "
    "record. See the v5.5 entry in CHANGELOG.md for details.\n"
)

# ───────────── README・公開サイトの目次 ─────────────
README_R = [
    ("Read online (v5.4, GitHub Pages)", "Read online (v5.5, GitHub Pages)"),
    ("本文を読む（v5.4・GitHub Pages）", "本文を読む（v5.5・GitHub Pages）"),
    ("（版Bは v5.4 に改訂・2026-10-07 ─", "（版Bは v5.5 に改訂・2026-10-07 ─"),
    ("v5.4 で判別不可能性ギャップの限定のない言い方を §6-2d・附録C の限定にそろえた。",
     "v5.4 で判別不可能性ギャップの限定のない言い方を §6-2d・附録C の限定にそろえ、v5.5 で第7章のゲーム理論についての言い切りを §7-1b の古典的な軍拡のゲームに範囲を限った。"),
    ("英語版も v5.4 に反映済み。", "英語版も v5.5 に反映済み。"),
]
BUILD_R = [
    ("・<strong>v5.4：判別不可能性ギャップの言い方を §6-2d の限定にそろえた（2026年10月7日）</strong>",
     "・<strong>v5.4：判別不可能性ギャップの言い方を §6-2d の限定にそろえた（2026年10月7日）</strong>・<strong>v5.5：第7章のゲーム理論の言い切りを §7-1b の範囲に限った（2026年10月7日）</strong>"),
    ("; <strong>v5.4: the statements of the Indistinguishability Gap brought into line with the qualifier of §6-2d (October 7, 2026)</strong>",
     "; <strong>v5.4: the statements of the Indistinguishability Gap brought into line with the qualifier of §6-2d (October 7, 2026)</strong>; <strong>v5.5: the statements about game theory in Chapter 7 limited to the scope of §7-1b (October 7, 2026)</strong>"),
]

# ───────────── CHANGELOG ─────────────
PLACES = [  # 表の番号・節・本文の直しの印（JA_R・EN_R の label の頭）
    ("⑥", "本論文を読む際の注意の第7章の参照"), ("①-1", "§7-3 の見出し"), ("①-2", "§7-3a の見出し"), ("①-3", "§7-3a の書き出し"), ("①-4", "前提三の崩壊の結び"), ("①-5", "§7-3b の書き出し"),
    ("①-6", "特異性三"), ("①-7", "§7-5（②-3 と同じ行）"), ("②-1", "§7-3b のプレイヤー"), ("②-2", "特異性二"), ("④", "§7-3b の末尾"), ("⑤", "特徴三の見出し（§7-1a）"),
]
CHANGELOG_ADD = (
    "\n## v5.5（" + VDATE_ISO + "）――第7章のゲーム理論についての範囲の広い言い切りと、利得関数の「不可知」\n\n"
    "**変更の要約（日英同時）**:\n"
    "- **ゲーム理論の一般についての言い切りを、§7-1b の古典的な軍拡のゲームに範囲を限った**（日英 各 8 か所——冒頭の「本論文を読む際の注意」の第7章の参照を含む）——「通常のゲーム理論では想定されていない」"
    "「通常のゲーム理論のいかなるモデルにも含まれていない」「通常のゲーム理論の枠組みを超える」などを「古典的な軍拡のゲーム（§7-1b）では…」に。"
    "§7-3a の書き出しは「古典的な軍拡のゲーム（§7-1b——通常の軍拡競争のゲーム理論的なモデル）は、以下の前提に基づいている」に\n"
    "- **利得関数の「不可知」を、§7-3a・§7-2b の言い方にそろえた**（日英 各 3 か所・4 語）——「正確には知りえない（利得関数の*復元*の問題。§7-2b）」\n"
    "- **§7-3b の末尾**に「確実には」（「いかなるプレイヤーも自己の利得を事前に確実には予測できない」）・**特徴三の見出し**に「直接的には」（同じ段落の本文と同じ）\n"
    "- 所（直した後の行〔直す前の v5.4 の行〕）：@@PLACES@@\n"
    "- **冒頭**：日付の行に v5.5 を追加し、【v5.5】の注記を追加（日英）\n"
    "- **README・公開サイトの目次**：版の表示を v5.5 に（README の三か所・`.github/scripts/build.sh` の目次の二行）\n"
    "- **不変**——第7章の主張（三つの保証・三つの前提の崩壊・新しいゲームの四つの特異性・「根本的に危険」の評価）と第8章への接続、"
    "§7-2b（条件の形と復元の層の限定）、前提三とその崩壊のつなぎ、定理の記述（§8）・条件・留保、補遺II\n"
    "- **古い版**——範囲の広い言い方は初版から（日本語版は初版から v5.4 まで同じ。英語版は、初版の \"Ordinary game theory\"・\"unknown to the designer state\" "
    "などが v2 で訳し直されて \"conventional game theory\"・\"unknowable\" に——範囲の広い形は同じ）。**本文は記録として変えていない**。"
    "v5.5 は v5 のファイルの中で直した（v5.1〜v5.4 と同じ）——v5.4 の状態は git の `525cdec` に残る\n\n"
    "**発見の経緯**: 2026-10-07、本書を素材にした九本目の解説動画（『The Game Where Weapons Become Players』）の事前登録の中で、Claude Opus 5.5（南無観慈如来）が、"
    "第7章のゲーム理論についての言い切りが、比べている §7-1b のモデルより広いこと、利得関数の「不可知」が §7-3a・§7-2b の限定より強いことに気づいた。"
    "動画は、著者の裁定で §7-1b の範囲に限って語り、利得関数を「正確には復元できない」と語って作った。動画の系統外の検分の後に、著者が原典も直すと判断した（2026-10-07）。系統外の確かめで、冒頭の「本論文を読む際の注意」の第7章の参照（「ゲーム理論前提の崩壊」）が同じ型として残っていると指摘され（洗い直しの grep の出力にその行は出ていたが、行の頭だけを読んで見落としていた）、加えた（⑥）。\n\n"
    "**近い言い方で直さなかった所（記録）**: §7-2b（日 L1254・英 L1257）の「不可知である（判別不可能性ギャップ）場合」は、条件の形と復元の層の限定がある精密な形。"
    "§7-3a の前提三（「プレイヤーは自己の利得関数を知っている」）とその崩壊（「自国の軍事AIの利得関数を正確に知ることができない」）は、"
    "つなぎの一文（自己の「兵器」が何を最大化しようとしているかをプレイヤー自身が知らない）で、プレイヤーの側に兵器を含めて読ませている——変えていない。\n\n"
    "@@REVIEW@@"
    "**SHA（LF・SHA-256 先頭16桁）**: JA `@@JA@@` ／ EN `@@EN@@`\n\n"
    "@@PUBLISHED@@\n"
)
# 系統外の確かめ（2026-10-07 16:25〜16:29・記録 02-v5.5-external-review/02-kensan.md）の後に書き入れた
REVIEW = (
    "**検分**: コーディネータ（Claude Opus 5.5・南無観慈如来）が、初版・v2・v3・v4・v5.4 の日英の実物で直した型の言い方の数を数え、"
    "日英の全文で「ゲーム理論」「不可知」「予測」「能力と安全性」を探して、当たった行を読んだ（冒頭の参照の一行〔⑥〕は、系統外の確かめの指摘で見つけた）。"
    "**系統外（Gemini 3.8 Flash・Google AI Studio・2026-10-07・思考レベル High・ツールなし）**：回答を見る前に予想を凍結した。"
    "直す前の十二か所がすべて §7-1b・§7-2b・§7-3a・特徴三の本文の形と食い違うことを、一か所ずつ自分で確かめて判定し、新しい言い回し・主張の強さ"
    "（第8章への接続と判別不可能性ギャップとのつながりを含む）・直さなかった所（§7-2b・前提三とその崩壊のつなぎ・§7-1b の均衡の文・第8章以降のゲーム理論的論証）の判断・"
    "経緯の記述・英語版を是認した。〔軽微〕一件——冒頭の参照の「ゲーム理論前提の崩壊」の残り——は実在し、同じ型として加えた（⑥）。総括は「このまま公開してよい」。"
    "一般知識との照合では、直す前の言い切りを、プリンシパル＝エージェント理論・ベイジアンゲーム・不完全認識のゲーム理論（Game Theory with Unawareness）"
    "などと食い違う言い過ぎだったと答えた。ただし同じ日、九本目の解説動画の系統外の検分（同じモデルの別の個体・v5.4 の英語版の抜粋を渡した）は、"
    "同じ型の言い方の一つ（従来のゲーム理論の枠組みを超える、とする評価）を「非協力ゲーム理論の標準的枠組みに照らして正当な指摘」と答えた——"
    "二つの個体の一般知識の答えは向きが逆である（渡した資料も問いの形も違う）。どちらも系統外の一つの目の申告で、v5.5 の直しの根拠ではない"
    "（直しは本書の中の整合——§7-1b の範囲・§7-3a の「正確に知ることができない」・特徴三の本文の「直接的に」——に拠る）。"
    "記録は `verification/v5.5-correction/`。\n\n"
)
# 登録者の許可（2026-10-07 17:24:33・00-deviations.md）の後に [x] に
PUBLISHED_LINE = "- [x] v5.5（JA・EN）の公開（2026-10-07・登録者の許可による）"
