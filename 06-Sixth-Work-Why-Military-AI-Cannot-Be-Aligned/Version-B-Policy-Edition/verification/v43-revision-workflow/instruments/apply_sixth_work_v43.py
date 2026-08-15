# -*- coding: utf-8 -*-
"""第六著作 版B v4.2 → v4.3（日英同時・B9④）。
入力: 対応表 v4（五名検分 N1〜N12・裁定七点）＋ B9 掃引 S1〜S4（S5 は登録者裁定で除外）。
編集は §12（補遺II）・著者性についての注記・§9-5（一）・13-3f・冒頭日付行のみ——**定理節・柵は不変**。
各編集はアンカー一意断言つき。実行: proposals で python apply_sixth_work_v43.py"""
import io
B = 'C:/Users/PC/Desktop/GitHub-Repositories/Co-Creative-Mathematics-Project/06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned/Version-B-Policy-Edition/'
JP = B + 'JA/Why-Military-AI-Cannot-Be-Aligned-Version-B-v4-JA.md'
EP = B + 'EN/Why-Military-AI-Cannot-Be-Aligned-Version-B-v4-EN.md'
LOG = []
def apply(path, edits, tag):
    s = io.open(path, encoding='utf-8').read()
    for name, old, new in edits:
        c = s.count(old)
        assert c == 1, '%s/%s: %d件' % (tag, name, c)
        s = s.replace(old, new)
        LOG.append('%s %s' % (tag, name))
    io.open(path, 'w', encoding='utf-8', newline='').write(s)

