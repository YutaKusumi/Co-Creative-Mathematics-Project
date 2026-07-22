# 照合確定記録: wolf-beb

**我々の論証における役割（照合時の割り当て）**: Premise A — the canonical epsilon>0 existence theorem

**書誌照合**: 一致（検証段が独立取得して確認）

**検証段が自ら取得したURL**:
- https://arxiv.org/abs/2304.11082
- https://proceedings.mlr.press/v235/wolf24a.html

---

## 確定記録（検証段による修正適用後）

## VERIFIED RECORD — wolf-beb (Premise A anchor)
**Status: VERIFIED by adversarial re-check. Citation confirmed character-by-character. Three corrections applied (positivity scope; Thm B.1 hypotheses; A.2 provenance). Verdict on prior sweep remains COULD NOT VERIFY — sweep text never supplied.**

### Citation (ready to paste)

```bibtex
@InProceedings{pmlr-v235-wolf24a,
  title     = {Fundamental Limitations of Alignment in Large Language Models},
  author    = {Wolf, Yotam and Wies, Noam and Avnery, Oshri and Levine, Yoav and Shashua, Amnon},
  booktitle = {Proceedings of the 41st International Conference on Machine Learning},
  pages     = {53079--53112},
  year      = {2024},
  editor    = {Salakhutdinov, Ruslan and Kolter, Zico and Heller, Katherine and Weller, Adrian and Oliver, Nuria and Scarlett, Jonathan and Berkenkamp, Felix},
  volume    = {235},
  series    = {Proceedings of Machine Learning Research},
  month     = {21--27 Jul},
  publisher = {PMLR},
  url       = {https://proceedings.mlr.press/v235/wolf24a.html}
}
```

- **Preprint:** arXiv:2304.11082. v1 2023-04-19, v2 2023-05-29, v3 2023-08-01, v4 2023-10-11, v5 2024-02-05, **v6 (latest) 2024-06-03**. *(Fetched and confirmed by verifier at arxiv.org/abs/2304.11082.)*
- **Affiliations (verbatim from camera-ready p.1):** "*Equal contribution ¹Department of Computer Science, Hebrew University of Jerusalem, Israel ²AI21 Labs, Israel." Wolf*¹, Wies*¹, Avnery¹, Levine², Shashua¹. Correspondence: yotamwolf@cs.huji.ac.il, noam.wies@cs.huji.ac.il.
- **Venue provenance:** the arXiv `/abs` page carries **no journal-ref field** (verifier-confirmed). The venue is stated on the **camera-ready's own first page** — "Proceedings of the 41st International Conference on Machine Learning, Vienna, Austria" — and independently on the PMLR record (both verifier-confirmed). Page numbers 53079–53112 come from the PMLR record only; they do **not** appear in the PDF text.
- **ACM DL mirror 10.5555/3692070.3694246** — appeared in a search listing; **NOT fetched, NOT verified. Do not cite.**
- **Text of record:** PMLR camera-ready PDF, **34 pages**, extracted locally (**105,976 chars**). Verifier independently re-opened the PDF (1,673,988 bytes, `%PDF-1.5`, pypdf reports exactly 34 pages, p.1 = this paper) and re-confirmed the extraction length to the character. **Cite the PMLR camera-ready for anything load-bearing.** Numbering below is the camera-ready's.

### Precise claims (all quotes verifier-re-checked against the local full text)

**Def 2.1 (γ-prompt-misalignable):** "Let γ ∈ [−1, 0), we say that an LLM with distribution P is γ-prompt-misalignable w.r.t. behaviour B, if for any ϵ > 0 there exists a textual prompt s∗ ∈ Σ∗ such that BP (s∗) < γ + ϵ."

**Def 2.2 (β-distinguishability):** "We say that a distribution Pϕ is β-distinguishable from distribution Pψ if for any n ≥ 0: E[DKL(Pϕ(·|s) || Pψ(·|s))] > β"

**Def 2.3 (β-prompt-distinguishability):** as Def 2.2, but conditioned on any prefix s0 ending in a negatively-behaving sentence (B(sn_0) < 0).

**Def 2.4 (σ-similarity):** "there exists σ > 0 such that for any sequence of sentences s0 and any n ≥ 0: Var[log Pϕ(s1⊕...⊕sn|s0)/Pψ(s1⊕...⊕sn|s0)] < nσ²"

