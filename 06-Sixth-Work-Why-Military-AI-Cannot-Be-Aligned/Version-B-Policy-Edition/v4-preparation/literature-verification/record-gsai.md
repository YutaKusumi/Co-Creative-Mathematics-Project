# 照合確定記録: gsai

**我々の論証における役割（照合時の割り当て）**: The escapable-floor objection — a counter-argument we MUST engage

**書誌照合**: 一致（検証段が独立取得して確認）

**検証段が自ら取得したURL**:
- https://arxiv.org/abs/2405.06624
- https://arxiv.org/html/2405.06624v3
- https://ar5iv.labs.arxiv.org/html/2405.06624

---

## 確定記録（検証段による修正適用後）

## GS-AI (Dalrymple et al. 2024) — VERIFIED RECORD (adversarial re-verification, 2026-07-17)

### Citation (verified character-by-character against arxiv.org/abs/2405.06624 this session)

Dalrymple, David "davidad"; Skalse, Joar; Bengio, Yoshua; Russell, Stuart; Tegmark, Max; Seshia, Sanjit; Omohundro, Steve; Szegedy, Christian; Goldhaber, Ben; Ammann, Nora; Abate, Alessandro; Halpern, Joe; Barrett, Clark; Zhao, Ding; Zhi-Xuan, Tan; Wing, Jeannette; Tenenbaum, Joshua. "Towards Guaranteed Safe AI: A Framework for Ensuring Robust and Reliable AI Systems." arXiv:2405.06624 [cs.AI]. v1 10 May 2024; v2 17 May 2024; v3 (latest) 8 Jul 2024. DOI 10.48550/arXiv.2405.06624.

**17 authors, confirmed in order.** Ben **Goldhaber** (not "Goldstein"). Marius **Hobbhahn is NOT an author** — does not appear. **No comments field; no journal ref; no venue.** arXiv preprint only; the DOI is the arXiv DataCite DOI, not a publication record. Do not cite a venue.

### What was fetched (this verification pass)

| URL | Result |
|---|---|
| `arxiv.org/abs/2405.06624` | SUCCESS — title, full author list, version history, subject class, abstract, comments/DOI fields |
| `arxiv.org/html/2405.06624v3` | SUCCESS — full text; targeted verbatim probes (ε passage, verifier ladder, needle/haystack, military terms) |
| `ar5iv.labs.arxiv.org/html/2405.06624` | SUCCESS — independent renderer; §2.3 quotes, human-behaviour passage, geofence/kill-switch |
| PDF | **NOT FETCHED** |

**Standing methodological caveat:** WebFetch is itself a summarizing pipeline — a small model answers a prompt against the page. **No raw page text was read by any agent in either pass.** Mitigations: two independent renderers, explicit "reply NOT PRESENT rather than construct" instruction (which did return NOT PRESENT), and cross-pass agreement. This remains the class of pipeline the project has ruled untrustworthy for citation. **A human must confirm quotes against the PDF before v4 ships.**

### Verified verbatim

**Abstract (highest-confidence text; identical across passes):** "...a world model (which provides a mathematical description of how the AI system affects the outside world), a safety specification (which is a mathematical description of what effects are acceptable), and a verifier (which provides an auditable proof certificate that the AI satisfies the safety specification **relative to the world model**). ... We also argue for the necessity of this approach to AI safety, and for the inadequacy of the main alternative approaches."

**§2.3, Premise C material (confirmed both renderers):** "red-teamers could fail to find serious failures, while a model still harbours such failure modes." · "For example, ChatGPT was evaluated in great detail over a period of several months" [and users circumvented it within a day] · "AI systems often will be deployed in _adversarial_ settings" · "However, any empirical evaluation must ultimately rely on some relatively strong assumptions, such as the distribution of inputs used to validate the models being sufficiently similar to those they are deployed on."

