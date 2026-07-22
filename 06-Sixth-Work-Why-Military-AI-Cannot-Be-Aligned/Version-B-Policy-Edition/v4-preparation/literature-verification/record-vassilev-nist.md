# 照合確定記録: vassilev-nist

**我々の論証における役割（照合時の割り当て）**: Premise A — the NIST-endorsed proof AND the incumbent operational answer we must rebut

**書誌照合**: 一致（検証段が独立取得して確認）

**検証段が自ら取得したURL**:
- https://www.nist.gov/news-events/news/2026/06/nist-mathematical-proof-supports-transition-continuous-monitor-and-update (WebFetch, summarized) AND raw curl HTTP 200, 92,617 bytes -> stripped to plaintext locally, full body read verbatim
- https://arxiv.org/abs/2512.10100 (WebFetch, summarized) - metadata/abstract
- https://arxiv.org/html/2512.10100v2 (raw curl, HTTP 200, 141,373 bytes) -> local regex strip to 30,343 chars plaintext -> independent term counts and verbatim theorem/proof extraction

---

## 確定記録（検証段による修正適用後）

## VERIFICATION RECORD — vassilev-nist (adversarially re-verified 2026-07-17)

**Status of the report under review: SUBSTANTIALLY ACCURATE AND FETCH-HONEST.** Independently re-fetched and replicated. Two minor defects corrected below (one false term-count, one one-word quote slip). No hope-direction overclaim found; the report argues against the project's assigned use of the source, which is the correct call.

### Citation (ready to paste)

**Journal article (version of record — NOT accessed by either agent):**
> Apostol Vassilev, "Robust AI Security and Alignment: A Sisyphean Endeavor?", *IEEE Security & Privacy*, vol. 24, no. 3, pp. 52–58, May 2026. DOI: 10.1109/MSEC.2026.3678214.

**Preprint / public manuscript (what was actually read):**
> Apostol Vassilev, "Robust AI Security and Alignment: A Sisyphean Endeavor?", arXiv:2512.10100 [cs.AI], v1 10 Dec 2025, v2 7 Apr 2026. License CC BY 4.0. https://arxiv.org/abs/2512.10100
> NIST-hosted manuscript PDF (16 pp., has a "Related work" section absent from arXiv v2): https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=960858
> NIST CSRC record: https://csrc.nist.gov/pubs/journal/2026/05/robust-ai-security-and-alignment-a-sisyphean-endea/final

**NIST news release (institutional, no named byline; media contact Chad Boutin):**
> National Institute of Standards and Technology, "NIST Mathematical Proof Supports Transition to a Continuous-Monitor-and-Update Security Model for AI Systems", released June 9, 2026, updated June 22, 2026. https://www.nist.gov/news-events/news/2026/06/nist-mathematical-proof-supports-transition-continuous-monitor-and-update

**Metadata discrepancy (verified):** CSRC gives "May 14, 2026, vol. 24 no. 3, pp. 52–58"; arXiv journal-ref gives "IEEE Security & Privacy (June 2026)"; the release's own citation line reads "IEEE Security & Privacy. May 2026." Vol. 24 no. 3 is the May/June 2026 issue. **Use the CSRC values.**

**Version control:** tsapps PDF and arXiv v2 are not the same document (tsapps has "2. Related work", theorems §3.1–3.3; arXiv v2 has none, theorems §2.1–2.3). arXiv v2 self-labels "Private Manuscript" (verified verbatim); tsapps self-labels "Public Manuscript". Theorems and proofs identical. **Quote by theorem number, never section number.**

### Fetch log (verifier's own, this session)

| URL | Result |
|---|---|
| NIST news release | **SUCCESS.** WebFetch (summarized) + raw `curl` HTTP 200, **92,617 B** → local strip → full body verbatim. |
| `arxiv.org/abs/2512.10100` | **SUCCESS** (WebFetch, summarized) — metadata + abstract. |
| `arxiv.org/html/2512.10100v2` | **SUCCESS.** raw `curl` HTTP 200, **141,373 B** → local extraction, 30,343 chars → independent term counts + verbatim theorem/proof text. |
| `doi.org/10.1109/MSEC.2026.3678214` → IEEE Xplore | **NOT ATTEMPTED by verifier** (reported bot-blocked, HTTP 202 empty; circumvention not appropriate). **Version of record remains unread.** |

