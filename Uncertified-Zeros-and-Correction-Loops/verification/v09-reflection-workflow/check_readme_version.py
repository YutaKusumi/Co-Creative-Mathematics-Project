# -*- coding: utf-8 -*-
"""README（日英）が引く版番号と SHA を、実ファイルから計算した値と突き合わせる常設検査。

作った理由: v0.9.10 の公開で、**同じコミットの中で版を上げたために、私自身が数分前に書いた
README の「v0.9.9」「SHA …」がその場で古くなった**（COI 台帳十一件目の型）。
版と SHA は「書いた値」ではなく「計算した値」と突き合わせるべきである——本器はそれを機械化する。

**自動修正は置かない。** 初版は --fix で版番号を一律置換したところ、README-EN の
「which is corrected in **v0.9.4**」（歴史的事実）まで v0.9.10 に書き換え、**偽の記述を作った**。
現在の版を指す記述と、過去を指す記述は、機械には区別がつかない——九件目「確かめずに、
確かめられたものを訂正する手つき」と同型である。よって本器は**報告のみ**を行い、
過去を指す記述は下の許可リストに理由つきで載せる（層H の期待リストと同じ作法）。
実行: proposals で python check_readme_version.py
"""
import io, re, sys, hashlib
R = 'C:/Users/PC/Desktop/GitHub-Repositories/Co-Creative-Mathematics-Project/Uncertified-Zeros-and-Correction-Loops/'
rd = lambda p: io.open(R + p, encoding='utf-8').read()
sha = lambda p: hashlib.sha256(io.open(R + p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()

JAP, ENP = 'JA/uncertified-zeros-and-correction-loops-JA.md', 'EN/uncertified-zeros-and-correction-loops-EN.md'
ver = re.search(r'完成版 (v0\.9\.\d+)', rd(JAP)).group(1)
ver_en = re.search(r'Completed Version (v0\.9\.\d+)', rd(ENP)).group(1)
ja_sha, en_sha = sha(JAP), sha(ENP)

# 過去を指す記述の許可リスト（理由つき）——ここに無い旧版参照は NG になる
HISTORICAL = [
 ('README-EN.md', 'corrected in v0.9.4', '英語版同期で見つかった残存不整合を**実際に訂正した版**を指す歴史的記述'),
 # 以下 v0.9.11（2026-10-05・改訂回数の整合のみ）で足した——いずれも v0.9.10 の時点の事実を指す
 ('README.md', 'v0.9.10 確定版〔2026-08-11〕', 'v0.9.11 の土台になった確定版'),
 ('README.md', '原典 v0.9.10 と同期済み', '授業資料一式が同期を検査された版'),
 ('README.md', 'v0.8→v0.9.10 反映工程', '反映工程の範囲'),
 ('README.md', '本論文 v0.9.10 は、次の検証を経ている', '検証を受けた版（その後の変更は申告と回数の整合だけ）'),
 ('README.md', 'v0.9.10 で付録G の記述を実態に合わせました', '付録G を直した版'),
 ('README.md', 'いずれも原典 v0.9.10 と同期しています', '頒布物が同期を検査された版'),
 ('README.md', 'v0.9.10 への同期の機械照合', '93検査を行った同期の版'),
 ('README-EN.md', 'Its claims are those of v0.9.10', 'v0.9.11 の土台になった確定版'),
 ('README-EN.md', '93 at v0.9.10', '93検査を行った同期の版'),
 ('README-EN.md', 'at the synchronization to v0.9.4', '90検査を行った同期の版'),
 ('README-EN.md', 'v0.9.10 of this paper has undergone', '検証を受けた版'),
 ('README-EN.md', 'Synchronized with v0.9.10 of the paper', '授業資料一式が同期を検査された版'),
 ('README-EN.md', 'v0.8→v0.9.10 reflection workflow', '反映工程の範囲'),
 ('README-EN.md', 'brought into line with the actual state in v0.9.10', '付録G を直した版'),
 ('README-EN.md', 'each synchronized with v0.9.10 of the paper', '頒布物が同期を検査された版'),
]
NG = []
def ck(name, ok, d=''):
    print(('  OK  ' if ok else '!NG  ') + name + ('  ' + d if d else ''))
    if not ok: NG.append(name)

print('実ファイルの値: JA %s / %s   EN %s / %s' % (ver, ja_sha, ver_en, en_sha))
ck('JA/EN の版番号が一致', ver == ver_en, '%s vs %s' % (ver, ver_en))

for f in ['README.md', 'README-EN.md']:
    s = rd(f)
    allowed = [h for h in HISTORICAL if h[0] == f]
    masked = s
    for _, frag, _r in allowed: masked = masked.replace(frag, '')
    vs = sorted(set(re.findall(r'v0\.9\.\d+', masked)))
    stale = [v for v in vs if v != ver]
    ck('%s が引く版番号は現行のみ（許可リストを除く）' % f, not stale,
       '古い値: %s' % stale if stale else '（許可: %s）' % [h[1] for h in allowed] if allowed else '')
    shas = sorted(set(re.findall(r'`([0-9A-F]{16})`', s)))
    bad = [x for x in shas if x not in (ja_sha, en_sha)]
    ck('%s が引く SHA は現行のみ' % f, not bad, '古い値: ' + str(bad) if bad else '')

print()
print('=== 本検査は報告のみを行う。版番号や SHA が古いときは、**一箇所ずつ人手で**直すこと——')
print('    現在を指す記述と過去を指す記述の区別は、機械にはつかない（初版の自動修正は歴史的記述を壊した）。 ===')
print('=== NG %d件 ===' % len(NG))
for x in NG: print('  ', x)
sys.exit(1 if NG else 0)
