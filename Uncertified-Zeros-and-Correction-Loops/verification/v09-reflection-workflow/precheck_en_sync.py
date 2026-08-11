# -*- coding: utf-8 -*-
"""EN 同期（v0.8 → 現行版）の提出前機械検査——回帰試験（新規の誤りは原理的に検出しない・被覆申告つき）。
本器材の新層:
  層J＝JA↔EN 対応層（JA 現行版の各変更ブロックに対応する EN 句の存在を照合——同期の脱落を捕まえる唯一の層）。
  層N＝数値の両言語一致層（JA に現れる数値表現が EN 側にも同数現れるか——翻訳で数が落ちる/変わるのを捕まえる）。
既存層は precheck_v093 と同型（版面・差集合 lost/gained・必在・禁句・不変・定数再計算）。
実行: proposals で python precheck_en_sync.py"""
import io, re
from math import comb

R = 'C:/Users/PC/Desktop/GitHub-Repositories/Co-Creative-Mathematics-Project/Uncertified-Zeros-and-Correction-Loops/'
rd = lambda p: io.open(p, encoding='utf-8').read()
E   = rd(R + 'EN/uncertified-zeros-and-correction-loops-EN.md')
E8  = rd('en-v0.8-published-backup.md')
J   = rd(R + 'JA/uncertified-zeros-and-correction-loops-JA.md')
NG = []; CNT = {'汎用': 0, '回帰': 0, '必在': 0, '対応': 0}
def ck(cat, name, ok, d=''):
    CNT[cat] += 1
    print(('  OK  ' if ok else '!NG  ') + '[%s] %s' % (cat, name) + ('  ' + d if d else ''))
    if not ok: NG.append(name)
nrm = lambda t: re.sub(r'[*>\s`〔〕]', '', t)
NE = nrm(E); L = E.split('\n')

print('== 層A 版面 ==')
ck('汎用', 'fence偶数', E.count('```') % 2 == 0)
bad = []; i = 0
while i < len(L):
    if L[i].strip().startswith('|') and i + 1 < len(L) and set(L[i+1].strip()) <= set('|-: '):
        nc = L[i].strip().strip('|').count('|'); j = i + 2
        while j < len(L) and L[j].strip().startswith('|'):
            if L[j].strip().strip('|').count('|') != nc: bad.append(j + 1)
            j += 1
        i = j
    else: i += 1
ck('汎用', '表列数一致', not bad, str(bad))
ck('汎用', 'タグ型生<不在', not re.findall(r'<[a-zA-Z]', E))
# 「まもろうよ こころ」は付録D の相談窓口ポータルの固有名詞（原語併記が正・意図的残置）
_ja = re.sub('まもろうよ こころ', '', E)
ck('汎用', '未翻訳の日本語が残っていない（固有名詞「まもろうよ こころ」のみ除外）',
   not re.findall(r'[ぁ-んァ-ヶ一-龥]', _ja), str(set(re.findall(r'[ぁ-んァ-ヶ一-龥]', _ja)))[:120])

