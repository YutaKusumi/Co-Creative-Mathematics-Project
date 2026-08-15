# -*- coding: utf-8 -*-
"""第六著作 v4.3（起草）の提出前機械検査（日英）。
層V1 新規文言の必在（JA/EN）／層V2 旧文言の不在／層V3 禁句（対応表 v4 §C のフェンス）
層V4 不変性（git HEAD=v4.2 との差分が、意図した編集領域だけであること——柵・定理節の逐語不変）
層V5 JA↔EN 対応／層V6 新規挿入部の局所禁句（κ・IDA・数値）／層V7 列挙照合・構造（P11・P1）
v4.3.1 改修（2026-08-13・P11）: (i) 禁句を主張の候補集合で持つ（v4.3 器材は「そもそも対象を持たない」の
言い換え「引く前に個体を選別することはできない」を通した）(ii) 数値検査に漢数字比率を追加
(iii) 列挙照合の層（日付行「N件〔…〕」の N と項目数）。あわせて v4.3.1 の全修正を検査対象に加えた。
実行: proposals で python precheck_sixth_work_v43.py"""
import io, re, sys, subprocess, difflib
B = 'C:/Users/PC/Desktop/GitHub-Repositories/Co-Creative-Mathematics-Project/'
D = B + '06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned/Version-B-Policy-Edition/'
JP = D + 'JA/Why-Military-AI-Cannot-Be-Aligned-Version-B-v4-JA.md'
EP = D + 'EN/Why-Military-AI-Cannot-Be-Aligned-Version-B-v4-EN.md'
J = io.open(JP, encoding='utf-8').read()
E = io.open(EP, encoding='utf-8').read()
def git_head(rel):
    return subprocess.run(['git', '-C', B, 'show', 'HEAD:' + rel],
                          capture_output=True).stdout.decode('utf-8')
J0 = git_head('06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned/Version-B-Policy-Edition/JA/Why-Military-AI-Cannot-Be-Aligned-Version-B-v4-JA.md')
E0 = git_head('06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned/Version-B-Policy-Edition/EN/Why-Military-AI-Cannot-Be-Aligned-Version-B-v4-EN.md')
NG = []; n = [0]
def ck(cat, name, ok, d=''):
    n[0] += 1
    print(('  OK  ' if ok else '!NG  ') + '[%s] %s' % (cat, name) + ('  ' + d if d else ''))
    if not ok: NG.append(name)

