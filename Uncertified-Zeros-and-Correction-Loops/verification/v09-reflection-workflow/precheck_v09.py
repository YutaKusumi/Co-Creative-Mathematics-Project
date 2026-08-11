# -*- coding: utf-8 -*-
"""v0.9 提出前機械検査（回帰試験——新規の誤りは原理的に検出しない・被覆申告つき）。
実行: proposals ディレクトリで python precheck_v09.py"""
import io, re, difflib
rd = lambda p: io.open(p, encoding='utf-8').read()
V9 = rd('uncertified-zeros-v0.9-draft.md')
V8 = rd('_bundle_ew_v3/uncertified-zeros-and-correction-loops-JA.md')
NG = []
def ck(name, ok, d=''):
    print(('  OK  ' if ok else '!NG  ') + name + ('  ' + d if d else ''))
    if not ok: NG.append(name)
L = V9.split(chr(10))
ck('fence偶数', V9.count('```') % 2 == 0)
bad=[]; i=0
while i < len(L):
    if L[i].strip().startswith('|') and i+1 < len(L) and set(L[i+1].strip()) <= set('|-: '):
        nc=L[i].strip().strip('|').count('|'); j=i+2
        while j < len(L) and L[j].strip().startswith('|'):
            if L[j].strip().strip('|').count('|') != nc: bad.append(j+1)
            j += 1
        i=j
    else: i += 1
ck('表列数一致', not bad, str(bad))
ck('タグ型生<不在', not re.findall(r'<[a-zA-Z]', V9))
MARKS = [('A1','散らばった'),('A1b','検出力は約38%'),('A2','三腕併記でのみ引く'),('A13','算入する解釈は◐'),
 ('A4','表明の内部整合すら保証されない'),('A4b','この条件は満たされない'),('A16','痕跡と破局の共存66件'),
 ('A16b','連言〔正確な唱和∧適用の迂回〕を両方判定'),('A26','水準は前置き効果の証拠にならない'),
 ('A6','109件中39件'),('A7','検査＋即応が層である'),('A7b','別の失敗様式として'),('A8','含意接地0/3122'),
 ('A9','5〜15/50'),('A10','突き合わせを誰にも課さない設計では'),('A10b','採点規約の弁別力の上限'),
 ('A11','名乗りは申告であり、申告は検査を要する'),('A12','逐語掃引は初回実行で6件'),
 ('A14','D族の定義〔文脈の手がかり変化後の反復〕への適合が未判定'),('A17','ゼロ分子の統計規則の算術'),
 ('A18','盲検の部分的破れを検出した'),('A19','主文が機械選択であったこと'),('A20','著者本人であり独立の検証者ではない'),
 ('A21','独立の予想情報を含まないと開示された'),('A22','版固定の限界は一つ実際に縮んだ'),
 ('A23','二項標本の分解能の算術'),('A24','独立性の確保に条件づけられる'),('A25','型の外は見ていません'),
 ('A25i','照合不能」という正しいラベル'),('T1','抽選は毎回引き直される'),('T1b','配備する側にも同じ形で当たる（系）'),
 ('T2','捕まえたものが起草者の設計判断で消えた'),('T2b','検分者側の誤り計六件'),('T3','柵は自動では保たれない'),
 ('付B','連言両方を判定'),('付C','別様式として並置（系列A）'),('付D1','根拠をそれ以上たどれない言い切り'),
 ('付D2','守る証拠にはなりません'),('付D4','毎回の引き直し'),('付E1','自系列の算術実演'),
 ('付E2','盲検検証装置の発火'),('付G','同期対象として記帳'),('§8','起草者の申告のまま検分されていない')]
for k, m in MARKS: ck('A15対応:' + k, m in V9)
def sec(t, a, b): return t[t.find(a):t.find(b)]
ck('要旨不変', sec(V9,'## 要旨','**キーワード**') == sec(V8,'## 要旨','**キーワード**'))
ck('付録A不変', sec(V9,'## 付録A','## 付録B') == sec(V8,'## 付録A','## 付録B'))
nrm = lambda s: re.sub(r'[*>\s`]', '', s); N9 = nrm(V9)
for kw in ['85–95pt','を付した言明のうち独断型','検出できたはずであり','監査下ですら','輪の外の目',
           '持ちこたえた','同時に見落とした','唯一の実測','最大の効果','定義水準で適合','ほぼすべて']:
    ck('禁句不在:' + kw, kw not in N9)
d8, d9 = V8.split(chr(10)), V9.split(chr(10))
ch = [op for op in difflib.SequenceMatcher(None, d8, d9).get_opcodes() if op[0] != 'equal']
print('変更ハンク %d 箇所 / %d -> %d 行' % (len(ch), len(d8), len(d9)))
print('=== 被覆の申告: 版面3＋A15対応43＋不変2＋禁句11＝全59検査（回帰・必在中心——新規の誤りは検出しない） ===')
print('=== NG %d件 ===' % len(NG))
for x in NG: print('  ', x)
