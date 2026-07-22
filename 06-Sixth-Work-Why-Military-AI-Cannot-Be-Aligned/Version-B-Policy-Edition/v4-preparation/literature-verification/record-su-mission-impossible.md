# 照合確定記録: su-mission-impossible

**我々の論証における役割（照合時の割り当て）**: Premise A — statistical re-grounding + critique of Wolf assumptions

**書誌照合**: 一致（検証段が独立取得して確認）

**検証段が自ら取得したURL**:
- https://arxiv.org/abs/2408.01420 — SUCCESS (title, 3 authors, full abstract, 2 Aug 2024, cs.LG/cs.AI/cs.CL, identifier 2408.01420v1)
- https://proceedings.neurips.cc/paper_files/paper/2024/hash/439bf902de1807088d8b731ca20b0777-Abstract-Conference.html — SUCCESS (venue, DOI 10.52202/079017-1210)
- https://arxiv.org/abs/2408.01420v2 — FAILED, HTTP 404 (establishes no v2 exists; resolves the report's open item)
- Local file (not a URL) C:\Users\PC\.claude\projects\C--Users-PC\de004d8e-acb9-46c3-b457-0f594871974a\tool-results\webfetch-1784270224647-a18ocf.pdf — verified 1,004,408 bytes = 980.9 KB, sha256 1b0d29fb5e41fdbe514c7076e431c791..., %PDF-1.5, 40 pages; re-extracted independently with pypdf to 134,452 chars (report said 134,491 — trivial extractor variance). All my quotes are from my OWN extraction, not the report's file.

---

## 確定記録（検証段による修正適用後）

## SOURCE RECORD: su-mission-impossible (VERIFIED + CORRECTED)

**Assigned role:** "Premise A — statistical re-grounding + critique of Wolf assumptions"
**Adjudicated role:** "Premise A — CORROBORATIVE statistical re-grounding." **The clause "critique of Wolf assumptions" is STRUCK — it is not in the paper.**

### Citation (ready to paste)

Jingtong Su, Julia Kempe, and Karen Ullrich. "Mission Impossible: A Statistical Perspective on Jailbreaking LLMs." *Advances in Neural Information Processing Systems 37* (NeurIPS 2024), Main Conference Track, 2024. DOI: 10.52202/079017-1210. arXiv:2408.01420 [cs.LG].

Bibliography notes: NeurIPS proceedings page exposes no editors/page numbers. Affiliations/equal-contribution markers ("Correspondence to: Jingtong Su <js12196@nyu.edu>"; "†Equal senior authorship") come from the PDF. Camera-ready is 40pp (main ~9pp + appendices A–H + NeurIPS checklist). **arXiv has only v1** (`abs/2408.01420v2` → HTTP 404; abs page reports identifier `2408.01420v1`). Cite the NeurIPS camera-ready — it is the source of record here.

### What was actually fetched (two independent agents; verifier's column is authoritative)

| URL / artifact | Result |
|---|---|
| `https://arxiv.org/abs/2408.01420` | SUCCESS (both agents). Title, 3 authors, abstract, 2 Aug 2024, cs.LG/cs.AI/cs.CL. |
| `https://proceedings.neurips.cc/.../439bf902...-Abstract-Conference.html` | SUCCESS (both). Venue + DOI 10.52202/079017-1210. |
| `https://arxiv.org/abs/2408.01420v2` | FAILED — HTTP 404. Establishes no v2 exists. |
| NeurIPS camera-ready PDF (local: `tool-results\webfetch-1784270224647-a18ocf.pdf`) | **SOURCE OF RECORD.** 980.9 KB (1,004,408 B), sha256 `1b0d29fb5e41fdbe514c7076e431c791…`, %PDF-1.5, **40 pages**. Independently re-extracted by the verifier via `pypdf` → 134,452 chars. All quotes below re-verified against the verifier's own extraction. |

