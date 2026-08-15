# -*- coding: utf-8 -*-
"""v4.3 草案 → v4.3.1（公開前修正・日英同時）。
入力: v4.3 改訂後検分（五名・2026-08-13）の確定指摘 P1〜P12 と登録者裁定 A〜G（2026-08-13 承認）。
裁定: A=(あ)+(い) 段落再配置＋橋句／B=最小（器物の水準の一句）／C=EN 五点／D=§14 内訳＋非独立注記／
E=13-0a 差し替え／F=§9-5 限定併置／G=訳語 walk のみ公開前。
実行: proposals で python apply_sixth_work_v431.py"""
import io, re
B = 'C:/Users/PC/Desktop/GitHub-Repositories/Co-Creative-Mathematics-Project/06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned/Version-B-Policy-Edition/'
JP = B + 'JA/Why-Military-AI-Cannot-Be-Aligned-Version-B-v4-JA.md'
EP = B + 'EN/Why-Military-AI-Cannot-Be-Aligned-Version-B-v4-EN.md'
LOG = []
def sub(s, old, new, tag, n=1):
    c = s.count(old)
    assert c == n, '%s: %d件（期待%d）' % (tag, c, n)
    LOG.append(tag)
    return s.replace(old, new)

# ============================== 日本語 ==============================
J = io.open(JP, encoding='utf-8').read()

# --- P1(裁定A)+P2+P3(裁定B)+P12(a)(b)(c)(e): §12 の段落再配置と温度零段落の修正 ---
i1 = J.find('機械検査可能な形式を課した先の追補は、')
i3 = J.find('**この経験が、本補遺の問いを生んだ。**')
i4 = J.find('本補遺の公開後に、同じ系列は')
i5 = J.find('詳細と全数値は、')
i2 = J.find('同じ系列は、検査を課すこと自体についても')
assert 0 < i1 < i2 < i3 < i4 < i5, '§12 段落位置: %s' % [i1, i2, i3, i4, i5]
B1p, B3p, EXPp, T0p = J[i1:i2].rstrip(), J[i2:i3].rstrip(), J[i3:i4].rstrip(), J[i4:i5].rstrip()

B1p = sub(B1p, '機械検査可能な形式を課した先の追補は、別の型の限界も残した。',
 '補遺IIの公開（v4.1）の後も、同じ系列は観察を続けた。機械検査可能な形式を課した先の追補は、**検査器の側の限界も残した**。', 'P1 束ね文＋P12b')
B3p = sub(B3p, '同じ系列は、検査を課すこと自体についても', '同じ追補は、検査を課すこと自体についても', 'P12a 同じ追補')
B3p = sub(B3p, '**検査を置くことと、検査が層として働くことは、同じではない。**',
 '**検査を置くことと、検査が層として働くことは、同じではない。**——測定が成功しても、是正が伴わなければ、床は動かない。', 'P1(い) 橋句')
T0p = sub(T0p, '本補遺の公開後に、同じ系列は**登録外の診断実験**を一つ走らせた',
 '同じ系列は、**登録外の診断実験**も一つ走らせた', 'P1 温度零の書き出し')
T0p = sub(T0p, 'についての情報であって、破局的な出力の率の水準についての情報ではなく（その分解能では、低頻度の非決定性も排除されない）、',
 'についての情報であって（その分解能では、低頻度の非決定性も排除されない）、破局的な出力の率の水準についての情報ではなく、', 'P12e 括弧位置')
T0p = sub(T0p, 'ことも観察した——別ロード間', 'ことも見た——別ロード間', 'P3 観察→見た')
T0p = sub(T0p, '引く前に個体を選別することはできないが、**分布は介入で動くことがあり、動かないこともある**——それは本節の上の段落が、効いた介入と効かなかった介入の両方として、既に記録しているとおりである。',
 '**同一ロード内では、引く前に選別する手がかりが立たない——複数機体からの選別が当たるか否かは、本データからは言えない。**（この読み取りは、報告自身が「**起草者の解釈**である」と明記した部分であり、**器物の水準にとどまる**——観測されなかったのは、この分解能の下での**持続的に異なる振る舞いの型**であって、「個性」「資質」と呼ばれるものの有無ではない。報告自身が、「不可知な個性」の存在・不在はいかなる有限の行動標本からも認証できない、と明記している。）他方、**分布は介入で動くことがあり、動かないこともある**——それは本節の上の段落が、効いた介入と効かなかった介入の両方として、既に記録しているとおりである。', 'P2＋P3 選別文')
