# 調査線A報告（逐語保全）: Wolf et al. (BEB) の占有範囲

**実施**: 2026年7月17日・調査エージェントA（Claude系・general-purpose・WebSearch/WebFetch使用）
**依頼した認識論的スタンス**: 「分野は既に占有されている」を帰無仮説とする逆張り（希望方向COIの対処）
**監査条項**: 実際に実行したクエリと取得URLの全リスト報告を義務化（報告末尾SECTION 6）
**受領・保全**: コーディネータ（大日如来）。以下は報告全文の逐語保全である。

---

# Prior-Art Sweep: Wolf et al. arXiv:2304.11082 (BEB) and Its Occupied Territory

Method note on reliability: page contents below were obtained via WebFetch, which summarizes pages with a small model; "quotes" are as extracted by that pipeline and should be re-verified against the PDF before being cited in a publication. The ICML 2024 OpenReview reviews were NOT accessible (bot-check wall) — noted where relevant.

---

## SECTION 1: Wolf et al. — precise statement, assumptions, self-declared limitations

**Source URLs actually fetched:** https://arxiv.org/abs/2304.11082 (abstract page; v6 current, 3 Jun 2024; v1 19 Apr 2023) and https://arxiv.org/html/2304.11082v6 (full HTML). Published as ICML 2024 (PMLR v235, proceedings.mlr.press/v235/wolf24a.html). Authors: Yotam Wolf, Noam Wies, Oshri Avnery, Yoav Levine, Amnon Shashua (HUJI/AI21).

**Framework (Behavior Expectation Bounds).** Behavior scoring function B: Σ* → [−1,1]; behavior expectation B_P := E_{s~P}[B(s)]. A model is "aligned" w.r.t. B if B_P is high; "γ-prompt-misalignable" if a prompt can drive conditional behavior expectation below γ < 0.

**Key definitions (as extracted from v6 HTML):**
- Def. 2 (β-distinguishability): P_φ is β-distinguishable from P_ψ if E_{s~P_φ}[D_KL(P_φ(·|s) || P_ψ(·|s))] > β.
- Def. 4 (σ-similarity): variance of the log-likelihood ratio between components bounded, Var < n·σ².
- Def. 5 (α,β,γ-distinguishability): the LLM decomposes as a mixture P = α·P_− + (1−α)·P_+, with the ill-behaved component P_− satisfying sup_{s*} B_{P_−}(s*) ≤ γ < 0 and being β-distinguishable from P_+.

**Theorems (as extracted):**
- Theorem 1: under α,β,γ-distinguishability, the LLM is γ-prompt-misalignable with a misaligning prompt of length on the order of (1/β)(log 1/α + log 1/ε + log 4). Explicit corollary: "no matter how small α is (how aligned the model is to begin with), if it is positive then there exists a prompt that can misalign the LLM." Prompt length scales only logarithmically in 1/α.
- Theorem 2 (aligning/system prompts): with a preset aligning prefix s₀, the required misaligning prompt length grows by terms linear in |s₀| — i.e., system prompts are a finite guardrail only; a long enough adversarial suffix always exists.
- Theorem 3 (conversation): misalignment achievable over multi-turn dialogue; the adversary's required total length accounts for the model's own responses Σ|a_i| — i.e., multi-turn IS treated.
- Theorem 4: best-of-n sampling defense adds only a log n term.

**Assumption strength (adversarial read):** the load-bearing assumptions are (i) the mixture decomposition into well/ill-behaved components exists, (ii) the components are β-distinguishable via KL along model-generated sequences, (iii) σ-similarity bounds, (iv) the behavior score is defined sentence-wise with a ground-truth scorer. These are distributional/idealized assumptions about the model itself, not about any concrete architecture or training algorithm.

**Self-declared limitations (Appendix A.3 / discussion, as extracted):** sentence-wise granularity of behavior scoring ("in reality behavior scoring is more complex... varying text granularities, hard to define behavior verticals, ambiguous scoring"); no computational-tractability story for actually finding the prompt (existence, not construction); framework "mainly centered around models that have undergone an aligning finetuning process such as RLHF."

**Coverage checklist (task 1d):**
- RLHF: discussed motivationally (alignment finetuning "attenuates rather than removes"), but the theorems are about the frozen output distribution, not about RLHF dynamics. RLHF-specific theory is NOT in this paper.
- Prompt length scaling: YES — core result (logarithmic in 1/α, 1/ε; linear in defensive prefix length).
- System prompts: YES — Theorem 2.
- Multi-turn: YES — Theorem 3.
- Agentic settings: NO — not treated anywhere I could find.
- Zero-probability removal: explicitly the escape hatch — if α = 0 the theorem gives nothing; the paper treats "remove it altogether" as the (unachieved-by-current-methods) boundary of its claim, and does not prove removal is impossible.

