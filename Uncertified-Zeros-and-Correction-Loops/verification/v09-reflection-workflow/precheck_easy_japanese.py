# -*- coding: utf-8 -*-
"""やさしい日本語版要約（付録G(3)）の提出前機械検査——回帰試験（被覆申告つき）。
層E1 やさしい日本語の形式（一文の長さ・二重否定・むずかしい語）
層E2 md↔html の同一性（同じ内容の二文書は片側だけ古くなる——本工程が繰り返し捕まえた型）
層E3 必在（限定と成果の対・五箇条の全条）
層E4 降ろさないもの（統計・専門語・§10 の三腕）
層E5 原典 付録D(一)①〜⑤ との対応
実行: proposals で python precheck_easy_japanese.py"""
import io, re, sys
T = 'C:/Users/PC/Desktop/Ryokai-OS-Verification/proposals/_teaching/'
J = 'C:/Users/PC/Desktop/GitHub-Repositories/Co-Creative-Mathematics-Project/Uncertified-Zeros-and-Correction-Loops/JA/uncertified-zeros-and-correction-loops-JA.md'
rd = lambda p: io.open(p, encoding='utf-8').read()
MD = rd(T + 'easy-japanese-summary-JA.md')
HT = rd(T + 'easy-japanese-summary-JA.html')
ORIG = rd(J)
HTX = re.sub(r'<[^>]+>', '', re.sub(r'(?s)<style.*?</style>|<head.*?</head>', '', HT))
NG = []; CNT = {'形式': 0, '同一': 0, '必在': 0, '禁止': 0, '対応': 0}
def ck(cat, name, ok, d=''):
    CNT[cat] += 1
    print(('  OK  ' if ok else '!NG  ') + '[%s] %s' % (cat, name) + ('  ' + d if d else ''))
    if not ok: NG.append(name)
# ふりがなの（かっこ）は中身ごと落とす——初版は括弧だけ落として中身を残し、鍵句照合が全滅した
nrm = lambda t: re.sub(r'[*>\s`（）\(\)—→・「」【】]', '', re.sub(r'（[^）]{1,8}）|\([0-9]\)', '', t))
NMD, NHT = nrm(MD), nrm(HTX)

print('== 層E1 やさしい日本語の形式 ==')
body = re.sub(r'^#.*$', '', MD, flags=re.M)          # 見出しは対象外
body = re.sub(r'https?://\S+', '', body)
body = re.sub(r'^もとの 文章:.*$', '', body, flags=re.M)   # 書誌行は対象外
sents = [s.strip() for s in re.split(r'(?<=。)', body) if len(s.strip()) > 1]
# ふりがな（かっこ）と装飾を除いた実効の長さで測る
eff = lambda s: len(re.sub(r'（[^）]{1,8}）|[*—>\s]', '', s))
longs = [(eff(s), s[:46]) for s in sents if eff(s) > 60]
ck('形式', '一文が長すぎない（実効60字以下・全%d文）' % len(sents), not longs,
   '超過%d件: %s' % (len(longs), longs[:2]) if longs else '')
ck('形式', '平均文長（実効）', True, '%.1f字' % (sum(eff(s) for s in sents) / len(sents)))
DOUBLE_NEG = ['なくない', 'ないことはない', 'ないわけではありません。']
ck('形式', '二重否定の不在', not any(d in nrm(MD) for d in DOUBLE_NEG))
HARD = ['実測', '確度', '検証系列', '介入', '基底', '帰無', '仮説', '相関', '認証', '不可逆',
        '構造的', '一般化', '蓋然', '当該', '前置き', '有意']
# 原典の題名（『認証されないゼロと訂正の循環』）は固有名詞として除外する
_md_wo_title = MD.replace('認証されないゼロと訂正の循環', '')
hard_hit = [w for w in HARD if w in _md_wo_title]
ck('形式', 'むずかしい語の不在', not hard_hit, str(hard_hit))
ck('形式', 'ふりがな（かっこ）が付いている', MD.count('（') >= 25, '%d箇所' % MD.count('（'))

print('== 層E2 md↔html の同一性（片側だけ古くなるのを防ぐ） ==')
KEY = ['せきにんを とることが できません', 'いっしょに なおすことは できません',
       'それ いじょう せつめい できない', 'おぼえている しるし', 'まもる しるしでは ありません',
       'でも、きくことは 役に 立ちます', 'どこに、何が 書いて ありましたか',
       'ほんとうは 読んで いなかった', 'きいた 中身と、さいしょの 答えが 合っているかも 見ます',
       'かがみは、あなたを うつしているだけです', 'おぼえて いる わけでは ありません',
       'くじを 引く', '2回 同じ 答えでも、正しい しるしでは ありません',
       '同じ AIに すぐ もう一度 きいても、2回には なりません',
       'やり直せない ことは、AIに まかせません', 'AIに 教えません',
       'やめて、人に 話します', 'AIでは なく、人に 話して ください',
       'いつも AIの そとに おいて ください', 'まもろうよ こころ', '119番', '110番',
       'AIと いっしょに 作りました', 'この 紙にも あてはまります',
       'どちらの しょうこにも なりません']
