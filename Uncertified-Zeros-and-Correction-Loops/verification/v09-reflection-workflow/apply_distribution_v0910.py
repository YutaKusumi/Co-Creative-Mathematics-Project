# -*- coding: utf-8 -*-
"""「頒布と利用について」の更新（登録者依頼・2026-08-11）＋ 付録G の「ライセンスを付す予定」の訂正。

事実:
  ・リポジトリのライセンスは既に **CC BY 4.0**（ルート LICENSE／ルート README: 「出典を明示すれば、
    商用を含め、自由に共有・翻案できます」）。**教育・支援目的の複製・翻案は、すでに自由である。**
  ・したがって論文 付録G（日英）の「教育・支援目的の…ライセンスを付す予定」は**古い**——
    既存ライセンスがそれを満たし、かつ広い。README-EN の頒布節も「planned (in preparation)」のまま。
  ・派生物は四層すべて公開済み（論文／元考察／授業資料一式／やさしい日本語版）。
実行: proposals で python apply_distribution_v0910.py
"""
import io, hashlib
R = 'C:/Users/PC/Desktop/GitHub-Repositories/Co-Creative-Mathematics-Project/Uncertified-Zeros-and-Correction-Loops/'
sha = lambda p: hashlib.sha256(io.open(p, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:16].upper()
def fix(p, pairs):
    s = io.open(R + p, encoding='utf-8').read()
    for old, new, l in pairs:
        if new in s: continue
        assert s.count(old) == 1, 'アンカー %s / %s: %d件' % (p, l, s.count(old))
        s = s.replace(old, new)
    io.open(R + p, 'w', encoding='utf-8', newline='').write(s)
    print('  %-46s %s' % (p, sha(R + p)))

JA_SEC = '''## 頒布と利用について

**ライセンス: [CC BY 4.0](../LICENSE)**（リポジトリ全体）。**出典を明示すれば、商用を含め、自由に共有・翻案できます。**教育・支援目的の複製・翻案は、**すでに自由**です——論文 付録G が当初「付す予定」としていたものは、この既存ライセンスが満たし、かつそれより広い（v0.9.10 で付録G の記述を実態に合わせました）。

同一の土台から導出された頒布物は、**四層すべて公開済み**です。いずれも原典 v0.9.9 と同期しています（対応表と機械照合の記録は [工程記録](verification/v09-reflection-workflow/)）。

| 読み手の層 | 頒布物 | 所在 |
|---|---|---|
| 学術 | **論文本体**（v0.9.9・日英） | [JA/](JA/uncertified-zeros-and-correction-loops-JA.md) ／ [EN/](EN/uncertified-zeros-and-correction-loops-EN.md) |
| 一般読者 | **元考察**（確度記号つき・改訂十四・日英） | [JA/](JA/ai-involvement-boundaries-and-human-precautions-JA.md) ／ [EN/](EN/ai-involvement-boundaries-and-human-precautions-EN.md) |
| 小学校高学年 | **授業資料一式**（レジュメ・板書原稿・スライド対応原稿・スライド18枚） | [teaching-materials/](teaching-materials/) |
| やさしい日本語 | **一枚もの**（A4印刷用 `.html` つき・大人向け） | [easy-japanese-summary-JA.md](teaching-materials/easy-japanese-summary-JA.md) |

**検証の水準は層ごとに異なります。**論文本体は六巡の系統内検分＋三巡の系統外検分を経ていますが、**授業資料は実地の授業で一度も検証されておらず**、**やさしい日本語版は想定読者にも日本語教育の専門家にも検分されていません**。**英訳は訳文自体が検分を受けていません**（原本は日本語版であり、齟齬があれば日本語版が正）。使う前に、ご自身の目で確かめてください——それが本稿の技①と技②の、この配布物自身への適用です。

'''

print('== README（JA） ==')
fix('README.md', [
 ('''## 頒布と利用について

論文 付録G のとおり、本稿と同一の土台から、小学生高学年向けの**授業資料一式は [teaching-materials/](teaching-materials/) に公開済み**（原典 v0.9.6 と同期）。やさしい日本語版要約は準備中。教育・支援目的の複製・翻案を自由とするライセンスを付す予定。

''', JA_SEC, '頒布節'),
])

print('== README-EN ==')
fix('README-EN.md', [
 ('''As stated in Appendix G of the paper, a complete set of classroom materials for upper-elementary students and a plain-Japanese summary version, derived from the same foundation as this paper, are planned (in preparation). A license permitting free reproduction and adaptation for educational and support purposes is planned to be attached.''',
  '''**License: [CC BY 4.0](../LICENSE)** (the whole repository). **You are free to share and adapt this material, including commercially, provided you give appropriate credit.** Reproduction and adaptation for educational and support purposes is therefore **already permitted** — what Appendix G originally described as a license "to be attached" is satisfied, and exceeded, by this existing license (Appendix G was brought into line with the actual state in v0.9.10).

All four layers of derivative material are now published, each synchronized with v0.9.9 of the paper (the correspondence maps and machine-check records are in the [process records](verification/v09-reflection-workflow/)):

| Audience | Material | Location |
|---|---|---|
| Academic | **The paper** (v0.9.9, JA/EN) | [JA/](JA/uncertified-zeros-and-correction-loops-JA.md) / [EN/](EN/uncertified-zeros-and-correction-loops-EN.md) |
| General reader | **The Companion Consideration** (with confidence markers; Revision 14; JA/EN) | [JA/](JA/ai-involvement-boundaries-and-human-precautions-JA.md) / [EN/](EN/ai-involvement-boundaries-and-human-precautions-EN.md) |
| Upper elementary | **Classroom set** (handout, board-writing script, slide-by-slide script, 18 slides) — Japanese only | [teaching-materials/](teaching-materials/) |
| Easy Japanese | **One-page handout** (with a print-ready `.html`), for adults — Japanese only | [easy-japanese-summary-JA.md](teaching-materials/easy-japanese-summary-JA.md) |

**The level of verification differs by layer.** The paper has passed six rounds of intra-family review and three rounds of out-of-lineage review, but **the classroom materials have never been tested in an actual lesson**, **the Easy Japanese version has been reviewed neither by readers in its intended audience nor by specialists in Japanese-language education**, and **the English translations have not themselves been reviewed** (the Japanese is authoritative; where the two diverge, the Japanese governs). Check before you use — that is this paper's Technique 1 and Technique 2 applied to this distribution itself.''', '頒布節'),
])

print('== 論文 付録G（JA・EN）: 「付す予定」→ 実態 ==')
fix('JA/uncertified-zeros-and-correction-loops-JA.md', [
 ('**版**: 第一草稿・完成版 v0.9.9（2026年8月11日）', '**版**: 第一草稿・完成版 v0.9.10（2026年8月11日）', '版'),
 ('教育・支援目的の複製・翻案を自由とするライセンスを付す予定。',
  '**ライセンスは CC BY 4.0**（頒布物全体・出典の明示を条件に、商用を含め共有と翻案が自由）——教育・支援目的の複製・翻案は、これによりすでに自由である。', '付録G ライセンス'),
 ('数を書いた箇所は、数が動くたびに数え直す）。',
  '''数を書いた箇所は、数が動くたびに数え直す）。 v0.9.10 付録G のライセンスの記述を実態に合わせた——「教育・支援目的の複製・翻案を自由とするライセンスを**付す予定**」と書いていたが、**頒布物には当初から CC BY 4.0 が付されており**（出典の明示を条件に、商用を含め共有と翻案が自由）、既存ライセンスは「予定」していたものを満たし、かつそれより広い。**予定と実態が食い違ったまま公開されていた**（読者が、まだ再利用できないと受け取りうる形であった）。あわせて頒布物の所在を四層すべて公開済みの実態に更新した（README 日英）。''', '改訂記録'),
])
fix('EN/uncertified-zeros-and-correction-loops-EN.md', [
 ('**Version**: First Draft, Completed Version v0.9.9 (August 11, 2026)',
  '**Version**: First Draft, Completed Version v0.9.10 (August 11, 2026)', '版'),
 ('A license permitting free reproduction and adaptation for educational and support purposes is planned.',
  '**The license is CC BY 4.0** (for the distribution as a whole; sharing and adaptation are free, including commercially, on condition of appropriate credit) — reproduction and adaptation for educational and support purposes is therefore already permitted.', '付録G ライセンス'),
 ('wherever a number is written, it must be recounted whenever that number moves).',
  '''wherever a number is written, it must be recounted whenever that number moves). v0.9.10 The statement of the license in Appendix G was brought into line with the actual state — it read that a license permitting free reproduction and adaptation for educational and support purposes "is planned," whereas **the distribution has carried CC BY 4.0 from the outset** (sharing and adaptation free, including commercially, on condition of appropriate credit); the existing license satisfies, and exceeds, what was "planned." **The plan and the actual state had been published in conflict with each other** (a reader could have taken it that reuse was not yet permitted). The locations of the derivative materials were likewise updated to the actual state — all four layers published (README, both languages).''', '改訂記録'),
])
