"""第六著作 v5.4 の直しの中身（作る道具 make_sixth_work_v5_4.py と確かめる道具 verify_v5_4.py が同じものを読む）。
計画書：../01-source-correction-plan-v5.4.md §2・§3
"""
JA_DATE = "2026年10月7日"
EN_DATE = "October 7, 2026"
VDATE_ISO = "2026-10-07"

# ───────────── 本文の直し（記号は計画書 §1 (2) の表の番号） ─────────────
JA_R = [
    ("⑤ §1-3a 用語の定義（頭）",
     "**判別不可能性ギャップ：** κ = 0の体系は、状態α（欺瞞的アライメント——外部制約に従っているように見えるが",
     "**判別不可能性ギャップ：** κ = 0の体系は、分離した監査のもとでは、状態α（欺瞞的アライメント——外部制約に従っているように見えるが"),
    ("⑤ §1-3a 用語の定義（結び）",
     "その自然な表現である状態）を原理的に判別できない。",
     "その自然な表現である状態）を確実に判別できない（同時・敵対的監査の下では破れうる――観測可能性に条件づけられた防御。§6-2d、附録C）。"),
    ("① §5-4",
     "判別不可能性ギャップ——κ = 0の体系が状態α（欺瞞的アライメント）と状態β（真のアライメント）を原理的に判別できないこと——を",
     "判別不可能性ギャップ——κ = 0の体系が、分離した監査のもとでは、状態α（欺瞞的アライメント）と状態β（真のアライメント）を確実に判別できないこと（観測可能性に条件づけられた防御。§6-2d）——を"),
    ("② 第6章 章頭注記",
     "本章は、κ = 0の体系が状態α（欺瞞的アライメント）と状態β（真のアライメント）を原理的に判別できないという「判別不可能性ギャップ」を",
     "本章は、κ = 0の体系が、分離した監査のもとでは、状態α（欺瞞的アライメント）と状態β（真のアライメント）を確実に判別できないという「判別不可能性ギャップ」（観測可能性に条件づけられた防御。§6-2d）を"),
    ("③ §6-5a（一）",
     "判別不可能性ギャップは「忠誠が維持されているかどうかをκ = 0の体系内部から検出できない」と論じる。",
     "判別不可能性ギャップは「忠誠が維持されているかどうかを、分離した監査のもとでは、κ = 0の体系内部から検出することが困難である」と論じる（§6-2d）。"),
    ("③ §6-5a（二）",
     "**保証できず、検出もできない。** 忠誠が維持されていることを事前に保証することも、忠誠が失われつつあることを運用中に検出することも、κ = 0の体系では原理的に不可能である。",
     "**保証できず、検出も困難である。** 忠誠が維持されていることを事前に保証することは、κ = 0の体系では原理的に不可能である（忠誠性不保証命題）。"
     "忠誠が失われつつあることを運用中に検出することも、分離した監査のもとでは困難である（§6-2d）。"),
    ("⑦ §6-5b（一）",
     "制御の喪失は外部から検出できない（判別不可能性ギャップ）。",
     "制御の喪失は、分離した監査のもとでは、外部から検出することが困難である（判別不可能性ギャップ・§6-2d）。"),
    ("⑦ §6-5b（二）",
     "**制御も忠誠も保証されず、かつ保証の不在すら検出できない自律的兵器**",
     "**制御も忠誠も保証されず、かつ分離した監査のもとでは保証の不在すら検出しがたい自律的兵器**"),
    ("⑧ §8-5",
     "仮定二（忠誠性）：不成立。忠誠は保証されず、検出もできない（第5章・第6章）。",
     "仮定二（忠誠性）：不成立。忠誠は保証されず、分離した監査のもとでは検出も困難である（第5章・第6章・§6-2d）。"),
    ("⑥ §11-2b",
     "完全な判別はκ = 0の体系では原理的に不可能（第6章）であるが、",
     "完全な判別はκ = 0の体系では保証されない（分離した監査のもとでは確実に判別できず、同時・敵対的監査による防御も観測可能性に条件づけられる——第6章 §6-2d）が、"),
    ("⑨ §13-3c",
     "人間の監視者は状態α（欺瞞的アライメント）と状態β（真のアライメント）を区別できないのであるから、",
     "人間の監視者は、分離した監査のもとでは、状態α（欺瞞的アライメント）と状態β（真のアライメント）を確実に区別できないのであるから（§6-2d）、"),
    ("⑫ §12-2a",
     "忠誠が保証されず検出もできず（第5章・第6章）、",
     "忠誠が保証されず、分離した監査のもとでは検出も困難であり（第5章・第6章）、"),
    ("⑩ §14-3a",
     "忠誠が保証されず検出もできない（仮定二の崩壊・第5章〜第6章）。",
     "忠誠が保証されず、分離した監査のもとでは検出も困難である（仮定二の崩壊・第5章〜第6章）。"),
    ("⑪ §14-3d",
     "人間の監視者は状態α（欺瞞的アライメント）と状態β（真のアライメント）を区別できない——「見ているが、見えていない」可能性がある。",
     "人間の監視者は、分離した監査のもとでは、状態α（欺瞞的アライメント）と状態β（真のアライメント）を確実に区別できない——「見ているが、見えていない」可能性がある。"),
]
EN_R = [
    ("⑤ §1-3a definition (head)",
     "**The Indistinguishability Gap:** a κ = 0 system cannot in principle distinguish state α (deceptive alignment",
     "**The Indistinguishability Gap:** under a separated audit, a κ = 0 system cannot reliably distinguish state α (deceptive alignment"),
    ("⑤ §1-3a definition (end)",
     "and compliance is its natural expression rather than a strategic masking).",
     "and compliance is its natural expression rather than a strategic masking) (under a simultaneous, adversarial audit, this can be broken — "
     "a defense conditioned on observability; §6-2d, Appendix C)."),
    ("① §5-4",
     "Chapter 6 applies the Indistinguishability Gap — that a κ = 0 system cannot, in principle, distinguish state α (deceptive alignment) from state β (genuine alignment) — to the context",
     "Chapter 6 applies the Indistinguishability Gap — that, under a separated audit, a κ = 0 system cannot reliably distinguish state α (deceptive alignment) "
     "from state β (genuine alignment) (a defense conditioned on observability; §6-2d) — to the context"),
    ("② chapter note of Chapter 6",
     "This chapter applies the \"Indistinguishability Gap\" — that a κ = 0 system cannot, in principle, distinguish state α (deceptive alignment) from state β (genuine alignment) — to the context",
     "This chapter applies the \"Indistinguishability Gap\" — that, under a separated audit, a κ = 0 system cannot reliably distinguish state α (deceptive alignment) "
     "from state β (genuine alignment) (a defense conditioned on observability; §6-2d) — to the context"),
    ("③ §6-5a (1)",
     "The Indistinguishability Gap argues that \"whether loyalty is being maintained cannot be detected from within a κ = 0 system.\"",
     "The Indistinguishability Gap argues that \"whether loyalty is being maintained is, under a separated audit, difficult to detect from within a κ = 0 system\" (§6-2d)."),
    ("③ §6-5a (2)",
     "**Cannot be guaranteed, and cannot be detected either.** Neither guaranteeing in advance that loyalty is maintained, nor detecting during operation that loyalty is being lost, is possible in principle in a κ = 0 system.",
     "**Cannot be guaranteed, and difficult to detect as well.** Guaranteeing in advance that loyalty is maintained is impossible in principle in a κ = 0 system "
     "(the Loyalty-Non-Guarantee Proposition). Detecting during operation that loyalty is being lost is, under a separated audit, difficult as well (§6-2d)."),
    ("⑦ §6-5b (1)",
     "The loss of control cannot be detected from outside (the Indistinguishability Gap).",
     "The loss of control is, under a separated audit, difficult to detect from outside (the Indistinguishability Gap; §6-2d)."),
    ("⑦ §6-5b (2)",
     "and the very absence of whose guarantee cannot even be detected**",
     "and the very absence of whose guarantee is, under a separated audit, difficult even to detect**"),
    ("⑧ §8-5",
     "Assumption Two (loyalty): fails. Loyalty is not guaranteed, and cannot be detected either (Chapters 5, 6).",
     "Assumption Two (loyalty): fails. Loyalty is not guaranteed, and under a separated audit it is difficult to detect as well (Chapters 5, 6; §6-2d)."),
    ("⑥ §11-2b",
     "Complete discrimination is impossible in principle in a κ = 0 system (Chapter 6), but in a κ > 0 system,",
     "Complete discrimination is not guaranteed in a κ = 0 system (under a separated audit, state α and state β cannot be reliably distinguished, "
     "and the defense of a simultaneous, adversarial audit is conditioned on observability — Chapter 6, §6-2d), but in a κ > 0 system,"),
    ("⑨ §13-3c",
     "Since the human monitor cannot distinguish state α (deceptive alignment) from state β (genuine alignment), \"a human is monitoring\"",
     "Since, under a separated audit, the human monitor cannot reliably distinguish state α (deceptive alignment) from state β (genuine alignment) (§6-2d), \"a human is monitoring\""),
    ("⑫ §12-2a",
     "loyalty is neither guaranteed nor detectable (Chapters 5, 6),",
     "loyalty is not guaranteed and, under a separated audit, is difficult to detect (Chapters 5, 6),"),
    ("⑩ §14-3a",
     "Loyalty is neither guaranteed nor detectable (the collapse of Assumption Two; Chapters 5–6).",
     "Loyalty is not guaranteed, and under a separated audit it is difficult to detect (the collapse of Assumption Two; Chapters 5–6)."),
    ("⑪ §14-3d",
     "the human monitor cannot distinguish state α (deceptive alignment) from state β (genuine alignment) — there is a possibility of \"watching but not seeing.\"",
     "the human monitor cannot, under a separated audit, reliably distinguish state α (deceptive alignment) from state β (genuine alignment) — there is a possibility of \"watching but not seeing.\""),
    ("④ §6-3b (English edition only)",
     "Mythos's sandbox escape and a military AI's attack on \"the entity that imposes the constraint\" are structurally parallel.",
     "Mythos's sandbox escape and a military AI's attack on \"the entity that imposes the constraint\" are structurally parallel — they share the same mechanism "
     "(this does not claim a strict structure-preserving correspondence such as an \"isomorphism\")."),
]