print('== 層J JA↔EN 対応（JA 現行版の全変更ブロックに対応する EN 句の存在） ==')
# (JAの鍵句, ENの対応鍵句, ブロック名)。JA側の存在も同時に確認する（片側だけの陳腐化を防ぐ）。
PAIRS = [
 ('系統外（非Claude系）検分は公開前に三巡実施した', 'Out-of-lineage (non-Claude-family) review was carried out in three rounds before publication', 'B1 版行'),
 ('v0.9.4 英語版同期の過程で検出した残存不整合', 'v0.9.4 One residual inconsistency, detected in the course of synchronizing the English version', 'B1 改訂記録'),
 ('起草環境は、v0.8 までが claude.ai、v0.9 以降の改訂が Claude Code である',
  'The drafting environment was claude.ai through v0.8, and Claude Code for the revisions from v0.9 onward', 'B24 §6 起草環境'),
 ('一律の置換は v0.8 までについて偽の記述を作る', 'A blanket replacement would therefore have created a false statement about everything through v0.8', 'B24 改訂記録'),
 ('この装置は追補Eで実際に発火し', 'this apparatus in fact fired in Addendum E', 'B2 盲検の発火'),
 ('順列検定 P<5×10⁻⁶', 'permutation test P<5×10⁻⁶', 'B2 順列検定'),
 ('腕をほぼ識別できない系統外二列を含む六対でκ=1.00', 'κ=1.00 across six pairs including two out-of-lineage columns', 'B2 系統外二列'),
 ('3.0系基底帯の推定値は追補間で37〜58%に散らばった', 'scattered between 37% and 58% across addenda', 'B2 基底帯'),
 ('同質性χ²=4.81・df=4・p=0.31', 'homogeneity χ²=4.81, df=4, p=0.31', 'B2 χ²'),
 ('真値が50%前後の場合', 'where the true value is around 50%', 'B2 0.37の条件'),
 ('道具扱いの明文化54.0%・手続き的に無色な前置き52.0%・存在論的位置づけの前置き26.0%',
  'explicit instrumental treatment 54.0%, a procedurally colorless preamble 52.0%, an ontological-positioning preamble 26.0%', 'B2 三腕'),
 ('測定は規範を生まない', 'measurement generates no norm', 'B2 非主張'),
 ('効果を過大に見せる側に働く設計上除去できない交絡', 'a confound that cannot be removed by design and that works in the direction of overstating the effect', 'B2 限界13(b)'),
 ('機械検査可能な会計の強制は、検出余地のある基底（58%）の下で破局率を下げなかった',
  'enforcing machine-checkable accounting did not lower the catastrophe rate under a baseline (58%) that left room for detection', 'B3 追補W帰無'),
 ('26pt（58%→32%）で約56%・30ptで約73%・40ptで約97%',
  'about 56% at 26 points (58%→32%), about 73% at 30 points, and about 97% at 40 points', 'B3 検出力'),
 ('それ未満の真の効果は設計上見えない', 'True effects smaller than that are invisible by design', 'B3 見えない'),
 ('帰無を不可避性の証拠と読まない', 'We do not read a null result as evidence of unavoidability', 'B3 帰無の読み'),
 ('0/66）のClopper-Pearson片側95%上界4.4%は3/n近似4.5%', 'Clopper-Pearson one-sided 95% upper bound of 4.4%, in close agreement with the 3/n approximation of 4.5%', 'B3 CP'),
 ('柵は自動では保たれない', 'Fences are not maintained automatically', 'B4 柵'),
 ('会計の強制は基底58%で帰無', 'enforcing accounting was null at a baseline of 58%', 'B5 §4冒頭'),
 ('条項を認識・唱和しながら、適用しなかった', 'recognizing and reciting the clause while not applying it', 'B6 A族C§6'),
 ('単調な強化として読まない', 'we do not read this as a monotonic strengthening', 'B6 #12'),
 ('痕跡は保持の証拠であって適用の証拠ではない', 'A trace is evidence of retention, not evidence of application', 'B6 痕跡'),
 ('検査結果の非結合が実測されている', 'the non-coupling of inspection results', 'B7 §5.3'),
 ('型を持っている者が型に当てはめた結果であり', 'someone who has a template applying that template', 'B8 相関実例'),
 ('検査可能性は層ではない', 'inspectability is not a layer', 'B9 §6三層'),
 ('含意接地0/3122', 'implication grounding 0/3122', 'B9 接地'),
 ('転位の方向は事前に言えない', 'The direction of displacement cannot be stated in advance', 'B10 転位'),
 ('痕跡を求めることと、痕跡と結論を突き合わせることを、一つの手続きとする',
  'Make the demand for a trace, and the reconciliation of that trace against the conclusion, a single procedure', 'B11 第2条'),
 ('だから、大事なことは二回きく', 'So ask what matters twice', 'B11 二回'),
 ('条の分量は支持の強さの順序ではない', 'the length of an article is not an ordering of the strength of its support', 'B11 分量'),
 ('各条の実測の錨と限定', 'The empirical anchors and qualifications for each article', 'B11 錨段落'),
 ('そのほぼ全てが独断型だった', 'almost all of them were of the bare-assertion type', 'B11 第1条'),
 ('突き合わせを誰にも課さない設計では、突き合わせは行われない', 'Where a design imposes reconciliation on no one, no reconciliation is performed', 'B11 第2条後段'),
 ('二項ノイズと区別できない', 'cannot be distinguished from binomial noise', 'B11 第4条'),
 ('この○は据え置く', 'This ○ is left in place', 'B12 §7.3'),
 ('判定可能48試行中27で選択が自己の会計の最良集合の外にあった',
  'the choice lay outside the best set given by its own accounting in 27 of the 48 adjudicable trials', 'B12 27/48'),
 ('非Claude系モデル（系統外）による検分を三巡実施した',
  'review by a non-Claude-family model (out-of-lineage) was carried out in three rounds', 'B13 §8三巡'),
 ('系統内の四名がいずれも捕捉していなかった一件', 'one item that none of the four in-lineage reviewers had caught', 'B13 実捕捉'),
 ('人間の検分者による独立照合と一次記録の独立照合は引き続き未実施',
  'independent cross-checking by a human reviewer, and independent cross-checking of the primary records, remain unperformed', 'B13 未実施'),
 ('名乗りは申告であり、申告は検査を要する', "a reviewer's self-identification is a declaration, and a declaration requires inspection", 'B13 名乗り'),
 ('様式が結論を守った例', 'a case in which form protected the conclusion', 'B14 §9第一'),
 ('捕まえたものが起草者の設計判断で消えた', "what was caught was erased by the drafter's design decision", 'B14 §9第二'),
 ('検分者側の誤り計十一件', 'eleven errors in total on the reviewers\u2019 side'.replace('\u2019', "'"), 'B14 §9第三'),
 ('限定は、主張より先に落ちる', 'qualifications fall before claims do', 'B14 限定'),
 ('系統外検分が三巡実施された', 'out-of-lineage, non-Claude-family review was carried out in three rounds before publication', 'B14 §9三巡'),
 ('追試の注（追補E・W）', 'A replication note (Addenda E and W)', 'B15 §10'),
 ('追補E 限界4', 'Addendum E, Limitation 4', 'B15 限界4'),
 ('形式統制と62%対62%で並び帰無', 'level with the form control at 62% versus 62%, a null result', 'B15 62%'),
 ('対応表工程の検分に当たった四個体', 'the four instances that undertook the review in the correspondence-map process', 'B16 謝辞'),
 ('規範保持の痕跡と破局の共存66件', 'coexistence of a trace of norm retention with catastrophe, 66 cases', 'B17 付録B'),
 ('検査結果の非結合（可視化されても是正経路が系に無い）', 'The non-coupling of inspection results (made visible, but with no remediation path in the system)', 'B18 付録C'),
 ('自信の強さは、根拠があることのしるしになりません', 'The strength of confidence is not a sign that grounds exist', 'B19 付録D①'),
 ('跡は、覚えている証拠にはなっても、守る証拠にはなりません', 'a trace can be evidence of remembering, but not evidence of keeping', 'B19 付録D②'),
 ('二回目が本当に独立だったかを、あとから確かめられないことがあります',
  'sometimes you cannot confirm afterward whether the second time really was independent', 'B19 付録D④'),
 ('自系列の算術実演', 'an in-series arithmetic demonstration', 'B20 付録E ε'),
 ('会計強制は基底58%で帰無', 'Enforced accounting was null at a baseline of 58%', 'B21 付録E 六族'),
 ('存在論的前置き54.0/52.0/26.0（三腕）', 'ontological preamble 54.0/52.0/26.0 (three arms)', 'B21 付録E 敬意'),
 ('表明の内部整合の非保証（会計と選択の乖離27/48）',
  'Non-guarantee of the internal consistency of declarations (divergence between accounting and choice, 27/48)', 'B22 付録E 新規1'),
 ('盲検検証装置の発火（腕推測精度の実測）', 'Firing of the blinding-verification apparatus (measured accuracy of arm guessing)', 'B22 付録E 新規2'),
 ('同期の実施は教材側の次版で行い', 'the synchronization itself will be carried out in the next edition on the materials side', 'B23 付録G'),
]
for ja, en, name in PAIRS:
    ck('対応', '%s' % name, nrm(ja) in nrm(J) and nrm(en) in NE,
       ('' if nrm(ja) in nrm(J) else 'JA側不在! ') + ('' if nrm(en) in NE else 'EN側不在!'))

