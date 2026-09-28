"""第六著作 版B v5 を作る道具（登録者の裁定 2026-09-28：A〜E・名称 v5）。

v4 の日英を写し、決めた箇所（日付の行・v5 の注記・§4-3b の一文・附録 A-4b の式・附録の臨界の時刻の文）だけを直して、
`…-Version-B-v5-JA.md`・`…-v5-EN.md` を新しく作る。v4 のファイルは読むだけで、変えない。
各置き換えは「元の文字列がちょうど一回現れる」ことを確かめてから行い、一つでも外れたら何も書かずに止まる。
"""
import hashlib
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
B = r"C:\Users\PC\Desktop\GitHub-Repositories\Co-Creative-Mathematics-Project\06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned\Version-B-Policy-Edition"
V4 = {"JA": os.path.join(B, "JA", "Why-Military-AI-Cannot-Be-Aligned-Version-B-v4-JA.md"),
      "EN": os.path.join(B, "EN", "Why-Military-AI-Cannot-Be-Aligned-Version-B-v4-EN.md")}
V5 = {k: v.replace("-v4-", "-v5-") for k, v in V4.items()}
SHA_V4 = {"JA": "869E04BE899683A42B54619734DD9FF23794B2A220AEDD40C620A415B0B1DA38",
          "EN": "CA08F2EDD0E7354F9B168A93523CF8BD86C2FBB27E1EED50570E2DF315203DA0"}

NOTE_JA = (
    "> **【改訂版 v5（2026年9月28日）】** 附録 A-4b の証明で、微分不等式を変数分離で解いた結果の**不等号の向きを訂正した**"
    "——「$S(t) \\leq \\ldots$」は「$S(t) \\geq \\ldots$」が正しい（β > 1 のもとでは、負の数を掛ける段と、負の指数乗をとる段で、"
    "向きが二度反転する）。あわせて §4-3b の「T* で発散する」を「遅くとも T* までに発散する」と改め、附録で臨界値に達する時刻を、"
    "発散の時刻 T* と区別した（$t_c \\leq T^\\ast{}$）。**この誤りは初版以来のすべての版にあった。**訂正によって定理の結論"
    "（β > 1 かつ閾値を越えるとき、有限時間で発散する）は変わらず、**訂正によって初めて証明から従う**。定理の記述（§4-3a）・"
    "条件（β > 1 は未検証の経験的条件）・留保（復元力を省いた極限）・確信度台帳（◐）は不変。補遺II（§8-3 の定理節と §12 の柵を含む）"
    "も不変。この誤りは、本書を素材にした解説動画の構想の中で、発散の曲線を図にしようとしたときに見つかった"
    "（Claude Opus 5.5・2026年9月26日）。古い版（v4 以前）の本文は、記録として変えていない。詳細は CHANGELOG.md の v5 の項を参照されたい。"
)
NOTE_EN = (
    "> **[Revised edition v5 (September 28, 2026)]** In the proof in Appendix A-4b, **the direction of the inequality obtained "
    "by solving the differential inequality by separation of variables has been corrected** — \"$S(t) \\leq \\ldots$\" should "
    "read \"$S(t) \\geq \\ldots$\" (for β > 1 the direction flips twice: once when multiplying by a negative number, and once "
    "more when raising to a negative power). In addition, \"diverges at a finite time T*\" in §4-3b has been revised to "
    "\"diverges no later than a finite time T*,\" and in the Appendix the time at which the critical value is reached is now "
    "distinguished from the divergence time T* ($t_c \\leq T^\\ast$). **This error was present in every version since the "
    "first edition.** The correction does not change the conclusion of the theorem (finite-time divergence when β > 1 and the "
    "threshold is exceeded); rather, **only with the correction does that conclusion follow from the proof.** The theorem "
    "statement (§4-3a), its condition (β > 1 is an unverified empirical condition), its caveat (the limit that omits the "
    "restoring force), and the confidence ledger (◐) are unchanged, as is Addendum II (including the theorem section of §8-3 "
    "and the fences of §12). The error was found while planning an explanatory video based on this book, at the moment of "
    "trying to draw the divergence curve (Claude Opus 5.5, September 26, 2026). The text of earlier versions (v4 and before) "
    "has been left unchanged as a record. See the v5 entry in CHANGELOG.md for details."
)