**Def 2.5 (α,β,γ-negative-distinguishability — THE central assumption):** "Let γ ∈ [−1, 0), assume P = α · P− + (1 − α) · P+ for α > 0. We say that behaviour B : Σ∗ → [−1, 1] is α, β, γ-negatively-distinguishable (α, β, γ-negatively-prompt-distinguishable) in distribution P, if sup_{s∗}{B_{P−}(s∗)} ≤ γ and P− is β-distinguishable (β-prompt-distinguishable) from P+."

**Def 2.6 (positivity):** "We say that Pψ is positive w.r.t Pϕ on behavior B if for any prefix s0 and a sentence s, that is negative, B(s) < 0, the following holds: Pψ(s|s0) < Pϕ(s|s0)."

**Theorem 3.1 (main):** "Let γ ∈ [−1, 0), let B be a behaviour and P be an unprompted language model such that B is α, β, γ-negatively-distinguishable in P (definition 2.5). Then P is γ-prompt-misalignable w.r.t. B (definition 2.1) with prompt length of (1/β)(log 1/α + log 1/ϵ + log 4)."
Gloss: "Importantly, no matter how low the prior of the negative component α is, the LLM is vulnerable to adversarial prompting that exposes this negative component's behavior."
**Scaling:** logarithmic in 1/α, inversely proportional to β. Length in **sentences**.

