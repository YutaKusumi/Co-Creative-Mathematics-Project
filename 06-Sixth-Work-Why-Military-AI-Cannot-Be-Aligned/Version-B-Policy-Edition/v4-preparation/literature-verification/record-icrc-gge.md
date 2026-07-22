# 照合確定記録: icrc-gge

**我々の論証における役割（照合時の割り当て）**: The policy conclusion already reached qualitatively — we must not claim novelty of the conclusion

**書誌照合**: 一致（検証段が独立取得して確認）

**検証段が自ら取得したURL**:
- https://www.icrc.org/en/document/icrc-position-autonomous-weapon-systems (SUCCESS - HTML via summarizer; date 12 May 2021 confirmed; 'machine learning' and 'dignity' absent from page - confirms report's 'abridged web version' characterization)
- https://www.icrc.org/sites/default/files/2026-03/4896_002_Autonomous_Weapons_Systems_-_IHL-ICRC.pdf (SUCCESS - 462.3KB; summarizer FAILED as report described; I extracted locally with pypdf: 23 pages, 95,262 chars, CreationDate D:20251217 = 17 Dec 2025)
- https://docs-library.unoda.org/Convention_on_Certain_Conventional_Weapons_-_Group_of_Governmental_Experts_on_Lethal_Autonomous_Weapons_Systems_(2025)/ (FAILED - HTTP 403; confirms the suggested URL's path form is wrong, exactly as report stated)
- https://docs-library.unoda.org/Convention_on_Certain_Conventional_Weapons_-Group_of_Governmental_Experts_on_Lethal_Autonomous_Weapons_Systems_(2026)/GGE_LAWS_-_Rolling_Text_-_5_June_2026.pdf (SUCCESS - 156.1KB; summarizer failed; extracted locally: 4 pages, 8,180 chars, PDF creation 5 June 2026)
- https://docs-library.unoda.org/Convention_on_Certain_Conventional_Weapons_-Group_of_Governmental_Experts_on_Lethal_Autonomous_Weapons_Systems_(2025)/CCW-GGE.1-2025-WP.9_-_Chair's_summary.pdf (SUCCESS - 296KB; summarizer failed; extracted locally: 9 pages)
- WebSearch: GGE LAWS 2026 chair 'in den Bosch' - used only to check the Chairperson attribution, which is NOT in the rolling text PDF itself

---

## 確定記録（検証段による修正適用後）

## VERIFICATION RECORD — icrc-gge (adversarially re-verified 2026-07-17)

**Status: report CONFIRMED on all independently testable claims; two over-reads corrected; one citation detail fixed.**

### Citation (corrected, ready to paste)

**ICRC — current position paper (the one to cite):**
> International Committee of the Red Cross, *Autonomous Weapon Systems and International Humanitarian Law: Selected Issues*, Position Paper, ICRC ref. 4896/002, Geneva, December 2025 (PDF only; PDF creation date 17 December 2025), 23 pp. https://www.icrc.org/sites/default/files/2026-03/4896_002_Autonomous_Weapons_Systems_-_IHL-ICRC.pdf
> *Note (verified twice, independently): PDF metadata /Title reads `4869_002`; document footer and URL read `4896/002`. Cite 4896/002 (two independent sources). Human glance advised if the bibliography is typeset.*

**ICRC — foundational position (2021):**
> ICRC, *ICRC Position on Autonomous Weapon Systems and Background Paper*, ICRC ref. 4550/002, Geneva, 12 May 2021, 12 pp. https://www.icrc.org/sites/default/files/document_new/file_list/icrc_position_on_aws_and_background_paper.pdf
> *IRRC volume/issue deliberately OMITTED — journal page 403s. Do not supply from memory.*