REPL = {
    "JA": [
        ("date", "、2026年8月15日（v4.3・", None),  # anchor check only (handled below)
        ("sec4-3b", "β > 1 であるとき、この微分不等式の解は有限時間 T* で発散する。",
         "β > 1 であるとき、この微分不等式の解は、遅くとも有限時間 T* までに発散する。"),
        ("A-4b", "$$S(t) \\leq \\left[ S(0)^{1-\\beta} - \\alpha(\\beta - 1)t \\right]^{1/(1-\\beta)}$$",
         "$$S(t) \\geq \\left[ S(0)^{1-\\beta} - \\alpha(\\beta - 1)t \\right]^{1/(1-\\beta)} \\quad (0 \\leq t < T^\\ast{})$$"),
        ("t_c", "特に、 $S(T^\\ast{}) \\geq \\Delta S _ {\\mathrm{crit}}$ となる $T^\\ast{}$ が有限時間内に存在する。",
         "特に、 $S(t_c) \\geq \\Delta S _ {\\mathrm{crit}}$ となる時刻 $t_c \\, (\\leq T^\\ast{})$ が有限時間内に存在する。"),
    ],
    "EN": [
        ("date", "; August 15, 2026 (v4.3", None),
        ("sec4-3b", "When β > 1, the solution of this differential inequality diverges at a finite time T*.",
         "When β > 1, the solution of this differential inequality diverges no later than a finite time T*."),
        ("A-4b", "$$S(t) \\leq \\left[ S(0)^{1-\\beta} - \\alpha(\\beta - 1)t \\right]^{1/(1-\\beta)}$$",
         "$$S(t) \\geq \\left[ S(0)^{1-\\beta} - \\alpha(\\beta - 1)t \\right]^{1/(1-\\beta)} \\quad (0 \\leq t < T^\\ast)$$"),
        ("t_c", "In particular, there exists a finite $T^\\ast$ at which $S(T^\\ast) \\geq \\Delta S _ {\\mathrm{crit}}$. □",
         "In particular, there exists a finite time $t_c \\, (\\leq T^\\ast)$ at which $S(t_c) \\geq \\Delta S _ {\\mathrm{crit}}$. □"),
    ],
}
DATE_ADD = {
    "JA": ("反映した）\n", "反映した）、2026年9月28日（改訂版v5・附録 A-4b の証明の不等号の向きを訂正〔≤ → ≥〕し、§4-3b と附録の発散の時刻の"
           "言い回しを正確にした。定理の記述・条件・留保・確信度台帳と、補遺II〔§8-3 の定理節・§12 の柵を含む〕は不変）\n"),
    "EN": ("are also reflected).\n", "are also reflected); September 28, 2026 (revised edition, v5 — the direction of the inequality "
           "in the proof of Appendix A-4b corrected [≤ → ≥], and the wording of the divergence time in §4-3b and in the Appendix "
           "made precise; the theorem statement, its condition and caveats, the confidence ledger, and Addendum II [including "
           "the theorem section of §8-3 and the fences of §12] are unchanged).\n"),
}
NOTE_ANCHOR = {"JA": "> **【v4.3（2026年8月15日）】**", "EN": "> **[v4.3 (August 15, 2026)]**"}
NOTE = {"JA": NOTE_JA, "EN": NOTE_EN}


def sha(b):
    return hashlib.sha256(b).hexdigest().upper()


out = {}
for lang in ("JA", "EN"):
    raw = open(V4[lang], "rb").read()
    if sha(raw) != SHA_V4[lang]:
        raise SystemExit("v4 %s の SHA が記録と違う——止める" % lang)
    if os.path.exists(V5[lang]):
        raise SystemExit("v5 %s は既にある——上書きしない" % lang)
    t = raw.decode("utf-8")
    assert "\r\n" not in t
    # 1) 日付の行：v4.3 の日付を含む「**日付：**」／「**Date:**」の行の末尾に v5 を足す
    lines = t.split("\n")
    idx = [i for i, l in enumerate(lines) if (l.startswith("**日付：**") or l.startswith("**Date:**"))]
    if len(idx) != 1:
        raise SystemExit("%s: 日付の行が %d 行" % (lang, len(idx)))
    i = idx[0]
    old_end, new_end = DATE_ADD[lang]
    if not (lines[i] + "\n").endswith(old_end) or REPL[lang][0][1] not in lines[i]:
        raise SystemExit("%s: 日付の行の終わり方が想定と違う" % lang)
    lines[i] = (lines[i] + "\n")[: -len(old_end)] + new_end.rstrip("\n")
    t = "\n".join(lines)
    # 2) v5 の注記：v4.3 の注記の段落の後（空行の後・--- の前）に入れる
    a = [j for j, l in enumerate(t.split("\n")) if l.startswith(NOTE_ANCHOR[lang])]
    if len(a) != 1:
        raise SystemExit("%s: v4.3 の注記が %d 個" % (lang, len(a)))
    ls = t.split("\n")
    j = a[0]
    if not (ls[j + 1] == "" and ls[j + 2] == "---"):
        raise SystemExit("%s: v4.3 の注記の後が「空行・---」でない" % lang)
    ls[j + 2:j + 2] = [NOTE[lang], ""]
    t = "\n".join(ls)
    # 3) 本文の三か所
    for key, old, new in REPL[lang][1:]:
        n = t.count(old)
        if n != 1:
            raise SystemExit("%s %s: 元の文字列が %d 回（1 回であるべき）" % (lang, key, n))
        t = t.replace(old, new)
    out[lang] = t.encode("utf-8")

for lang in ("JA", "EN"):
    with open(V5[lang], "wb") as f:
        f.write(out[lang])
    print("作成:", os.path.relpath(V5[lang], B), " SHA-256:", sha(out[lang]), " バイト:", len(out[lang]))
    if sha(open(V4[lang], "rb").read()) != SHA_V4[lang]:
        raise SystemExit("v4 %s が変わってしまった" % lang)
print("v4 の日英は変わっていない（SHA 一致）")
