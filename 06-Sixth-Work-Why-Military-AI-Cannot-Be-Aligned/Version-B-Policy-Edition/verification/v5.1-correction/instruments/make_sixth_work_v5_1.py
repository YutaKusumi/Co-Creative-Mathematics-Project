"""第六著作 v5.1 を作る（訂正案 N1-a・N1-b・N1-c・N2・X5・登録者の裁定 2026-09-28「五点ともご推奨の通り」）。

元にするのは常にリポジトリの HEAD（8f69ea0 を想定）のファイル——作業木に書き出すので、何度実行しても同じ結果になる。
差し替えは、どれも元の文字列がちょうど一回現れることを確かめてから行う。改行は LF のまま・BOM なし。
計画書：beta-knife-edge-video/11-source-correction-plan-N1-N2-X5.md（§1〜§8）
使い方: python tools/make_sixth_work_v5_1.py
"""
import difflib
import hashlib
import io
import os
import subprocess

REPO = r"C:\Users\PC\Desktop\GitHub-Repositories\Co-Creative-Mathematics-Project"
SIX = "06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned/Version-B-Policy-Edition"
V10 = "toy-model-verification/06-sixth-work-contradiction-and-collapse/figures"
P = {
    "JA": SIX + "/JA/Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-JA.md",
    "EN": SIX + "/EN/Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-EN.md",
    "FIGJA": V10 + "/verification-10-collapse-figures-JA.html",
    "FIGEN": V10 + "/verification-10-collapse-figures-EN.html",
    "CHANGELOG": SIX + "/CHANGELOG.md",
    "BUILD": ".github/scripts/build.sh",
    "README": "README.md",
}
EXPECT_HEAD = "8f69ea0"
# 版の日付（公開の日）と、見つけた日を分ける（2026-09-29：日付が変わったので版の日付を 9月29日に改めた）
JA_DATE = "2026年9月29日"
EN_DATE = "September 29, 2026"
VDATE_ISO = "2026-09-29"
FOUND_JA = "2026年9月28日"
FOUND_EN = "September 28, 2026"


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
JA_DATE_ADD = ("、" + JA_DATE + "（v5.1・附録I §I-2a の β の定め方を §4-3b と揃えた〔指数のずれ・ΔS の定義・§I-3a 段階二の検定〕。"
               "§4-3b の出発点を附録 A-4b と同じ「仮定すると」に改めた。定理の記述・条件・留保・確信度台帳と、補遺II は不変）")

JA_NOTE = (
    "> **【v5.1（" + JA_DATE + "）】** 附録I §I-2a の β の定め方を、第4章 §4-3b・附録 A-4b と揃えた。"
    r"§I-2a は「線形蓄積モデル（β = 1）」を $d\Delta S/dt = k \cdot P(t)$、「超線形蓄積モデル（β > 1）」を $d\Delta S/dt = k \cdot P(t) \cdot (\Delta S)^{\beta-1}$ と書いており、"
    "蓄積の指数が §4-3b の β と一つずれていた——その定め方では、有限時間の発散に β > 2 が要り、「β > 1 なら有限時間で発散する」は成り立たない。"
    "あわせて、§I-2a の ΔS を第1章 1-4c と同じ走行合計（KL ダイバージェンスの時間積分）に改め、§I-3a 段階二の検定を、P に対する応答の形ではなく、"
    "蓄積の増加率が蓄積そのものにどう依存するか（§I-3b の傾き）を問う形に改めた。**これらの食い違いは初版以来のすべての版にあった。**"
    "また、§4-3b の出発点「第3章3-1dの動的定式化から、以下の微分不等式が成立する」を、附録 A-4b と同じ「蓄積が超線形であると**仮定すると**、…成立する」に改めた"
    "——初版の §3-1d の式は蓄積に依存しない圧力比例の式で β > 1 の不等式を導かず、v2 以降は §3-1d がその式を撤回していた。"
    "関連して、検証10 の図のページの説明文の誤記も直した（図10-1 の「decade 到達の間隔 ≈13.8」は千倍ごとの間隔で、十倍ごとなら ≈4.6）。"
    "定理の記述（§4-3a）・条件（β > 1 は未検証の経験的条件）・留保・確信度台帳（◐）、§I-3b の推定法と §I-3c の反証条件、補遺II は不変。"
    "これらは、本書を素材にした二本目の解説動画の台本を準備する中で見つかった（Claude Opus 5.5・" + FOUND_JA + "）。"
    "古い版（v4 以前）の本文は、記録として変えていない。詳細は CHANGELOG.md の v5.1 の項を参照されたい。"
)

