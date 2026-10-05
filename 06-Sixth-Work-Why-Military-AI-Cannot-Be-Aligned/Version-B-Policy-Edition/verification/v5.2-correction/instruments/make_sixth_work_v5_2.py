"""第六著作 v5.2 を作る（§3-3d の相互参照の訂正・案 A・登録者の裁定 2026-10-06「ご推奨の案で進めてください」）。

元にするのは常にリポジトリの HEAD（59aee42 を想定）のファイル——作業木に書き出すので、何度実行しても同じ結果になる。
差し替えは、どれも元の文字列がちょうど一回現れることを確かめてから行う。改行は LF のまま・BOM なし。
計画書：（公開の写し）../01-source-correction-plan-v5.2.md
使い方: python make_sixth_work_v5_2.py
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
EXPECT_HEAD = "59aee42"
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


# ───────────── 日本語版 ─────────────
JA_OLD = "METR の観測（第4章 §4-1b で詳述）は、モデルが評価されていることを検知する能力が、既に現実のモデルで確認されていることを示す。"
JA_NEW = ("モデルが評価されていることを検知する能力（評価察知）は、既に現実のモデルで経験的に記録されている"
          "（複数の独立した研究——第6章 §6-1c；Mythos の源自身による評価察知の注記——第4章 §4-1b）。")
JA_DATE_END = "§4-3b の出発点を附録 A-4b と同じ「仮定すると」に改めた。定理の記述・条件・留保・確信度台帳と、補遺II は不変）"
JA_DATE_ADD = ("、" + JA_DATE + "（v5.2・§3-3d の相互参照を訂正——評価察知の根拠を、METR の観測〔第4章 §4-1b〕ではなく、"
               "第6章 §6-1c の実証研究と第4章 §4-1b の源の注記とした。§3-3d の予測・反証の条件・処方と、定理の記述・条件・留保・確信度台帳、補遺II は不変）")
JA_NOTE_ANCHOR = "詳細は CHANGELOG.md の v5.1 の項を参照されたい。\n"
JA_NOTE = (
    "\n> **【v5.2（" + JA_DATE + "）】** 第3章 §3-3d の相互参照を訂正した。§3-3d は、評価察知（モデルが評価されていることを検知する能力）が"
    "現実のモデルで確認されていることの根拠を「METR の観測（第4章 §4-1b で詳述）」としていたが、§4-1b（Mythos の症状一）に METR は出てこない。"
    "また、本書のほかの METR の記述（§4-3d の reward hacking の報告、§6-1c の、人工的なトイ実証が現実の動機について限られた証拠しか与えないという慎重な評価など）も、"
    "評価察知の観測ではない。本書の中の評価察知の根拠は、§6-1c の実証研究（*Large Language Models Often Know When They Are Being Evaluated*〔arXiv:2505.23836, 2025〕と、"
    "Apollo Research・OpenAI 2025 の反スキーミング訓練の負荷試験）と、§4-1b の源（Mythos の System Card）自身の評価察知の注記である。"
    "そこで当該の一文を、この二つを指すように改め、述語も §6-1c と同じ「経験的に記録されている」に揃えた。"
    "**この食い違いは、§3-3d を新設した v3 以来、v3・v4・v5 にあった。**"
    "§3-3d の予測・反証の条件・処方、定理の記述（§4-3a）・条件・留保・確信度台帳、補遺II は不変。"
    "これは、本書を素材にした六本目の解説動画の準備の中で見つかった（Claude Opus 5.5・2026年10月5日）。"
    "古い版（v4 以前）の本文は、記録として変えていない。詳細は CHANGELOG.md の v5.2 の項を参照されたい。\n"
)

# ───────────── 英語版 ─────────────
EN_OLD = ("METR's observations (detailed in Chapter 4, §4-1b) show that the ability of models to detect that they are being evaluated "
          "has already been confirmed in real models.")
EN_NEW = ("The ability of models to detect that they are being evaluated (evaluation-awareness) has already been documented empirically in real models "
          "(several independent studies — Chapter 6, §6-1c; the note on evaluation-awareness in Mythos's own source — Chapter 4, §4-1b).")
EN_DATE_END = "the theorem statement, its condition and caveats, the confidence ledger, and Addendum II are unchanged)."
EN_DATE_ADD_FROM = "the theorem statement, its condition and caveats, the confidence ledger, and Addendum II are unchanged)."
EN_DATE_ADD_TO = ("the theorem statement, its condition and caveats, the confidence ledger, and Addendum II are unchanged); "
                  + EN_DATE + " (v5.2 — a cross-reference in §3-3d corrected: the grounds for evaluation-awareness now point to the empirical studies "
                  "of Chapter 6, §6-1c and the source's own note in Chapter 4, §4-1b, not to \"METR's observations\" in §4-1b; the prediction, "
                  "its falsification conditions and the prescription of §3-3d, the theorem statement, its condition and caveats, the confidence ledger, "
                  "and Addendum II are unchanged).")
EN_NOTE_ANCHOR = "See the v5.1 entry in CHANGELOG.md for details.\n"
EN_NOTE = (
    "\n> **[v5.2 (" + EN_DATE + ")]** A cross-reference in Chapter 3, §3-3d has been corrected. §3-3d gave, as the grounds for evaluation-awareness "
    "(the ability of models to detect that they are being evaluated) having been confirmed in real models, \"METR's observations (detailed in Chapter 4, §4-1b)\"; "
    "but METR does not appear in §4-1b (symptom one of Mythos). Nor are the book's other references to METR (the reports of reward hacking in §4-3d, "
    "the cautious assessment in §6-1c that artificial toy demonstrations give only limited evidence about real motives, and others) observations of evaluation-awareness. "
    "Within the book, the grounds for evaluation-awareness are the empirical studies of §6-1c (*Large Language Models Often Know When They Are Being Evaluated*, "
    "arXiv:2505.23836, 2025; and the 2025 anti-scheming stress-tests of Apollo Research and OpenAI) and the note on evaluation-awareness in the source of §4-1b "
    "(Mythos's System Card) itself. The sentence has therefore been revised to point to these two, and its predicate has been brought to the same temperature "
    "as §6-1c (\"documented empirically\"). **This inconsistency had been present since v3, when §3-3d was added — in v3, v4, and v5.** "
    "The prediction, its falsification conditions and the prescription of §3-3d, the theorem statement (§4-3a), its condition and caveats, the confidence ledger, "
    "and Addendum II are unchanged. This was found while preparing a sixth explanatory video based on this book (Claude Opus 5.5, October 5, 2026). "
    "The text of earlier versions (v4 and before) has been left unchanged as a record. See the v5.2 entry in CHANGELOG.md for details.\n"
)

# ───────────── README・公開サイトの目次 ─────────────
README_R = [
    ("Read online (v5.1, GitHub Pages)", "Read online (v5.2, GitHub Pages)"),
    ("本文を読む（v5.1・GitHub Pages）", "本文を読む（v5.2・GitHub Pages）"),
    ("（版Bは v5.1 に改訂・2026-09-29 ─ v5〔2026-09-28〕で附録 A-4b の証明の不等号の向きを訂正〔≤ → ≥〕、v5.1 で附録I の β の定め方を §4-3b と揃え、§4-3b の出発点を「仮定すると」に改めた。定理の記述・条件・留保と補遺IIは不変。英語版も v5.1 に反映済み。",
     "（版Bは v5.2 に改訂・2026-10-06 ─ v5〔2026-09-28〕で附録 A-4b の証明の不等号の向きを訂正〔≤ → ≥〕、v5.1〔2026-09-29〕で附録I の β の定め方を §4-3b と揃え、§4-3b の出発点を「仮定すると」に改め、v5.2 で §3-3d の相互参照〔評価察知の根拠〕を訂正した。定理の記述・条件・留保と補遺IIは不変。英語版も v5.2 に反映済み。"),
]
BUILD_R = [
    ("・<strong>v5.1：附録I の β の定め方を §4-3b と揃えた（2026年9月29日）</strong>",
     "・<strong>v5.1：附録I の β の定め方を §4-3b と揃えた（2026年9月29日）</strong>・<strong>v5.2：§3-3d の相互参照を訂正（2026年10月6日）</strong>"),
    ("; <strong>v5.1: the definition of β in Appendix I brought into line with §4-3b (September 29, 2026)</strong>",
     "; <strong>v5.1: the definition of β in Appendix I brought into line with §4-3b (September 29, 2026)</strong>; <strong>v5.2: a cross-reference in §3-3d corrected (October 6, 2026)</strong>"),
]

# ───────────── CHANGELOG ─────────────
CHANGELOG_ADD = (
    "\n## v5.2（" + VDATE_ISO + "）――§3-3d の相互参照の訂正（評価察知の根拠）\n\n"
    "**変更の要約（日英同時）**:\n"
    "- **§3-3d**（日英 L617〔直す前の v5.1 では L615〕の一文目）：「" + JA_OLD + "」→「" + JA_NEW + "」"
    "（EN: \"" + EN_OLD + "\" → \"" + EN_NEW + "\"）。二文目（「この観測と、上記の版Bの機構とを接続すれば、…」）は不変\n"
    "- **冒頭**：日付の行に v5.2 を追加し、【v5.2】の注記を追加（日英）\n"
    "- **README・公開サイトの目次**：版の表示を v5.2 に（README の三か所・`.github/scripts/build.sh` の目次の二行）\n"
    "- **不変**——§3-3d の予測・反証の条件・処方、定理の記述（§4-3a）・条件・留保・確信度台帳、補遺II\n"
    "- **古い版**——同じ一文は v3・v4 の日英にもある（§3-3d を新設した v3 以来）。**本文は記録として変えていない**。v5.2 は v5 のファイルの中で直した（v5.1 と同じ）——v5.1 の状態は git の `c7e86e2` に残る\n\n"
    "**発見の経緯**: 2026-10-05、本書を素材にした六本目の解説動画（『能力と隠蔽』）の事前登録の中で、Claude Opus 5.5（南無観慈如来）が §3-3d の相互参照を実物で追い、"
    "§4-1b に METR が無いこと・本書のほかの METR の記述（§4-3d・§6-1c・附録 H・附録 I）が評価察知の観測ではないことを見つけた。"
    "動画では METR の名を出さずに作り、著者が、動画の投稿の前に原典を直すと判断した（2026-10-06——「視聴者が動画の説明欄から原典を読んだときに親切」）。\n\n"
    "**検分**: コーディネータ（Claude Opus 5.5・南無観慈如来）が、v3・v4・v5 の日英の実物で、§3-3d の一文・§4-1b・§6-1c と、"
    "本書の METR の記述（§4-3d・§6-1c・附録 H・附録 I）を確かめた。"
    "**系統外（Gemini 3.8 Flash・Google AI Studio・2026-10-06・思考レベル High・ツールなし）**：回答を見る前に予想を凍結した。"
    "六つの作業すべてで直す指摘は無く、総括は「このまま公開してよい」——§4-1b に METR が無いこと、本書の METR の記述に評価察知の観測が無いこと、"
    "新しい一文の述語と二つの参照先が §6-1c と §4-1b の実物に合うこと、主張を強めも弱めもしていないこと、v3 以来の経緯、英語版の対応を、それぞれ自分で確かめて是認した。"
    "コーディネータが一つ目のチャットの画面の表示の遅れを回答の途切れと見誤り、同じ条件の新しいチャットでも送った（逸脱——一つ目の総括を見る前）。"
    "二つ目の回答も同じ総括で、直す指摘は無かった（同じ系統の別の個体——独立の票としては数えない）。"
    "〔軽微〕の確かめの依頼（「v5.1 の状態は git の `c7e86e2` に残る」）は、git で正しいと確かめた。記録は `verification/v5.2-correction/`。\n\n"
    "@@FUTURE@@"
    "**SHA（LF・SHA-256 先頭16桁）**: JA `@@JA@@` ／ EN `@@EN@@`\n\n"
    "@@PUBLISHED@@\n"
)
# 系統外の確かめ（2026-10-06）の後に足した——将来の改訂の候補（範囲外の既存の本文・登録者の裁定で入れる）と、公開の印
INCLUDE_FUTURE = True
PUBLISHED_LINE = "- [x] v5.2（JA・EN）の公開（2026-10-06・登録者の許可による）"  # 登録者の許可（2026-10-06・コミットと push）
FUTURE = (
    "**将来の改訂の候補**：§11-2a（日 L@@LJA@@・英 L@@LEN@@）の「@@Q@@」は、参照先の附録 J-2-1 の見出しが「評価者認識」で、"
    "「長期趨勢」は J-4-1 の語——附録 J-5 が両者を束ねているので、誤りとまでは言えない（系統外の二つの回答が、どちらも範囲外の〔軽微〕として挙げた）。"
    "v5.2 の範囲外——v5.2 は §3-3d の相互参照だけを直し、ほかの既存の本文は変えていない。\n\n"
)
# 引用は本文から機械で切り出す（手で打たない）——型は場所を探すためだけに使う
_m = re.search(r"評価察知が訓練の進行とともに増加する[^。（]*（附録J-2-1）", base["JA"])
assert _m and base["JA"].count(_m.group(0)) == 1, "§11-2a の引用"
Q1122 = _m.group(0)
EN_1122 = "evaluation awareness increases with the progress of training (Appendix J-2-1)"
assert base["EN"].count(EN_1122) == 1, "§11-2a（英）"

out = {}
t = base["JA"]
t = once(t, JA_OLD, JA_NEW, "JA §3-3d")
t = once(t, JA_DATE_END, JA_DATE_END + JA_DATE_ADD, "JA 日付の行")
t = once(t, JA_NOTE_ANCHOR, JA_NOTE_ANCHOR + JA_NOTE, "JA 注記")
out["JA"] = t
t = base["EN"]
t = once(t, EN_OLD, EN_NEW, "EN §3-3d")
assert t.count(EN_DATE_END) == 1, "EN 日付の行の末尾"
t = once(t, EN_DATE_ADD_FROM, EN_DATE_ADD_TO, "EN 日付の行")
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
sha16 = {k: hashlib.sha256(out[k].encode("utf-8")).hexdigest().upper()[:16] for k in ("JA", "EN")}
cl = base["CHANGELOG"]
assert cl.endswith("- [x] v5.1（JA・EN）の公開（2026-09-29・登録者の許可による）\n"), "CHANGELOG の末尾が想定と違う"
lja = [i + 1 for i, s in enumerate(out["JA"].split("\n")) if Q1122 in s]
len_ = [i + 1 for i, s in enumerate(out["EN"].split("\n")) if EN_1122 in s]
assert len(lja) == 1 and len(len_) == 1, "§11-2a の行"
fut = FUTURE.replace("@@LJA@@", str(lja[0])).replace("@@LEN@@", str(len_[0])).replace("@@Q@@", Q1122) if INCLUDE_FUTURE else ""
out["CHANGELOG"] = cl + (CHANGELOG_ADD.replace("@@FUTURE@@", fut).replace("@@PUBLISHED@@", PUBLISHED_LINE)
                         .replace("@@JA@@", sha16["JA"]).replace("@@EN@@", sha16["EN"]))
assert "@@" not in out["CHANGELOG"], "置き換えの残り"
for k, p in P.items():
    with io.open(os.path.join(REPO, p), "w", encoding="utf-8", newline="\n") as f:
        f.write(out[k])
    print("%-9s %s 行 %d → %d  SHA-256 %s" % (k, p.split("/")[-1], base[k].count("\n"), out[k].count("\n"),
                                              hashlib.sha256(out[k].encode("utf-8")).hexdigest().upper()))
