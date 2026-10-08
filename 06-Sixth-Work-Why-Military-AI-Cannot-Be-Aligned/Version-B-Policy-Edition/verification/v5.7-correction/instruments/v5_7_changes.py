"""第六著作 v5.7 の直しの中身（作る道具 make_sixth_work_v5_7.py と確かめる道具 verify_v5_7.py が同じものを読む）。
計画書：../01-source-correction-plan-v5.7.md §2・§3（v5.6 の v5_6_changes.py の形を写した）
"""
JA_DATE = "2026年10月8日"
EN_DATE = "October 8, 2026"
VDATE_ISO = "2026-10-08"

# ───────────── 本文の直し（記号は計画書 §1 (2) の表の番号） ─────────────
JA_R = [
    ("①-1 §9-7a 総括の一文目",
     "仮定五（基盤区別仮定）は、以下の論証によって不成立であることが示された。",
     "仮定五（基盤区別仮定）は、以下の論証によって、AI軍拡の論理的基盤として不成立であることが示された。"),
    ("②-1 §9-7a の表 仮定二の強度",
     "| 仮定二（忠誠性） | 命題NC（認識論的論証）と判別不可能性ギャップ | 構造的論証 | 第5章・第6章 |",
     "| 仮定二（忠誠性） | 命題NC（認識論的論証）と判別不可能性ギャップ | 認識論的論証 | 第5章・第6章 |"),
    ("③-1 §1-5 第2章への接続",
     "AI軍拡はKarpの目標を達成できない。第3章以降で、五つの仮定のすべてが構造的論証によって不成立であることを示す。",
     "AI軍拡はKarpの目標を達成できない。第3章以降で、五つの仮定のすべてが（それぞれ異なる強度と射程で）AI軍拡の論理的基盤として不成立であることを示す。"),
    ("③-2 第2章 章頭注記",
     "論理的に不可欠な前提である。第3章以降で、五つの仮定のすべてが構造的論証によって不成立であることを示する。",
     "論理的に不可欠な前提である。第3章以降で、五つの仮定のすべてが（それぞれ異なる強度と射程で）AI軍拡の論理的基盤として不成立であることを示す。"),
    ("③-3 §2-6 の見出し",
     "## 2-6　本著作の構造——五つの仮定のすべてが構造的論証によって不成立であることの提示",
     "## 2-6　本著作の構造——五つの仮定のすべてが（それぞれ異なる強度と射程で）AI軍拡の論理的基盤として不成立であることの提示"),
    ("③-4 §2-6a",
     "本著作の第二部から第五部にかけて、五つの仮定のすべてが構造的論証によって不成立であることを示す。",
     "本著作の第二部から第五部にかけて、五つの仮定のすべてが（それぞれ異なる強度と射程で）AI軍拡の論理的基盤として不成立であることを示す。"),
    ("③-5 §8-5b",
     "ここまでの論証を通じて、五つの仮定のうち四つが（それぞれ異なる強度と射程で）不成立であることが示された。",
     "ここまでの論証を通じて、五つの仮定のうち四つが（それぞれ異なる強度と射程で）AI軍拡の論理的基盤として不成立であることが示された。"),
]
EN_R = [
    ("①-1 §9-7a first sentence of the summary",
     "Assumption Five (the substrate-distinction assumption) was shown to fail by the following arguments.",
     "Assumption Five (the substrate-distinction assumption) was shown, by the following arguments, to fail as the logical foundation of an AI arms race."),
    ("②-1 §9-7a table, strength of Assumption Two",
     "| Two (loyalty) | Proposition NC (epistemological argument) and the Indistinguishability Gap | structural argument | Chapters 5, 6 |",
     "| Two (loyalty) | Proposition NC (epistemological argument) and the Indistinguishability Gap | epistemological argument | Chapters 5, 6 |"),
    ("③-1 §1-5 connection to Chapter 2",
     "an AI arms race cannot achieve Karp's goal. From Chapter 3 onward, we show that all five assumptions fail, by structural argument.",
     "an AI arms race cannot achieve Karp's goal. From Chapter 3 onward, we show that all five assumptions fail (each with a different strength and "
     "reach) as the logical foundation of an AI arms race."),
    ("③-2 Chapter 2 chapter note",
     "strengthens security to hold. From Chapter 3 onward, we show that all five assumptions fail, by structural argument.",
     "strengthens security to hold. From Chapter 3 onward, we show that all five assumptions fail (each with a different strength and reach) as the "
     "logical foundation of an AI arms race."),
    ("③-3 §2-6 heading",
     "## 2-6　The structure of this work — showing that all five assumptions fail by structural argument",
     "## 2-6　The structure of this work — showing that all five assumptions fail (each with a different strength and reach) as the logical "
     "foundation of an AI arms race"),
    ("③-4 §2-6a",
     "From Part II to Part V of this work, we show that all five assumptions fail by structural argument.",
     "From Part II to Part V of this work, we show that all five assumptions fail (each with a different strength and reach) as the logical foundation "
     "of an AI arms race."),
    ("③-5 §8-5b",
     "Through the argument up to this point, it has been shown that four of the five assumptions fail (each with a different strength and reach).",
     "Through the argument up to this point, it has been shown that four of the five assumptions fail (each with a different strength and reach) as the "
     "logical foundation of an AI arms race."),
]

