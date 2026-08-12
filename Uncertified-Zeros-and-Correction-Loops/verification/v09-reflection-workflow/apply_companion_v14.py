# -*- coding: utf-8 -*-
"""元考察 改訂十四（登録者裁定 (A)+(B)+(C)・2026-08-11）＋それが波及する改訂回数の整合。

(A) 「二回きく」→「二回以上きく」（原典 v0.9.8 と同じ理由: ε<3/n は n が増えるほど上界が下がる）
(B) 条番号の取り違えの訂正——元考察の五箇条は 第一条=たしかめる／第二条=追い問い／第三条=逆もきく／
    第四条=二回以上きく／第五条=不可逆 であり、本文の三箇所がこれと食い違っていた。
    （同文書 L200 の第三層の行が「追い問い・…｜第5節第二条」と正しく対応させており、これが照合の正。）
(C) EN も同じ5箇所。

波及（本改訂が古くする数・および本改訂で発見した既存の食い違い）:
  ・元考察 R項「九度（本改訂で十度）」——実際の改訂履歴は十三項（本改訂で十四）。**本改訂**を指す語が
    追随していなかった（原典 COI 台帳十一件目と同型）。
  ・原典 付録F「十一次」——実際は十三（本改訂で十四）。**本改訂とは独立の既存の食い違い**。
  ・原典 §9「十三次」——本改訂で十四になる。
実行: proposals で python apply_companion_v14.py
"""
import io, hashlib
R = 'C:/Users/PC/Desktop/GitHub-Repositories/Co-Creative-Mathematics-Project/Uncertified-Zeros-and-Correction-Loops/'
sha = lambda p: hashlib.sha256(io.open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()
def fix(p, pairs):
    s = io.open(R + p, encoding='utf-8').read()
    for old, new, l in pairs:
        n = s.count(old)
        # 適用済みの判定: 新文字列がすでにあるなら飛ばす。**新が旧を含む場合 n>=1 でも適用済みでありうる**
        # （初版はここを n==0 のみで判定し、再実行で改訂記録を二重に書いた）
        if new in s: continue                                # 適用済み（再実行可）
        assert n == 1, 'アンカー %s / %s: %d件' % (p.split('/')[-1], l, n)
        s = s.replace(old, new)
    io.open(R + p, 'w', encoding='utf-8', newline='').write(s)
    print('  %-52s %s' % (p.split('/')[-1], sha(R + p)))

LOG_JA = ('以後、修正した旧文字列の全ファイル横断grepによる残存ゼロ確認を修正手順の標準とする。'
          '／改訂十四（2026年8月11日）——姉妹論文 v0.9.8 との同期と、条番号の取り違えの訂正。'
          '契機は、付録G(3)「やさしい日本語版要約」の起草中に登録者が「二回きく」の標語を検出したこと。'
          '修正: (1) 第四条の標語を「二回きく」から**「二回以上きく」**へ（第四条の根拠は ε<3/n であり、'
          'n が増えるほど上界は下がる。「二回きく」は「二回で足りる」という偽の十分性を含みうる。'
          '論文側 §7.1・付録D(一)④ と同時に改めた）。(2) **条番号の取り違えを三箇所訂正**——本文書の'
          '五箇条は 第一条=たしかめる／第二条=追い問い／第三条=逆もきく／第四条=二回以上きく であるのに、'
          '4-3(教育の層)・6の一(六層表)・7(恋愛)の三箇所が「たしかめる・二回きく・逆もきく」を'
          '「第一〜三条」と対応させ、**第二条（追い問い）を落として第四条を第二条または第三条の位置に'
          '置いていた**（同表の第三層の行は「追い問い｜第5節第二条」と正しく対応させており、これが照合の正）。'
          'この圧縮が、派生教材から第二条が落ちていた出所でもある。(3) R項の「九度（本改訂で十度）」が'
          '実際の改訂数に追随していなかったのを訂正——「本改訂」を指す語は改訂のたびに数え直す。')
LOG_EN = ('Henceforth, confirming zero remaining instances of a corrected old string via a cross-file grep is '
          'adopted as the standard correction procedure. / Revision Fourteen (August 11, 2026) — synchronization '
          'with v0.9.8 of the sister paper, and correction of misattributed article numbers. The occasion: while '
          'the Easy Japanese summary of Appendix G(3) was being drafted, the registrant caught the maxim "ask twice." '
          'Corrections: (1) the maxim of Article Four changed from "ask twice" to **"ask at least twice"** (the ground '
          'of Article Four is ε<3/n, and the bound falls as n grows; "ask twice" can carry a false sufficiency — '
          'changed at the same time as §7.1 and Appendix D(1)④ of the paper). (2) **Three misattributed article '
          'numbers corrected** — this document\'s five articles are Article One = verify / Article Two = follow up with '
          'further questions / Article Three = ask the opposite too / Article Four = ask at least twice, yet three '
          'passages (§4-3 the layer of education, §6-bis(1) the six-layer table, §7 romance) paired "verify, ask twice, '
          'ask the opposite too" with "Articles One through Three," **dropping Article Two (follow-up questioning) and '
          'putting Article Four in the position of Article Two or Three** (the Layer Three row of the same table pairs '
          '"follow-up questioning" with "§5 Article Two" correctly, and that row is the authority for the check). '
          'This compression is also the origin of Article Two\'s absence from the derivative teaching materials. '
          '(3) The count in item R, "nine (ten, with this revision)," had not kept pace with the actual number of '
          'revisions; a phrase that says "with this revision" must be recounted at every revision.')

print('== 元考察 JA（5箇所＋R項＋改訂十四） ==')
fix('JA/ai-involvement-boundaries-and-human-precautions-JA.md', [
 ('これは第5節第二条（二回きく）の組織版であり',
  'これは第5節第二条（申告ではなく検証可能な作業の痕跡を求め、追い問いをする）の組織版であり', '(B)1 L159'),
 ('検証の作法（たしかめる・二回きく・逆もきく）を各世代・各職域の言葉に翻訳して教える仕事',
  '検証の作法（たしかめる・追い問い・逆もきく・二回以上きく）を各世代・各職域の言葉に翻訳して教える仕事', '(A)(B)2 L163'),
 ('第5節第一〜三条（たしかめる・二回きく・逆もきく） | 第5節 |',
  '第5節第一〜四条（たしかめる・追い問い・逆もきく・二回以上きく） | 第5節 |', '(A)(B)3 L199'),
 ('本稿の技（たしかめる・二回きく・逆もきく）は、使う人に検証の動機があることを前提とする',
  '本稿の技（たしかめる・追い問い・逆もきく・二回以上きく）は、使う人に検証の動機があることを前提とする', '(A)(B)4 L231'),
 ('第5節第一〜三条は、恋愛においても、関係を壊さずに実行できる形がある——たとえば、生活上の事実確認だけは外部で行う、大きな決断の前だけは人間にも話す',
  '第5節第一条と第四条は、恋愛においても、関係を壊さずに実行できる形がある——たとえば、生活上の事実確認だけは外部で行う、大きな決断の前だけは人間にも話す（挙げた二例はこの二条に対応する。第三条〔逆もきく〕を恋人に適用しにくいことは、本節（二）に述べたとおりである）', '(B)5 L237'),
 ('九度（本改訂で十度）の改訂履歴と契機の記帳', '十三度（本改訂で十四度）の改訂履歴と契機の記帳', '(波及)R項'),
 ('以後、修正した旧文字列の全ファイル横断grepによる残存ゼロ確認を修正手順の標準とする。', LOG_JA, '改訂十四'),
])

print('== 元考察 EN（5箇所＋R項＋改訂十四） ==')
fix('EN/ai-involvement-boundaries-and-human-precautions-EN.md', [
 ("This is the organizational version of §5's Second Article (Ask Twice)",
  "This is the organizational version of §5's Second Article (demand verifiable traces of work rather than a self-report, and follow up with further questions)", '(B)1'),
 ('the practice of verification (Verify, Ask Twice, Ask the Reverse Too) translated into the language of each generation',
  'the practice of verification (Verify, Follow Up with Further Questions, Ask the Reverse Too, Ask at Least Twice) translated into the language of each generation', '(A)(B)2'),
 ('§5 Articles One through Three (verify, ask twice, ask the opposite too) | §5 |',
  '§5 Articles One through Four (verify, follow up with further questions, ask the opposite too, ask at least twice) | §5 |', '(A)(B)3'),
 ("This paper's techniques (verify, ask twice, ask the opposite too) presuppose",
  "This paper's techniques (verify, follow up with further questions, ask the opposite too, ask at least twice) presuppose", '(A)(B)4'),
 ('§5 Articles One through Three have forms that can be carried out, even within a romance, without breaking the',
  '§5 Articles One and Four have forms that can be carried out, even within a romance, without breaking the', '(B)5'),
 ('the record of nine (ten, with this revision) rounds of revision',
  'the record of thirteen (fourteen, with this revision) rounds of revision', '(波及)R項'),
 ('Henceforth, confirming zero remaining instances of a corrected old string via a cross-file grep is adopted as the standard correction procedure.',
  LOG_EN, '改訂十四'),
])

print('== 原典（改訂回数の整合） ==')
fix('JA/uncertified-zeros-and-correction-loops-JA.md', [
 ('**版**: 第一草稿・完成版 v0.9.8（2026年8月11日）', '**版**: 第一草稿・完成版 v0.9.9（2026年8月11日）', '版'),
 ('元考察の十三次の改訂はすべて契機つきで公開の履歴に記帳され', '元考察の十四次の改訂はすべて契機つきで公開の履歴に記帳され', '§9'),
 ('本稿の元文書（『検証事例を踏まえた考察』）は、十一次にわたる改訂のすべてを',
  '本稿の元文書（『検証事例を踏まえた考察』）は、十四次にわたる改訂のすべてを', '付録F'),
 ('（登録者裁定・2026年8月11日）。',
  '''（登録者裁定・2026年8月11日）。 v0.9.9 元考察の改訂十四（同じ標語の変更と、元考察内の条番号の取り違えの訂正）に伴い、改訂回数の記述を整合させた——第9節「十三次」→「十四次」、付録F「十一次」→「十四次」。**付録F の「十一次」は本改訂以前からの食い違いであり**（元考察は改訂十三まで進んでいた）、今回の掃引で検出した（COI 台帳十一件目「変えなかった文が、他が変わったことで偽になる」の再発——数を書いた箇所は、数が動くたびに数え直す）。''', '改訂記録'),
])
fix('EN/uncertified-zeros-and-correction-loops-EN.md', [
 ('**Version**: First Draft, Completed Version v0.9.8 (August 11, 2026)',
  '**Version**: First Draft, Completed Version v0.9.9 (August 11, 2026)', '版'),
 ('All thirteen rounds of revision of the Companion Consideration were logged',
  'All fourteen rounds of revision of the Companion Consideration were logged', '§9'),
 ('records, in a public revision history, all eleven rounds of revision',
  'records, in a public revision history, all fourteen rounds of revision', '付録F'),
 ("(registrant's adjudication, August 11, 2026).",
  '''(registrant's adjudication, August 11, 2026). v0.9.9 Following Revision Fourteen of the Companion Consideration (the same change of maxim, plus correction of misattributed article numbers inside that document), the statements of the revision count were brought into line — §9 "thirteen" → "fourteen," Appendix F "eleven" → "fourteen." **Appendix F's "eleven" was already out of step before this revision** (the Companion Consideration had reached Revision Thirteen); it was caught in the present sweep (a recurrence of the eleventh entry in the COI ledger, "a sentence that was never changed becomes false because something else changed" — wherever a number is written, it must be recounted whenever that number moves).''', '改訂記録'),
])