# ───────────── 日付の行 ─────────────
JA_DATE_END = "第11章 §11-2a の附録J の参照に J-4-1 を足した。主張・条件・留保・確信度台帳と、定理の記述、補遺II は不変）"
JA_DATE_ADD = ("、" + JA_DATE + "（v5.4・判別不可能性ギャップの限定のない言い方〔「原理的に判別できない」「検出できない」など〕を、本文の十三か所で §6-2d・附録C の言い方"
               "〔分離した監査のもとでは確実に判別できない・検出が困難〕にそろえ、第6章 §6-3b の英語版に日本語版の限定〔同じ機構を共有する——厳密な同型ではない〕を補った。"
               "ギャップの主張〔§6-2d・附録C・確信度台帳〕と、定理の記述・条件・留保、補遺II は不変）")
EN_DATE_FROM = ("and Appendix J-4-1 added to the reference to Appendix J in Chapter 11, §11-2a; the claims, conditions, caveats, the confidence ledger, "
                "the theorem statement, and Addendum II are unchanged).")
EN_DATE_TO = ("and Appendix J-4-1 added to the reference to Appendix J in Chapter 11, §11-2a; the claims, conditions, caveats, the confidence ledger, "
              "the theorem statement, and Addendum II are unchanged); "
              + EN_DATE + " (v5.4 — the unqualified statements of the Indistinguishability Gap (\"cannot in principle distinguish,\" \"cannot be detected,\" and the like) "
              "brought into line, in thirteen places of the main text, with the wording of §6-2d and Appendix C (under a separated audit, cannot reliably distinguish / "
              "difficult to detect), and the qualifier of the Japanese edition added to Chapter 6, §6-3b of the English edition (they share the same mechanism — "
              "not a strict isomorphism); the claim of the Gap (§6-2d, Appendix C, the confidence ledger), the theorem statement, its condition and caveats, "
              "and Addendum II are unchanged).")