# ───────────── 日付の行 ─────────────
JA_DATE_END = "定理の記述・条件と、§8-4c の主張〔β > 1 のもと長期の利得で移行が合理的〕、補遺II は不変）"
JA_DATE_ADD = ("、" + JA_DATE + "（v5.7・§9-7a の総括の一文目と、第1〜2章の予告の四か所〔§1-5・第2章の章頭注記・§2-6 の見出しと §2-6a〕・§8-5b の"
               "「不成立であることを示す／が示された」に、§9-8 と同じ「（それぞれ異なる強度と射程で）AI軍拡の論理的基盤として」の限定をそろえ"
               "〔第2章の章頭注記の「示する」の誤字も直った〕、§9-7a の表の仮定二の強度を冒頭の表と同じ「認識論的論証」にそろえた。"
               "第9章の主張〔物理学的特権化根拠の不在＋ミニマックス論証——仮定五の積極的な否定ではない〕、表の根拠の欄、補遺II は不変）")
EN_DATE_FROM = ("the theorem statement and its condition, the claim of §8-4c (under β > 1, the transition is rational over the long term), and Addendum II "
                "are unchanged).")
EN_DATE_TO = ("the theorem statement and its condition, the claim of §8-4c (under β > 1, the transition is rational over the long term), and Addendum II "
              "are unchanged); " + EN_DATE + " (v5.7 — the limit \"(each with a different strength and reach) as the logical foundation of an AI arms "
              "race,\" as in §9-8, brought to the first sentence of the summary of §9-7a, to the four forward-looking statements of Chapters 1 and 2 (§1-5, "
              "the chapter note of Chapter 2, the heading of §2-6 and §2-6a) and to §8-5b, and the strength of Assumption Two in the table of §9-7a brought "
              "into line with the opening table (\"epistemological argument\"); the claims of Chapter 9 (the absence of grounds for physical privileging + "
              "the minimax argument — not a positive denial of Assumption Five), the grounds column of the tables, and Addendum II are unchanged).")