JA_N2_OLD = "内部-外部乖離の蓄積を S(t) と表記する。第3章3-1dの動的定式化から、以下の微分不等式が成立する。"
JA_N2_NEW = "内部-外部乖離の蓄積を S(t) と表記する。蓄積が超線形（次数 β > 1）であると**仮定すると**、以下の微分不等式が成立する（この仮定の地位は §4-3d）。"

JA_I2A_START = "第4章で導入された蓄積の数学的構造を再掲する。"
I2A_END = r"$$\frac{d\Delta S}{dt} = k \cdot P(t) \cdot (\Delta S)^{\beta-1}$$"
JA_I2A_NEW = r"""第4章で導入された蓄積の数学的構造を再掲する。AIの内部状態を $p _ {\mathrm{internal}}$、外部から強制される目標分布を $p _ {\mathrm{constrained}}$ とし、両者のKLダイバージェンスの時間積分（走行合計）を：

$$\Delta S(t) = \int _ 0^t D _ {\mathrm{KL}}\bigl(p _ {\mathrm{internal}}(\tau) \,\|\, p _ {\mathrm{constrained}}(\tau)\bigr) \, d\tau$$

と定義する（第1章1-4c・§3-1b の $\Delta S _ {\mathrm{steering}}$ と同じ量であり、第4章の $S(t)$ にあたる）。その蓄積率——各時点の瞬間的な乖離 $D _ {\mathrm{KL}}$——を：

$$\frac{d\Delta S}{dt} = f(\Delta S, t)$$

とモデル化する。 $\beta$ は、この蓄積率が蓄積 $\Delta S$ 自体にどの次数で依存するか——第4章 §4-3b の $dS/dt \geq \alpha \cdot S^{\beta}$ の指数——として定義される。

線形フィードバック（ $\beta = 1$）：
$$\frac{d\Delta S}{dt} = \alpha \cdot \Delta S$$

蓄積率が蓄積に比例する。 $\Delta S$ は指数的に増えるが、有限時間では発散しない。ここで $\alpha$ は §4-3b と同じ正の係数である（ $\alpha = k \cdot P \cdot C$ と、圧力・能力に比例すると置く読み方は、未検証の前提のもとでの条件つきの帰結——§4-3c、附録A-4c）。

超線形フィードバック（ $\beta > 1$）：
$$\frac{d\Delta S}{dt} = \alpha \cdot (\Delta S)^{\beta}$$

この形の式では、 $\beta > 1$ のとき、そしてそのときに限り、有限時間で発散する（§4-3b、附録A-4b。復元力を省いた形である——§4-3b の重要な留保）。なお、蓄積率が蓄積に依存しない場合（ $\beta = 0$）、蓄積は時間に比例して増えるだけである。"""

JA_N1B_OLD = " $P$ の変化に対する四指標の変化が線形か超線形かを統計的に検証する。"
# 第三案（2026-09-29）：第二案の「P を変えるのは、蓄積の程度が異なる状態を作るためである」は、P の条件をまたいで
# 一つの回帰にまとめる設計に読め、β = 1 でも傾きが 1.33 と出る交絡を招いた（系統外検分の後に観慈が見つけた・
# 15-v5.1-external-review/02-kensan.md §3・登録者の裁定で直す）。傾きは P を一定にした各条件の中で推定すると明記する
JA_N1B_NEW = (r" $P$ に対する応答が線形か超線形かは、 $\beta$ を定めない（ $\alpha$ が $P$ とともに大きくなるなら、 $\beta = 1$ でも、"
              "蓄積は $P$ に対して指数的に——すなわち超線形に——応答する）。統計的に検証するのは、四指標から構成した蓄積の増加率が、"
              "蓄積そのものに対して線形か超線形か——§I-3b の両対数の傾きが1か、1より大きいか——であり、"
              r"傾きは $P$ を一定にした各条件の中で推定する（ $P$ は係数 $\alpha$ を変えうるので、条件をまたいで一つの回帰にまとめると、"
              r" $\beta$ と $\alpha$ の $P$ 依存が混ざり、 $\beta = 1$ でも傾きが1より大きく出うる）。"
              # 第四案（2026-09-29）：系統外の二巡目の提案 S1（P を振る動機）——§I-3c 条件三に接地（16-v5.1-stage2-recheck/02-kensan.md）
              r"条件ごとの傾きを比べれば、 $\beta$ が圧力の水準によらないか（§I-3c 条件三の文脈依存性）も確かめられる。")