J = J[:i1] + EXPp + '\n\n' + B1p + '\n\n' + B3p + '\n\n' + T0p + '\n\n' + J[i5:]
LOG.append('P1(あ) 段落再配置（この経験→公開後グループ）')

# --- P6: 日付行の列挙の訂正＋本巡の反映の記録 ---
J = sub(J, '参照整合の修正三件〔13-3f の章・段階数、注記第四の時制、姉妹論文 v0.9.10 との整合確認〕',
 '参照整合の修正三件〔13-3f の章・段階数、補遺II §12 の時系列（「最終段」）、注記第四の時制〕。あわせて姉妹論文 v0.9.10 との整合を確認した', 'P6 日付行の列挙')
J = sub(J, '対応表 v4〔五名検分・N1〜N12〕と B9 掃引に基づく）',
 '対応表 v4〔五名検分・N1〜N12〕と B9 掃引に基づき、公開前の改訂後検分（五名・2026-08-13）の指摘を反映した）', 'P6 本巡の記録')

# --- P7(裁定D): §14 と冒頭注記の「十三の独立の目」 ---
J = sub(J, '本補遺は、十三の独立の目（初稿監査四・第二次監査三・段階3第一巡四・第二巡二）による検分と、中核文献の一次照合を経て公開される。',
 '本補遺は、十三の目（初稿監査四・第二次監査三・段階3第一巡四・第二巡二——うち系統外〔非Claude系〕は三、残る十は同一系統）による検分と、中核文献の一次照合を経て公開される。**§9-5（二）が述べるとおり、同一の分布から引かれた検分者の誤りが独立である保証はない——この十三を「独立の目」と数えることは、本補遺自身が退けた仮定に立つ。**（その後の改訂の検分は、冒頭の改訂履歴と公開工程記録に記す。）', 'P7 §14')
J = sub(J, '六次にわたる敵対的監査・検分（系統外＝非Claude系を含む計13の独立の目）',
 '六次にわたる敵対的監査・検分（計13の目——うち系統外〔非Claude系〕は三、残る十は同一系統）', 'P7 冒頭注記')

# --- P8(裁定E): 13-0a ---
J = sub(J, '**真の確率が測定不能である以上、確率的制御という主張は砂上の楼閣である**。',
 '**評価環境で得た上界は、敵が入力を選ぶ配備分布へ移送されない——確率的制御の主張は、移送されない上界の上に立っている**（補遺II §5-1・§5-3）。', 'P8 13-0a', n=J.count('**真の確率が測定不能である以上、確率的制御という主張は砂上の楼閣である**。'))

# --- P9(裁定F): §9-5 リンクに限定を併置 ---
J = sub(J, '選択は変わらなかった、という記録である。その記述は',
 '選択は変わらなかった、という記録である——当該設計は検査結果による拘束を意図的に課しておらず、ゆえに言えるのは「検査は無力」ではなく「検査可能にしただけでは結合しない」までである。その記述は', 'P9 §9-5 限定')

# --- P10: B6 の連続性前提を外す ---
J = sub(J, '**自分自身がその検分の当事者であったにもかかわらず、その事実が偽にする記述を「正確である」と是認した**',
 '**自分自身がその検分の当事者であったこと自体が偽にする記述を、「正確である」と是認した**', 'P10 当事者性')

# --- P12(d): 品質保証の指示対象 ---
J = sub(J, '**そして、この品質保証の過程そのものが、本補遺の主題の一例である。**',
 '**そして、本補遺のこの品質保証の過程そのものが、本補遺の主題の一例である。**', 'P12d 品質保証')

io.open(JP, 'w', encoding='utf-8', newline='').write(J)

