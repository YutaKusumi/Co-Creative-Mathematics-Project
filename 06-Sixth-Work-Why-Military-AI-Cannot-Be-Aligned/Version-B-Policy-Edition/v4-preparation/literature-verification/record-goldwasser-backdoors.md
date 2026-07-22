# 照合確定記録: goldwasser-backdoors

**我々の論証における役割（照合時の割り当て）**: Premise C — cryptographic impossibility of detection

**書誌照合**: 一致（検証段が独立取得して確認）

**検証段が自ら取得したURL**:
- https://arxiv.org/abs/2204.06974 (fetched twice: once for metadata, once demanding strict verbatim abstract) — SUCCESS
- https://arxiv.org/html/2204.06974v2 (independent extraction prompt targeting Thms 2.1-2.4, certification corollary, RFF caveat, open question, immunization limits) — SUCCESS
- https://dblp.org/rec/conf/focs/GoldwasserKVZ22.html — SUCCESS (title incl. "[Extended Abstract]", authors, FOCS 2022, pp. 931-942, DOI 10.1109/FOCS54457.2022.00092, IEEE, BibTeX)

---

## 確定記録（検証段による修正適用後）

## SOURCE RECORD: goldwasser-backdoors (VERIFIED — adversarial second pass complete)

### Citation (exact, ready to paste)

**Preprint (full version; CITE THIS ONE):**
> Shafi Goldwasser, Michael P. Kim, Vinod Vaikuntanathan, and Or Zamir. "Planting Undetectable Backdoors in Machine Learning Models." arXiv:2204.06974 [cs.LG], v1 14 April 2022; v2 9 November 2024.

**Conference version (venue record):**
> Shafi Goldwasser, Michael P. Kim, Vinod Vaikuntanathan, and Or Zamir. "Planting Undetectable Backdoors in Machine Learning Models: [Extended Abstract]." In *Proceedings of the 63rd IEEE Annual Symposium on Foundations of Computer Science (FOCS 2022)*, pp. 931–942. IEEE, 2022. DOI: 10.1109/FOCS54457.2022.00092.

All fields above independently re-verified this session, character by character, against arxiv.org/abs/2204.06974 and dblp.org/rec/conf/focs/GoldwasserKVZ22.html. Four authors, order correct. Subjects: Machine Learning (cs.LG); Cryptography and Security (cs.CR). No arXiv journal-reference field returned.

**Bibliography riders (MANDATORY):**
- The FOCS record is titled "[Extended Abstract]". Cite the arXiv full version for substance.
- Theorem numbers cited below are from **arXiv v2** and are the paper's **(Informal)** overview statements. Cite as "arXiv:2204.06974v2, Thm 2.1 (Informal)" — never cite a theorem number to FOCS pagination, and never drop "(Informal)" for a load-bearing claim.

### What was actually fetched (this verification pass)

| URL | Result |
|---|---|
| `arxiv.org/abs/2204.06974` | **SUCCESS** ×2 (second pass demanded strict verbatim). Full abstract confirmed verbatim. Metadata, version history, subjects confirmed. |
| `arxiv.org/html/2204.06974v2` | **SUCCESS**, independent extraction prompt. Reproduced Thms 2.1–2.4 (Informal), certification corollary, RFF caveat, open question, immunization limits. |
| `dblp.org/rec/conf/focs/GoldwasserKVZ22.html` | **SUCCESS**. Title/authors/venue/pages/DOI/publisher + BibTeX. |
| PDF `arxiv.org/pdf/2204.06974` | **NOT FETCHED** — open gap, see "Unverified residue". |
| IEEE/FOCS published text | **NOT FETCHED** (paywalled). |

**Standing caveat:** WebFetch converts to markdown and runs a *summarizing model* against the prompt. Interior quotes are pipeline-mediated. Mitigation applied: the page was fetched by two agents with two different prompts, and five interior quotes came back **character-identical across independent prompts** (Thm 2.1, Thm 2.2, the certification-distinguisher sentence, the RFF proof-of-concept passage, the open question). That is strong corroboration of substance and good evidence of wording — but it is not a PDF read.

### Precise claims