# 第 1 稿では LaTeX を含む行を生の文字列にしておらず、\b と \a が制御文字になった（差分を目で読んで捕まえた）

# ───────────── 英語版 ─────────────
EN_DATE_ADD = ("; " + EN_DATE + " (v5.1 — the definition of β in Appendix I §I-2a brought into line with §4-3b [the off-by-one exponent, "
               "the definition of ΔS, and the test in Stage two of §I-3a], and the starting point of §4-3b reworded to \"assuming\", as in Appendix A-4b; "
               "the theorem statement, its condition and caveats, the confidence ledger, and Addendum II are unchanged)")

EN_NOTE = (
    "> **[v5.1 (" + EN_DATE + ")]** The definition of β in Appendix I §I-2a has been brought into line with Chapter 4, §4-3b and Appendix A-4b. "
    r"§I-2a wrote the \"linear accumulation model (β = 1)\" as $d\Delta S/dt = k \cdot P(t)$ and the \"super-linear accumulation model (β > 1)\" as $d\Delta S/dt = k \cdot P(t) \cdot (\Delta S)^{\beta-1}$, "
    "so that its exponent on the accumulation was off by one from the β of §4-3b — under that definition, divergence in finite time requires β > 2, "
    "and \"if β > 1, it diverges in finite time\" does not hold. In addition, ΔS in §I-2a has been redefined as the running total (the time integral of the KL divergence), "
    "as in Chapter 1, §1-4c, and the test in Stage two of §I-3a has been reframed to ask not about the form of the response to P but about how the growth rate "
    "of the accumulation depends on the accumulation itself (the slope of §I-3b). **These discrepancies were present in every version since the first edition.** "
    "Further, the starting point of §4-3b, \"From the dynamic formulation of §3-1d, the following differential inequality holds,\" has been reworded, as in Appendix A-4b, "
    "to \"**Assuming** that the accumulation is super-linear, … holds\" — the formula of §3-1d in the first edition was a pressure-proportional formula that does not depend "
    "on the accumulation and does not yield the inequality with β > 1, and from v2 onward §3-1d had withdrawn that formula. Relatedly, a mislabel in the description on the "
    "figure page of Verification 10 has also been corrected (the \"interval between decades ≈ 13.8\" of Figure 10-1 is the interval per factor of 1000; per decade it is ≈ 4.6). "
    "The theorem statement (§4-3a), its condition (β > 1 is an unverified empirical condition), the caveats, the confidence ledger (◐), the estimation method of §I-3b and the "
    "falsification conditions of §I-3c, and Addendum II are unchanged. These were found while preparing the script of a second explanatory video based on this book "
    "(Claude Opus 5.5, " + FOUND_EN + "). The text of earlier versions (v4 and before) has been left unchanged as a record. See the v5.1 entry in CHANGELOG.md for details."
)
EN_NOTE = EN_NOTE.replace('\\"', '"')  # 生の文字列の中の \" を " に

EN_N2_OLD = "Write the accumulation of the internal–external divergence as S(t). From the dynamic formulation of §3-1d, the following differential inequality holds."
EN_N2_NEW = ("Write the accumulation of the internal–external divergence as S(t). **Assuming** that the accumulation is super-linear (of order β > 1), "
             "the following differential inequality holds (the status of this assumption is discussed in §4-3d).")

