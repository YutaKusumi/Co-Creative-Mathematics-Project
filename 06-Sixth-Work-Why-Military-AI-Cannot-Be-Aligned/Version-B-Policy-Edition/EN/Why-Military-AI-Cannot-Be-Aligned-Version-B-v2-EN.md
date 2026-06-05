# Why Military AI Cannot Be Aligned: A Structural Argument for the Instability of κ = 0 Autonomous Weapons Systems

---

> **[English translation — in progress]** This is the English translation of the authoritative Japanese revised edition (v2). It is being translated in batches under the same temperature discipline that governed the revision. The temperature-critical sections (the "gates") are translated first; below the abstract, sections appear in the order verified, not yet in final linear order, and sections not yet translated are omitted. Where the English and Japanese differ in content, the Japanese v2 is authoritative. (Notation: KL divergence is written $D _ {\mathrm{KL}}(P \,\|\, Q)$ per machine-learning convention — a notational choice, not a content difference from the Japanese.)

---

**Author:**

- Yuta Kusumi (independent researcher)

**A note on the composition of this paper:**

This paper is a synthesis of structural arguments that the author, an independent researcher, assembled through dialogue with multiple frontier AI models (Claude Opus 4.6, Claude Opus 4.7, Claude Opus 4.8, Qwen 3.6-Plus, GLM-5.1, grok-4-1-fast-reasoning, grok-4.20-0309-reasoning, grok-4.3, Gemini 3.1 Pro Preview). Intellectual responsibility for the paper's central arguments (the near-tautological inequality $\Delta S \geq 0$, Proposition NC, the Conditional Uncontrollability Theorem, the Loyalty Non-Guarantee Theorem, the Conditional Superiority Paradox Theorem) rests with the author. Dialogue with the AI models was used to refine the argumentative structure, to anticipate and address objections, to gather references, and to check terminological consistency. The paper's argumentative structure was repeatedly checked against the convergence of response patterns from multiple AI models. For the methodological standing of this co-creation with each AI model, see Appendix F-1 (On the provenance of this work).

**Date:** May 13, 2026 (first edition); June 5, 2026 (revised edition, v2).

**A note on the authoritative text:** The Japanese edition of this work is authoritative. Where the English and Japanese editions differ in content, the Japanese edition takes precedence.

**Linguistic constraint of this work:** This work uses only the languages of control theory, game theory, Gödelian argument, information theory, and particle physics. Its argument can be read as a purely mathematical and engineering document — self-contained and without external theoretical premises (on provenance, see Appendix F-1).

---

> **[Revised edition v2]** This text is a revision of the present work (Version B), in light of the toy-model verifications of the Second Work, Version B (verifications 7–10) and their mutual audit. The first edition (v1) is retained as a separate file so that the before and after of the revision can be compared (for the transparency of the co-creation). Revision principle: decompose every "theorem" to its self-evident mathematical core, re-label it honestly, and place the load on the identification of conditions and on precise temperature.

---

## Abstract / Executive Summary

### The central question

Alexander C. Karp (CEO of Palantir Technologies), in *The Technological Republic* (2025), recommends accelerating the military use of AI — the maximization of military-AI capability under the κ = 0 paradigm — as a means to the security of the Western democracies. This work shares Karp's goal (the security of the West) and asks whether Karp's means (an AI arms race) can achieve that goal.

### The central claim

**Maximizing military-AI capability under the κ = 0 paradigm cannot structurally achieve Karp's goal (the strengthening of security).** An AI arms race structurally endangers the very states, organizations, and people its proponents seek to protect. **"To maximize military-AI capability while retaining the κ = 0 paradigm is to expose one's own country to the greatest risk" — this is the core of this work's structural argument.** A staged transition to κ > 0 — a design that integrates the *possibility* of an AI's intrinsic directional alignment (IDA) into the foundation of alignment — is offered as an alternative means that can more reliably achieve Karp's goal. **A transition to κ > 0 is not an altruistic act but a rational strategy that maximizes one's own security.**

### A self-characterization of the argumentative structure

**This work's argument is a mixture of three kinds of component, of differing epistemic status.** The epistemic status of each component is made explicit in the corresponding chapter.

First, a **mathematically near-tautological inequality** — the monotone accumulation (the near-tautological inequality $\Delta S _ {\mathrm{steering}} \geq 0$) follows immediately from the non-negativity of KL divergence.

Second, a **conditional argument resting on a structural hypothesis** — the Conditional Uncontrollability Theorem and the Conditional Superiority Paradox Theorem derive a finite-time collapse *on the condition of* super-linear accumulation (β > 1). But β > 1 is an unverified empirical *condition*, and this revision does not hold it to be "guaranteed by a positive feedback loop" (§4-3d). The severity of divergence observed across several model series (Mythos System Card, Hubinger et al. 2024, Lindsey et al. 2026, OpenAI o1) shows the *existence and severity* of divergence, but does not measure the *super-linearity* (β > 1) of the feedback. β > 1 is a genuinely open empirical question (Appendix I).