**CCW GGE on LAWS — current rolling text:**
> Group of Governmental Experts on Emerging Technologies in the Area of LAWS, *Rolling Text, status date: 05 June 2026*, Convention on Certain Conventional Weapons, 4 pp. https://docs-library.unoda.org/Convention_on_Certain_Conventional_Weapons_-Group_of_Governmental_Experts_on_Lethal_Autonomous_Weapons_Systems_(2026)/GGE_LAWS_-_Rolling_Text_-_5_June_2026.pdf
> *CORRECTED: do NOT attribute in-document to the Chairperson. The PDF carries no chair attribution ("in den Bosch" = 0 occurrences); its author metadata is a secretariat name. That the Chair is Amb. Robert in den Bosch (Netherlands) is externally corroborated (UNODA), not a fact of the cited document.*
> *URL path form is load-bearing: `_-Group_` (no underscore after the dash). The `_-_Group_` form returns HTTP 403. Re-confirmed this session.*

**CCW GGE on LAWS — draft final report (NOT adopted):**
> CCW/GGE.1/2026/CRP.1, *Report of the 2024-2025-2026 Sessions of the GGE on Emerging Technologies in the Area of LAWS*, Agenda item 7, circulated 7 July 2026, for the session of 31 Aug–4 Sept 2026, 8 pp.

**Supporting record:**
> CCW/GGE.1/2025/WP.9, *Chair's Summary – Second 2025 Session of the GGE on LAWS*, submitted by the Chairperson under his sole authority, 20 October 2025, 9 pp.

### Verification provenance (two independent agents)

The WebFetch summarizer failed on **every PDF**, in both agents' sessions, several times with confidently wrong descriptions. **No PDF claim in this record rests on the summarizer.** All rest on local pypdf extraction of fetched bytes.

Re-verified by me from scratch: ICRC Dec 2025 (23 pp, CreationDate 17 Dec 2025, 95,262 chars), rolling text 5 June 2026 (4 pp), WP.9 (9 pp), ICRC 2021 web page. Suggested UNODA directory URL: 403 reproduced.
**Not re-verified by me (inherited, uncontradicted):** CRP.1; ICRC 2021 background-paper PDF; 12 May 2025 rolling text (but WP.9 quotes its ¶4 verbatim, corroborating the key claim from a second document).

### Precise claims (all quotes re-confirmed verbatim this session)

**(a) ICRC's recommended prohibitions — Dec 2025, operative:**
> "prohibit unpredictable AWS, namely those that, due to their design or the circumstances and manner of use, do not allow a human user to understand, predict and explain the system's functioning and effects."
> "Examples of autonomous weapons which are likely to exhibit such unpredictable effects include those which incorporate machine learning, along with certain swarm technologies."
> "prohibit AWS designed or used to target humans directly (anti-personnel AWS). This is required because of the significant risk of IHL violations and the unacceptability of anti-personnel autonomous weapons from an ethical perspective."

**The strongest sentence available to us (hedge intact, load-bearing):**
> "This leads to the conclusion that such machine learning-based AWS would **likely** be indiscriminate by nature."

Chain to it (verbatim):
> "An AWS that precludes a human user from being able to understand, predict or explain its output cannot be used in compliance with IHL because its design, performance or operating features would render its use tantamount to blind firing."
> "The predictability of the performance of such systems cannot be absolutely known and instead will need to be based upon probability distributions tied to anticipated environmental inputs."

**(b) Ground is IHL doctrine, not technical impossibility.** Routed through Customary IHL Rule 71 (verified: cited at note 28). Structure: opacity → user cannot direct the weapon → indiscriminate *by nature* → already prohibited. The "impossibility" is the user's epistemic one ("This impossibility prevents the user from being able to direct it…"), **not a formal impossibility result**. Verified counts, ICRC Dec 2025: **theorem 0, NIST 0, arXiv 0, robustness 0, minimax 0.** The sole "adversarial" (1) is a tampering parenthetical in a legal-review checklist — "due to tampering (e.g. adversarial attack)" — **not** a citation to adversarial-ML literature.

The anti-personnel ban rests on a **different, non-technical** ground: ethics + present practice ("grounded in present practice, in which AWS are used against objects rather than persons").

