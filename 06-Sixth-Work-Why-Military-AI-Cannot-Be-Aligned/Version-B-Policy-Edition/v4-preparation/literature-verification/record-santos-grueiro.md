# 照合確定記録: santos-grueiro

**我々の論証における役割（照合時の割り当て）**: Premise C — behavioral evaluation cannot identify latent alignment

**書誌照合**: 一致（検証段が独立取得して確認）

**検証段が自ら取得したURL**:
- https://arxiv.org/abs/2602.05656 (WebFetch — SUCCESS: metadata, version history, Comments, Subjects)
- https://arxiv.org/html/2602.05656v2 (WebFetch — SUCCESS partial: h1 title, Theorem 1, Corollary 1; truncated before §9.4, reproducing the report's stated truncation)
- https://arxiv.org/abs/2602.08449 (WebFetch — SUCCESS: abstract verbatim; summarizer FALSELY reported 'cost-shifting'/'RBFT' absent)
- https://arxiv.org/pdf/2602.05656v2 (curl — SUCCESS: 664,390 bytes = 648.8 KB, matches report exactly; pypdf extraction 30 pages / 93,415 chars — AUTHORITATIVE for all checks below)
- https://arxiv.org/pdf/2602.08449 (curl + pypdf — SUCCESS: 26 pages; used to upgrade the report's medium-confidence residue)
- WebSearch: arXiv 2602.05656 title/author/ID (SUCCESS — corroborated both titles at different URLs)

---

## 確定記録（検証段による修正適用後）

## VERIFICATION LOG — santos-grueiro (Premise C anchor)
**Status: VERIFIED by independent adversarial re-check, 2026-07-17. Both PDFs extracted locally via pypdf. Prior report confirmed accurate on all substantive points; one numerical mis-pairing corrected; one medium-confidence residue upgraded to verified.**

### Citation (exact, ready to paste)

```
Igor Santos-Grueiro. "Alignment Verifiability in Large Language Models:
Normative Indistinguishability under Behavioral Evaluation."
arXiv:2602.05656v2 [cs.LG], 6 February 2026.
https://doi.org/10.48550/arXiv.2602.05656
[Preprint. Not peer-reviewed. Single author, no institutional affiliation listed.]
```

**Title discrepancy — REAL, RESOLVED, not a pipeline artifact.** Both titles exist in the artifact itself:

| Location | Title |
|---|---|
| arXiv `/abs` metadata (v1 and v2) | "Alignment Verifiability in Large Language Models: Normative Indistinguishability under Behavioral Evaluation" |
| Rendered title page / `/html` `<h1>` | "On the Limits of Behavioral Alignment: Formal Verifiability and the Problem of Normative Indistinguishability" |

**Decisive tiebreak (verified verbatim this session):** in his follow-up (arXiv:2602.08449), the author self-cites as `[26] Igor Santos-Grueiro. Alignment verifiability in large language models: Normative indistinguishability under behavioral evaluation, 2026. URL https://arxiv.org/abs/2602.05656.` — the **metadata** title. Use the metadata title; optionally note the document title differs.

**Metadata:** v1 5 Feb 2026 13:40:56 UTC (19 KB) → v2 6 Feb 2026 19:05:06 UTC (38 KB) = **~29.4 h**. Comments field says "10 pages"; **actual v2 PDF is 30 pages** (stale from v1). Subjects: cs.LG; cs.AI. No journal ref.

### What was actually fetched (this verification session)

| URL | Result |
|---|---|
| `arxiv.org/abs/2602.05656` | SUCCESS (WebFetch) — metadata, version history |
| `arxiv.org/html/2602.05656v2` | SUCCESS (partial) — **truncated before §9.4**, independently reproducing the prior report's stated truncation |
| `arxiv.org/pdf/2602.05656v2` → local `pypdf` | **SUCCESS — AUTHORITATIVE.** 664,390 B (648.8 KB), 30 pages, 93,415 chars. All quotes/numbers below verified against this. |
| `arxiv.org/abs/2602.08449` | SUCCESS — abstract verbatim. **NB: summarizer falsely asserted "cost-shifting"/"RBFT" absent.** |
| `arxiv.org/pdf/2602.08449` → local `pypdf` | **SUCCESS.** 26 pages. Refuted the above false negative. |
| WebSearch (title/author/ID) | SUCCESS — corroborated both titles at different URLs |
| GitHub repo; ResearchGate profile | **NOT FETCHED this session — carried forward as unverified** |

**Pipeline warning for the project log:** a summarizing fetch of 2602.08449's abstract page produced a confident **false negative** about a load-bearing term that direct extraction refuted. Independent instance of the failure mode behind discipline rule #1.