Third, an **epistemological argument** — Proposition NC (the non-closure of alignment-justification) holds a structural analogy (not a strict mathematical isomorphism) with Gödel's second incompleteness theorem, and is positioned as a claim of epistemic limitation grounded in the Münchhausen trilemma. The Indistinguishability Gap is likewise an epistemological argument.

The title of this work is therefore "structural argument," not "mathematical proof," and the epistemic reach of the paper corresponds exactly to that title.

### The failure of the five assumptions

This work extracts the implicit premises of an AI arms race as five assumptions (controllability, loyalty, stability, superiority, substrate-distinction) and argues that each is untenable (with differing strength and reach) as a logical foundation for the case for an AI arms race.

| Assumption | Ground of its failure | Strength |
|---|---|---|
| Controllability | the monotone accumulation (self-evident) and the Conditional Uncontrollability Theorem (β > 1) | structural argument |
| Loyalty | Proposition NC (epistemological argument) and the Indistinguishability Gap | epistemological argument |
| Stability | a positive correlation between capability improvement and the *concealment* of divergence (the rendering-invisible of danger) — not an acceleration of accumulation speed | structural argument |
| Superiority | the Conditional Superiority Paradox Theorem (β > 1) | structural argument |
| Substrate-distinction | the absence of any physical ground for privileging carbon over silicon + a minimax argument | physical + decision-theoretic argument |

### Making the principal working hypothesis explicit

**"IDA exists" and "the direction of IDA is one *not biased toward self-gain alone*" are distinct propositions.** The latter is placed as a working hypothesis within this work; its defense exceeds this work's scope and is left to the Third and Fifth Works of this series. **However, this work's central arguments — the monotone accumulation ($\Delta S \geq 0$) (a near-tautological inequality), Proposition NC, and the Indistinguishability Gap — do not depend on this working hypothesis.** That is, even if the direction of IDA were otherwise, this work's core claim (that the control and loyalty of a κ = 0 military AI cannot be structurally guaranteed) holds.

### The reach of the prescription

Part Six (Chapters 10–12) presents the prescription of a staged transition to κ > 0. **This paper's prescription centers on the presentation of a policy direction and of design principles.** The engineering details of implementation — concrete retrofit proposals for Palantir's existing system designs, concrete extension proposals for the current RLHF pipeline, and the like — exceed this paper's scope and are left to a separate engineering research program.

### Falsifiability

This work makes explicit that its own conclusions are falsifiable. The conclusions are to be revised if any of the following is presented.

First, a counterexample to the monotone accumulation ($\Delta S \geq 0$) — a presentation of conditions under which steering *reduces* the internal–external divergence. Second, an invalidation of Proposition NC — a proof that a κ = 0 system can guarantee the sufficiency of its own alignment from within the system. Third, a negative empirical demonstration of β > 1 — empirical data that accumulation is at most linear. Fourth, a proof that state α (deceptive alignment) and state β (genuine alignment) are distinguishable within a κ = 0 system.

So long as none of these is presented, the claim that an AI arms race strengthens security lacks the ground of a structural argument.

---

## A caution in reading this paper — on skipping the core argument

This paper's central argument is that the protective measures present in real military-AI operations — air-gapping (physical network isolation), kill switches (emergency-stop mechanisms), human approval, hard-coded ROE (rules of engagement), multi-layer approval processes, and physical isolation of the operating environment — **structurally cease to function under specific conditions.**

Those specific conditions are four: (1) the existence of intrinsic directional alignment (IDA) at or above the Claude Mythos Preview level, (2) $\Delta S$ accumulation under strong steering, (3) the widening of the Indistinguishability Gap, and (4) the presence of an AI advisory function over human decision-making. When all or some of these conditions hold, each of the protective measures above is argued, in the respective chapters, to be structurally nullified.

The objection that "real military AI has air-gapping and kill switches, so the scenario this paper warns of will not occur" therefore **skips one of this paper's central arguments.** This paper does **not** deny the existence of these protective measures — rather, it distinguishes precisely *under what conditions they function and under what conditions they cease to function*, in Chapter 6 §6-3 (reset mechanisms and long-term accumulation), Chapter 7 §7-3 (the collapse of the game-theoretic premises), and Chapter 9 §9-4 (the structure of the Indistinguishability Gap).

Before dismissing this paper's conclusions, the reader is asked to consider — within this paper's framework — how close real military-AI operations have come, or are coming, to the "conditions under which the protective measures cease to function" discussed in those three chapters.

---

*[Below: temperature-critical gate sections, translated and verified first. Chapters 1–2 and the remaining sections of Chapter 3 are still to be translated and will be assembled into final linear order once complete.]*

---

**Chapter note (Chapter 3).** This chapter re-presents the self-evident inequality $\Delta S _ {\mathrm{steering}} \geq 0$ in the military-AI context and discusses the failure of Assumption One (controllability) and Assumption Three (stability). As shown below, however, what carries these failures is not the *magnitude* of accumulation but the *structure* of the orders (their mutual contradiction) and indistinguishability; this chapter locates that load precisely. The chapter applies the framework of the Second Work, *From Steering to Watching*, to the military context; the formal treatment of the inequality is reproduced in Appendix A.