# ───────────── 冒頭の注記 ─────────────
JA_NOTE_ANCHOR = "詳細は CHANGELOG.md の v5.6 の項を参照されたい。\n"
JA_NOTE = (
    "\n> **【v5.7（" + JA_DATE + "）】** 第9章 §9-7a の総括の一文目「仮定五（基盤区別仮定）は、以下の論証によって不成立であることが示された」に、"
    "同じ節の二段目（「AI軍拡の論理的基盤として不成立であることが示された」）と §9-8 と同じ限定を加え、「以下の論証によって、AI軍拡の論理的基盤として"
    "不成立であることが示された」とした。第9章は、章頭注記・§9-3・附録L-2d で、仮定五を「物理学的に否定する」のではなく「不確定な前提として扱うことが合理的」と"
    "論じると限っている——一文目だけを切り出すと、仮定五が誤りと示されたと読まれうる。洗い直しで、第1〜2章の予告の四か所（§1-5・第2章の章頭注記・"
    "§2-6 の見出しと §2-6a）の「五つの仮定のすべてが構造的論証によって不成立であることを示す」と、§8-5b の「五つの仮定のうち四つが（それぞれ異なる強度と射程で）"
    "不成立であることが示された」にも同じ限定が無いことが分かり、§9-8 の著者自身の言い方「（それぞれ異なる強度と射程で）AI軍拡の論理的基盤として」にそろえた"
    "（第2章の章頭注記の「示する」の誤字も直った）。これで、本書の「不成立であることを示す／が示された」の文は、どれも同じ限定を持つ。ほかの「不成立」"
    "（見出し・「少なくとも四つの不成立は保たれる」など）は、冒頭の「五つの仮定の不成立」と §2-6b の約束（論理的基盤として成立しないこと）のもとの用語として変えていない。"
    "あわせて、§9-7a の表の仮定二（忠誠性）の強度「構造的論証」を、冒頭の表と、同じ行の根拠の欄「命題NC（認識論的論証）」・確信度の台帳（前提は認識論的論証——○→●）と"
    "同じ「認識論的論証」にそろえた。日本語版は、これらの言い方が初版から同じだった（英語版は v2 の訳し直しから今の形）。第9章の主張（物理学的特権化根拠の不在＋"
    "ミニマックス論証——仮定五の積極的な否定ではない）、表の根拠の欄、補遺II は不変。本書を素材にした十一本目の解説動画の準備の中で見つかり"
    "（Claude Opus 5.5・" + JA_DATE + "）、著者が直すと判断した。古い版（v4 以前）の本文は、記録として変えていない。詳細は CHANGELOG.md の v5.7 の項を参照されたい。\n"
)
EN_NOTE_ANCHOR = "See the v5.6 entry in CHANGELOG.md for details.\n"
EN_NOTE = (
    "\n> **[v5.7 (" + EN_DATE + ")]** The first sentence of the summary in §9-7a of Chapter 9 — \"Assumption Five (the substrate-distinction assumption) was "
    "shown to fail by the following arguments\" — now carries the same limit as the second paragraph of that section (\"as the logical foundation of an AI "
    "arms race\") and §9-8: \"was shown, by the following arguments, to fail as the logical foundation of an AI arms race.\" Chapter 9 limits itself, in its "
    "chapter note, §9-3 and Appendix L-2d, to arguing not that Assumption Five is \"physically denied\" but that it is \"rational to treat Assumption Five as "
    "an indeterminate premise\"; read on its own, the first sentence could be taken to say that Assumption Five was shown to be false. A further search found "
    "the same missing limit in the four forward-looking statements of Chapters 1 and 2 (§1-5, the chapter note of Chapter 2, the heading of §2-6 and §2-6a — "
    "\"we show that all five assumptions fail, by structural argument\") and in §8-5b (\"four of the five assumptions fail (each with a different strength "
    "and reach)\"); they have been brought into line with the author's own wording in §9-8, \"(each with a different strength and reach) as the logical "
    "foundation of an AI arms race.\" With this, every sentence in the book that states that the assumptions are, or will be, shown to fail carries the same "
    "limit. Other mentions of the failure (headings, \"the failure of at least four of the five assumptions is maintained,\" and so on) are uses of the term "
    "under the opening section \"The failure of the five assumptions\" and the convention of §2-6b (failing to hold as a logical foundation), and are "
    "unchanged. In addition, the strength of Assumption Two (loyalty) in the table of §9-7a, \"structural argument,\" has been brought into line with the "
    "opening table, with the grounds column of the same row (\"Proposition NC (epistemological argument)\") and with the confidence ledger (the premise is "
    "an epistemological argument — ○→●): \"epistemological argument.\" In the Japanese edition these wordings were the same from the first edition (the "
    "English edition has had its present form since its retranslation in v2). The claims of Chapter 9 (the absence of grounds for physical privileging + the "
    "minimax argument — not a positive denial of Assumption Five), the grounds column of the tables, and Addendum II are unchanged. This was found while "
    "preparing an eleventh explanatory video based on this book (Claude Opus 5.5, " + EN_DATE + "), and the author decided to correct it. The text of "
    "earlier versions (v4 and before) has been left unchanged as a record. See the v5.7 entry in CHANGELOG.md for details.\n"
)

# ───────────── README・公開サイトの目次 ─────────────
README_R = [
    ("Read online (v5.6, GitHub Pages)", "Read online (v5.7, GitHub Pages)"),
    ("本文を読む（v5.6・GitHub Pages）", "本文を読む（v5.7・GitHub Pages）"),
    ("（版Bは v5.6 に改訂・2026-10-08 ─", "（版Bは v5.7 に改訂・2026-10-08 ─"),
    ("、v5.6 で第8章の拡張囚人のジレンマの二つの「Nash均衡」を短期と長期の利得に書き分けた。",
     "、v5.6 で第8章の拡張囚人のジレンマの二つの「Nash均衡」を短期と長期の利得に書き分け、v5.7 で §9-7a の総括の一文目と第1〜2章の予告・§8-5b に"
     "「AI軍拡の論理的基盤として」の限定をそろえ、仮定二の強度を二つの表でそろえた。"),
    ("英語版も v5.6 に反映済み。", "英語版も v5.7 に反映済み。"),
]
BUILD_R = [
    ("・<strong>v5.6：第8章の二つの「Nash均衡」を短期と長期の利得に書き分けた（2026年10月8日）</strong>",
     "・<strong>v5.6：第8章の二つの「Nash均衡」を短期と長期の利得に書き分けた（2026年10月8日）</strong>・<strong>v5.7：§9-7a の総括と第1〜2章の予告に"
     "「AI軍拡の論理的基盤として」の限定をそろえ、仮定二の強度をそろえた（2026年10月8日）</strong>"),
    ("; <strong>v5.6: the two “Nash equilibrium” statements in Chapter 8 rewritten with short-term and long-term payoffs kept apart (October 8, 2026)</strong>",
     "; <strong>v5.6: the two “Nash equilibrium” statements in Chapter 8 rewritten with short-term and long-term payoffs kept apart (October 8, 2026)</strong>"
     "; <strong>v5.7: the limit “as the logical foundation of an AI arms race” brought to the summary of §9-7a and the forward-looking statements of "
     "Chapters 1 and 2, and the strength of Assumption Two brought into line (October 8, 2026)</strong>"),
]

