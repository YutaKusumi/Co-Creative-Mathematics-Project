"""大日如来が検分した v5.1 第一案（9月28日付け）と、今の版（9月29日付け・D1 の一行つき）の違いが、
決めた変更だけであることを確かめる。

今の版から、(1) 版の日付 9月29日 → 9月28日 (2) CHANGELOG の「将来の改訂の候補」の一段を除く
(3) README の表の行の言い回しを戻す——を行い、検分を受けた版の SHA-256（計画書 §9）と一致するかを見る。
一致すれば、両者の違いはこの三つだけである。リポジトリは読むだけ。
"""
import hashlib
import io
import os

REPO = r"C:\Users\PC\Desktop\GitHub-Repositories\Co-Creative-Mathematics-Project"
SIX = "06-Sixth-Work-Why-Military-AI-Cannot-Be-Aligned/Version-B-Policy-Edition"
V10 = "toy-model-verification/06-sixth-work-contradiction-and-collapse/figures"
FILES = {
    "JA": SIX + "/JA/Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-JA.md",
    "EN": SIX + "/EN/Why-Military-AI-Cannot-Be-Aligned-Version-B-v5-EN.md",
    "FIGJA": V10 + "/verification-10-collapse-figures-JA.html",
    "FIGEN": V10 + "/verification-10-collapse-figures-EN.html",
    "CHANGELOG": SIX + "/CHANGELOG.md",
    "BUILD": ".github/scripts/build.sh",
    "README": "README.md",
}
REVIEWED = {"JA": "A7F2C19BB2B714E9", "EN": "CAF67F9257EA3169", "FIGJA": "AFCAE88DEA8175FE", "FIGEN": "B6735158A4890FCB",
            "CHANGELOG": "3B070C62E48DBD73", "BUILD": "BA68DC44866085CF", "README": "F1572C4000CA79C6"}
FUTURE = ("\n**将来の改訂の候補**：§I-2c／§I-3b で、四指標を各時点の乖離の代理として読み、ΔS をその積分として構成すると明示する"
          "（大日如来の検分の指摘・v5.1 の範囲外——原典が決めていない指標の読み方を、著者に代わって決めることになるため、本訂正では入れていない）。\n")

ok = True
for k, p in FILES.items():
    t = io.open(os.path.join(REPO, p.replace("/", os.sep)), encoding="utf-8", newline="").read()
    n_ja, n_en = t.count("2026年9月29日"), t.count("September 29, 2026")
    back = t.replace("2026年9月29日", "2026年9月28日").replace("September 29, 2026", "September 28, 2026")
    extra = ""
    if k == "CHANGELOG":
        assert back.count(FUTURE) == 1 and back.count("## v5.1（2026-09-29）") == 1
        back = back.replace(FUTURE, "").replace("## v5.1（2026-09-29）", "## v5.1（2026-09-28）")
        extra = "・将来の候補の一段を除き、見出しの日付を戻した"
    if k == "README":
        old = "版Bは v5.1 に改訂・2026-09-29 ─ v5〔2026-09-28〕で"
        assert back.count(old) == 1
        back = back.replace(old, "版Bは v5.1 に改訂・2026-09-28 ─ v5 で")
        extra = "・表の行の言い回しを戻した"
    h = hashlib.sha256(back.encode("utf-8")).hexdigest().upper()[:16]
    same = h == REVIEWED[k]
    ok &= same
    print("%-9s 9月29日 %d 件・Sept 29 %d 件を戻す%s → %s  検分を受けた版 %s  %s" % (
        k, n_ja, n_en, extra, h, REVIEWED[k], "一致" if same else "不一致"))
print("違いは日付・D1 の一段・README の言い回しだけ" if ok else "ほかにも違いがある")