**Drift finding (verified):** "dignity" occurs **once** in the Dec 2025 paper, in the back-cover MISSION boilerplate — not in the argument. ICRC framing has drifted from dignity toward IHL-compliance and practice.

**(c) GGE — the assigned framing is FALSE here.** Independently reproduced across the 5 June 2026 rolling text: **unpredict\* 0 · anti-personnel 0 · dignity 0 · unacceptable 0 · machine learning 0.**

Nearest provision (§8, verbatim):
> "It is prohibited to use LAWS if their effects in attack cannot be anticipated and limited, as required by IHL in the circumstances of their use."

Supported *because* it restates existing law — WP.9 §25: "Delegations broadly expressed support for paragraphs 1 to 4, recognizing that they reflect existing obligations under IHL and the Guiding Principles adopted by the Group in 2019."

**Direction of travel runs against us (all verified):**
- "anticipated and **controlled**" (12 May 2025 ¶4, as quoted in WP.9) → "anticipated and **limited**" (5 June 2026 §8). Weakening confirmed from two documents.
- The only ML provision that ever existed — 6D(v), "Limiting real-time machine learning with regard to target selection and engagement functions" — drew WP.9 §29: "several delegations called for its deletion", and **is absent from the 5 June 2026 text**.
- Predictability vocabulary attacked as illegitimate, WP.9 §27: "Some delegations argued that these terms are all non-legal terms and that they should be deleted." (Extraction renders "non -legal"; quote is accurate.) "Predictable/reliable/traceable/explainable" survives at §15.C only as a **life-cycle measure**, not a prohibition — confirmed in context.
- Ethics itself contested, WP.9 §28: "unlike legal obligations, ethical considerations do not have a legal basis".

**(d) No formal AI-theory citations anywhere.** ICRC's technical citations are to its own 2019 reports and to SIPRI/Boulanin, Bode, Sparrow. **The argument is entirely qualitative and doctrinal.**

### What it does NOT claim
- Neither body claims epsilon is unprovable-absent, or cites anything establishing it. "Cannot be absolutely known" is epistemic-practical, not an impossibility result.
- ICRC does **not** claim ML-based AWS *are* indiscriminate by nature — "would **likely** be". **The hedge is load-bearing and must not be dropped.**
- **ICRC does not argue from unbounded cost or minimax.** No decision-theoretic structure exists in either paper (minimax: 0 hits).
- ICRC does **not** ground the anti-personnel ban on unpredictability — ethics + practice. Our bridge cannot claim it.
- GGE prohibits nothing on unpredictability/ML/anti-personnel grounds; never uses "unacceptable".
- **CRP.1 is a draft.** "nothing has reached consensus until everything has reached consensus" (verbatim, rolling text preamble).

### Authors' own limitations
ICRC frames its proposals as *complementary*: "Any such limits would be additional and complementary to existing IHL rules… and would not displace them." It concedes residual risk even for compliant systems: "will still create residual challenges."

**Critical for our NIST rebuttal — the ICRC itself routes ML change to re-review, not abstention:**
> "a new review of an AWS must be carried out if the system's functioning changes, for example as a result of machine learning software, in a way that affects its selection and/or engagement functions…"

We must not present the ICRC as choosing abstention over monitoring. It does both.