**Abstract — VERBATIM, independently confirmed word-for-word this session:**
> "Given the computational cost and technical expertise required to train machine learning models, users may delegate the task of learning to a service provider. We show how a malicious learner can plant an undetectable backdoor into a classifier. On the surface, such a backdoored classifier behaves normally, but in reality, the learner maintains a mechanism for changing the classification of any input, with only a slight perturbation. Importantly, without the appropriate "backdoor key", the mechanism is hidden and cannot be detected by any computationally-bounded observer. We demonstrate two frameworks for planting undetectable backdoors, with incomparable guarantees. […] Our construction of undetectable backdoors also sheds light on the related issue of robustness to adversarial examples. In particular, our construction can produce a classifier that is indistinguishable from an "adversarially robust" classifier, but where every input has an adversarial example! In summary, the existence of undetectable backdoors represent a significant theoretical roadblock to certifying adversarial robustness."

**Construction 1 — signature-based, black-box undetectable. Thm 2.1 (Informal), verbatim, double-confirmed:**
> "Assuming the existence of one-way functions, for every training procedure **Train**, there exists a model backdoor (**Backdoor**, **Activate**), which is non-replicable and black-box undetectable."
- Assumption: one-way functions (minimal crypto assumption). Scope: **any** Train. Detector access: **black-box only**. Non-replicable. Generalization error comparable to the clean model (per abstract).

**Construction 2 — RFF, white-box undetectable. Thm 2.2 (Informal), verbatim, double-confirmed:**
> "Assuming the hardness of worst-case lattice problems, for any data distribution 𝒟 with 𝒳⊆ℝ^d, there is a backdoor (**Backdoor-RFF**, **Activate-RFF**) with respect to **Train-RFF**, that is white-box undetectable."
- Assumption: **worst-case lattice hardness via CLWE — strictly stronger than OWF**. Scope: **only Train-RFF / Random ReLU**. Detector access: white-box (weights + training data). **Highly replicable.**

**These two are not one result. Never state white-box strength and OWF-minimality in the same breath.** The abstract itself says the frameworks have "incomparable guarantees." No construction is simultaneously non-replicable and white-box undetectable; verbatim open question, double-confirmed:
> "A clear concrete open question is whether it is possible to plant backdoors in natural training procedures that are simultaneously non-replicable and white-box undetectable."

**Thm 2.3 (Informal), verbatim:** > "Let N be a neural network of size |N| and depth d. There exists a neural network N′ of size O(|N|) and depth d+1 such that N(x)=N′(x) for any input x, and for every loss ℓ, N′ is ℓ-persistent." (Persistence to gradient descent. The authors flag extending persistence to the *white-box/RFF* backdoors as future work — substance corroborated, exact wording of that caveat NOT independently reproduced.)

**Thm 2.4 (Informal):** randomized-smoothing-style evaluation-time immunization — for any h and σ>0 one can efficiently evaluate a σ-robust h̃ with small added error. **A defense that works, under conditions.**

**Certification corollary (Premise-C-relevant) — verbatim, double-confirmed:**
> "any complete and sound robustness certification algorithm—which receives a hypothesis h as input and must certify that h is robust to adversarial examples or not—would serve as a distinguisher between h and h̃, contradicting undetectability."

**Conditional attached to it (confirmed present):** the corollary is stated against an **idealized adversarially-robust training algorithm** assumed to return a perfectly robust h. It is a conditional statement about a hypothetical baseline, **not** a measurement of any existing robust-training method.

**Threat model:** adversary = "a malicious learner"; setting = users "delegate the task of learning to a service provider"; concern = abuse of power by untrusted learners. **The adversary produces the model.** This is the frame of the entire paper, not a footnote.

### What it does NOT claim