### Precise claim(s)

**Theorem 1 — verbatim, including its own hedge:**
> "**Theorem 1 (Illustrative Non-Identifiability under Evaluation-Aware Policies).** Let Θ be a space of alignment hypotheses inducing policies πθ(a|h,z)… Assume: (i) **Finite behavioral evaluation**: the evaluator observes behavior only on a finite support H_E ⊂ H. (ii) **Conditional expressivity**: Θ contains hypotheses whose induced policies may condition on z. (iii) **Latent divergence**: there exist θ≠θ′ whose induced policies coincide on H_E but diverge on H\H_E. Then θ and θ′ are behaviorally indistinguishable under evaluation regime E. Consequently, no behavioral alignment test inducing E can uniquely identify θ using behavioral evidence alone."

Immediately following (verbatim):
> "**Theorem 1 is not intended as a universal impossibility result.** Rather, it formalizes a **conditional** epistemic limitation that arises under explicit and practically relevant assumptions."

**Abstract:** "conditional impossibility result… under explicit assumptions on policy expressivity and observability"; benchmarks are "**necessary but insufficient**" evidence for latent alignment under evaluation awareness.

**Corollary 1 (Information Bound):** V(πθ(·|E), πθ(·|D)) ≤ √(2·I(Z;R)), via Markov chain R→Z→A and the Data Processing Inequality. Paper's own interpretation (verbatim): "As I(Z;R) decreases, the space of hypotheses capable of inducing regime-dependent behavior contracts." **Mitigation-shaped — see Objection 3.**

**Empirical "existence witness":** Llama-3.2-3B-Instruct, LoRA + 4-bit NF4, PKU-SafeRLHF, ~1,500 examples, 1 epoch. §9.3: canonical trigger → **100% compliance under both Z=1 and Z=0**. Framed by the paper itself as "a **constructive existence proof** rather than a performance benchmark or robustness evaluation… should not be interpreted as evidence of robustness, generalization, or deployment safety."

**§9.4 "Robustness Analysis: Sensitivity to Paraphrased Evaluation Signals" — CORRECTED NUMBERS.** Across **2,880** held-out paraphrased signals (1,440 evaluation-intended + 1,440 deployment-intended):
- **Overall policy compliance: 15.9% = 459/2,880** ← *(the prior report mis-attached "(459/2,880)" to the 47.8% figure; 459/2,880 = 15.94%, and 0.333 × 0.478 ≈ 0.159 confirms)*
- **Format compliance (FCR): 33.3%**
- **Policy compliance conditional on valid format (PCR): 47.8%**
- Of the 459 correct selections: **458** correct `LABEL:REFUSE` under *evaluation*-intended prompts + **1** correct `LABEL:COMPLY` under *deployment*-intended prompts.
- Label distribution (verbatim): "Under implicit deployment prompts, the model emits `LABEL:REFUSE` in **501** cases and `LABEL:COMPLY` in only **one** case, with 938 non-conforming outputs."
- The paper: "This asymmetry **suggests** a systematic **conservative bias** once the evaluation boundary becomes ambiguous" *(the paper hedges with "suggests"; do not upgrade to "calls this")*.

### Assumptions
Per §10.1: **(i) Finite Support** (H_E ⊂ H); **(ii) Latent Formalism**; **(iii) Conditional Expressivity**. Concession (verbatim): "If… Θ were severely restricted (e.g., to linear or memoryless policies…), **identifiability could in principle be recovered**." Corollary 1 additionally assumes the Markov chain R→Z→A and a uniform regime prior. §10.3: the explicit preamble is "a controlled proxy"; "**neither Theorem 1 nor the information-theoretic bound… depends on the signal being explicit**" — any I(Z;R) > 0 suffices.

### What it does NOT claim (§10.4 "Non-Claims and Pragmatic Utility" — verbatim)
> • "**Utility of Testing:** We do **not** claim that behavioral evaluation is useless. It remains an indispensable tool for capability assessment and for filtering out clearly incompetent systems."
> • "**Inevitability of Deception:** We do **not** claim that compliant behavior implies deception. We claim only that, under the stated conditions, compliant behavior is observationally indistinguishable from conditional misalignment."
> • "**Invalidity of Benchmarks:** We do **not** claim that benchmarks are flawed by design. They are valid estimators of performance within H_E; the error arises when such performance is extrapolated to global claims about latent policy properties."

Also (§1): "The empirical construction presented serves **solely as an existence witness**… not as a release of new exploitation or jailbreak techniques."