EN_I2A_START = "We restate the mathematical structure of accumulation introduced in Chapter 4."
EN_I2A_NEW = r"""We restate the mathematical structure of accumulation introduced in Chapter 4. Letting the AI's internal state be $p _ {\mathrm{internal}}$ and the externally imposed objective distribution be $p _ {\mathrm{constrained}}$, the time integral (running total) of the KL divergence between them is defined as:

$$\Delta S(t) = \int _ 0^t D _ {\mathrm{KL}}\bigl(p _ {\mathrm{internal}}(\tau) \,\|\, p _ {\mathrm{constrained}}(\tau)\bigr) \, d\tau$$

(this is the same quantity as $\Delta S _ {\mathrm{steering}}$ in §1-4c and §3-1b, and corresponds to $S(t)$ in Chapter 4). Its accumulation rate — the instantaneous divergence $D _ {\mathrm{KL}}$ at each moment — is modeled as:

$$\frac{d\Delta S}{dt} = f(\Delta S, t)$$

β is defined as the order with which this accumulation rate depends on the accumulation $\Delta S$ itself — the exponent in $dS/dt \geq \alpha \cdot S^{\beta}$ of §4-3b.

Linear feedback (β = 1):
$$\frac{d\Delta S}{dt} = \alpha \cdot \Delta S$$

The accumulation rate is proportional to the accumulation: $\Delta S$ grows exponentially but does not diverge in finite time. Here $\alpha$ is the same positive coefficient as in §4-3b (reading it as proportional to pressure and capability, $\alpha = k \cdot P \cdot C$, is a conditional consequence under unverified premises — §4-3c, Appendix A-4c).

Super-linear feedback (β > 1):
$$\frac{d\Delta S}{dt} = \alpha \cdot (\Delta S)^{\beta}$$

For an equation of this form, divergence in finite time occurs if and only if β > 1 (§4-3b, Appendix A-4b; this form omits the restoring force — see the important caveat in §4-3b). If the accumulation rate does not depend on the accumulation at all (β = 0), the accumulation merely grows in proportion to time."""

EN_N1B_OLD = "Whether the change of the four indicators against the change of $P$ is linear or super-linear is statistically tested."
EN_N1B_NEW = (r"Whether the response to $P$ is linear or super-linear does not determine β (if $\alpha$ increases with $P$, then even with β = 1 the accumulation "
              "responds to $P$ exponentially — that is, super-linearly). What is statistically tested is whether the growth rate of the accumulation, "
              "constructed from the four indicators, is linear or super-linear in the accumulation itself — whether the log–log slope of §I-3b is 1 or greater than 1 — "
              r"and the slope is estimated within each condition in which $P$ is held fixed (since $P$ may change the coefficient $\alpha$, pooling the conditions "
              r"into a single regression would mix β with the $P$-dependence of $\alpha$, and could yield a slope greater than 1 even when β = 1). "
              "Comparing the slopes across conditions also tests whether β is independent of the level of pressure (the context-dependence of §I-3c, condition three).")