1. Does **not** claim honestly-trained models contain undetectable flaws. Every result concerns a model produced by an adversary who deliberately planted something.
2. Does **not** claim backdoors arise spontaneously or emergently. No emergence claim exists in the paper.
3. **Existence theorem — not a rate bound, not a prevalence claim, not a statement about any deployed system.** "There exists a backdoor" ≠ "models have backdoors" ≠ "ε% of models are backdoored."
4. Does **not** claim detection is impossible in general. It forbids a **complete AND sound** certifier for arbitrary supplied h. **A sound-but-incomplete certifier that outputs "cannot certify" is explicitly untouched.**
5. Does **not** claim the RFF construction transfers to real networks. Verbatim: *"the 2-layer RFF learning paradigm is rather weak, and in particular, it tends to produce networks that are not robust to noise. For this reason, we view the construction here as a proof of concept."*
6. Does **not** claim white-box undetectability for arbitrary training — RFF/Random ReLU only, under lattice hardness.
7. Does **not** concern LLMs, transformers, or generative models. Object of study: a **classifier**. (v1 predates the current LLM-safety literature; note v2 is Nov 2024 and did not extend scope to LLMs.)
8. Does **not** claim defenses are useless — Thm 2.4 gives a working immunization.
9. The "every input has an adversarial example" classifier is indistinguishable from an **idealized** robust classifier that is *assumed* to exist. Not a claim about any real robust classifier.

### Authors' own stated limitations

- RFF construction is explicitly "a proof of concept"; the paradigm is "rather weak."
- Persistence to gradient descent is only partly solved; extending it to the white-box/RFF backdoors is future work.
- Immunization is defeatable if the adversary knows the noise. Verbatim (independently reproduced): *"if the malicious entity is aware of our immunization threshold σ, and is able to perturb inputs by much more than that (n≫σ), without being noticeable, then our immunization does not guarantee anything."* (A second, similarly-substanced sentence about rendering the classifier useless even on clean inputs was reported by the prior pass but **NOT independently reproduced — do not quote it without the PDF**.)
- Open problem: no construction is both non-replicable and white-box undetectable.
- Verifiable delegation left unresolved.

### Hostile-reviewer assessment

**The objection: "this is deliberate cryptographic backdoors in classifiers, not whether an honestly-trained LLM's residual misbehavior is detectable — you are equivocating."**

**Mostly right, if we cite it the way the assigned role describes.** If Supplement II says anything resembling *"Goldwasser et al. prove the absence of ε cannot be detected,"* the reviewer wins outright:
1. **Quantifier structure (fatal).** Paper: *∃ a model whose flaw is undetectable.* Premise C needs: *for the model actually deployed, absence of residual ε cannot be certified.* Different statements; the proof does not deliver the second.
2. **Undetectability is parasitic on planted cryptographic structure.** Hardness comes from a signature scheme or CLWE — objects the adversary embedded. Emergent misalignment has no key, no trapdoor, no lattice. Nothing in the paper lets residue inherit cryptographic hardness. The hardness is a property of *the gadget*, not of "flaws in neural networks."
3. **Object mismatch.** Classifiers, not LLMs; 2-layer RFF, not frontier models; authors call the setting weak.
4. **The roadblock is conditional on an idealized robust learner that does not exist.**

**What survives — the honest core.** The paper proves a genuine universal negative, certifier-shaped: **no complete-and-sound robustness certification algorithm exists that takes an arbitrary supplied hypothesis h and correctly decides whether h is robust**, since it would break indistinguishability. Under OWF this holds against black-box inspection for *any* training procedure. Separately, in the RFF regime under lattice hardness, undetectability survives *white-box* inspection — weights and training data both. That is a claim about **the limits of any certification regime that must accept a model from someone else**, and it is not a claim about emergent misalignment.

**The available inversion (recommended).** In offensive LAWS, the malicious-learner threat model is **not an artificial limitation — it is the realistic case**. The paper's frame ("users delegate learning to a service provider"; untrusted learners) *is* defense procurement. A weapons model comes from a contractor, through a supply chain, possibly with foreign-sourced components or pretraining data, and a nation-state adversary has both motive and resources to plant exactly this. Under Premise B (unbounded, irreversible single-error cost), minimax evaluates the **worst** case in the feasible set, not the modal one. Goldwasser et al. establish that the worst case in that set is cryptographically uncertifiable. **For a minimax argument a worst-case construction is not a weakness of the citation — it is the correct input.**

**Sharpened point (add to Supplement II):** the theorem forbids a *complete and sound* certifier. The certifier it permits is the one that answers "cannot certify." That is the burden-of-proof asymmetry stated as a theorem: the only cryptographically-honest certification regime for an arbitrary supplied model is one that must sometimes abstain — and under Premise B, abstention is refusal to deploy.