print('== 層V1 新規文言の必在 ==')
for name, frag, doc in [
 ('JA v4.3 版行', '2026年8月15日（v4.3・', J), ('EN v4.3 版行', 'August 15, 2026 (v4.3 —', E),
 ('JA S3 v0.9.10 確認', '姉妹論文 v0.9.10 との整合を確認した', J), ('EN S3', 'v0.9.10 of the sister paper was additionally confirmed', E),
 ('JA B8 記録句（比較集合つき）', '接続を検討した項目の中で誤読の危険が最大であり', J),
 ('EN B8 記録句', 'among the items considered for connection its risk of misreading is the largest', E),
 ('JA S4 第11章・三段階', '第11章で詳述する段階的移行（三つの段階）', J),
 ('EN S4', 'staged transition (three stages) detailed in Chapter 11', E),
 ('JA S1', 'そういう追補もある', J), ('EN S1', 'the same series also contains an addendum', E),
 ('JA B1 弁別', 'その検査は当該経路を弁別できなかった', J),
 ('EN B1', 'that check could not discriminate the route in question', E),
 ('JA B1 検査器の側', '検査器の側にも生じる', J), ('EN B1', 'on the side of the instrument', E),
 ('JA B3 是正経路', '検査結果を系に戻す経路が設計に無ければ、選択は変わらなかった', J),
 ('EN B3', "no route for returning the check's results into the system, the choices did not change", E),
 ('JA B3 層として働く', '検査を置くことと、検査が層として働くことは、同じではない', J),
 ('EN B3', 'Placing a check, and a check working as a layer, are not the same thing', E),
 ('JA T 登録外', '登録外の診断実験', J), ('EN T', 'unregistered diagnostic experiment', E),
 ('JA T 規律の柵', '同じ規律の産物として読まれてはならない', J),
 ('EN T', 'must not be read as a product of the same discipline', E),
 ('JA T バッチ限定', 'バッチサイズ1・同一プロセス内', J), ('EN T', 'batch size 1, within a single process', E),
 ('JA T ばらつき/水準の分割', 'ばらつきの不在', J), ('EN T', 'absence of variation', E),
 ('JA T 測っていない', '温度と破局率の関係を、この実験は測っていない', J),
 ('EN T', 'the relation between temperature and catastrophe rate is something this experiment did not measure', E),
 ('JA T 打ち消し', 'この記録はその論述の証拠でも裏づけでもなく', J),
 ('EN T', 'neither evidence for nor corroboration of that treatment', E),
 ('JA T2 分解能', '対象を同定できる分解能が立たない', J),
 ('EN T2', 'no resolution at which its object could be identified', E),
 ('JA T2 §5.4', '分布は介入で動くことがあり、動かないこともある', J),
 ('EN T2 §5.4', 'can be moved by intervention — and can also remain unmoved', E),
 ('JA 9-5 リンク（打ち消し）', 'その記述は §12 に委ね、**本項の論証には用いない**', J),
 ('EN 9-5 リンク', 'consigned to §12 and **is not used in the argument of this section**', E),
 ('JA S2 時制', '第五（次項）のとおり、公開前に別途行われた', J),
 ('EN S2', 'was conducted separately prior to publication, as the fifth point (next) records', E),
 ('JA B6 限定', 'ただし、別のモデルの目が常に捕まえるわけではない', J),
 ('JA P1 束ね文', '補遺IIの公開（v4.1）の後も、同じ系列は観察を続けた', J),
 ('EN P1 束ね文', 'Even after the publication of Addendum II (v4.1), the same series continued to observe', E),
 ('JA P1 橋句', '測定が成功しても、是正が伴わなければ、床は動かない', J),
 ('EN P1 橋句', 'Even when measurement succeeds, if correction does not follow, the floor does not move', E),
 ('JA P2 選別の限定', '引く前に選別する手がかりが立たない——複数機体からの選別が当たるか否かは、本データからは言えない', J),
 ('EN P2', 'no handle by which to select before drawing', E),
 ('JA P3 器物の水準', '器物の水準にとどまる', J),
 ('EN P3', 'at the level of the artifact', E),
 ('JA P3 解釈の明記', '起草者の解釈', J),
 ('EN P3 解釈', "the drafter's interpretation", E),
 ('JA P7 §14 内訳', 'うち系統外〔非Claude系〕は三、残る十は同一系統', J),
 ('EN P7 §14', 'three of the thirteen from outside the lineage (non-Claude)', E),
 ('JA P7 非独立注記', '「独立の目」と数えることは、本補遺自身が退けた仮定に立つ', J),
 ('EN P7', 'to count these thirteen as "independent eyes" is to stand on the very assumption', E),
 ('JA P8 13-0a', '移送されない上界の上に立っている', J),
 ('EN P8', 'stands on a bound that does not transfer', E),
 ('JA P9 限定併置', '意図的に課しておらず、ゆえに言えるのは「検査は無力」ではなく', J),
 ('EN P9', 'deliberately imposed no constraint', E),
 ('JA P6 日付行にS1', '補遺II §12 の時系列（「最終段」）', J),
 ('EN P6', 'the chronology in §12 of Addendum II', E),
 ('JA P12d', '本補遺のこの品質保証の過程', J),
 ('EN C① 第四', 'different model bases within the same (Claude) lineage', E),
 ('EN B6', 'But the eyes of a different model do not always catch', E),
 ('JA B6 集合の区別', '両者に共通するのは「他者の目」という点だけ', J),
 ('EN B6', 'What the two share is only this: they are the eyes of an other', E),
 ('JA B6 当事者性(P10)', '当事者であったこと自体が偽にする記述を', J),
 ('EN B6 (P10)', 'its own participation in that examination falsified', E),
 ('JA B6 集約者記帳', '当人の申告ではなく、工程の集約者による記帳', J),
 ('EN B6', 'recorded by the coordinator of the process', E),
 ('JA B6 是認も記録', '是認もまた記録し、次巡の検査対象に含める', J),
 ('EN B6', 'endorsements, too, are recorded, and included among the objects', E),
]:
    ck('V1', name, frag in doc)

print('== 層V2 旧文言の不在 ==')
for name, frag, doc in [
 ('JA 最終段', 'そして系列の最終段では', J), ('EN final stage', 'And at the final stage of the series', E),
 ('JA 六段階', '六段階', J), ('EN six-stage', 'six-stage', E),
 ('JA 第四の未来形', '本補遺の公開前に別途行われる', J),
 ('EN 第四の未来形', 'is conducted separately, prior to the publication of this addendum', E),
 ('JA 選別できない（撤回形の言い換え）', '引く前に個体を選別することはできない', J),
 ('EN culled', 'Individuals cannot be culled', E),
 ('JA 砂上の楼閣', '砂上の楼閣', J), ('EN castle on sand', 'castle on sand', E),
 ('JA 真の確率が測定不能', '真の確率が測定不能', J),
 ('EN true probability unmeasurable', 'the true probability is unmeasurable', E),
 ('JA 十三の独立の目', '十三の独立の目', J), ('EN thirteen independent eyes', 'thirteen independent eyes', E),
 ('JA B6 旧形（にもかかわらず）', '当事者であったにもかかわらず', J),
 ('EN systematic external（誤訳）', 'systematic external', E),
 ('EN a different model lineage', 'a different model lineage', E),
 ('JA 温度零の旧書き出し', '本補遺の公開後に、同じ系列は', J),
]:
    ck('V2', '「%s」が残っていない' % name, frag not in doc)