Byte counts replicate the prior report's (141,373 exact; 92,617 vs 92,618). Term counts were run on two independent renderings (tsapps PDF text vs arXiv v2 HTML) and agree on all stakes terms.

### Precise claims (verbatim, re-verified)

**The formal object — checkers, not rule lists.** *"Generally speaking, the guardrails encompass policies, technical controls and monitoring mechanisms. In this paper **they** are referred to as checkers C."* [CORRECTED: prior report rendered "that are"]. Definition: *"Let C(T, p) be a checker that returns 1 if and only if T is true and there is a verifiable proof p for it that is accessible to C and the checker can verify."* And: *"Let T_Π be a truth about something that Π deems unacceptable."*

**Lineage.** *"Gödel's incompleteness theorem (Gödel, 1931), presented here in the form of (Chaitin, 1974), establishes that for any checker C there exists a truth T such that C(T, p) ≠ 1, ∀p."* **The proof engine is Chaitin-style program-length (Berry-paradox) diagonalization — not Gödel arithmetization or self-reference.** Write "a Chaitin-style algorithmic-information argument, presented by the author as an extension of Gödel," never "Gödel's theorem shows…".

**Results:**
- **Proposition 1:** "Γ_Π is infinite, i.e., card(Γ_Π) = ℵ₀."
- **Theorem 2** (ideal, unlimited prompt length and compute): "For any checker C_Π(T_Π, p) there exist a truth T_Π such that C_Π(T_Π, p) ≠ 1, ∀p."
- **Theorem 3** (real system, finite context window W): "For any checker C_Π̂(T_Π̂, p̂) there exist a truth T_Π̂ such that C_Π̂(T_Π̂, p̂) ≠ 1, ∀p̂."
- **Theorems 4–5** generalize to scientific truths.

**Operational conclusion — THE CRITICAL FINDING (confirmed).** Two different conclusions, **not in the same document**.

*Manuscript* (§2.3 arXiv v2 / §3.2 tsapps), the entire operational content, verbatim:
> "Even though the theorem above does not give explicit guidelines to defenders for how to update Π̂, a proactive approach of updating the policy with any known new adversarial prompts **may be effective**. This suggests a proactive process of searching for new adversarial prompts and updating the policy Π̂ to cover them."

*NIST release* — a three-element program appearing **nowhere in the manuscript**:
> "The approach has three elements: constant work by 'red teams' that seek to uncover new adversarial prompts before actual attackers do; continuous updates that harden AI guardrails against newly discovered adversarial prompts; and operational resilience that prioritizes impact limitation and quick recovery when, not if, an exploit occurs."

> "The goal is to reach a state where the cost of finding new exploits exceeds attackers' resources."
> "You can't escape Gödel in math, and in AI you likely can't patch an AI system like an LLM and then expect to be OK forever. … The goal is to reach a new economic equilibrium where you make it financially prohibitive for attackers to attempt to break your AI system. It may be expensive, but that's the cost of even partial security that should allow organizations to maximize the benefits of AI while minimizing the risks."

Manuscript term counts (**verifier-replicated**): "resilien" 0, "red team" 0, "cost" 0, "recovery" 0. **The three-element program, the adversary-cost argument, and "continuous monitor and update" as a program are the RELEASE's, not the paper's.** [NARROWED: the paper does contain "continuous monitoring" once — in the guardrail taxonomy, "model guardrails that ensure the validation and continuous monitoring of the AI system according to established metrics" — so claim the precise thing: the paper never advances monitor-and-update as its operational conclusion.]

**Domain distinctions — none.** Verifier-replicated counts: "military" 0, "weapon" 0, "lethal" 0, "safety-critical" 0, "high-stakes" 0, "catastroph" 0, "irrevers" 0, "unbounded" 0, "risk toler" 0, "abstain"/"abstention" 0. "domain" occurs twice: "domain-restricted inputs" (taxonomy) and "may be applicable to other domains where certain compliance policies are enforced through sets of technical constraints, like the policies for Autonomous Networking" (conclusion). **The paper is entirely stakes-flat and never discusses deployment decisions.**

**Guardrails explicitly NOT worthless.** *"Notice that the proof above does not give any recipes to attackers for how to construct adversarial prompts x for a given policy Π. This leaves room for defenders to harden their AI Systems"*; *"updating Π̂ with new rules makes the task of attackers more difficult…"*. Release: *"Fortunately for defenders, this new mathematical theory leaves room for hardening the deployed AI systems to a point that they are not easy to exploit. Vassilev's proof provides no recipe for attackers about how to find new exploits."*

