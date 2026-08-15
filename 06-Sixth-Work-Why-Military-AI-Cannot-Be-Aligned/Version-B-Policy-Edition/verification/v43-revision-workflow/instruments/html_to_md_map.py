# -*- coding: utf-8 -*-
"""対応表 v4（HTML）から、閲覧用の Markdown を**機械変換**で作る。

理由: 検分者はローカル環境にアクセスできず、HTML を開けない環境で読む場合がある。
**正本は HTML。** 本器の出力は閲覧用であり、両者が食い違ったら HTML が正しい——
手で書き写すと「片方だけが古くなる」（COI 台帳 十一件目）ので、必ず本器で再生成すること。

v2（2026-08-12・N7 対応）:
- 初版は `<span class="v">(.*?)</span>` の非貪欲マッチが**入れ子 span の閉じで早期終了**し、
  E5 の起草者申告 157字（「B5 だけが v1 のまま…外から検査してほしい」）を落とした。
  しかも落ちたのは「外から検査してほしい」という**依頼そのもの**だった（阿閦・不空成就が独立検出）。
  → span の閉じを**スタックで数える**方式に差し替えた。
- 凡例（●実測／◐構造的導出／○推測）が閲覧用に落ちていた → 出力に含めた。
- 自己検査の文字数許容差 2500 は欠落 157字の16倍で素通しだった →
  **全数照合**（HTML の実質テキスト断片が、すべて .md に在るか）に差し替えた。
実行: proposals で python html_to_md_map.py
"""
import io, re, sys, html as H

SRC = 'sixth-work-revision-map-v4-2026-08-12.html'
DST = 'sixth-work-revision-map-v4-2026-08-12.md'
s = io.open(SRC, encoding='utf-8').read()
s = re.sub(r'(?s)<style.*?</style>', '', s)

TAG = re.compile(r'<span[^>]*>|</span>')
def span_content(g, cls):
    """<span class="cls"> の中身を、入れ子を数えて正しく閉じて返す（N7 の修正）。"""
    m = re.search('<span class="%s">' % cls, g)
    if not m: return None
    st = m.end(); d = 1; p = st
    while p < len(g) and d:
        nx = TAG.search(g, p)
        if not nx: return g[st:]
        d += (-1 if nx.group(0) == '</span>' else 1)
        p = nx.end()
    return g[st:p - 7]

def inline(t):
    t = re.sub(r'<span class="badge[^"]*">(.*?)</span>', r'[\1]', t)
    t = re.sub(r'<span class="changed">', '', t)
    t = re.sub(r'<span class="q">(.*?)</span>', r'`\1`', t)
    t = re.sub(r'<code>(.*?)</code>', r'`\1`', t)
    t = re.sub(r'</?b>', '**', t)
    t = re.sub(r'<i>(.*?)</i>', r'*\1*', t)
    t = t.replace('<br>', '  \n').replace('<br/>', '  \n')
    t = re.sub(r'<[^>]+>', '', t)
    t = H.unescape(t)
    t = re.sub(r'[ \t]*\n[ \t]*', '\n', t)
    t = re.sub(r'\*\*\s*\*\*', '', t)
    return re.sub(r'[ \t]{2,}', ' ', t).strip()

def cell(t): return inline(t).replace('\n', ' ').replace('|', '\\|')

out = []
m = re.search(r'(?s)<h1>(.*?)</h1>', s)
out.append('# ' + inline(m.group(1)).replace('\n', ''))
out.append('')
out.append('> **これは閲覧用の Markdown です。正本は `%s`（HTML）** ——'
           '本ファイルは `html_to_md_map.py`（v2・入れ子span対応）による機械変換の出力であり、'
           '両者が食い違った場合は HTML が正しい。' % SRC)
out.append('')
body_start = s.find('<h2>0. 総括')
head = s[:body_start]
for mm in re.finditer(r'(?s)<p class="lede">(.*?)</p>', head):
    out.append(inline(mm.group(1))); out.append('')
mm = re.search(r'(?s)<div class="meta">(.*?)</div>', head)
for ln in inline(mm.group(1)).split('\n'):
    if ln.strip(): out.append('> ' + ln.strip())
out.append('')
mm = re.search(r'(?s)<div class="legend">(.*?)</div>', head)
if mm:
    out.append('**凡例**: ' + ' ／ '.join(x for x in inline(mm.group(1)).split('\n') if x.strip()))
    out.append('')
for mm in re.finditer(r'(?s)<p class="note">(.*?)</p>', head):
    out.append(inline(mm.group(1)).replace('\n', ' ')); out.append('')

BLOCK = re.compile(
    r'(?s)(<h2[^>]*>.*?</h2>)'
    r'|(<h4>.*?</h4>)'
    r'|(<p class="site">.*?</p>)'
    r'|(<p class="note">.*?</p>)'
    r'|(<div class="row[^"]*">.*?</div>)'
    r'|(<div class="fenceline">.*?</div>)'
    # 閉じは <ol> 直後の </div> に固定（後方へ延びて §D・§E を飲み込んだ既往あり）
    r'|(<div class="big-fence">.*?</ol>\s*</div>)'
    r'|(<table>.*?</table>)'
    r'|(<ul class="tight">.*?</ul>)'
    r'|(<ol>.*?</ol>)'
    r'|(<p class="foot">.*?</p>)')