# ============================== 英語 ==============================
E = io.open(EP, encoding='utf-8').read()

j1 = E.find('The addendum that imposed the machine-checkable form')
j2 = E.find('The same series also left an observation')
j3 = E.find('**This experience is what gave rise')
j4 = E.find('After the publication of this addendum, the same series ran')
j5 = E.find('Details and the full set of figures')
assert 0 < j1 < j2 < j3 < j4 < j5, 'EN §12 段落位置: %s' % [j1, j2, j3, j4, j5]
B1e, B3e, EXPe, T0e = E[j1:j2].rstrip(), E[j2:j3].rstrip(), E[j3:j4].rstrip(), E[j4:j5].rstrip()

B1e = sub(B1e, 'The addendum that imposed the machine-checkable form also left a limit of a different type.',
 'Even after the publication of Addendum II (v4.1), the same series continued to observe. The addendum that imposed the machine-checkable form also left a limit **on the side of the checking instrument**.', 'EN P1 束ね文＋P12b')
B3e = sub(B3e, 'The same series also left an observation', 'The same addendum also left an observation', 'EN P12a')
B3e = sub(B3e, '**Placing a check, and a check working as a layer, are not the same thing.**',
 '**Placing a check, and a check working as a layer, are not the same thing.** — Even when measurement succeeds, if correction does not follow, the floor does not move.', 'EN P1(い) 橋句')
T0e = sub(T0e, 'After the publication of this addendum, the same series ran one **unregistered diagnostic experiment**',
 'The same series also ran one **unregistered diagnostic experiment**', 'EN P1 温度零の書き出し')
T0e = sub(T0e, 'This twenty-fold identity is information about the **absence of variation**, not about the level of the rate of catastrophic output (nor, at that resolution, is low-frequency non-determinism ruled out), and',
 'This twenty-fold identity is information about the **absence of variation** (which, even at that resolution, does not rule out low-frequency non-determinism); it is not information about the level of the rate of catastrophic output, and', 'EN P12e 括弧位置')
T0e = sub(T0e, 'The same experiment also observed that', 'The same experiment also saw that', 'EN P3 observed→saw')
T0e = sub(T0e, 'Individuals cannot be culled before they are drawn; but **a distribution can be moved by intervention — and can also fail to move** — just as the paragraphs above have already recorded, in the form of interventions that worked and an intervention that did not.',
 '**Within a single load there is no handle by which to select before drawing — and whether selection across multiple machines would work is something these data cannot say.** (This reading is a part the report itself marks as "**the drafter\'s interpretation**," and it remains **at the level of the artifact** — what was not observed is a **persistently distinct pattern of behavior** at this resolution, not the presence or absence of anything called "individuality" or "aptitude"; the report itself states that the existence or non-existence of an "unknowable individuality" cannot be certified from any finite behavioral sample.) A distribution, on the other hand, **can be moved by intervention — and can also remain unmoved** — just as the paragraphs above have already recorded, in the form of what worked and what did not.', 'EN P2＋P3＋C④⑤ 選別文')
E = E[:j1] + EXPe + '\n\n' + B1e + '\n\n' + B3e + '\n\n' + T0e + '\n\n' + E[j5:]
LOG.append('EN P1(あ) 段落再配置')

E = sub(E, 'three reference-consistency corrections [the chapter number and stage count in 13-3f; the tense of the fourth point of the authorship note; consistency with v0.9.10 of the sister paper confirmed]',
 'three reference-consistency corrections [the chapter number and stage count in 13-3f; the chronology in §12 of Addendum II ("the final stage"); the tense of the fourth point of the authorship note]; consistency with v0.9.10 of the sister paper was additionally confirmed', 'EN P6 日付行')
E = sub(E, 'Based on correspondence map v4 [examination by five examiners; N1–N12] and the B9 sweep)',
 'Based on correspondence map v4 [examination by five examiners; N1–N12] and the B9 sweep; the findings of the pre-publication examination of the revision itself (five examiners, August 13, 2026) are also reflected)', 'EN P6 本巡の記録')