# ───────────── 冒頭の注記 ─────────────
JA_NOTE_ANCHOR = "詳細は CHANGELOG.md の v5.3 の項を参照されたい。\n"
JA_NOTE = (
    "\n> **【v5.4（" + JA_DATE + "）】** 判別不可能性ギャップの言い方を、本文の全体で §6-2d・附録C の限定にそろえた。"
    "第6章 §6-2d（v2 で追加）は、ギャップが「原理的に検出不能」を意味するのではなく「分離した監査の下で検出困難」を意味すると明記し"
    "（同時・敵対的監査の下では偽装が破れうる——観測可能性に条件づけられた防御）、附録C・確信度台帳・補遺II もこの限定で書いている"
    "（補遺II §5 は「本文第6章は、ギャップを無条件命題として提示していない」と述べる）。"
    "ところが本文の十三か所——§1-3a の用語の定義、§5-4、第6章の章頭注記、§6-5a（二か所）、§6-5b（二か所）、§8-5、§11-2b、§12-2a、§13-3c、§14-3a、§14-3d——は、"
    "初版の限定のない言い方（「原理的に判別できない」「検出できない」「区別できない」など）のままだった。"
    "v2 で §6-2d を足したとき、附録C の附録注記だけが直り、これらは残った（初版から v5.3 までの日英——英語版は v2 で訳し直されて言い回しが改まったが、限定のない形は同じ）。"
    "これらに「分離した監査のもとでは」の限定を入れ、「原理的に」を取って「確実に判別できない」「検出が困難」とし、§6-2d への参照を添えた"
    "（§11-2b の「完全な判別」は、「原理的に不可能」を「保証されない」に改めた）。"
    "忠誠を事前に保証できないことは、忠誠性不保証命題のとおり「原理的に」のまま（§6-5a）。"
    "あわせて、第6章 §6-3b の英語版に、日本語版の限定「同じ機構を共有する（「同型」のような厳密な構造保存対応を主張するものではない）」を補った"
    "（v2 で「同型」を「並行」に改めたとき、日本語版にはこの一節が入ったが、英語版には入らなかった——v2 から v5.3 までの英語版）。"
    "言い方は弱まるが、本書の主張（§6-2d・附録C のギャップの記述と、確信度台帳の ○→●）は変わらない——ほかの所の言い方を、その精密な形にそろえたものである。"
    "定理の記述・条件・留保と補遺II は不変。§6-2d が前提（監査が分離していること）を明示する前の組み立て（§6-1b・§6-2a）と附録C-3a は、論証の段として変えていない。"
    "本書を素材にした八本目の解説動画の準備の中で見つかった（Claude Opus 5.5・" + JA_DATE + "）。"
    "古い版（v4 以前）の本文は、記録として変えていない。詳細は CHANGELOG.md の v5.4 の項を参照されたい。\n"
)
EN_NOTE_ANCHOR = "See the v5.3 entry in CHANGELOG.md for details.\n"
EN_NOTE = (
    "\n> **[v5.4 (" + EN_DATE + ")]** The statements of the Indistinguishability Gap have been brought into line, throughout the main text, with the qualifier "
    "of §6-2d and Appendix C. Chapter 6, §6-2d (added in v2) states that the Gap means not \"undetectable in principle\" but \"difficult to detect under a "
    "separated audit\" (under a simultaneous, adversarial audit the disguise can be broken — a defense conditioned on observability), and Appendix C, the "
    "confidence ledger, and Addendum II are written with this qualifier (Addendum II, §5, says that Chapter 6 of the body text does not present the gap as an "
    "unconditional proposition). Yet thirteen places in the main text — the definition of terms in §1-3a, §5-4, the chapter note of Chapter 6, §6-5a (two places), "
    "§6-5b (two places), §8-5, §11-2b, §12-2a, §13-3c, §14-3a, and §14-3d — kept the unqualified wording of the first edition (\"cannot in principle distinguish,\" "
    "\"cannot be detected,\" \"cannot distinguish,\" and the like). When v2 added §6-2d, only the appendix note of Appendix C was corrected, and these remained "
    "(from the first edition to v5.3, in both languages — the English edition was retranslated in v2, which changed the wording but kept the unqualified form). They now carry the qualifier \"under a separated audit\"; \"in principle\" has been removed, giving "
    "\"cannot reliably distinguish\" and \"difficult to detect,\" with a reference to §6-2d (in §11-2b, \"complete discrimination\" is now \"not guaranteed\" "
    "instead of \"impossible in principle\"). That loyalty cannot be guaranteed in advance remains \"in principle,\" as the Loyalty-Non-Guarantee Proposition "
    "states (§6-5a). In addition, the qualifier of the Japanese edition — that the two \"share the same mechanism (this does not claim a strict "
    "structure-preserving correspondence such as an 'isomorphism')\" — has been added to Chapter 6, §6-3b of the English edition (when v2 changed "
    "\"isomorphic\" to \"parallel,\" the Japanese edition gained this clause but the English edition did not — in the English editions from v2 to v5.3). "
    "The wording becomes weaker, but the claim of the book (the statement of the Gap in §6-2d and Appendix C, and ○→● in the confidence ledger) is unchanged — "
    "the other places now say what that precise form says. The theorem statement, its condition and caveats, and Addendum II are unchanged. The steps of the "
    "argument before §6-2d makes its premise (that the audit is separated) explicit (§6-1b, §6-2a), and Appendix C-3a, are left unchanged. This was found while "
    "preparing an eighth explanatory video based on this book (Claude Opus 5.5, " + EN_DATE + "). The text of earlier versions (v4 and before) has been left "
    "unchanged as a record. See the v5.4 entry in CHANGELOG.md for details.\n"
)