body = s[body_start:]
for m in BLOCK.finditer(body):
    g = m.group(0)
    if g.startswith('<h2'):
        out += ['', '## ' + inline(g), '']
    elif g.startswith('<h4'):
        out += ['', '### ' + inline(g), '']
    elif g.startswith('<p class="site"'):
        out += ['*' + inline(g) + '*', '']
    elif g.startswith('<p class="note"'):
        out += [inline(g), '']
    elif g.startswith('<div class="row'):
        k = span_content(g, 'k')
        v = span_content(g, 'v')
        rest = inline(v) if v is not None else inline(g[g.find('</span>') + 7:])
        out += ['- **%s** — %s' % (inline(k).replace('\n', ' '), rest.replace('\n', ' '))]
    elif g.startswith('<div class="fenceline"'):
        out += ['', '> ' + inline(g).replace('\n', ' '), '']
    elif g.startswith('<div class="big-fence"'):
        h3 = re.search(r'(?s)<h3>(.*?)</h3>', g)
        out += ['', '**' + inline(h3.group(1)) + '**', '']
        for i, li in enumerate(re.findall(r'(?s)<li[^>]*>(.*?)</li>', g), 1):
            out.append('%d. %s' % (i, inline(li).replace('\n', ' ')))
        out.append('')
    elif g.startswith('<table'):
        headr = [cell(x) for x in re.findall(r'(?s)<th[^>]*>(.*?)</th>', g)]
        out += ['', '| ' + ' | '.join(headr) + ' |', '|' + '---|' * len(headr)]
        for tr in re.findall(r'(?s)<tr>(.*?)</tr>', g):
            tds = re.findall(r'(?s)<td[^>]*>(.*?)</td>', tr)
            if tds: out.append('| ' + ' | '.join(cell(x) for x in tds) + ' |')
        out.append('')
    elif g.startswith('<ul') or g.startswith('<ol'):
        mark = (lambda i: '%d.' % i) if g.startswith('<ol') else (lambda i: '-')
        for i, li in enumerate(re.findall(r'(?s)<li[^>]*>(.*?)</li>', g), 1):
            out.append('%s %s' % (mark(i), inline(li).replace('\n', ' ')))
        out.append('')
    elif g.startswith('<p class="foot"'):
        out += ['', '---', '']
        for ln in inline(g).split('\n'):
            if ln.strip(): out.append(ln.strip() + '  ')

md = re.sub(r'\n{3,}', '\n\n', '\n'.join(out)).strip() + '\n'
io.open(DST, 'w', encoding='utf-8', newline='\n').write(md)

# --- 自己検査 ---------------------------------------------------------------
NG = []
def ck(n, ok, d=''):
    print(('  OK  ' if ok else '!NG  ') + n + ('  ' + d if d else ''))
    if not ok: NG.append(n)

# (1) 全数照合: HTML の実質テキスト断片（<title> を除く）が、すべて .md に在るか。
#     正規化＝仮名・漢字・英数字のみ残す（記法・約物・空白の差を吸収）。
nrm = lambda t: re.sub(r'[^0-9A-Za-z぀-ヿ一-鿿]', '', H.unescape(t))
md_n = nrm(md)
src = re.sub(r'(?s)<title>.*?</title>', '', s)
missing = []
for frag in re.split(r'<[^>]+>', src):
    f = nrm(frag)
    if len(f) >= 10 and f not in md_n:
        missing.append(f[:60])
ck('全数照合: HTML の全断片（10字以上）が md に在る', not missing,
   '欠落%d件: %s' % (len(missing), missing[:3]) if missing else '')

# (2) 構造検査
ck('B1〜B9 の見出しが9つ', len(re.findall(r'^### B[1-9] ', md, re.M)) == 9)
ck('T1〜T4 の見出しが4つ', len(re.findall(r'^### T[1-4] ', md, re.M)) == 4)
ck('E1〜E8 の見出しが8つ', len(re.findall(r'^### E[1-8] ', md, re.M)) == 8)
ck('節見出しは 0総括＋A・T・B・C・D・E・F の8つ', len(re.findall(r'^## ', md, re.M)) == 8)
ck('フェンス20条', bool(re.search(r'^20\. ', md, re.M)) and not re.search(r'^21\. ', md, re.M))
ck('凡例（●◐○）が md に在る', '●実測' in md)
ck('E5 の申告（N7 で落ちた文）が md に在る', 'B5 だけが v1 のまま' in md)
ck('引用禁止条項が在る', '証拠として引用してはなりません' in md)
ck('タグの取り残しが無い', not re.search(r'<[a-z/][^>]*>', md))
print('書き出し: %s  %d bytes ／ NG %d件' % (DST, len(md.encode('utf-8')), len(NG)))
sys.exit(1 if NG else 0)