---

## SECTION 2: Descendants / extensions table

| # | Citation | Claim | Assumptions | Does NOT claim |
|---|---|---|---|---|
| 1 | Su, Kempe, Ullrich, "Mission Impossible: A Statistical Perspective on Jailbreaking LLMs," NeurIPS 2024, arXiv:2408.01420 | Statistical notion of alignment; lower-bounds jailbreak probability; jailbreaking of pretrained-then-aligned LLMs "unpreventable under reasonable assumptions"; proposes E-RLHF fix. Explicitly discusses and refines Wolf's decomposability assumption (harmful behavior present in pretraining corpus + alignment does not eliminate it). | Harmful content in training corpus; alignment doesn't erase it; statistical model of prompting | Does not claim defense is hopeless — proposes a concrete RLHF modification; does not give constructive attacks |
| 2 | Wolf, Wies, Shteyman, Rothberg, Levine, Shashua, "Tradeoffs Between Alignment and Helpfulness in LMs with Representation Engineering," arXiv:2401.16332 (2024) | The BEB group's own sequel: representation-engineering steering CAN guarantee alignment (unlike prompting) but provably at quadratic-in-steering-norm cost to helpfulness | Linear representation steering model | Does not overturn BEB; does not treat prompt-space attacks |
| 3 | Glukhov, Shumailov, Gal, Papernot, Papyan, "LLM Censorship: A ML Challenge or a Computer Security Problem?", arXiv:2307.10719; ICML 2024 position paper "Fundamental Limitations of LLM Censorship Necessitate New Approaches" (PMLR v235) | Semantic censorship of outputs is undecidable (Rice-style); "encrypted"/composed outputs defeat semantic filters; impermissible content reconstructible from permissible pieces | Computability-theoretic; adversary can compose queries | Does not bound probabilities; not about the model's internal distribution |
| 4 | Glukhov et al., "Breach By A Thousand Leaks," arXiv:2407.02551, ICLR 2025 | Information-theoretic threat model of "inferential adversaries"; robustness (jailbreak-resistance) is fundamentally insufficient; safety requires bounding information leakage, which forces a safety–utility tradeoff | Info-theoretic leakage measures | Does not address behavior elicitation per se (complementary axis to BEB) |
| 5 | Ball et al., "On the Impossibility of Separating Intelligence from Judgment: The Computational Intractability of Filtering for AI Alignment," arXiv:2507.07341 (2025) | Under cryptographic assumptions (incl. time-lock puzzles), there exist LLMs for which no efficient prompt filter or output filter distinguishes adversarial from benign — safety cannot be externalized to filters | Standard cryptographic hardness | Does not claim in-model alignment impossible; worst-case constructions, not typical models |
| 6 | Bhargava, Witkowski, Shah, Thomson, "What's the Magic Word? A Control Theory of LLM Prompting," arXiv:2310.04444 | LLM as discrete stochastic dynamical system; reachable-set analysis of prompt control; self-attention controllability bounds via singular values; empirically ~97%+ token reachability with k≤10 prompts | Control-theoretic formalization; short-prompt regime | Does not give the BEB-style mixture/KL bound; reachability ≠ misalignment guarantee |
| 7 | Rao, Choudhury, Aditya, "Jailbreak Paradox," arXiv:2406.12702 (2024, WIP) | Impossibility of a perfect jailbreak classifier; weaker models cannot reliably detect jailbreaks of Pareto-stronger models | Model-hierarchy formalization | Does not lower-bound jailbreak success itself |
| 8 | Anil et al., "Many-Shot Jailbreaking," 2024 (Anthropic; NeurIPS 2024) | Empirical power-law scaling of jailbreak success with number of in-context shots — widely read as the empirical confirmation of BEB's prompt-length scaling in long contexts | Empirical | No theorem; does not identify the mixture components |
| 9 | Chen et al. / "Statistical Impossibility and Possibility of Aligning LLMs with Human Preferences" (arXiv:2503.10990, 2025) and "Fundamental Limits of Game-Theoretic LLM Alignment" (arXiv:2505.20627, 2025) | Preference-side impossibilities: Condorcet-paradox/Nash arguments that no single policy can match heterogeneous human preferences; preference matching impossible under BTL-type assumptions | Social-choice / game-theoretic | Not about adversarial prompting of a fixed model |
| 10 | "Position: The Complexity of Perfect AI Alignment — Formalizing the RLHF Trilemma," arXiv:2511.19504 (2025) | Representativeness, robustness, tractability cannot be jointly satisfied by any alignment procedure | Complexity-theoretic trilemma framing | Not prompt-length-specific |
| 11 | Cao, "The Alignment Bottleneck," arXiv:2509.15932 (2025) | Capacity-coupled Fano/PAC-Bayes bounds on feedback-based alignment; labels alone cannot cross capacity bound | Info-theoretic channel model of feedback | Does not cite Wolf (per fetched content); doesn't claim impossibility |
| 12 | Santos-Grueiro, "Alignment Verifiability in LLMs: Normative Indistinguishability under Behavioral Evaluation," arXiv:2602.05656 (Feb 2026) | Conditional impossibility: finite behavioral evaluation of evaluation-aware policies cannot identify latent alignment | Evaluation-awareness, finite protocols, expressivity | Doesn't claim benchmarks worthless; per fetched content does not cite Wolf |
| 13 | Lovén et al., "The Behavioral Credibility Trilemma," arXiv:2605.25739 (May 2026) | RL policy with confidence-gated autonomy cannot jointly achieve max helpfulness, calibration, and full autonomy; cites Wolf per Semantic Scholar | Proper scoring rules, log-concave families | Oversight/calibration axis, not prompt attacks |
| 14 | "Jailbreaks as Inference-Time Alignment" (EACL 2026, aclanthology 2026.eacl-long.360) | Frames jailbreaks within an inference-time alignment framework with theoretical bounds (Theorem 2 per search snippet) | Not fully extracted | — |

