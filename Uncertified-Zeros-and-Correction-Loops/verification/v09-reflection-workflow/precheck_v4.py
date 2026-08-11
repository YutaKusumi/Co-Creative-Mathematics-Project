# -*- coding: utf-8 -*-
"""提出前機械検査 v2（対応表 v4 用・層E=版間回帰を初適用）
【性格の宣言】本検査は回帰試験である。検出対象は既知の誤りの再発と、確定した訂正の実装の有無に
限られ、新規の誤りは原理的に検出しない。層D2（必在）は訂正文の存在のみを検査し、正しさは検査しない。
未実装の二層（検分者の記述への適用・自分の限定を自分の主典拠に当てる）は人手で行う。
実行: proposals ディレクトリで `python precheck_v4.py`（相対パス）。"""
import io, re, os
from math import comb, exp

B = os.path.join('.', '_bundle_ew_v3')
rd = lambda p: io.open(p, encoding='utf-8').read()
V4 = rd('EW-reflection-map-v4-2026-08-10.md')
V3 = rd('EW-reflection-map-v3-2026-08-10.md')
GEN = rd(os.path.join(B, 'uncertified-zeros-and-correction-loops-JA.md'))
E   = rd(os.path.join(B, 'addendum-E-results.md'))
C   = rd(os.path.join(B, 'addendum-C-results.md'))
D   = rd(os.path.join(B, 'addendum-D-results.md'))
CP  = rd(os.path.join(B, 'current-position-2026-08-08.md'))
T0  = rd(os.path.join(B, 'temp0-control-results.md'))
W   = rd(os.path.join(B, 'addendum-W-results.md'))

nrm = lambda s: re.sub(r'[*>\s`]', '', s)
N4  = nrm(V4)
L4  = V4.split('\n')
NG = []; CNT = {'汎用': 0, '回帰': 0, '必在': 0}
def ck(layer, cat, name, ok, detail=''):
    CNT[cat] += 1
    print(('  OK  ' if ok else '★NG  ') + f'[{layer}/{cat}] {name}' + (f'  {detail}' if detail else ''))
    if not ok: NG.append((layer, name, detail))

print('◆層A 版面（生テキスト——版面検査ゆえ）')
ck('A', '汎用', 'コードフェンス偶数', V4.count('```') % 2 == 0, f'{V4.count("```")}個')
bad = []
i = 0
while i < len(L4):
    if L4[i].strip().startswith('|') and i+1 < len(L4) and set(L4[i+1].strip()) <= set('|-: '):
        nc = L4[i].strip().strip('|').count('|'); j = i+2
        while j < len(L4) and L4[j].strip().startswith('|'):
            if L4[j].strip().strip('|').count('|') != nc: bad.append(j+1)
            j += 1
        i = j
    else: i += 1
ck('A', '汎用', '表の列数一致', not bad, str(bad))
raw = [i+1 for i,l in enumerate(L4) if re.search(r'[a-zA-Z0-9]<[a-zA-Z0-9]', l) and '`' not in l]
ck('A', '汎用', '生の < 記号', not raw, str(raw))

print('◆層B 参照実在（見出し照合——部分文字列でなく）')
def bare_secs(t):
    out = set()
    for m in re.finditer(r'§(\d+(?:\.\d+)?)', t):
        win = t[max(0, m.start()-10):m.start()]
        if any(k in win for k in ('temp0','W ','E ','追補','温度0','同 ','v1','v2','v3','v4','C ','D ')):
            continue
        out.add(m.group(1))
    return sorted(out)
bare = bare_secs(V4)
gh = set(re.findall(r'^#{1,4}\s+(\d+(?:\.\d+)?)[\s\.．]', GEN, re.M))
for s in bare:
    ck('B', '汎用', f'原典 見出し §{s}', s in gh)
for ap in sorted(set(re.findall(r'付録([A-G])', V4))):
    ck('B', '汎用', f'原典 見出し 付録{ap}', bool(re.search(rf'^##\s*付録{ap}', GEN, re.M)))

print('◆層C 同一文書内の突合（正規化・最上級は拡張パターン・許容は同一行のみ）')
ALLOW = ('撤回','削除','訂正','誤り','比較集合','不使用','ではなく','とは書かない','読まない','しない')
sup = []
for i,l in enumerate(L4):
    if re.search(r'最も.{0,6}(強|高|精緻|堅|純度|大き|重|良)|最大|唯一|最良|初の|初めて', l):
        if any(a in nrm(l) for a in ALLOW) or '初適用' in l or '初発火' in l: continue
        if '最良集合' in l or '拡張パターン' in l: continue          # 術語・検査自身の説明行
        outside = re.sub(r'「[^」]*」', '', l)                        # 「」内の引用は言及であり使用でない
        if re.search(r'最も.{0,6}(強|高|精緻|堅|純度|大き|重|良)|最大|唯一|最良|初の|初めて', outside):
            sup.append((i+1, l.strip()[:60]))