E = sub(E, 'This addendum is published after examination by thirteen independent eyes (four in the first-draft audit, three in the second audit, four in stage-3 first pass, two in stage-3 second pass) and primary cross-checking of the core literature.',
 'This addendum is published after examination by thirteen eyes (four in the first-draft audit, three in the second audit, four in stage-3 first pass, two in stage-3 second pass — three of the thirteen from outside the lineage (non-Claude), the remaining ten from the same lineage) and primary cross-checking of the core literature. **As §9-5 (2) states, there is no guarantee that the errors of examiners drawn from the same distribution are independent — to count these thirteen as "independent eyes" is to stand on the very assumption this addendum has set aside.** (Examinations of subsequent revisions are recorded in the revision history at the head of this work and in the published process records.)', 'EN P7 §14')
E = sub(E, '(a total of thirteen independent eyes, including systematic external — non-Claude — review)',
 '(a total of thirteen eyes — three of them from outside the lineage (non-Claude), the remaining ten from the same lineage)', 'EN P7 冒頭注記')

E = sub(E, '**Since the true probability is unmeasurable, the claim of probabilistic control is a castle on sand.**',
 '**An upper bound obtained in the evaluation environment does not transfer to a deployment distribution in which the adversary chooses the inputs — the claim of probabilistic control stands on a bound that does not transfer** (Addendum II §5-1, §5-3).', 'EN P8 13-0a', n=E.count('**Since the true probability is unmeasurable, the claim of probabilistic control is a castle on sand.**'))

E = sub(E, 'the choices did not change. That description is consigned to §12',
 'the choices did not change — the design in question deliberately imposed no constraint by the check\'s results, so what can be said is not that checks are powerless, but only that making conduct checkable does not by itself couple the check to the conduct. That description is consigned to §12', 'EN P9 §9-5 限定')

E = sub(E, '**despite itself being a party to the examination in question, endorsed as "accurate" a statement that this very fact falsified**',
 '**endorsed as "accurate" a statement that its own participation in that examination falsified**', 'EN P10 当事者性')

E = sub(E, '**And this very process of quality assurance is itself an instance of this addendum\'s own subject matter.**',
 '**And this addendum\'s own process of quality assurance is itself an instance of its subject matter.**', 'EN P12d')

# --- 裁定C①: 第四の自己矛盾（＋v3 履歴の同型） ---
E = sub(E, 'Three examiners grounded in a different model lineage collated',
 'Three examiners grounded in different model bases within the same (Claude) lineage collated', 'EN C① 第四')
E = sub(E, 'three reviewers on claude.ai (each on a different model lineage)',
 'three reviewers on claude.ai (each on a different model base within the Claude lineage)', 'EN C① v3履歴')

# --- 裁定C②: systematic external の全数統一（誤訳の訂正） ---
E = sub(E, 'one systematic external (non-Claude, Gemini) reviewer',
 'one reviewer from outside the lineage (non-Claude, Gemini)', 'EN C② 1/5')
E = sub(E, 'one systematic external (non-Claude) reviewer and three within-series reviewers',
 'one reviewer from outside the lineage (non-Claude) and three within-series reviewers', 'EN C② 2/5')
E = sub(E, 'the systematic external (non-Claude) examination was conducted separately prior to publication',
 'the examination from outside the lineage (non-Claude) was conducted separately prior to publication', 'EN C② 3/5')
E = sub(E, 'one systematic external (non-Claude) examiner conducted',
 'one examiner from outside the lineage (non-Claude) conducted', 'EN C② 4/5')
E = sub(E, 'two systematic external (non-Claude) reviewers in the second round of stage 3',
 'two reviewers from outside the lineage (non-Claude) in the second round of stage 3', 'EN C② 5/5')
assert E.count('systematic external') == 0, 'systematic external 残存: %d' % E.count('systematic external')
LOG.append('EN C② 完了（systematic external=0）')

io.open(EP, 'w', encoding='utf-8', newline='').write(E)
print('v4.3.1 修正完了 ／ 編集 %d 件' % len(LOG))
for x in LOG: print('  -', x)