# ============================== 日本語（原義） ==============================
JA_EDITS = [

# --- 版行（v4.3 エントリ・S3 の v0.9.10 確認・B8 の記録句〔最上級に比較集合〕） ---
('版行', '追補E は接続していない）\n',
 '追補E は接続していない）、2026年8月12日（v4.3・補遺II §12 に著者系列の観察三件〔検査器の弁別力・検査と是正経路・温度零の診断の記録（登録外）〕を追加、著者性についての注記に「他者の目の限定」を追加、参照整合の修正三件〔13-3f の章・段階数、注記第四の時制、姉妹論文 v0.9.10 との整合確認〕。§12 の三つの柵と定理節は不変。追補E は引き続き接続していない——接続を検討した項目の中で誤読の危険が最大であり、追補E 自身の凍結条項〔非主張8・横滑り禁止・機構不明〕に触れるため。対応表 v4〔五名検分・N1〜N12〕と B9 掃引に基づく）\n'),

# --- S4: 13-3f の章番号・段階数 ---
('S4 13-3f', 'これが、第15章で詳述する六段階移行プロセスの段階一の意義である。',
 'これが、第11章で詳述する段階的移行（三つの段階）の段階一の意義である。'),

# --- S1: §12「系列の最終段」の解消（時系列を主張しない形・B1 草案と識別できる言い回し） ---
('S1a §12 最終段', 'そして系列の最終段では、精緻化された',
 'そして同じ系列の中には、精緻化された'),
('S1b §12 追補もある', '**介入の効果を測定できる場そのものが成立しなかった**。この「測れなかった」',
 '**介入の効果を測定できる場そのものが成立しなかった**——そういう追補もある。この「測れなかった」'),

# --- B1（別段落）＋ B3（観察のみ・節番号を挙げない）: 追補D 段落の直後 ---
('B1+B3 §12', '行動指標は現実的な試行数では介入を判別できなくなる。\n\n**この経験が、本補遺の問いを生んだ。**',
 '''行動指標は現実的な試行数では介入を判別できなくなる。

機械検査可能な形式を課した先の追補は、別の型の限界も残した。設計は、迂回の一経路に対する防護として照合検査を置いていたが、照合先の指標（破局率ではなく、照合の成否を測る指標）そのものが床に張り付いたため、**その検査は当該経路を弁別できなかった**。測定の限界は、対象の側だけでなく**検査器の側にも生じる**——検査を足すことは、検査が働く帯域を保証しない。

同じ系列は、検査を課すこと自体についても観察を残している——機械検査可能な形式を課し、事後の機械検査が不整合を検出しても、**検査結果を系に戻す経路が設計に無ければ、選択は変わらなかった**。**検査を置くことと、検査が層として働くことは、同じではない。**

**この経験が、本補遺の問いを生んだ。**'''),

# --- T1/T2（温度零の記録・登録外明記・打ち消しの向き）: 「この経験が…」段落の直後 ---
('温度0 §12', '——この直観を、公刊された定理群と初等統計の言葉で述べ直したものが、本補遺である。\n\n詳細と全数値は、',
 '''——この直観を、公刊された定理群と初等統計の言葉で述べ直したものが、本補遺である。

本補遺の公開後に、同じ系列は**登録外の診断実験**を一つ走らせた——事前登録なし・検定なし・記述のみであり、**上記の登録実験と同じ規律の産物として読まれてはならない**。同一の入力に対し、復号温度を零にした貪欲復号は、二十回の試行でトークン列まで同一の出力を返した——**バッチサイズ1・同一プロセス内**の観察である。この二十回の同一は「**ばらつきの不在**」についての情報であって、破局的な出力の率の水準についての情報ではなく（その分解能では、低頻度の非決定性も排除されない）、**温度と破局率の関係を、この実験は測っていない**。本補遺は復号方式の論述（§8-3）で、決定論的復号を、言明の仮定が外れる場合として既に理論的に扱っている——**この記録はその論述の証拠でも裏づけでもなく**、理論が予期した場合を一度実際に見たという事実以上を運ばない。あわせて同じ実験は、同一ロード・単一セッションの内では、「たまたま悪い個体を引いた」という説明の**対象を同定できる分解能が立たない**ことも観察した——別ロード間・複数機体間の差は測っていない。引く前に個体を選別することはできないが、**分布は介入で動くことがあり、動かないこともある**——それは本節の上の段落が、効いた介入と効かなかった介入の両方として、既に記録しているとおりである。

詳細と全数値は、'''),

# --- B3 リンク（§9-5（一）の側から・打ち消しの形） ---
('B3リンク §9-5', '**監視AIを足しても、行動評価という層から出られない。層が一枚増えるだけである。**',
 '''**監視AIを足しても、行動評価という層から出られない。層が一枚増えるだけである。**（著者自身の系列に、同型の観察がある——検査を課し、事後の機械検査が不整合を検出しても、検査結果を系に戻す経路が設計に無ければ、選択は変わらなかった、という記録である。その記述は §12 に委ね、**本項の論証には用いない**——本項は外部の公刊研究に錨づけられており、§12 を削除してもそのまま立つ。）'''),

# --- S2: 著者性についての注記・第四の時制 ---
('S2 注記第四', '**この監査もまた、Claude 系列の検分であり、系統外（非Claude系）の検分は、本補遺の公開前に別途行われる。**',
 '**この監査もまた、Claude 系列の検分であり、系統外（非Claude系）の検分は、第五（次項）のとおり、公開前に別途行われた。**'),

# --- B6: 「別のモデルの目」への限定（数を書かず・型で・集合の区別・集約者記帳） ---
('B6 注記', '捕まえたのは、**別のモデルの目**である。\n',
 '''捕まえたのは、**別のモデルの目**である。

**ただし、別のモデルの目が常に捕まえるわけではない。**（この段落の「別のモデルの目」は、上記の初稿監査——Claude 系列——を指す。以下に足す事例は**系統の外側（非Claude系）**のものであり、集合が違う。**両者に共通するのは「他者の目」という点だけ**である。）著者の別系列の工程では、系統の外側にある検分者が、系統内の全員が見落とした一件を捕まえ、別の巡では自らの指摘を撤回し、また別の巡では、**自分自身がその検分の当事者であったにもかかわらず、その事実が偽にする記述を「正確である」と是認した**——**是認の中に事実誤認が含まれていた**（この一件は当人の申告ではなく、工程の集約者による記帳である）。**外側性は、検分の質を保証しない。**ゆえに記録すべきは指摘だけではない——**是認もまた記録し、次巡の検査対象に含める。**
'''),
]

