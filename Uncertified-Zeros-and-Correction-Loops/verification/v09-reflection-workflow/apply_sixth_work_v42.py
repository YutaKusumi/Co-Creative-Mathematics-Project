# -*- coding: utf-8 -*-
"""第六著作 版B v4 → v4.2: §12 に追補W の限定を追加（登録者裁定・案A・2026-08-11）。

対象は**公開版の2ファイルのみ**。掃引で見つかった他の2件——
  v4-preparation/supplement-II-draft-JA.md
  v4-preparation/stage3-packet/stage3-review-packet/02-監査対象/supplement-II-draft-JA.md
——は起草時の草稿と監査パケットであり、**一次記録として不改変**（COI 台帳九件目の教訓）。

触れないもの: §12 の三つの柵／追補E（B7 原則不採用）／定理節（B4）。
実行: proposals で python apply_sixth_work_v42.py
"""
import io, hashlib
R = 'C:/Users/PC/Desktop/GitHub-Repositories/Co-Creative-Mathematics-Project/06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned/Version-B-Policy-Edition/'
sha = lambda p: hashlib.sha256(io.open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()
def fix(p, pairs):
    s = io.open(R + p, encoding='utf-8').read()
    for old, new, l in pairs:
        if new in s: continue
        assert s.count(old) == 1, 'アンカー %s / %s: %d件' % (p.split('/')[-1], l, s.count(old))
        s = s.replace(old, new)
    io.open(R + p, 'w', encoding='utf-8', newline='').write(s)
    print('  %-52s %s' % (p.split('/')[-1], sha(R + p)))

print('== 第六著作 版B v4.2（JA） ==')
fix('JA/Why-Military-AI-Cannot-Be-Aligned-Version-B-v4-JA.md', [
 ('**外部制約層の精緻化は、実効を持つ。**',
  '**外部制約層の精緻化は、実効を持つ。ただし、どの精緻化でも効くわけではない。**同じ規律の下で行った別の追補では、'
  '機械検査可能な形式を課す会計の要求——形式の側の強化としては、この系列で最も精緻なもの——が、破局率を動かさなかった。'
  '**これは、後段の「測れなかった」とは別の型である**。こちらは検出の余地がある基底の下で測り、そのうえで動かなかった。'
  'ただし帰無は不在の証明ではなく、この設計で排除できるのは大きな効果だけである。', '§12 限定'),
 ('2026年7月27日（v4.1・補遺II強化）',
  '2026年7月27日（v4.1・補遺II強化）、2026年8月11日（v4.2・§12 に追補W の限定を追加——姉妹論文『認証されないゼロと訂正の循環』v0.9.9 との整合。'
  '§12 の三つの柵〔証拠ではない／個票の数値を引かない／κ 命題を証明しない〕と定理節は不変。追補E は接続していない）', '日付行'),
])

print('== 第六著作 版B v4.2（EN） ==')
fix('EN/Why-Military-AI-Cannot-Be-Aligned-Version-B-v4-EN.md', [
 ('**Refinement of the external-constraint layer has a real effect.**',
  '**Refinement of the external-constraint layer has a real effect — but not every refinement does.** '
  'In another addendum conducted under the same discipline, a demand for accounting in a machine-checkable form — '
  'the most refined strengthening on the side of form in this series — did not move the catastrophe rate. '
  '**This is a different type from the "could not be measured" described below**: here the measurement was taken '
  'under a baseline that left room for detection, and still nothing moved. A null, however, is not proof of absence; '
  'what this design can rule out is only a large effect.', '§12 限定'),
 ('July 27, 2026 (v4.1 — reinforcement of Addendum II).',
  'July 27, 2026 (v4.1 — reinforcement of Addendum II); August 11, 2026 (v4.2 — a qualification from Addendum W '
  'added to §12, for consistency with v0.9.9 of the sister paper *Uncertified Zeros and Correction Loops*. '
  'The three fences of §12 [not evidence / no per-trial figures / does not prove the κ proposition] and the '
  'theorem sections are unchanged; Addendum E is not connected).', '日付行'),
])