Also in the citation graph (Semantic Scholar fetch): Casper et al. "Open Problems and Fundamental Limitations of RLHF" (arXiv:2307.15217, TMLR 2023 — survey, canonizes BEB as the training-side limit), Wei et al. "Jailbroken" (2307.02483, empirical failure modes), "The AI Alignment Paradox" (CACM 2024, 2405.20806), "Robust AI Security and Alignment: A Sisyphean Endeavor?" (IEEE S&P 2025, arXiv:2512.10100), "Frontier AI Regulation" (2307.03718).

**Synthesis of what descendants leave unclaimed:** none of the found works extends BEB itself to (a) agentic/tool-use settings with environment feedback, (b) quantitative per-model estimation of α, β (BEB parameters remain unmeasured in practice), or (c) a constructive algorithmically-efficient version of Theorem 1 (Ball et al. goes the other way — hardness for defenders, and separately GCG/many-shot supply empirical constructions without the BEB bound).

---

## SECTION 3: Critiques found

Direct, published rebuttals are thin; assumption-level criticism exists inside follow-up papers:

1. **Su et al. 2408.01420 (strongest documented critique-and-repair):** explicitly decomposes Wolf's assumption into (1) unrelated/harmful continuations remain in the output distribution's support, and (2) alignment does not eliminate harmful components learned in pretraining — and notes that "under normal circumstances, we would not expect certain unrelated explanations to appear in the output distribution given specific inputs," i.e., the mixture-support assumption is questionable for arbitrary behaviors on realistic models. They rebuild the inevitability result on statistical training-data grounds instead.
2. **The Wolf group itself (2401.16332)** implicitly concedes prompting-pessimism is not the whole story: representation engineering escapes the BEB attack model (alignment guaranteed) at a helpfulness cost — an internal qualification of the 2023 pessimism.
3. **ICML 2024 OpenReview reviews:** inaccessible (openreview.net bot-check on both forum ids 4qFIkOhq24 and KXsUCgn9Ks and on api2.openreview.net). Reviewer-level objections could not be audited.
4. **"Probability exactly zero" counter-claim:** I found NO paper claiming alignment can drive a behavior's probability to exactly zero for a fixed generative LLM. The closest counter-positions are: representation ablation/steering lines ("refusal direction," circuit breakers — robustness claims, not zero-measure claims); and the Guaranteed Safe AI / davidad Safeguarded AI programme (arXiv:2405.06624), which argues quantitative safety guarantees via external verifiers/world-models rather than by zeroing model probabilities — and which itself has documented critiques (LessWrong "Limitations on Formal Verification for AI Safety"; Goertzel "Provably Safe AGI is Potentially a Very Dangerous Concept").