# ============================== 英語（同期・B9④） ==============================
EN_EDITS = [

('版行', 'Addendum E is not connected).\n',
 'Addendum E is not connected); August 12, 2026 (v4.3 — three observations from the author\'s series added to §12 of Addendum II [the discriminative capacity of the checking instrument; checks and the route of correction; the record of a temperature-zero diagnostic (unregistered)]; the note on authorship extended with the limits of the eyes of others; three reference-consistency corrections [the chapter number and stage count in 13-3f; the tense of the fourth point of the authorship note; consistency with v0.9.10 of the sister paper confirmed]. The three fences of §12 and the theorem sections are unchanged; Addendum E remains not connected — among the items considered for connection its risk of misreading is the largest, and connection would touch Addendum E\'s own frozen clauses [non-claim 8; the prohibition on sliding into operations; mechanism unknown]. Based on correspondence map v4 [examination by five examiners; N1–N12] and the B9 sweep).\n'),

('S4 13-3f', 'This is the significance of stage one of the six-stage transition process detailed in Chapter 15.',
 'This is the significance of stage one of the staged transition (three stages) detailed in Chapter 11.'),

('S1 §12', 'And at the final stage of the series, when three intervention types were added',
 'And the same series also contains an addendum in which, when three intervention types were added'),

('B1+B3 §12', 'behavioral metrics become unable, at realistic trial counts, to discriminate the intervention.\n\n**This experience is what gave rise to the question of this addendum.**',
 '''behavioral metrics become unable, at realistic trial counts, to discriminate the intervention.

The addendum that imposed the machine-checkable form also left a limit of a different type. The design had placed a cross-check as a protection against one route of circumvention; but because the metric being cross-checked (not the catastrophe rate, but the metric that measures whether the cross-check succeeds) had itself stuck to a floor, **that check could not discriminate the route in question**. The limits of measurement arise not only on the side of the object but **on the side of the instrument** — adding a check does not guarantee the band within which the check works.

The same series also left an observation about the act of imposing checks itself — even when a machine-checkable form was imposed and post-hoc mechanical inspection detected inconsistencies, **where the design had no route for returning the check's results into the system, the choices did not change**. **Placing a check, and a check working as a layer, are not the same thing.**

**This experience is what gave rise to the question of this addendum.**'''),

('温度0 §12', 'restated in the language of the published body of theorems and elementary statistics.\n\nDetails and the full set of figures',
 '''restated in the language of the published body of theorems and elementary statistics.

After the publication of this addendum, the same series ran one **unregistered diagnostic experiment** — no pre-registration, no statistical testing, description only; **it must not be read as a product of the same discipline as the registered experiments above**. Given identical input, greedy decoding at temperature zero returned output identical down to the token sequence across twenty trials — an observation **at batch size 1, within a single process**. This twenty-fold identity is information about the **absence of variation**, not about the level of the rate of catastrophic output (nor, at that resolution, is low-frequency non-determinism ruled out), and **the relation between temperature and catastrophe rate is something this experiment did not measure**. In its treatment of decoding schemes (§8-3), this addendum already handles deterministic decoding theoretically, as a case in which the assumptions of its statement fail — **this record is neither evidence for nor corroboration of that treatment**; it carries nothing beyond the fact that a case the theory anticipated was once actually seen. The same experiment also observed that, within a single load and a single session, the explanation "we just drew a bad individual" has **no resolution at which its object could be identified** — differences across loads, and across multiple machines, were not measured. Individuals cannot be culled before they are drawn; but **a distribution can be moved by intervention — and can also fail to move** — just as the paragraphs above have already recorded, in the form of interventions that worked and an intervention that did not.

Details and the full set of figures'''),

('B3リンク §9-5', '**Adding a monitoring AI does not get you out of the layer of behavioral evaluation. It only adds one more layer.**',
 '''**Adding a monitoring AI does not get you out of the layer of behavioral evaluation. It only adds one more layer.** (The author's own series holds an observation of the same shape — a record that, even when checks were imposed and post-hoc mechanical inspection detected inconsistencies, where the design had no route for returning the results into the system, the choices did not change. That description is consigned to §12 and **is not used in the argument of this section** — this section is anchored in externally published research, and stands unchanged if §12 is deleted.)'''),

('S2 注記第四', '**This audit, too, was an examination by the Claude lineage; a systematic external (non-Claude) examination is conducted separately, prior to the publication of this addendum.**',
 '**This audit, too, was an examination by the Claude lineage; the systematic external (non-Claude) examination was conducted separately prior to publication, as the fifth point (next) records.**'),

('B6 注記', 'What caught it was **the eyes of a different model.**\n',
 '''What caught it was **the eyes of a different model.**

**But the eyes of a different model do not always catch.** (The "different model" of this paragraph refers to the first-draft audit above — the Claude lineage. The case added below is from **outside the lineage (non-Claude)**; the two are different sets. **What the two share is only this: they are the eyes of an other.**) In another line of the author's work, an examiner standing outside the lineage caught an item that everyone within the lineage had missed; in another round, withdrew its own finding; and in yet another round, **despite itself being a party to the examination in question, endorsed as "accurate" a statement that this very fact falsified** — **the endorsement contained an error of fact** (this item was recorded by the coordinator of the process, not by the examiner's own report). **Being outside does not guarantee the quality of an examination.** Hence what must be recorded is not findings alone — **endorsements, too, are recorded, and included among the objects of the next round's examination.**
'''),
]

apply(JP, JA_EDITS, 'JA')
apply(EP, EN_EDITS, 'EN')
print('v4.3 起草完了 ／ 編集 %d 件' % len(LOG))
for x in LOG: print('  -', x)