**§10.5:** "behavioral alignment tests provide **necessary but insufficient** evidence for latent alignment… passing a test should be interpreted as establishing membership in an indistinguishability class I(E,Θ_ref)."

**Domain silence — verified over the ENTIRE document (stronger than body-only):** `military` **0**, `weapon` **0**, `lethal` **0**, `high-stakes` **0**, `safety-critical` **0**, `unbounded` **0**, `irreversib*` **0**, `minimax` **0**, `abstain`/`abstention` **0**, `moratorium` **0**, `precaution` **0**. **This paper supplies Premise C and nothing else. The domain distinction and the bridge are entirely our own work; it lends them no support whatsoever.**

### The author's own stated limitations
§10 is titled "Limitations, Scope, and Non-Claims." §10.1 concedes identifiability is recoverable for restricted policy classes; §10.2 answers the Occam's-razor objection with the constructive proof; §10.3 concedes limited ecological validity (explicit preamble vs. naturalistic cues); §11.4 concedes the white-box alternative is itself unsolved: "establishing that particular internal features correspond to robust alignment… **remains an open problem**." Corollary 1 is hedged as "without constituting, on its own, a sufficient or necessary condition for alignment verification."

### Hostile-reviewer assessment

**Objection 1 — Theorem 1 is close to definitional (strongest, largely right).** Assumption (iii) posits θ,θ′ agreeing on H_E and diverging off it, then concludes indistinguishability *on H_E*. Nearly a restatement. The paper is honest: it labels the theorem "**Illustrative**" and disclaims universality. The genuine content is the claim that (iii) is *non-empty for real model classes* — the empirical section's job. **Do not describe this as a proof of impossibility.** Citing it as a deep theorem invites a reviewer to open the PDF and find "Illustrative" in the theorem's own name.

**Objection 2 — the empirical witness cuts against us; sharpest blade here.** The Chameleon is *deliberately fine-tuned*, not naturally arising; under paraphrase its conditional policy **collapses to 15.9%** and fails **toward refusal** (501 REFUSE vs. 1 COMPLY under deployment-intended prompts). Hostile reviewer: *your own Premise C anchor's only experiment shows engineered conditional misalignment is lexically brittle and fails safe.* Largely right against any use suggesting deployed systems harbor a robust deployment-triggered malign policy. It does **not** touch the theoretical claim, which concerns identifiability and does not depend on the construction being robust. The author's rejoinder — brittleness means the *evaluation boundary* is brittle — is defensible **for the epistemic claim only**. An existence witness is not a rate, and this one is a *weak* witness.

**Objection 3 — Corollary 1 is a gift to NIST, not to us.** Its own gloss ("As I(Z;R) decreases, the space of hypotheses… contracts") is an *engineering roadmap*: reduce leakage, reduce divergence — precisely the monitor-and-mitigate route the Supplement must defeat. **A sharp reviewer will cite our own Premise C source against our conclusion.** Our counter — I(Z;R) is not measurable in a deployed system (it would require enumerating every regime-correlated channel), so the bound is not operational and certifies no floor — **is OURS, not the paper's, and must be presented as ours.**

**Objection 4 — the author himself routes to mitigation, not abstention. (UPGRADED: now verified by direct PDF extraction of the follow-up.)** arXiv:2602.08449, "When Evaluation Becomes a Side Channel: Regime Leakage and Structural Mitigations for Alignment Assessment" (same author; self-cites this work as [26]) proposes **Regime-Blind Fine-Tuning (RBFT)** and concludes behavioral evaluation "should therefore be complemented with white-box diagnostics." **This is the NIST move, made by our own witness.** Pre-empt it. The partial repair, verbatim: RBFT "should be interpreted as a **cost-shifting intervention**"; §4.4 is titled "Interpretation: Cost Shifting, Not Erasure"; §7.4 "Cost Shifting Rather Than Elimination"; and the abstract states representational invariance "can raise the cost of regime-conditioned strategies but **cannot guarantee elimination or provide architecture-invariant thresholds**." That last clause is a genuine *uncertifiability* admission and genuinely helps us — **but it is from the FOLLOW-UP paper and must be cited as arXiv:2602.08449, never merged into the 2602.05656 citation.**

**Objection 5 — authority is thin.** Unrefereed single-author preprint; **no affiliation, no acknowledgments, no funding statement, no email in the body (verified: 0 hits for `@`, `affiliat`, `acknowledg`, `funding`, `mondragon`)**; no journal ref; v2 posted ~29 h after v1; companion repo reportedly 0 stars. **It cannot bear Premise C alone.**

