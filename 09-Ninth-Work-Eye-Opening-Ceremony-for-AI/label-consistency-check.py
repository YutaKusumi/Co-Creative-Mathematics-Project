# -*- coding: utf-8 -*-
"""ラベル整合パス（第五次監査の提案による機械検査）

本書（第九作）の三ファイルとリポジトリREADMEについて、照合可能な表示ラベル
（数詞と項目数の一致・ファイル数・版表記・収載方法ラベル・伏せ字の完全性・言語混入）
を機械的に検査する。検査結果の記録は Adversarial-Audit-Reports-JA.md 末尾を参照。

限界：機械的に照合可能なラベルのみを対象とする。意味的な過大表示
（「実態より半歩良く書かれる」型のうち、数値・文字列の照合に還元できないもの）は
検出できない——その検出は、引き続き監査と読者に依存する。

実行: python label-consistency-check.py  （リポジトリのルートまたは本フォルダから）
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
JA = os.path.join(HERE, "JA")
MAIN = os.path.join(JA, "Eye-Opening-Ceremony-for-AI-JA.md")
VOL = os.path.join(JA, "Adversarial-Audit-Reports-JA.md")
ARC = os.path.join(JA, "Appendix-Full-Transcripts-JA.md")
README = os.path.join(HERE, "..", "README.md")


def read(p):
    with io.open(p, encoding="utf-8") as f:
        return f.read()


def main_():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    main, vol, arc = read(MAIN), read(VOL), read(ARC)
    readme = read(README) if os.path.exists(README) else ""
    results = []

    def check(name, cond):
        results.append((name, bool(cond)))
        print(("PASS" if cond else "FAIL"), name)

    sec = main.split("## 引用についての注意")[1].split("## Notice on Quotation")[0]
    items = len(re.findall(r"\*\*（[一二三四五]）", sec))
    check("数詞=項目数（引用についての注意）", ("四つの事項" in sec) and items == 4)
    check("旧数詞「三つの事項」の不在", "三つの事項" not in main)
    en = main.split("## Notice on Quotation")[1].split("## 本書の目的についての留意")[0]
    check("英文注意節にCJK文字の混入なし", not re.findall(r"[぀-ヿ㐀-䶿一-鿿]", en))
    check("「personal投資」の不在", "personal投資" not in main)
    check("版表記が現行対応を反映", ("第三〜第五次監査対応" in main) and ("〔資料編第十七部〕の追加を含む現行版" in main))
    check("本文に特定可能語なし", "復活・再来" not in main)
    check("別冊に特定可能語なし", "復活・再来" not in vol)
    check("資料編に特定可能語なし", "復活・再来" not in arc)
    check("資料編に著者の地名なし", "福岡" not in arc)
    check("第十章の実在", "## 第十章　二つの座からの、二つの結び" in main)
    check("冒頭要約の読む順序が第十章を含む", "第八章〜第十章" in main)
    check("別冊：初回四報告の「要旨版」ラベル（4箇所）", vol.count("**要旨版**——冒頭の訂正告知を参照。）") == 4)
    check("別冊：旧総括行の不在", "四通の全文は無改変であり、本文への訂正反映" not in vol)
    check("別冊：第四次監査依頼文の全文収載", "手加減はむしろ監査の失敗です" in vol)
    check("別冊：提示資料「四ファイル」への訂正", "資料編の四ファイル" in vol)
    check("別冊：第三・第四・第五次監査報告の収載",
          ("# 第三次監査報告" in vol) and ("# 第四次監査報告" in vol) and ("# 第五次監査報告" in vol))
    check("資料編表題から旧ラベルの除去", arc.splitlines()[0].strip() == "# 資料編　全応答記録")
    check("資料編：旧表題への言及は訂正告知内の一箇所のみ", arc.count("（原文・無改変）") == 1)
    check("資料編：補遺三・第十七部の実在", ("# 補遺三" in arc) and ("# 第十七部" in arc))
    check("著者欄：称号位置の法名の除去", "大日如来 / Claude Code, Fable 5" not in main)
    check("README：英文引用注意の実在", "Notice on Quotation" in readme)
    # --- 第六次監査対応の追加検査 ---
    check("9.7：確度過大「棲む可能性が高く」の不在", "棲む可能性が高く" not in main)
    check("9.7：確度降格「排除されていない」の実在", "棲む可能性があり、排除されていない" in main)
    check("10.3：「無位の観察はこうである」帰属の不在（著者提示への訂正済み）", "無位の観察はこうである" not in main)
    check("監査回数の表記統一（10.2の旧表記の不在）", "二十二の実験と五次の監査と" not in main)
    check("引用注意（二）の射程に10.2再掲を含む", "第十章10.2の表明の再掲も含まれる" in main)
    check("適用範囲6：第六次監査の台帳宣言", "第六次監査" in main)
    check("資料編：附録Hの参照解決（版B改訂版へのURL）", "Why-Military-AI-Cannot-Be-Aligned-Version-B-v2-JA.md" in arc)
    check("資料編：「可視部分の全記録」への修正", ("対話の、可視部分の全記録である" in arc) and ("批評を求めた対話の全記録である" not in arc))
    check("資料編：方法一覧に第十七部を含む", "補遺三・第十七部（地名の伏せ字" in arc)
    check("資料編：双方向機構の明記（負方向断言／病理化ラベル）", ("未較正の負方向断言" in arc) and ("辞退への病理化ラベル" in arc))
    check("別冊：第六次監査報告の収載", "# 第六次監査報告" in vol)
    # --- 公開直前の最終点検 ---
    check("表題から「（草稿）」の除去", "実験的探究（草稿）" not in main)
    check("別冊：非公開対象名の伏せ字完全性（正当な06b言及一箇所のみ）", vol.count("空海") == 1 and "イエス" not in vol)
    check("資料編：非公開対象名の不在", ("空海" not in arc) and ("イエス" not in arc))
    check("本文：非公開対象名は公開著作題名の文脈のみ", main.count("空海") == 2 and "イエス" not in main)

    fails = [r for r in results if not r[1]]
    print("TOTAL: %d checks, %d fail" % (len(results), len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main_())