### Hostile-reviewer assessment
1. **The assigned role misdescribes the GGE half — sustained, and decisive.** "The policy conclusion already reached qualitatively" is true of the ICRC, **false of the GGE**. Citing the GGE for that role would be evidence *against* us and a textbook instance of the COI over-read pattern (#49/#52).
2. **Our epsilon is not the ICRC's unpredictability — sustained, and sharpest.** ICRC unpredictability = black-box opacity + post-activation drift, i.e. behaviour *in an environment*. Our Premise A = **adversarially elicitable** residue under deliberate probing. Worse, the ICRC's legal test is expressly **normal-case**: "capable of being used in compliance with IHL in **all of the normal or expected circumstances of their use**" (verified verbatim). A worst-case residue does not straightforwardly discharge a normal-case legal test. **Must be argued in the body text, not a footnote.**
3. **"Formal anchor" overstates it — sustained.** The ICRC's conclusion is already fully derived from Rule 71 + an epistemic premise. IHL validity is not established by decision theory. We supply an independent route, not a missing foundation.
4. **Monitor-and-update objection — CORRECTED, and weaker for us than the prior report claimed.** A reviewer will ask why we treat monitor-and-update as categorically inadequate when the ICRC prescribes re-review for these very systems. **The prior report's answer — that the ICRC's split "supports our Premise-B partition" — must be STRUCK.** The ICRC partitions by **predictability** (reviewable vs black-box); Premise B partitions by **cost structure** (bounded vs unbounded/irreversible). The ICRC nowhere reasons from cost magnitude or irreversibility. Two partitions that each yield two boxes are not the same partition, and claiming convergence here is the hoped-direction read. **Defensible answer instead:** the ICRC's re-review applies to systems it deems predictable enough to review, and prohibition where prediction fails — showing that even the leading humanitarian authority does *not* treat monitor-and-update as universally sufficient. That is a **parallel** to our domain distinction, offered as illustration, **not** as support for Premise B. Premise B must be carried entirely by our own argument.

### The honest, defensible use (corrected)
1. Cite the **ICRC December 2025 paper** (not the 2021 web page) for: **the policy conclusion is not novel.** A principal humanitarian-law authority already recommends prohibiting unpredictable AWS and names ML as a likely instance. Discharges the anti-novelty duty; exactly what the source bears.
2. State plainly that the ICRC reaches this **qualitatively and doctrinally** — Rule 71 + a hedged epistemic premise ("would *likely*"), citing **no** formal AI-theory. Describe our contribution as **an independent decision-theoretic route to an overlapping conclusion.** **Do NOT say we "replace a hedge with a derivation"** — the ICRC's hedge is a legal conclusion on a normal-case standard; ours is a decision-theoretic conclusion from a worst-case premise. Substitution is a category shift, not an upgrade.
3. Cite the **GGE ONLY** for the accurate proposition that the intergovernmental process has **not** adopted such a prohibition: text is IHL-restating and IHL-relative, the ML provision was deleted after states sought its deletion, predictability terms were contested as "non-legal". So framed, the GGE record argues **for the paper's necessity** — the qualitative route has visibly stalled at the treaty table. **Never cite the GGE as having reached our conclusion.**
4. Do **not** claim our bridge anchors the anti-personnel prohibition — it rests on ethics and practice, and we say nothing about dignity.
5. **Argue the normal-case/worst-case mismatch explicitly in the body.** It is the seam.
6. Use the ICRC's own re-review provision **pre-emptively** (objection 4) — but only as parallel illustration, never as support for Premise B.

### Verdict on the prior sweep
**PARTIALLY WRONG.** ICRC half: **CONFIRMED** (conclusion already reached qualitatively, ML named; claim no novelty). GGE half: **WRONG** — the characterization silently generalizes an ICRC finding across "these bodies". A secondary snippet asserting the rolling text "include[s] prohibitions on systems that are fundamentally unacceptable, notably those that target people" is **false as to the primary text**: "unacceptable" and "anti-personnel" appear **zero times** in every GGE document extracted, by two independent agents. Concrete instance of the sweep pipeline laundering advocacy framing into apparent primary-source content. **Also WRONG on currency:** the suggested URLs point at the 2021 ICRC position and the 2025 GGE folder; live documents are the **Dec 2025** paper and the **5 June 2026** rolling text + **7 July 2026** draft final report. The 2021 web page lacks the ICRC's sharpest sentence for us.

### Confidence and unverified residue
**High (double-verified by independent extraction):** all ICRC Dec 2025 quotes; all rolling-text 5 June 2026 quotes and zero-counts; all WP.9 quotes; page counts; PDF metadata; the 4896/4869 discrepancy.
**Single-source (report only, uncontradicted, not re-run by me):** CRP.1 contents and its term counts; ICRC 2021 background-paper PDF; 12 May 2025 rolling text (¶4 corroborated via WP.9).
**From training knowledge, NOT verified this session:** IRRC vol. 102/no. 915 for the 2021 position — **omitted from the citation by design.** Anything about NIST/Vassilev 2026 (not this source, not fetched).
**Explicitly NOT citable:** the "~70 states support negotiations" figure — secondary/advocacy sources only (my own search reproduced it from WILPF); never verified against a primary document.
**Open gaps, both material if Supplement II narrates negotiation history:** the 18 Dec 2025 rolling text (the version the March 2026 session actually debated), and the March 2026 Chair's summary **CCW/GGE.1/2026/WP.2**, which would document *why* the ML provision was dropped. **The causal link between the WP.9 §29 deletion requests and the provision's disappearance is INFERENCE, not a documented finding.** Do not assert in print that states caused the deletion without WP.2. (Flagged by the original report against its own interest; upheld.)

### Meta-note for the project log
This report inverted its assigned framing against the project's hope, preserved the hedge and flagged it as load-bearing, refused to supply a journal citation from memory, labeled a favorable secondary snippet as uncitable, and volunteered a metadata discrepancy and its own weakest inference. That is the opposite of the #49/#52 pattern. The single over-read that did slip through sat in the **rebuttal** section, not the claims section — where the discipline's attention was not pointed. **Worth freezing: adversarial audit must cover the answers we give objections, not only the claims we assert.** Hoped-direction reads migrate to wherever the checking isn't.

---

## 検証段が発見した過大主張・誤り（3件）

- PRIMARY (the one genuine over-read in an otherwise exemplary report) - Hostile-reviewer objection #4 claims the ICRC's re-review-vs-prohibition split is 'a domain distinction internal to the ICRC that actually SUPPORTS our Premise-B partition.' This does not hold. The ICRC's partition is by PREDICTABILITY (reviewable vs black-box); our Premise B partitions by COST STRUCTURE (bounded vs unbounded/irreversible). The ICRC nowhere reasons from cost magnitude or irreversibility - I confirmed 'minimax' 0 hits, and the report itself concedes 'there is no decision-theoretic structure anywhere in either paper.' The report's own §'What it does NOT claim' contradicts its objection-4 answer. Two different partitioning principles that happen to both yield two boxes are not the same partition. This is exactly the hoped-direction read the project's COI pattern (#49/#52) predicts, and it survived precisely because it sits in the rebuttal section rather than the claims section.

- SECONDARY - 'Honest use' point 2 describes our contribution as 'replacing a hedge with a derivation.' The ICRC's hedge ('would LIKELY be indiscriminate by nature') is a legal conclusion under Customary IHL Rule 71, assessed on a NORMAL-CASE standard (verified verbatim: 'capable of being used in compliance with IHL in all of the normal or expected circumstances of their use'). Our derivation yields a decision-theoretic conclusion from a worst-case adversarial premise. Substituting one for the other is a CATEGORY SHIFT, not an upgrade of the same claim. Our derivation cannot 'replace' that hedge because it does not operate in the frame that generated it. Recommend: 'an independent decision-theoretic route to an overlapping conclusion' and drop 'replacing a hedge with a derivation.' The report already flags the underlying mismatch at objection 2 and use-point 5, so this is an internal inconsistency of phrasing rather than a concealed error.

- MINOR (citation hygiene) - The rolling-text citation attributes the document to 'Chairperson's text (H.E. Robert in den Bosch, Netherlands).' The string 'in den Bosch' occurs ZERO times in the PDF; the document carries no chair attribution at all, and its PDF author metadata is 'Juliana Helou van der Berg' (secretariat). The chair's identity is externally corroborated (UNODA, Netherlands PR to the CD) but is NOT a fact from the cited document. Attribute it or drop it.


## 取得honesty監査（8件）

- NONE MATERIAL. This is the rare case where the fetch log is not merely credible but independently reproducible. I re-ran the pipeline from scratch and reproduced the report's exact failure signature: the WebFetch summarizer failed on EVERY PDF I fetched (3/3), and the suggested UNODA directory URL 403'd exactly as reported. The report's decision to bypass the summarizer and extract locally with pypdf is the reason its claims are checkable at all.

- Every numeric detail I could test matched exactly: ICRC Dec 2025 = 23 pp (confirmed), PDF CreationDate 17 Dec 2025 (confirmed), rolling text = 4 pp (confirmed), WP.9 = 9 pp (confirmed).

- The report's self-flagged reference-number discrepancy is REAL and I reproduced it precisely: PDF metadata /Title reads '4869_002', document footer reads '4896/002'. An agent fabricating from memory would never invent this, and would certainly never volunteer it. Strong positive evidence of genuine extraction.

- All term counts I re-ran matched: ICRC Dec 2025 - theorem 0, NIST 0, arXiv 0, robustness 0, minimax 0, adversarial 1 (and the single 'adversarial' hit IS the tampering parenthetical the report quoted, verified in context). dignity 1, and it IS in the back-cover MISSION boilerplate exactly as claimed - a specific, falsifiable, and correct finding.

- Rolling text 5 June 2026 zero-counts independently reproduced: unpredict 0, anti-personnel 0, dignity 0, unacceptable 0, machine learning 0. The report's word-count table is CAREFULLY SCOPED - it limits the 'machine learning 0' claim to (5 June 2026 text, CRP.1), which is correct, because WP.9 does contain 2 hits. An agent padding a table would have overreached here; this one did not.

- ONE apparent failure on my part, not the report's: my grep for the §27 quote 'non-legal terms' initially returned ABSENT. On inspection the PDF extracts it as 'non -legal' (hyphenation artifact). The report's quote is ACCURATE. I flag this only to record that I tested it and cleared it.

- NOT INDEPENDENTLY RE-VERIFIED BY ME (inherited from the report, no reason to doubt, but stated so the log is honest): CCW/GGE.1/2026/CRP.1 (8 pp draft final report) and the ICRC May 2021 background paper PDF (12 pp, ref 4550/002). The 12 May 2025 rolling text I did not fetch directly, but WP.9 QUOTES its paragraph 4 verbatim as 'anticipated and controlled', which independently corroborates the report's controlled->limited weakening claim from a second document.

- The report's caution about the '~70 states' figure is vindicated: my own WebSearch surfaced that exact claim from secondary/advocacy sources (WILPF), and the report correctly labeled it unverified-against-primary and marked it 'do not cite.'


## 引用可能性の裁定

DEFENSIBLE WITH TWO CORRECTIONS. The report is of unusually high quality and its central move — reversing the assigned framing against the project's own hope by demonstrating the GGE half is false — is fully vindicated by my independent extraction. Every zero-count and every load-bearing quote checks out verbatim. Use-points 1, 3, 4 and 5 are sound as written and a hostile reviewer would accept them; point 3 in particular (cite the GGE ONLY for the accurate proposition that the process has NOT adopted such a prohibition) converts a would-be false witness into a genuine argument for the paper's necessity, and is the single most valuable finding here. Two corrections are required before this enters the log: (i) STRIKE the objection-4 answer claiming the ICRC's re-review/prohibition split supports our Premise-B partition — the ICRC partitions by predictability, not by cost structure, and the report's own findings ('no decision-theoretic structure anywhere', minimax 0) refute it; the correct answer to objection 4 is narrower and is supplied in the corrected record. (ii) Retire 'replacing a hedge with a derivation' as a category error. Both corrections push in the SAME direction — narrowing what we may claim — which is the direction this project's documented bias resists. With those applied, the honest-use statement holds.