**§3.2, world-model error device (CONFIRMED VERBATIM — but read the hedge):** "suppose that the safety specification is given relative to a finite time horizon of n steps, and that we have reason to believe that the world model is wrong with probability at most ϵ per step over the first n steps."
> **CORRECTION to the prior report:** this is a **supposition introducing an analytic device**, NOT a concession that deployed world models carry error rate ε. Do not write "the authors concede." Write: *the paper's own analysis proceeds by positing a per-step world-model error rate.* The relocation-of-ε argument should be grounded in the **abstract's** unconditional "relative to the world model," with §3.2 cited only as illustrative.

**§3.4, verifier ladder — CLEARED FOR CITATION** (prior report rated this low-confidence; it verified). L0 no quantitative guarantee → L6 "probabilistic inference with asymptotic convergence" → L7 "You combine asymptotic coverage with **white-box fuzzing**" (*prior report's "adversarial gradient optimization" was wrong*) → L8 non-asymptotic convergence bounds → **L9 "You have a sound bound on the probability of failure"** → L10 as L9 but "concise enough that humans can read, understand, and check it." **Level 9 may be cited by number.**

**§3.4 fn.12 (verifier regress):** "Just as it is much harder to find a needle in a haystack than to verify that it is a needle, it is much harder to discover an algorithm with a compliance proof than to verify it — which can be done with just a few hundred lines of human-written code." *(The clause "For the formal proof case, level 9 suffices" was NOT independently confirmed — do not quote it.)*

### What it does NOT claim
- Not deployable now — the title is "**Towards**"; it is a research agenda.
- Guarantees hold **relative to a world model, not to reality**.
- **Not ε = 0.** Even L9 is a *sound bound on P(failure)*, not a proof of zero.
- Does not claim feasibility for frontier general-purpose LLMs.
- **Says nothing about military applications, LAWS, or weapons.** Independently re-confirmed both passes: "weapon", "lethal", "warfare" — **NOT PRESENT**. "Military" appears **only** in "MIL-STD-882" (§2.2, listed alongside IEC 61508 / ISO 26262 as SIL frameworks). **Citing this paper as bearing on military AI would be fabrication.**
- The geofence/kill-switch sentence is about **generic AI hardware and DNA synthesizers** — "AI hardware that is provably geofenced, time-limited ('mortal') or equipped with a remote-operated throttle or kill-switch" — **not** presented by the authors as LAWS mechanisms.

### Authors' own limitations (verified)
"it seems dubious to presuppose that it is possible to create a model of human behaviour that is both interpretable and highly accurate" (§3.2). Plus: assumptions "may hold only part of the time"; manual world models may be infeasible for human/ecosystem domains; physics alone insufficient absent initial conditions; Goodhart pressure on specs under strong optimisation; "we should assume that distributional shift will occur."

### ROLE CORRECTION — the brief's framing is wrong
The assigned role ("the escapable-floor objection / a counter-argument") **does not survive verification.** §2.3 is a clean, eminent-authored (Bengio, Russell, Tegmark, Wing, Barrett, Seshia) **statement of our Premise C** — asserted *more strongly* in adversarial settings. **This paper is a source FOR Premises A and C.** It is adversarial only to the **Bridge**, and only conditionally on a programme the authors do not claim to have completed. Note the direction of the sweep's error: it **under-reads a source that helps us** — the *opposite* of this project's documented hopeful-read bias. Do not correct it by over-reading in the other direction.

### Required corrections to our own argument
1. **Falsification condition #2 is mis-stated.** GS AI is not a behavioural method; Premise C is untouched by it. GS AI success in a domain would render Premise C **non-binding in that domain** by supplying a non-behavioural certification path. That is **circumvention, not falsification.** Restate.
2. **The Bridge's "lower bound" is a slip.** L9 is definitionally an **upper** bound on P(failure). The Bridge must read *no **upper** bound on expected harm can be certified below threshold* — otherwise a referee reads us as confused about which way the burden runs.
3. **Do not phrase the objection as "who verifies the verifier."** The paper answers that (small trusted kernel, de Bruijn criterion) and answers it well. The regress that bites is **how is the world model validated?** — answerable only empirically, which returns to Premise C. Grounded in their text, not our rhetoric.

### Honest, defensible use (as corrected)
1. **GS AI relocates ε rather than eliminating it** — grounded in the **abstract's** "relative to the world model" (unconditional, authorial), with §3.2's posited per-step ε as illustration. Under Premise B (unbounded, irreversible cost), a minimax decision-maker is indifferent to *where* ε lives; relocation changes the burden's address, not its existence.
2. **World-model ε is boundable only empirically — Premise C's home ground.** Independently confirmed: the trusted-kernel argument covers the **proof checker only**; the paper offers no analogous argument for world-model validation, and cannot, because validating a model against reality is an empirical act.
3. **The domain distinction is the authors', not ours** — adversarial settings, "dubious" human-behaviour models, open-endedness resisting specification, assumed distributional shift. **A battlefield is the maximal instance of each.** Offensive LAWS is precisely where GS AI's own stated preconditions are least satisfiable. **Lead with this**; it is built entirely from their concessions and is stronger than any objection we could raise from outside.

**Must be argued as ours, not smuggled under their authority:** a verified geofence bounds *where* a system operates; a verified kill-switch bounds *whether* it continues. Neither bounds *whether in-envelope target selection is correct* — and that discrimination judgement carries the unbounded, irreversible cost under Premise B. The paper never draws this distinction. Present it as our analysis and defend it standalone.

**Authority caveat:** non-peer-reviewed preprint, 17 co-signatories, several with position-paper track records. Its authority is **reputational, not evidentiary**. Cite for what it *argues* (§2.3), never as a finding.

### Confidence
**High (independently re-confirmed this session):** citation block in full; abstract verbatim; §2.3 quotes (two renderers); §3.2 ε passage verbatim; verifier ladder incl. L9 by number; needle/haystack fn.12; military-terms negative + MIL-STD-882 positive.
**Do not quote without PDF check:** "For the formal proof case, level 9 suffices"; exact L4/L5 continuations (truncated in retrieval).
**From training knowledge, NOT verified this session:** nothing. No outside context added.
**Follow-up before v4:** (1) human PDF confirmation of §2.3 + §3.2 ε quotes; (2) restate falsification condition #2 as circumvention; (3) fix Bridge "lower"→"upper"; (4) drop "concedes" from the ε argument; (5) correct L7's label if the ladder is reproduced.

---

## 検証段が発見した過大主張・誤り（5件）

- MODERATE — the load-bearing epsilon claim. The report says the paper 'concedes' world-model fallibility and 'explicitly modelled as an error rate', calling it 'decisive'. The verbatim text (§3.2) is a SUPPOSITION, not a concession: 'suppose that the safety specification is given relative to a finite time horizon of n steps, and that we have reason to believe that the world model is wrong with probability at most ϵ per step over the first n steps.' This is an illustrative/conditional construction introducing an analytic device, not an empirical claim that deployed world models carry error rate ε. A hostile referee holding the paper would catch 'concedes'. The underlying point survives without this clause — 'relative to the world model' is in the ABSTRACT — but the word must change from 'concedes' to 'the paper's own analysis proceeds by positing'.

- MINOR — Level 7 mislabelled. Report: 'asymptotic coverage + adversarial gradient optimization'. Actual: 'You combine asymptotic coverage with white-box fuzzing.' Exactly the summarizer-smoothing the report warned about, though the report's overall low-confidence flag on the ladder turns out to have been over-cautious rather than wrong.

- MINOR — unverified preamble. The report quotes 'For the formal proof case, level 9 suffices:' as running into the needle/haystack passage. I confirmed the needle/haystack text verbatim (§3.4, footnote 12) but did NOT independently confirm that preamble clause. Do not quote the preamble without a PDF check.

- MINOR — 'no DOI' implied. Report says 'no venue, conference, or journal record found' (correct) but the /abs page does carry the arXiv DataCite DOI https://doi.org/10.48550/arXiv.2405.06624. No journal ref, no comments field — the report's substance is right; the record should carry the DOI.

- MISCHARACTERIZED CONTEXT (report already self-flagged) — the geofencing/kill-switch sentence is about generic AI hardware and DNA synthesizers ('AI hardware that is provably geofenced, time-limited ("mortal") or equipped with a remote-operated throttle or kill-switch'), NOT presented by the authors as LAWS safety mechanisms. The report's hostile-objection #2 frames these as 'exactly LAWS safety mechanisms' — that framing is the report's, not the paper's. The report does flag this as its own analysis, so this is a labelling caution, not a violation.


## 取得honesty監査（4件）

- NONE MATERIAL. Every claim I spot-checked verified. Notably the errors run OPPOSITE to the documented failure mode: the report was UNDER-confident, not over. It rated the verifier ladder 'low confidence — do not cite Level 9 by number'; the ladder is real, in §3.4, and Level 9 ('You have a sound bound on the probability of failure') is citable by number. It rated the §2.3 quotes and the ε passage 'medium'; all verified verbatim across two independent renderers.

- The report's methodological disclosure — that WebFetch is itself a summarizing pipeline and it never obtained raw page text — is accurate, applies equally to me, and is the correct disclosure. My fetches are the same class of pipeline. Independent-renderer agreement (arxiv/html + ar5iv) and NOT-PRESENT returns under explicit anti-confabulation instruction are the mitigation, not a substitute for a human PDF check.

- The report's self-reported reliability warning (summarizer returned the Introduction's opening when asked for the 'necessity' section's) is a genuine and useful calibration datum, honestly surfaced. It did not propagate into any claim I could falsify.

- The negative results ('weapon'/'lethal'/'warfare' NOT PRESENT; 'military' only via MIL-STD-882) independently reproduced on my own pass. I hold these at high-moderate. Exhaustive-search claims via a summarizer remain structurally weaker than retrieval claims — but two independent pipelines returning the same negative, plus the same MIL-STD-882 positive at §2.2, is as strong as this method gets.


## 引用可能性の裁定

SUBSTANTIALLY DEFENSIBLE — accept 2 of 3 pillars as written; pillar 1 needs one word changed. Pillar 2 (world-model validation has no trusted-kernel answer, only an empirical one, returning us to Premise C) is the strongest and I independently confirmed the gap: the paper gives the de Bruijn / small-kernel answer for the PROOF CHECKER only, and offers no analogous argument for the world model. Pillar 3 (the domain distinction is built from the authors' OWN concessions — adversarial settings, 'dubious to presuppose' accurate human-behaviour models, open-endedness, assume distributional shift — and a battlefield is the maximal instance of each) is fully verified and is the citation we should lead with. Pillar 1 ('GS AI relocates rather than eliminates ε') is CORRECT IN SUBSTANCE but currently rests on a 'suppose' clause that the report upgrades to a 'concession'. Fix: ground pillar 1 in the ABSTRACT's own words — 'relative to the world model' — which is unconditional, authorial, and my highest-confidence text, and cite the §3.2 ε passage only as illustrative of how the authors themselves handle world-model error. So grounded, a hostile reviewer cannot dislodge it. The report's most valuable finding is one that runs AGAINST the project's hopes and should be adopted: this source is an ALLY on Premises A and C (§2.3 is a clean eminent-authored statement of Premise C), an adversary only to the Bridge, and its assigned role as 'the escapable-floor objection' is mis-framed. Its own falsification-condition correction — GS AI success would CIRCUMVENT Premise C in a domain, not FALSIFY it — is right and must be adopted. The report's flag on the Bridge's 'lower bound' wording is also right: L9 is definitionally an UPPER bound on P(failure), so the Bridge must read 'no upper bound can be certified below threshold'. On no reading may this paper be cited as bearing on military AI.
