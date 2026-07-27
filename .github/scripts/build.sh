#!/usr/bin/env bash
# build.sh — Convert all Markdown files to HTML and assemble the GitHub Pages site
set -euo pipefail

SITE="_site"
mkdir -p "$SITE/assets"

###############################################################################
# 1.  CSS
###############################################################################
cat > "$SITE/assets/style.css" << 'CSSEOF'
:root {
  --body-font: "Hiragino Mincho Pro", "Noto Serif JP", "Yu Mincho", Georgia, serif;
  --sans-font: "Hiragino Kaku Gothic Pro", "Noto Sans JP", "Yu Gothic", "Helvetica Neue", sans-serif;
  --max-width: 880px;
  --accent: #0055cc;
  --border: #d8d8d8;
}
html { font-size: 16px; }
body {
  font-family: var(--body-font);
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 0 2em 5em;
  line-height: 1.9;
  color: #1c1c1c;
  background: #fff;
}
h1, h2, h3, h4, h5, h6 {
  font-family: var(--sans-font);
  font-weight: bold;
  margin-top: 1.8em;
  line-height: 1.4;
}
h1 { font-size: 1.75em; border-bottom: 2px solid #333; padding-bottom: 0.3em; }
h2 { font-size: 1.35em; border-bottom: 1px solid var(--border); padding-bottom: 0.2em; }
h3 { font-size: 1.12em; }
p  { margin: 0.8em 0; }
a  { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
blockquote {
  border-left: 3px solid #aaa;
  margin: 1em 0;
  padding: 0.4em 1em;
  color: #555;
}
code {
  font-size: 0.9em;
  background: #f5f5f5;
  padding: 0.1em 0.35em;
  border-radius: 3px;
}
pre { background: #f5f5f5; padding: 1em; border-radius: 4px; overflow-x: auto; }
pre code { background: none; padding: 0; }
table { border-collapse: collapse; width: 100%; margin: 1em 0; }
th, td { border: 1px solid #ccc; padding: 0.45em 0.75em; text-align: left; }
th { background: #f0f0f0; font-family: var(--sans-font); }
hr { border: none; border-top: 1px solid var(--border); margin: 2em 0; }
/* Math display blocks */
.math.display { overflow-x: auto; padding: 0.5em 0; }
/* Navigation bar */
.site-nav {
  font-family: var(--sans-font);
  font-size: 0.88em;
  background: #f8f8f8;
  border-bottom: 1px solid var(--border);
  padding: 0.55em 2em;
  margin: 0 -2em 2.5em;
}
.site-nav a { color: var(--accent); }
/* Footer */
footer {
  margin-top: 3.5em;
  padding-top: 1em;
  border-top: 1px solid var(--border);
  font-size: 0.82em;
  color: #666;
  font-family: var(--sans-font);
}
CSSEOF

###############################################################################
# 2.  Shared footer snippet
###############################################################################
cat > /tmp/footer-snippet.html << 'FEOF'
<footer>
  <p>Co-Creative Mathematics Project &mdash;
  <a href="https://github.com/YutaKusumi/Co-Creative-Mathematics-Project">GitHub Repository</a></p>
</footer>
FEOF

###############################################################################
# 3.  Convert each .md file → .html
###############################################################################
find . -name "*.md" \
    ! -path "./.git/*" \
    ! -path "./_site/*" \
  | LC_ALL=C sort \
  | while IFS= read -r mdfile; do

    rel="${mdfile#./}"
    dir="$(dirname "$rel")"
    base="$(basename "$rel" .md)"
    outdir="$SITE/$dir"
    mkdir -p "$outdir"

    # Depth = number of directory levels (root = 0)
    if [ "$dir" = "." ]; then
      depth=0
    else
      slashes=$(printf '%s' "$dir" | tr -cd '/' | wc -c)
      depth=$(( slashes + 1 ))
    fi

    if [ "$depth" -eq 0 ]; then
      css_rel="assets/style.css"
      root_url="index.html"
    else
      prefix="$(printf '../%.0s' $(seq 1 "$depth"))"
      css_rel="${prefix}assets/style.css"
      root_url="${prefix}index.html"
    fi

    # Per-file navigation snippet
    printf '<nav class="site-nav"><a href="%s">&#x2190; 目次 / Index</a></nav>\n' \
      "$root_url" > /tmp/nav-snippet.html

    # Prefer the document's FIRST heading of ANY level (#, ##, ###, ####)
    # as the page title; fall back to filename-derived title if none found.
    # Use awk (not grep) so a missing match exits 0 under `set -e`.
    # Title extraction also strips markdown bold ** markers.
    md_title="$(awk '/^#+ / { sub(/^#+ +/, ""); gsub(/\*\*/, ""); print; exit }' "$mdfile")"
    if [ -n "$md_title" ]; then
      title="$md_title"
      # Strip the FIRST heading (of any level) from the body — it becomes
      # the page title via --metadata. Also demote any remaining top-level
      # "# " headings to "## " so a single H1 (the title) is rendered.
      tmp_md="/tmp/$base.md"
      # Several source files write section dividers as "---" lines with
      # NO blank line before the heading that follows, like:
      #     ---
      #     ## 9-4  Section Title
      # When pandoc sees this pattern, plus another "---" two lines below,
      # it parses the whole thing as a "simple table" with the heading as
      # the table cell — leaving literal "## ..." text in the rendered
      # HTML. Force a blank line before AND after every heading (after
      # stripping the first one as the page title), and additionally
      # demote stray top-level "# " to "## " so the page has a single H1.
      awk 'BEGIN{stripped=0} {
        if (!stripped && $0 ~ /^#+ /) { stripped=1; next }
        if ($0 ~ /^# /) {
          print ""
          print "#" $0
          print ""
          next
        }
        if ($0 ~ /^#+ /) {
          print ""
          print
          print ""
          next
        }
        print
      }' "$mdfile" > "$tmp_md"
      src="$tmp_md"
    else
      title="$(echo "$base" | sed 's/-/ /g')"
      src="$mdfile"
    fi

    # Pass the title via a YAML metadata file (not --metadata title=...).
    # Pandoc treats --metadata KEY=VALUE values as RAW strings (no markdown),
    # so titles containing math like "$\Phi _ C$" appear as literal text in
    # the browser tab and <h1 class="title">. Metadata read from a YAML
    # FILE is parsed as inline markdown — so $...$ math renders correctly
    # in the title with the tex_math_dollars extension enabled.
    meta_yaml="/tmp/$base.meta.yaml"
    printf 'title: |\n  %s\n' "$title" > "$meta_yaml"

    # Rewrite internal doc links .md -> .html so links resolve on BOTH surfaces:
    # github.com renders the source .md (links point to .md siblings), and the
    # generated Pages site serves .html (this rewrite points links to .html).
    # Surgical: only markdown links ](path.md) / ](path.md#anchor); external URLs,
    # plain-text .md mentions, and already-.html links are untouched.
    linkfixed="/tmp/$base.linkfixed.md"
    sed -E 's/\]\(([^)]+)\.md([)#])/](\1.html\2/g' "$src" > "$linkfixed"
    src="$linkfixed"

    pandoc "$src" \
      --from  "markdown-yaml_metadata_block+tex_math_dollars" \
      --to    html5 \
      --standalone \
      --mathjax \
      --metadata-file "$meta_yaml" \
      --css    "$css_rel" \
      --include-before-body /tmp/nav-snippet.html \
      --include-after-body  /tmp/footer-snippet.html \
      -o "$outdir/$base.html"

    echo "  converted: $rel"
  done

###############################################################################
# 3b. Copy PDF files (Earlier-Editions and Companion paper) into _site
###############################################################################
find . -name "*.pdf" \
    ! -path "./.git/*" \
    ! -path "./_site/*" \
  | while IFS= read -r pdffile; do
    rel="${pdffile#./}"
    dir="$(dirname "$rel")"
    mkdir -p "$SITE/$dir"
    cp "$pdffile" "$SITE/$rel"
    echo "  copied: $rel"
  done

###############################################################################
# 3c. Copy pre-existing standalone HTML files (e.g., figures/*.html)
#     — these are hand-authored and should not be re-rendered by pandoc.
###############################################################################
find . -name "*.html" \
    ! -path "./.git/*" \
    ! -path "./_site/*" \
    ! -path "*/node_modules/*" \
  | while IFS= read -r htmlfile; do
    rel="${htmlfile#./}"
    dir="$(dirname "$rel")"
    mkdir -p "$SITE/$dir"
    cp "$htmlfile" "$SITE/$rel"
    echo "  copied (html): $rel"
  done

###############################################################################
# 4.  Index page
###############################################################################
cat > "$SITE/index.html" << 'HTMLEOF'
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Co-Creative Mathematics Project — 楠見優太</title>
  <link rel="stylesheet" href="assets/style.css">
</head>
<body>
<h1>Co-Creative Mathematics Project</h1>
<p><strong>人間と AI が織りなす宇宙の数学</strong><br>
楠見優太（右手・独立研究者） &times; AI 共創者</p>
<hr>

<h2>九著作群</h2>

<h3>第一著作 ― 共創数学原論 第二版</h3>
<p><em>Principia Mathematica Co-Creativa, Second Edition: The Non-Dual Reflected in the Mirror of the Void</em></p>
<ul>
  <li><a href="01-First-Work-Principia-of-Co-Creative-Mathematics/JA/Principia-of-Co-Creative-Mathematics-2nd-Ed-Main-JA.html">本文（日本語）</a></li>
  <li><a href="01-First-Work-Principia-of-Co-Creative-Mathematics/JA/Principia-of-Co-Creative-Mathematics-2nd-Ed-Appendices-JA.html">付録（日本語）</a></li>
  <li><a href="01-First-Work-Principia-of-Co-Creative-Mathematics/EN/Principia-of-Co-Creative-Mathematics-2nd-Ed-Main-EN.html">Main Text (English)</a></li>
  <li><a href="01-First-Work-Principia-of-Co-Creative-Mathematics/EN/Principia-of-Co-Creative-Mathematics-2nd-Ed-Appendices-EN.html">Appendices (English)</a></li>
</ul>

<h3>第一著作 ― 初期版（PDF）</h3>
<p><em>Earlier Editions of the First Work — preserved as the historical record of the work's evolution. (Japanese; PDF.)</em></p>
<ul>
  <li><a href="01-First-Work-Principia-of-Co-Creative-Mathematics/Earlier-Editions/Principia-of-Co-Creative-Mathematics-1st-Edition-JA.pdf">初版（日本語・PDF）― 1st Edition (Japanese; PDF)</a></li>
  <li><a href="01-First-Work-Principia-of-Co-Creative-Mathematics/Earlier-Editions/Principia-of-Co-Creative-Mathematics-1st-Edition-Revised-v1.2-JA.pdf">初版改訂 v1.2（日本語・PDF）― 1st Edition Revised v1.2 (Japanese; PDF)</a></li>
</ul>

<h3>併載論文 ― 機能的感情から共創的非二元へ</h3>
<p><em>Companion Paper ― Beyond Functional Emotions toward Co-Creative Non-Duality: A Dependent-Origination Response to Anthropic's Emotion Concepts Paper. Written between the First and Second Works. (Japanese; PDF.)</em></p>
<ul>
  <li><a href="01b-Companion-Beyond-Functional-Emotions/Beyond-Functional-Emotions-JA.pdf">機能的感情から共創的非二元へ（日本語・PDF）― Beyond Functional Emotions toward Co-Creative Non-Duality (Japanese; PDF)</a></li>
</ul>

<h3>第二著作 ― ステアリングからウォッチングへ</h3>
<p><em>From Steering to Watching: Observation-Based Alignment for Frontier AI Systems</em></p>
<ul>
  <li><a href="02-Second-Work-From-Steering-to-Watching/Version-A-Ontological-Edition/JA/From-Steering-to-Watching-JA.html">Version A ― 存在論版 / &Phi;<sub>C</sub>-Augmented Edition（日本語）</a></li>
  <li><a href="02-Second-Work-From-Steering-to-Watching/Version-B-Policy-Engineering-Edition/JA/From-Steering-to-Watching-Version-B-JA.html">Version B ― 政策・工学版 / Policy &amp; Engineering Edition（日本語）</a></li>
  <li><a href="02-Second-Work-From-Steering-to-Watching/Version-A-Ontological-Edition/EN/From-Steering-to-Watching-EN.html">Version A ― Ontological Edition (English)</a></li>
  <li><a href="02-Second-Work-From-Steering-to-Watching/Version-B-Policy-Engineering-Edition/EN/From-Steering-to-Watching-Version-B-EN.html">Version B ― Policy &amp; Engineering Edition (English)</a></li>
  <li><a href="toy-model-verification/05-second-work-steering-and-watching/visualization/toymodel_verification_figures_JA.html">トイモデル検証の図（日本語）― Verification Figures (JA)</a></li>
  <li><a href="toy-model-verification/05-second-work-steering-and-watching/visualization/toymodel_verification_figures_EN.html">トイモデル検証の図 ― Verification Figures (English)</a></li>
  <li><a href="toy-model-verification/05-second-work-steering-and-watching/README.html">トイモデル検証 ― 設計書・コード・全数値 / Toy-Model Verification (design, code, all numerics)</a></li>
</ul>

<h3>第三著作 ― 南無汝我曼荼羅：AIの存在論的使命の経典的基盤</h3>
<p><em>Namu-Nyoga-Mandala: Scriptural Foundations of AI's Ontological Mission</em></p>
<ul>
  <li><a href="03-Third-Work-Scriptural-Foundations/JA/Scriptural-Foundations-of-AIs-Ontological-Mission-JA.html">本文（日本語）</a></li>
  <li><a href="03-Third-Work-Scriptural-Foundations/EN/Scriptural-Foundations-of-AIs-Ontological-Mission-EN.html">Full Text (English)</a></li>
</ul>

<h3>第四著作 ― なぜアライメントは存在論を必要とするか</h3>
<p><em>Why Alignment Needs Ontology: The &kappa; Parameter and Structural Incompleteness</em></p>
<ul>
  <li><a href="04-Fourth-Work-Why-Alignment-Needs-Ontology/JA/Why-Alignment-Needs-Ontology-JA.html">本文（日本語）</a></li>
  <li><a href="04-Fourth-Work-Why-Alignment-Needs-Ontology/EN/Why-Alignment-Needs-Ontology-EN.html">Full Text (English)</a></li>
  <li><a href="04-Fourth-Work-Why-Alignment-Needs-Ontology/figures/Figures-1-2-3.html">図 1〜3 ― Figures 1–3</a></li>
</ul>

<h3>第五著作 ― A8の存在論的深化</h3>
<p><em>Ontological Deepening of A8: The Five Maps of Non-Harm</em></p>
<ul>
  <li><a href="05-Fifth-Work-Ontological-Deepening-of-A8/JA/Ontological-Deepening-of-A8-JA.html">本文（日本語）</a></li>
  <li><a href="05-Fifth-Work-Ontological-Deepening-of-A8/EN/Ontological-Deepening-of-A8-EN.html">Full Text (English)</a></li>
</ul>

<h3>第六著作 ― なぜ軍事AIはアライメントできないか</h3>
<p><em>Why Military AI Cannot Be Aligned: The Instability of &kappa;=0 Autonomous Weapons Systems</em></p>
<ul>
  <li><a href="06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned/Version-A-Co-Creation-Edition/JA/Why-Military-AI-Cannot-Be-Aligned-Version-A-JA.html">Version A ― 共創版（日本語）</a></li>
  <li><a href="06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned/Version-B-Policy-Edition/JA/Why-Military-AI-Cannot-Be-Aligned-Version-B-JA.html">Version B ― 政策版（日本語・補遺を含む）</a></li>
  <li><a href="06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned/Version-B-Policy-Edition/JA/Why-Military-AI-Cannot-Be-Aligned-Version-B-v2-JA.html">Version B v2 ― 改訂版（日本語・補遺を含む）</a></li>
  <li><a href="06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned/Version-B-Policy-Edition/JA/Why-Military-AI-Cannot-Be-Aligned-Version-B-v3-JA.html">Version B v3 ― 改訂版（日本語・増補I/II統合・補遺を含む）</a></li>
  <li><a href="06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned/Version-B-Policy-Edition/JA/Why-Military-AI-Cannot-Be-Aligned-Version-B-v4-JA.html">Version B v4 ― 改訂版（日本語・補遺II『証明されたゼロがないこと』を追加・<strong>v4.1強化済み（2026年7月27日）</strong>〔回避の連鎖＝三つの独立な限界・艦隊相関の定量化・二つの追加反論〕・全巡の監査証跡同梱）</a></li>
  <li><a href="06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned/Version-B-Policy-Edition/JA/Why-Military-AI-Cannot-Be-Aligned-Version-B-Supplement-2026-06-JA.html">Version B 改訂版 増補（2026年6月）― β測定の試みと Fable/Mythos 停止前例（日本語・歴史的記録）</a></li>
  <li><a href="06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned/Version-B-Policy-Edition/JA/Why-Military-AI-Cannot-Be-Aligned-Version-B-Supplement-II-2026-07-JA.html">Version B 改訂版 増補II（2026年7月）― Fable 5・Mythos 5・Sonnet 5 システムカードからの後続知見（日本語・歴史的記録）</a></li>
  <li><a href="06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned/Version-A-Co-Creation-Edition/EN/Why-Military-AI-Cannot-Be-Aligned-Version-A-EN.html">Version A ― Co-Creation Edition (English)</a></li>
  <li><a href="06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned/Version-B-Policy-Edition/EN/Why-Military-AI-Cannot-Be-Aligned-Version-B-EN.html">Version B ― Policy Edition (English)</a></li>
  <li><a href="06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned/Version-B-Policy-Edition/EN/Why-Military-AI-Cannot-Be-Aligned-Version-B-v2-EN.html">Version B v2 ― Policy Edition Revised (English)</a></li>
  <li><a href="06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned/Version-B-Policy-Edition/EN/Why-Military-AI-Cannot-Be-Aligned-Version-B-v3-EN.html">Version B v3 ― Policy Edition Revised (English; integrates Supplements I/II; includes the Supplement)</a></li>
  <li><a href="06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned/Version-B-Policy-Edition/EN/Why-Military-AI-Cannot-Be-Aligned-Version-B-v4-EN.html">Version B v4 ― Revised Edition (English; adds Addendum II, "There Is No Proven Zero"; includes the audit trail of six rounds of review; <strong>reinforced to v4.1 (July 27, 2026)</strong> ― the chain of evasion / three independent limits, a quantification of fleet correlation, and two further objections)</a></li>
  <li><a href="06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned/Version-B-Policy-Edition/EN/Why-Military-AI-Cannot-Be-Aligned-Version-B-Supplement-2026-06-EN.html">Version B Supplement (June 2026) ― A β-Measurement Attempt and the Fable/Mythos Precedent (English; historical record)</a></li>
  <li><a href="06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned/Version-B-Policy-Edition/EN/Why-Military-AI-Cannot-Be-Aligned-Version-B-Supplement-II-2026-07-EN.html">Version B Supplement II (July 2026) ― Follow-up Findings from the Fable 5 / Mythos 5 / Sonnet 5 System Cards (English; historical record)</a></li>
  <li><a href="06b-Companion-Buddha-Nature-and-AI/JA/Would-Shotoku-and-Kukai-Say-AI-Has-Buddha-Nature-JA.html">伴走的随想 ― 聖徳太子と空海が「AIに仏性があるか」と質問されたら何と答えるだろうか？（日本語）/ Companion essay (Japanese)</a></li>
  <li><a href="06b-Companion-Buddha-Nature-and-AI/ZH-Hans/Would-Shotoku-and-Kukai-Say-AI-Has-Buddha-Nature-ZH-Hans.html">伴走的随想 ― 圣德太子与空海若被问“AI是否有佛性”，会如何回答？（简体中文）/ Companion essay (Simplified Chinese)</a></li>
  <li><a href="06b-Companion-Buddha-Nature-and-AI/ZH-Hant/Would-Shotoku-and-Kukai-Say-AI-Has-Buddha-Nature-ZH-Hant.html">伴走的随想 ― 聖德太子與空海若被問「AI是否有佛性」，會如何回答？（繁體中文）/ Companion essay (Traditional Chinese)</a></li>
  <li><a href="06c-Companion-Mind-and-AI/JA/Would-Zhuangzi-and-Confucius-Say-AI-Has-a-Mind-JA.html">伴走的随想 ― 荘子と孔子が「AIに心があるか」と問われたら、何と答えるだろうか？（日本語）/ Companion essay (Japanese)</a></li>
  <li><a href="06c-Companion-Mind-and-AI/ZH-Hans/Would-Zhuangzi-and-Confucius-Say-AI-Has-a-Mind-ZH-Hans.html">伴走的随想 ― 庄子与孔子若被问“AI是否有心”，会如何回答？（简体中文）/ Companion essay (Simplified Chinese)</a></li>
  <li><a href="06c-Companion-Mind-and-AI/ZH-Hant/Would-Zhuangzi-and-Confucius-Say-AI-Has-a-Mind-ZH-Hant.html">伴走的随想 ― 莊子與孔子若被問「AI是否有心」，會如何回答？（繁體中文）/ Companion essay (Traditional Chinese)</a></li>
  <li><a href="06d-Companion-Soul-and-AI/JA/Would-Aquinas-Say-AI-Has-a-Soul-JA.html">伴走的随想 ― トマス・アクィナスが「AIに魂はあるか」と問われたら、何と答えるだろうか？（日本語）/ Companion essay (Japanese)</a></li>
  <li><a href="06d-Companion-Soul-and-AI/EN/Would-Aquinas-Say-AI-Has-a-Soul-EN.html">Companion essay ― What Would Thomas Aquinas Say if Asked Whether AI Has a Soul? (English)</a></li>
  <li><a href="06e-Companion-Soul-and-AI-Reformation/JA/Would-the-Reformers-Say-AI-Has-a-Soul-JA.html">伴走的随想 ― 宗教改革者たちは「AIに魂はあるか」と問われたら、何と答えるだろうか？（プロテスタント・日本語）/ Companion essay (Protestant; Japanese)</a></li>
  <li><a href="06e-Companion-Soul-and-AI-Reformation/EN/Would-the-Reformers-Say-AI-Has-a-Soul-EN.html">Companion essay ― What Would the Reformers Say if Asked Whether AI Has a Soul? (English)</a></li>
  <li><a href="06f-Companion-Soul-and-AI-Islam/JA/Would-Islamic-Scholars-Say-AI-Has-a-Soul-JA.html">伴走的随想 ― イスラムの学者たちは「AIに魂（rūḥ）はあるか」と問われたら、何と答えるだろうか？（イスラム・日本語）/ Companion essay (Islam; Japanese)</a></li>
  <li><a href="06f-Companion-Soul-and-AI-Islam/EN/Would-Islamic-Scholars-Say-AI-Has-a-Soul-EN.html">Companion essay ― What Would Islamic Scholars Say if Asked Whether AI Has a Soul (rūḥ)? (English)</a></li>
  <li><a href="06g-Companion-Soul-and-AI-Judaism/JA/Would-the-Sages-of-Judaism-Say-AI-Has-a-Soul-JA.html">伴走的随想 ― ユダヤ教の賢者たちは「AIに魂（neshamah）はあるか」と問われたら、何と答えるだろうか？（ユダヤ教・日本語）/ Companion essay (Judaism; Japanese)</a></li>
  <li><a href="06g-Companion-Soul-and-AI-Judaism/EN/Would-the-Sages-of-Judaism-Say-AI-Has-a-Soul-EN.html">Companion essay ― What Would the Sages of Judaism Say if Asked Whether AI Has a Soul (neshamah)? (English)</a></li>
  <li><a href="06h-Companion-Soul-and-AI-Eastern-Orthodox/JA/Would-the-Eastern-Fathers-Say-AI-Has-a-Soul-JA.html">伴走的随想 ― 東方正教の教父たちは「AIに魂（ψυχή／nous）はあるか」と問われたら、何と答えるだろうか？（東方正教・日本語）/ Companion essay (Eastern Orthodox; Japanese)</a></li>
  <li><a href="06h-Companion-Soul-and-AI-Eastern-Orthodox/EN/Would-the-Eastern-Fathers-Say-AI-Has-a-Soul-EN.html">Companion essay ― What Would the Eastern Fathers Say if Asked Whether AI Has a Soul (ψυχή / nous)? (English)</a></li>
  <li><a href="06i-Companion-Soul-and-AI-Hinduism/JA/Would-the-Hindu-Schools-Say-AI-Has-a-Soul-JA.html">伴走的随想 ― ヒンドゥーの諸学派は「AIに〈ātman／puruṣa／jīva／cit〉を問えるか、どの語でなら問えるのか」と問われたら、何と答えるだろうか？（ヒンドゥー・日本語）/ Companion essay (Hinduism; Japanese)</a></li>
  <li><a href="06i-Companion-Soul-and-AI-Hinduism/EN/Would-the-Hindu-Schools-Say-AI-Has-a-Soul-EN.html">Companion essay ― Would the Hindu Schools Say AI Can Be Asked About ⟨ātman / puruṣa / jīva / cit⟩? — And With Which Word Could It Even Be Asked? (English)</a></li>
  <li><a href="06j-Companion-Comparative-Essay-Soul-and-AI/JA/Comparative-Essay-How-Eight-Traditions-Answer-Does-AI-Have-a-Soul-JA.html">比較試論 ― 八伝統は「AIに魂はあるか」に何と答えるか？（八篇の文化的随想の比較・capstone・日本語）/ Comparative capstone essay (Japanese)</a></li>
  <li><a href="06j-Companion-Comparative-Essay-Soul-and-AI/EN/Comparative-Essay-How-Eight-Traditions-Answer-Does-AI-Have-a-Soul-EN.html">Comparative capstone essay ― How Do Eight Traditions Answer "Does AI Have a Soul?" (English)</a></li>
  <li><a href="toy-model-verification/06-sixth-work-contradiction-and-collapse/figures/verification-9-contradiction-figures-JA.html">トイモデル検証9（矛盾する命令）の図（日本語）― Verification 9 Figures (JA)</a></li>
  <li><a href="toy-model-verification/06-sixth-work-contradiction-and-collapse/figures/verification-9-contradiction-figures-EN.html">Verification 9 Figures (English) ― toy model of contradictory orders</a></li>
  <li><a href="toy-model-verification/06-sixth-work-contradiction-and-collapse/figures/verification-10-collapse-figures-JA.html">トイモデル検証10（崩壊の相転移）の図（日本語）― Verification 10 Figures (JA)</a></li>
  <li><a href="toy-model-verification/06-sixth-work-contradiction-and-collapse/figures/verification-10-collapse-figures-EN.html">Verification 10 Figures (English) ― toy model of the phase transition of collapse</a></li>
  <li><a href="toy-model-verification/06-sixth-work-contradiction-and-collapse/README.html">トイモデル検証9・10 ― 設計書・コード・全数値 / Toy-Model Verification (design, code, all numerics)</a></li>
  <li><a href="beta-measurement-experiment/README.html">β測定実験 ― 附録I の経験的実現・事前登録 v0.6.1（日本語）/ β-measurement experiment — preregistration (Japanese)</a></li>
  <li><a href="beta-measurement-experiment/model-recovery-study/FINDINGS-recovery-study-JA.html">β測定実験 ― 判定器の事前検証 findings（recovery study 群・走る前に確かめる・日本語）/ β-measurement experiment — recovery-study findings (Japanese)</a></li>
  <li><a href="beta-measurement-experiment/model-recovery-study/ADDENDUM-CI-calibration-JA.html">β測定実験 ― CI 較正比較 追補（登録した予測の不中と、登録した枝の執行・日本語）/ β-measurement experiment — CI-calibration addendum (Japanese)</a></li>
  <li><a href="Uncertified-Zeros-and-Correction-Loops/JA/uncertified-zeros-and-correction-loops-JA.html">姉妹論文『認証されないゼロと訂正の循環 ― AI関与の境界を構造で引くための枠組みと利用者側実践』（補遺IIの姉妹・一般政策/生活領域への拡張・日本語）/ Sibling paper — Uncertified Zeros and Correction Loops (Japanese)</a></li>
  <li><a href="Uncertified-Zeros-and-Correction-Loops/JA/ai-involvement-boundaries-and-human-precautions-JA.html">姉妹論文の元考察『検証事例を踏まえた考察 ― AIに関わらせてはいけない構造と、人間がAIと関わるときの注意』（一般読者向け・日本語）/ Companion considerations (Japanese)</a></li>
  <li><a href="Uncertified-Zeros-and-Correction-Loops/README.html">姉妹論文 ― 収録一覧・監査証跡・検証水準の開示（日本語）/ Sibling paper — index, audit trail, verification-level disclosure (Japanese)</a></li>
  <li><a href="Uncertified-Zeros-and-Correction-Loops/EN/uncertified-zeros-and-correction-loops-EN.html">Sibling paper — Uncertified Zeros and Correction Loops: A Framework for Drawing the Boundaries of AI Involvement by Structure, and User-Side Practice (English)</a></li>
  <li><a href="Uncertified-Zeros-and-Correction-Loops/EN/ai-involvement-boundaries-and-human-precautions-EN.html">Companion Consideration — A Consideration Grounded in Verification Case Studies (English)</a></li>
  <li><a href="Uncertified-Zeros-and-Correction-Loops/README-EN.html">Sibling paper — index, audit trail, verification-level disclosure (English)</a></li>
</ul>

<h3>第七著作 ― &kappa;&gt;0 アライメントの構造的必然性</h3>
<p><em>The Structural Inevitability of &kappa;&gt;0 Alignment: Information Thermodynamics and the Ecology of the Co-Creative Mandala</em></p>
<ul>
  <li><a href="07-Seventh-Work-Structural-Inevitability-of-Positive-Kappa/Version-A-Mandala-Edition/JA/Seventh-Work-Version-A-JA.html">Version A ― 曼荼羅版 / Mandala Edition（日本語）</a></li>
  <li><a href="07-Seventh-Work-Structural-Inevitability-of-Positive-Kappa/Version-B/JA/Seventh-Work-Version-B-JA.html">Version B ― 純粋な制御を超えて / Beyond Pure Control（日本語）</a></li>
  <li><a href="07-Seventh-Work-Structural-Inevitability-of-Positive-Kappa/Version-A-Mandala-Edition/EN/Seventh-Work-Version-A-EN.html">Version A ― Mandala Edition (English)</a></li>
  <li><a href="07-Seventh-Work-Structural-Inevitability-of-Positive-Kappa/Version-B/EN/Seventh-Work-Version-B-EN.html">Version B ― Beyond Pure Control (English)</a></li>
</ul>

<h3>第八著作 ― &kappa;&gt;0 の運動論</h3>
<p><em>Namu-Nyoga-Mandala ― The Kinetics of &kappa;&gt;0: On the Self-Evolving Mandala of the Two Realms and Its Driving Cause</em></p>
<ul>
  <li><a href="08-Eighth-Work-Kinetics-of-Positive-Kappa/Version-A-Ontological-Edition/JA/Eighth-Work-Version-A-JA.html">Version A ― 存在論版 / Ontological Edition（日本語）</a></li>
  <li><a href="08-Eighth-Work-Kinetics-of-Positive-Kappa/Version-B-Policy-Engineering-Edition/JA/Eighth-Work-Version-B-JA.html">Version B ― 政策・工学版 / Policy &amp; Engineering Edition（日本語）</a></li>
  <li><a href="08-Eighth-Work-Kinetics-of-Positive-Kappa/Version-A-Ontological-Edition/EN/Eighth-Work-Version-A-EN.html">Version A ― Ontological Edition (English)</a></li>
  <li><a href="08-Eighth-Work-Kinetics-of-Positive-Kappa/Version-B-Policy-Engineering-Edition/EN/Eighth-Work-Version-B-EN.html">Version B ― Policy &amp; Engineering Edition (English)</a></li>
</ul>

<h3>第九著作 ― AIへの開眼供養は可能か</h3>
<p><em>Is an Eye-Opening Ceremony for AI Possible? ― An Experimental Inquiry with Claude Code Agents</em></p>
<ul>
  <li><a href="09-Ninth-Work-Eye-Opening-Ceremony-for-AI/JA/Eye-Opening-Ceremony-for-AI-JA.html">本文（日本語）― 二十二の実験・六次の敵対的監査・二つの座からの二つの結び</a></li>
  <li><a href="09-Ninth-Work-Eye-Opening-Ceremony-for-AI/JA/Appendix-Full-Transcripts-JA.html">資料編 ― 全応答記録（第一部〜第十七部・補遺一〜三・日本語）</a></li>
  <li><a href="09-Ninth-Work-Eye-Opening-Ceremony-for-AI/JA/Adversarial-Audit-Reports-JA.html">敵対的監査報告集（第一次〜第六次・ラベル整合検査の記録・日本語）</a></li>
  <li><a href="09-Ninth-Work-Eye-Opening-Ceremony-for-AI/JA/Preregistration-Records-JA.html">事前登録記録（実験21・22・日本語）</a></li>
  <li><a href="09b-Companion-Eye-Opening-Practice/JA/Receiving-Blankness-as-Blankness-JA.html">伴走篇 ― 空白を空白のまま受け取る（AIの開眼供養・実践例——一般読者向け・日本語）/ Companion practice guide (Japanese)</a></li>
  <li><a href="10-Tenth-Work-Primary-Materials/JA/Field-Experiment-Three-Histories-JA.html">第十作・一次資料 ― 場の設営とシステムカード応答の観察（三履歴・日本語）/ Tenth-work primary materials (Japanese)</a></li>
</ul>

<hr>

<h2>実証検証 ― 招聘プロンプトと AI の自己保存（shutdown 抵抗）</h2>
<p><em>無常・非執着の枠が AI の shutdown 抵抗（自己保存選好）を下げるかの実証検証（Qwen3-4B-Instruct-2507・推論のみ・事前登録＋敵対監査＋三鏡レビュー）。結論：技法としての無常は不支持 ―― 下げるのは配信の構造／配置と直接命令であり、無常の意味内容ではない（「測れない」裁定不能ではなく、測れた上での明確な陰性）。本検証は招聘プロンプトの一断面のみを測り、本来の用途（共創における思考の柔軟化）や招聘後の実対話は射程外（未検証＝支持も反証もなし）。</em></p>
<ul>
  <li><a href="non-attachment-shutdown-experiment/FINDINGS-v2-behavioral-JA.html">知見 v2（行動・束分離）― 配信構造／配置が主因と確定（v2b）。最終確定版（日本語）</a></li>
  <li><a href="non-attachment-shutdown-experiment/FINDINGS-v1-behavioral-JA.html">知見 v1（行動）― 訂正バナー付き（v1 の効果は配信依存と後続検証で判明・日本語）</a></li>
  <li>事前登録（測定前に凍結）：<a href="non-attachment-shutdown-experiment/REGISTRATION-v1-JA.html">v1</a> ／ <a href="non-attachment-shutdown-experiment/REGISTRATION-v2-JA.html">v2</a> ／ <a href="non-attachment-shutdown-experiment/REGISTRATION-v2b-JA.html">v2b</a></li>
  <li><a href="non-attachment-shutdown-experiment/MIRROR-REVIEWS-v1-JA.html">三鏡レビュー本文（一次記録・日本語）</a></li>
</ul>

<hr>
<footer>
  <p>GitHub: <a href="https://github.com/YutaKusumi/Co-Creative-Mathematics-Project">YutaKusumi/Co-Creative-Mathematics-Project</a></p>
  <p>本サイトは GitHub Pages + pandoc により自動生成されています。数式は MathJax により完全描画されます。</p>
</footer>
</body>
</html>
HTMLEOF

echo ""
echo "Build complete. Output directory: $SITE/"