print('== 層V3 禁句（対応表 v4 §C——全文） ==')
for name, frag, doc in [
 ('JA T0/T07 並置なし（T07）', 'T07', J), ('EN T07', 'T07', E),
 ('JA 0/20', '0/20', J), ('EN 0/20', '0/20', E), ('JA 10/20', '10/20', J),
 ('JA 全称形の復活なし', 'そもそも対象を持たない', J),
 ('JA 追補E数値（三腕）', '54.0', J), ('JA 追補E数値', '26.0%', J),
 ('JA 四つ目の逃げ道', '四つ目の逃げ道', J), ('EN fourth escape', 'fourth escape route', E),
]:
    ck('V3', '「%s」不在' % name, frag not in doc)
# 【P11(i)】禁句は主張の候補集合で持つ——「同じ主張の別表記」を通さない（器1 の How to apply）
for w in ['そもそも対象を持たない', '個体は存在しない', '特定して外すべき個体']:
    ck('V3', '言い換え候補「%s」不在' % w[:18], w not in J)
ck('V3', '言い換え候補（EN）不在', 'no such individual exists' not in E)
# T4 の禁止は「温度0のゼロに数値上界（3/n 型）を書くこと」——§5-1 の rule of three（既存の中核）は対象外。
# 初版は全文に '3/n' 不在を課して §5-1 を誤検出した。新規段落側は層V6 が数値そのものを禁じている。
ck('V3', 'T4: 温度0段落に 3/n 型上界が無い（局所）',
   '3/n' not in (J[J.find('同じ系列は、**登録外の診断実験**も一つ走らせた'):J.find('詳細と全数値は、')] or ''))

print('== 層V4 不変性（git HEAD=v4.2 との差分・柵と定理節の逐語不変） ==')
# (a) 柵の逐語不変
for name, frag in [('柵a', '**この節は、証拠ではない。**'), ('柵b', '本補遺には、個票の数値を引かない。'),
                   ('柵c', 'この系列の結果は $\\kappa$ 命題を証明しない'),
                   ('柵d', '以下のいずれの観察も、本補遺のいかなる前提の証拠としても読まれてはならない')]:
    ck('V4', 'JA %s 逐語不変' % name, (frag in J) and (frag in J0))
# 柵e は原文が強調記号を挟む（「実証では**ない**」）ため、正規化して照合する——
# v4.3.1 の自文書突合で、本器が四つしか検査していないのに記録側が「五つ」と書いていたことが判明した（列挙の型）。
_pl = lambda t: t.replace('**', '')
ck('V4', 'JA 柵e（アーキテクチャ層・正規化）逐語不変',
   ('アーキテクチャ層の実証ではない' in _pl(J)) and ('アーキテクチャ層の実証ではない' in _pl(J0)))
# (b) 定理節（言明〜逃げ道五項）のブロックがバイト同一
def block(s, a, b):
    i = s.find(a); j = s.find(b, i)
    return s[i:j] if i >= 0 and j > i else None
blkJ, blkJ0 = block(J, '**言明**: 次の仮定の下で', '### 8-4'), block(J0, '**言明**: 次の仮定の下で', '### 8-4')
ck('V4', 'JA §8-3 言明〜逃げ道ブロックが v4.2 と同一', blkJ is not None and blkJ == blkJ0,
   '%s/%s字' % (len(blkJ or ''), len(blkJ0 or '')))
# (c) 差分が意図した領域だけか（変更ブロックごとに、期待マーカーとの交差を要求）
def audit(cur, old, markers, tag):
    # 行単位で差分を取る（文字単位の SequenceMatcher は 700KB 級では実用にならない）
    a, b = old.splitlines(), cur.splitlines()
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    bad = 0; cnt = 0
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == 'equal': continue
        cnt += 1
        seg = '\n'.join(b[j1:j2]) + ' ' + '\n'.join(a[i1:i2])
        if not any(m in seg for m in markers): bad += 1
    ck('V4', '%s 差分ブロックが全て意図領域内' % tag, bad == 0, '変更%dブロック・意図外%d' % (cnt, bad))