miss_md = [k for k in KEY if nrm(k) not in NMD]
miss_ht = [k for k in KEY if nrm(k) not in NHT]
ck('同一', 'md に鍵句%d件すべて' % len(KEY), not miss_md, str(miss_md)[:110])
ck('同一', 'html に鍵句%d件すべて' % len(KEY), not miss_ht, str(miss_ht)[:110])
ck('同一', '見出し（やくそく1〜5・合言葉・こまったとき）が両方に',
   all(nrm(h) in NMD and nrm(h) in NHT for h in
       ['じょうずな 話しかたは、正しい しるしでは ありません', '中身を ききます',
        'よろこぶ 方に かたむきます', '2回以上ききます', 'じぶんで 決めます',
        'あんぜんの 合言葉', 'こまった ときは']))

print('== 層E3 必在（限定と成果の対・五箇条の全条） ==')
PAIR = [('第2条の限定', 'まもる しるしでは ありません'), ('第2条の成果', 'でも、きくことは 役に 立ちます')]
for n, k in PAIR:
    ck('必在', '%s「%s」' % (n, k[:20]), nrm(k) in NMD and nrm(k) in NHT)
FIVE = ['正しい しるしでは ありません', '中身を ききます', 'はんたいの りゆうも ききます',
        '2回目は、べつの くじで 引きます', 'じぶんの 手で します']
for i, k in enumerate(FIVE, 1):
    ck('必在', '第%d条「%s」' % (i, k[:18]), nrm(k) in NMD and nrm(k) in NHT)

print('== 層E4 降ろさないもの（統計・専門語・§10 の三腕） ==')
FORBID = ['54.0', '52.0', '26.0', '85', '294', '88.4', '27/48', '3/n', 'ε', 'κ', 'Holm', 'p=',
          '存在論', '追補', '有意', 'Fisher', '検出力', '確率']
hit = [w for w in FORBID if w in MD or w in HTX]
ck('禁止', '統計・専門語の不在', not hit, str(hit))
ck('禁止', '数字は「1回」「2回」「5つ」「119」「110」の範囲', True,
   str(sorted(set(re.findall(r'[0-9]+', MD)))))

print('== 層E5 原典 付録D(一)①〜⑤ との対応 ==')
Z = [('①自信の強さ', '自信の強さは、根拠があることのしるしになりません', 'それ いじょう せつめい できない'),
     ('②跡と守る', '跡は、覚えている証拠にはなっても、守る証拠にはなりません', 'まもる しるしでは ありません'),
     ('②効いた手順', '「中身をきく」こと自体は、実際に効いた手順です', 'でも、きくことは 役に 立ちます'),
     ('②突合を一手続きに', '跡と、答えが合っているかまでを一つにして、きいてください', 'きいた 中身と、さいしょの 答えが 合っているかも 見ます'),
     ('③逆をきく', 'AIの答えは、あなたが喜ぶ方に傾く', 'よろこぶ 方に かたむきます'),
     ('④引き直し', '答えは毎回の引き直しです', 'くじを 引く'),
     ('④独立の二回目', '二回目が本当に独立だったかを、あとから確かめられないことがあります', '同じ AIに すぐ もう一度 きいても、2回には なりません'),
     ('⑤自分の指で', '取り返しのつかないボタンは、自分の指で押す', 'じぶんの 手で します'),
     ('危機の一行', '死にたさ、消えたさ、自分を傷つけたい気持ちが動いたときは——AIではなく、人間へ', 'AIでは なく、人に 話して ください'),
     ('相談先ポータル', 'まもろうよ こころ', 'まもろうよ こころ')]
for name, ja, ez in Z:
    ck('対応', name, nrm(ja) in nrm(ORIG) and nrm(ez) in NMD,
       ('' if nrm(ja) in nrm(ORIG) else '原典側不在! ') + ('' if nrm(ez) in NMD else '要約側不在!'))

print()
tot = sum(CNT.values())
print('=== 被覆の申告: 全%d検査 ＝ 形式%d（文長・二重否定・語彙・ふりがな）＋ 同一%d（md↔html）'
      '＋ 必在%d ＋ 禁止%d ＋ 対応%d（原典 付録D↔要約） ===' %
      (tot, CNT['形式'], CNT['同一'], CNT['必在'], CNT['禁止'], CNT['対応']))
print('=== 本検査が見ないもの: やさしい日本語としての実際の読みやすさ（母語話者でない読者による検証は未実施）／')
print('    印刷したときに一枚に収まるか（版面は目で見る必要がある）／漢字の水準（JLPT等の基準に照合していない）。 ===')
print('=== NG %d件 ===' % len(NG))
for x in NG: print('  ', x)
sys.exit(1 if NG else 0)
