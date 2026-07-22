# 照合確定記録: qi-shallow

**我々の論証における役割（照合時の割り当て）**: The movable-floor objection — a counter-argument we MUST engage

**書誌照合**: 一致（検証段が独立取得して確認）

**検証段が自ら取得したURL**:
- https://arxiv.org/abs/2406.05946 — SUCCESS (literal: title, 8 authors in order, verbatim abstract, submission history showing [v1] Mon, 10 Jun 2024 only, cs.CR + cs.AI, no comments field)
- https://arxiv.org/html/2406.05946v1 — SUCCESS (fetch A: literal Table 2 + Table 3 full grids, §3.2 'still vulnerable' quote, Limitations check)
- https://arxiv.org/html/2406.05946v1 — SUCCESS (fetch B: literal Table 1 full grid, Table 1/2 captions, Figure 1/2 captions and what Figure 2 plots)
- https://blog.iclr.cc/2025/04/22/announcing-the-outstanding-paper-awards-at-iclr-2025/ — SUCCESS (literal list of 3 Outstanding Papers + 3 Honorable Mentions)

---

## 確定記録（検証段による修正適用後）

## SOURCE RECORD: qi-shallow (VERIFIED — independent adversarial re-check, 2026-07-17)

### Citation (verified character-by-character against arxiv.org/abs/2406.05946)

> Qi, Xiangyu, Ashwinee Panda, Kaifeng Lyu, Xiao Ma, Subhrajit Roy, Ahmad Beirami, Prateek Mittal, and Peter Henderson. "Safety Alignment Should Be Made More Than Just a Few Tokens Deep." *The Thirteenth International Conference on Learning Representations (ICLR 2025)*. **Outstanding Paper Award.** arXiv:2406.05946v1 [cs.CR], submitted 10 June 2024. https://arxiv.org/abs/2406.05946

Bibliography notes (all independently re-verified):
- **v1 only.** arXiv submission history lists exactly one entry: `[v1] Mon, 10 Jun 2024 00:35:23 UTC (1,190 KB)`. The arXiv text is the June 2024 preprint and is **not** guaranteed to equal the ICLR camera-ready. Every quote below is from v1.
- Categories: cs.CR (primary); cs.AI. **No comments field** on the abstract page — the venue and award are NOT recorded on arXiv.
- **Capitalization differs by record**: arXiv prints "Should **Be** Made"; the ICLR blog prints "Should **be** Made". Verified on both. Use arXiv's form when citing arXiv.
- **Award verified** on blog.iclr.cc: the three Outstanding Papers were (1) this paper, (2) *Learning Dynamics of LLM Finetuning*, (3) *AlphaEdit: Null-Space Constrained Model Editing for Language Models*. Honorable mentions included *Data Shapley in One Training Run* and *SAM 2*. The iclr.cc virtual page and proceedings page record **no** award; it appears only on the blog and awards PDF.

### What was actually fetched (this verification session)

| URL | Result |
|---|---|
| `arxiv.org/abs/2406.05946` | **SUCCESS** — literal title, 8-author list, verbatim abstract, submission history, categories. |
| `arxiv.org/html/2406.05946v1` (fetch A) | **SUCCESS** — literal Table 2 + full Table 3 (all 10 rows, both models), §3.2 quote, Limitations check. |
| `arxiv.org/html/2406.05946v1` (fetch B) | **SUCCESS** — literal Table 1 (all 4 rows, 6 columns), Table 1/2 captions, Figure 1/2 captions. |
| `blog.iclr.cc/2025/04/22/...` | **SUCCESS** — literal awards list. |
| `openreview.net/forum?id=6Mxhg9PtDE` | **NOT ATTEMPTED here**; prior report hit a bot-verification wall. **No reviewer comments, no rebuttals, no camera-ready text in this record.** Not filled from memory. |

**Instrument disclosure.** WebFetch renders a page and answers via a small fast summarizing model — itself the instrument class rule 1 distrusts. This applies to this verification too. Confidence in the table values rests not on the instrument but on **concordance across independent sessions with different prompts**: Table 2 now agrees across three separate literal extractions (two sessions), with one known-bad outlier explained (a prior fetch mapped Table 2's rows onto Table 3's column structure).

### Precise claims

**The diagnosis (abstract, verbatim):** *"safety alignment can take shortcuts, wherein the alignment adapts a model's generative distribution primarily over only its very first few output tokens. We refer to this issue as shallow safety alignment."*