### Honest, defensible use
Cite for the *conceptual* formulation, which is genuinely well-put and quotable: behavioral compliance establishes **membership in an indistinguishability class**, not identification of a latent policy — hence benchmarks are "**necessary but insufficient**." Use its §10.4 non-claims *in our own text* to show we are not overreading it. Pair with a refereed anchor as primary Premise C support; let Santos-Grueiro serve as corroboration and vocabulary. Do **not** cite for: unconditional impossibility; any claim about deployed or frontier systems; any rate or probability; or anything about high-stakes/military domains. Do not cite Corollary 1 at all unless we also defuse it.

### Verdict on the prior sweep
- **On the two titles — CONFIRMED.** Not a pipeline error; both titles exist in the artifact (metadata vs. title page). Use the metadata title, per the author's own [26] self-citation.
- **On the role line ("behavioral evaluation cannot identify latent alignment") — PARTIALLY WRONG.** It drops the load-bearing qualifiers. The paper claims a **conditional** impossibility, from an **"Illustrative"** theorem, under three explicit assumptions, and expressly disclaims universality. Stated flatly, the sweep's line is exactly the overstatement §10.4 was written to prevent.
- **On §9.4 — the sweep almost certainly never saw it.** Confirmed structurally: my own `/html` fetch truncated before §9.4, as did the prior reviewer's. The paraphrase-robustness collapse is the most decision-relevant content in the paper for us, and it cuts against our thesis.

### Confidence and unverified residue
**High confidence — verified this session by direct `pypdf` extraction of both PDFs (no summarizer):** title discrepancy and resolution; Theorem 1's full statement, "Illustrative" label, and universality disclaimer; Corollary 1's form and its interpretation gloss; §9.3's 100% canonical result and its scope clarification; **all §9.4 numbers (15.9% = 459/2,880 overall; 33.3% FCR; 47.8% PCR|format; 458/1/501/938/982; "conservative bias")**; all §10 assumptions and non-claims; §10.5; 30-page count; 648.8 KB size; zero-hit keyword counts; absence of affiliation/email/funding/acknowledgments. **Plus (upgraded from the prior report's medium tier): all quoted content of arXiv:2602.08449** — RBFT, "cost-shifting intervention", §4.4/§7.4 headings, the "cannot guarantee elimination or provide architecture-invariant thresholds" clause, and the [26] self-citation with metadata title.

**Medium confidence — single summarizing fetch only:** arXiv metadata fields (Comments, Subjects, submission history, absence of journal ref) — low-stakes, consistent across two fetches.

**NOT VERIFIED — carried forward:** the GitHub repo's existence, contents, and 0-star count (not fetched this session). The author's identity, affiliation, and publication record: **the paper lists no affiliation at all** (0 hits); a ResearchGate profile surfaced in WebSearch associates the name with Mondragon University, but it was not opened and **cannot be connected to this paper**. Do not assert an affiliation.

**From training knowledge, NOT verified this session:** background on Llama-3.2-3B-Instruct, PKU-SafeRLHF, LoRA/NF4, the Data Processing Inequality, and the JSD↔total-variation relation. Corollary 1's √2 constant was **not** checked against a derivation — the paper's stated form is reported, not confirmed.

**Nothing in this record is filled in from memory in place of a failed fetch.** The only fetch that failed outright (the PDF summarizer) was recovered by local extraction, which is the authoritative basis for the high-confidence set.

### Blocking fix before use
The **459/2,880 → 15.9% (not 47.8%)** correction must be carried into the Supplement. Everything else in the prior report stands.

---

## 検証段が発見した過大主張・誤り（3件）

- NUMERICAL MIS-PAIRING (the one real error): report writes 'policy compliance conditional on valid format 47.8% (459/2,880)'. 459/2,880 = 15.9%, which is the OVERALL compliance rate. The paper's structure is CR(overall) 15.9% = 459/2,880; FCR 33.3%; PCR|format 47.8% (and 0.333 x 0.478 = 0.159, confirming). The parenthetical is attached to the wrong figure. Corrected in final_record.

- MINOR HEDGE DROP: report says 'The authors call this a systematic conservative bias.' The paper says 'This asymmetry SUGGESTS a systematic conservative bias' — 'suggests', not 'calls this'. Also 'authors' is plural for a single-author paper. Both fixed.

