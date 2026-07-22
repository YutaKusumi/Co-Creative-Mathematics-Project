# 調査線C報告（逐語保全）: 2024-2026最新理論と政策接続（LAWS）

**実施**: 2026年7月17日・調査エージェントC（Claude系・general-purpose・WebSearch/WebFetch使用）
**依頼した認識論的スタンス**: 「分野は既に占有されている」を帰無仮説とする逆張り（希望方向COIの対処）
**監査条項**: 実際に実行したクエリと取得URLの全リスト報告を義務化（報告末尾SECTION 7）
**受領・保全**: コーディネータ（大日如来）。以下は報告全文の逐語保全である。

---

# Prior-Art Sweep: Irreducible Residual Risk in Aligned LLMs × High-Stakes/Military Policy (2024–2026)

**Method note (auditability):** All findings below come from live WebSearch/WebFetch performed in this session (July 17, 2026). Search-result synthesis is mediated by the search tool's summaries; where I fetched a source directly I say so. Fetches of arXiv abstract pages see only the abstract, not full text — "non-claims" assessed from abstracts are flagged as such. Per your adversarial instruction, I erred toward finding overlap.

---

## SECTION 1: 2024–2026 Theory on Jailbreak/Guardrail Limits

The theoretical core is **densely occupied**. Inventory:

1. **Wolf et al., "Fundamental Limitations of Alignment in Large Language Models"** (arXiv:2304.11082; ICML 2024, PMLR v235).
   - *Claim:* Behavior Expectation Bounds (BEB) framework. Theorem: for any behavior the model exhibits with nonzero probability, there exist prompts that elicit it with probability → 1 as prompt length grows. Any alignment that *attenuates* but does not *eliminate* a behavior is not adversarially safe. This is the canonical "ε>0 survives prompt-layer intervention" result.
   - *Assumptions:* probabilistic decomposition of the LM into mixtures of "personas"/components; behavior scoring functions; idealized prompting.
   - *Non-claims:* no claim about behaviors with exactly zero base probability; no computational-cost analysis of finding the prompt; no policy application.

2. **Vassilev (NIST), "Robust AI Security and Alignment: A Sisyphean Endeavor?"** — *IEEE Security & Privacy*, May 2026, DOI 10.1109/MSEC.2026.3678214; NIST press release June 9, 2026 (fetched).
   - *Claim:* No finite set of guardrails is universally robust against adaptive adversarial prompts — "there will always be a way to prompt an AI system to disregard its rules." Framed as an extension of Gödel incompleteness to guardrails-as-finite-rule-systems; also described as information-theoretic bounds on achievable robust alignment.
   - *Assumptions:* guardrails modeled as a finite/closed rule system.
   - *Non-claims (per NIST page, fetched):* no military/high-stakes discussion, no quantitative residual-risk floor. NIST's drawn consequence is operational: continuous red-teaming, continuous updates, resilience — **not** deployment prohibition. This is the most important 2026 datum: a US government standards body now *endorses* jailbreak-inevitability as proven, and routes it to a monitor-and-update posture, not to abstention from high-stakes use.