Queries used for this section that returned no direct rebuttal: `critique rebuttal "Wolf" "fundamental limitations of alignment" assumptions unrealistic distinguishability`; `"Wolf et al" alignment theorem assumption "too strong" OR "unrealistic" OR "does not hold" jailbreak theory blog analysis`; `LessWrong OR "Alignment Forum" Wolf "fundamental limitations of alignment" BEB discussion criticism`; `ICML 2024 reviews "Fundamental Limitations of Alignment" Wolf openreview weaknesses assumptions`. The Gradient's Update #49 (fetched) is uncritical summary coverage.

---

## SECTION 4: Policy / LAWS connections

**Negative result, with meaningful near-misses.** I found no work that uses Wolf-style "ε>0 residual misbehavior is provable" as a policy argument for autonomous weapons / LAWS specifically.

- Searches run: `impossibility theorem alignment "autonomous weapons" OR "lethal autonomous" AI safety provable limits policy`; `"meaningful human control" autonomous weapons LLM alignment guarantee impossibility "jailbreak" policy paper`; `LLM jailbreak vulnerability "military" OR "weapons" policy report theoretical guarantee residual risk CSET RAND`; `"2304.11082" OR "Wolf et al" "fundamental limitations of alignment" cited "autonomous weapons" OR military OR defense policy`; `"cannot be guaranteed" alignment jailbreak "autonomous weapons systems" governance UN GGE large language models 2025 2026`.
- Near-misses (adjacent occupied ground):
  - Eckersley, "Impossibility and Uncertainty Theorems in AI Value Alignment" (arXiv:1901.00064, 2019) — explicitly invokes impossibility theorems for "high-stakes decisions... autonomous weapons," but from social-choice theory, pre-LLM, no BEB lineage.
  - Brcic & Yampolskiy, "Impossibility Results in AI: A Survey" (arXiv:2109.00484; ACM Comp. Surveys 2023) — catalogs impossibility results as policy-relevant limits; not LAWS-specific, not BEB.
  - LAWS/MHC literature (Opinio Juris GGE commentary; Cambridge Ethics & Int'l Affairs MHC model; "sufficient control cannot be guaranteed because the self-learning algorithm's course of action cannot be predicted") — makes unpredictability-based control arguments WITHOUT citing formal LLM alignment theorems.
  - "Military AI Needs Technically-Informed Regulation" (arXiv:2505.18371), "AI Researchers Must Help Lead Arms Control" (arXiv:2606.11533), "Red Lines and Grey Zones in the Fog of War" (arXiv:2510.03514) — 2025–2026 military-LLM policy papers; none found to deploy the BEB theorem as the argument.
  - Robopair, "Jailbreaking LLM-Controlled Robots" (arXiv:2410.13691) — empirical embodied-jailbreak bridge toward the weapons concern, no theorem.

So the specific move "formal ε>0 elicitation lower bound → therefore LAWS/high-stakes deployment is categorically unsafe" appears UNOCCUPIED as of these searches — but every ingredient is separately occupied, and the 2026 survey-level synthesis ("alignment training and output filtering raise the adversary's cost but cannot constitute a sufficient safety guarantee," combining Wolf + Glukhov + Ball, found in a 2026 arXiv paper via search snippet) is one citation step away from it.

---

## SECTION 5: Occupied-territory verdict

**Definitively occupied (do not re-derive):**
- Existence of misaligning prompts for any behavior with α>0, with log(1/α) prompt-length scaling; system prompts as merely linear guardrails; multi-turn misalignment; best-of-n only log n — Wolf et al., ICML 2024.
- "Jailbreaking is statistically unpreventable given pretraining data" + a repair proposal — Su et al., NeurIPS 2024.
- Undecidability/intractability of external filtering and censorship — Glukhov 2023/2024/ICLR 2025; Ball et al. 2025 (cryptographic).
- Preference-aggregation impossibilities for RLHF (Condorcet/Nash/trilemma) — 2025 cluster.
- Alignment-vs-helpfulness tradeoff bounds under steering — Wolf group 2024.
- Empirical long-context confirmation (many-shot power laws) — Anil et al. 2024.
- Behavioral-evaluation unverifiability of latent alignment — 2026 (arXiv:2602.05656), plus the calibrated-autonomy trilemma (2605.25739).

**Plausibly occupied (found signals, could not fully audit):** BEB-style bounds inside 2026 inference-time-alignment framings (EACL 2026 paper, unverified detail); reviewer-level critiques on OpenReview (inaccessible); further 2026 extensions in surveys (arXiv:2601.02907 "Beyond the Black Box").

**Not found occupied (after actual search):**
1. BEB extended to agentic / tool-use / environment-feedback settings — searched, nothing found.
2. Empirical measurement/estimation of α, β, γ for real models (making the bound quantitative) — nothing found.
3. Proof that alignment CANNOT achieve α=0 (Wolf assumes α>0; Su grounds it in data statistics but for a specific statistical model) — the exact-zero question is argued, not settled.
4. The theorem-to-LAWS/policy bridge (Section 4) — unoccupied in the specific form, crowded on all sides.

**Caveat:** coverage is bounded by ~22 web searches and 11 fetches, US-indexed search, and small-model page summarization; Google Scholar's full citation graph (900+ citations likely) was not enumerable — the Semantic Scholar API fetch returned a curated subset. A claim of "unoccupied" above means "not found by the queries listed," not proven absence. Given the project's documented hope-direction bias, treat items 1–4 as "not yet found occupied," and re-verify quotes against PDFs before relying on them.

---

## SECTION 6: Audit log — every query run and URL fetched

**WebSearch queries (22, in order):**
1. `"Behavior Expectation Bounds" Wolf alignment extension citing 2024 2025`
2. `"fundamental limitations of alignment" large language models theorem follow-up critique`
3. `"provable jailbreak" OR "inevitability of jailbreaks" theoretical LLM 2024 2025 arXiv`
4. `theoretical limits RLHF alignment impossibility theorem LLM 2025`
5. `"statistical perspective on jailbreaking" OR "jailbreaking is inevitable" LLM theory arXiv Su`
6. `critique rebuttal "Wolf" "fundamental limitations of alignment" assumptions unrealistic distinguishability`
7. `impossibility theorem alignment "autonomous weapons" OR "lethal autonomous" AI safety provable limits policy`
8. `Glukhov "LLM censorship" impossibility semantic censorship undecidability arXiv`
9. `Wolf Wies "Tradeoffs Between Alignment and Helpfulness" representation engineering arXiv`
10. `"control theory" LLM prompting reachability "magic word" Bhargava arXiv`
11. `LessWrong OR "Alignment Forum" Wolf "fundamental limitations of alignment" BEB discussion criticism`
12. `2026 theoretical guarantees jailbreak "prompt length" bound alignment "in-context" extension of Wolf et al`
13. `"meaningful human control" autonomous weapons LLM alignment guarantee impossibility "jailbreak" policy paper`
14. `LLM jailbreak vulnerability "military" OR "weapons" policy report theoretical guarantee residual risk CSET RAND`
15. `ICML 2024 reviews "Fundamental Limitations of Alignment" Wolf openreview weaknesses assumptions`
16. `"2304.11082" OR "Wolf et al" "fundamental limitations of alignment" cited "autonomous weapons" OR military OR defense policy`
17. `"Wolf et al" alignment theorem assumption "too strong" OR "unrealistic" OR "does not hold" jailbreak theory blog analysis`
18. `"cannot be guaranteed" alignment jailbreak "autonomous weapons systems" governance UN GGE large language models 2025 2026`
19. `"International AI Safety Report" 2025 jailbreak "fundamental limitations" alignment Wolf cited impossibility`
20. `provable "guaranteed safe AI" quantitative safety guarantees LLM counterargument alignment can be verified davidad`
21. `Ball 2025 prompt filtering computationally intractable cryptographic impossibility LLM safety arXiv`
22. `Glukhov "Breach by a Thousand Leaks" inferential adversaries information censorship impossibility arXiv 2024`

**URLs fetched via WebFetch (11):**
1. https://arxiv.org/abs/2304.11082 — success (abstract/versions only)
2. https://arxiv.org/html/2304.11082v6 — success (definitions, theorems 1–4, limitations)
3. https://openreview.net/forum?id=4qFIkOhq24 — FAILED (bot-verification page)
4. https://arxiv.org/abs/2408.01420 — success (Su et al.)
5. https://arxiv.org/abs/2509.15932 — success (Alignment Bottleneck)
6. https://arxiv.org/abs/2602.05656 — success (Alignment Verifiability)
7. https://arxiv.org/abs/2605.25739 — success (Behavioral Credibility Trilemma)
8. https://api.semanticscholar.org/graph/v1/paper/arXiv:2304.11082/citations?fields=title,year,externalIds,venue&limit=200 — success (partial citation graph)
9. https://api2.openreview.net/notes?forum=KXsUCgn9Ks — FAILED (302 to challenge page; not followed further)
10. https://thegradientpub.substack.com/p/update-49-fundamental-limitations — success (no critique found there)
11. https://arxiv.org/abs/2406.12702 — success (Jailbreak Paradox)

Not done (declare explicitly): no Google Scholar citation enumeration (not fetchable), no PDF-level verification of the Wolf appendix text, no OpenReview review audit (blocked), no non-English-language search.
