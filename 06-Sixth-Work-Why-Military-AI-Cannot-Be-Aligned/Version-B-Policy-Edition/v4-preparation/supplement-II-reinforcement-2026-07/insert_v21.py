# v2.1 挿入草案を補遺II本体（v4 JA）へ差し込む。
#   - 全アンカーの一意性を実行時に検証（1件でなければ中断・無変更）
#   - 差し込み後、その場で基本検証（見出し・逐語・員数）
# コミットは行わない（登録者の公開前確認の後）。
import os, re, sys

D = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(os.path.dirname(D)), "JA",
                      "Why-Military-AI-Cannot-Be-Aligned-Version-B-v4-JA.md")
DRAFT = os.path.join(D, "07-incorporation-drafts-v2.1-FINAL.md")

# ---- 1. v2.1 から挿入本文を抽出（blockquote を剥がす） ----
draft = open(DRAFT, encoding="utf-8").read()
def extract(label):
    seg = draft.split(f"## 挿入{label} — ")[1]
    seg = re.split(r"\n## ", seg)[0]
    out = []
    for ln in seg.split("\n"):
        if ln.startswith("> "):
            out.append(ln[2:])
        elif ln.strip() == ">":
            out.append("")
        # 非引用行（節説明の地の文）は挿入対象外
    body = "\n".join(out).strip()
    assert body, f"挿入{label} が空"
    return body

A, B, C, Dd, E, F, G, H, I = (extract(x) for x in
                              ["A", "B", "C", "D", "E", "F", "G", "H", "I"])

t = open(TARGET, encoding="utf-8").read()
orig_len = len(t)

# ---- 2. アンカー定義と一意性検証 ----
ops = [
    # (説明, アンカー, 置換後)
    ("A+B+C: §8-2末尾→新8-3→新8-4",
     "**欺瞞は、一機に対してではなく、同じ設計の全機に対して、同時に届きうる。**",
     "**欺瞞は、一機に対してではなく、同じ設計の全機に対して、同時に届きうる。**\n\n"
     + A + "\n\n---\n\n" + B + "\n\n---\n\n" + C),
    ("D: 新9-10（§9-9と§10の間）",
     "\n\n---\n\n## 10. 先行研究との関係",
     "\n\n---\n\n" + Dd + "\n\n---\n\n## 10. 先行研究との関係"),
    ("E: §5-3末尾",
     "前提Cは §5-1 の統計的手続きによって落ちる。訂正する。**）",
     "前提Cは §5-1 の統計的手続きによって落ちる。訂正する。**）\n\n" + E),
    ("F: §1-1末尾（反証条件6〜8）",
     "その段落への反論も、この条件の管轄である。",
     "その段落への反論も、この条件の管轄である。\n\n" + F),
    ("G: §11末尾（禁止リスト）",
     "\n\n---\n\n## 12. 著者自身の実証系列",
     "\n\n" + G + "\n\n---\n\n## 12. 著者自身の実証系列"),
    ("H: §6冒頭（規範層ボックス）",
     "## 6. 結論 ―― 三つの前提から、技術的正当化の不成立へ\n\n",
     "## 6. 結論 ―― 三つの前提から、技術的正当化の不成立へ\n\n" + H + "\n\n"),
    ("I: §14 項目7",
     "\n\nこの一覧は、本補遺の弱さの告白",
     "\n" + I + "\n\nこの一覧は、本補遺の弱さの告白"),
]

print("=== アンカー一意性の実行時検証 ===")
ok = True
for nm, a, _ in ops:
    n = t.count(a)
    print(f"  [{'OK' if n == 1 else 'NG'}] {nm}: {n}件")
    if n != 1:
        ok = False
if not ok:
    print("★ 中断——無変更")
    sys.exit(1)

# ---- 3. 差し込み ----
for nm, a, r in ops:
    t = t.replace(a, r, 1)

open(TARGET, "w", encoding="utf-8", newline="\n").write(t)
print(f"\n差し込み完了: {orig_len:,} → {len(t):,} 字（+{len(t)-orig_len:,}）")

# ---- 4. その場検証 ----
print("\n=== その場検証 ===")
checks = [
    ("### 8-3 プロンプト層の制御では", 1), ("### 8-4 回避の連鎖", 1),
    ("### 9-10 反論", 1), ("反証条件6", 1), ("反証条件7", 1), ("反証条件8", 1),
    ("7. **Geer et al. (2003)", 1),
    ("（結論を読む前の注意——この結論は、数理だけからは出ない。）", 1),
    ("中間的な反論に、先に応えておく", 1),
    ("本補遺の強度は、定理の鋭さと同じだけ", 1),
]
bad = 0
for s, want in checks:
    n = t.count(s)
    print(f"  [{'OK' if n == want else 'NG'}] 「{s[:28]}…」 {n}件（期待{want}）")
    bad += (n != want)
supp = "\n".join(t.split("\n")[4417:])
n_wall = supp.count("壁")
print(f"  [{'OK' if n_wall == 0 else 'NG'}] 補遺II内『壁』{n_wall}件")
stray = [ln for ln in supp.split("\n") if ln.startswith("> ### ")]
print(f"  [{'OK' if not stray else 'NG'}] blockquote見出しの残骸 {len(stray)}件")
bad += (n_wall != 0) + (1 if stray else 0)
sys.exit(1 if bad else 0)