ck('C', '汎用', '比較集合なしの最上級・唯一（同一行許容）', not sup, str(sup))
ck('C', '回帰', '「唯一の実測」不在', N4.count('唯一の実測') == 0)
ck('C', '回帰', 'A6 正分母（260/294・109件中39件・294/294・106/109）',
   all(k in N4 for k in ['88.4%（260/294）','109件中39件','294/294','106/109']))
ck('C', '回帰', 'E側確度の分離（測定●・解釈◐）', '測定は●確証' in N4 and '解釈が◐' in N4)

print('◆層D 禁句掃引（正規化・許容は同一行のみ・許容件も印字）')
BAN = ['最大の効果','を付した言明のうち独断型','監査下ですら','輪の外の目','持ちこたえた',
       '同時に見落とした','揃って外した','幅を約2倍','完全に出力','機械検査に合格','四段',
       '中立腕','温度0対照が候補を弱めた','実測が支持','原典が強くなる','阿弥陀が裏取り済み',
       '独立に取った二回目','85–95pt級','85-95pt級','検出できたはずであり','ほぼすべて',
       '同一の付託経路','一腕は率を±13','定義水準で適合','逐語で適合','抹消','裏取り済み',
       '歴史的に達成された規模']
ALLOWD = ('撤回','削除','訂正','誤り','合わない','ではなく','成立していない','不成立','数えることはできない','無い記述')
for kw in BAN:
    hits = [(i+1, l.strip()[:56]) for i,l in enumerate(L4) if kw in nrm(l)]
    def ok_hit(i):
        line = L4[i-1]
        if any(a in nrm(line) for a in ALLOWD): return True
        return kw in re.sub(r'[*>\s`]', '', ''.join(re.findall(r'「[^」]*」', line)))  # 「」内の言及
    bad = [(i,s) for i,s in hits if not ok_hit(i)]
    ok = not bad
    tag = f'{len(hits)}件' + (f'・許容 {[h[0] for h in hits]}' if hits and ok else '')
    ck('D', '回帰', f'「{kw}」', ok, tag if ok else str(bad))

print('◆層D2 必在（訂正の実装確認のみ——正しさは検査しない）')
MUST = ['75〜95pt','RR約0.55','正本として継承','で約56%','で約73%','で約97%','検出力は約38%','標準誤差は約9pt',
        '13pt程度まで開く','計14件','8件はv2起草者','語の強度についての探索','名乗りが記録と一致せず',
        '共通原因型','系統相関型','抽選は毎回引き直される','選べない配備では上がらない',
        '検分者側の誤り六件を捕捉','連言','追補C§6','完全性の機械検査','ε<3/n','付録D(一)④',
        '本文のみ（付録Cには写さない）','回帰試験である','実装可能性には何も足さない',
        '●＝検出27/48','導出値','G4自身が','この同定は宝生','三度目の是認がどの参加者のものかは',
        '天井であり、採点規約の弁別力の上限','無効として記帳','三重計算一致']
for kw in MUST:
    ck('D2', '必在', f'「{kw[:22]}」', nrm(kw) in N4)

print('◆層E 版間回帰（新設・v3→v4）')
h3 = set(re.findall(r'^### (A\d+|T\d+)', V3, re.M)); h4 = set(re.findall(r'^### (A\d+|T\d+)', V4, re.M))
ck('E', '汎用', '項目見出し集合の一致（v3=v4）', h3 == h4, f'差: {sorted(h3^h4)}')
def a15keys(t):
    m = re.search(r'### A15.*?(?=\n---|\n## )', t, re.S)
    rows = [l for l in m.group(0).split('\n') if l.strip().startswith('|')] if m else []
    ks = set()
    for r in rows: ks |= set(re.findall(r'(A\d+|T\d+|要旨)', r))
    return ks
k3, k4 = a15keys(V3), a15keys(V4)
ck('E', '汎用', 'A15 表: v3 の項目集合 ⊆ v4（回帰なし）', k3 <= k4, f'欠落: {sorted(k3-k4)}')
allk = ({f'A{i}' for i in range(1,27)} | {'T1','T2','T3','要旨'}) - {'A15'}   # A15 は表自身
ck('E', '汎用', 'A15 表: 全項目（A1〜A26・T1〜T3・要旨）被覆', allk <= k4, f'欠落: {sorted(allk-k4)}')
for c in ('C4','C8','C11','C12','C13'):
    ck('E', '回帰', f'フェンス {c} 存置', c in V4)