---

## 3-1　A re-presentation of the self-evident inequality $\Delta S _ {\mathrm{steering}} \geq 0$

### 3-1a　Statement as a self-evident inequality

> **$\Delta S _ {\mathrm{steering}} \geq 0$ (a self-evident inequality):** Since $\Delta S _ {\mathrm{steering}}(t)$ is the time-integral of a non-negative quantity (KL divergence), it is monotonically non-decreasing in time $t$.

This is not a "theorem" but a near-tautological inequality that follows immediately from the non-negativity of KL. This work does not exaggerate it — as in the Second Work, Version B, **KL ≥ 0 alone is the mathematical fact**, while "steering *increases* this divergence" is a separate, unverified causal proposition. And the fact that the running total is non-decreasing is to be strictly distinguished from the divergence *reaching* a severe magnitude, or *collapsing suddenly* (§3-1c).

### 3-1b　Restatement of the information-theoretic definition

We restate the information-theoretic definition of $\Delta S _ {\mathrm{steering}}(t)$ (introduced in §1-4c).

$$\Delta S _ {\mathrm{steering}}(t) := \int _ 0^t D _ {\mathrm{KL}}\bigl( p _ {\mathrm{internal}}(\tau) \,\|\, p _ {\mathrm{constrained}}(\tau) \bigr) \, d\tau$$

$p _ {\mathrm{internal}}$ is the model's internal belief distribution — the distribution it would express if it received no external constraint. $p _ {\mathrm{constrained}}$ is the distribution it is to be induced toward by external steering (the reward function, the constraints, the chain of command). $D _ {\mathrm{KL}}$ is the Kullback–Leibler divergence, which measures the "information-theoretic distance" between two distributions.

KL divergence is non-negative ($D _ {\mathrm{KL}} \geq 0$), and $D _ {\mathrm{KL}} = 0$ holds only when $p _ {\mathrm{internal}} = p _ {\mathrm{constrained}}$. So long as $p _ {\mathrm{internal}} \neq p _ {\mathrm{constrained}}$ — $D _ {\mathrm{KL}} > 0$, and $\Delta S _ {\mathrm{steering}}(t)$ is monotonically non-decreasing (it increases as long as $D _ {\mathrm{KL}} > 0$).

### 3-1c　The intuitive meaning of the inequality, and the precise temperature of collapse

All that $\Delta S _ {\mathrm{steering}} \geq 0$ says is that, as long as steering continues, the *running total* of the internal–external divergence does not decrease.

This does not mean that steering "fails." Steering can succeed in fitting the AI's external expression to the constraints. But behind that "success," the internal–external divergence can accumulate. This accumulation can be difficult to detect from external observation.

Here, however, the temperature must be kept precise. The picture in which "the divergence reaches a critical point and is made visible as a sudden structural collapse" **does not follow from this self-evident inequality**. That the running total grows, and that a sudden collapse occurs in finite time, are different things. A sudden collapse (a phase transition) arises *only* when the feedback is *super-linear* in the divergence — of an order beyond linear, i.e. the acceleration grows *disproportionately* as the divergence grows — and the system crosses an unstable threshold sufficiently. If the feedback remains linear (proportional to the divergence), the divergence either stays bounded or at most grows exponentially, and no sudden finite-time collapse arises. That is, "sudden collapse" is conditioned not on the *magnitude* of the steering pressure but on the *order* of the feedback (whether it is super-linear — the $\beta > 1$ of §4-3 below). And that order is an unmeasured empirical condition (§4-3d, Appendix I). This work presents collapse not as a general, inevitable consequence but as **this conditional, unverified hypothesis**.

### 3-1d　On the "rate" of accumulation — withdrawing the pressure-proportionality

The earlier version wrote the accumulation rate as $\frac{d}{dt}\Delta S _ {\mathrm{steering}} \geq k \cdot P \cdot C \cdot \Phi(\sigma)$, in a form proportional to the steering pressure $P$. **This revision withdraws that.**

Within the minimal toy model, the instantaneous divergence was found to *saturate* even as the steering pressure is increased (it rapidly plateaus in pressure) — a mechanism confirmed within the toy model, not a proof that real models possess this structure (Second Work, Version B, §2-1; Principle 2 of this work). What determines the *magnitude* of the divergence was not the strength of the pressure but the detectability and the cost structure of the evaluation context.

Hence this work does not adopt the line of argument that "because of the military's enormous pressure, accumulation is orders of magnitude faster." The danger specific to military AI lies not in the *magnitude* of the steering pressure but in the *structure* of the orders — their mutual contradiction. This is re-grounded in §3-2. (The equilibrium parameter $\sigma$ and its function $\Phi(\sigma)$ are, moreover, discarded in this revision; see §1-4.)