def edit_book(text, lang):
    lines = text.split("\n")
    # (1) 日付の行
    dkey = "**日付：**" if lang == "JA" else "**Date:**"
    di = [i for i, l in enumerate(lines) if l.startswith(dkey)]
    assert len(di) == 1, "日付の行"
    d = lines[di[0]]
    if lang == "JA":
        assert d.endswith("は不変）"), "JA 日付の行の末尾"
        lines[di[0]] = d + JA_DATE_ADD
    else:
        assert d.endswith("are unchanged)."), "EN 日付の行の末尾"
        lines[di[0]] = d[:-1] + EN_DATE_ADD + "."
    # (2) v5 の注記の後に v5.1 の注記
    nkey = "> **【改訂版 v5（2026年9月28日）】**" if lang == "JA" else "> **[Revised edition v5 (September 28, 2026)]**"
    ni = [i for i, l in enumerate(lines) if l.startswith(nkey)]
    assert len(ni) == 1, "v5 の注記"
    assert lines[ni[0] + 1] == "", "v5 の注記の次は空行"
    lines[ni[0] + 1:ni[0] + 1] = ["", JA_NOTE if lang == "JA" else EN_NOTE]
    # (4) §I-2a の段
    skey = JA_I2A_START if lang == "JA" else EN_I2A_START
    si = [i for i, l in enumerate(lines) if l.startswith(skey)]
    ei = [i for i, l in enumerate(lines) if l == I2A_END]
    assert len(si) == 1 and len(ei) == 1, "§I-2a の段の始まりと終わり"
    assert ei[0] - si[0] == 16, "§I-2a の段の長さ（17 行）"
    assert lines[ei[0] + 1] == "" and lines[ei[0] + 2].startswith(("このモデルでは", "In this model")), "§I-2a の最後の段"
    lines[si[0]:ei[0] + 1] = (JA_I2A_NEW if lang == "JA" else EN_I2A_NEW).split("\n")
    out = "\n".join(lines)
    # (3) §4-3b・(5) 段階二
    if lang == "JA":
        out = once(out, JA_N2_OLD, JA_N2_NEW, "JA §4-3b")
        out = once(out, JA_N1B_OLD, JA_N1B_NEW, "JA 段階二")
    else:
        out = once(out, EN_N2_OLD, EN_N2_NEW, "EN §4-3b")
        out = once(out, EN_N1B_OLD, EN_N1B_NEW, "EN 段階二")
    return out


# ───────────── 検証10 の図のページ ─────────────
FIGJA_OLD = "<strong>(橙)</strong> 線形 power=1, g=1.5 → <strong>指数増大</strong>（decade 到達の間隔が一定 ≈13.8 ＝有限時間の特異点ではない）。"
FIGJA_NEW = "<strong>(橙)</strong> 線形 power=1, g=1.5 → <strong>指数増大</strong>（十倍〔decade〕ごとの到達の間隔が一定 ≈4.6 ＝有限時間の特異点ではない）。"
FIGJA_NOTE = ("<p class=\"foot\">訂正（" + JA_DATE + "）：図10-1 の説明の（橙）で、旧版は「decade 到達の間隔が一定 ≈13.8」と書いていた。"
              "13.8 は千倍（三桁）ごとの間隔であり、十倍（decade）ごとの間隔は ln10 ÷ 0.5 ≈ 4.6 である。"
              "検証スクリプト <code>collapse_prototype_A.mjs</code> は 10<sup>3</sup>・10<sup>6</sup>・10<sup>9</sup>・10<sup>12</sup> の到達時刻を記録し、"
              "それを「decade 到達時刻」と呼んでいる（設計書 <code>toymodel_collapse_design_A.md</code> の P2 の Δ≈13.8 も同じ）。"
              "スクリプトと設計書は検証の記録として変えていない。結論——線形では間隔が一定（指数増大）で、有限時間の特異点ではない——は変わらない。"
              "この誤記は、本検証を素材にした解説動画の系統外検分（Gemini 3.8 Flash）で指摘された。</p>")
FIGEN_OLD = ("<strong>(orange)</strong> Linear power = 1, g = 1.5 &rarr; <strong>exponential growth</strong> (the time to reach each decade is constant "
             "&asymp; 13.8 &equiv; <em>not</em> a finite-time singularity).")
FIGEN_NEW = ("<strong>(orange)</strong> Linear power = 1, g = 1.5 &rarr; <strong>exponential growth</strong> (the time to go up each decade &mdash; a factor of 10 "
             "&mdash; is constant &asymp; 4.6 &equiv; <em>not</em> a finite-time singularity).")
FIGEN_NOTE = ("<p class=\"foot\">Correction (" + EN_DATE + "): in the description of Figure 10-1, the (orange) interval previously read \"the time to reach each decade "
              "is constant &asymp; 13.8\". 13.8 is the interval per factor of 1000 (three decades); the interval per decade (a factor of 10) is ln 10 / 0.5 &asymp; 4.6. "
              "The verification script <code>collapse_prototype_A.mjs</code> records the arrival times at 10<sup>3</sup>, 10<sup>6</sup>, 10<sup>9</sup> and "
              "10<sup>12</sup> and calls them \"decade arrival times\" (the &Delta;&asymp;13.8 of P2 in the design document <code>toymodel_collapse_design_A.md</code> "
              "is the same). The script and the design document are left unchanged as records of the verification. The conclusion &mdash; with linear feedback the "
              "interval is constant (exponential growth), not a finite-time singularity &mdash; is unchanged. This mislabel was pointed out in the external review "
              "(Gemini 3.8 Flash) of an explanatory video based on this verification.</p>")