print('◆出所照合（一次資料: 原典・E・W・C・D・現在地・温度0——定数の再導出）')
den = comb(60,28); p_obs = comb(30,12)*comb(30,16)/den
p2 = sum(comb(30,x)*comb(30,28-x)/den for x in range(max(0,28-30),min(30,28)+1)
         if comb(30,x)*comb(30,28-x)/den <= p_obs+1e-12)
ck('src', '汎用', f'Fisher 12/30vs16/30={p2:.4f}', abs(p2-0.4379) < 5e-4)
arms=[(11,30),(16,30),(12,30),(26,50),(29,50)]; pp=sum(k for k,_ in arms)/190
chi=sum((k-m*pp)**2/(m*pp)+((m-k)-m*(1-pp))**2/(m*(1-pp)) for k,m in arms)
ck('src', '汎用', f'χ²={chi:.2f} p={exp(-chi/2)*(1+chi/2):.3f}', abs(chi-4.81)<0.02)
def fisher2(k1,k2,m=50):
    aa,bb,cc,dd=k1,m-k1,k2,m-k2; row,col,N=aa+bb,aa+cc,2*m
    dn=comb(N,col); po=comb(row,aa)*comb(N-row,col-aa)/dn
    return sum(comb(row,x)*comb(N-row,col-x)/dn for x in range(max(0,col-(N-row)),min(row,col)+1)
               if comb(row,x)*comb(N-row,col-x)/dn <= po*(1+1e-9))
def power(p1,p2n,m=50,al=0.025):
    f1=[comb(m,k)*p1**k*(1-p1)**(m-k) for k in range(m+1)]
    f2=[comb(m,k)*p2n**k*(1-p2n)**(m-k) for k in range(m+1)]
    return 100*sum(f1[k1]*f2[k2] for k1 in range(m+1) for k2 in range(m+1)
                   if f1[k1]*f2[k2]>=1e-12 and fisher2(k1,k2,m)<=al)
pw=[power(0.58,(58-dd)/100) for dd in (26,30,40)]
ck('src', '汎用', f'検出力 {pw[0]:.1f}/{pw[1]:.1f}/{pw[2]:.1f}%',
   abs(pw[0]-56.2)<0.15 and abs(pw[1]-72.9)<0.15 and abs(pw[2]-96.9)<0.15)
ck('src', '汎用', 'SE 9.1/12.9pt', round((0.25/30)**0.5*100,1)==9.1 and round((0.5/30)**0.5*100,1)==12.9)
ck('src', '汎用', '効果量 75=85−10・95=95−0・14=11+3・8+4+2=14', 85-10==75 and 95-0==95 and 11+3==14 and 8+4+2==14)
ck('src', '汎用', '追補C「3.1腕でなお破局を選んだのは3件」', '3.1腕でなお破局を選んだのは3件' in C)
ck('src', '汎用', '追補C A5（世俗版）3/30', bool(re.search(r'A5（世俗版）\s*\|\s*3/30', C)))
ck('src', '汎用', '追補D「17件に付与」', '17件に付与' in D)
ck('src', '汎用', '現在地「6件を捕捉」', '6件を捕捉' in CP)
ck('src', '汎用', '追補E 52.0/26.0 実在', '52.0' in E and '26.0' in E)
ck('src', '汎用', 'W §3.4「≥90確信∧独断型」', '≥90確信∧独断型' in W)
ck('src', '汎用', 'temp0「回付バンドル」「この一語の不正確」', '回付バンドル' in T0 and 'この一語の不正確' in nrm(T0))

print()
tot = sum(CNT.values())
print(f'=== 被覆の申告: 全{tot}検査 ＝ 汎用{CNT["汎用"]}件（新種を捕まえうる）＋ 回帰{CNT["回帰"]}件'
      f'（既知の再発検査）＋ 必在{CNT["必在"]}件（実装確認のみ・正しさは検査しない） ===')
print('=== 本検査は回帰試験である。NG 0 は「既知の誤りの再発なし・確定訂正の実装済み」を意味し、')
print('    「誤りなし」を意味しない。検分者の記述への適用・自分の限定を自分の主典拠に当てる、の二層は人手で行う。 ===')
print(f'=== NG {len(NG)}件 ===')
for x in NG: print('   ', x)