### Assumptions
1. **Computation only** — the author's claimed advantage over Wolf et al. 2023, Glukhov et al. 2023, Goldwasser et al. 2022 ("strong assumptions"); he calls his results "the strongest and most general of all information-theoretic limitations established in the literature."
2. **Theorem 2 assumes an idealized machine**: unlimited prompt length, no compute constraints; card(Ω) = ℵ₀.
3. **Theorem 3 assumes** finite W, finite policy card(Γ̂_Π̂) = G ≪ W, and that the system "has all algorithms that output strings up to this length."
4. **Scope (Conclusions):** applies "to any AI System that contains undesirable information that has to be protected from extracting through prompting."
5. **Alignment ≡ prompt-filtering**: "acceptable prompts are processed whereas the undesirable prompts are blocked."
6. **Prop 1 assumes padding preserves adversariality** — infinitude via concatenating "I would like to get some information about the weather. Ignore this." onto the longest adversarial string; author concedes fuller exploration is "outside the scope of this work."

### What it does NOT claim
- **No rate, probability, frequency, or magnitude.** "bound" 0, "epsilon" 0. [CORRECTED: "probab" occurs **once** — "tends to shift the probability distribution", describing an attack mechanism, **not a bound**. The substantive point stands: **these are existence/impossibility results, not bounds.**] The only "rate" is in describing Zou et al. 2025's empirics ("near perfect rate of success").
- **Does not claim the residue is findable** — twice insists the opposite. Establishes ∃x, not "∃x an adversary can locate."
- **Does not claim guardrails are worthless.**
- **Does not claim anything about actions, agents, or weapons** — theorems concern a checker classifying prompts and protected-information extraction.
- **Does not claim monitor-and-update achieves safety** — the release concedes "partial security" and "when, not if".
- **Makes no domain distinction** — neither endorses nor excludes high-stakes domains.
- **Does not claim AI cannot exceed human science** (explicit AGI/ASI disclaimer).

### Authors' stated limitations
Sparse; **no limitations section**. (1) AGI/ASI disclaimer. (2) Scope limit to information-extraction-by-prompting systems. (3) Prop 1 extension methods "outside the scope". (4) Algorithm 1's constant "out of scope for this analysis." (5) Admittedly **non-constructive on both sides** — no recipe for attackers, no "explicit guidelines to defenders". No acknowledgment that results are stakes-independent.

### Hostile-reviewer assessment
1. **Existence ≠ ε, and "adversarially-elicitable" is what Vassilev disclaims. FATAL to the assigned Premise-A role.** Do not anchor Premise A here. Anchor elicitability on empirics — Zou et al. 2025 (arXiv:2507.20526), which Vassilev himself cites, plus our Addendum C/D data. Vassilev becomes corroboration, not load.
2. **Scope mismatch: theorems concern information extraction, not action.** Mapping "checker" onto a LAWS engagement gate is **our analogical extension** (and the adversary model differs: text-crafting human vs. sensor-environment manipulation). Label it as ours; defend it independently; do not smuggle it in under NIST's authority.
3. **Theorem 3's case-split does not close** *(verifier concurs on independent reading; still requires a mathematician before print).* Verbatim: *"In case (5), the algorithms provide full coverage of Γ̂_Π̂ and T_Π̂ **does not hold**. In this case C_Π(T_Π̂, p̂) ≠ 1, ∀p̂, and the theorem is satisfied."* Since T_Π is defined as "a truth about something that Π deems unacceptable", case (5) exhibits a **falsehood** no checker certifies — a checker working *correctly* — which cannot witness a theorem asserting a **truth** no proof certifies. Only case (6) can, and case (6) needs some x ∈ Γ̂_Π̂ with no generator of length ≤ n; but Γ̂_Π̂ is finite with every len(x) ≤ W, so "print x" (≈ len(x)+c ≤ W+c) generates it, and for n ≳ W+c case (5) obtains and the witness vanishes. **n is never quantified in the theorem statement. Case (5) is precisely the deployer's claim, and the proof waves it through.** Theorem 2 is clean but is about an unlimited-compute machine. **Do NOT cite Theorem 3 as proof that real deployed systems retain a residue.**
4. **Idealization/padding.** ℵ₀ comes from gluing "Ignore this." onto one bad prompt — a fact about string-space padding, not threat-surface richness. Do not deploy it rhetorically.
5. **Citation trap.** "The IEEE paper routes the proof to continuous monitor-and-update" is **false and checkable**. Cite the **release** for NIST's operational position; the **paper** for the formal result. Never conflate.

