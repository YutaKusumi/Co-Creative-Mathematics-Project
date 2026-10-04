# -*- coding: utf-8 -*-
"""changes.json（台本が実際に行った置き換えの組）から、登録者に見ていただく一覧を書き出す。
初版は置き場と写しの字の単位の比較（difflib）だったが、この PC では重すぎて止めた（05:5x）——組から直接書く形に替えた。"""
import io, os, json
HERE = os.path.dirname(os.path.abspath(__file__)).replace(chr(92), '/') + '/'
C = json.load(io.open(HERE + 'changes.json', encoding='utf-8'))
NAMES = {
 'JA/ai-involvement-boundaries-and-human-precautions-JA.md': '元考察（日本語）',
 'EN/ai-involvement-boundaries-and-human-precautions-EN.md': '元考察（英語）',
 'JA/uncertified-zeros-and-correction-loops-JA.md': '論文（日本語）',
 'EN/uncertified-zeros-and-correction-loops-EN.md': '論文（英語）',
 'README.md': 'README（日本語）', 'README-EN.md': 'README（英語）',
 'teaching-materials/README.md': '授業資料の README',
 'verification/v09-reflection-workflow/check_readme_version.py': '常設検査の許可リスト',
}
out = ['# 置き換えの一覧（台本 apply_r15_v0911.py が写しに行った 34 組）', '',
       '各組は「旧文字列がちょうど一件」を確かめてから置き換えた。改行は ⏎ で示す。', '']
cur = None
for i, c in enumerate(C, 1):
    rel = c['file'].split('Uncertified-Zeros-and-Correction-Loops/', 1)[1]
    if rel != cur:
        out += ['', '## %s　`%s`' % (NAMES.get(rel, rel), rel), '']
        cur = rel
    old, new = c['old'].replace('\n', '⏎'), c['new'].replace('\n', '⏎')
    # 末尾に足すだけの組は、足した部分だけを示す
    if new.startswith(old):
        out += ['%d. **%s**（後ろに足した）' % (i, c['label']), '', '   > ' + new[len(old):], '']
    elif new.endswith(old):
        out += ['%d. **%s**（前に足した）' % (i, c['label']), '', '   > ' + new[:-len(old)], '']
    else:
        # 共通の頭と尻を除いて、変わった所だけを示す
        a = 0
        while a < min(len(old), len(new)) and old[a] == new[a]:
            a += 1
        b = 0
        while b < min(len(old), len(new)) - a and old[-1 - b] == new[-1 - b]:
            b += 1
        o, n = old[a:len(old) - b], new[a:len(new) - b]
        ctx_pre = old[max(0, a - 30):a]
        out += ['%d. **%s**' % (i, c['label']), '',
                '   - 前：…' + ctx_pre,
                '   - **旧**：' + (o or '（無し）'),
                '   - **新**：' + (n or '（無し）'), '']
io.open(HERE + '01-changes.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
print('書き出した', len(C), '組')