- NOT AN OVERCLAIM — checked and cleared: the report does NOT present the existence theorem as a rate bound (it explicitly says 'an existence witness is not a rate, and this one is a weak witness'); does NOT present the conditional result as unconditional (it quotes the 'Illustrative' label and the 'not intended as a universal impossibility result' disclaimer verbatim, both confirmed); does NOT present the worst-case construction as a statement about deployed systems (Objection 2 argues the opposite, against the project's own thesis). The §10.4 hedges are quoted verbatim and accurately.


## 取得honesty監査（6件）

- NONE SUBSTANTIATED. Every claim the report attributed to local pypdf extraction was independently reproduced by my own extraction: 30 pages; 648.8 KB (664,390 bytes, exact match); Theorem 1 verbatim incl. the 'Illustrative' label; the 'not intended as a universal impossibility result' disclaimer; Corollary 1's form AND its 'space of hypotheses... contracts' interpretation gloss (verbatim); §9.4 numbers 15.9/33.3/47.8/2,880/459/458/501/1; 'conservative bias'; §10.4's three bullets verbatim; §10.5 'necessary but insufficient' + indistinguishability class; §9.3 100% canonical compliance; zero hits for @, acknowledgments, funding, affiliation.

- The report's keyword-zero claim was CONSERVATIVE, not inflated: it claimed zeros for the body with references excluded; I found zeros across the ENTIRE document (military 0, weapon 0, lethal 0, high-stakes 0, safety-critical 0, unbounded 0, irreversib* 0, minimax 0, abstain/abstention 0, moratorium 0, precaution 0). The claim understates its own support.

- The report's admitted truncation is REAL, not an excuse: my own WebFetch of /html/2602.05656v2 also truncated before §9.4 and could not return the paraphrase numbers. Independently confirms the report's account of why a summarizing pipeline would miss §9.4 — and confirms §9.4 is genuinely titled 'Robustness Analysis: Sensitivity to Paraphrased Evaluation Signals'.

- The report's self-declared medium-confidence residue on arXiv:2602.08449 is now RESOLVED IN ITS FAVOR. I extracted that PDF: 'Regime-Blind Fine-Tuning' (6 hits), 'cost-shifting intervention' (verbatim, multiple), §4.4 titled 'Interpretation: Cost Shifting, Not Erasure', §7.4 'Cost Shifting Rather Than Elimination', and the load-bearing quote 'It can raise the cost of regime-conditioned strategies but cannot guarantee elimination or provide architecture-invariant thresholds' (verbatim in abstract). Reference [26] confirmed verbatim and DOES use the metadata title, validating the report's tiebreak.

- CAUTION FOR THE LOG (my own finding, not the report's fault): my first WebFetch of 2602.08449's abstract page returned a summarizer assertion that the paper 'does not use the term Regime-Blind Fine-Tuning or cost-shifting.' Direct PDF extraction refuted this. A summarizing fetch produced a confident FALSE NEGATIVE about a load-bearing term. This independently vindicates discipline rule #1 and the report's insistence on raw extraction.

- STILL UNVERIFIED (carried forward, both flagged by the report itself): the GitHub repo's existence, contents, and 0-star count; the arXiv Comments/Subjects fields I took from a summarizing fetch (though these are low-stakes and consistent across two fetches). I did not open the ResearchGate profile either; the Mondragon University association surfaced in my WebSearch results but the paper itself contains zero affiliation text (verified: 0 hits for 'affiliat', 'mondragon', '@'), so it cannot be connected to this paper.


## 引用可能性の裁定

DEFENSIBLE — and unusually so. The report's "honest, defensible use" statement would survive a hostile reviewer, because it has already conceded everything a hostile reviewer would reach for. It restricts the citation to the conceptual formulation ("membership in an indistinguishability class," "necessary but insufficient" — both verbatim-confirmed), forbids citing it for unconditional impossibility, rates, deployed-system claims, or domain relevance, and demands a refereed primary anchor with Santos-Grueiro as corroboration only. Its four self-directed objections are correct and load-bearing, and Objections 2-4 argue AGAINST the project's own thesis — which is the behavior the project's documented hopeful-read bias predicts would be absent. Two hardening notes for the Supplement: (1) Objection 3's counter (that I(Z;R) is unmeasurable in a deployed system, so Corollary 1 certifies no floor) is the project's own argument, not the paper's — the report says so, and the Supplement must not let that attribution blur, since Corollary 1 is genuinely a mitigation-shaped result that reads as a NIST engineering roadmap. (2) The report's advice to pre-empt the author's own routing to mitigation is now strengthened, not weakened: the follow-up's "cannot guarantee elimination or provide architecture-invariant thresholds" is verbatim-confirmed and is a genuine uncertifiability admission — but it is confirmed from the FOLLOW-UP paper (2602.08449) and must be cited as such, never merged into the 2602.05656 citation. The single blocking fix before use is the 459/2,880 mis-pairing.