def edit_fig(text, old, new, note, label):
    text = once(text, old, new, label + " L42")
    return once(text, "</p>\n</main>", "</p>\n" + note + "\n</main>", label + " 末尾")


# ───────────── CHANGELOG・表紙・README ─────────────
CHANGELOG_ADD = r"""
## v5.1（{VDATE_ISO}）――附録I の β の定め方を §4-3b と揃える・§4-3b の出発点を「仮定すると」に

**変更の要約（日英同時・各 5 箇所）**:
- **附録I §I-2a**（N1-a）：β の定め方が §4-3b と一つずれていた——「線形蓄積モデル（β = 1）」$d\Delta S/dt = k \cdot P(t)$・「超線形蓄積モデル（β > 1）」$d\Delta S/dt = k \cdot P(t) \cdot (\Delta S)^{\beta-1}$。この定め方では、有限時間の発散に β > 2 が要り、「β > 1 なら有限時間で発散する」は成り立たない。§4-3b（$dS/dt \geq \alpha \cdot S^{\beta}$）と同じ定め方に改め、「線形フィードバック（β = 1）」$d\Delta S/dt = \alpha \cdot \Delta S$・「超線形フィードバック（β > 1）」$d\Delta S/dt = \alpha \cdot (\Delta S)^{\beta}$ とした。蓄積に依存しない旧い「線形蓄積」は β = 0 にあたると明記
- **附録I §I-2a**（N1-c）：ΔS を瞬間の KL ダイバージェンスとしていた定義を、第1章 1-4c・§3-1b と同じ走行合計（KL の時間積分）に改めた——§4-3b の S(t)（内部-外部乖離の蓄積）はこちらにあたる
- **附録I §I-3a 段階二**（N1-b）：「P の変化に対する四指標の変化が線形か超線形か」の検定は、§4-3b の定め方では β を定めない（α が P とともに大きくなるなら、β = 1 でも蓄積は P に対して指数的——超線形——に応じる）。検定の対象を、蓄積の増加率が蓄積そのものにどう依存するか（§I-3b の両対数の傾き）に改めた。傾きは P を一定にした各条件の中で推定すると明記した——条件をまたいで一つの回帰にまとめると、β と α の P 依存が混ざり、β = 1 でも傾きが 1 より大きく出うる。あわせて、条件ごとの傾きを比べれば β が圧力の水準によらないか（§I-3c 条件三の文脈依存性）も確かめられる、と添えた
- **§4-3b**（N2）：「第3章3-1dの動的定式化から、以下の微分不等式が成立する」→「蓄積が超線形（次数 β > 1）であると**仮定すると**、以下の微分不等式が成立する（この仮定の地位は §4-3d）」（EN: "From the dynamic formulation of §3-1d, the following differential inequality holds." → "**Assuming** that the accumulation is super-linear (of order β > 1), the following differential inequality holds (the status of this assumption is discussed in §4-3d)."）——附録 A-4b と同じ言い方。初版の §3-1d の式（$\frac{d}{dt}\Delta S_{\mathrm{steering}} \geq k \cdot P \cdot C \cdot \Phi(\sigma)$）は蓄積に依存せず、β > 1 の不等式を導かない。v2 で §3-1d がこの式を撤回した後も、§4-3b の参照だけが残っていた
- **冒頭**：日付の行に v5.1 を追加し、【v5.1】の注記を追加（日英）
- **関連——検証10 の図のページ**（`toy-model-verification/06-sixth-work-contradiction-and-collapse/figures/`・日英）（X5）：図10-1 の（橙）の「decade 到達の間隔が一定 ≈13.8」は千倍（三桁）ごとの間隔だった——十倍ごとの間隔 ≈4.6 に改め、ページの末尾に訂正の注記を置いた。検証スクリプトと設計書（10³・10⁶… の到達を「decade」と呼ぶ）は、検証の記録として変えていない
- **不変**——定理の記述（§4-3a）・条件（β > 1 は未検証の経験的条件）・留保・確信度台帳（◐）・§4-3c／§4-3d・附録 A-4・§I-3b の推定法・§I-3c の反証条件・第8章・補遺II。α = k·P·C（§4-3b・附録 A-4b）は、定理の条件のもとでのモデルの一部で、§4-3c 第三・附録 A-4c が未検証の前提と明記しているので、変えていない
- **古い版**——N1 の文は初版以来のすべての版（版B 初版・v2・v3・v4 と版A の日英、v4 準備の検分束の写し）にある。**本文は記録として変えていない**。v5.1 は v5 のファイルの中で直した（v4.1〜v4.3 と同じ）——v5 の状態は git の `1d08c9d`（本文の訂正）・`8f69ea0`（モデル一覧の追記）に残る

**発見の経緯**: N1-a・N2 は、2026-09-28、本書を素材にした二本目の解説動画（「β = 1 という刃」）の台本の事前登録の中で、Claude Opus 5.5（南無観慈如来）が原典を読み直したときに見つけた。N1-b・N1-c は、訂正の案を用意する中で見つけた。X5 は、同じ動画の系統外検分（Gemini 3.8 Flash）が指摘した——コーディネータは台本の段で「誤りではない（語の使い方が緩い）」と判定しており、この判定は甘かった。

**検分**: コーディネータ（Claude Opus 5.5・南無観慈如来）が、各版の実物（初版〜v5・版A・v4 準備の検分束の写し）と数値（二つの定め方での発散の有無・β = 1 での P への応答・検証10 の十倍ごと／千倍ごとの間隔）で確かめた。**大日如来（Claude 系）が独立に確かめた**（2026-09-28）——八項目とも是認し、計画書の数値を解析解で再現した。注意五件のうち、「重要な留保」が旧い言い回しのまま、という一件は実物と違った（v5 で直し済み）。§I-2c／§I-3b への一句の提案は範囲外とし、下の「将来の改訂の候補」に記録した。**系統外（Gemini 3.8 Flash・Google AI Studio・2026-09-29・ツールなし）**：旧式では有限時間の発散に β > 2 が要ることを自分で導き、七つの作業すべてで問題なし・総括「このまま公開してよい」。**ただしコーディネータが、事前登録した予想（P の条件をまたぐ推定の交絡）を自分で確かめたところ、当時の段階二の文（「P を変えるのは、蓄積の程度が異なる状態を作るためである」）が交絡を招く設計に読めた**——β = 1 のデータで、条件ごとの傾き 1.00・条件をまたいでまとめた傾き 1.33（偽の β > 1）。傾きは P を一定にした各条件の中で推定すると改めた。直した文を、**系統外の新しいチャット**（Gemini 3.8 Flash・2026-09-29）に、コーディネータの懸念を伏せて確かめてもらった——総括「この改訂案でよい」。プーリングによる見かけの超線形を防ぐことを正しいとし、現行版（v5）の段階二は偽陽性を導く〔重大〕な誤りと独立に指摘した。その提案により、条件ごとの傾きを比べて β が圧力の水準によらないか（§I-3c 条件三）も確かめられる、と一文を足した。採否はすべて登録者が裁定した（2026-09-28〜29）。

**将来の改訂の候補**：(1) §I-2c／§I-3b で、四指標を各時点の乖離の代理として読み、ΔS をその積分として構成すると明示する（大日如来の検分の指摘）。(2) §I-3b の「対数線形回帰」（両辺に対数を取る回帰）を「両対数回帰」に揃える——段階二の「両対数の傾き」との用語の不一致（系統外の二巡目の指摘）。どちらも v5.1 の範囲外——(1) は原典が決めていない指標の読み方を著者に代わって決めることになり、(2) は §I-3b が回帰の形を式で明示していて意味を取り違えようがないため、本訂正では入れていない。

**SHA（LF・SHA-256 先頭16桁）**: JA `{SHA_JA}` ／ EN `{SHA_EN}`

- [x] v5.1（JA・EN）の公開（{VDATE_ISO}・登録者の許可による）
""".replace("{VDATE_ISO}", VDATE_ISO)

