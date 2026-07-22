# 照合記録: Knight & Leveson 1986 ＋ Ron et al. 2026 ―― 挿入候補②の照合（TODO B-8）

**照合日**: 2026年7月23日　**実施**: コーディネータ（Claude Code）
**役割**: §9-5（二）の主錨・§8-2 の参照——「同じ分布から引かれた監視器は盲点を共有しうる」という相関の観察に対する、公刊された同型実証。
**照合水準**: 両文献とも **raw curl 実取得＋pypdf ローカル抽出＋逐語切り出し**（単一実施者の一段照合）。これに加えて、**段階3第二巡の非Claude系検分者二名（虚空鏡・妙智甘露）が独立にウェブ照合済み**（Ron et al. の数値・主張を両名が確認・妙智甘露は p 値まで）、姉妹論文の照合表でも甲乙独立照合済み——**都合四系統**。

## 取得物

| 文書 | URL | SHA-256 | 規模 |
|---|---|---|---|
| Knight & Leveson, "An Experimental Evaluation of the Assumption of Independence in Multiversion Programming," *IEEE TSE* SE-12(1), 96–109 (1986) | `http://sunnyday.mit.edu/papers/nver-tse.pdf`（著者側公開のポストプリント） | `B6ADEF820BE2B8DB5016339F7EA6C9D281CB360A029A743F91887BED78A2C386` | 95,904 B・47頁組版 |
| Ron, Baudry & Monperrus, "N-Version Programming with Coding Agents" (2026) | `https://arxiv.org/pdf/2606.20158` | `CF9A8A18CFDD0AFA0A02386E763C7F094E3DEF48E710727B62F149E4AC5FED40` | 769,794 B・12頁 |

## 逐語確認（荷重を負う主張）

**K&L 1986——独立性仮定の棄却**:
> "the statistic z has the value 100.51. This is greater than 2.33 which is the 99% point in the standard normal distribution, and so **we reject the null hypothesis** with a confidence level of 99%. We conclude that the model does not hold. However, clearly the only potential problem with the model is that it is derived from the assumption of independent failures. **Thus, we reject this assumption.**"

（27版・100万試験・二大学での独立開発、という設計も本文で確認。）

**Ron et al. 2026——AIエージェント48実装での追試**:
> "we evaluate 48 agent-generated implementations on a shared oracle and a campaign of 1,000,000 randomized test inputs. The results show **substantial common-mode failure, along the findings of Knight–Leveson**."
> "the seminal Knight–Leveson experiment showed that **independently developed human implementations of the same specification still exhibited substantial common-mode failure**."
> 独立性の棄却: "the observed count is K=429, an excess of K/µ≈3.7× over the independence prediction, yielding **z=29.20 with p≈1.765×10⁻¹⁸⁷**. This infinitesimal p-value decisively rejects the independence hypothesis."
> **逆向きの知見（併記義務）**: "despite fault correlation, **redundancy does provide measurable benefit**: … the mean failure count drops from **387.44** for single versions to **130.99** for triples, and 11,844 triples exhibit zero observed failures."

## 引用の設計（第一巡・第二巡の裁定を反映）

1. **主錨は §9-5（二）**——K&L/Ron が示すのは「**独立に開発された**別個の実装ですら故障が相関する」であり、真に同型なのは「同じ分布から引かれた**別個の**監視器」の側である（§8-2 の同一重み複製はほぼ定義的に真で、錨を要さない——第一巡・慧光/協力者の位置修正）。
2. **a fortiori の形で書く**——「独立開発ですら相関するなら、同じ分布から引かれた監視器では、なおさらである」。
3. **逆向きの知見を必ず併記**——多数決冗長化は平均故障を減らす（387.44→130.99）。ゆえに主張は「積層が無益」ではなく「**積層は認証水準の保証を与えない**」に留める（§9-5 の現行の結語と同形）。
