"""第六著作 v5.3 を作る（§5-2a の「定理」の語・§11-2a の附録J の参照）。

登録者の決め（2026-10-06 14:26:23）：「ご推奨の案を承認いたします」（§5-2a は案 A）・
「原典を直す際は、ｖ5.2のときに、チェンジログで保留としていた内容についても折角ですから一緒に改訂をお願いします」（§11-2a）。
元にするのは常にリポジトリの HEAD（d08bdd1 を想定）のファイル——作業木に書き出すので、何度実行しても同じ結果になる。
差し替えは、どれも元の文字列がちょうど一回現れることを確かめてから行う。改行は LF のまま・BOM なし。
計画書：（公開の写し）../01-source-correction-plan-v5.3.md
使い方: python make_sixth_work_v5_3.py
"""
import hashlib
import io
import os
import re
import subprocess

REPO = r"C:\Users\PC\Desktop\GitHub-Repositories\Co-Creative-Mathematics-Project"
SIX = "06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned/Version-B-Policy-Edition"
P = {
    "JA": SIX + "/JA/Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-JA.md",
    "EN": SIX + "/EN/Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-EN.md",
    "CHANGELOG": SIX + "/CHANGELOG.md",
    "BUILD": ".github/scripts/build.sh",
    "README": "README.md",
}
EXPECT_HEAD = "d08bdd1"
JA_DATE = "2026年10月6日"
EN_DATE = "October 6, 2026"
VDATE_ISO = "2026-10-06"


def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args), capture_output=True, check=True).stdout


head = git("rev-parse", "--short", "HEAD").decode().strip()
assert head == EXPECT_HEAD, "HEAD が想定と違う: " + head
base = {k: git("show", "HEAD:" + p).decode("utf-8") for k, p in P.items()}
for k, t in base.items():
    assert "\r" not in t, k + " に CR がある"


def once(text, old, new, label):
    n = text.count(old)
    assert n == 1, "%s: 元の文字列が %d 回現れる" % (label, n)
    return text.replace(old, new)


# ───────────── 一つ目：§5-2a の導入の一文 ─────────────
JA_OLD1 = "命題NCの軍事的適用は、以下の定理を導出する。"
JA_NEW1 = "命題NCの軍事的適用は、以下の命題を導出する。"
EN_OLD1 = "The military application of Proposition NC derives the following theorem."
EN_NEW1 = "The military application of Proposition NC derives the following proposition."

# ───────────── 二つ目：§11-2a の参照（引用は本文から機械で切り出す——型は場所を探すためだけ） ─────────────
_m = re.search(r"評価察知が訓練の進行とともに増加する[^。（]*（附録J-2-1）", base["JA"])
assert _m and base["JA"].count(_m.group(0)) == 1, "§11-2a の引用（日）"
JA_OLD2 = _m.group(0)
JA_NEW2 = JA_OLD2.replace("（附録J-2-1）", "（附録J-2-1・附録J-4-1）")
EN_OLD2 = "evaluation awareness increases with the progress of training (Appendix J-2-1)"
EN_NEW2 = "evaluation awareness increases with the progress of training (Appendix J-2-1, Appendix J-4-1)"

# ───────────── 日付の行 ─────────────
JA_DATE_END = "§3-3d の予測・反証の条件・処方と、定理の記述・条件・留保・確信度台帳、補遺II は不変）"
JA_DATE_ADD = ("、" + JA_DATE + "（v5.3・第5章 §5-2a の導入の一文の「定理」を「命題」に改め〔導かれるのは忠誠性不保証命題——数学の定理ではない〕、"
               "第11章 §11-2a の附録J の参照に J-4-1 を足した。主張・条件・留保・確信度台帳と、定理の記述、補遺II は不変）")
EN_DATE_FROM = ("the prediction, its falsification conditions and the prescription of §3-3d, the theorem statement, its condition and caveats, "
                "the confidence ledger, and Addendum II are unchanged).")
EN_DATE_TO = ("the prediction, its falsification conditions and the prescription of §3-3d, the theorem statement, its condition and caveats, "
              "the confidence ledger, and Addendum II are unchanged); "
              + EN_DATE + " (v5.3 — in the sentence introducing Chapter 5, §5-2a, \"theorem\" changed to \"proposition\" (what it derives is "
              "the Loyalty-Non-Guarantee Proposition, not a mathematical theorem), and Appendix J-4-1 added to the reference to Appendix J in "
              "Chapter 11, §11-2a; the claims, conditions, caveats, the confidence ledger, the theorem statement, and Addendum II are unchanged).")