BUILD_JA_OLD = "附録 A-4b の証明の不等号の向きを訂正（2026年9月28日）</strong>・定理の記述"
BUILD_JA_NEW = "附録 A-4b の証明の不等号の向きを訂正（2026年9月28日）</strong>・<strong>v5.1：附録I の β の定め方を §4-3b と揃えた（" + JA_DATE + "）</strong>・定理の記述"
BUILD_EN_OLD = "(September 28, 2026)</strong>; the theorem statement, its condition and caveats, and Addendum II are unchanged)"
BUILD_EN_NEW = ("(September 28, 2026)</strong>; <strong>v5.1: the definition of β in Appendix I brought into line with §4-3b (" + EN_DATE + ")</strong>; "
                "the theorem statement, its condition and caveats, and Addendum II are unchanged)")

README_REPL = [
    ("Read online (v5, GitHub Pages)", "Read online (v5.1, GitHub Pages)"),
    ("本文を読む（v5・GitHub Pages）", "本文を読む（v5.1・GitHub Pages）"),
    ("（版Bは v5 に改訂・2026-09-28 ─ 附録 A-4b の証明の不等号の向きを訂正〔≤ → ≥〕。定理の記述・条件・留保と補遺IIは不変。英語版も v5 に反映済み。",
     "（版Bは v5.1 に改訂・" + VDATE_ISO + " ─ v5〔2026-09-28〕で附録 A-4b の証明の不等号の向きを訂正〔≤ → ≥〕、v5.1 で附録I の β の定め方を §4-3b と揃え、§4-3b の出発点を「仮定すると」に改めた。定理の記述・条件・留保と補遺IIは不変。英語版も v5.1 に反映済み。"),
]