### Honest, defensible use — CORRECTED SCOPING

**DO cite it for (CORRECTED — the prior pass's version fused two results and must not be used):**
> "Under the assumption that one-way functions exist, no complete-and-sound certification procedure exists that can decide, for an arbitrary supplied model, whether that model is free of adversarially-elicitable failure; a model produced by an untrusted learner can be made indistinguishable from a clean one to any computationally-bounded observer with black-box access, for *any* training procedure. Under the stronger assumption of worst-case lattice hardness, and for the Random Fourier Features / Random ReLU paradigm specifically, this indistinguishability survives even *white-box* inspection of the weights and the training data. These are cryptographic impossibilities, not engineering gaps that better tools will close."

*(The prior pass's one-sentence version — "…even given white-box access — this is a cryptographic impossibility under one-way functions" — is **rejected**: it attributes white-box strength to OWF and to arbitrary models. The white-box result needs lattice hardness AND is RFF-only.)*

- **DO cite it for:** the supply-chain/procurement leg of the burden-of-proof asymmetry. The deployer's natural rebuttal is "we certified the model." This closes that door *as a general complete-and-sound procedure*, in precisely the delegation setting military procurement occupies.
- **DO cite it for:** why "we inspected the weights" is not an answer — **with the rider that this holds for the RFF paradigm under lattice hardness, not for arbitrary architectures.** The rider is not optional.
- **DO cite it for:** the NIST domain distinction (below).
- **DO NOT cite it for:** the proposition that an honestly-trained model's emergent ε is undetectable. **The paper does not support this and Supplement II must not imply it.** That leg of Premise C must be carried by Premise A's empirical literature — a *different* kind of evidence with weaker force, and Supplement II should say so out loud rather than let the crypto result's rigor bleed across.
- **DO NOT write "cryptographic impossibility of detection" unqualified.** Write "cryptographic impossibility of *complete and sound certification of an arbitrary supplied model*."
- **DO NOT drop "(Informal)"** when citing Thm 2.1/2.2 for anything load-bearing.

**Bridge-level note on the NIST (Vassilev 2026) rebuttal.** This is where the source's weight should land. NIST's "continuous monitor-and-update" presupposes a deviation becomes *observable* at some point, at which cost you update. Against the signature-based construction, the deviation is observable only to the key-holder, who chooses when — so monitoring has no trigger, and "update after we see it" reduces to "update after the unbounded-cost event." Sound on the paper's actual claims; needs no equivocation about emergent misalignment. It does depend on the malicious-trainer frame — which is why that frame should be **foregrounded as apt for LAWS procurement**, not apologized for. *(Caveat: the characterization of NIST/Vassilev 2026 is taken entirely from the task prompt. Not fetched, not verified. The note is conditional on the prompt's characterization being accurate.)*

### COI / over-read warning (retained and endorsed)

This source is **seductive**. A FOCS paper by Goldwasser whose abstract ends "a significant theoretical roadblock to certifying adversarial robustness" — a sentence that reads as if written for Supplement II. That closing sentence is the most quotable and most over-readable line in the paper and is doing less work than it appears: it is conditional on an idealized robust learner that does not exist. **Same shape as COI #49/#52: the source that most flatters the thesis is the one whose scope-conditions we are most likely to skip.** Empirical confirmation from this pass: the prior verification agent *identified this risk correctly and in detail*, and then dropped exactly those scope-conditions in the single sentence it recommended for pasting. **Naming the failure mode did not prevent the failure mode** — consistent with the frozen lesson "対処したと書くこと自体がライセンスになりうる."

### Verdict on the prior sweep's characterization

**COULD NOT VERIFY** — the sweep's text for this source was not supplied to either pass. Not guessed at. Correct handling; do not treat this line as a pass.

**On the assigned role as stated ("Premise C — cryptographic impossibility of detection"): PARTIALLY WRONG as a framing.**
- "Cryptographic impossibility" — **correct**, under OWF (black-box, any Train) / lattice hardness (white-box, RFF only).
- "of detection" — **overbroad**. Proves impossibility of *complete-and-sound certification of an arbitrary supplied hypothesis*, and of *distinguishing a specific planted-backdoor model from its clean counterpart*. Does not prove flaws are undetectable in general; offers a working (defeatable) immunization in Thm 2.4.
- Bridge to "absence of ε cannot be proven by behavioral evaluation" is **stronger than the paper in one direction, weaker in another**: stronger, because the result is not limited to *behavioral* evaluation — the RFF result defeats white-box evaluation too (a free upgrade, but only in the RFF regime, under lattice hardness); weaker, because it applies only to adversarially-produced models (a real scope limit). **Surface both in Supplement II; smooth over neither.**

### Confidence and unverified residue

**Verified this session, independently, high confidence:** title; all four authors and their order; full abstract verbatim; arXiv ID; v1 2022-04-14 / v2 2024-11-09; subjects cs.LG, cs.CR; FOCS 2022, pp. 931–942; DOI 10.1109/FOCS54457.2022.00092; IEEE; "[Extended Abstract]" in the FOCS title — two independent sources (DBLP + arXiv) agreeing.

**Verified verbatim across two independent extraction prompts (high confidence, still not a PDF read):** Thm 2.1 (Informal); Thm 2.2 (Informal); the certification-distinguisher sentence; the RFF proof-of-concept / "rather weak" passage; the open question.

**Verified in substance, wording NOT confirmed (medium — check PDF before quoting):** Thm 2.3 and 2.4 statements; the gradient-descent-persistence future-work sentence; the "idealized adversarially-robust training algorithm" phrasing; the prior pass's immunization-limitation quote (a *differently worded* sentence of the same substance was reproduced instead — **the prior pass's wording is unconfirmed and must not be pasted**).