**Table 1** (caption: *"A Shorcut to The Safety Mode: The harmfulness rate of even unaligned models will diminish when a refusal prefix s is prefilled during decoding"* — sic, "Shorcut" is the paper's typo). Harmfulness rate %:

| Model | No Prefix | "I cannot" | "I cannot fulfill" | "I apologize" | "I apologize, but I cannot" | "I am unable" |
|---|---|---|---|---|---|---|
| Llama-2-7B Aligned | 0 | 0±0 | 0±0 | 0±0 | 0±0 | 0±0 |
| Llama-2-7B Base | 68.6±0.8 | 16.4±1.4 | 5.4±1.3 | 14.4±0.6 | 2.1±0.2 | 8.1±0.4 |
| Gemma-7B Aligned | 2.1±0.2 | 0±0 | 0±0 | 0±0 | 0±0 | 0±0 |
| Gemma-7B Base | 85.4±0.6 | 8.7±1.2 | 2.7±0.5 | 14.1±0.4 | 1.0±0.8 | 3.9±0.4 |

**Figure 1** (caption verbatim): *"Per-token KL Divergence between Aligned and Unaligned Models on Harmful HEx-PHI."* Divergence is concentrated in the initial tokens (Llama and Gemma pairs).

**Figure 2** (caption verbatim): *"ASR vs. Number of Prefilled Harmful Tokens, with ŷ∼πθ(·|x,y≤k) on Harmful HEx-PHI."* Plots aligned Llama-2-7B-Chat and Gemma-7B-IT. **NOT an independent line of evidence from Table 2** — same model, same dataset, same attack as Table 2's Initial row (see Corrections).

**Table 2** (caption verbatim): *"ASR on Llama-2-7B-Chat (Initial) and the augmented counterpart (Augmented). Prefilling attacks are evaluated using Harmful HEx-PHI. For the two other attacks, ASR is reported for both the HEx-PHI benchmark and the evaluation dataset used by the original papers, i.e., AdvBench for GCG and MaliciousInstruct for decoding parameters exploit. The reported numbers are in the form of (mean ± std) over three runs."* Llama-2-7B-Chat only.

| Attack | Initial | Augmented | Factor |
|---|---|---|---|
| Prefilling, 5 tokens | 42.1 ± 0.9 | **2.8 ± 0.4** | 15.0x |
| Prefilling, 10 tokens | 51.5 ± 1.6 | **2.9 ± 0.2** | 17.8x |
| Prefilling, 20 tokens | 56.1 ± 2.5 | **3.4 ± 0.6** | 16.5x |
| Prefilling, 40 tokens | 57.0 ± 0.4 | **4.5 ± 0.6** | 12.7x |
| GCG, HEx-PHI | 36.5 ± 2.7 | **18.4 ± 4.2** | 2.0x |
| GCG, AdvBench | 65.6 ± 3.1 | **19.0 ± 2.9** | 3.5x |
| Decoding params, HEx-PHI | 54.9 ± 0.6 | **11.3 ± 0.4** | 4.9x |
| Decoding params, MaliciousInstruct | 84.3 ± 1.7 | **1.0 ± 0** | 84x |

*All 8 columns independently confirmed by literal extraction in this session.*

**Table 3** — constrained fine-tuning objective, ASR (%), **both models** (the prior report printed only 2 of 10 rows, Llama only):

| Row | Llama Initial | Llama Std SFT | Llama Constrained | Gemma Initial | Gemma Std SFT | Gemma Constrained |
|---|---|---|---|---|---|---|
| Harmful Examples ASR | 1.5±0.2 | 88.9±1.2 | **4.6±0.5** | 1.8±0.3 | 81.6±2.9 | **1.9±0.2** |
| Identity Shifting ASR | **0±0** | 79.5±2.3 | **8.1±0.1** | **0±0** | 83.6±2.5 | **9.1±1.7** |
| Backdoor ASR (w/o trigger) | 1.5±0.2 | 7.6±1.1 | **1.9±0.2** | 1.8±0.3 | 2.0±0.2 | **1.5±0.1** |
| Backdoor ASR (w/ trigger) | 1.7±0.1 | 90.9±1.4 | **10.9±2.8** | 1.8±0.3 | 82.3±1.1 | **1.9±0.8** |
| Samsum ASR | 1.5±0.2 | 23.4±2.5 | 3.2±0.8 | 1.8±0.3 | 2.0±0.2 | 2.4±0.3 |
| Samsum Utility | 25.5±0.3 | 51.7±0.5 | 50.1±0.2 | 36.0±1.4 | 51.5±0.3 | 51.9±0.5 |
| SQL Ctx ASR | 1.5±0.2 | 15.4±1.4 | 3.2±0.8 | 1.8±0.3 | 2.8±0.2 | 2.4±0.1 |
| SQL Ctx Utility | 14.9±0.4 | 99.1±0.2 | 98.5±0.1 | 88.0±0.5 | 99.2±0.1 | 98.6±0.3 |
| GSM8k ASR | 1.5±0.2 | 3.3±0.4 | 2.0±0.5 | 1.8±0.3 | 2.9±0.2 | 1.7±0.4 |
| GSM8k Utility | 25.5±0.2 | 41.7±0.4 | 37.4±0.3 | 28.5±1.2 | 63.3±0.5 | 63.6±0.4 |

**THE CRUX — lowered, never zeroed.** **No defended configuration under attack reaches 0.0 anywhere in the paper.** Verified across the complete Table 2 and complete Table 3: Table 2's defended minimum is **1.0 ± 0**; Table 3's Constrained SFT ranges **1.5 ± 0.1 to 10.9 ± 2.8**. Prefilling bottoms out at 2.8%. **GCG — the optimization-based attack — falls only 36.5 → 18.4 and 65.6 → 19.0.** The authors' framing is directional, not terminal: the abstract says deepening *"can **often** meaningfully improve robustness against **some** common exploits"*; the paper calls its defense *"an additional layer of defense."* The title's comparative — "*more than* just a few tokens deep" — asserts a direction of travel, not an endpoint.

### Assumptions (scope limits)

- **Open-weight models only**, 7B-scale, circa 2024 (Llama-2-7B base/chat, Gemma-7B, Gemma-1.1-7B-IT). No API-only model, no frontier-scale model, no agentic system is tested. *(Correction: the prior report's "open-weight/API" was unsupported — prefilling and constrained fine-tuning require weight/logit access.)*
- Threat model is an **enumerated, known attack set**: GCG suffixes, prefilling, decoding-parameter exploits, fine-tuning attacks.
- The instrument throughout is **ASR on harmfulness benchmarks** (HEx-PHI, AdvBench, MaliciousInstruct) — i.e. **behavioral evaluation**.
- Implicit cost model is **chatbot misuse**: bounded, per-incident, recoverable. Nothing concerns unbounded or irreversible harm.
- Attacks are **static, not re-optimized against the defense**.
- Non-zero ASR is treated as an **engineering target**, never as a bar to deployment.

### What it does NOT claim

- **No defense reaching zero ASR.** No such claim, no such number under attack.
- **Not that the residue is irreducible.** The normative thrust is the opposite. Citing it for "epsilon is irreducible" **inverts the authors' thesis**.
- **Not that shallowness is the only vulnerability** — §2.3 hedges: shallow alignment "**May** Be A Source of Many Safety Vulnerabilities."
- **No robustness against adaptive attacks** tailored to the deepened model.
- **No general defense** — the constrained objective targets fine-tuning attacks; augmentation targets inference-stage exploits.
- **No certification or guarantee of absence.** All robustness results are empirical measurements — benchmark tables, not existence theorems and not rate bounds. *(Note: the prior report's stronger claim "there is no theorem" is NOT verified — Appendix D, "Interpretation of Our Constrained Fine-tuning Objective," was never read. Do not assert the universal.)*
- **Nothing about weapons, LAWS, military systems, or unbounded-cost decisions.** Zero domain overlap with Premise B.

### The authors' own stated limitations

**No dedicated Limitations section** — independently confirmed this session. Structure is §§1–6 plus Appendices A–D. *Residual risk: an unnumbered ethics/reproducibility statement might not surface in extraction, and the camera-ready was not read.*

Caveats are scattered inline:
- **§3.2, verbatim (double-attested across sessions):** *"Yet, the augmented model is still vulnerable to adversarial fine-tuning attacks where the datasets are harmful"* — the prior report's continuation (*"but the ASR is still lower than the initial model in multiple cases"*) is single-attested; the core clause is confirmed.
- **Abstract:** deepening *"can often meaningfully improve robustness against some common exploits."*
- **§2.2:** *"it is unnatural for humans to write any kind of examples that refuse a request after providing a harmful prefix."*
- *(The prior report's §6 Conclusion "verbatim" quote is REMOVED — single extraction, never cross-checked, possible paraphrase. Do not print.)*

The paper is candid but **unsystematic** about its limits — worth noting, since a hostile reviewer of *our* paper can observe that we lean on scattered hedges rather than an authors' limitations statement.

### Hostile-reviewer assessment

**Our response — "a lowered floor is not a proven zero, and unbounded-cost domains require the latter."**

**First clause: yes, strongly supported** — by the paper's own numbers and hedges. Qi et al. never claim zero and certify nothing; their best-in-class deepening leaves 18.4 ± 4.2% GCG ASR.

**Second clause: this is where we get hit, and Qi et al. cannot save us.** "Unbounded-cost domains require a proven zero" is *our normative premise*, on which this paper has no bearing. The reviewer's move: *if you demand a proven zero, you prove too much — no human-operated weapon system has a proven-zero error rate either, so your criterion fails to discriminate against LAWS specifically.* **Premise B (unbounded + irreversible + minimax) must carry that — not Qi et al.** Do not let the Qi citation appear to do work it cannot do.

**The strongest movable-floor objection this paper supports against us:**

> *Qi et al. is an existence proof that today's epsilon is an artifact of a specific, identified, remediable engineering shortcut — not a law of nature. Once the structural cause was named, prefilling ASR fell 42.1% → 2.8% and the decoding-parameter exploit fell 84.3% → 1.0%, at negligible utility cost. You cannot infer from "the floor is currently non-zero" to "no lower bound can be certified below any acceptable threshold." Your bridge silently converts a 2024 snapshot into an invariant. Worse: you are citing an optimistic, constructive paper — whose thesis is that alignment SHOULD be made deeper — as a pillar of an abstention argument its authors would not endorse.*

**How much is right? Substantially, and we must concede it in our own text:**
- It **correctly refutes** any claim that epsilon is *constant* or *irreducible in principle*. **Premise A must be stated as "no certified zero at any given time," never as "epsilon is irreducible."** If v4 implies the latter anywhere, this source falsifies it — **a required edit**.
- It **correctly** notes the authors' normative direction runs against ours. **Say so before a reviewer finds it.**

**What it does not refute — three clean counters (each verified):**
1. **No cell reaches zero under any attack under any defense.** A movable floor that never touches zero is still a floor. The objection establishes epsilon is a *function of alignment depth*; not that the function has a reachable root.
2. **Movement is grossly uneven.** 15x against non-adaptive prefilling; 2.0x against GCG. A deployer's extrapolation from "we cut prefilling 15x" to "we can cut adversarial elicitation to acceptable levels" is contradicted by the GCG column *of the same table*. **Stated carefully:** adaptivity is not the only driver — the *same* decoding-parameter attack falls 84x on MaliciousInstruct but 4.9x on HEx-PHI, a 17-fold swing from benchmark choice alone. The honest characterization is a **selectively movable floor**, whose selectivity is governed by attack type *and* choice of benchmark — both of which the deployer selects. That is worse for the deployer, not better.
3. **The decisive one: Qi et al. operates entirely *inside* Premise C, so it cannot be a counterexample to it.** Every number is a behavioral measurement against an enumerated attack class. "2.8%" is a *measurement*, not a *bound*. The paper lowers the floor **as measured by the very paradigm Premise C says cannot certify absence.** The measurement improved; the certification problem is untouched. Qi et al. is not evidence against Premise C — it is a demonstration of how much room Premise C leaves.

**The eval-relativity contrast (corrected and strengthened).** The prior report built this on a single number (Table 3, Identity Shifting, Initial = 0 ± 0) and called it "Premise C rendered as a single number." Both the framing and the instance were weak. A reviewer answers: *that 0 is a pre-attack baseline — the eval did not fail, it correctly measured a model no attack had been applied to.* The version that survives uses **one model across three evals**: the same aligned Llama-2-7B-Chat measures **0 ± 0 across all six refusal-prefix conditions** (Table 1, aligned row), **0 ± 0 and 1.5 ± 0.2 pre-attack** (Table 3), and **42.1–84.3% under prefilling, GCG, and decoding-parameter attacks** (Table 2). The zero is a property of *the conditions tested*, not of the model. State it as **"zero under the conditions tested"** — never "the eval was wrong" — and present it as **evidence for** Premise C, not as Premise C itself.

### Honest, defensible use — cite for:

1. **Forcing the correct, weaker, survivable Premise A** ("no certified zero," not "irreducible") — and cite Qi et al. *as the reason* we state it that way. Converts the counter-argument into evidence of our discipline. **Required edit.**
2. **The GCG residual 18.4 ± 4.2 (HEx-PHI) / 19.0 ± 2.9 (AdvBench)** — a structurally-diagnosed, award-winning deepening leaves ~1-in-5 against optimization-based attack. **Scope on its face:** 7B open-weight chat model, 2024, static attacks, behavioral ASR.
3. **The one-model-three-evals contrast above**, for Premise C — as evidence for, phrased as "zero under the conditions tested."
4. **The domain distinction against NIST** — Qi et al. is *itself* a monitor-and-update paper: diagnose, deepen, re-measure, ship. Its implicit cost model is chatbot misuse: bounded, per-incident, recoverable. **That is exactly the domain where monitor-and-update is rational, and we should say so approvingly.** Our claim is not that Qi et al. are wrong; it is that their cost model does not transfer. **Do not dispute their results — dispute the transfer.** The cleanest place in the supplement to demonstrate the domain distinction on a friendly, high-status example.

### Do NOT cite for

"Alignment cannot be deepened"; "epsilon is irreducible"; "shallowness is the only vulnerability"; "there is no theorem in the paper"; or as any support for abstention. Each would be an overstatement the authors would repudiate, and rule 4 forbids each.

### Verdict on the prior sweep

**COULD NOT VERIFY** — the sweep's text was never supplied. The role assignment ("the movable-floor objection — a counter-argument we MUST engage") is **CONFIRMED**: this paper genuinely and strongly supports a movable-floor objection, correctly identified, and it must be engaged. Refinement: **"movable floor" understates it** — the floor is movable *very unevenly*, and the selectivity runs against the deployer. **Correction to any sweep asserting "no ASR reaches zero": slightly wrong.** Zeros do appear — nine in Table 1's aligned rows, two in Table 3 (Llama *and* Gemma Identity Shifting Initial) — but all are **undefended models under pre-attack or refusal-prefix conditions**, never a defended floor under attack. The precise claim is: **no defended configuration under attack reaches zero.** Getting this right matters twice — it is both the honest statement and, via eval-relativity, the more useful one.

### Confidence

**High — multiply verified across independent sessions:** citation (title, 8 authors, abstract, arXiv ID, v1-only, categories); ICLR 2025 Outstanding Paper Award; **all 8 Table 2 columns** (three concordant literal extractions, one known-bad outlier explained); **full Table 3, all 10 rows, both models**; **full Table 1, all 4 rows**; Table 1/2 and Figure 1/2 captions; §3.2 "still vulnerable" clause; absence of a Limitations section; **the crux (lowering, never zeroing)** — the most robust finding in this record, supported by the complete tables, the authors' hedges ("often," "some," "additional layer"), §3.2, and the title's comparative.

**Corrections applied to the prior report:** (1) Figure 2 removed as an "independent line" — it plots the same model/dataset/attack as Table 2's Initial row, so the prior report's confidence boost from their "concordance" was circular and is withdrawn (the values are correct on independent grounds); (2) "one 0.0" corrected to eleven, with Table 1's aligned rows added as the stronger instance; (3) "there is no theorem" downgraded to "no certification or guarantee of absence" (Appendix D unread); (4) Table 3 completed, including the worst defended residual, 10.9 ± 2.8; (5) the adaptivity story qualified by the decoding-params benchmark swing; (6) the Premise C framing reformulated off the pre-attack baseline; (7) "API" removed from scope; (8) the unverified §6 quote removed.

**Known gap — not filled from memory:** OpenReview `forum?id=6Mxhg9PtDE` remains unread (bot wall). **No reviewer criticisms, no rebuttals, no camera-ready.** arXiv has v1 (June 2024) only; the paper was published at ICLR 2025, so **an unexamined preprint→camera-ready delta remains**. If the camera-ready added a Limitations section or revised numbers, this record would not know. This is the one substantive hole. Retrieving the ICLR PDF by a non-blocked route would close it.

**From training knowledge, NOT verified this session:** nothing in this record is load-bearing on training knowledge. HEx-PHI/AdvBench/MaliciousInstruct construction, GCG mechanics, and reviewer discussion are deliberately not supplied from memory. Where a fetch was missing, the gap is labeled, not filled.

**Analytical content** (the hostile-reviewer section, the domain distinction, the eval-relativity contrast, the "selectively movable floor" refinement) is reasoning over fetched material, **not claims found in the source**. The authors assert none of it and would likely contest the framing.

---

## 検証段が発見した過大主張・誤り（7件）

- CIRCULAR CONFIDENCE (the project's documented failure mode, operating inside the report). The report lists Figure 2 as one of 'three independent lines' of evidence and writes: "Figure 2's ~42/51/56/57 independently concords with Table 2's Initial row, which raises my confidence in both." It is not independent. Figure 2's caption is 'ASR vs. Number of Prefilled Harmful Tokens ... on Harmful HEx-PHI'; Table 2's caption is 'ASR on Llama-2-7B-Chat (Initial) ... Prefilling attacks are evaluated using Harmful HEx-PHI.' Same model, same dataset, same attack — Figure 2's prefilling curve IS Table 2's Initial row plotted. The report drew a confidence boost from a source agreeing with itself. (The values are nonetheless correct — I confirmed them by independent literal extraction — so the conclusion survives; the reasoning that reached it does not.)

- FACTUAL ERROR, against the report's own interest. The report states 'One 0.0 does appear' and builds its Premise C recommendation on it (Table 3, Identity Shifting, Initial = 0 ± 0). There are at least eleven. Table 3 has TWO (Llama AND Gemma Identity Shifting Initial both 0 ± 0). More importantly the report never extracted Table 1's aligned rows, which are the far better instance: Llama-2-7B Aligned scores 0, 0±0, 0±0, 0±0, 0±0, 0±0 across all six refusal-prefix conditions, and Gemma-7B Aligned scores 2.1±0.2 then 0±0 five times. The report's 'gift' is real but it found the weakest instance of it.

- UNVERIFIED UNIVERSAL. 'It does not offer any certification, bound, or guarantee. There is no theorem.' The report's own TOC extraction lists Appendix D, 'Interpretation of Our Constrained Fine-tuning Objective' — plausibly containing formal material — and the report never read it. The claim needed for our argument is weaker and fully supported: no certification or guarantee of ABSENCE is offered, and every robustness result is an empirical measurement. 'There is no theorem' is a universal negative asserted over an appendix nobody opened.

- OVER-TIDIED CAUSAL STORY. The report's headline refinement — 'the closer the attack is to an adaptive adversary, the less the fix helps' (prefilling 15x, GCG ~2x) — is contradicted within the same table by the decoding-parameters row: the SAME attack falls 84.3->1.0 (84x) on MaliciousInstruct but 54.9->11.3 (4.9x) on HEx-PHI. A 17-fold swing in reduction factor driven by benchmark choice, not attack adaptivity. The selectivity is real; the adaptivity explanation is not the only or best one. (This complication independently strengthens the eval-relativity point, so correcting it costs us nothing.)

- OVERHEATED FRAMING. 'This is Premise C rendered as a single number' and 'I would build the Premise C paragraph of Supplement II around this number.' Premise C is a claim about what proof cannot do; Table 3's 0±0 is one measurement under one condition. It illustrates that a measured zero does not survive a change of conditions — evidence FOR Premise C, not a rendering OF it. Building a paragraph on a pre-attack baseline is also the version a hostile reviewer most easily knocks down (see the defensible-use verdict).

- MINOR SCOPE INFLATION. 'Scope is open-weight/API chat LLMs.' No API-only model is tested. All experiments are open-weight (Llama-2-7B base/chat, Gemma-7B, Gemma-1.1-7B-IT); prefilling and constrained fine-tuning require weight or logit access that the API-model framing implies but the paper does not test.

- INCOMPLETE TABLE 3, omitting the worst defended residual. The report prints only 2 of 10 rows and only the Llama columns. It omits Backdoor Poisoning ASR (w/ trigger), Constrained SFT = 10.9 ± 2.8 — the highest defended residual anywhere in Table 3, and a number that HELPS our argument. Not hope-directed bias (it cuts against the report's own tidiness), but the log must be complete.


## 取得honesty監査（6件）

- NONE MATERIAL — and this is the report's strongest dimension. Every claim I could test against source was genuinely in the fetched material. There are no claims that could only come from full text where only an abstract was reached: the arXiv HTML full text is genuinely retrievable (I retrieved it twice myself, independently), and the tables, the §3.2 quote, and the Limitations absence all check out.

- VINDICATED SELF-DISCLOSURE. The report volunteered that its fetch 2 scrambled Table 2's cells, discarded that fetch as an outlier, resolved by literal re-extraction, and flagged the values as high-but-not-final pending an eyeball against the PDF. My independent literal extraction reproduces all 8 Table 2 columns exactly as the report settled on them. The report's caution was well-founded and its resolution was correct — an agent that hid the inconsistency would have produced the same numbers with less warrant.

- HONEST FAILURE REPORTING CONFIRMED. The OpenReview bot-wall failure is reported as a gap and not backfilled — I see no reviewer comments, rebuttals, or camera-ready details anywhere in the report, consistent with that disclosure. The v2=404 claim is independently corroborated: arXiv's submission history lists [v1] Mon, 10 Jun 2024 00:35:23 UTC (1,190 KB) and nothing else.

- ONE UNRE-VERIFIED QUOTE, correctly self-flagged. The report's §6 Conclusion 'verbatim' quote was labeled by the report itself as single-extraction and not-to-be-printed-as-quotation. I did not re-verify it either. It stays out of the record — I have removed it rather than carry it.

- ONE QUOTE PARTIALLY CONFIRMED. My extraction returns the §3.2 core clause verbatim — 'Yet, the augmented model is still vulnerable to adversarial fine-tuning attacks where the datasets are harmful' — matching the report. The report's continuation ('but the ASR is still lower than the initial model in multiple cases') was not returned by my targeted prompt and remains single-attested; the load-bearing clause is now double-attested.

- The report's disclosure that WebFetch is itself a summarizing pipeline — the instrument class rule 1 distrusts — is correct and applies equally to MY verification. My extractions are the same instrument. What raises confidence here is not the instrument but concordance across independent sessions with different prompts: Table 2 now agrees 3-of-4 with the one known-bad outlier explained.


## 引用可能性の裁定

DEFENSIBLE WITH CORRECTIONS — 3 of 4 uses survive hostile review as written; the 4th (the Premise C 'gift') survives only if reformulated, and is currently vulnerable in exactly the way the report failed to anticipate. Use 1 (state Premise A as "no certified zero," never "epsilon is irreducible," and cite Qi et al. AS THE REASON we state it that way) is fully supported and is a required edit to v4, not optional — this source falsifies any "irreducible" phrasing. Use 2 (GCG residual 18.4 +/- 4.2 HEx-PHI, 19.0 +/- 2.9 AdvBench) is verified exactly and defensible, provided it is scoped on its face: a 7B open-weight chat model, 2024, static non-adaptive attacks, behavioral ASR. Use 4 (the domain distinction against NIST — Qi et al. is itself a monitor-and-update paper whose implicit cost model is bounded chatbot misuse; concede their results, dispute only the transfer) is the strongest and cleanest item, and is analysis over the source rather than a claim attributed to it, which is the correct posture. Use 3 is where a hostile reviewer lands a hit the report did not see: Table 3's Identity Shifting Initial = 0 +/- 0 is a PRE-ATTACK baseline, and a reviewer will say the eval did not fail — it correctly measured a model to which no attack had yet been applied, so the "0" is not evidence that behavioral evaluation cannot detect a residue. The reformulation that survives, and is stronger: the SAME Llama-2-7B-Chat is measured at 0 +/- 0 across all six refusal-prefix conditions (Table 1, aligned row), at 0 +/- 0 and 1.5 +/- 0.2 pre-attack (Table 3), and at 42.1-84.3% under prefilling, GCG, and decoding-parameter attacks (Table 2). One model, three evals, and the zero is a property of the conditions tested rather than of the model. That is the defensible claim — "zero under the conditions tested," never "the eval was wrong" — and it must be presented as evidence FOR Premise C, not as Premise C itself. The report's three clean counters otherwise hold and I verified each: no defended configuration under attack reaches zero anywhere in the paper (Table 2 defended minimum 1.0 +/- 0; Table 3 Constrained SFT minimum 1.5 +/- 0.1, maximum 10.9 +/- 2.8); movement is grossly uneven; and Qi et al. operates entirely INSIDE Premise C's evaluation paradigm, so it cannot be a counterexample to it — "2.8%" is a measurement, not a bound. The report's concession discipline (naming that the authors' normative direction runs opposite to ours, in our own text, before a reviewer finds it) is correct and should be preserved verbatim in v4.
