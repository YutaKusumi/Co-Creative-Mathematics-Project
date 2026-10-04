# -*- coding: utf-8 -*-
"""元考察 改訂十五＋論文 v0.9.11（改訂回数の整合）＋README・授業資料の README・常設検査の許可リスト。

事前登録: 00-preregistration.md（2026-10-05 05:48・案一）
実行:
  python apply_r15_v0911.py stage   … 置き場の写しを staged/ に作って当てる（置き場は変えない）
  python apply_r15_v0911.py repo    … 置き場に当てる（登録者の裁定と push の許しの後だけ）
各置き換えは「旧文字列がちょうど一件」を確かめてから行う（前例 apply_companion_v14.py の作法）。
README の SHA は、論文を直した後のファイルから計算して書く（書いた値ではなく計算した値）。
"""
import io, os, sys, shutil, hashlib, json
CHANGES = []

REPO = 'C:/Users/PC/Desktop/GitHub-Repositories/Co-Creative-Mathematics-Project/'
U = 'Uncertified-Zeros-and-Correction-Loops/'
HERE = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') + '/'
mode = sys.argv[1] if len(sys.argv) > 1 else ''
assert mode in ('stage', 'repo'), '引数は stage か repo'
ROOT = HERE + 'staged/' if mode == 'stage' else REPO

FILES = {
    'cj': U + 'JA/ai-involvement-boundaries-and-human-precautions-JA.md',
    'ce': U + 'EN/ai-involvement-boundaries-and-human-precautions-EN.md',
    'pj': U + 'JA/uncertified-zeros-and-correction-loops-JA.md',
    'pe': U + 'EN/uncertified-zeros-and-correction-loops-EN.md',
    'rj': U + 'README.md',
    're': U + 'README-EN.md',
    'tr': U + 'teaching-materials/README.md',
    'ck': U + 'verification/v09-reflection-workflow/check_readme_version.py',
}

if mode == 'stage':
    if os.path.exists(ROOT):
        shutil.rmtree(ROOT)
    for p in FILES.values():
        os.makedirs(os.path.dirname(ROOT + p), exist_ok=True)
        shutil.copyfile(REPO + p, ROOT + p)

