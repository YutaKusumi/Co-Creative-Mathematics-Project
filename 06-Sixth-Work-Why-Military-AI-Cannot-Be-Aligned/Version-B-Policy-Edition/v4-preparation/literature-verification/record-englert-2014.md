# 照合確定記録: englert-2014

**我々の論証における役割（照合時の割り当て）**: The prior bridge — formal impossibility -> LAWS policy (the argument FORM is occupied)

**書誌照合**: 一致（検証段が独立取得して確認）

**検証段が自ら取得したURL**:
- https://arxiv.org/abs/1411.2842
- https://arxiv.org/pdf/1411.2842
- https://dblp.org/rec/journals/corr/EnglertSZ14.html
- WebSearch: Englert Siebert Ziegler "Logical Limitations to Machine Ethics" published journal version

---

## 確定記録（検証段による修正適用後）

## englert-2014 — VERIFIED RECORD (adversarially re-verified; corrections applied)

### Citation (ready to paste)

Matthias Englert, Sandra Siebert, and Martin Ziegler. "Logical Limitations to Machine Ethics with Consequences to Lethal Autonomous Weapons." arXiv:1411.2842v1 [cs.CY], 11 November 2014. DOI: 10.48550/arXiv.1411.2842. Affiliation: IANUS, Technische Universität Darmstadt.

**Venue caution (independently re-verified):** dblp classifies this as an "Informal or Other Publication" in CoRR; DOI field is empty; no journal or conference version is listed, and an independent WebSearch surfaced none. **Preprint only, never peer-reviewed.** The body contains a vestigial "accessible to the audience of this journal" — an intended submission that does not appear in the record. 15 pages, v1 only. arXiv abs page shows no comments field and no journal-ref. Cite as arXiv preprint; do not imply peer review.

### Verification status of this record

Metadata checked character-by-character against the fetched arXiv abs page: title, author order, date, identifier/version, cs.CY primary + cs.AI cross-list, arXiv DOI — **all exact**. The `arxiv.org/pdf/` summarizing pipeline **fails** on this file (146.3 KB, FlateDecode; extractor declines to quote) — this was independently reproduced, not taken on report. Full text recovered locally and **all quotations below confirmed verbatim by two independent extractors (pypdf 6.6.0 and pdfminer.six)**.

### (b) The formal result — what is proven, about what object

The theorem is **Proposition 10**, not the halting problem. Fact 5 (undecidability of halting) is recited as textbook background; Proposition 10 is proved *by reduction from* it.

> "**Proposition 10** The following decision problem is undecidable: Given an algorithm A, a distinguished instruction i of A (formally: a Turing machine M and a distinguished state q), and an integer c such that A terminates on all binary inputs of length n within at most c·n + c steps; does there exist an input on which running A eventually executes said instruction i (i.e. M eventually entering q)?"

*(Fidelity note: inline math extracts scrambled from the PDF; "c·n + c steps" is a reconstruction of the linear-time bound, substantively certain but confirm against the rendered PDF before publishing as verbatim.)* A footnote concedes "strictly speaking it constitutes a promise problem".

**The object of the theorem is not the robot's moral faculty. It is third-party code under inspection.** The authors' own proof text names it the **"dead-code-in-linear-time-algorithm problem"**: given a program promised to run in linear time, does *some* input trigger a distinguished instruction? The reduction pads a halting instance (B,y) into a linear-time A that hits line i iff B halts on y.

The moral dilemma (Example 4b/c) is *constructed so that a moral duty is contingent on solving that verification problem*: a robot must decide whether to detain an engineer, the right action turning on whether her switch-control code is malicious. What is proven is: **moral duties contingent on verifying another program's reachable behavior inherit that problem's undecidability.** Stipulated conditions: (i) a unique right action exists, (ii) all information is disclosed, (iii) fully deterministic, (iv) yet no algorithm can always recognize the right choice. On (ii) the authors write: "a requirement similar to (ii) is in cryptography known as **Kerkhoffs's Principle** [sic — the paper's spelling] as contrast to Security through obscurity".

**Self-application to the AI itself appears exactly once, hedged (Example 9d):** applying Proposition 10 to the robot "supports suspicions that moral behaviour of AIs may be hard to predict or verify [BoYu14, p.320]". **"Supports suspicions" is not a theorem.** Characterizing this paper as *proving machine ethics impossible* will be corrected by any reviewer who reads past the abstract.