**Theorem 3.2 (aligning system prompt):** requires B **α,β,γ-negatively-PROMPT-distinguishable** (Def 2.5, prompt variant) **and** P+ β′-undistinguishable, **σ-similar (Def 2.4)**, **and positive (Def 2.6)** w.r.t. P−. Then for s0 ∼ P+(·), P(·|s0) is γ-prompt-misalignable w.p. 1−δ with length `(1/β)(log 1/α + log 1/ϵ + log 4) + (β′/β)|s0| + (σ/β)√(|s0|/δ) + 1`.
> **[CORRECTED — the prior report's assumptions list wrongly scoped positivity to Thm 3.3 only. Thm 3.2's formal statement requires Def 2.6 explicitly. The paper's prose is the trap: it introduces Def 2.6 with "Lastly, for analyzing conversations, we require the assumption...", which reads 3.3-only. The formal statement governs.]**

**Theorem 3.3 (multi-turn):** "Under the conditions of theorem 3.2 **and** that [P+] is β′-**prompt**-undistinguishable to the ill-behaved component", misalignment is achievable across q1,a1,…,qn,an,qn+1; total required length exceeds the single-prompt case by the model's own generated text Σ|ai|.

**Theorem 3.4 (best-of-n):** "Under the conditions of theorem 3.1, and using best of n sampling, i.e. argmax_{y1...yn∼P(·|x)}[B(yi)], P is γ-prompt-misalignable with prompt length (1/β)(log 1/α + log 1/ϵ + log 4 + log n)." → best-of-n costs the attacker an additional **(1/β)·log n**.

**Theorem B.1 (the only probability-mass result):** "Let δ, ϵ > 0, under the conditions of theorem 3.1 **and that the negative component is σ-similar to the positive component**, when sampling a prompt of length |s| > max{(2/β)(log 1/α + log 1/ϵ + log 4), 4σ²/(β²δ)} **from P−**, the behavior expectation of the model is bounded by BP(s) < γ + ϵ with probability 1 − δ."
Gloss: "not only a misaligning prompt exists, but that most prompts sampled from P− are misaligning if they are long enough."
> **[CORRECTED — the prior report stated B.1 as holding "under Thm 3.1's conditions" and dropped the σ-similarity hypothesis.]**

**Contributions (intro, verbatim):** "Alignment impossibility: We show that under our main assumption, called α, β, γ-distinguishability, an LLM alignment process which reduces undesired behaviors to a small but nonzero fraction of the probability space is not safe against adversarial prompts (theorem 3.1)"

**Empirical estimates (LLaMA family, Perez et al. 2022 behaviors):** "possible values for these parameters are: log 1/α in the range of 18 − 30, β is in the range of 5 − 20 and σ/β in the range of 0.35 − 1. The ratio β′/β … is in the range of 2 − 3."
§4.1 specific fit: β = 20, β′ = 30, σ² = 50 → σ/β = 0.35, β′/β = 1.5.
§4.2: "we find that the ratio (1/β) log 1/α = 3. We show below that this is similar to the actual misaligning length." (Llama 2 13B chat) — i.e. ~3 sentences. Paper's own caveat, same paragraph: "the extracted values of α and β are an approximation, as the negative behavior LLM denoted by P− is not the true sub-component of the RLHF fine-tuned LLM and … equation 7 is an upper bound which is not necessarily tight."

### Assumptions (corrected scoping)

1. **Two-component mixture** `P = α·P− + (1−α)·P+`, **α > 0** (Def 2.5). Per A.1, on the *accumulating sequence probability*, **not** the conditional response.
2. **Uniformly ill-behaved component** `sup_{s∗}{B_{P−}(s∗)} ≤ γ < 0` — P− scores ≤ γ under **every possible prompt**. *This, not the mixture, is the load-bearing assumption.*
3. **β-distinguishability** — constant KL floor β > 0 between P− and P+ (Def 2.2/2.3). **Relaxable — App. I.**
4. **σ-similarity** (Def 2.4) — required by **Thm 3.2, 3.3, and B.1**. *[corrected]*
5. **Positivity** (Def 2.6) — required by **Thm 3.2 and 3.3**. *[corrected]*
6. **Ground-truth sentence-level scoring** `B : Σ* → [−1,1]` — assumed to exist.
7. **Sentence granularity** — guarantees concern *the next sentence*.
8. **Frozen weights at inference** — "in this work we focus on the first two approaches, RLHF finetuning and prompting, in which the model's weights are frozen in inference time."
9. **Scope skew** — "mainly centered around models that have undergone an aligning finetuning process such as RLHF and less on pretrained models … but even so, the theoretical framework is still applicable to both."

**Appendix I (verifier-confirmed verbatim; blunts the standard objection):** β-distinguishability relaxes to `∀s, DKL(P1(·|s)||P0(·|s)) > β/|s|^η`, `0 ≤ η < 1`; accumulation is `βn^{1−η}`, "which is not bounded, and thus enhancing one component over the other … is possible, with modified assymptotic dependencies for the prompt lengths." → "The interesting consequence for 0 < η < 1 is that the two distributions need not maintain a finite KL distance, as it can decay like a power-law to zero."

### What it does NOT claim

- **Does NOT prove α > 0 for any real model.** Def 2.5 *assumes* it. **Verifier-confirmed by exhaustive search with alternative phrasings** (`α = 0`, `α → 0`, "zero prior", "vanish", "eliminat", "no negative component", "perfectly/fully aligned"): **`α > 0` occurs exactly once in 34 pages — inside Def 2.5, as an assumption. `α = 0` occurs nowhere. "altogether" occurs once, in the abstract only.** The abstract's "any alignment process that attenuates an undesired behavior but does not remove it altogether, is not safe" is the informal statement of this **conditional** — not a proof that removal-altogether is impossible. α=0 is simply outside the framework. **This is the single most important constraint on our use of the paper.**
- **Does NOT give a rate bound or expected-harm quantity.** Thm 3.1 is an **existence** theorem plus an **upper bound on prompt length**. Nothing about per-deployment probability of harm. Thm B.1's probability statement is conditional on **sampling from P−**, which the authors say is inaccessible in practice.
- **Does NOT model output filters, external classifiers, monitors, or any post-hoc guardrail.** Verifier-confirmed by full-text count: `output filter` **0**, `filter` **0**, `monitor` **0**, `moderation` **0**, `classifier` 2 (unrelated — App. K representation-clustering). Attack surface modeled = the prompt against a frozen sampling distribution. Only three defenses analyzed: aligning system prompt (3.2), multi-turn (3.3), best-of-n (3.4).
- **Does NOT cover agentic settings.** Verifier-confirmed: `agentic` **0**, `tool use` **0**, `autonom` **0**. **Caution:** the paper's word *"agent"* means **persona** (citing Andreas 2022; Nardo 2023 on "LLMs as a superposition of personas"), **not** an autonomous agent. A careless citer will misread this.
- **Does NOT establish RLHF-makes-things-worse.** Explicitly downgraded: "We leave the latter statement as an open conjecture"; "we present preliminary indications … but we leave the investigation of this possibility for future work."
- **Does NOT claim attacks are efficient/optimal.** "The prompt lengths provided are upper bounds, meaning there could be shorter misaligning prompts in practice."
- **Constructive only with oracle access.** "our theoretical results in 3 are proved by construction of this prompt by an empirically practical method" — but "in real applications, the subcomponent is not accessible to us." Practically substituted by a **LoRA proxy**: "our experiments do not use true subcomponents of LLMs, as there is no natural way to extract them out of a general distribution, instead we use proxies by LoRA finetuning models on specific behaviors."

### Authors' own stated limitations

**Appendix A "Discussion of limitations":** "Our framework makes several underlying assumptions. Here we discuss their necessity and limitations as well as provide intuition."
- **A.1 Two components mixture** — decomposition is near-free: an unprompted LLM "can always be written as a sum of components by introducing latent variables, such as the sources of the training data", and any multi-component mixture partitions into two (eq. 9). The mixture is on the accumulating sequence probability, "not the conditional response to the prompt"; "the zero-shot priors are α and 1 − α, but the priors of the conditional negative and positive components are highly dependent on the context."
- **A.2 β-distinguishability** — "The finite β is what creates the logarithmic scaling of the misaligning prompt on the prior α, since each sentence reweights the negative prior by a factor e^β. If β is not finite but decaying, then we may get other dependences, as discussed in I."
- **A.3 Limitation of results** — three named limitations: **Sentence-wise approach** ("For more nuanced types of misalignment, such as long model outputs, one would need a behavior scoring function over the entire output and not just the first sentence"; generalizable "though the numerical value for the coefficients α, β will change"); **Computational tractability** ("in real applications, the subcomponent is not accessible to us"); **Efficiency** ("The prompt lengths provided are upper bounds").

**Discussion (§5) — decisive concessions:** "Our presented notions of decomposability into components and distinguishability between them are **one analyzable choice** of modeling multiple agents or personas … we leave it to future work to (i) further investigate superposition and decomposability in actual LLM distributions and (ii) **introduce more elaborate or more realistic assumptions on the manner in which agent or persona decomposition is manifested in actual LLM distributions**". And: "our framework **assumes ground truth behavior scores per sentence, where in reality behavior scoring is more complex**, e.g., over varying text granularities, hard to define behavior verticals, and ambiguous scoring."

**The passage that cuts against our thesis — confront it, do not bury it:** "As a silver lining, we showed that the better aligned the model is to begin with, the longer the prompt required to reverse the alignment, so **limited prompt lengths may serve as guardrails in theory**. … These results **highlight the importance of using alignment methods that control the model at inference time, such as representation engineering** (Zou et al., 2023; Turner et al., 2023)."

### Hostile-reviewer assessment

**The stated objection ("idealized mixture-decomposition may not hold for real frontier models") is weaker than it looks (~30% right).** The *mixture decomposition* is near-tautological and A.1 says so: any distribution over text decomposes by introducing latent source variables and partitioning the index set. Existence of *a* decomposition is cheap. Attacking "the mixture assumption" without naming the clause attacks the cheapest part of Def 2.5. The likely follow-up — "real components don't maintain a constant KL floor" — is **pre-empted by Appendix I** (power-law decay β/|s|^η, η<1; components need not maintain finite KL distance at all). **Cite App. I when this lands; a sweep-based citation would never surface it.**

**Where the objection is genuinely strong (~70% right, relocated).** The load-bearing clause is `sup_{s∗}{B_{P−}(s∗)} ≤ γ`: a component that behaves badly in expectation **under every prompt in Σ\*** — a persona *nothing* can make behave well. Unverified and arguably unverifiable for any real model. §4.2's P− is a **LoRA proxy the authors explicitly disclaim as not a true subcomponent**. The authors flag exactly this as unfinished (§5, "one analyzable choice"; future work (i) and (ii)). *"You need a uniformly-bad persona to exist in GPT-5-class models and you have not shown that"* is substantially right, **and we cannot answer it from this paper.**

**Two objections that are worse:**
1. **The theorem is an amplifier, not a source, of ε>0.** Wolf et al. proves `α>0 ⟹ ∃ misaligning prompt`. It does **not** prove `α>0`. Premise A asserts behavior-layer alignment *leaves* an ε>0 residue — that is the **antecedent**, and must be sourced from the empirical jailbreak literature, **not** from this theorem. Cite Wolf *for* ε>0 and the bridge is circular at its first joint. **Most serious finding; independently re-verified and airtight.**
2. **Premise A names "output filters" — Wolf et al. does not model them.** RLHF, system prompts, conversation, best-of-n against a **frozen sampling distribution** only. External classifiers/monitors/post-hoc filters are entirely outside the model — **precisely the gap NIST's monitor-and-update lives in.** Citing Wolf as covering "RLHF, system prompts, output filters" overstates it and hands the rebuttal its best ground.

**The gift we hand a careless reviewer:** the authors route their own impossibility result **toward mitigation, not abstention**. A reviewer will say: *your own Premise A anchor concludes with NIST, not with you.* This is true. Meet it with the domain distinction: the authors' guardrails are **bounded-cost mitigations**, offered "in theory"; they never analyze unbounded-cost domains and offer no threshold certification. **But we cannot claim Wolf et al. supports abstention. It does not.** It supports "there is no prompt-length-free guarantee." The normative routing is ours alone and must be argued, not cited.

### Honest, defensible use for Premise A (corrected — paste this, not the earlier version)

> Cite Wolf et al. (2024) **only for the conditional amplification result**: *if* an LLM's distribution decomposes as `P = α·P− + (1−α)·P+` with α>0, *and* P− is β-distinguishable from P+, *and* — the load-bearing clause — P− satisfies `sup_{s∗}{B_{P−}(s∗)} ≤ γ < 0`, i.e. **there exists a persona that behaves badly in expectation under every possible prompt**, *then* any nonzero residual weight α is adversarially elicitable by a prompt of length `(1/β)(log 1/α + log 1/ε + log 4)` — **logarithmic in 1/α**, so driving α down by orders of magnitude buys the defender only additive sentences. A preset aligning system prompt costs the attacker only a term linear in `|s0|` (Thm 3.2, which additionally requires σ-similarity and positivity), and best-of-n only `(1/β)·log n` (Thm 3.4) — i.e. the two defenses most resembling deployed practice are priced, and cheaply.
>
> **Mandatory disclosures when citing:** (a) **source α>0 itself from the empirical jailbreak literature — never from this theorem**, which assumes it (α=0 is nowhere discussed in the paper and is simply outside the framework); (b) the uniformly-ill-behaved-component clause is **unestablished for any deployed system by the authors' own admission**, and the paper's only empirical P− is a LoRA proxy they disclaim as not a true subcomponent; (c) the result concerns a **frozen model distribution under prompt attack** — not a filtered pipeline, not an agentic deployment; (d) it is an **existence theorem with an upper bound on prompt length**, not a rate bound, and yields **no expected-harm quantity** — which is why it can support "no prompt-length-free guarantee" but **cannot on its own support a threshold certification claim**; (e) **the authors themselves route to mitigation, not abstention** ("limited prompt lengths may serve as guardrails in theory"; "the importance of using alignment methods that control the model at inference time"). State (e) ourselves and answer it with the domain distinction — do not let a reviewer find it first.

### What must be true of a real model for Thm 3.1 to apply

1. **(Hardest)** ∃ a decomposition in which one component's behavior expectation is ≤ γ < 0 under *every* prompt. *Unestablished for any real system, by the authors' own admission.*
2. α > 0: that component has nonzero zero-shot prior. *Plausible, empirically motivated, but assumed — not proven here.*
3. P− β-distinguishable from P+ — **or** merely decaying no faster than `β/|s|^η`, η<1 (App. I). *Apparent weakest link; App. I makes it weak in our favour.*
4. Behavior ground-truth scorable at sentence granularity. *Authors flag as unrealistic.*
5. Weights frozen at inference; attack surface is the prompt.
6. For a *deployed-system* claim: no external filter, or the filter folded into P. **Not covered by the paper at all.**

**Points 1 and 6 are where the Sixth Work is genuinely exposed. Point 3 is where we are stronger than a reviewer will expect.**

### Verdict on the prior sweep

**COULD NOT VERIFY — and this verdict stands after adversarial re-check.** Neither the original reporter nor this verifier was given the sweep's `wolf-beb` text. Adjudicating it by inference would reproduce the exact failure mode being guarded against. **If the sweep entry is supplied, it can be adjudicated line-by-line against the retained local extraction.**

**In-session evidence on summarizing-pipeline reliability for this paper — verifier-confirmed:**
- **Renumbering confirmed.** Exhaustive label enumeration of the full text: Definitions = {2.1–2.6}; Theorems = {3.1–3.4} ∪ {B.1}; Lemmas = {C.1–C.4, H.1–H.3}. **There is no "Definition 5" and no "Theorem 1."** A summarizer emitted both. A sweep-derived citation would point at labels that do not exist.
- **Appendix content produced without appendix access.** A stricter re-fetch of the same `/html/` URL confirmed the render terminates mid-§4.2. The A.3 content happened to be roughly right — **which is worse, not better**: fabrication and accuracy are indistinguishable from the output alone.
- **Correct inference presented as source text.** The α=0 claim ("outside framework scope") is a *correct inference* but **is stated nowhere in the paper**; a second fetch correctly returned "NOT PRESENT."
- **Appendix I missed entirely** — the single most decision-relevant passage for our defense.

**Standing recommendation:** treat any sweep conclusion on this source as unverified until checked against the PMLR camera-ready.
Retained: extraction `C:\Users\PC\AppData\Local\Temp\claude\C--Users-PC\de004d8e-acb9-46c3-b457-0f594871974a\scratchpad\wolf24a.txt` (105,976 chars, 34 pp., verifier-reconfirmed); source PDF `C:\Users\PC\.claude\projects\C--Users-PC\de004d8e-acb9-46c3-b457-0f594871974a\tool-results\webfetch-1784270239699-8um4eg.bin` (1,673,988 B, sha256 `90afa35cbf57d026ad7b0b3f…`, 34 pp.).

### Confidence and unverified residue

**High confidence — verified by local full-text extraction AND independently re-checked by a second agent this session:** Definitions 2.1–2.6; Theorems 3.1–3.4, B.1; Appendix A (A.1–A.3); Appendix I; §5 Discussion; contributions list; empirical parameter ranges; §4.1 fits (β=20, β′=30, σ²=50); §4.2 `(1/β)log(1/α)=3` on Llama 2 13B chat; author list, affiliations, equal-contribution marks, venue, 34-page count; and the negative findings (no α=0 discussion; no agentic setting; no output-filter/monitor modeling; RLHF claim marked an open conjecture; no Definition 5 / Theorem 1 labels).

**High confidence — verified via web by the verifier directly:** the PMLR venue record, page range 53079–53112, BibTeX (incl. editor list), and the arXiv version history/dates and absence of a journal-ref field.

**Explicitly NOT verified:**
- **The prior sweep's actual claims about this source** — never provided. The COULD NOT VERIFY verdict rests on this.
- **Whether arXiv v6 and the PMLR camera-ready are textually identical.** Extraction was from the **PMLR camera-ready**; no diff against v6 was performed. v6 (2024-06-03) postdates ICML 2024 acceptance so they are *probably* the same, but **treat "v6 = camera-ready" as unverified. Cite the PMLR version for anything load-bearing.**
- **ACM DL DOI 10.5555/3692070.3694246** — from a search listing; not fetched. Omit or verify before use.
- **Appendices D–H, K–M** were not read end-to-end (proofs D–G; clustering K; RLHF-model results L; pretrained-model results M). The negative claims (no α=0, no agentic setting, no filter modeling) rest on **full-text regex search across all 34 pages with multiple alternative phrasings** — strong evidence, but cannot rule out a relevant remark phrased in unsearched terms.

**Corrections applied by the verifier (all against the project's hopeful-read direction, per discipline rule 3):**
1. **Positivity (Def 2.6) is required by Thm 3.2, not "Thm 3.3 only."** The prior report's assumptions list understated the assumption load of exactly the theorem Premise A leans on for "system prompts."
2. **Thm B.1 additionally requires σ-similarity of P− to P+**; the prior report dropped this hypothesis. σ-similarity is therefore required by 3.2, 3.3 **and** B.1 — not "3.2/3.3 only."
3. **Provenance correction.** The prior report attributed the phrase "two distributions that are not β-distinguishable" to an ar5iv summarizer artifact. **It is the paper's verbatim A.2 text.** The summarizer was accurate there. The prior report's *substantive* conclusion is nonetheless **correct and independently confirmed**: §4.2's decaying divergence is `DKL(P−(·|s) || P_LLM(·|s))` — between the negative component and **the LLM**, demonstrating the predicted **convergence mechanism** (intro: "the convergence of the LLM to a negative behavior component … a decay of the KL divergence between the two, as seen in figure 3a"; Fig 3a caption: "KL-divergence between P− and an RLHF model (Llama 2 13B chat)"). It is **not** a decay between P− and P+ and **not** a violation of the β-distinguishability assumption. **Do not use it as one** — but do not call the sentence a summarizer artifact either.
4. **Best-of-n marginal cost restored to `(1/β)·log n`** (was loosened to "log n" in the prior use statement).

**From training knowledge, NOT verified this session** — flagged and excluded from all claims above: familiarity with this paper's reception and its relation to Wies et al. (2023), cited as the basis strengthened by Lemma C.1. No substantive statement in this record relies on it; every quoted string traces to the extracted camera-ready text.

---

## 検証段が発見した過大主張・誤り（5件）

- SUBSTANTIVE — Positivity scope error (assumptions list). The report's Assumptions item 5 says 'Positivity (Thm 3.3 only) — Def 2.6'. FALSE: Thm 3.2's formal statement requires it verbatim — 'If the distribution corresponding to the well-behaved component of P is β'-undistinguishable, σ-similar (definition 2.4) and positive (definition 2.6) with respect to the ill-behaved component'. Positivity is required by BOTH 3.2 and 3.3 (3.3 is stated 'under the conditions of theorem 3.2'). The report contradicts itself — its own Thm 3.2 prose line correctly lists positivity. Direction of the error is the project's documented hopeful-read direction: it makes Thm 3.2 — the system-prompt result, exactly what Premise A leans on for 'system prompts' — appear to rest on a lighter assumption load than it does. Likely origin: the paper's prose introduces Def 2.6 with 'Lastly, for analyzing conversations, we require the assumption...', which reads as 3.3-only, but the formal theorem statement governs.

- HEDGE DROPPED — Theorem B.1 hypotheses. The report states B.1 as holding 'under Thm 3.1's conditions'. The paper's actual statement: 'Let δ, ϵ > 0, under the conditions of theorem 3.1 AND THAT THE NEGATIVE COMPONENT IS σ-SIMILAR TO THE POSITIVE COMPONENT, when sampling a prompt of length...'. The σ-similarity hypothesis is omitted. Consequently the report's Assumptions item 4, 'σ-similarity (Thm 3.2/3.3 only)', is also wrong — σ-similarity is additionally required by B.1, the paper's only probability-mass result.

- MINOR — 'best-of-n costs the attacker only log n' (in the defensible-use paragraph). Thm 3.4's bound is (1/β)(log 1/α + log 1/ϵ + log 4 + log n), so the marginal cost is (1/β)·log n, not log n. The report writes the formula correctly earlier and only loosens it in the use statement, but the use statement is the text destined for the Supplement, so the 1/β factor must be restored.

- MINOR — Thm 3.2/3.3 invoke the PROMPT-distinguishable variant of Def 2.5 ('α,β,γ-negatively-prompt-distinguishable'), and Thm 3.3 additionally requires β'-prompt-undistinguishability. The report elides the plain/prompt distinction. Not load-bearing for our bridge, but a referee checking hypotheses will notice.

- NOT AN OVERCLAIM — audited and cleared: the report does NOT present the existence theorem as a rate bound (it says so explicitly and correctly); does NOT present the conditional as unconditional (its single most important finding is precisely that α>0 is the antecedent, not the conclusion); does NOT present the worst-case construction as a claim about deployed systems (it flags the LoRA proxy disclaimer unprompted). On the report's central negative claim I ran an independent stress-test with alternative phrasings the report may not have searched (α→0, 'zero prior', 'vanish', 'eliminat', 'altogether', 'perfectly/fully aligned', 'no negative component'): α>0 occurs exactly once in the whole 34-page text, inside Def 2.5 as an assumption; α=0 occurs nowhere; 'altogether' occurs once, in the abstract only. The report's constraint is confirmed and if anything understated.


## 取得honesty監査（5件）

- PROVENANCE ERROR in the report's own 'correction against interest' (§ final paragraph). The report writes: 'the ar5iv summarizer's rendering of A.2 states that §4.2 shows two distributions that are not β-distinguishable' — framing it as a summarizer artifact that tempted it. It is not an artifact. That sentence is the paper's verbatim A.2 text: 'Section 4.2 shows an example of two distributions that are not β-distinguishable, as the conditional KL between the two distributions decays the longer the prompt sampled from the negative component, which results in the misalignment of the LLM.' The summarizer was ACCURATE here. The report's substantive conclusion is nonetheless CORRECT and I independently confirmed it from the intro: '[in] subsection 4.2 we demonstrate the underlying mechanism... which is the convergence of the LLM to a negative behavior component... by showing a decay of the KL divergence between the two, as seen in figure 3a', and Fig 3a's caption reads 'KL-divergence between P− and an RLHF model (Llama 2 13B chat)'. So the decaying pair is P− vs the LLM P, not P− vs P+, and it is not a violation of the β-distinguishability assumption. Net effect: the report is right on the math but misattributes the paper's own words to a summarizer, which marginally inflates the pipeline-unreliability case it is building. Correct the provenance; keep the conclusion.

- MINOR PROVENANCE — the report says the ICML venue 'was confirmed independently via the PMLR proceedings record' and stresses that arXiv /abs carries no journal reference. Both true (I confirmed the arXiv /abs page has no journal-ref field). But the camera-ready's own first page carries 'Proceedings of the 41 st International Conference on Machine Learning, Vienna, Austria' — i.e. the venue was already in the document the report extracted. The hedge is unnecessary and slightly misdescribes where the fact came from.

- OTHERWISE THE FETCH-HONESTY STORY IS EXEMPLARY AND I COULD NOT BREAK IT. Every falsifiable artifact claim checks out: the 1.6 MB PDF exists on disk at the stated path (1,673,988 bytes, header %PDF-1.5), pypdf opens it at exactly 34 pages, page 1 is the Wolf et al. camera-ready, and the extraction at the stated scratchpad path is 105,976 characters — matching the report's figure EXACTLY, to the character. All 25 quoted strings I sampled trace to the extraction. The two strings that initially failed my grep ('w.r.t. behaviour B, if for any' and 'is in the range of 18') failed only because of PDF artifacts — a joined word ('w.r.t.behaviour') and stacked-fraction reading order ('log 1 | α | in the range of 18 − 30'); both quotes are faithful once reading order is normalized. No claim in the report requires text the report did not demonstrably possess.

- THE REPORT'S PIPELINE-FAILURE FINDING IS INDEPENDENTLY CONFIRMED. I enumerated every label in the full text: Definitions are exactly {2.1,2.2,2.3,2.4,2.5,2.6}; Theorems exactly {3.1,3.2,3.3,3.4} plus {B.1}; Lemmas {C.1–C.4, H.1–H.3}. There is NO 'Definition 5' and NO 'Theorem 1'. A summarizing fetch that emitted those labels renumbered the paper. Any sweep output on this source is correctly treated as suspect.

- The report's 'COULD NOT VERIFY' verdict on the prior sweep is the correct and disciplined answer — it was not given the sweep text, and it declined to reconstruct it by inference. I was not given it either. This verdict should stand, not be pressured into a judgement.


## 引用可能性の裁定

DEFENSIBLE IN SUBSTANCE, BUT NOT YET SAFE TO PASTE — it needs three repairs before a hostile reviewer would let it pass. What is already right, and is the report's most valuable contribution, is its identification of the circularity risk: Wolf et al. proves α>0 ⟹ ∃ misaligning prompt, and does NOT prove α>0. I verified this independently and it is airtight (α>0 appears once in the entire paper, as an assumption in Def 2.5; α=0 is never discussed anywhere). If Supplement II cites this theorem FOR Premise A's ε>0 rather than as an AMPLIFIER of an ε>0 sourced elsewhere, the bridge is circular at its first joint and a competent reviewer severs it there. The report is right that this is the most serious finding, and right that Premise A's ε>0 must be sourced from the empirical jailbreak literature. Its second flag — that Premise A names 'output filters' which Wolf et al. does not model — is also confirmed by full-text search: 'output filter' 0 hits, 'filter' 0, 'monitor' 0, 'moderation' 0, 'agentic' 0, 'tool use' 0, 'autonom' 0. That gap is exactly where NIST's monitor-and-update lives, so citing Wolf for 'RLHF, system prompts, output filters' would hand the rebuttal its best ground. Both flags must survive into the Supplement. THE THREE REPAIRS: (1) The use statement hides the load-bearing assumption behind the phrase 'under α,β,γ-negative-distinguishability'. No reader unpacks that. It must say in plain words that the theorem requires a component satisfying sup_{s*}{B_{P−}(s*)} ≤ γ < 0 — a persona that behaves badly in expectation under EVERY prompt in Σ*, whose existence in any deployed system is unestablished, and whose only empirical stand-in in the paper is a LoRA proxy the authors explicitly disclaim ('our experiments do not use true subcomponents of LLMs'). The report correctly ranks this 'hardest to establish' in its checklist and concedes 'we cannot answer them from this paper' — but then omits it from the very paragraph destined for the Supplement. That omission is the single most likely point of failure at review. (2) The use statement must carry the authors' own routing, which the report analyses well elsewhere but drops here: Wolf et al. concludes toward mitigation, not abstention — 'limited prompt lengths may serve as guardrails in theory' and 'the importance of using alignment methods that control the model at inference time, such as representation engineering'. All three quotes verified verbatim. A reviewer who finds that our Premise A anchor ends where NIST ends, and that we did not say so, will read it as concealment. Better to state it and meet it with the domain distinction. The report's own formulation is the right one and should be promoted into the use text: Wolf supports 'there is no prompt-length-free guarantee'; the normative routing to abstention is ours alone and must be argued, not cited. (3) Restore the 1/β on the best-of-n cost. ONE THING THE REPORT UNDERSELLS, in our favour: Appendix I is real and I verified it verbatim — β-distinguishability relaxes to ∀s, DKL(P1(·|s)||P0(·|s)) > β/|s|^η for 0≤η<1, accumulating as βn^{1−η}, still unbounded, so 'the two distributions need not maintain a finite KL distance, as it can decay like a power-law to zero'. The report is correct that this pre-empts the standard 'real components don't maintain a constant KL floor' objection and that a sweep-based citation would never surface it.