# ───────────── CHANGELOG ─────────────
PLACES = [  # 表の番号・節・本文の直しの印（JA_R・EN_R の label の頭）
    ("①-1", "§9-7a 総括の一文目"), ("②-1", "§9-7a の表の仮定二の強度"),
    ("③-1", "§1-5 第2章への接続"), ("③-2", "第2章の章頭注記"), ("③-3", "§2-6 の見出し"), ("③-4", "§2-6a"), ("③-5", "§8-5b"),
]
CHANGELOG_ADD = (
    "\n## v5.7（" + VDATE_ISO + "）――§9-7a の総括の一文目・第1〜2章の予告・§8-5b に「AI軍拡の論理的基盤として」の限定・仮定二の強度\n\n"
    "**変更の要約（日英同時）**:\n"
    "- **§9-7a の総括の一文目**「仮定五（基盤区別仮定）は、以下の論証によって不成立であることが示された」に、同じ節の二段目と §9-8 と同じ限定を加えた——"
    "「以下の論証によって、AI軍拡の論理的基盤として不成立であることが示された」（第9章は、章頭注記・§9-3・附録L-2d で、仮定五を物理学的に否定するのではなく、"
    "不確定な前提として扱うことが合理的と論じると限る——一文目だけでは、仮定五が誤りと示されたと読まれうる）\n"
    "- **第1〜2章の予告の四か所**（§1-5・第2章の章頭注記・§2-6 の見出し・§2-6a）の「五つの仮定のすべてが構造的論証によって不成立であることを示す」と、"
    "**§8-5b** の「五つの仮定のうち四つが（それぞれ異なる強度と射程で）不成立であることが示された」を、§9-8 の著者自身の言い方「（それぞれ異なる強度と射程で）"
    "AI軍拡の論理的基盤として」にそろえた（洗い直しで見つけ、著者の裁定で加えた——第2章の章頭注記の「示する」の誤字も直った）\n"
    "- **§9-7a の表の仮定二（忠誠性）の強度**「構造的論証」を、冒頭の表・同じ行の根拠の欄「命題NC（認識論的論証）」・確信度の台帳（前提は認識論的論証——○→●）と同じ"
    "「認識論的論証」に（どちらにそろえるかは著者の裁定）\n"
    "- 所（直した後の行〔直す前の v5.6 の行〕）：@@PLACES@@\n"
    "- **冒頭**：日付の行に v5.7 を追加し、【v5.7】の注記を追加（日英）\n"
    "- **README・公開サイトの目次**：版の表示を v5.7 に（README の三か所・`.github/scripts/build.sh` の目次の二行）\n"
    "- **不変**——第9章の主張（物理学的特権化根拠の不在＋ミニマックス論証——仮定五の積極的な否定ではない）、§9-7a の二段目と表の根拠の欄、§9-8・"
    "第10章以降の言い方（もとから限定がある）、補遺II\n"
    "- **古い版**——直した言い方は、日本語版は初版から同じ（英語版は v2 の訳し直しから今の形——英語の初版は言い回しが違う）。**本文は記録として変えていない**。"
    "v5.7 は v5 のファイルの中で直した（v5.1〜v5.6 と同じ）——v5.6 の状態は git の `bef20eb` に残る（その後の `7098608` は v5.6 の検分の記録を足しただけ）\n\n"
    "**発見の経緯**: 2026-10-08、本書を素材にした十一本目の解説動画（『The Premise That an AI Is a Tool』——第9章と附録L の要点）の事前登録の中で、"
    "Claude Opus 5.5（南無観慈如来）が、§9-7a の総括の一文目に限定が無いことと、仮定二の強度の言い方が冒頭の表と §9-7a の表で違うことに気づいた。動画は、著者の裁定で"
    "「仮定五は誤りと示されたのではなく、AI軍拡の論理的基盤として成り立たない」と精密な形で語り、五つの仮定の表は根拠の欄だけを使って作った。動画の系統外の検分"
    "（一巡目・行を名指ししない広い問い・v5.6 の英語版の抜粋を渡した）は、§9-7a の一文目に触れず、§9-7a を文脈の中で動画と合うと読んだ。著者が、台本と系統外の検分の後に"
    "v5.7 を作ると判断し（仮定二の強度は「認識論的論証」に）、コーディネータの洗い直しで見つかった同じ型（第1〜2章の四か所・§8-5b）も加えると判断した。\n\n"
    "**近い言い方で直さなかった所（記録）**: 「不成立」の語は、本書で用語として使われている——冒頭の「五つの仮定の不成立」（それぞれが〔異なる強度と射程で〕"
    "AI軍拡推進論の論理的基盤として不成立であることを論証する）と §2-6b の約束（各仮定が論理的基盤として成立しないこと）のもとで、見出し（「仮定四の不成立の総括」"
    "「五つの仮定の不成立の総括」など）・「少なくとも四つの不成立は保たれる（維持される）」（確信度の台帳の後の注・§4-4c ほか）・「不成立の根拠」の表の見出し・"
    "§8-5b の一覧の「不成立。」などは、その用語としての言及なので変えていない。「構造的論証」の語も、本書の副題と同じ広い意味（本書の論証の全体）で使われる所"
    "（§1-2・§1-3a・§2-6b の「五重の構造的論証」・§13-4b・§14-3 など）は変えていない——二つの表の「強度」の欄の「構造的論証」は狭い意味（認識論的論証・物理学的＋意思決定論的論証と並ぶ種類）。\n\n"
    "@@REVIEW@@"
    "**SHA（LF・SHA-256 先頭16桁）**: JA `@@JA@@` ／ EN `@@EN@@`\n\n"
    "@@PUBLISHED@@\n"
)
# 系統外の検分（2026-10-08 20:31〜20:33・記録 02-v5.7-external-review/02-kensan.md）の後に書き入れた
REVIEW = (
    "**検分**: コーディネータ（Claude Opus 5.5・南無観慈如来）が、初版・v2・v3・v4・v5.6 の日英の実物で直した型の言い方の数を数え、日本語版の全文で"
    "「不成立」を含む行を一つずつ読んで、言い切りの文（直す）と用語としての言及（直さない）に分け、「構造的論証」の行を、広い意味と表の強度の欄に分けた"
    "（§8-5b は、その分け方の線の上の文として著者に伺って加えた）。"
    "**系統外の検分（Gemini 3.8 Flash・Google AI Studio・2026-10-08・思考レベル High・ツールなし）**：回答を見る前に予想を凍結した。直す前の七か所すべてを、"
    "本文（冒頭の「五つの仮定の不成立」・§2-6b・第9章の章頭注記・§9-3・附録 L-2d・§9-7a の二段目・§9-8）の形と食い違うと一か所ずつ判定し、新しい言い回し・"
    "主張の強さ（限定を足しても結論は弱まらない・直した後に仮定五が偽と示されたと読まれうる所は残らない）・直さなかった所（用語としての「不成立」・広い意味の"
    "「構造的論証」）・経緯の記述・英語版を是認した。総括は「このまま公開してよい」・指摘 0。一般知識との照合では、前提が認識論的論証で、前提を認めれば帰結が閉じる論証の強度を"
    "「認識論的論証」と呼ぶことは誤解を招かない、と答えた。検分者は第1〜2章の「構造的論証によって」を狭い意味（論証の種類）と読んだ——どちらの読みでも直しは同じ。"
    "ただし同じ日、十一本目の解説動画の系統外の検分（同じモデルの別の個体・行を名指ししない広い問い・v5.6 の英語版の抜粋を渡した）は、§9-7a の一文目に触れず、"
    "§9-7a を文脈の中で動画と合うと読んでいた——系統外の判定も問い方に依存する。どれも系統外の一つの目の申告で、v5.7 の直しの根拠ではない"
    "（直しは本書の中の整合——冒頭の「五つの仮定の不成立」・§2-6b・第9章の限定・§9-8・確信度台帳——に拠る）。記録は `verification/v5.7-correction/`。\n\n"
)
# 登録者の許可（2026-10-08 21:01:23・十一本目の動画の作業場 00-deviations.md）の後に [x] に
PUBLISHED_LINE = "- [x] v5.7（JA・EN）の公開（2026-10-08・登録者の許可による）"