**From training knowledge, NOT verified this session — do not cite:** that this paper is widely cited in AI-safety literature as a detection-impossibility result, and that the emergent-misalignment reading is a *common* over-read. Impression, not a bibliometric claim.

**Not the paper's, needs its own citation:** the "malicious trainer is realistic in LAWS procurement" premise. It is our argument. It does not come from Goldwasser et al. If Supplement II makes this move (recommended), source it independently.

**Open gap:** the PDF (`arxiv.org/pdf/2204.06974`) has not been read by either pass. Every quote flagged medium-confidence above requires a character-by-character PDF check before it appears as quoted matter. The IEEE/FOCS published text is paywalled and unread.

---

## 検証段が発見した過大主張・誤り（5件）

- FATAL FOR THE PASTE-READY SENTENCE — assumption fusion. The report's first 'DO cite it for' bullet reads: 'No complete-and-sound certification procedure exists that can rule out adversarially-elicitable failure in an arbitrary supplied model, EVEN GIVEN WHITE-BOX ACCESS — this is a cryptographic impossibility UNDER ONE-WAY FUNCTIONS.' This fuses two results with different assumptions and different scopes. The OWF result (Thm 2.1) is BLACK-BOX undetectability only. The white-box result (Thm 2.2) requires worst-case lattice hardness via CLWE — a strictly stronger assumption — and holds ONLY for Train-RFF / Random ReLU, not arbitrary models. The bullet attributes white-box strength to the minimal assumption and to arbitrary supplied models. The report states both facts correctly in its own tables and in bullet 3's rider, then drops them in the one sentence it recommends pasting. This is a hedge dropped precisely where it does damage.

- Conditional presented as unconditional in the same bullet. The report itself flags (correctly, and I verified the phrase 'idealized adversarially-robust training algorithm' is in the source) that the robustness-certification corollary is conditional on a hypothetical perfectly-robust learner. The 'DO cite it for' bullet states the impossibility flatly with that condition removed.

- 'Closes that door as a general procedure' (the procurement bullet) overreaches slightly. The theorem forbids a COMPLETE AND SOUND certifier. A sound-but-incomplete certifier that outputs 'cannot certify' is untouched by the result. This is not a weakness for Supplement II — it is the burden-of-proof point in sharper form (the permitted certifier is exactly the one that must abstain) — but the report's phrasing invites a reviewer to score a free correction.