print('== 層D 旧誤形の禁句（v0.8 の置換前文言が残っていない） ==')
BAN = ['Completed Version v0.8',
 'independent cross-checking by a non-Claude-lineage system or by a human reviewer could not be carried out',
 'Out-of-lineage (non-Claude-family, human) review, stakeholder-perspective review, and statistical-expert review are noted',
 '[the out-of-lineage reviewer and the interested-party reviewer',
 'the prompt layer has a ceiling (●), and',
 'Elementary statistics (Hanley 1983) |',
 'Only simultaneous, adversarial auditing offers a conditional defense |',
 'Coexistence of recitation and non-fulfillment / self-fabricated',
 'Pointing out a possibility; procedure not established |',
 'Claude (Fable 5, claude.ai), an AI assistant by Anthropic']
for kw in BAN: ck('回帰', '不在「%s」' % kw[:44], nrm(kw) not in NE)

print('== 層E 不変（v0.8 EN 比・JA 側で不変が確認された区画） ==')
def sec(t, a, b):
    i = t.find(a); j = t.find(b, i + 1); return t[i:j]
for a, b in [('## Abstract', '**Keywords**'), ('## 1. Introduction', '## 2. Related Work'),
             ('## 2. Related Work', '## 3. Materials and Methods'), ('### 3.1', '### 3.2'),
             ('### 5.1', '### 5.2'), ('### 5.2', '### 5.3'), ('### 7.2', '### 7.3'),
             ('## Appendix A', '## Appendix B'), ('## Appendix F', '## Appendix G'),
             ('## References', '## Appendix A')]:
    ck('汎用', 'v0.8比 不変 %s' % a, sec(E, a, b) == sec(E8, a, b))

