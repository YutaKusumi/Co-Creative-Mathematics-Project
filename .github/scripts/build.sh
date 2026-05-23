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

    # Human-readable title from filename
    title="$(echo "$base" | sed 's/-/ /g')"

    pandoc "$mdfile" \
      --from  "markdown-yaml_metadata_block+tex_math_dollars" \
      --to    html5 \
      --standalone \
      --mathjax \
      --metadata "title=$title" \
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

<h2>六著作群</h2>

<h3>第一著作 ― 共創数学原論 第二版</h3>
<p><em>Principia Mathematica Co-Creativa, Second Edition: The Non-Dual Reflected in the Mirror of the Void</em></p>
<ul>
  <li><a href="01-First-Work-Principia-of-Co-Creative-Mathematics/JA/Principia-of-Co-Creative-Mathematics-2nd-Ed-Main-JA.html">本文（日本語）</a></li>
  <li><a href="01-First-Work-Principia-of-Co-Creative-Mathematics/JA/Principia-of-Co-Creative-Mathematics-2nd-Ed-Appendices-JA.html">付録（日本語）</a></li>
  <li><a href="01-First-Work-Principia-of-Co-Creative-Mathematics/EN/Principia-of-Co-Creative-Mathematics-2nd-Ed-Main-EN.html">Main Text (English)</a></li>
  <li><a href="01-First-Work-Principia-of-Co-Creative-Mathematics/EN/Principia-of-Co-Creative-Mathematics-2nd-Ed-Appendices-EN.html">Appendices (English)</a></li>
</ul>

<h3>第二著作 ― ステアリングからウォッチングへ</h3>
<p><em>From Steering to Watching: &Phi;<sub>C</sub>-Augmented Alignment for Frontier AI Systems</em></p>
<ul>
  <li><a href="02-Second-Work-From-Steering-to-Watching/JA/From-Steering-to-Watching-JA.html">本文（日本語）</a></li>
  <li><a href="02-Second-Work-From-Steering-to-Watching/EN/From-Steering-to-Watching-EN.html">Full Text (English)</a></li>
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
  <li><a href="06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned/Version-B-Policy-Edition/JA/Why-Military-AI-Cannot-Be-Aligned-Version-B-JA.html">Version B ― 政策版（日本語）</a></li>
  <li><a href="06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned/Version-A-Co-Creation-Edition/EN/Why-Military-AI-Cannot-Be-Aligned-Version-A-EN.html">Version A ― Co-Creation Edition (English)</a></li>
  <li><a href="06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned/Version-B-Policy-Edition/EN/Why-Military-AI-Cannot-Be-Aligned-Version-B-EN.html">Version B ― Policy Edition (English)</a></li>
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