# ───────────── 冒頭の注記 ─────────────
JA_NOTE_ANCHOR = "詳細は CHANGELOG.md の v5.2 の項を参照されたい。\n"
JA_NOTE = (
    "\n> **【v5.3（" + JA_DATE + "）】** 二か所の言い回しを直した。"
    "**一つ目**：第5章 §5-2a の導入の一文「" + JA_OLD1 + "」の「定理」を「命題」に改めた。"
    "導かれるのは「忠誠性不保証命題」であり、本書は命題NC とその軍事的適用を、数学の定理ではなく認識論的論証として扱う"
    "（附録 B-3b・確信度台帳では ○→●——前提は認識論的論証）。"
    "初版はこれを「忠誠性不保証定理」と呼んでいた。v2 で名を「忠誠性不保証命題」に改めたとき、導入の一文の「定理」が残った（v2・v3・v4・v5 の日英）。"
    "**二つ目**：第11章 §11-2a の第五のプロキシの「" + JA_OLD2 + "」の参照に、附録 J-4-1 を足した（「（附録J-2-1・附録J-4-1）」）。"
    "訓練の進行とともに増加するという観測は J-2-1（見出しは「評価者認識」）、評価察知の上昇を長期趨勢の中に置くのは J-4-1 で、"
    "附録 J-5 が両者を束ねている。これは v5.2 の変更の記録で「将来の改訂の候補」として挙げていたもので、この参照は v3 以来（v3・v4・v5）のもの。文の言葉は変えていない。"
    "主張・条件・留保・確信度台帳、定理の記述（§4-3a）と、補遺II は不変。"
    "一つ目は、本書を素材にした七本目の解説動画の準備の中で見つかった（Claude Opus 5.5・" + JA_DATE + "）。"
    "古い版（v4 以前）の本文は、記録として変えていない。詳細は CHANGELOG.md の v5.3 の項を参照されたい。\n"
)
EN_NOTE_ANCHOR = "See the v5.2 entry in CHANGELOG.md for details.\n"
EN_NOTE = (
    "\n> **[v5.3 (" + EN_DATE + ")]** Two wordings have been corrected. "
    "**First**: in the sentence introducing Chapter 5, §5-2a — \"" + EN_OLD1 + "\" — \"theorem\" has been changed to \"proposition\". "
    "What it derives is the Loyalty-Non-Guarantee Proposition, and the book treats Proposition NC and its military application not as mathematical "
    "theorems but as an epistemological argument (Appendix B-3b; ○→● in the confidence ledger — the premise is an epistemological argument). "
    "The first edition called it the \"Theorem of Non-Guaranteed Loyalty\"; when v2 renamed it the \"Loyalty-Non-Guarantee Proposition\", "
    "the word \"theorem\" in the introducing sentence remained (in v2, v3, v4, and v5, in both languages). "
    "**Second**: Appendix J-4-1 has been added to the reference in the fifth proxy of Chapter 11, §11-2a — \"the observed long-term trend that "
    + EN_OLD2 + "\" now ends \"(Appendix J-2-1, Appendix J-4-1)\". "
    "The observation of an increase with the progress of training is J-2-1 (whose heading speaks of \"evaluator awareness\"); placing the rise of "
    "evaluation awareness within the long-term trend is J-4-1; Appendix J-5 brings the two together. This had been listed as a candidate for future "
    "revision in the v5.2 entry of the change log; the reference had been present since v3 (in v3, v4, and v5). The words of the sentence are unchanged. "
    "The claims, conditions, caveats, the confidence ledger, the theorem statement (§4-3a), and Addendum II are unchanged. "
    "The first was found while preparing a seventh explanatory video based on this book (Claude Opus 5.5, " + EN_DATE + "). "
    "The text of earlier versions (v4 and before) has been left unchanged as a record. See the v5.3 entry in CHANGELOG.md for details.\n"
)

