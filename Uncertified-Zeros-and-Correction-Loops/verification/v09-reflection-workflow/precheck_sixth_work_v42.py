# -*- coding: utf-8 -*-
"""第六著作 v4.2 の提出前機械検査——回帰試験（被覆申告つき）。
層S1 追加された限定の必在（日英）／層S2 触れないと決めたものの不変（柵・定理節・追補E 非接続）
層S3 日英の同時性（片側だけ古くならないこと）／層S4 一次記録の不改変（v4-preparation を触っていない）
層S5 原典との対応（限定の出所が原典 v0.9.9 に逐語で存在すること）
実行: proposals で python precheck_sixth_work_v42.py"""
import io, re, sys, hashlib
R = 'C:/Users/PC/Desktop/GitHub-Repositories/Co-Creative-Mathematics-Project/'
S = R + '06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned/Version-B-Policy-Edition/'
rd = lambda p: io.open(p, encoding='utf-8').read()
JA = rd(S + 'JA/Why-Military-AI-Cannot-Be-Aligned-Version-B-v4-JA.md')
EN = rd(S + 'EN/Why-Military-AI-Cannot-Be-Aligned-Version-B-v4-EN.md')
ORIG = rd(R + 'Uncertified-Zeros-and-Correction-Loops/JA/uncertified-zeros-and-correction-loops-JA.md')
NG = []; CNT = {'必在': 0, '不変': 0, '同時': 0, '一次': 0, '対応': 0}
def ck(cat, name, ok, d=''):
    CNT[cat] += 1
    print(('  OK  ' if ok else '!NG  ') + '[%s] %s' % (cat, name) + ('  ' + d if d else ''))
    if not ok: NG.append(name)

print('== 層S1 追加した限定の必在 ==')
for k in ['ただし、どの精緻化でも効くわけではない', '機械検査可能な形式を課す会計の要求',
          'これは、後段の「測れなかった」とは別の型である', '検出の余地がある基底の下で測り、そのうえで動かなかった',
          '帰無は不在の証明ではなく', 'v4.2・§12 に追補W の限定を追加']:
    ck('必在', 'JA「%s」' % k[:24], k in JA)
for k in ['but not every refinement does', 'a demand for accounting in a machine-checkable form',
          'a different type from the "could not be measured" described below',
          'left room for detection, and still nothing moved', 'A null, however, is not proof of absence',
          'v4.2 — a qualification from Addendum W']:
    ck('必在', 'EN「%s」' % k[:30], k in EN)

print('== 層S2 触れないと決めたものの不変 ==')
FENCE_JA = ['**この節は、証拠ではない。**', '本補遺には、個票の数値を引かない。',
            'この系列の結果は $\\kappa$ 命題を証明しない', '以下のいずれの観察も、本補遺のいかなる前提の証拠としても読まれてはならない']
for k in FENCE_JA: ck('不変', '§12 の柵「%s」' % k[:22], k in JA)
ck('不変', '結びの一文が不変', '下がった床と、認証されたゼロとの距離は、測定の努力によっては縮まらない。' in JA)
ck('不変', '追補C の記述が不変（37%→7%・p=0.0102）', '37% から 7% へ低減' in JA and 'p=0.0102' in JA)
ck('不変', '追補D の記述が不変（測れなかった）', '介入の効果を測定できる場そのものが成立しなかった' in JA)
print('   —— 追補E を接続していないこと（B7 原則不採用）——')
# 「追補E」の語自体は日付行の但し書き（「追補E は接続していない」）に現れるので、
# 検査するのは**E の中身**の不在とする（初版は語だけを見て、自分の但し書きを誤検出した）
_ja_wo_note = JA.replace('追補E は接続していない', '')
for k in ['追補E', '存在論的前置き', '54.0', '52.0', '26.0', '限界4', '執着の解消', '語彙圏']:
    ck('不変', 'JA に現れない「%s」（但し書きを除く）' % k, k not in _ja_wo_note)
_en_wo_note = EN.replace('Addendum E is not connected', '')
for k in ['Addendum E', 'ontological-positioning preamble', '54.0%', '26.0%', 'dissolution of attachment']:
    ck('不変', 'EN に現れない「%s」（但し書きを除く）' % k, k not in _en_wo_note)
print('   —— 定理節に混ぜていないこと（B4）——')
i = JA.find('# 8-3'); j = JA.find('\n## ', i + 10)
ck('不変', '§8-3 に「会計」「帰無」を持ち込んでいない',
   ('会計' not in JA[i:j]) and ('帰無' not in JA[i:j]) if i > 0 else False)

print('== 層S3 日英の同時性 ==')
ck('同時', 'JA/EN とも §12 に限定が入っている',
   ('どの精緻化でも効くわけではない' in JA) == ('but not every refinement does' in EN) is True)
ck('同時', 'JA/EN とも日付行が v4.2', ('v4.2' in JA) and ('v4.2' in EN))
ck('同時', '旧形（限定なしの太字）が両方から消えている',
   ('**外部制約層の精緻化は、実効を持つ。**' not in JA) and
   ('**Refinement of the external-constraint layer has a real effect.**' not in EN))

print('== 層S4 一次記録の不改変（v4-preparation を触っていない） ==')
import glob, os
for p in glob.glob(S + 'v4-preparation/**/supplement-II-draft-JA.md', recursive=True):
    t = rd(p)
    ck('一次', '不改変 %s' % os.path.basename(os.path.dirname(p))[:22],
       '**外部制約層の精緻化は、実効を持つ。**' in t and 'どの精緻化でも効くわけではない' not in t)

print('== 層S5 原典 v0.9.9 との対応（限定の出所） ==')
Z = [('どの精緻化でも効くわけではない', 'ただしどの介入でも動くわけではない'),
     ('機械検査可能な形式を課す会計', '機械検査可能な会計の強制は、検出余地のある基底（58%）の下で破局率を下げなかった'),
     ('排除できるのは大きな効果だけ', 'この帰無が排除できるのは大きな効果だけである'),
     ('帰無は不在の証明ではない', '帰無を不可避性の証拠と読まない')]
for name, src in Z:
    ck('対応', '%s ← 原典逐語' % name[:22], src in ORIG)

print()
tot = sum(CNT.values())
print('=== 被覆の申告: 全%d検査 ＝ 必在%d ＋ 不変%d（柵・追補C/D・追補E非接続・定理節）＋ 同時%d（日英）'
      '＋ 一次%d（草稿と監査パケットの不改変）＋ 対応%d（原典への出所照合） ===' %
      (tot, CNT['必在'], CNT['不変'], CNT['同時'], CNT['一次'], CNT['対応']))
print('=== 本検査が見ないもの: 追加した限定が第六著作の論証の流れに馴染むか（人手の読みが要る）／')
print('    B群の残り7項目（保留継続・再開の引き金は登録者裁定待ち）／英訳の語調。 ===')
print('=== NG %d件 ===' % len(NG))
for x in NG: print('  ', x)
sys.exit(1 if NG else 0)