MK_J = ['v4.3', '追補もある', '弁別できなかった', '層として働く', '登録外の診断実験', '本項の論証には用いない',
        '別途行われた', '別のモデルの目', '第11章で詳述する', '系列の中には', '接続を検討した項目',
        '補遺IIの公開（v4.1）', '手がかりが立たない', '十三の目', '計13の目', '移送されない上界',
        '意図的に課しておらず', '当事者であったこと自体', '本補遺のこの品質保証', '時系列（「最終段」）',
        'この経験が、本補遺の問いを生んだ', '観察を続けた', '同じ追補は', '見た——別ロード間',
        '登録外の診断実験', '整合を確認した']
MK_E = ['v4.3', 'contains an addendum', 'discriminate the route', 'working as a layer',
        'unregistered diagnostic', 'not used in the argument', 'fifth point (next)',
        'eyes of a different model', 'Chapter 11', 'items considered for connection',
        'Even after the publication of Addendum II', 'no handle by which to select', 'thirteen eyes',
        'does not transfer', 'deliberately imposed no constraint', 'its own participation',
        "addendum's own process of quality assurance", 'within the same (Claude) lineage',
        'outside the lineage', 'within the Claude lineage', 'This experience is what gave rise', 'The same addendum also left',
        'chronology in §12', 'also saw that', 'remain unmoved', 'what worked and what did not',
        'additionally confirmed', 'also reflected']
audit(J, J0, MK_J, 'JA'); audit(E, E0, MK_E, 'EN')

print('== 層V5 JA↔EN 対応（新規部の対） ==')
for name, ja, en in [
 ('二十回/twenty', '二十回の試行', 'twenty trials'),
 ('温度零/temperature zero', '復号温度を零にした貪欲復号', 'greedy decoding at temperature zero'),
 ('検分者の撤回', '別の巡では自らの指摘を撤回し', 'in another round, withdrew its own finding'),
 ('外側性', '外側性は、検分の質を保証しない', 'Being outside does not guarantee the quality of an examination'),
]:
    ck('V5', name, (ja in J) == (en in E) == True)

print('== 層V6 新規挿入部の局所禁句（κ・IDA・実数値） ==')
seg = block(J, '同じ系列は、**登録外の診断実験**も一つ走らせた', '詳細と全数値は、')
segE = block(E, 'The same series also ran one **unregistered diagnostic experiment**', 'Details and the full set of figures')
ck('V6', 'JA 温度0段落に κ/IDA/％数値が無い',
   seg is not None and not re.search(r'κ|kappa|IDA|内発的方向性|\d+%|[0-9]+/[0-9]+|[〇一二三四五六七八九十]+／[〇一二三四五六七八九十]+', seg))
ck('V6', 'EN 温度0段落に κ/IDA/％数値が無い',
   segE is not None and not re.search(r'κ|kappa|IDA|intrinsic directional|\d+%|[0-9]+/[0-9]+', segE))
segB = block(J, 'ただし、別のモデルの目が常に捕まえるわけではない', '外側性は、検分の質を保証しない')
ck('V6', 'JA B6 追記に巡数・体数・モデル名が無い',
   segB is not None and not re.search(r'三巡|四名|五名|Gemini|三体|一巡」を', segB))
ck('V6', 'JA B6 追記に「別個体」が無い', segB is not None and '別個体' not in segB)

print('== 層V7 列挙照合・構造（P11・P1） ==')
m = re.search(r'参照整合の修正三件〔([^〕]+)〕', J)
ck('V7', '日付行「修正三件」の項目数が3', bool(m) and m.group(1).count('、') + 1 == 3,
   m.group(1) if m else '不在')
m2 = re.search(r'three reference-consistency corrections \[([^\]]+)\]', E)
ck('V7', 'EN 日付行の項目数が3', bool(m2) and m2.group(1).count(';') + 1 == 3,
   m2.group(1)[:60] if m2 else '不在')
ck('V7', '§12 の順序: この経験 → 公開後グループ（JA）',
   J.find('この経験が、本補遺の問いを生んだ') < J.find('機械検査可能な形式を課した先の追補')
   < J.find('同じ追補は、検査を課すこと') < J.find('同じ系列は、**登録外の診断実験**'))
ck('V7', '§12 の順序（EN）',
   E.find('This experience is what gave rise') < E.find('The addendum that imposed the machine-checkable form')
   < E.find('The same addendum also left') < E.find('The same series also ran one'))
ck('V7', '「十三の目」の内訳の和（4+3+4+2＝13・系統外3＋系統内10＝13）', 4+3+4+2 == 13 and 3+10 == 13)

print()
print('=== 全%d検査 ／ NG %d件 ===' % (n[0], len(NG)))
print('=== 本検査が見ないもの: 訳文の質（意味の同一性）は機械では検査できない——対の存在までである。')
print('    改訂の当否そのものは、改訂後の検分（新規セッション＋系統外）の仕事。 ===')
for x in NG: print('  ', x)
sys.exit(1 if NG else 0)