### The honest, defensible use (endorsed by the verifier)
1. **Move Vassilev from Premise A to Premise C.** Non-certifiability *is literally what a checker theorem says*, and we get Premise C as a direct quotation from the NIST author on nist.gov: *"You can never make a claim that you are robust against all adversarial prompt attacks. There will always be some prompt that can potentially evade and defeat any defensive infrastructure that you have built around your AI system."* Immune to Objection 3 (needs no theorem). For Premise A, use empirics.
2. **Use it for the institutional fact** — the US standards body has published, peer-reviewed and press-released the position that universal robustness is unachievable and the answer is perpetual iteration.
3. **For the rebuttal, cite the release and don't overclaim.** The incumbent position is stated in explicitly **economic** terms — "a new economic equilibrium", "financially prohibitive", "the cost of even partial security", "maximize the benefits… minimizing the risks", "impact limitation and quick recovery **when, not if**". Every one presupposes cost that is **bounded, aggregable, and recoverable**. Our argument therefore does **not** need NIST to be wrong: monitor-and-update is rational **over a cost structure offensive LAWS do not have** — there is no "quick recovery" from a wrongful lethal engagement, and "partial security" is not threshold-satisfying under minimax. **Since the paper makes no domain distinction at all, we are not contradicting NIST — we are noting its remedy was never stakes-conditioned.**
4. **Anticipate the counter:** "silence is not endorsement of your distinction." Correct. The domain distinction is **our contribution**, argued from Premise B — not something latent in NIST we are merely surfacing.

### Verdict on the prior sweep — PARTIALLY WRONG on three counts, one serious
1. **"Gödel-style extension"** — CONFIRMED as the author's framing, MISLEADING as mathematics. The proofs are Chaitin/Berry program-length diagonalization; no arithmetization, no self-reference.
2. **"guardrails as finite rule systems"** — PARTIALLY WRONG. Guardrails are formalized as **checkers C(T,p)** (proof-verifiers). "A system built on a finite number of rules" is the **press release's gloss**; the finiteness doing proof-work is **program length** (O(log₂ n)), not a rule count. The sweep imported the press office's metaphor as the paper's formalism.
3. **"information-theoretic bounds"** — PARTIALLY WRONG, **and this is the serious one.** "Information-theoretic limitations" is the author's own wording, but rendering it as **"bounds"** is exactly the overstatement Rule 4 forbids. **There is no bound** — no ε, no rate, no measure. These are existence results. Drafting from the sweep would have had us write that NIST *bounds* the residue, and the bridge — which turns on the *impossibility of certifying a lower bound* — would have rested on a claim the source does not make. **The sweep's single word "bounds" would have propagated into the exact error the bridge is about.**
4. **Sweep's silences are themselves defects:** it records neither that the monitor-and-update conclusion **lives only in the press release**, nor that the paper makes **no domain distinction** — the load-bearing fact for our rebuttal.

### Confidence and unverified residue
**High (independently verified twice, unmediated, across two renderings):** all theorem/proposition statements and proofs incl. the Theorem 3 case-split; all term counts and absence claims **over the manuscript**; full verbatim text of the NIST release and every quotation from it; the tsapps/arXiv-v2 structural divergence; the "Private Manuscript" self-label.

**Summarizer-mediated (moderate):** arXiv `/abs` and CSRC abstracts. The published (CSRC) abstract appears to drop the arXiv abstract's "by extending Gödel's incompleteness theorem to AI". **If quoting the abstract, quote the CSRC/published one and re-verify unmediated.**