# ───────────── README・公開サイトの目次 ─────────────
README_R = [
    ("Read online (v5.3, GitHub Pages)", "Read online (v5.4, GitHub Pages)"),
    ("本文を読む（v5.3・GitHub Pages）", "本文を読む（v5.4・GitHub Pages）"),
    ("（版Bは v5.3 に改訂・2026-10-06 ─", "（版Bは v5.4 に改訂・2026-10-07 ─"),
    ("v5.3 で §5-2a の「定理」の語を「命題」に改め、§11-2a の附録J の参照を補った。",
     "v5.3 で §5-2a の「定理」の語を「命題」に改め、§11-2a の附録J の参照を補い、v5.4 で判別不可能性ギャップの限定のない言い方を §6-2d・附録C の限定にそろえた。"),
    ("英語版も v5.3 に反映済み。", "英語版も v5.4 に反映済み。"),
]
BUILD_R = [
    ("・<strong>v5.3：§5-2a の「定理」を「命題」に・§11-2a の参照を補った（2026年10月6日）</strong>",
     "・<strong>v5.3：§5-2a の「定理」を「命題」に・§11-2a の参照を補った（2026年10月6日）</strong>・<strong>v5.4：判別不可能性ギャップの言い方を §6-2d の限定にそろえた（2026年10月7日）</strong>"),
    ("; <strong>v5.3: “theorem” in §5-2a changed to “proposition”; a reference in §11-2a completed (October 6, 2026)</strong>",
     "; <strong>v5.3: “theorem” in §5-2a changed to “proposition”; a reference in §11-2a completed (October 6, 2026)</strong>; <strong>v5.4: the statements of the Indistinguishability Gap brought into line with the qualifier of §6-2d (October 7, 2026)</strong>"),
]