def sha(p):
    return hashlib.sha256(io.open(ROOT + p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()

def fix(key, pairs):
    p = FILES[key]
    raw = io.open(ROOT + p, 'rb').read()
    assert b'\r\n' not in raw, '改行が CRLF: ' + p
    s = raw.decode('utf-8')
    for old, new, label in pairs:
        n = s.count(old)
        assert n == 1, '%s / %s: 旧文字列 %d 件' % (p.split('/')[-1], label, n)
        s = s.replace(old, new)
        CHANGES.append({'file': p, 'label': label, 'old': old, 'new': new})
    io.open(ROOT + p, 'w', encoding='utf-8', newline='').write(s)
    print('  %-58s %s' % (p.split('/')[-1], sha(p)))

# ---------------------------------------------------------------- 元考察（改訂十五）
LOG_CJ = ('「本改訂」を指す語は改訂のたびに数え直す。'
          '／改訂十五（2026年10月5日）——見出しと日付の行の訂正。契機は、本稿と姉妹論文の動画化を計画する過程で'
          '原典を照合したこと（照合と訂正の作業は Claude Code 上の Claude Opus 5.5・登録者裁定）。'
          '修正: (1) 第5の二節の見出し「六層の防護の中の一〜二層」を「**二〜四層**」へ——同じ節の本文'
          '（「五箇条は二〜四層の個人版であり、一・五・六層には個人の手がほぼ届かない」）と六層の表、および姉妹論文 第6節'
          '（「個人にできるのは主に二〜四層」）が正であり、**見出しだけが食い違っていた**（本文書の公開の最初の版'
          '〔2026年7月23日〕から）。(2) 冒頭の日付の行「2026年7月18日（草稿・改訂一）」を、改訂の番号を持たない形へ——'
          '公開の最初の版の時点で、改訂はすでに十三まで進んでいた。数を書いた箇所は数が動くたびに数え直さねばならないので、'
          '日付の行には初版の日付だけを置き、改訂の番号と日付は本履歴に記す。(3) R項の「十三度（本改訂で十四度）」を'
          '「十四度（本改訂で十五度）」へ（「本改訂」を指す語の数え直し）。あわせて、姉妹論文（v0.9.11）と README の'
          '改訂回数を整合させた。本文の主張の変更はない。')
LOG_CE = ('a phrase that says "with this revision" must be recounted at every revision.'
          ' / Revision Fifteen (October 5, 2026) — correction of a heading and of the date line. The occasion: a check of '
          'the sources carried out while planning a video series on this paper and its sister paper (the check and the '
          'corrections were made by Claude Opus 5.5 in Claude Code; registrant\'s adjudication). Corrections: (1) the heading '
          'of §5-bis, "One or Two Layers within the Six-Layer Structure of Safeguards," changed to "**Layers Two through '
          'Four** within the Six-Layer Structure of Safeguards" — the body of the same section ("the five articles are the '
          'individual-level version of Layers Two through Four; Layers One, Five, and Six are almost beyond an individual\'s '
          'reach"), the six-layer table, and §6 of the sister paper ("what an individual can do is mainly confined to Layers '
          'Two through Four") are the authority; **only the heading disagreed** (since the first public version of this '
          'document, July 23, 2026). (2) the opening date line, "July 18, 2026 (draft, revision one)," changed to a form '
          'that carries no revision number — by the first public version, the revisions had already reached thirteen. Since '
          'any place that states a number must be recounted whenever the number moves, the date line now carries only the '
          'date of the first edition, and revision numbers and dates are recorded in this history. (3) item R\'s "thirteen '
          '(fourteen, with this revision)" changed to "fourteen (fifteen, with this revision)" (recounting a phrase that '
          'says "with this revision"). The revision counts in the sister paper (v0.9.11) and the README were brought into '
          'line at the same time. No claim in the body has changed.')

print('== 元考察 JA（改訂十五）')
fix('cj', [
    ('**日付**: 2026年7月18日（草稿・改訂一）',
     '**日付**: 2026年7月18日（草稿・初版）——改訂の番号と日付は、下の改訂履歴に記す', 'A3 日付の行'),
    ('## 5の二.（補）個人の注意の位置 ―― 六層の防護の中の一〜二層',
     '## 5の二.（補）個人の注意の位置 ―― 六層の防護の中の二〜四層', 'A1 見出し'),
    ('十三度（本改訂で十四度）の改訂履歴と契機の記帳', '十四度（本改訂で十五度）の改訂履歴と契機の記帳', 'R項'),
    ('「本改訂」を指す語は改訂のたびに数え直す。\n**性格**', LOG_CJ + '\n**性格**', '改訂十五'),
])
print('== 元考察 EN（Revision Fifteen）')
fix('ce', [
    ('**Date**: July 18, 2026 (draft, revision one)',
     '**Date**: July 18, 2026 (draft, first edition) — revision numbers and dates are recorded in the revision history below',
     'A3 date line'),
    ('## 5-bis. (Supplementary) Where Individual Precaution Sits — One or Two Layers within the Six-Layer Structure of Safeguards',
     '## 5-bis. (Supplementary) Where Individual Precaution Sits — Layers Two through Four within the Six-Layer Structure of Safeguards',
     'A1 heading'),
    ('the record of thirteen (fourteen, with this revision) rounds of revision',
     'the record of fourteen (fifteen, with this revision) rounds of revision', 'item R'),
    ('a phrase that says "with this revision" must be recounted at every revision.\n**Character**',
     LOG_CE + '\n**Character**', 'Revision Fifteen'),
])

# ---------------------------------------------------------------- 論文（v0.9.11）
LOG_PJ = (' v0.9.11 元考察の改訂十五（第5の二節の見出し「一〜二層」を、同じ節の本文と本稿 第6節〔個人にできるのは主に二〜四層〕'
          'に合わせて「二〜四層」へ・冒頭の日付の行の訂正）に伴い、改訂回数の記述を整合させた——第9節「十四次」→「十五次」、'
          '付録F「十四次」→「十五次」（v0.9.9 と同型。本文の主張には触れない改訂であり、追補の反映ではない——第9節末尾の'
          '未反映の申告〔2026年8月31日〕は据え置く）。あわせて英語版の「訳についての注記」を同期の実態（v0.9.4 以後の各版も'
          '英語版に適用・同期の検査は v0.9.10 で93検査）に合わせた。作業は Claude Code 上の Claude Opus 5.5（登録者裁定・'
          '2026年10月5日）。')
LOG_PE = (' v0.9.11 Following Revision Fifteen of the Companion Consideration (the heading of §5-bis, "One or Two Layers," '
          'brought into line with the body of that section and with §6 of this paper [what an individual can do is mainly '
          'confined to Layers Two through Four] as "Layers Two through Four"; correction of the opening date line), the '
          'statements of the revision count were brought into line — §9 "fourteen" → "fifteen," Appendix F "fourteen" → '
          '"fifteen" (the same type as v0.9.9; a revision that does not touch the claims of the body and is not a reflection '
          'of the addenda — the declaration of unreflected material at the end of §9 [August 31, 2026] stands). The note on '
          'this translation was brought into line with the actual synchronization at the same time (each version after '
          'v0.9.4 has also been applied to the English; the synchronization check counted 93 checks at v0.9.10). The work '
          'was done by Claude Opus 5.5 in Claude Code (registrant\'s adjudication, October 5, 2026).')

print('== 論文 JA（v0.9.11）')
fix('pj', [
    ('**版**: 第一草稿・完成版 v0.9.10（2026年8月11日）', '**版**: 第一草稿・完成版 v0.9.11（2026年10月5日）', '版の行'),
    ('元考察の十四次の改訂はすべて契機つきで公開の履歴に記帳され', '元考察の十五次の改訂はすべて契機つきで公開の履歴に記帳され', '§9'),
    ('本稿の元文書（『検証事例を踏まえた考察』）は、十四次にわたる改訂のすべてを',
     '本稿の元文書（『検証事例を踏まえた考察』）は、十五次にわたる改訂のすべてを', '付録F'),
    ('期待リストの承認元併記と未使用警告（阿弥陀・不空成就）→ precheck_v093。\n**執筆体制の注記**',
     '期待リストの承認元併記と未使用警告（阿弥陀・不空成就）→ precheck_v093。' + LOG_PJ + '\n**執筆体制の注記**', '改訂記録'),
])
print('== 論文 EN（v0.9.11）')
fix('pe', [
    ('**Version**: First Draft, Completed Version v0.9.10 (August 11, 2026)',
     '**Version**: First Draft, Completed Version v0.9.11 (October 5, 2026)', 'version line'),
    ('All fourteen rounds of revision of the Companion Consideration were logged',
     'All fifteen rounds of revision of the Companion Consideration were logged', '§9'),
    ('records, in a public revision history, all fourteen rounds of revision',
     'records, in a public revision history, all fifteen rounds of revision', 'Appendix F'),
    ('all four layers published (README, both languages).\n**Note on the drafting process**',
     'all four layers published (README, both languages).' + LOG_PE + '\n**Note on the drafting process**', 'revision log'),
    ('and synchronized to v0.9.4 on August 11, 2026. The synchronization was checked mechanically — clause-level '
     'correspondence against the Japanese for every changed block, cross-language agreement of all principal figures, and '
     'byte-level invariance of the sections that did not change (90 checks, no failures) —',
     'and synchronized to v0.9.4 on August 11, 2026; each later version (currently v0.9.11, October 5, 2026) has also been '
     'applied to this English text. The synchronization was checked mechanically — clause-level correspondence against the '
     'Japanese for every changed block, cross-language agreement of all principal figures, and byte-level invariance of the '
     'sections that did not change (90 checks at the synchronization to v0.9.4 and 93 at v0.9.10, no failures; the v0.9.11 '
     'alignment of revision counts was checked by string anchors and a cross-file search) —', 'B4 translation note'),
])

PJ_SHA, PE_SHA = sha(FILES['pj']), sha(FILES['pe'])
print('   論文の新しい SHA: JA %s / EN %s' % (PJ_SHA, PE_SHA))

# ---------------------------------------------------------------- README（日本語）
print('== README JA')
fix('rj', [
    ('**学術論文本体**（**v0.9.10 確定版**・2026-08-11・SHA-256(LF)先頭16 `553FBC3DEDBCEA7A`・枠組み提示型構造的論証',
     '**学術論文本体**（**v0.9.11**・2026-10-05・SHA-256(LF)先頭16 `%s`——v0.9.10 確定版〔2026-08-11〕に、第9節末尾の'
     '未反映の申告〔2026-08-31・改訂ではない〕と、元考察の改訂十五に伴う改訂回数の整合〔v0.9.11〕を加えた版で、'
     '主張の変更はない・枠組み提示型構造的論証' % PJ_SHA, 'B7 論文の版と SHA'),
    ('本論文の元文書・十三次の改訂履歴つき）', '本論文の元文書・十五次の改訂履歴つき）', 'A2 改訂の数'),
    ('本論文 v0.9.10 は、次の検証を経ている——',
     '本論文 v0.9.10 は、次の検証を経ている（その後の変更は、第9節の申告と v0.9.11 の改訂回数の整合だけ）——', 'v0.9.11 の性格'),
    ('いずれも原典 v0.9.10 と同期しています（',
     'いずれも原典 v0.9.10 と同期しています（v0.9.11 は改訂回数の整合のみで、頒布物に関わる変更はありません。', 'v0.9.11 の性格（頒布物）'),
    ('| 学術 | **論文本体**（v0.9.10・日英） |', '| 学術 | **論文本体**（v0.9.11・日英） |', '頒布物の表 論文'),
    ('**元考察**（確度記号つき・改訂十四・日英）', '**元考察**（確度記号つき・改訂十五・日英）', '頒布物の表 元考察'),
    ('**英語版論文も v0.9.10 に同期済み**（SHA `0D1F6C927801E343`・機械照合93検査・',
     '**英語版論文も v0.9.11 に同期済み**（SHA `%s`。v0.9.10 への同期の機械照合は93検査・' % PE_SHA, 'B8 英語版の版と SHA'),
])

# ---------------------------------------------------------------- README（英語）
B2_OLD = ('This paper has undergone adversarial audits by the Claude series (first through final, four rounds in total) and '
          'primary-source cross-checking of its core literature. **However, the out-of-lineage (non-Claude) review that its '
          'sibling, Addendum II, received has not yet been carried out for this paper.** This paper is published on that basis, '
          'with §8 stating explicitly: "Independent, non-Claude, human cross-checking could not be carried out in this version. '
          'It is the foremost item on the standing correction shelf after publication." In particular, the new primary sources '
          'not present in Addendum II (judicial records, suicide-related statistics, literature on human-AI relationships) were '
          'cross-checked by the drafting AI (of the Claude series), but have not passed before non-Claude eyes. Verification, '
          'counterexamples, and corrections from readers and experts, regardless of direction, will be logged in the public record.')
B2_NEW = ('v0.9.10 of this paper has undergone the following verification (the only changes since are the declaration in §9 and '
          'the v0.9.11 alignment of revision counts): (1) adversarial audits by the Claude series (first through final, four '
          'instances in total, up to v0.8); (2) **six rounds in total** of adversarial review by four Claude-family instances '
          '(Opus 5) in the v0.9 reflection workflow (three rounds on the correspondence map plus three rounds of '
          'difference-limited review, with verbatim preservation and machine checks before submission); and (3) **three rounds '
          'of out-of-lineage review (non-Claude, Gemini 3.6 Flash)** — the first round independently recomputed the statistics '
          'and checked five external references, and caught one item that none of the four intra-family reviewers had caught '
          '(the catastrophe-conditional denominator); in the second round the out-of-lineage reviewer itself withdrew one of its '
          'first-round points; and the third (final) round approved every item.\n\n'
          '**Still outstanding** (stated in §8 of the paper; the foremost items on the standing post-publication correction '
          'shelf): independent cross-checking by human reviewers, independent cross-checking against the primary records, and '
          'review by a statistics specialist **have still not been carried out**. The out-of-lineage review, too, was carried '
          'out at the level of this paper and the addendum reports, without reaching the primary records. The workflow\'s COI '
          'ledger records, on both sides, the drafter\'s lapses six through ten and the reviewers\' errors 1 through 12 — **what '
          'this workflow could show is a record that errors were actually detected, not a certification of zero errors**. '
          'Verification, counterexamples, and corrections from readers and experts, regardless of direction, will be logged in '
          'the public record.')
B3_ROWS = ('\n| [teaching-materials/](teaching-materials/) | **Classroom set** (for upper elementary; handout / board-writing '
           'script / slide-by-slide script / 18 slides) — Appendix G(1). Synchronized with v0.9.10 of the paper (the '
           'correspondence map and the record of 68 checks are in the process records). **Not yet tested in an actual lesson** '
           '· Japanese only |'
           '\n| [verification/v09-reflection-workflow/](verification/v09-reflection-workflow/) | **Full record of the '
           'v0.8→v0.9.10 reflection workflow** (correspondence maps v1–v4 · verbatim reviews, six rounds plus three '
           'out-of-lineage rounds · COI ledger [both sides] · machine-check instruments · version lineage and diffs · '
           'primary-record collation · drafter\'s re-review record) |')
print('== README EN')
fix('re', [
    ('> **Version note (2026-08-11):** Both the Japanese original and this English translation are now at **v0.9.10**, '
     'reflecting verification-series addenda E & W and the temperature-0 control, confirmed through six rounds of '
     'intra-family adversarial review plus three rounds of external (non-Claude-family) review.',
     '> **Version note (2026-08-11; updated 2026-10-05):** Both the Japanese original and this English translation are now at '
     '**v0.9.11**. Its claims are those of v0.9.10 (August 11, 2026), reflecting verification-series addenda E & W and the '
     'temperature-0 control, confirmed through six rounds of intra-family adversarial review plus three rounds of external '
     '(non-Claude-family) review; since then, a declaration of unreflected material was added at the end of §9 (August 31, '
     '2026; not a revision), and v0.9.11 (October 5, 2026) aligned the revision counts following Revision Fifteen of the '
     'Companion Consideration.', 'B5 版の注 その一'),
    ('the synchronization was checked mechanically (90 checks, including a JA↔EN clause-correspondence layer)',
     'the synchronization was checked mechanically (90 checks at the synchronization to v0.9.4 and 93 at v0.9.10, including '
     'a JA↔EN clause-correspondence layer)', 'B5 版の注 その二'),
    ('**The academic paper itself** (v0.8 · a framework-presenting structural argument',
     '**The academic paper itself** (v0.9.11 · SHA-256 (LF), first 16: `%s` · a framework-presenting structural argument' % PE_SHA,
     'B1 論文の版'),
    ('(for a general readership · the document from which this paper originated · with a thirteen-round revision history) |',
     '(for a general readership · the document from which this paper originated · with a fifteen-round revision history) |',
     'A2 改訂の数'),
    ('(**a format that visualizes unverified items as blank cells** — an implementation of this paper\'s own method) |',
     '(**a format that visualizes unverified items as blank cells** — an implementation of this paper\'s own method) |' + B3_ROWS,
     'B3 表の行'),
    (B2_OLD, B2_NEW, 'B2 検証水準の開示'),
    ('| Academic | **The paper** (v0.9.10, JA/EN) |', '| Academic | **The paper** (v0.9.11, JA/EN) |', '頒布物の表 論文'),
    ('(with confidence markers; Revision 14; JA/EN)', '(with confidence markers; Revision 15; JA/EN)', '頒布物の表 元考察'),
])

# ---------------------------------------------------------------- 授業資料の README
print('== 授業資料の README')
fix('tr', [
    ('教育・支援目的の複製・翻案を自由とするライセンスを付す予定（原典 付録G）。',
     '**ライセンス: [CC BY 4.0](../../LICENSE)**（リポジトリ全体）——出典を明示すれば、商用を含め、自由に共有・翻案できます。'
     '教育・支援目的の複製・翻案は、すでに自由です（原典 付録G は当初「付す予定」と書いていましたが、原典 v0.9.10 で'
     '記述を実態に合わせました——本 README のこの一文は、そのとき直し漏れていました）。', 'B6 ライセンス'),
])

# ---------------------------------------------------------------- 常設検査の許可リスト
print('== 常設検査の許可リスト')
fix('ck', [
    (" ('README-EN.md', 'corrected in v0.9.4', '英語版同期で見つかった残存不整合を**実際に訂正した版**を指す歴史的記述'),\n]",
     " ('README-EN.md', 'corrected in v0.9.4', '英語版同期で見つかった残存不整合を**実際に訂正した版**を指す歴史的記述'),\n"
     " # 以下 v0.9.11（2026-10-05・改訂回数の整合のみ）で足した——いずれも v0.9.10 の時点の事実を指す\n"
     " ('README.md', 'v0.9.10 確定版〔2026-08-11〕', 'v0.9.11 の土台になった確定版'),\n"
     " ('README.md', '原典 v0.9.10 と同期済み', '授業資料一式が同期を検査された版'),\n"
     " ('README.md', 'v0.8→v0.9.10 反映工程', '反映工程の範囲'),\n"
     " ('README.md', '本論文 v0.9.10 は、次の検証を経ている', '検証を受けた版（その後の変更は申告と回数の整合だけ）'),\n"
     " ('README.md', 'v0.9.10 で付録G の記述を実態に合わせました', '付録G を直した版'),\n"
     " ('README.md', 'いずれも原典 v0.9.10 と同期しています', '頒布物が同期を検査された版'),\n"
     " ('README.md', 'v0.9.10 への同期の機械照合', '93検査を行った同期の版'),\n"
     " ('README-EN.md', 'Its claims are those of v0.9.10', 'v0.9.11 の土台になった確定版'),\n"
     " ('README-EN.md', '93 at v0.9.10', '93検査を行った同期の版'),\n"
     " ('README-EN.md', 'at the synchronization to v0.9.4', '90検査を行った同期の版'),\n"
     " ('README-EN.md', 'v0.9.10 of this paper has undergone', '検証を受けた版'),\n"
     " ('README-EN.md', 'Synchronized with v0.9.10 of the paper', '授業資料一式が同期を検査された版'),\n"
     " ('README-EN.md', 'v0.8→v0.9.10 reflection workflow', '反映工程の範囲'),\n"
     " ('README-EN.md', 'brought into line with the actual state in v0.9.10', '付録G を直した版'),\n"
     " ('README-EN.md', 'each synchronized with v0.9.10 of the paper', '頒布物が同期を検査された版'),\n]",
     '許可リスト'),
])
if mode == 'stage':
    io.open(HERE + 'changes.json', 'w', encoding='utf-8', newline='\n').write(json.dumps(CHANGES, ensure_ascii=False, indent=1))
print('== 終わり（%s）' % mode)