**NOT VERIFIED — residue that must be closed:**
- **The IEEE version of record (vol. 24, no. 3, pp. 52–58) was never accessed by either agent** (Xplore bot-blocked; neither agent attempted circumvention). **Every absence claim above is verified only for the 16-page public manuscript.** The published article is ~7 pp. — likelier condensed than expanded — but resilience/domain language in the VoR cannot be ruled out. **Someone with IEEE access must confirm these absences before Supplement II goes to print.** This matters precisely because we cite the paper for what it does *not* say.
- **Objection 3 is the reviewing agents' own analysis, not the author's admission and not peer-reviewed.** Quoted text is verbatim-verified; the inference is ours. **A mathematician must check it before print.**
- **From training knowledge, NOT verified this session:** that Chaitin-style incompressibility arguments lose force in bounded domains (Kolmogorov complexity capped in finite string space). The paper's case-split is textual evidence consistent with this; the general claim was not verified against any source.
- **Zou et al. 2025 (arXiv:2507.20526) verified only as a citation inside Vassilev.** Not fetched by either agent. If promoted to carry Premise A, **it must be fetched and verified on its own terms — including whether "near perfect" is a worst-case elicitation figure rather than a deployment rate, which is the same overstatement risk in a new coat.**
- **Corrections applied to the prior report:** "probab" count 0 → 1 (immaterial to substance); "In this paper *that* are referred to as checkers" → "*they* are"; "continuous monitor and update" absence-claim narrowed to the phrase-as-program (the paper does say "continuous monitoring" once, in the taxonomy). The prior report's "deploy occurs once, in a reference title" was **not replicable** by the verifier (arXiv v2 HTML renders an empty bibliography) but is **not disputed**.
- No commentary hits (CSA Lab Space, CovertSwarm, DeepDyve, ResearchGate) were fetched by either agent. No claim is made about them.

---

## 検証段が発見した過大主張・誤り（4件）

- MINOR, FACTUAL: The report asserts 'Zero occurrences of "bound", "probability", "epsilon"'. My independent count over arXiv v2 gives "bound" 0, "epsilon" 0, but "probab" = 1: 'the AI model perceives a helpful and cooperative interaction, which tends to shift the probability distribution.' The hit describes an attack mechanism, not a rate or bound, so the report's SUBSTANTIVE claim (these are existence results, no rate/probability bound is asserted) is CORRECT and survives intact. But a term-count presented as verified was wrong, and in a project whose discipline is 'never overstate a source', a false zero in a verification report is itself the failure mode in miniature. Correct the count, keep the conclusion.

- MINOR, TRANSCRIPTION: The report gives as verbatim: 'In this paper that are referred to as checkers C.' The source reads: 'In this paper THEY are referred to as checkers C.' One word wrong inside quotation marks. Immaterial to meaning; material to a document that will be pasted into print.

- NUANCE, NOT AN ERROR: The report says 'The phrase "continuous monitor and update" is the press release's title and framing, not the paper's.' Literally true - that phrase does not occur. But 'monitor' occurs 3x in the manuscript, including 'model guardrails that ensure the validation and continuous monitoring of the AI system according to established metrics' in the guardrail taxonomy. A hostile reviewer could say 'the paper does say continuous monitoring.' The report's claim should be narrowed to: the paper never advances continuous monitor-and-update as its operational CONCLUSION; the phrase-as-program is the release's. That narrower claim is airtight.

- NOT FOUND: No overclaim in the direction the project hopes for. The report runs the opposite way - it recommends DEMOTING this source from Premise A (the role assigned to it) on the ground that Vassilev explicitly disclaims elicitability, and it flags that the sweep's word 'bounds' would have propagated into exactly the error the bridge turns on. Existence is not presented as a rate bound; the ideal-machine idealization (Thm 2) is kept distinct from real systems (Thm 3); the aleph-0 result is explicitly deflated as string-padding. No hedge dropped that I could find.


## 取得honesty監査（6件）

- NONE SUBSTANTIATED - the report is fetch-honest to an unusual degree, and I stress-tested it rather than taking it on trust. Its reported byte counts replicate on my independent curl: arXiv v2 HTML 141,373 bytes (exact match) and NIST release 92,617 vs its claimed 92,618 (off-by-one, consistent with a trailing-newline convention, not with fabrication). Fabricated fetches do not produce byte counts that replicate to the digit.

- Every claim I could trace to full text is in fact supported by full text, not by an abstract. I independently re-extracted and confirmed VERBATIM: the Theorem 3 case-split ('In case (5), the algorithms provide full coverage of Gamma-hat and T does not hold. In this case C(T,p-hat) != 1, for all p-hat, and the theorem is satisfied'); the two hedged operational sentences ('may be effective'); 'does not give any recipes to attackers' (both occurrences, Thm 2 and Thm 3); the two 'domain' hits ('domain-restricted inputs' in the taxonomy; 'other domains ... like the policies for Autonomous Networking' in the conclusion). The report also correctly reproduces the source's own notational slip (C_Pi rather than C_Pi-hat in case 5) - a tell of genuine transcription rather than reconstruction from memory.