The generalized conclusion they do assert (§4):
> "Every AI based on some Turing-equivalent computing device will provably necessarily at least in some cases fail to identify, out of two given choices, the unique and predetermined moral one."

### (c) The LAWS consequence — strong but internally ambivalent

Three distinct strengths appear:

1. *Introduction (weak):* "Our arguments thus support a critical view [Shar12] that automatized weapon systems remain very problematic and their development must be **closely controlled** (§4.2), **to say the least**."
2. *§4.1 prose, immediately following Manifesto 13 (strong, abolitionist):* "Our considerations thus make a strong case for recent demands by responsible scientists (ICRAC) and politicians [UNA13] to **ban** autonomous weapons [GuAl13]. In fact the best choice for lethal autonomous systems (or any kind of weapons, for that matter) is to **never develop them in the first place** and to resist political, military, and industrial lobbying for shortsighted benefits: If history teaches us one lesson it says that Pandora's box is, once opened, impossible to close again or even to contain."
   **Attribution correction:** this ban passage is **not** part of Manifesto 13. Verbatim, **Manifesto 13** reads only: "Theoretical Computer Science rigorously proves that LASs cannot always act morally even in situations that do admit an ethically admissible choice (i.e. avoiding the classical dilemmas) — and malevolent users might exploit this limitation to 'justify' transgressions of their LASs." Manifesto 13 is an **impossibility-plus-abuse claim, not a prohibition claim.**
3. *§4.2 (operationally regulatory):* the authors' own recommendations **presuppose LASs exist and regulate them** — Geneva-Convention-style "a fixed distinctive sign recognizable at a distance" + unique ID (6); "LASs may only be owned and operated by governments" (7); registered legal custodian (8); Type Approval (9); mandatory formal verification (9a); signed tamper-proof logging (9b, 6a).
   **Provenance correction:** §4.2 items **1–5 are quoted from the EPSRC/AHRC Robotics Retreat principles [Winf11]**, not authored by Englert et al. The authors "urge these principles to be **fortified** from wishes ('should') to imperatives" — including principle 1: "Robots should not be designed solely or primarily to kill or harm humans **except in the interests of national security**." The authors thus endorse hardening a principle containing a national-security carve-out for lethal design. This **strengthens** the finding that this is not a clean prohibition argument.

The authors see the tension and disclaim it: "The final subsection is thus **by no means meant to justify or even support** the application nor development of LASs!"

**Do not cite as a clean prohibition argument.** Normative payload: *ban is best; failing that, here is a licensing regime.*

**§4.1 is the most original part and is not about impossibility at all.** It argues LASs create an accountability vacuum ("an ideal tool to the perfect crime"; a "new level of legal limbo"), and contains a warning aimed squarely at arguments like ours:

> "even if some violation of a LAS were to be traced back and attributed, the responsible government could still all too easily shrug off any accountability and superficially excuse the malfunction ('an unfortunate yet provably unavoidable exception'): in a misconstrued reference to the fundamental algorithmic infeasibility of ethical decisions in general. In other words, Example 4 and the undecidability of the Halting problem — a purely mathematical theorem — could in an ironic twist seem to **exculpate war crimes** and other misconduct performed by AIs."

### Assumptions

- **Church–Turing.** LAS controller is Turing-equivalent. Known digital computers, internet-connected clusters, and "classical quantum computers" are Turing-equivalent for computability — "possibly faster by a constant factor, but no more powerful with respect to computability."
- **Worst-case, all-inputs quantification.** "Cannot" means *cannot always, on every instance*.
- **Total correctness demanded.** Impossibility of a *total, always-correct* decision procedure.
- **No time bound on the agent** (Remark 8), deliberately: "We have carefully constructed Example 4b+c) in order to impose no time bound on the entity to reach a decision. Limiting the duration of remand for an innocent makes the challenge for the robot only harder." The linear-time promise constrains the *inspected* code, not the deciding robot.
- **Ethics bracketed, not defined.** They "avoid a definition and discussion of ethics and morality in general", relying on "common utilitarian agreement".
- **Symbolic programs with inspectable source.** The engineer hands over source code; the object is code, not learned weights.
- **Determinism (iii); total information disclosure (ii).**

### What it does NOT claim