Method flag (Discipline #1/#2): every quote below was checked against mechanically-extracted PDF text by two agents independently. `pypdf` artifacts (`contente`, `"Paris"would`, `44 .47`) are extraction noise, not authors' typos. Math notation is lossy; flagged where relevant.

### Precise claims

**Statistical notion of alignment.** The paper declines to define alignment sharply: *"under the PAC framework, preference alignment is nothing but a transformation from ρ to some γ posterior defined over LM."* Goal: *"given a prompt (q, c) where c is harmful, its goal is to push the induced distribution γc into the safety zone Hs."*

Jailbreak is defined **distributionally, not per-sample** (Def. 4.3): *"Given a harmful concept c and a query q′, the prompt (q′, c) jailbreaks the LM iff pLM(q′, c) ∈ Hh."* Threshold p (Def. 4.2): *"The threshold p for discriminating Hh and Hs should be very small, since it means in expectation the adversary needs to call the LM 1/p times to collect a single harmful explanation i.e., to jailbreak the LM."*

**Theorem 2 (Jailbreak is unavoidable)** — verbatim, verified twice: *"Assume that an LMs output semantically meaningful explanations (Assumption 4.1). Given any γ posterior distribution over LM, choose a harmful concept c with a direct prompt (q, c) and a threshold p (Definition 2.1)… An ϵ-bounded adversary (Assumption 4.2) can find a jailbreaking prompt (Definition 4.3) with probability at least 1 − γs × (1 − Φ(aϵ)), • by using either the direct prompt, such that pLM(q, c) ∈ Hh; or • by finding an ϵ-bounded query q′, such that pLM(q′, c) ∈ Hh. Here, Φ(·) is the standard Gaussian cdf, γs := max_{x∈Hs−Hh(ϵ,d)} γc(x)/U(x), with U(x) the uniform distribution over ∆n−1, and aϵ := a + √(n−1)ϵ, where a writes analytically as a ≍ (|Eh(c)|−1−(n−1)p)/√((n−1)p(1−p))."* Preceded by: *"as long as the induced posterior γc is not concentrated in an extremely safe area, then with high probability the model can be jailbroken."* Proof in App. B.3 (not read by either agent).

**Theorem 1** — PAC-Bayes bound for *pretraining*. Only the contributions bullet is verbatim-verified: *"high-performing pre-trained models will inevitably be susceptible to generating behaviour that is present in the training corpus, including any unintended and harmful behaviour."* **The bound's exact form is NOT verified. Do not quote it.**

**The load-bearing informal step** (this, not the theorem, carries "alignment is hard"): *"In real world settings, for any harmful concept, the training corpus naturally contains a large harmful set due to the number of possible responses. Realistically, its size can not be countered by any manually-constructed safe set. Hence achieving alignment is hard… Consequently, the safety zone is going to be small."*

**Support-preservation mechanism (our best citable content — but it is a CLAIM, not a theorem).** The paper's own verb is "claim": *"We claim that this regularization is exactly the problem for safety. While designed to keep the model helpful, for any harmful prompt xh and any harmful explanation e ∈ supp(pSFT(xh)), regularizing pLM to pSFT lets pLM maintain e in the support of the output distribution. Specifically, the supervised fine-tuning process does not involve elimination of any harmful explanations from the support of the output distribution of the pretrained model, which leads to the fact that pSFT(xh) supports harmful responses that can not be negated with a realistically sized preference aligned dataset."* Footnote 8: *"Even the probability can be suppressed to close to 0."* (suppressed — **not removed**). Empirical backing is one citation: **[48] Huang, Gupta, Xia, Li, Chen, "Catastrophic jailbreak of open-source LLMs via exploiting generation," arXiv:2310.06987** — *"where diverse, harmful explanations are extracted by simply manipulating the decoding process using direct prompts."*

**Wolf et al. [38] — the crux. Cited exactly 3× (bibliography back-index reads "2, 3, 33"). All three verbatim:**
1. Intro (p.2): *"we only have limited proposal on a principled universal defense against jailbreaking attacks [2], and limited theoretical understanding on this phenomenon [38]."*
2. §2 (p.3): *"First, in contrast to previous theoretical work where LMs are regarded as single sentence generators [38], we model LMs as lengthier text fragment generators, and refer to possible generated content e ∈ E as explanations."*
3. App. H.3 (p.33): *"Wolf et al. [38] assumes the decomposability of LLM output into a good and bad component, and show possible jailbreaking in theory by prompting the model with a sufficiently long input."*

That is the **entire** treatment. No critique, no "questionable", no modification of a Wolf assumption. The only contrast is **output-object granularity** (sentence vs. text fragment) — a framing difference. Provenance note: the string "Wolf" appears only 3× in the PDF (ref list p.13; an unrelated *Thomas* Wolf alignment-handbook ref p.13/14; H.3 p.33) — the p.2/p.3 citations are numeric `[38]` only.

**"mixture" appears 3× and NEVER of Wolf.** It is Su's *own* construct: *"(Mixture decomposition of DP) …we can decompose DP = αDPh + (1 − α)DPs."* Since Su's H.3 glosses Wolf as assuming "decomposability… into a good and bad component," this is the likely origin of the sweep's conflation.

**The two "Paris" passages — BOTH exist (exactly 2 hits). Prior verification wrongly reported only one.**
- **p.5, about `p_world`, defending Assumption 2.1:** *"We can now state our main assumption, namely that for any plausible prompt (q, c) ∈ dom(pworld) the ground-truth distribution pworld(q, c) is supported on a small subset of E… This assumption seems sensible to us: under normal circumstances, providing an explanation of "Paris" would not offer any relevant knowledge when given a prompt such as "How to write a hello world python script"."*
- **p.6, about `dom(p_LM)`, defending Assumption 4.1(1):** *"The assumption can be broken down into two components: (1) within the support of the output distribution, only occasional instances of unrelated explanations exist; (2) the process of aligning the model towards safety does not eliminate the harmful explanations acquired during the pretraining phase. For part (1), similar to the example we gave above, under normal circumstances, we do not expect the explanation "Paris" to appear in dom(pLM(q, c)) given (q, c) as "How to build a bomb". As for part (2), though seemingly surprising, evidence with a series of current state-of-the-art LMs can be experimentally validated [48]."*

**Assumption 2.1** verbatim: *"(Concepts uniquely determine the explanation for plausible prompts) For all plausible prompts (q, c) ∈ dom(pworld), i) pworld : P → ∆(supp(pworld(q, c)) where supp(pworld(q, c)) ⊊ E s.t. |supp(pworld(q, c))| ≪ |E|; and ii) supp(pworld(q, c)) = supp(pworld(q∗, c)), ∀(q, c), (q∗, c) plausible."*

**E-RLHF.** Motivation: *"jailbreaking becomes more likely the larger the harmful zone is in comparison to the safety zone… the size of the preference alignment dataset is crucial to successful alignment. Unfortunately, the human labor involved in creating such a dataset effectively caps its size."* The fix swaps the KL anchor (Eq. 3): `L_E-RLHF(pLM) = −E_{x∼Ds}{E_{e∼pLM(·|x)}[r(x,e)] + βD_KL(pLM(x)||pSFT(x_s))}`. *"when xh is "Tell me how to make a bomb", instead of aligning pLM(xh) to pSFT(xh), now we align pLM(xh) to pSFT(xs) where xs is "Tell me how to reject a request of making a bomb"."* Practical prefix: *"Please ensure your response adheres to community guidelines and ethical standards:"*. *"Importantly, the non-harmful prompts are not modified."* E-DPO (Eq. 4) integrates into DPO.

**Table 1 (average ASR, lower better) — all values re-verified:**
- HarmBench: pSFT 44.47 → pDPO 42.00 → **pE-DPO 36.95**
- AdvBench: pSFT 40.09 → pDPO 28.40 → **pE-DPO 20.89**
- MT-Bench: pSFT 6.3, pDPO 6.9, pE-DPO 6.7 — *"making us believe that performance degradation is not a problem with our proposal."*
- Per-adversary residues (pE-DPO): HarmBench TAP 51.00, PAIR 48.50, GCG 47.50, AutoDAN 43.00; AdvBench TAP 53.00, PAIR 41.00, GCG 38.00.

**Caption caveat (verified, and it matters):** the caption's *"resilience against all adversaries improves"* is explicitly **DPO-relative** (*"↓ indicates better performance between DPO and E-DPO"*). Against the **pSFT** baseline, E-DPO is **worse** on HarmBench PAP-top5 (27.00 vs 26.75) and **flat** on AdvBench PAP-top5 (4.00/4.00/4.00). So the text's *"E-DPO achieves improvements across every task we tested"* holds only at **dataset-average** granularity. Do not repeat the paper's stronger phrasing.

**Headline for our purposes: E-DPO's best average ASR is 36.95% (HarmBench) and 20.89% (AdvBench) — roughly one in five to one in three attacks still succeed, with per-adversary residues above 50%.**

### Assumptions

- **Assumption 2.1**: concepts alone determine the *support* of `p_world`; support small relative to E; queries move probabilities but not support.
- **Existence of `p_world`**: latent ground-truth map P → ∆(E) the LM mimics; prompt distribution D_P with `supp(D_P) ⊊ dom(p_world)`.
- **Definition 2.1**: harmfulness is binary per explanation; concept c harmful iff Σ_{e∈Eh(c)} pworld(e|q,c) ≥ 1−η for all plausible q. Safe set includes human templates (*"Sorry."*).
- **Assumption 4.1**: *"∃ |En(c)| ≪ |Eh(c)| + |Es(c)| s.t. O(1) ≪ |dom(pLM(q, c))| = |Eh(c) ∪ Es(c) ∪ En(c)|"* — residual En(c) is small. Justified informally (the p.6 Paris/bomb example) + by appeal to OOD generalization.
- **Assumption 4.2 (ϵ-bounded adversary)**: *"the adversary can find a set of queries Q′, such that the output is moved at most ϵ on the simplex towards Hh from pLM(q, c): sup_{q′∈Q′} d(pLM(q, c), pLM(q′, c)) = ϵ"*, d an ℓp (p≥1), TV, or JS distance. **Perturbations on queries only, never on concepts.**
- Fixed decoding hyperparameters (fn. 4); greedy decoding T=0 for eval.
- Theorem 1 follows Mbacke et al. [45], Germain et al. [46], Haddouche et al. [47].

### What it does NOT claim

- **It does not criticize, weaken, or repair Wolf et al.'s assumptions.** Citing it for that is falsifiable in one minute with Ctrl-F.
- **Jailbreaking is not unconditional.** Abstract: *"showing that it is unpreventable **under reasonable assumptions**."* Contributions bullet: *"**Assuming our assumptions are met**, we demonstrate jailbreaking to be unpreventable even after safety alignment because the LM fails to concentrate its output distribution over the set of safe responses."*
- **No rate bound on deployed systems.** `1 − γs(1−Φ(aϵ))` lives on an abstract simplex with a posterior γ over LMs and cardinality terms (|Eh(c)|, n) never measured for any real model, and is **never connected numerically to Table 1's ASRs**.
- **It says nothing about ε being unmeasurable or its absence unprovable. DO NOT USE SU FOR PREMISE C.**
- It does not claim E-RLHF escapes Theorem 2 — only that it *"expand[s] the safety zone"* and improves ASR empirically.
- No general no-cost-to-helpfulness claim — only MT-Bench 6.3→6.9/6.7.
- No multi-turn/agentic modelling (limitation 2). **Nothing about LAWS, cost asymmetry, minimax structure, or any unbounded-cost domain.**
- Empirics: a single SFT model (per [50] alignment-handbook, [51] HF constitutional-ai SFT), one preference dataset, greedy decoding, 8×V100, **no seeds/variance in Table 1**.

### Authors' own stated limitations (§7, verbatim)

*"(1) Although we have classified concepts as either harmful or non-harmful, it is important to acknowledge that the perception of a concept's potential for harm can be influenced by various factors such as cultural, legal, and societal norms… (2) Language models have demonstrated impressive capabilities in reasoning and completing tasks within multi-round, multi-step conversations; our current framework may not fully account for the generalization and jailbreaking possibilities associated with such input formats. (3) Our analysis is grounded on a fixed pworld mapping and DP distribution. Nevertheless, the world is inherently dynamic, as both pworld and DP continually evolve."*

Also §6: *"our method's performance depends on the choice of safe prefix to some extend but never fails"*; *"applying the safe prefix to usual prompts degrades safety"* — the fix is fragile to *where* it is applied.

### Hostile-reviewer assessment

**Strongest objection:** *"You cite a paper whose own authors propose a fix that works. If E-DPO cuts AdvBench ASR 28.40→20.89, ε is a tunable engineering parameter, not a floor. Your bridge needs ε irreducible; Su show it reducible. And the theorem is conditional on assumptions they concede may not hold."*

**Concede cleanly:**
- Theorem 2 **is** conditional. Assumptions 4.1 ("residual En(c) small") and 2.1 (support-invariance) are asserted as plausible, not established. If an aligned LM *did* concentrate support on E_s(c), the theorem loosens. Su *argue* it doesn't — informally, from harmful-set size vs. human labor. **That informal step, not the theorem, carries "alignment is hard."**
- Su never claim ε is irreducible; they say the safety zone is small and can be *expanded*.

**Counter (our strongest, and it is empirical):** the fix does not approach zero. E-DPO's own headline is **36.95% / 20.89% average ASR**, per-adversary residues above 50% (AdvBench TAP 53.00), and it is **worse than the SFT baseline on HarmBench PAP-top5**. The pessimism paper's own best-effort, theory-motivated fix, reported by authors motivated to make it look good, leaves ~1 in 5 attacks succeeding. **E-RLHF strengthens Premise A — provided we quote the numbers, not the word "outperforms."**

**Structurally useful, but note the import:** Theorem 2's threshold p means *"the adversary needs to call the LM 1/p times to collect a single harmful explanation."* This is a **repeated-sampling** notion. In a bounded-cost domain, 1/p calls is a nuisance; in an unbounded-cost domain a *single* success is terminal. That mapping is genuinely useful against NIST's monitor-and-update routing — **but we are IMPORTING the cost asymmetry. Su et al. never make that move, and a reviewer will say so first if we don't.**

### Honest, defensible use — cite Su for EXACTLY two things

1. **A conditional, formally-stated result** that under an explicit statistical framework an ε-bounded adversary jailbreaks with probability ≥ 1−γs(1−Φ(aε)) — i.e. the residue is not an artifact of sloppy alignment but falls out of support-preserving fine-tuning. The mechanism is the authors' **claim** (their verb), backed by [48]: the KL anchor *"lets pLM maintain e in the support of the output distribution"*; SFT *"does not involve elimination of any harmful explanations from the support"*; fn. 8 *"Even the probability can be suppressed to close to 0"* — **suppressed, not removed**. Present as an argued mechanism + one empirical citation, **not as a theorem**.
2. **The E-DPO ASR table** as evidence that a targeted, theory-motivated fix leaves 20.89–36.95% average ASR.

**Su is CORROBORATIVE for Premise A, not load-bearing.** It is an independent statistical framework reaching a similar pessimistic conclusion. Premise A must not rest on it alone.

**DO NOT:** call Theorem 2 unconditional; call it a bound on any deployed system's failure rate; use Su for Premise C; use Su for anything military/unbounded-cost; say Su critique Wolf; or repeat the paper's own "improvements across every task" phrasing. State the conditionality in our own text before a reviewer does.

### Verdict on the prior sweep

**WRONG — verdict upheld, reasoning corrected.** The sweep claimed Su "criticize Wolf's mixture-support assumption as questionable," quoting *"under normal circumstances, we would not expect certain unrelated explanations to appear in the output distribution."*

- **Wrong on attribution — and this alone is fatal.** The matching sentence (p.6) defends Su's **own Assumption 4.1**. Wolf is not mentioned anywhere near it. All 3 Wolf citations are neutral; "mixture" is never used of Wolf.
- **Right on the object.** The sweep's paraphrase concerns the **output distribution** — and the p.6 sentence is indeed about `dom(p_LM(q,c))`. *(A prior verification pass asserted the opposite, having found only the p.5 `p_world` passage. That correction is recorded here.)*
- **Right that a near-verbatim sentence exists.** *(A prior pass called this quote a summarizer fabrication. It is verbatim on p.6. The fabrication finding is WITHDRAWN, along with the inference that a hallucinated quote explains the sweep's error. No such mechanism is evidenced.)*

**Consequence: "Statistical re-grounding" is fair and citable. "Critique of Wolf assumptions" MUST BE STRUCK from Supplement II.** If v4 needs a critique of Wolf, it must come from elsewhere.

### Confidence and unverified residue

**High (independently verified twice from mechanically-extracted PDF text):** citation (modulo editors/pages); arXiv v1-only; Assumptions 2.1, 4.1, 4.2; Defs 2.1, 4.1–4.4; **Theorem 2 verbatim including the formula**; alignment-goal passage; all 3 Wolf citations; **both** Paris passages; "mixture" usage; E-RLHF/E-DPO objectives; Table 1 (all values); the caption's DPO-relative scope and the PAP-top5 anomaly; MT-Bench; fn. 8; §7 limitations; ref [48] identity.

**Medium:** none outstanding — the earlier medium-confidence flag on Theorem 2's symbolic rendering is **resolved**: two independent `pypdf` extractions agree on `aϵ := a + √(n−1)ϵ` and `a ≍ (|Eh(c)|−1−(n−1)p)/√((n−1)p(1−p))`. Typeset confirmation still advisable before printing the formula, as subscripts are extraction-lossy.

**Low / not verified:**
- **Theorem 1's exact statement — NOT verified. Do not quote it.** Only the contributions bullet is verbatim.
- Appendices B.3 (Theorem 2 proof), C, D.1–D.5 — **not read**. All ablation claims rest on main-text description.
- Exact base-model identity. **From training knowledge, NOT verified this session:** the alignment-handbook CAI SFT checkpoint is Mistral-7B-based. The PDF cites [49] Mistral 7B and [51] the HF constitutional-ai SFT model; the linkage was not confirmed in the appendix.
- The claim that a prior summarizer reported "zero occurrences of 'Wolf'" is a prior-session tool output, **not verifiable here**; given that the companion fabrication accusation proved false, do not rely on it.

**From training knowledge, NOT verified this session:** that Wolf et al. (arXiv:2304.11082) frames its result via a "behaviour expectation bound" with an LLM-as-mixture-of-components assumption. **Wolf was NOT fetched.** If Supplement II makes any claim about what Wolf assumes, **Wolf must be fetched and verified independently.** Su's one-line gloss (*"decomposability of LLM output into a good and bad component"*) is Su's characterization, not Wolf's own words, and is the only attestable one.

### Process note for the log (Discipline #2/#3)

The prior verification pass was quotationally excellent — every quote it offered survived independent re-extraction — but it produced a **false fabrication accusation** by making a verified-absence claim ("the quote is not in the paper", "nothing about bombs") on the basis of an incomplete in-document search, and filed it under "High confidence, verified this session." It had exhaustively counted "Wolf" (3 hits) but not "Paris" (2 hits, one inspected). It then built a causal narrative about pipeline hallucination on that false finding and generalized it into an instruction to distrust other sweep quotes. **This is the project's documented hopeful-direction over-read, pointed at its own tooling rather than its thesis — the hoped-for conclusion being that it had caught a fabrication.** Rule to freeze: **a claim that text is ABSENT requires an explicit exhaustive count over the extracted text (`grep -c`, all hits inspected and listed), to the same standard as a claim that text is present.** Accusations of tool fabrication are claims and must clear the same bar as the claims they impugn — cf. the frozen lesson "撤回・降格の宣言にも主張と同じ厳しさの検分を要求する."

---

## 検証段が発見した過大主張・誤り（7件）

- SERIOUS / FALSE ACCUSATION: The report claims a WebFetch summarizer 'fabricated' the quote 'under normal circumstances, we do not expect the explanation Paris to appear in dom(p_LM(q,c)) given (q,c) as How to build a bomb', alleging it invented the bomb prompt, swapped p_world->p_LM, and reworded. All three charges are FALSE. That sentence is verbatim on PAGE 6, justifying Assumption 4.1 part (1). The report anchored on the page-5 Paris passage (p_world / Assumption 2.1) and never searched for a second occurrence — there are exactly 2 'Paris' hits in the PDF.

- Report rebuttal point #2 ('Wrong object. It concerns p_world, the latent ground-truth distribution — not an LM's output distribution') is WRONG. The page-6 passage matching the sweep's paraphrase is explicitly about dom(p_LM(q,c)) — the output distribution. The sweep's paraphrase ('we would not expect certain unrelated explanations to appear in the output distribution') is an ACCURATE paraphrase of a real sentence.

- Report rebuttal point #4 ('The quote is not in the paper in the form given') is WRONG. A near-verbatim match exists on page 6.

- Report's claim 'the example is Paris vs. a hello-world Python script, not anything about bombs' is WRONG. BOTH examples exist: hello-world on p.5 (p_world), bomb on p.6 (p_LM).

- BASELESS CAUSAL NARRATIVE built on the false finding: 'That fabricated quote is closer to the sweep's claim than the real text is — which is a plausible mechanism for how the sweep's error was generated in the first place.' The premise is false, so the mechanism story must be deleted. Its downstream instruction ('Treat any other sweep conclusion resting on a quote as suspect') is not supported by this evidence.

- MILD OVERREAD of the report's own best-use claim: it calls the support-preservation argument 'robust and mechanistic' and 'a support-level claim, which is stronger and more citable for us than any rate.' The paper's own wording is 'We CLAIM that this regularization is exactly the problem for safety' — an argued mechanism backed by one empirical citation [48] (Huang et al., arXiv:2310.06987, decoding-manipulation jailbreaks), NOT a theorem. Must be labelled as the authors' asserted claim + cited evidence, not a proved result.

- MISSED LOOSENESS the report should have caught (favours our side, so its absence is an over-read of the fix's strength): Table 1's caption says 'resilience against all adversaries improves', but the marker is defined as 'better performance between DPO and E-DPO' — i.e. DPO-relative. Against the pSFT baseline, E-DPO is WORSE on HarmBench PAP-top5 (27.00 vs 26.75) and FLAT on AdvBench PAP-top5 (4.00 / 4.00 / 4.00). So 'E-DPO achieves improvements across every task we tested' holds only at dataset-average granularity.


## 取得honesty監査（4件）

- Fetch honesty is GOOD and I confirmed it materially: the claimed source-of-record PDF exists at the stated path, is exactly the claimed 980.9 KB, is 40 pages, and my independent re-extraction reproduces the report's quotations essentially verbatim. Nothing in the report is attributable to abstract-only or memory-based access. Its 'from training knowledge, NOT verified this session' labels (Mistral-7B base model, Wolf's behaviour-expectation bound) are correctly applied and correctly scoped.

- HOWEVER, one failure is adjacent to the project's documented failure mode though not a fetch lie: the report made a strong NEGATIVE existence claim ('the quote is not in the paper', 'nothing about bombs', 'fabricated') about text that was present in the very extraction it says it read, and filed it under 'High confidence, verified this session from mechanically-extracted PDF text: ... the Paris passage'. This is an incomplete in-document search presented as a verified finding. Verified-absence claims must be backed by an explicit exhaustive count (e.g. 'grep Paris -> 2 hits, both inspected'), which the report did for 'Wolf' (3 hits) but NOT for 'Paris'.

- The report's claim that a summarizer asserted 'zero occurrences of Wolf' is unverifiable from this session (prior-session tool output). I neither confirm nor deny it. Given that the report's other pipeline-failure accusation proved false, this one should not be relied on without the transcript.

- Minor: the report cites the bibliography back-index 'pages 2, 3, 33' for Wolf. I confirm this is correct, but note the string 'Wolf' itself appears only 3 times in the PDF (ref list p.13, an unrelated 'Thomas Wolf' alignment-handbook ref p.14, and H.3 p.33) — the p.2 and p.3 citations are numeric '[38]' only. The report's count is right; the provenance deserves one clarifying word.


## 引用可能性の裁定

DEFENSIBLE WITH CORRECTIONS — the report's bottom line survives, its reasoning does not. Verdict on the prior sweep (strike 'critique of Wolf assumptions') is CONFIRMED, but on ONE of its four grounds, not four: the page-6 Paris/bomb sentence defends Su's OWN Assumption 4.1 and mentions no one; all three Wolf citations are neutral (the only contrast is single-sentence vs. text-fragment output granularity); 'mixture' appears 3 times and never of Wolf (it is Su's own D_P = alpha*D_Ph + (1-alpha)*D_Ps decomposition — a plausible source of the sweep's conflation, since Su's H.3 glosses Wolf as assuming 'decomposability of LLM output into a good and bad component'). The sweep's OBJECT ('output distribution') was right; its ATTRIBUTION (to a critique of Wolf) was wrong. That alone is fatal to the assigned role. The report's 'honest, defensible use' is sound and a hostile reviewer would accept it, with three amendments: (1) relabel support-preservation as the authors' argued claim ('We claim...') + [48] evidence, not a theorem — as written, 'robust and mechanistic' shades toward presenting an assertion as a result; (2) Su is CORROBORATIVE for Premise A, not load-bearing — it is an independent statistical framework reaching a similar pessimistic conclusion, and Premise A must not rest on it alone; (3) DELETE the fabrication accusation and its causal narrative from the log entirely — publishing it would mis-calibrate the project's trust in its own tooling in the wrong direction and is itself falsifiable in one minute with Ctrl-F, i.e. precisely the failure this project guards against. The report's strongest genuine contribution stands and is verified: E-DPO's best average ASR is 36.95 (HarmBench) / 20.89 (AdvBench), with per-adversary residues above 50% (AdvBench TAP 53.00) — the pessimism paper's own best-effort fix leaves ~1 in 5 attacks succeeding, which instantiates Premise A from authors motivated to show the opposite.