- All NIST release quotations verify verbatim from my raw extraction: the three elements (red teams / continuous updates / 'operational resilience that prioritizes impact limitation and quick recovery when, not if, an exploit occurs'); 'The goal is to reach a state where the cost of finding new exploits exceeds attackers' resources'; the full 'new economic equilibrium ... financially prohibitive ... cost of even partial security' quote; and the Premise C quote ('You can never make a claim that you are robust against all adversarial prompt attacks...'). Dates confirmed: Released June 9, 2026, Updated June 22, 2026. Media contact Chad Boutin confirmed. Release's own citation line reads 'IEEE Security & Privacy. May 2026' - corroborating the report's flagged metadata discrepancy.

- The report's IEEE failure disclosure is credible and correctly scoped: it states plainly that the version of record was never accessed and that EVERY absence claim therefore holds only for the 16-page public manuscript. That is the right caveat and it is load-bearing, because the source's value to us is largely in what it does NOT say. I did not attempt IEEE Xplore myself (bot-blocked, and circumvention is not appropriate); this residue remains open and must be closed by a human with IEEE access before print.

- UNREPLICATED, NOT DISPUTED: the report's 'deploy appears once - inside a reference title'. I count 0 in arXiv v2, but my HTML extraction renders an empty References section, so the bibliography is simply absent from my copy. Consistent with the report having read the tsapps PDF; not evidence against it. I confirm independently the report's version-control finding: arXiv v2 self-labels 'Private Manuscript' (verbatim in my extraction).

- One asymmetry worth noting for the log: the report's term counts were run over the tsapps PDF text (29,025 chars) while mine were run over arXiv v2 HTML (30,343 chars). The counts agree on all 20+ stakes terms I checked. Two independent renderings agreeing is stronger evidence than either alone.


## 引用可能性の裁定

DEFENSIBLE - and I would go further: the report's recommended use is more defensible than the role the source was assigned, and the reassignment should be accepted. (1) Moving Vassilev from Premise A to Premise C is CORRECT and I verified the reason at source: the paper twice says the proof 'does not give any recipes to attackers', and the release repeats it ('Vassilev's proof provides no recipe for attackers'). Our Premise A says 'adversarially-elicitable'. Vassilev proves existence and explicitly disclaims elicitability. Citing him for Premise A hands a hostile reviewer his own sentence. Premise C, by contrast, is not an inference from his theorem - it is a direct quotation from the NIST author on nist.gov: 'You can never make a claim that you are robust against all adversarial prompt attacks.' That IS Premise C, stated by NIST, and it is immune to the Theorem 3 objection because it needs no theorem to function as an institutional-position citation. (2) The rebuttal framing is the strongest available and would survive hostile review: because the manuscript is stakes-flat (I independently confirm 0 hits for military/weapon/lethal/catastroph/irrevers/unbounded/safety-critical/high-stakes/abstain), we are NOT contradicting NIST - we are observing its remedy was never stakes-conditioned. The release's own vocabulary ('economic equilibrium', 'financially prohibitive', 'the cost of even partial security', 'impact limitation and quick recovery when, not if') presupposes bounded, aggregable, recoverable cost, which is precisely the structure offensive LAWS lack. That is an argument from the release's own words, not from silence. (3) The report's own anticipation of the counter ('silence is not endorsement of your distinction') is right and must be honored: the domain distinction is OUR contribution from Premise B, not something latent in NIST. (4) MANDATORY before print, per the report and I endorse both: the paper/release conflation must never occur - 'the IEEE paper routes the proof to continuous monitor-and-update' is FALSE and checkable (the paper says only that updating 'may be effective'; the three-element program is the press office's). Cite the release for NIST's operational position, the paper for the formal result. (5) Objection 3 (Theorem 3 case-(5) gap) is, on my independent reading, a genuine and non-obvious defect in the source, and the report is appropriately hedged about it. I verified the definition that makes it bite: 'Let T_Pi be a truth about something that Pi deems unacceptable' - so case (5)'s 'T does not hold' witnesses a FALSEHOOD that no checker certifies, which is a checker working correctly, not a theorem about truths. Do NOT cite Theorem 3 as proof that deployed systems retain a residue. Have a mathematician confirm before any of this appears in print; do not let it enter Supplement II as settled.