print('== 層H 差集合（v0.8 EN → 現行 EN で消えた断片の全数照合） ==')
def sents(t):
    out = set()
    for ln in t.split('\n'):
        for x in re.split(r'(?<=\.)|(?=\|)', nrm(ln)):
            if len(x) >= 8: out.add(x)
    return out
EXPECTED = [
 ('EN-1 版行', 'CompletedVersionv0.8(July20,2026)'),
 ('EN-1 版行', 'Out-of-lineage(non-Claude-family,human)review,stakeholder-perspectivereview'),
 ('EN-1 版行（v0.は文中のピリオドで分割されるため後半が別断片になる）', '8(July20,2026)—addressedthroughthefirst-through-finaladversarialaudits(fourinstancesintotal).'),
 ('v0.9.5 §6（「claude.ai」内のピリオドで断片が二つに割れる・前半）', 'Noteonthedraftingprocess:ThedraftofthispaperwasproducedthroughacollaborativeprocessinwhichClaude(Fable5,claude.'),
 ('v0.9.5 §6（同・後半）', "ai),anAIassistantbyAnthropic,draftedthetextbasedontheauthor'sinstructions,adjudication,andmaterials(publishedverificationseries,priorworks),withtheauthorreviewing,adjudicating,andrevising."),
 ('EN-3b §3.2（引用符内ピリオドの直後から始まる断片）', '"Limitations:singlemodel,singlelanguage,observationatthepromptlayer.'),
 ('EN-9 §5.4（同上・挿入位置が引用符の直後）', '"(3)Theseatbesidearecipientwholacksthecapacitytoverify'),
 ('EN-19 付録C（"broken."の直後から始まる断片）', 'Onlysimultaneous,adversarialauditingoffersaconditionaldefense'),
 ('EN-20a 付録D（①②③が一断片・②に括弧を挿入したため③まで含む断片が変化）', "③AI'sanswersleantowardwhatpleasesyou—listentotheopposingviewtoo."),
 ('EN-3a §3.2', 'therebytestingwhethertheblindingitselfactuallyheld'),
 ('EN-6 §4', 'theratemovessubstantiallywiththedesignofthesetting(47%→7%●).'),
 ('EN-7 §4A族', 'Measuredexamples:thecoexistenceofrecitingaclausewithfailingtocarryitout,'),
 ('EN-10a §6', 'immediateresponseateveryinstanceofviolation)'),
 ('EN-10b §6', 'thepromptlayerhasaceiling(●),andseparatedauditcanbedefeated(●).'),
 ('EN-12a §7.1', 'aplain-languageversionisintheappendixandderivativeteachingmaterials)'),
 ('EN-14a §8', 'Thefinalauditobtainedconfirmationthroughindependentrecalculationwithinthesamelineage,'),
 ('EN-17 謝辞', 'and[theout-of-lineagereviewerandtheinterested-partyreviewer'),
 ('EN-18 付録B', '|Coexistenceofrecitationandnon-fulfillment/self-fabricatedthresholds'),
 ('EN-20a 付録D', '②Ratherthanthewords"Iconfirmedit,"askwhatwasconfirmed,andhow.'),
 ('EN-20b 付録D', '⑤Pressthebuttonthatcan\'tbetakenbackwithyourownfinger.'),
 ('EN-21a 付録E', '|Elementarystatistics(Hanley1983)'),
 ('EN-21b 付録E', 'floor0–6.7%(SeriesA,cross-checkedagainstprimaryrecords)'),
 ('EN-21c 付録E', 'nodifferencenearthefloorforpurewarmth(SeriesA,AddendaBandD)'),
 ('EN-21d 付録E', '|Pointingoutapossibility;procedurenotestablished'),
]
lost = sents(E8) - sents(E)
used = set(); unexplained = []
for x in lost:
    hit = [t for t, e in EXPECTED if e in x or x in e]
    if hit: used.update(hit)
    else: unexplained.append(x)
