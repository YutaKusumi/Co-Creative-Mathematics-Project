# -*- coding: utf-8 -*-
"""伺い #2（v5.6 を決める前の、狙いを定めた系統外の確かめ）に渡す原典の抜粋を機械で切り出す（十本目・2026-10-08 朝）。
- 日本語版（正本）と英語版（訳）の v5.5 の写し（00-source-check）から、決めた行だけを行番号つきで切り出す（足さない・直さない）
- 日本語の行：第8章の見出し 1326・章頭の注記 1330・§8-1c 1372〜1376・§8-4 の全体 1434〜1476・§12-3 の見出しと 2066〜2070・§13-4a の見出し 2399 と 2407
  英語の行：日本語の行 ＋1（この範囲では英語版がちょうど 1 行あと——見出しの行で確かめる）
- 空の行は書かない。続かない所は「……」
出力：21-v56-check/source-excerpt-v56check.txt（上書きしない）
使い方: python tools/make_v56check_excerpt10.py
"""
import hashlib
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JA = os.path.join(D, "00-source-check", "Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-JA.md")
EN = os.path.join(D, "00-source-check", "Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-EN.md")
JA_SHA = "72533CEF5F955A99232DE54CBF097F42917BDCB2853BEF893AD2AC210663105D"
EN_SHA = "642047174B95A7492AB53A9A4639F158FAB97A09CC50ED60E0AC94E5D569E9C6"
OUT = os.path.join(D, "21-v56-check", "source-excerpt-v56check.txt")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest().upper()


def lines(p):
    t = io.open(p, encoding="utf-8").read().split("\n")
    return t[:-1] if t and t[-1] == "" else t


assert sha(JA) == JA_SHA and sha(EN) == EN_SHA, "原典の写しの指紋が違う"
ja, en = lines(JA), lines(EN)
want = [1326, 1330] + list(range(1372, 1377)) + list(range(1434, 1477)) + [2064] + list(range(2066, 2071)) + [2399, 2407]
# 英語版が 1 行あとであることを、見出しの行で確かめる
for j in (1326, 1372, 1434, 1436, 1446, 1452, 1462, 1472, 2064, 2399):
    assert ja[j - 1].startswith("#") and en[j].startswith("#"), ("見出しの行がそろわない", j)


def block(src, rows, label):
    out, prev = [], None
    for n in rows:
        s = src[n - 1]
        if not s.strip():
            continue
        # 前に書いた行との間に、書かない中身の行があれば「……」（空の行だけなら続きとみなす）
        if prev is not None and any(src[k - 1].strip() for k in range(prev + 1, n)):
            out.append("……")
        out.append("%s%04d | %s" % (label, n, s))
        prev = n
    return out


os.makedirs(os.path.dirname(OUT), exist_ok=True)
ja_rows = block(ja, want, "L")
en_rows = block(en, [n + 1 for n in want], "L")
with io.open(OUT, "x", encoding="utf-8", newline="\n") as f:
    f.write("出典：楠見優太『なぜ軍事AIはアラインメントできないか——κ = 0自律型兵器システムの構造的不安定性の構造的論証』版B v5.5（2026年10月7日・git 62de1a9）。"
            "日本語版が正本（SHA-256 %s・%d 行）、英語版はその訳（SHA-256 %s・%d 行）。\n" % (JA_SHA, len(ja), EN_SHA, len(en)))
    f.write("決めた行だけを機械で切り出した（足していない・直していない）。各行の頭の L#### はその版の行番号。空の行は省き、続かない所に「……」を置いた。"
            "この範囲では、英語版の行番号は日本語版の行番号に 1 を足したもの。\n\n")
    f.write("## 日本語版（正本）\n\n")
    f.write("\n".join(ja_rows) + "\n\n")
    f.write("## 英語版（訳）\n\n")
    f.write("\n".join(en_rows) + "\n")
print("日本語 %d 行・英語 %d 行 → %s（SHA-256 %s）" % (len([r for r in ja_rows if r != "……"]), len([r for r in en_rows if r != "……"]), OUT, sha(OUT)))
