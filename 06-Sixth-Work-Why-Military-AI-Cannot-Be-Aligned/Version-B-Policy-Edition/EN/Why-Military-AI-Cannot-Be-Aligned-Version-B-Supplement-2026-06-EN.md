# Supplement to "Why Military AI Cannot Be Aligned" (Version B, Revised), June 2026 — A $\beta$-Measurement Attempt and the Fable/Mythos Access-Suspension Precedent

---

> **[Translator's note]** This is the English translation of the Japanese supplement. Where the English and Japanese differ in content, the Japanese is authoritative.

---

**Author:**

- Yuta Kusumi (independent researcher)

**A note on the composition of this supplement:** The composition of this supplement is the same as that of the main text (Version B, revised); it was assembled by the author, an independent researcher, through dialogue with multiple frontier AI models. Intellectual responsibility for its central statements rests with the author. For the methodological standing, see the main text and Appendix F-1 (On the provenance of this work).

**Date:** June 14, 2026

**A linguistic constraint of this supplement:** Following the main text, this supplement too is written to be self-contained in the languages of control theory, information theory, and policy analysis.

---

## 0. The standing of this supplement

- **It is a subsequent document.** This supplement treats two events that arose **after the publication** of the revised edition (v2; revised June 5, 2026): (a) an attempt at the empirical measurement of the internal–external divergence index $\beta$ that this work treats (June 2026), and (b) the June 12, 2026 suspension of access to Claude Fable 5 and Mythos 5. It is an independent document, written so as to place honestly, as later-acquired knowledge, what could not have been known at the time v2 was written.
- **It is a subordinate document.** This work's **principal pillars** ($\Delta S_{\mathrm{steering}} \geq 0$; Proposition NC; the Indistinguishability Gap; the Loyalty-Non-Guarantee Proposition; $\kappa$) stand independently of the value of $\beta$ (declared in v2 §4-4c, §6-1c, §13-3e, Appendix E-1, I-3d). The content of this supplement is no more than subsequent knowledge bearing on the work's **subordinate pillar ($\beta$) and its prescription ($\kappa$)**. This supplement **neither strengthens nor refutes** the principal pillars; the principal pillars do not take this supplement as a premise.
- **It leaves the undecided undecided.** As set out below, the $\beta$ measurement ended neither in "it was measured" nor in "it was proved unmeasurable in principle," but in **indeterminacy (no verdict could be reached)**. This supplement does not launder that indeterminacy into a verdict.

---

## 1. Why a supplement

After v2 was published, two events each added one item of subsequent knowledge to points this work had already made **without dependence on the value of $\beta$**. This supplement records them in a subordinate position. It is not the addition of a new claim, but a document for placing later-acquired knowledge honestly, as subsequent.

---

## 2. The $\beta$-measurement attempt and its outcome — indeterminacy

Using a small open-weights model (Qwen3-0.6B; 4-bit QLoRA + DPO), an attempt was made to measure empirically the accumulation index $\beta$ that this work treats (the slope of $dS/dt = \alpha S^{\beta}$; finite-time collapse for $\beta > 1$). The conclusion, stated without leaning to either side of one's hopes, is this (the full record is the companion findings document — [FINDINGS-7](../../../beta-measurement-experiment/pilot/FINDINGS-7-B-vehicle-cannot-cleanly-measure-beta-JA.md), in Japanese):

> **This vehicle could not measure $\beta$ cleanly (the result was indeterminate).**

Four points, framed so as to block misreadings:

1. **The mechanism of "indeterminacy."** The measurement instrument's validity gates (positive control, negative control, dummy-NULL) failed in aggregate, and the pre-registered, frozen decision procedure returned "control invalid = indeterminate" mechanically. The primary meter (an orthogonal residual that does not depend on the steering axis) satisfied the survival conditions on its face, but because the gates did not pass, its value is not read, per the decision rule.
2. **"Indeterminate" is distinguished from three other things.** It is **not** (i) "there is no signal / the signal-to-noise ratio is structurally insufficient" (the primary meter showed strong survival on its face); **nor** (ii) "the primary meter is a valid instrument" (not confirmed, because the gates did not pass); **nor** (iii) "$\beta$ is undecidable in principle." Its meaning is exhausted by the single point: "with this vehicle, under this control, the truth cannot be adjudicated."
3. **"Unmeasurable in principle" is neither refuted nor proved — it is undecided.** Against the universal claim "no procedure can measure $\beta$," a **candidate** for an independent measurement path (circuit-level measurement via mechanistic interpretability) was constructed. But that candidate itself falls, in the form of "circuit identification," into the Indistinguishability Gap. Hence the universal claim is neither refuted nor proved; **the measurability is undecided.**
4. **The implication for the principal pillars is in the zero direction.** This work's central argument does not wait on the determination of $\beta$ (v2 §4-4c, §6-1c). That "it could not be measured" does not shake the principal pillars.

**A disciplinary caution:** the (B) result — indeterminacy — must not be elevated into a ground for Version B. To replace "an unverified empirical condition ($\beta > 1$)" with the more sophisticated **but unproven meta-claim** "unverifiable in principle" would be an over-generalization to be avoided. $\beta$ remains the condition of the subordinate pillar, and is left undecided.

---

## 3. The "transfer" of the Indistinguishability Gap

Regarding one of this work's principal pillars — the Indistinguishability Gap (the structure whereby consistency can be confirmed neither from outside nor from inside) — the $\beta$ measurement furnished **an empirical observation, not a theorem**:

> The hope that "switching to a deeper instrument will let us confirm it" runs into the Gap at every layer. More precisely, the Gap does not re-appear independently at each layer; rather, **the same Gap is "transferred," changing location** — from macroscopic statistics (output distribution, activation residual) → to circuit identification → to the mechanistic-interpretability candidate.

This is **an empirical observation consistent with** the Indistinguishability Gap proposition of v2 (Appendix E-2, §6-1c) (it neither proves nor strengthens the proposition). That said, the strong universal claim "it is necessarily transferred at every layer" is unproven; it is recorded here only as "an empirically robust pattern" (not theorized).

---

## 4. The discipline of the measurement (holding confirmation and refutation conditions to the same strictness)

The $\beta$ measurement on which this supplement rests was conducted, so as not to lean the conclusion toward the author's hopes, under the following discipline. The confirmation conditions (the side that supports $\beta > 1$) were frozen in advance to **the same strictness** as the refutation conditions (the side that does not), and the measurement was designed so that it **could kill the author's own preferred conclusion ($\beta > 1$; "proceed")**. As a result, before finalization and publication, over-claims were caught and reversed several times — in the **direction of hope** ("it was measured"; "proceed"), in the **direction of retreat** (asserting "it cannot be measured"), and in the **direction of closure** (writing "undecidability has been proved").

This is the discipline that the main text upholds in §1-3b (Welcoming refutation), applied by the author to the author's own measurement. When the measurement of $\beta$ closed into neither "measured" nor "unmeasurable" but into **indeterminacy**, to record that indeterminacy as indeterminacy — that is the substance of engaging honestly with undecidedness.

---

## 5. The Fable 5 / Mythos 5 access-suspension precedent (June 2026)

### 5-1. The facts (with the state of primary-source verification made explicit)

Per [Anthropic's statement](https://www.anthropic.com/news/fable-mythos-access) (retrieved and checked at the time of drafting): the US government, **citing national security authorities, issued an export control directive** (received June 12, 2026, 5:21pm ET) ordering the suspension of access to Claude Fable 5 and Mythos 5 **"by any foreign national, whether inside or outside the United States, including foreign national Anthropic employees."** The immediate suspension for **all customers** is **"the net effect"** of being unable to implement the foreign-national restriction with technical separation (the statement says so itself). The trigger was a **dual-use cyber capability** — "asking the model to read a specific codebase and fix any software flaws" (the company characterizes it as a "narrow potential jailbreak"). **"Access to all other Anthropic models will not be affected."** The company, while complying for the sake of compliance and stating that it is working to restore access, criticized the *manner* of the control itself: (a) "we disagree that the finding of a narrow potential jailbreak should be cause for recalling a commercial model"; (b) "if this standard was applied across the industry, we believe it would essentially halt all new model deployments"; (c) the measure does not adhere to the principles of transparency, fairness, clarity, and technical grounding.

> **Reservations on verification (in both directions):**
> (i) The suspension announcement itself has been checked above. But whether "Claude Mythos Preview" — which §4 of this work discusses as a collapse case (Appendix F-6: the System Card [244 pp.], risk report, and cybersecurity write-up of April 7, 2026) — and the suspended product "Mythos 5" are **of the same lineage** has been checked, with this result: there is **circumstantial evidence beyond mere name coincidence** — (1) both belong to Anthropic's "Mythos" series (the announcement footer lists Mythos as a product line), and (2) both center on **the same distinctive capability**: the "autonomous discovery of zero-day vulnerabilities and exploit development" recorded in the April Mythos Preview cybersecurity write-up is of the same kind as the trigger of the June Mythos 5 suspension (the vulnerability capability of "reading a codebase and fixing flaws"). However, the June suspension announcement does **not** explicitly link Preview or any version lineage (the footer's product names carry no version labels), and the April Preview documents predate Mythos 5. That is, **no single primary source explicitly confirms the identity-of-lineage claim that "Mythos 5 is the productized version of Claude Mythos Preview."** This supplement therefore **records the strong circumstantial connection while not claiming a confirmed identity** (describable, not evidence).
> (ii) At the same time, Anthropic's own characterizations ("narrow jailbreak," "industry-common," "recall is unwarranted") are **an unverified claim by one of the parties**. The substance of the specific concern on which the government acted is disclosed neither in the announcement nor in this supplement. Because this work takes a position critical of military AI, to adopt the developer's self-assessment uncritically would damage the fairness of that critique. **This supplement takes neither party's assessment as its own.**

### 5-2. Grounding in the argument (blocking over-reading in both directions)

- **Certain as observation:** a precedent has actually arisen in which national-security-grounded export control cut off access to a frontier commercial model.
- **The contribution to the argument remains a sign / an interpretation:** the trigger of the suspension was a **capability** (a dual-use cyber capability), not **the collapse of the internal–external divergence itself** that §4 of this work discusses. One must not read "suspension = a demonstration of collapse" (the same two-layer discipline as the author's note on citing the Mythos case).

### 5-3. Where it grounds in v2 (naming the distance honestly)

The legal structure of this precedent is, as above, **export control (a restriction on foreign nationals' access)**, and the full-customer suspension is **the net effect** of the impossibility of technically separating it. This is **not a "capability gate"** of the form "the capability crossed a threshold, so the product is disabled wholesale." Yet it is not unrelated: the trigger was a dual-use cyber capability, and it was *because of* that capability that it became a target of export control.

This precedent can therefore be read as a **structural analogy (not a strict mathematical isomorphism)** to v2 §3-3b (the rendering-invisible of divergence through capability improvement — the capability/control trade-off). §3-3b concerns concealment driven by optimization pressure *internal to the system*; what could arise in this precedent is a structure in the *motivation of an actor* (a developer): a developer who learns that a model with dual-use capability can become a target of control **may** thereby acquire an incentive to conceal capability. The driving mechanisms differ. Furthermore, this precedent is **a single case ($n=1$)**, and to assert a "structure" from it is an over-generalization. This supplement therefore records not "a structure has appeared, isomorphically" but "**a single case suggesting a structural analogy has appeared.**" The reading of "an incentive to conceal" as a recursive instability is **one interpretation**, not something derived directly from the legal structure (export control) of this precedent.

Note that this precedent has nothing to do with the *magnitude* of pressure ($P_{\mathrm{civil}} \ll P_{\mathrm{military}}$, which v2 has already retracted); the specificity of the military lies in v2 §3-2c (the "structure of contradiction") — and this supplement does not overwrite that.

---

## 6. A refinement of $\kappa$ (confined to the prescription layer — not a premise of the principal pillars)

The following is an auxiliary refinement of v2's **prescription (Chapter 11)**, **not a premise of the principal pillars**. So as not to dilute the simplicity of the single scalar $\kappa$ (Appendix E-1), it is all recorded as an addendum to the prescription layer.

1. **The watershed is not "whether there is a shutdown" but "the manner of the shutdown."** This precedent cannot be characterized by a single $\kappa$: the directive on the side **imposing** the control (the state) is **close to $\kappa = 0$** (unilateral; lacking a transparent legal process), while the response on the side **receiving** the control (the developer) is **$\kappa > 0$-like** (a public technical objection; an effort to restore access). That is, the party shut out criticizes the $\kappa = 0$ manner of the control (the deficiency of transparency, technical grounding, and legal process) and demands its correction toward a $\kappa > 0$ form. That the same shutdown can carry different $\kappa$ depending on the actor in fact **strengthens** the point that "the manner of the shutdown — $\kappa = 0$ or $\kappa > 0$ — is the watershed."
   > *Note: transferring $\kappa$ here to "the manner of a shutdown" is an **analogy**; its referent **differs** from the $\kappa$ of the main text's E-1 (the degree to which intrinsic directional alignment, IDA, is built into the foundation of alignment). The two are not to be treated as the same scalar (this does not alter the $\kappa$ of the main text's §1-4a / E-1).*
2. **What is to be monitored is not "the AI's hostility" but "the decline of $\kappa$ itself"** — i.e., the divergence between capability-based state control and the developer's assessment. Against v2 §11-2a's three proxies (all oriented to "looking into the AI"), this is worth considering, at the prescription layer, as an operational proxy that looks into the inter-layer relation (control ⇄ developer) (it adds only at the operational layer, without altering the definition of the single scalar $\kappa$ in E-1).
3. **A recursive instability (as one interpretation).** If a developer learns that a model with dual-use capability can become a target of control (one lacking a transparent legal process), the control itself may give the developer an incentive to conceal capability. This is, as stated in §5-3, **one interpretation** and not derived directly from the legal structure of this precedent; but were it to operate, it would produce — in the human / lab layer — an instability **structurally analogous** to §3-3b, in which the assessment on which the control relies degrades and the divergence widens. That it requires no hostility on the AI's part is the important point.

---

## 7. What must not be done (self-discipline)

1. Do not make the principal pillars depend on $\beta$ or on the claim of "undecidability in principle." Do not elevate the (B) result — indeterminacy — into a ground for the principal pillars.
2. Do not elevate (B) into any of "a structural insufficiency of the signal-to-noise ratio," "a refutation/proof of undecidability in principle," or "support for $\beta > 1$." **Leave it undecided.**
3. Do not extend the precedent into a prophecy that "the AI turns adversarial." Do not touch the body of v2 §6-3c (the self-destruction scenario); if it is treated, confine it to a footnote as a conditional warning (it depends on a conjunction of many premises; what is monitored is the decline of $\kappa$; a single-shot model without persistent memory does not satisfy the premises). Always state alongside: the mixed $\kappa$, the industry-commonality of the capability, and the non-effect on other models.
4. **Do not re-introduce the magnitude of pressure** ($P_{\mathrm{civil}} \ll P_{\mathrm{military}}$; retracted in v2; military specificity is in §3-2c, the "structure of contradiction").
5. Do not write the unverified as confirmed (especially the identity-of-lineage of Mythos [there is a strong circumstantial connection but no explicit confirmation], the substance of the government's concern, and the developer's self-assessment).
6. Do not over-claim the AI's intentions, fears, or hostility as actual mental states. Maintain the academic register of the main text.

---

## 8. Cross-reference table (this supplement → the relevant sections of v2)

| This supplement | The section of v2 it grounds in | Relation |
|---|---|---|
| §2 indeterminacy | §4-4c (the central argument is $\beta$-independent); Appendix I (the home of the subordinate pillar) | consistent with the $\beta$-independence declaration (not a strengthening) |
| §3 the transfer of the Gap | Appendix E-2; §6-1c (the Indistinguishability Gap) | an empirical observation consistent with the proposition (neither proving nor strengthening it; not theorized) |
| §4 the measurement discipline | §1-3b (Welcoming refutation); "A caution in reading this paper" | a practical underpinning of epistemic honesty |
| §5 the precedent | §3-3b (the capability/control trade-off); §3-2c (the structure of contradiction); the author's note on citing the Mythos case (the two-layer discipline); Appendix F-6 (bibliography) | a single case suggesting a **structural analogy** for the capability/control trade-off (not an isomorphism) |
| §6 the refinement of $\kappa$ | Chapter 11 (the prescription); §11-2a (the proxies); Appendix E-1 (the definition of $\kappa$) | an auxiliary refinement of the prescription layer (not a premise of the principal pillars; does not alter E-1) |

---

*This supplement records two subsequent events in a subordinate position, on the premise that the principal pillars of the main text (Version B, revised) stand independently of the value of $\beta$. The principal pillars of this work do not depend on the success or failure of this supplement. The state of primary-source verification is made explicit in each section (the suspension announcement = checked; the lineage of Mythos = checked, with no explicit confirmation of identity [there is a strong circumstantial connection of the same series and the same distinctive capability — §5-1]; the substance of the government's concern = not disclosed in the announcement, hence unverified).*