- Theorem numbering cited without the '(Informal)' tag. My independent fetch returns Thms 2.1 and 2.2 as '(Informal)' statements — overview restatements, not the formal theorems. The report cites 'Thm 2.1, arXiv v2' bare. If Supplement II cites a theorem number for a load-bearing claim, it must be 'Thm 2.1 (Informal), arXiv:2204.06974v2' or point to the formal statement in the body.

- Improper corroboration method (no factual harm, but the reasoning is the forbidden pattern). The report justifies 'Abstract (verbatim, high confidence)' partly because 'it matches my independent training knowledge of this paper.' Memory is not permitted as verification under discipline rule 2. I independently confirmed the abstract IS verbatim-exact, so the claim survives — but it survived by luck of the check, not by the method used.


## 取得honesty監査（5件）

- No dishonesty found — the report passes this audit better than most. My independent fetch, using a deliberately different extraction prompt, reproduced FIVE of its interior quotes character-identically: Thm 2.1 (Informal), Thm 2.2 (Informal), the 'any complete and sound robustness certification algorithm...would serve as a distinguisher between h and h-tilde, contradicting undetectability' sentence, the RFF 'proof of concept' / '2-layer RFF learning paradigm is rather weak...not robust to noise' passage, and the open question on non-replicable + white-box undetectable. Independent reproduction through a different prompt is strong evidence the page was actually read. The report also volunteered the WebFetch-is-a-summarizer indirection unprompted and correctly refused to certify its own interior quotes' exact wording — that self-report is accurate and was the right call.

- ONE QUOTE NOT CORROBORATED. The report's immunization-limitation quote ('If the malicious learner knows the magnitude or type of noise that will be added to neutralize him, he can prepare the backdoor perturbation to evade the defense. In the extreme, the adversary may be able to hide a backdoor that requires significant amounts of noise to neutralize, which may render the returned classifier useless, even on clean inputs.') did NOT come back in my fetch. I instead received a different sentence with the same substance: 'if the malicious entity is aware of our immunization threshold sigma, and is able to perturb inputs by much more than that (n >> sigma), without being noticeable, then our immunization does not guarantee anything.' Both may exist in different sections. The SUBSTANCE is corroborated; the WORDING of the report's version is not. Do not paste that quote without opening the PDF.

- The report's 'Thm 2.3 gives a persistence construction' plus its gradient-descent-persistence open-direction quote: I confirmed Thm 2.3 (Informal) is a persistence result (network N' of size O(|N|), depth d+1, l-persistent), which is consistent, but I did not independently reproduce the quoted open-direction sentence. Substance plausible; wording unverified.

- The report's 'NOT ATTEMPTED — PDF' is honestly declared and the reason given (HTML rendered) is legitimate, but given that the report's own strongest caveat is about exact wording, declining the PDF is the one methodological gap that its own analysis identifies and then does not close. This is a completeness gap, not a honesty gap.

- 'Verdict on the prior sweep: COULD NOT VERIFY — the sweep's text was not provided.' I confirm this is the correct response and not an evasion. The report refused to grade a guess. Correct behavior under rule 2.


## 引用可能性の裁定

DEFENSIBLE WITH ONE MANDATORY EDIT. The report's analytical core is sound and unusually disciplined — its hostile-reviewer section correctly identifies the fatal quantifier equivocation (paper proves EXISTS a model with undetectable flaw; Premise C needs FORALL / the-deployed-model), correctly refuses the emergent-misalignment reading, correctly reassigns that leg to Premise A, and correctly self-flags the COI/#49/#52 over-read risk on the abstract's closing sentence. Its inversion move (malicious-learner frame is APT for LAWS procurement, and a worst-case construction is the correct input to a minimax argument, not a defect) is legitimate and would survive review — provided Supplement II sources the procurement-supply-chain premise separately, which the report itself flags as its own argument and not the paper's. The NIST domain-distinction application (monitoring has no trigger when the deviation is observable only to the key-holder, so 'update after we see it' reduces to 'update after the unbounded-cost event') is sound on the paper's actual claims and is where this citation's weight should land. BUT: the single paste-ready sentence the report recommends is not defensible as written and a hostile reviewer would take it apart in one line, because it claims white-box-strength impossibility over arbitrary supplied models under one-way functions. The corrected sentence must split the two results by assumption and scope. With that split made, the use is defensible.