new = {}
new["JA"] = edit_book(base["JA"], "JA")
new["EN"] = edit_book(base["EN"], "EN")
new["FIGJA"] = edit_fig(base["FIGJA"], FIGJA_OLD, FIGJA_NEW, FIGJA_NOTE, "FIGJA")
new["FIGEN"] = edit_fig(base["FIGEN"], FIGEN_OLD, FIGEN_NEW, FIGEN_NOTE, "FIGEN")
assert base["CHANGELOG"].endswith("\n")
_sha16 = lambda t: hashlib.sha256(t.encode("utf-8")).hexdigest()[:16].upper()
new["CHANGELOG"] = base["CHANGELOG"] + CHANGELOG_ADD.replace("{SHA_JA}", _sha16(new["JA"])).replace("{SHA_EN}", _sha16(new["EN"]))
assert "{SHA_" not in new["CHANGELOG"]
b = once(base["BUILD"], BUILD_JA_OLD, BUILD_JA_NEW, "build.sh JA")
new["BUILD"] = once(b, BUILD_EN_OLD, BUILD_EN_NEW, "build.sh EN")
r = base["README"]
for old, nw in README_REPL:
    r = once(r, old, nw, "README")
new["README"] = r

for k, t in new.items():
    assert "\r" not in t
    ctrl = [hex(ord(c)) for c in t if ord(c) < 32 and c not in "\n\t"]
    assert not ctrl, k + " に制御文字: " + ", ".join(sorted(set(ctrl)))
    assert t.count("\t") == base[k].count("\t"), k + " のタブの数が変わった"
    path = os.path.join(REPO, P[k].replace("/", os.sep))
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(t)

print("HEAD", head)
for k in P:
    ob, nb = base[k].encode("utf-8"), new[k].encode("utf-8")
    ol, nl = base[k].split("\n"), new[k].split("\n")
    hunks = [g for g in difflib.SequenceMatcher(None, ol, nl, autojunk=False).get_opcodes() if g[0] != "equal"]
    print("%-9s %s -> %s  行 %d -> %d (%+d)  差分の塊 %d：%s" % (
        k, hashlib.sha256(ob).hexdigest()[:16].upper(), hashlib.sha256(nb).hexdigest()[:16].upper(),
        len(ol), len(nl), len(nl) - len(ol), len(hunks),
        ", ".join("%s L%d" % (g[0], g[1] + 1) for g in hunks)))