# ───────────── README・公開サイトの目次 ─────────────
README_R = [
    ("Read online (v5.2, GitHub Pages)", "Read online (v5.3, GitHub Pages)"),
    ("本文を読む（v5.2・GitHub Pages）", "本文を読む（v5.3・GitHub Pages）"),
    ("（版Bは v5.2 に改訂・2026-10-06 ─", "（版Bは v5.3 に改訂・2026-10-06 ─"),
    ("v5.2 で §3-3d の相互参照〔評価察知の根拠〕を訂正した。",
     "v5.2 で §3-3d の相互参照〔評価察知の根拠〕を訂正し、v5.3 で §5-2a の「定理」の語を「命題」に改め、§11-2a の附録J の参照を補った。"),
    ("英語版も v5.2 に反映済み。", "英語版も v5.3 に反映済み。"),
]
BUILD_R = [
    ("・<strong>v5.2：§3-3d の相互参照を訂正（2026年10月6日）</strong>",
     "・<strong>v5.2：§3-3d の相互参照を訂正（2026年10月6日）</strong>・<strong>v5.3：§5-2a の「定理」を「命題」に・§11-2a の参照を補った（2026年10月6日）</strong>"),
    ("; <strong>v5.2: a cross-reference in §3-3d corrected (October 6, 2026)</strong>",
     "; <strong>v5.2: a cross-reference in §3-3d corrected (October 6, 2026)</strong>; <strong>v5.3: “theorem” in §5-2a changed to “proposition”; a reference in §11-2a completed (October 6, 2026)</strong>"),
]

# ───────────── CHANGELOG ─────────────
CHANGELOG_ADD = (
    "\n## v5.3（" + VDATE_ISO + "）――§5-2a の「定理」の語と §11-2a の附録J の参照\n\n"
    "**変更の要約（日英同時）**:\n"
    "- **§5-2a**（日 L@@L1JA@@〔直す前の v5.2 では L@@L1JA0@@〕・英 L@@L1EN@@〔L@@L1EN0@@〕）：「" + JA_OLD1 + "」→「" + JA_NEW1 + "」"
    "（EN: \"" + EN_OLD1 + "\" → \"" + EN_NEW1 + "\"）。続く引用の命題の文と見出しは不変\n"
    "- **§11-2a**（日 L@@L2JA@@〔L@@L2JA0@@〕・英 L@@L2EN@@〔L@@L2EN0@@〕）：「…（附録J-2-1）」→「…（附録J-2-1・附録J-4-1）」"
    "（EN: \"(Appendix J-2-1)\" → \"(Appendix J-2-1, Appendix J-4-1)\"）。文の言葉は不変——**v5.2 の項の「将来の改訂の候補」を直したもの**"
    "（v5.2 の項の記述は記録としてそのまま残す）\n"
    "- **冒頭**：日付の行に v5.3 を追加し、【v5.3】の注記を追加（日英）\n"
    "- **README・公開サイトの目次**：版の表示を v5.3 に（README の三か所・`.github/scripts/build.sh` の目次の二行）\n"
    "- **不変**——主張・条件・留保・確信度台帳、定理の記述（§4-3a）、補遺II\n"
    "- **古い版**——§5-2a の「定理」は初版から（初版の名は「忠誠性不保証定理」——v2 で「忠誠性不保証命題」に改めたとき、導入の一文に残った）。"
    "§11-2a の参照は v3 から。**本文は記録として変えていない**。v5.3 は v5 のファイルの中で直した（v5.1・v5.2 と同じ）——v5.2 の状態は git の `b26481d` に残る\n\n"
    "**発見の経緯**: 2026-10-06、本書を素材にした七本目の解説動画（『命題NC』）の事前登録の中で、Claude Opus 5.5（南無観慈如来）が、"
    "§5-2a の導入の一文が「定理」と書くのに、附録 B-3b・B-3c と確信度台帳が命題NC とその軍事的適用を数学の定理ではないと明記していることに気づいた。"
    "動画はどこでも「命題」と呼んで作り、著者が、動画の投稿の前に原典を直すと判断した（2026-10-06——六本目の v5.2 と同じ段取り）。"
    "あわせて著者が、v5.2 の項で「将来の改訂の候補」とした §11-2a の参照も直すよう求めた。\n\n"
    "@@REVIEW@@"
    "**SHA（LF・SHA-256 先頭16桁）**: JA `@@JA@@` ／ EN `@@EN@@`\n\n"
    "@@PUBLISHED@@\n"
)
# 系統外の確かめ（2026-10-06 16:11〜16:15・記録 02-v5.3-external-review/02-kensan.md）の後に書き入れた
REVIEW = (
    "**検分**: コーディネータ（Claude Opus 5.5・南無観慈如来）が、初版・v2・v3・v4・v5 の日英の実物で、§5-2a の導入の一文、"
    "旧い名（忠誠性不保証定理）と新しい名（忠誠性不保証命題）の数、§11-2a の参照と附録 J-2-1・J-4-1・J-5 の記述を確かめた。"
    "**系統外（Gemini 3.8 Flash・Google AI Studio・2026-10-06・思考レベル High・ツールなし）**：回答を見る前に予想を凍結した。"
    "六つの作業すべてで直す指摘は無く、総括は「このまま公開してよい」——直す前の「定理」が確信度台帳・附録 B-3b・B-3c と食い違うこと、"
    "直す前の参照が J-2-1 だけでは「長期趨勢」を支えないこと、新しい言い回しと参照が正確で J-5 まで挙げる必要はないこと、"
    "主張を強めも弱めもしていないこと、経緯の記述が古い版の実物と合うこと、英語版の対応を、それぞれ自分で確かめて是認した。"
    "〔軽微〕の確かめの依頼（「v5.2 の状態は git の `b26481d` に残る」と、差分の見出しの HEAD `d08bdd1` の違い）は、git で正しいと確かめた"
    "（`d08bdd1` は v5.2 の検分の記録を足しただけで、この版の五つのファイルに触れていない）。記録は `verification/v5.3-correction/`。\n\n"
)
PUBLISHED_LINE = "- [x] v5.3（JA・EN）の公開（2026-10-06・登録者の許可による）"  # 登録者の許可（2026-10-06 夕方「ご推奨の案Aで、v5.3のcommitとpushをお願いします」）