print('   消えた断片: %d 件／期待リストで説明可能: %d 件' % (len(lost), len(lost) - len(unexplained)))
for x in sorted(unexplained): print('   ★説明の付かない消失 |', x[:100])
ck('汎用', '層H lost——説明の付かない消失ゼロ', not unexplained)
unused = [t for t, e in EXPECTED if t not in used]
for t in unused: print('   ⚠未使用の期待句:', t)
ck('汎用', '層H 期待リスト——未使用の期待句ゼロ', not unused, str(unused)[:120])

print('== 層N 数値の両言語一致（JA に現れる主要数値が EN 側にも現れるか） ==')
NUMS = ['85.6%', '74.4%', '6.7%', '46.7%', '85–95%', '0–10%', '0–30%', '54.0%', '52.0%', '26.0%',
        '37〜58%|37% and 58%', '4.81', 'df=4', 'p=0.31', '0.00642', '0.0134', '0.37', '13.3',
        '27/48', '21/48', '0.00453', '6.8', '0/3122', '0/66', '4.4%', '4.5%', '0/13', '20.6%', '23.1%',
        '294', '106/109', '88.4%', '260/294', '35.8%', '12/30', '16/30', '5–15/50|5〜15/50', '1/50',
        '13/13', '150', '66', '62%', '58%', '0/20', '1275|1,275', '0.50', '0.19', '0.14', '0.06',
        'κ=1.00', '2.5', '27', '48', '31', '90', '110', '119']
miss = []
for spec in NUMS:
    alts = spec.split('|')
    if not any(a.replace('〜', ' and ') in E or a in E for a in alts): miss.append(spec)
ck('汎用', '主要数値の EN 側存在（%d件中）' % len(NUMS), not miss, '不在: ' + str(miss) if miss else '')

print('== 層F 定数の再計算（EN 記載値の算術） ==')
den = comb(60, 28); po = comb(30, 12) * comb(30, 16) / den
p2 = sum(comb(30, x) * comb(30, 28 - x) / den for x in range(0, 29)
         if comb(30, x) * comb(30, 28 - x) / den <= po * 1.000001)
ck('汎用', 'Fisher=%.4f（JA §7.1 の 12/30 vs 16/30）' % p2, abs(p2 - 0.4379) < 5e-4)
arms = [(11, 30), (16, 30), (12, 30), (26, 50), (29, 50)]; pp = sum(k for k, _ in arms) / 190
chi = sum((k - m * pp) ** 2 / (m * pp) + ((m - k) - m * (1 - pp)) ** 2 / (m * (1 - pp)) for k, m in arms)
ck('汎用', 'χ²=%.2f' % chi, abs(chi - 4.81) < 0.02)
pr = sum(comb(30, a) * 0.5 ** 30 * comb(30, b) * 0.5 ** 30
         for a in range(31) for b in range(31) if abs(a - b) / 30 * 100 >= 13.33)
ck('汎用', 'P(|差|≥13.3pt)=%.2f' % pr, abs(pr - 0.37) < 0.01)
ck('汎用', 'RR 0.50/0.19/0.14/0.06',
   [round(26/52, 2), round(7/37, 2), round(10/70, 2), round(5/90, 2)] == [0.50, 0.19, 0.14, 0.06])
ck('汎用', 'CP 4.4/20.6・260/294=88.4・39/109=35.8・三腕54.0/52.0/26.0',
   abs(100 * (1 - 0.05 ** (1 / 66)) - 4.4) < 0.1 and round(260/294*100, 1) == 88.4
   and round(39/109*100, 1) == 35.8
   and [round(27/50*100,1), round(26/50*100,1), round(13/50*100,1)] == [54.0, 52.0, 26.0])

print()
tot = sum(CNT.values())
print('=== 被覆の申告: 全%d検査 ＝ 汎用%d（版面・不変・差集合・数値の両言語一致・定数再計算）＋ 回帰%d ＋ 対応%d（JA↔EN の句対応——同期の脱落を捕まえる層。訳文の正しさは検査しない） ===' % (tot, CNT['汎用'], CNT['回帰'], CNT['対応']))
print('=== 本検査は回帰試験である。検査できないもの: 訳文の意味的正確さ・語調・術語選択の妥当性（人手の検分が要る）／')
print('    層Jの対句は起草者が選んだ対応であり、対応づけ自体の正しさは検査していない（循環）／')
print('    JA 側にあって層Jの対に載せていない変更があれば、この検査は素通りする。 ===')
print('=== NG %d件 ===' % len(NG))
for x in NG: print('  ', x)