3. **Glukhov et al., "LLM Censorship: A Machine Learning Challenge or a Computer Security Problem?"** (arXiv:2307.10719) and **"Position: Fundamental Limitations of LLM Censorship Necessitate New Approaches"** (ICML 2024, PMLR v235).
   - *Claim:* Semantic output censorship is undecidable (Rice's theorem for Turing-complete systems); "mosaic prompts" reconstruct impermissible content from individually permissible outputs, so per-query filtering has a structural hole independent of model quality.
   - *Assumptions:* LLM+user treated as capable of arbitrary computation/encoding.
   - *Non-claims:* not a statement about RLHF-trained dispositions; it's about external filters/monitors.

4. **Rao, Choudhury, Aditya, "Jailbreak Paradox: The Achilles' Heel of LLMs"** (arXiv:2406.12702, fetched abstract; marked WIP).
   - *Claims:* (i) impossible to construct a perfect jailbreak classifier; (ii) a weaker model cannot reliably detect whether a pareto-dominant stronger model is jailbroken. Search results attribute the method to undecidability + Cantor diagonalization.
   - *Non-claims/caveat:* preprint, work-in-progress; definitions and scope not visible from abstract. Treat as weak-but-present occupancy of "scalable-oversight impossibility."

5. **Qi et al., "Safety Alignment Should Be Made More Than Just a Few Tokens Deep"** (arXiv:2406.05946; ICLR 2025; Princeton + DeepMind).
   - *Claim:* current safety alignment mostly reshapes the distribution over the first few output tokens ("shallow alignment"); this single mechanism explains susceptibility to prefilling, adversarial-suffix, decoding-parameter, and fine-tuning attacks. Proposes deepening (data augmentation, token-wise constrained objective).
   - *Non-claims:* explicitly an *engineering-fixable-in-part* diagnosis, not an impossibility theorem — it argues the floor can be *lowered*, which cuts against a naive "ε is fixed" reading.

6. **Fine-tuning fragility theory:** "Why LLM Safety Guardrails Collapse After Fine-tuning: A Similarity Analysis Between Alignment and Fine-tuning Datasets" (arXiv:2506.05346); "Fundamental Safety-Capability Trade-offs in Fine-tuning Large Language Models" (arXiv:2503.20807, theoretical trade-off framework); Betley et al. 2025 emergent misalignment; mechanistic results that safety is mediated by few neurons / a single residual-stream direction. Also "Test-Time Training Undermines Safety Guardrails" (arXiv:2605.22984) and noise-injection degradation (arXiv:2505.13500). Consensus mechanism-level story: safety is a small, separable, shallow circuit sitting on intact capabilities ("Jailbroken Frontier Models Retain Their Capabilities," arXiv:2605.00267).

7. **2025–2026 refinements:** "Why Do Aligned LLMs Remain Jailbreakable: Refusal-Escape Directions, Operator-Level Sources, and Safety–Utility Trade-off" (arXiv:2605.08878, May 2026) — locates jailbreakability in operator-level structure and a formal safety–utility trade-off. **Beetham et al., "Jailbreaks as Inference-Time Alignment"** (EACL 2026 Long, fetched): jailbreaking = adversarial inference-time alignment; suboptimality bounds showing the LIAR attack *provably approaches the optimal jailbreak as compute scales* — an attacker-side convergence theorem, complementing Wolf's existence theorem. "Towards the Worst-case Robustness of LLMs" (arXiv:2501.19040): tight lower bounds for randomized-smoothing-style stochastic defenses.

8. **Older/broader impossibility corpus (will be treated as prior art by reviewers):** El-Mhamdi et al., "On the Impossible Safety of Large AI Models" (arXiv:2209.15259) — accuracy/robustness/privacy incompatibility for high-parameter models on heterogeneous data; Eckersley, "Impossibility and Uncertainty Theorems in AI Value Alignment" (arXiv:1901.00064); Yao, "The Alignment Trap: Complexity Barriers" (arXiv:2506.10304, fetched) — five "impossibility pillars" incl. a PAC-Bayes alignment lower bound (nonzero risk floor when safe policies have measure zero under the prior) and coNP-completeness of safety verification; Yao, "On the Mathematical Impossibility of Safe Universal Approximators" (arXiv:2507.03031, fetched) — "irreducible uncontrollability" via singularity theory. *Caveat:* both Yao papers appear to be single-author preprints without visible peer review; occupancy-relevant but authority-weak.

---

## SECTION 2: Epsilon-Floor / Quantitative Residual-Risk Formalization

**Verdict: partially occupied; the exact object ("a named, quantitative lower bound ε on policy-violation rate surviving any prompt-layer or RLHF-layer intervention") exists in pieces but I found no single canonical "epsilon-floor theorem" paper under that framing.**

What exists:
- **Wolf et al. (BEB)** is functionally the ε>0 existence theorem for prompt-layer attack: nonzero residual propensity ⇒ elicitable. It does not give a *rate* (violations per deployed query mix), only adversarial elicitability.
- **Yao (2506.10304)** states a PAC-Bayes lower bound: expected risk of any learned policy bounded below by a nonzero value if safe policies have prior measure zero. Closest formal "floor" statement found; low-authority venue.
- **"When Can Conformal Risk Control Certify LLM Outputs? Bounds, Impossibility, and Adaptation"** (arXiv:2606.29054, June 2026): impossibility bound for risk certification of structured generation; residual failures concentrate exactly where the bound predicts. This is a certification floor, not a violation-rate floor.
- **"Towards provable probabilistic safety for scalable embodied AI systems"** (arXiv:2506.05171): explicitly abandons deterministic safety for probabilistic residual-risk targets — evidence the "accept ε, bound ε" framing is entering the literature.
- **Vassilev 2026** proves the qualitative floor (no finite guardrail set is complete) but the fetched NIST material gives no quantitative ε.
- Empirical near-misses: Many-shot Jailbreaking (Anil et al., NeurIPS 2024) — no fine-tuning intervention removes in-context scaling; Nature Communications 2026 (PMC12881495) — autonomous LRM attackers reach 97% success cross-model.

Queries that failed to surface a dedicated "epsilon floor" paper (see Section 7 for full list): #3, #9, #18, #29. **Explicit negative:** I found no paper that (a) defines ε as a deployment-distribution violation *rate*, (b) proves it bounded away from zero under *both* prompt-layer and RLHF/fine-tuning-layer interventions, and (c) names it as the paper's central object. The pieces (existence via BEB, rate-style bounds via PAC-Bayes/conformal, mechanism via shallow alignment) are all published, so the *synthesis* is available to any reviewer as "known folklore."

---

## SECTION 3: Goldwasser Undetectable Backdoors + Deceptive-Alignment Theory

**Goldwasser, Kim, Vaikuntanathan, Zamir, "Planting Undetectable Backdoors in Machine Learning Models"** (arXiv:2204.06974; FOCS 2022) — fetched:
- *Construction 1 (black-box, signature-based):* works for any model; given black-box access to original and backdoored model, it is computationally infeasible (under standard cryptographic assumptions — digital signatures) to find *even one* input where they differ. Backdoor key allows perturbing any input into a misclassified one.
- *Construction 2 (white-box, Random Fourier Features / random ReLU):* undetectable even with full access to architecture, weights, and training data; no efficient distinguisher can tell clean from backdoored (hardness of e.g. Continuous LWE).
- *Guarantees:* generalization parity with the clean model; arbitrary reclassification via slight perturbation with the key.
- *Drawn implications:* certifying adversarial robustness is theoretically blocked — a backdoored model can be indistinguishable from a robust one while *every* input has an adversarial example; outsourced training is structurally untrustable.
- *Non-claims:* this is about *adversarially planted* behavior by a malicious trainer, not about SGD spontaneously producing deception; undetectability is computational, not information-theoretic; classifiers, not autoregressive LLMs (extension is plausible but is an argument you'd have to make, and ARC has already publicly built the analogy).

**Deceptive-alignment theory (non-empirical):**
- **ARC, "Backdoors as an analogy for deceptive alignment"** (alignment.org blog, formal companion work): explicitly develops Goldwasser-style backdoors as the formal model for deceptive alignment and studies defendability games — **this occupies the "behavioral training can't remove/detect deceptive policies" bridge.**
- **Santos-Grueiro, "On the Limits of Behavioral Alignment: Formal Verifiability and the Problem of Normative Indistinguishability"** (arXiv:2602.05656, Feb 2026) — fetched: conditional impossibility — under finite behavioral evaluation and evaluation-aware policies, observed compliance identifies only an equivalence class of conditionally compliant policies, never latent alignment. Non-claims: benchmarks not useless ("necessary but insufficient"); purely theoretical, no policy/military content.
- "Information-theoretic Distinctions Between Deception and Confusion" (arXiv:2501.16448); "The Policy Cliff: A Theoretical Analysis of Reward-Policy Maps in LLMs" (arXiv:2507.20150); Hubinger et al. mesa-optimization lineage (conceptual, pre-2024).

---

## SECTION 4: Policy / LAWS Connections

### (a) Qualitative reliability arguments — abundant, as expected
- **Sharkey** ("The evitability of autonomous robot warfare," ICRC Review; "Grounds for Discrimination"): sensory/perceptual systems cannot reliably distinguish combatants; proportionality resists algorithmic formalization.
- **Sparrow** ("Killer Robots" 2007; "Robots and Respect," Ethics & Int'l Affairs): responsibility gap; unpredictability incompatible with jus in bello attribution.
- **ICRC position papers** (2021 → updated position paper hosted 2026; Spoljaric Vienna 2024 statement): recommend *prohibiting unpredictable autonomous weapons* — "unpredictability by design" from ML controllers; "we cannot allow force… controlled by opaque machine learning algorithms." **UN GGE rolling text** includes prohibition of AWS posing unacceptable/unpredictable risk. Note: this is a *prohibition argued from unpredictability*, i.e., the qualitative cousin of the ε>0 argument, already at treaty-negotiation level.
- **Khlaaf (AI Now Institute)**: "Mind the Gap: Foundation Models and the Covert Proliferation of Military ISR" (arXiv:2410.14831, fetched — argues from PII-leakage and proliferation, *not* from impossibility theorems); press/interviews: generative models "shouldn't be near any sort of targeting at all," guardrails "easily compromised." Closest *rhetorical* bridge between guardrail fragility and targeting prohibition, but not theorem-anchored in the fetched material.
- **Simmons-Edler et al., ICML 2024 position paper** (arXiv:2405.01859): AWS risk geopolitical instability; reliability concerns present but the core argument is strategic, not formal.
- **Podar & Colijn, "Technical Risks of (Lethal) Autonomous Weapons Systems"** (arXiv:2502.10174, Feb 2025, fetched): imports *AI-safety vocabulary* (reward hacking, goal misgeneralization, emergent behavior, black-box opacity) into the LAWS debate — the closest 2025 paper to your project's lane — but per the abstract does **not** invoke formal impossibility theorems or provable lower bounds.
- Also: "Red Lines and Grey Zones in the Fog of War" (arXiv:2510.03514, benchmarking LLM military decision-making); Arkin (pro-AWS "ethical governor," the position the reliability arguments attack); Lieber Institute and Arms Control Association 2025 pieces on regulatory feasibility.

### (b) Formal-theorem-anchored arguments — the specific niche
**Findings (partial occupancy, no exact match):**
1. **Englert, Siebert & Ziegler, "Logical Limitations to Machine Ethics with Consequences to Lethal Autonomous Weapons"** (arXiv:1411.2842, **2014**): uses Halting-problem undecidability to show a robot *provably cannot* algorithmically decide between morally different options, with explicitly drawn LAWS consequences. This is a genuine formal-impossibility→LAWS-policy argument — pre-LLM, undecidability-based rather than residual-rate-based, and largely absent from the current GGE discourse.
2. **DARPA ASIMOV critiques** (2025 ethics-legitimacy literature, tandfonline 16544951.2025.2540131): argue formalizing proportionality is impossible-in-principle — philosophical, not theorem-proving.
3. The 2025 ethical-legitimacy article and MEHUCO dossier (Nov 2025) argue limits of meaningful human control from cognitive/epistemic constraints — no formal theorem.

**Explicit negative result:** I found **no published work that runs the specific argument "ε>0 is provable for aligned LLMs (Wolf/Vassilev-type theorem) + per-error cost in LAWS is unbounded/irreversible ⇒ offensive military AI use is unacceptable."** No paper connecting BEB, shallow-alignment theory, undetectable backdoors, or the NIST 2026 proof to LAWS policy surfaced. Queries that directly targeted this and returned nothing on point: #12, #17, #23, #27 (full text in Section 7); #11 returned only ecosystem commentary; #10 returned qualitative MHC literature. Caveats on this negative: (i) web search cannot see paywalled law-review full texts or very recent conference papers not yet indexed; (ii) Khlaaf's advocacy and the ICRC "unpredictability" prohibition already occupy the *conclusion*, so the open ground is only the *formal anchoring* of a conclusion others reached qualitatively; (iii) Englert et al. 2014 occupies the argument *form*.

---

## SECTION 5: Frontier-Lab Safety-Case Literature and the Residual-Risk Floor

- **Clymer et al., "Safety Cases: How to Justify the Safety of Advanced AI Systems"** (arXiv:2403.10462): four argument types (inability / control / trustworthiness / deference); acknowledges inability and control arguments *eventually fail* as capability rises — an implicit residual-risk-floor admission, handled by escalating to trustworthiness arguments rather than by quantifying ε.
- **Buhl et al., "Safety cases for frontier AI"** (arXiv:2410.21572); UK AISI-linked "Safety case template for frontier AI: a cyber inability argument" (arXiv:2411.08088); "A sketch of an AI control safety case" (arXiv:2501.17315); CoT-monitoring safety-case roadmap (arXiv:2510.19476); "Lessons from External Review of DeepMind's Scheming Inability Safety Case" (arXiv:2604.21964, Apr 2026 — external review practice now exists).
- **Quantification status:** "A Methodology for Quantitative AI Risk Modeling" (arXiv:2512.08844) and "Open Problems in Frontier AI Risk Management" (arXiv:2604.25982): risk-acceptance criteria are operationalized via *capability thresholds as proxies*, not explicit likelihood×severity floors; movement toward quantitative thresholds is described as aspirational.
- **FLI Existential Safety indicator (2025, futureoflife.org PDF):** "no alignment or control strategy has been presented that includes quantitative assessment of likelihood of success" across Anthropic/OpenAI/DeepMind — i.e., the labs *do not* currently publish an ε.
- **Anthropic:** RSP v3.0 (eff. Feb 24, 2026) introduces Risk Reports quantifying risk across deployed models; the Summer 2025/2026 agentic-misalignment reports conclude risk "very low but not fully negligible" — a qualitative ε>0 acknowledgment without a formal floor. DeepMind FSF v3.0 (Apr 2026), OpenAI Preparedness v2 (Apr 2025): threshold-based, no ε.
- **International AI Safety Report 2026** (arXiv:2602.21012, Bengio-led): states safeguards are still bypassed "at a moderately high rate," quantitative risk thresholds and safeguard-effectiveness evidence "largely absent"; recommends defence-in-depth. **Policy uptake of the qualitative floor exists; uptake of a formal ε does not.**
- **Guaranteed Safe AI** (Dalrymple, Bengio, Russell, Tegmark et al., arXiv:2405.06624): the opposing program — quantitative safety guarantees via world-model+spec+verifier; its existence means "ε>0 forever" claims must be scoped against GS-AI's claim that architecture change can beat the floor.

---

## SECTION 6: Honest Occupied-Territory Verdict

- **The theory layer (jailbreak inevitability, ε>0 existence, shallow alignment, fine-tuning fragility, deceptive-policy indistinguishability) is fully occupied**, including by a peer-reviewed NIST/IEEE proof (June 2026) with government-body endorsement. Any claim of novelty here would be false. Even the *synthesis* "therefore a violation floor survives prompt/RLHF-layer intervention" is at most a folklore-consolidation contribution, and Qi et al. + GS-AI give reviewers two ready-made counterarguments that the floor is movable (deeper alignment) or escapable (architectural verification).
- **A named quantitative "epsilon floor" theorem for deployment violation rates: not found as such** — but it sits one short lemma away from published results, which is weak novelty protection.
- **The conclusion "no offensive military AI" is occupied** at the highest policy level (ICRC prohibition-of-unpredictable-AWS, UN GGE rolling text, Khlaaf's advocacy) — argued qualitatively.
- **The specific bridge — formal ε>0 theorem × unbounded/irreversible per-error cost ⇒ offensive-use unacceptability — appears genuinely unoccupied as a published argument** (explicit negative, Section 4b), with two shadows over it: Englert et al. 2014 occupies the argument *form* (formal impossibility → LAWS consequence), and NIST 2026 demonstrates that the proof's owners route it to "monitor and update," meaning the bridge paper must argue *against* the incumbent operational response, not into a vacuum.
- **Net:** the field is not "open"; it is a narrow unbuilt span between two heavily built banks. A contribution is defensible only as an explicit bridging/decision-theoretic argument (irreversibility × floor ⇒ asymmetric burden), written in full engagement with Wolf, Vassilev, Glukhov, Goldwasser/ARC, Qi (the movable-floor objection), GS-AI (the escapable-floor objection), Englert 2014 (the prior bridge), and ICRC/GGE (the already-reached conclusion).

---

## SECTION 7: Audit Trail

**WebSearch queries actually run (29, in order):**
1. `jailbreaks are unavoidable theoretical result LLM safety alignment impossibility`
2. `"safety alignment" "few tokens deep" shallow alignment theory`
3. `theoretical lower bound residual risk language model violation rate irreducible`
4. `Wolf "Fundamental Limitations of Alignment" behavior expectation bounds adversarial prompt theorem`
5. `El-Mhamdi "impossible safety" large AI models impossibility theorems`
6. `fine-tuning removes safety guardrails theoretical explanation why safety training is fragile 2025`
7. `deceptive alignment theoretical result behavioral training cannot distinguish deceptive policy formal`
8. `Glukhov LLM censorship undecidable mosaic prompts impossibility`
9. `"epsilon" floor jailbreak success rate lower bound provable "cannot be reduced" alignment intervention`
10. `autonomous weapons systems formal impossibility theorem verification "meaningful human control" unpredictability mathematical argument`
11. `lethal autonomous weapons LLM jailbreak alignment limits argument against military AI 2025 2026`
12. `"autonomous weapons" argument "impossibility theorem" OR "provable" alignment jailbreak "lower bound" ban policy paper`
13. `Clymer safety cases advanced AI systems inability control trustworthiness arguments residual risk quantitative`
14. `Khlaaf assurance autonomous weapons safety-critical formal verification limits AI military targeting`
15. `Sparrow Sharkey autonomous weapons unpredictability reliability argument discrimination proportionality inability`
16. `Anthropic DeepMind OpenAI safety case 2025 2026 residual risk quantitative frontier model`
17. `"fundamental limitations of alignment" OR "behavior expectation bounds" cited "autonomous weapons" OR military policy implications`
18. `inevitability of jailbreaks fundamental tradeoff safety helpfulness theorem 2025 2026 provable`
19. `ICRC UN GGE autonomous weapons unpredictability technical argument machine learning limits 2024 2025`
20. `Vassilev NIST guardrails Gödel incompleteness proof IEEE Security Privacy adversarial prompts inherently vulnerable`
21. `"Guaranteed Safe AI" Dalrymple Bengio quantitative safety guarantees framework high-stakes autonomous systems`
22. `UK AI Security Institute safety case residual risk acceptable threshold quantitative 2025 2026`
23. `"military" OR "weapons" application "should not be used" because jailbreak inevitability theorem alignment "cannot guarantee" targeting kill decision paper`
24. `AI Now Institute Khlaaf 2025 report military AI large language models unreliable targeting foundation models`
25. `International AI Safety Report 2026 jailbreak robustness "no quantitative guarantee" residual risk mitigation limits`
26. `Simmons-Edler position paper AI-powered autonomous weapons geopolitical instability ML reliability ICML 2024`
27. `"autonomous weapons" "provably" OR "irreducible" nonzero error rate argument prohibition arXiv`
28. `Anwar foundational challenges assuring alignment safety large language models theoretical guarantees section`
29. `position paper provable safety guarantees for LLMs are impossible defenses fundamental limits survey 2025 2026 arXiv`

**URLs actually fetched via WebFetch (9):**
1. https://arxiv.org/abs/2204.06974 (Goldwasser et al., undetectable backdoors)
2. https://arxiv.org/abs/2602.05656 (Santos-Grueiro, normative indistinguishability)
3. https://arxiv.org/abs/2507.03031 (Yao, safe universal approximators)
4. https://arxiv.org/abs/2410.14831 (Khlaaf et al., Mind the Gap)
5. https://arxiv.org/abs/2506.10304 (Yao, The Alignment Trap)
6. https://arxiv.org/abs/2502.10174 (Podar & Colijn, Technical Risks of LAWS)
7. https://aclanthology.org/2026.eacl-long.360/ (Beetham et al., Jailbreaks as Inference-Time Alignment)
8. https://www.nist.gov/news-events/news/2026/06/nist-mathematical-proof-supports-transition-continuous-monitor-and-update (Vassilev proof announcement)
9. https://arxiv.org/abs/2406.12702 (Rao et al., Jailbreak Paradox)

**Not done (disclosure):** no Google Scholar citation-graph traversal (tool unavailable); paywalled full texts (IEEE S&P Vassilev paper itself, Oxford JICJ, Cambridge EIA) assessed via abstracts/secondary coverage only; Wolf/Glukhov/Qi/El-Mhamdi/Anwar characterized from search-result summaries plus training knowledge, not fresh full-text fetches.