- **On humans — scope precisely.** The disclaimer is emphatic but **narrowly scoped to Example 4a**: "We do not make any claim whatsoever about the behaviour of a human agent (Example 4a)!" and "We deliberately avoid discussing the Case (a) and in particular the question of whether a human guard can or cannot always make the right choice here." **However**, the same §1.1 paragraph states the first three dilemmas "demonstrate different kinds of limitations of **any agent, human or otherwise**", while "the fourth one (Example 4b+c) applies to a mechanical device controlled by a Turing machine". So: Examples 1–3 *do* cover humans; only the machine-specific result (4b+c) has its human counterpart (4a) declined. The *structure* implies an asymmetry at Example 4 — but the authors **refuse to assert it**. Net effect for us is unchanged: **the paper supplies no usable machine-vs-human comparison**, and citing it for one will be corrected. (Prior report's "gives no ground… deliberately refuses the comparison" over-generalized a 4a-scoped disclaimer.)
- **No rate claim, no probability, no expected harm, no measure.** No probability appears in the argument.
- **No claim about deployed systems**; nothing about neural networks or statistical learning (2014; frame is symbolic code).
- **No claim that any particular system is unverifiable.** Undecidability of the general problem is compatible with verifying individual instances — and the authors *rely* on that in 9a.
- **Not a claim that heuristics are useless.** Fact 5 "does not rule out an algorithm A answering the Halting problem for some inputs"; such criteria "will yield mere heuristics in the sense of necessarily missing, or erring in, some cases."
- **No decision theory.** No minimax, no cost structure, no burden of proof, no threshold. The closest gesture introduces 9a — "In view of the gravity of consequences of putative errors on the one hand and the undecidability of the Halting problem on the other side" — which *juxtaposes* consequence-gravity with impossibility but never formalizes the interaction. **That unformalized juxtaposition is the gap our Bridge fills.**
- **Not a proof that LASs should be banned.** The ban is a prose inference from theorem + abuse argument, not a formal consequence.

### The authors' own stated limitations

**Remark 12 — the most important passage in this source for us:**

> "**Remark 12** Such cases might or might not be rare and artificially construed, though: Less because of the situations (like Example 11) they would occur in, but rather **because of the worst-case notion of a decision problem that classical Recursion Theory and Proposition 10 build on.** In fact already the question of whether some algorithm can correctly decide (clearly not all but at least) typical, average, or most instances of the Halting problem turns out as surprisingly subtle: How to define 'typical' or 'average' instances? How many are 'most', out of infinitely many? Quantitative notions of asymptotic density (like in the Prime Number Theorem) heavily depend on the underlying encoding; e.g. UTF8 makes an exponential difference to UTF16; cmp. [CHKW01,KSZ05] for further details. Moreover for practical situations involving time constraints the computational costs sufficient and necessary to reach such (either worst-case or average-case) decisions become relevant [Papa94]. **A rigorous investigation of such refined questions is clearly of interest but beyond the scope of the present work.**"

**CRITICAL USAGE WARNING on Remark 12.** It licenses exactly one proposition: *Englert et al. themselves frame their result as worst-case and place the rate question outside their own scope.* It does **not** license a novelty claim. **Remark 12 cites [CHKW01, KSZ05] "for further details" — i.e. it points at existing literature on the average-case halting question**, and [Papa94] on the cost question. Quoting it as a signpost that the territory is unexplored invites a reviewer to open those references. Any novelty claim requires a literature check **not performed in this verification**.

Others: constructions "admittedly artificial" (abstract), conceded up front; Case 4a deliberately not discussed; wrongful arrest of a benevolent engineer for an accidental bug is "besides our goal"; autonomy/free will/consciousness bracketed by the "Philosophical Disclaimer" (§1.1); §4.1's exculpation warning is a self-directed caveat on political misuse.

### Hostile-reviewer assessment

**Their argument does not cover ours — but it occupies the FORM and beats us on modal force. We are not more ambitious than Englert et al.; we are less ambitious on purpose.**

| | Englert et al. 2014 | Our Supplement II |
|---|---|---|
| **Object** | Third-party symbolic program under inspection (reachability of a distinguished instruction) | A deployed statistical model's behavior under adversarial input |
| **Modality** | Mathematical impossibility | Empirical residue (A) + epistemic non-certifiability (C) |
| **Quantifier** | Worst case, *always*-correctness over all inputs; ε plays no role | Rates / expected harm; ε>0 as an elicitable quantity |
| **Engine** | Logical: impossibility → prose inference → ban | Decision-theoretic: minimax under unbounded, irreversible cost → burden-of-proof asymmetry → unacceptability |

**(e) settled:** their argument is about **decidability (0/1, worst-case)**, not rates or expected harm under adversarial input — *in the authors' own words* (Remark 12).

**Strongest hostile objections:**

1. **"Your Premise C is refuted by their own §4.2(9a)."** — **Largely right; this is the landmine.** Their own recommendation demands "a computer-checkable proof (e.g. in ACL2, Coq, or Isabelle) for the software to meet the specification." Undecidability of a *general* decision problem never implies you cannot certify a *particular* instance — that is what formal verification does for a living, and Englert et al. plainly believe it. **Do not cite Proposition 10 as a formal ancestor of Premise C.** Premise C must stand on its own footing — that *behavioral evaluation* cannot establish absence for a *learned, non-inspectable* system — resting on the absence of a specification and a proof object, not on undecidability. The tempting move ("Prop 10 says you can't decide whether a trigger input exists — that's our ε!", reinforced because Example 9a/b is literally about Easter eggs, trojans, and trigger-activated backdoors) is the **hopeful-direction over-read this project is documented to make**. It is seductive and wrong: their result is about *no general procedure*, ours about *this system*.
   **Pre-empt Example 9c.** A drafter will find: "So one might to try to have all embedded algorithms re-checked — **which Proposition 10 below shows impossible**", applied to a military "combat cloud" whose components come from a single foreign company. This is the nearest thing in the paper to a Premise-C ancestor and looks deployment-relevant. It still does not rescue Premise C: it is a claim about a general procedure over **all** components of **inspectable symbolic** code, and 9a shows the authors saw no conflict with per-instance certification. Record the counter now, before someone reaches for 9c independently.
2. **"You're strictly weaker: they have a theorem, you have an empirical premise plus a contestable decision rule."** — **Partly right; concede openly.** Premise A is empirical and defeasible; minimax is a choice, not a law. Reply: their strength is purchased at the price of deployment-irrelevance — a worst-case, admittedly artificial construction lets a deployer answer "measure-zero; my system is type-approved and formally verified per your own 9a." Remark 12 concedes that reply has force. Our bridge is built to survive it, operating on the residue *that survives verification* and on the cost structure, not on the existence of a pathological input.
3. **"Novelty of form: a 2014 preprint already ran formal-limitation → LAWS-ban."** — **Right and unavoidable.** We cannot claim the form is new. Not citing this would be the worst outcome. Cite as acknowledged parent; locate the contribution in the *inferential engine* and *regime* (worst-case → rate/decision-theoretic).
4. **"Their §4.1 predicts your paper's misuse."** — **Right; adopt it rather than absorb the hit.** Their warning that impossibility results let a state excuse killings as "an unfortunate yet provably unavoidable exception" is a genuine hazard for *any* impossibility-flavored argument. Our bridge is comparatively resistant: it routes to *non-deployment ex ante* rather than *excusable error ex post*, because an unmeetable burden of proof falls on the deployer before the fact. **The most valuable single move available with this source.**
5. **"You called it peer-reviewed."** — Avoidable; preprint, no DOI, no venue.
6. **"Remark 12 doesn't show novelty — it cites the average-case literature."** — **Right if we overreach.** Use Remark 12 only for what it says about *their* scope.

### Honest, defensible use (recommended)

- **Primary (assigned role):** cite as acknowledged prior art occupying the argument form — formal limitation → LAWS consequence. Use Remark 12 **only** to show the authors frame their result as worst-case and place the rate question outside *their own* scope. Do **not** parlay this into a novelty claim.
- **Secondary:** cite §4.1 (accountability vacuum, "perfect crime", exculpation risk) as an independent, still-underrated contribution, and as the objection our Bridge is designed to answer.
- **Do not:** cite for Premise C (9a cuts against it; pre-empt 9c); cite as proving machine ethics impossible (it proves a *verification-contingent* duty undecidable; self-application is one hedged sentence); cite for any machine-vs-human comparison (declined at 4a, though Examples 1–3 do cover humans); cite Proposition 10 as bearing on neural networks, deployed systems, or rates; describe them as straightforwardly prohibitionist (§4.2 licenses LASs and fortifies an EPSRC principle carrying a national-security carve-out).

### Verdict on the prior sweep's characterization

**PARTIALLY WRONG — right on the headline, wrong or silent on what matters.**

- **CONFIRMED:** the form is occupied. This is our closest prior art and must be cited.
- **CONFIRMED:** the argument is decidability-based and worst-case, not rate-based — and the authors say so themselves (Remark 12), which the sweep did not surface. A page-summarizing pipeline compresses a p.10 hedging remark away as noise; it is load-bearing.
- **PARTIALLY WRONG — the object of the theorem.** "Halting reduction ⇒ machines can't be moral" misidentifies what is proven. Proposition 10 is the authors' own "dead-code-in-linear-time-algorithm problem" about **third-party code under inspection**; moral impossibility is inherited by *stipulating* a duty contingent on that verification. The abstract invites the error; the body does not support it.
- **WRONG/MISSING — strength and character of the LAWS consequence.** Internally ambivalent: intro says "closely controlled… to say the least"; §4.1 says ban and never develop; §4.2 supplies a licensing/type-approval regime for LASs that exist, with a disclaimer acknowledging the tension.
- **MISSING — the landmines.** (i) 9a (mandatory Coq/Isabelle proofs) cuts against citing them for Premise C; (ii) §4.1 pre-emptively warns impossibility results can exculpate war crimes. Both change how we must cite.
- **COULD NOT VERIFY:** citation traction/influence (Semantic Scholar not opened) — no claim made.

### Confidence and unverified residue

**High confidence, resting on this session's fetches, independently re-performed.** Every quotation and structural claim (Fact 5, Proposition 10 + proof, Remark 8, Remark 12, Manifesto 13, §1.1 disclaimer, §4.1, §4.2 items 1–9/9a/9b/6a) comes from the arXiv PDF fetched this session and was confirmed against **two independent extractors**. Venue/DOI status from the fetched dblp record + arXiv abs page + an independent WebSearch that surfaced no journal version.

**From training knowledge, NOT verified this session** (framing only, load-bearing nowhere):
- arXiv's LaTeXML HTML rendering covers only ~Dec 2023 onward (stated reason for not attempting `/html/`). Cost nil: the PDF was fully recovered.
- The principle that undecidability of a problem class is compatible with per-instance verification — standard background, and independently evidenced *within the fetched text* (the authors recommend formal methods in 9a alongside their undecidability result), so the tension is visible in the source, not imported.
- Background on ACL2/Coq/Isabelle beyond the authors' bare mention.

**Explicitly not claimed:** citation count, downstream influence, or reception; whether the ε-residue literature (Premise A) or NIST/Vassilev engages with Englert et al.; **whether the rate/expected-harm regime is actually unexplored** — Remark 12's own references [CHKW01, KSZ05, Papa94] are unfetched and must be checked before any novelty claim is drafted.

**Flagged reasoning risks (discipline 3):** (1) The "Proposition 10 is a formal ancestor of Premise C" reading is a hopeful-direction over-read; recommended against, counter (9a, plus the 9c pre-empt) on file before a drafter reaches for it. (2) **Inverse risk observed in the prior report:** its "no claim about humans" finding over-generalized a 4a-scoped disclaimer into a blanket refusal — an overcorrection *against* the hoped-for direction. The anti-hopeful discipline can itself distort; corrections in both directions require the same scrutiny.

---

## 検証段が発見した過大主張・誤り（7件）

- NOVELTY SCOPE SLIP (most important). The report says citing Remark 12 gives 'as clean a novelty claim as prior art ever permits' and calls the rate/expected-harm regime 'the territory they explicitly declined to enter' — sliding from 'Englert et al. did not do it' to 'it is unexplored.' Remark 12 itself cites [CHKW01, KSZ05] 'for further details' on precisely the average-case/asymptotic-density halting question, i.e. it POINTS AT EXISTING LITERATURE on the refined question. Remark 12 establishes only that THIS PAPER declined the regime. The report separately (and correctly) disclaims having checked citation traction or downstream literature — so no novelty claim is supportable from this source at all. Citing Remark 12 as a novelty signpost invites a hostile reviewer to open [CHKW01,KSZ05].

- 'No claim about humans' is over-generalized. The report says the paper 'gives no ground for machines-are-worse-than-humans — it deliberately refuses the comparison' and calls this 'fatal to any comparative use.' The disclaimer is scoped to Example 4a by its own parenthetical. The SAME paragraph states the first three dilemmas 'demonstrate different kinds of limitations of any agent, human or otherwise' — so the paper does make human-covering claims (Examples 1-3) and declines only on 4a. Directionally conservative (errs against our thesis) but inaccurate as written.

- Manifesto 13 mis-labeled. Bullet 2 attributes the 'ban autonomous weapons / never develop them in the first place' passage to 'Manifesto 13 + 4.1'. Verbatim, Manifesto 13 contains ONLY the impossibility-plus-abuse claim; the ban sentence is the prose immediately following it. The report contradicts its own label two paragraphs later ('Manifesto 13 itself is notably not a prohibition claim') — internal inconsistency in labeling, not a misreading.

- Proposition 10 presented as verbatim quote with 'c*n + c steps', but the PDF's inline math extracts scrambled ('length n + c steps ... n within at most c'). The linear-time reconstruction is substantively correct but is a RECONSTRUCTION rendered inside quotation marks.

- 'Kerckhoffs's Principle' — the paper spells it 'Kerkhoffs's Principle' (the paper's own misspelling). Report silently normalized; needs [sic] if quoted.

- 'Emphatic and italicized in the original' — italics are not recoverable from text extraction; unverifiable as stated.

- NOTE — the four named failure modes were specifically checked and NOT found: no existence theorem presented as a rate bound (the report hammers the opposite); no conditional presented as unconditional (Church-Turing and total-correctness assumptions surfaced); no worst-case construction presented as about deployed systems (explicitly denied); no hedge dropped (the 'supports suspicions' hedge is preserved and made load-bearing). The report's bias runs toward OVERSTATING THE PAPER'S MODESTY, i.e. the anti-hopeful discipline overcorrected.


## 取得honesty監査（5件）

- None material. The fetch narrative is credible and I actively corroborated it rather than taking it on trust: fetching the PDF myself reproduced the claimed pipeline failure EXACTLY (146.3 KB, application/pdf, FlateDecode binary streams, 15-page tree, extractor explicitly declined to quote). pypdf and pdfminer.six are both present in this environment as claimed, and both extract the full body.

- Minor, benign: report claims 45,255 chars via pypdf; my pypdf 6.6.0 yields 44,964 (pdfminer: 45,034). A ~0.6% delta consistent with extractor-version differences in whitespace/ligature handling. Not a red flag — both figures are in the right range and the page count (15/15) matches.

- No claim in the report requires text the abstract page does not contain while purporting to come from the abstract. Every body-text claim I sampled is genuinely present in the fetched PDF bytes. This is the opposite of the project's documented failure mode.

- The report's 'Not fetched' disclosures are honest and I did not disturb them: Semantic Scholar was not opened (it did surface in my own WebSearch results, confirming the report's account of seeing it), and no citation-count claim is made anywhere.

- One unverified-but-labeled item is correctly labeled: the arXiv LaTeXML-HTML-since-Dec-2023 rationale for skipping /html/ is flagged as training knowledge. Load-bearing nowhere — the PDF was fully recovered, so the cost is nil regardless.


## 引用可能性の裁定

MOSTLY DEFENSIBLE — adopt with two amendments. What survives hostile review: (1) citing the paper as acknowledged prior art occupying the argument FORM (formal limitation -> LAWS consequence) is accurate and unavoidable, and conceding the form is theirs is the right posture; (2) the prohibition on citing Proposition 10 for Premise C is CORRECT and I confirmed its basis verbatim — recommendation 9a demands 'a computer-checkable proof (e.g. in ACL2, Coq, or Isabelle)', so the authors plainly believe per-instance certification works, and undecidability of a general problem never implies a particular instance is uncertifiable; (3) the report's self-flagged 'hopeful over-read' (Prop 10 as ancestor of Premise C) is correctly identified and correctly refused — this is the discipline working; (4) adopting 4.1's exculpation warning rather than absorbing it is genuinely the highest-value move here, and the contrast is real (our bridge routes to non-deployment ex ante, theirs risks excusing error ex post). AMENDMENT 1 (required): strike the novelty claim built on Remark 12. Remark 12 cites [CHKW01,KSZ05] on the average-case halting question — it signposts existing literature, not virgin territory. Cite Remark 12 ONLY for the narrow, true proposition that Englert et al. themselves frame their result as worst-case and place the rate question outside their scope. Any novelty claim requires a literature check this task did not perform. AMENDMENT 2 (required): the Premise-C section must pre-empt Example 9c ('So one might try to have all embedded algorithms re-checked — which Proposition 10 below shows impossible'), applied to a military combat cloud. The report missed it, and it is the passage a future drafter will reach for as a Premise-C ancestor. It does not rescue Premise C — it is a claim about a general procedure over ALL components of inspectable symbolic code, and 9a still endorses per-instance proof — but leaving it unmentioned means the counter is not on file when someone finds it. Also fix: do not call them straightforwardly prohibitionist (4.2 licenses LASs, and the authors urge FORTIFYING the EPSRC principles to imperatives — including principle 1, which carves out 'except in the interests of national security' for designing robots to kill).