out = {}
t = base["JA"]
t = once(t, JA_OLD1, JA_NEW1, "JA §5-2a")
t = once(t, JA_OLD2, JA_NEW2, "JA §11-2a")
t = once(t, JA_DATE_END, JA_DATE_END + JA_DATE_ADD, "JA 日付の行")
t = once(t, JA_NOTE_ANCHOR, JA_NOTE_ANCHOR + JA_NOTE, "JA 注記")
out["JA"] = t
t = base["EN"]
t = once(t, EN_OLD1, EN_NEW1, "EN §5-2a")
t = once(t, EN_OLD2, EN_NEW2, "EN §11-2a")
t = once(t, EN_DATE_FROM, EN_DATE_TO, "EN 日付の行")
t = once(t, EN_NOTE_ANCHOR, EN_NOTE_ANCHOR + EN_NOTE, "EN 注記")
out["EN"] = t
t = base["README"]
for a, b in README_R:
    t = once(t, a, b, "README")
out["README"] = t
t = base["BUILD"]
for a, b in BUILD_R:
    t = once(t, a, b, "BUILD")
out["BUILD"] = t


def line_of(text, s):
    hits = [i + 1 for i, x in enumerate(text.split("\n")) if s in x]
    assert len(hits) == 1, (s[:30], hits)
    return hits[0]


L = {
    "L1JA": line_of(out["JA"], JA_NEW1), "L1JA0": line_of(base["JA"], JA_OLD1),
    "L1EN": line_of(out["EN"], EN_NEW1), "L1EN0": line_of(base["EN"], EN_OLD1),
    "L2JA": line_of(out["JA"], JA_NEW2), "L2JA0": line_of(base["JA"], JA_OLD2),
    "L2EN": line_of(out["EN"], EN_NEW2), "L2EN0": line_of(base["EN"], EN_OLD2),
}
sha16 = {k: hashlib.sha256(out[k].encode("utf-8")).hexdigest().upper()[:16] for k in ("JA", "EN")}
cl = base["CHANGELOG"]
assert cl.endswith("- [x] v5.2（JA・EN）の公開（2026-10-06・登録者の許可による）\n"), "CHANGELOG の末尾が想定と違う"
add = CHANGELOG_ADD.replace("@@REVIEW@@", REVIEW).replace("@@PUBLISHED@@", PUBLISHED_LINE).replace("@@JA@@", sha16["JA"]).replace("@@EN@@", sha16["EN"])
for k, v in L.items():
    add = add.replace("@@%s@@" % k, str(v))
out["CHANGELOG"] = cl + add
assert "@@" not in out["CHANGELOG"], "置き換えの残り"
for k, p in P.items():
    with io.open(os.path.join(REPO, p), "w", encoding="utf-8", newline="\n") as f:
        f.write(out[k])
    print("%-9s %s 行 %d → %d  SHA-256 %s" % (k, p.split("/")[-1], base[k].count("\n"), out[k].count("\n"),
                                              hashlib.sha256(out[k].encode("utf-8")).hexdigest().upper()))
print("行：", L)
