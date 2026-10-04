# -*- coding: utf-8 -*-
"""K2: 直した旧文字列の全ファイル横断の検索（追跡されているファイル全部・直したファイルは写しの方を読む）。

合格: 旧文字列が残るのは EXPECTED に挙げた所だけ（理由つき）。挙げていない所に残れば NG。
"""
import io, os, subprocess, sys

REPO = 'C:/Users/PC/Desktop/GitHub-Repositories/Co-Creative-Mathematics-Project/'
HERE = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') + '/'
STAGED = HERE + 'staged/'
U = 'Uncertified-Zeros-and-Correction-Loops/'
W = U + 'verification/v09-reflection-workflow/'

files = subprocess.run(['git', '-C', REPO, 'ls-files', '-z'], capture_output=True).stdout.decode('utf-8').split('\0')
files = [f for f in files if f]

def read(f):
    p = STAGED + f if os.path.exists(STAGED + f) else REPO + f
    try:
        return io.open(p, encoding='utf-8').read()
    except (UnicodeDecodeError, IsADirectoryError, FileNotFoundError):
        return None

CJ, CE = U + 'JA/ai-involvement-boundaries-and-human-precautions-JA.md', U + 'EN/ai-involvement-boundaries-and-human-precautions-EN.md'
PJ, PE = U + 'JA/uncertified-zeros-and-correction-loops-JA.md', U + 'EN/uncertified-zeros-and-correction-loops-EN.md'
TR = U + 'teaching-materials/README.md'
HIST = '過去の記録（工程記録・器材・差分）——その時点の文字列を保存している'
# run1（05:5x）で想定外 8 件——すべて過去の記録だった（表の漏れ）。表を直して run2 とした
SIX6 = '06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned/Version-B-Policy-Edition/verification/'

# (旧文字列, {ファイル: 理由}) ——ファイル名の末尾が '/' のものは、その下の全部
OLD = [
 ('一〜二層', {CJ: '改訂十五の記録が旧見出しを引く', PJ: 'v0.9.11 の記録が旧見出しを引く'}),
 ('One or Two Layers', {CE: 'Revision Fifteen の記録が旧見出しを引く', PE: 'v0.9.11 の記録が旧見出しを引く'}),
 ('（草稿・改訂一）', {CJ: '改訂十五の記録が旧日付の行を引く'}),
 ('(draft, revision one)', {CE: 'Revision Fifteen の記録が旧日付の行を引く'}),
 ('十三度（本改訂で十四度）', {CJ: '改訂十五の記録が旧 R項を引く', W: HIST}),
 ('thirteen (fourteen, with this revision)', {CE: 'Revision Fifteen の記録が旧 R項を引く', W: HIST}),
 ('十三次', {PJ: 'v0.9.9 の記録（「十三次」→「十四次」）', W: HIST}),
 ('thirteen-round', {}),
 ('十四次', {PJ: 'v0.9.9 と v0.9.11 の記録', W: HIST,
            '06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned/Version-B-Policy-Edition/verification/': HIST}),
 ('fourteen rounds', {PE: 'v0.9.9 と v0.9.11 の記録', W: HIST}),
 ('改訂十四', {CJ: '改訂十四の記録そのもの', PJ: 'v0.9.9 の記録', W: HIST}),
 ('Revision 14', {W: HIST}),
 ('Revision Fourteen', {CE: '改訂十四の記録そのもの', PE: 'v0.9.9 の記録', W: HIST}),
 ('(v0.8 ·', {}),
 ('has not yet been carried out for this paper', {}),
 ('(90 checks, no failures)', {W: HIST}),
 ('付す予定', {PJ: 'v0.9.10 の記録（「付す予定」と書いていた）', U + 'README.md': '当初「付す予定」としていたことの説明',
             TR: '当初「付す予定」と書いていたことの説明（今回の直し）', W: HIST, SIX6: HIST}),
 ('553FBC3DEDBCEA7A', {W: HIST, SIX6: HIST}),
 ('0D1F6C927801E343', {W: HIST}),
 ('06398EF63FFD3A76', {}),
 ('74AE1C0253E3B451', {}),
]

def expected(f, table):
    for k, why in table.items():
        if (k.endswith('/') and f.startswith(k)) or f == k:
            return why
    return None

NG = 0
for old, table in OLD:
    hits = []
    for f in files:
        s = read(f)
        if s is None or old not in s:
            continue
        hits.append((f, s.count(old), expected(f, table)))
    bad = [h for h in hits if h[2] is None]
    NG += len(bad)
    print('%s「%s」 %d ファイル' % ('!NG ' if bad else '  OK', old, len(hits)))
    for f, n, why in hits:
        print('      %s %s ×%d  %s' % ('予定' if why else '想定外', f, n, why or ''))
print('=== 想定外の残り %d 件 ===' % NG)
sys.exit(1 if NG else 0)