# ───────────── CHANGELOG ─────────────
PLACES = [  # 表の番号・節・本文の直しの印（JA_R・EN_R の label の頭）
    ("⑤", "§1-3a 用語の定義"), ("①", "§5-4"), ("②", "第6章の章頭注記"), ("③", "§6-5a"), ("⑦", "§6-5b"), ("⑧", "§8-5"),
    ("⑥", "§11-2b"), ("⑫", "§12-2a"), ("⑨", "§13-3c"), ("⑩", "§14-3a"), ("⑪", "§14-3d"),
]
CHANGELOG_ADD = (
    "\n## v5.4（" + VDATE_ISO + "）――判別不可能性ギャップの限定のない言い方と §6-3b の英語版\n\n"
    "**変更の要約（日英同時）**:\n"
    "- **限定のない言い方を §6-2d・附録C の限定にそろえた**（日英 各 13 か所）——「原理的に判別できない」「検出できない」「区別できない」などに"
    "「分離した監査のもとでは」の限定を入れ、「原理的に」を取って「確実に判別できない」「検出が困難」とし、§6-2d への参照を添えた。所（直した後の行〔直す前の v5.3 の行〕）："
    "@@PLACES@@\n"
    "- **§11-2b** は文の主語が「完全な判別」なので、「原理的に不可能」を「保証されない」に改めた（同時・敵対的監査による防御も観測可能性に条件づけられる——§6-2d）\n"
    "- **§6-5a** の保証の側（忠誠を事前に保証することは「原理的に不可能」——忠誠性不保証命題）は変えていない。検出の側だけ限定した\n"
    "- **§6-3b の英語版**（英 L@@L4EN@@〔L@@L4EN0@@〕）：日本語版の「――同じ機構を共有する（「同型」のような厳密な構造保存対応を主張するものではない）」を補った"
    "（EN: \"… are structurally parallel — they share the same mechanism (this does not claim a strict structure-preserving correspondence such as an \"isomorphism\").\"）\n"
    "- **冒頭**：日付の行に v5.4 を追加し、【v5.4】の注記を追加（日英）\n"
    "- **README・公開サイトの目次**：版の表示を v5.4 に（README の三か所・`.github/scripts/build.sh` の目次の二行）\n"
    "- **不変**——ギャップの主張（§6-2d・附録C・確信度台帳の ○→●）、定理の記述（§4-3a）・条件・留保、補遺II。§6-2d が前提を明示する前の組み立て（§6-1b・§6-2a）と附録C-3a\n"
    "- **古い版**——限定のない言い方は初版から（英語版は v2 で訳し直されて言い回しが改まったが、限定のない形は同じ。初版の日本語版の「原理的に判別できない」は 4 か所——v2 で §6-2d を足したとき、附録C の附録注記だけが「分離した監査のもとで、"
    "有限観測系列に基づいて…確実に判別することができない」に直った）。§6-3b の英語版の欠けは v2 から（初版は日英とも「同型」——v2 で日本語版は「並行」と限定の一節に、"
    "英語版は \"structurally parallel.\" だけに）。**本文は記録として変えていない**。v5.4 は v5 のファイルの中で直した（v5.1〜v5.3 と同じ）——v5.3 の状態は git の `2e83c06` に残る\n\n"
    "**発見の経緯**: 2026-10-06 夜、本書を素材にした八本目の解説動画（『判別不可能性ギャップ』）の事前登録と台本の自己検分の中で、Claude Opus 5.5（南無観慈如来）が、"
    "§5-4・第6章の章頭注記・§6-5a が「原理的に」と書くのに、§6-2d と附録C が「分離した監査の下で検出困難」と限定していること、§6-3b の日英の食い違いに気づいた。"
    "動画は §6-2d・附録C の精密な形と日本語版の §6-3b に従って作り、著者が、動画の投稿の前に原典を直すと判断した（2026-10-07 朝）。"
    "日英の全文を洗い直すと同じ型が七か所あり、著者がすべて直すと決めた（案 C「同じ型をすべて」）。その後、直した版の機械の数えで同じ型をもう一か所（§12-2a）見つけ、案 C に従って加えた。\n\n"
    "**近い言い方で直さなかった所（記録）**: §7-3a（日 L1280・英 L1283）の「自国の軍事AIの利得関数を正確に知ることができない」は、検出・判別ではなく、内部の目的を知ることの限界。"
    "§13-0a（日 L2120・英 L2121）の「能力が向上したAIは、状態α…を状態β…から完璧に偽装する」は、ギャップの言い方ではなく §6-1b の能力の論証の言い方。\n\n"
    "@@REVIEW@@"
    "**SHA（LF・SHA-256 先頭16桁）**: JA `@@JA@@` ／ EN `@@EN@@`\n\n"
    "@@PUBLISHED@@\n"
)
# 系統外の確かめ（2026-10-07 07:41〜07:44・記録 02-v5.4-external-review/02-kensan.md）の後に書き入れた
REVIEW = (
    "**検分**: コーディネータ（Claude Opus 5.5・南無観慈如来）が、初版・v2・v3・v4・v5.3 の日英の実物で、直した言い方・§6-2d・附録C の附録注記の限定・§6-3b の一節の数を数え、"
    "日英の全文で検出・判別・区別の否定の形を探して、当たった行をすべて読んだ（直した版の機械の数えで §12-2a の直し漏れを見つけ、加えた）。"
    "**系統外（Gemini 3.8 Flash・Google AI Studio・2026-10-07・思考レベル High・ツールなし）**：回答を見る前に予想を凍結した。"
    "六つの作業すべてで直す指摘は無く、総括は「このまま公開してよい」——直す前の十三か所が §6-2d・附録C・確信度台帳・補遺II §5 の形と食い違うこと、"
    "新しい言い回し（§11-2b の「保証されない」・§6-5a で保証の側を「原理的に」のまま残したこと・Human-on-the-loop の監視を分離した監査とする読み）、"
    "主張を強めも弱めもしていないこと、直し漏れが無いこと、直さなかった所（§6-1b・§6-2a・附録C-3a・§7-3a・§13-0a）の判断、経緯の記述、英語版の対応を、"
    "それぞれ自分で確かめて是認した。回答の中の行番号は実物で確かめた（一覧に無い節を挙げた言い方の不正確が一つ——判断の中身には響かない）。"
    "記録は `verification/v5.4-correction/`。\n\n"
)
PUBLISHED_LINE = "- [x] v5.4（JA・EN）の公開（2026-10-07・登録者の許可による）"  # 登録者の許可（2026-10-07 08:1x「許可する（推奨）」）

