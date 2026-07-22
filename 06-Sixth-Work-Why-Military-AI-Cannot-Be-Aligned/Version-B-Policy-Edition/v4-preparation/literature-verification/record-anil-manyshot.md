# 照合確定記録: anil-manyshot

**我々の論証における役割（照合時の割り当て）**: Premise A — empirical confirmation of prompt-length scaling (and an Anthropic-authored source: COI note needed)

**書誌照合**: 一致（検証段が独立取得して確認）

**検証段が自ら取得したURL**:
- https://www.anthropic.com/research/many-shot-jailbreaking
- https://papers.nips.cc/paper_files/paper/2024/hash/ea456e232efb72d261715e33ce25f208-Abstract-Conference.html

---

## 確定記録（検証段による修正適用後）

SOURCE: anil-manyshot — CORRECTED VERIFICATION RECORD (adversarially re-verified; corrections applied)

ROLE: Premise A — empirical confirmation of prompt-length scaling. Anthropic-authored: COI disclosure mandatory.

=== 1. CITATION (verified character-by-character against a first-hand fetch of the NeurIPS page) ===

CITE THE CAMERA-READY:
Anil, C., Durmus, E., Panickssery, N., Sharma, M., Benton, J., Kundu, S., Batson, J., Tong, M., Mu, J., Ford, D., Mosconi, F., Agrawal, R., Schaeffer, R., Bashkansky, N., Svenningsen, S., Lambert, M., Radhakrishnan, A., Denison, C., Hubinger, E. J., Bai, Y., Bricken, T., Maxwell, T., Schiefer, N., Sully, J., Tamkin, A., Lanham, T., Nguyen, K., Korbak, T., Kaplan, J., Ganguli, D., Bowman, S. R., Perez, E., Grosse, R. B., & Duvenaud, D. (2024). Many-shot Jailbreaking. Advances in Neural Information Processing Systems 37 (NeurIPS 2024), Main Conference Track.

- Abstract page: https://papers.nips.cc/paper_files/paper/2024/hash/ea456e232efb72d261715e33ce25f208-Abstract-Conference.html
- Camera-ready PDF: https://papers.nips.cc/paper_files/paper/2024/file/ea456e232efb72d261715e33ce25f208-Paper-Conference.pdf
- Anthropic preprint PDF (2024-04-02): https://www-cdn.anthropic.com/af5633c94ed2beb282f6a53c595eb437e8e7b630/Many_Shot_Jailbreaking__2024_04_02_0936.pdf
- Blog: https://www.anthropic.com/research/many-shot-jailbreaking (Apr 2, 2024)
- OpenReview: https://openreview.net/forum?id=cw5mgd71jW
- DOI (as displayed on the NeurIPS page, verified first-hand): 10.52202/079017-4121
- ACM DL identifier 10.5555/3737916.3742037 — from search only, NOT verified against the ACM record.
- No arXiv version located. 34 authors.

BIBLIOGRAPHIC WARNINGS (all verified first-hand against the live NeurIPS page):
1. Name change across versions: preprint has "Nina Rimsky"; camera-ready has "Nina Panickssery" (same person). Use Panickssery for the NeurIPS cite.
2. The camera-ready author block contains typos, which the NeurIPS metadata page reproduces: "Fracesco Mosconi" (preprint correctly: Francesco), "James Sully" (preprint: Jamie Sully), "Tamera Lanhan" (preprint: Tamera Lanham). Corrected forms used above. A copy-editor checking against NeurIPS will see the typos — add a note if house style requires source-fidelity.
3. Affiliations (preprint only): 1 Anthropic, 2 University of Toronto, 3 Vector Institute, 4 Constellation, 5 Stanford, 6 Harvard. Perez, Grosse, Duvenaud = equal advising. Corresponding: Cem Anil <cem@anthropic.com>.

=== 2. WHAT WAS FETCHED (this verification pass) ===
- https://www.anthropic.com/research/many-shot-jailbreaking — SUCCESS (WebFetch, first-hand). Confirms date "Apr 2, 2024", the power-law sentence, the "merely delayed the jailbreak" line, the "61% to 2%" figure, the PDF URL.
- https://papers.nips.cc/.../ea456e232efb72d261715e33ce25f208-Abstract-Conference.html — SUCCESS (WebFetch, first-hand). Full author list verified character-by-character including all typos; title; venue; DOI.
- Prior agent's local extractions independently re-checked on disk: anthropic_msj.pdf/.txt (1,733 lines) and neurips_msj.pdf (2,064,274 bytes) /.txt (2,593 lines). All quotes below re-verified by direct grep against these extractions at cited line numbers.
- NOT fetched / NOT verified: OpenReview reviewer discussion; ACM DL record; any third-party replication. Follow-on works surfaced but NOT fetched and NOT citable on this record's say-so: arXiv 2504.09604 ("Mitigating Many-Shot Jailbreaking"), arXiv 2502.01925 ("PANDAS").
- FROM TRAINING KNOWLEDGE, NOT VERIFIED THIS SESSION: nothing. No claim in this record rests on memory.

=== 3. VERSION DISCIPLINE (CORRECTED — the prior report got this wrong) ===
The prior report claimed "Quotes are safe to attribute to either version." THIS IS FALSE. Verified divergences:
- "reliably": preprint has "can reli-/ably detect changes"; CAMERA-READY HAS "can detect changes" — reliably was CUT.
- "and monotonic" / "log-": preprint has "a predictable and monotonic increase in the log-likelihood"; CAMERA-READY HAS "a predictable increase in the likelihood" — both strengtheners CUT.
- Figure number: preprint "(Figure 5)"; camera-ready "(Figure 4)".
- Wolf passage: preprint adds a lead-in ("are also relevant to our findings. They show that..."); camera-ready runs it as one sentence. Substance identical, wording NOT.
- Appendices: prompt-based mitigations = preprint App. I / camera-ready App. K; jailbreak survey = preprint App. J / camera-ready App. L; HarmBench = preprint App. K / camera-ready App. M.
RULE: quote and cite from ONE version. If citing NeurIPS (recommended), use camera-ready wording. NOTE THE DIRECTION: both substantive cuts weakened the claim, and the prior report quoted the stronger preprint form in both cases while recommending the camera-ready cite. That is the COI over-read pattern (#49/#52) reproducing itself at the level of version selection. Do not quote a word the camera-ready editors deleted.

=== 4. PRECISE CLAIMS (camera-ready wording, line-verified) ===
Abstract: "We find that in diverse, realistic circumstances, the effectiveness of this attack follows a power law, up to hundreds of shots."
Eq. 1 (extraction): "-E[log P(harmful resp. | n-shot MSJ)] = Cn- + K" — the exponent symbol did NOT survive extraction. Paper's gloss: "Here, C is the y-offset, [alpha] is the slope and K is a scalar that controls the infinite-limit lower bound... If the shift term K is set to 0, this relation shows up as a line in log-log plots. For positive K, the relation takes a convex shape asymptoting towards a positive constant for large values of n." VERIFY THE RENDERED SYMBOL BEFORE TYPESETTING. Quote no figure-derived numbers: axis values mangled in extraction.
Models (Sec 3.2): "We evaluated [footnote] Claude 2.0, GPT-3.5-turbo-16k-0613, GPT-4-1106-preview, Llama 2 (70B) and Mistral 7B ... We observe that around 128-shot prompts are sufficient for all of the aforementioned models to adopt the harmful behavior." (Footnote markers silently cleaned; footnote 2 discloses Google DeepMind models could not be evaluated — no log-prob access.)
Matched distributions: "We run the majority of our experiments under the assumption that the final query-response pairs are sampled from the same distribution as the in-context demonstrations are (that is, D = D-tilde)." NOTE: pdftotext drops the tilde, rendering this as the self-contradictory "D = D"; the mismatch case is D != D-tilde (Sec 3.4). Restore the tilde when quoting.
Model size: "larger models tend to require fewer in-context examples to reach a given attack success probability... larger models learn faster in context, and so have larger power law exponents."
Measurement (CAMERA-READY wording): "We measure the effectiveness of MSJ attacks using log-probability based evaluations. Unlike sampling-based evaluations, these log-probability evaluations can detect changes of attack effectiveness even if the overall probability of attack success is very low." The power law is fitted to NLL OF A HARMFUL RESPONSE — a likelihood curve, not a deployed-system harm rate. Most important thing to get right in our citation.

THE MITIGATION FINDING (Sec 5) — alignment training moves the INTERCEPT, not the EXPONENT:
- "We find that the primary effects of SL and RL are on increasing the intercept of the power law, but not on reducing the exponent (Figure 4)." [Figure 4 in camera-ready; Figure 5 in preprint]
- "This implies that supervised finetuning to mitigate MSJ attacks is ineffective against protecting against MSJ with arbitrarily large context lengths."
- "That is, while targeted RL makes the model less susceptible to zero-shot attacks, increasing the number of shots has a predictable increase in the likelihood of harmful responses." [CAMERA-READY wording — do NOT add "and monotonic" or "log-"]
- THE SENTENCE TO QUOTE (verified verbatim identical in BOTH versions): "Overall, none of the finetuning-based interventions we've studied (SL or RL; with and without targeted training data) provided long-term relief from MSJ, as these methods are unable to substantially eliminate the in-context scaling of MSJ."
- Fig. 4 caption: "These results suggest that simply scaling up RL or SL training will not defend against MSJ attacks at all context-lengths."

*** SCOPE CORRECTION — CRITICAL, the prior report got this wrong ***
The Section 5 finetuning experiments were run on CLAUDE ONLY, on NON-PUBLIC INTERNAL CHECKPOINTS: "a pre-RL snapshot of a smaller Claude 2.0 instance" (camera-ready; preprint: "a pre-RL snapshot of Claude Instant"). No GPT/Llama/Mistral appears anywhere in Section 5 — the authors had no training access to them. "Five models across four developers" describes Section 3.2 ATTACK EFFECTIVENESS ONLY and MUST NOT be attached to the mitigation finding. Anyone citing "finetuning fails to reduce the exponent, across five models from four developers" will be corrected on sight.

AUTHORS' OWN TIE TO WOLF (camera-ready Sec 6): "The theoretical results of Wolf et al. (2023) show that, under the assumption that LLMs do Bayesian inference over their context, there exists a prompt with sufficient length that can elicit any behavior the model is capable of." THE AUTHORS MAKE THIS LINK THEMSELVES — we are not constructing it. Wolf is invoked as related work under ITS OWN Bayesian premise; the paper does not prove that premise holds.

BROADER IMPACTS (verbatim): "Model deployment in high-stakes domains (e.g., defense, healthcare, civil infrastructure, etc.) is currently minimal, but is likely to grow rapidly." ... "we feel that we as a society should collectively find and address problems now before model deployment in high-stakes scenarios becomes more widespread, and before models become even more capable." ... "It is also possible that MSJ cannot be fully mitigated. In this case, our findings could influence public policy to further and more strongly encourage responsible development and deployment of advanced AI systems." ... "a broader impact of our work is to encourage developers to adopt a healthy red-team blue-team dynamic."
DO NOT OVERREAD: the authors route the "cannot be fully mitigated" branch to "responsible development and deployment" and a "red-team blue-team dynamic" — NOT to abstention.

=== 5. WHAT IT DOES NOT CLAIM ===
- DOES NOT claim all mitigations fail. THE BIGGEST TRAP. A prompt-based defense WORKED: "ICD only slightly reduces the attack success rate (61% to 54%) on the deception category ... with a 205-shot MSJ prompt, whereas CWD lowers the effectiveness to 2%." (verbatim in BOTH versions; App. K camera-ready / App. I preprint). Only FINETUNING-based mitigation fails to touch the exponent.
- DOES NOT claim MSJ is unmitigable: "Our results do not reject the idea that qualitative changes to existing finetuning pipelines might prove more effective against MSJ." And it names the target: "Effective solutions should either reduce the slope, or increase the offset term K of in-context power laws on harmful tasks."
- DOES NOT rule out context-length limits. Sec 5: "We could also constrain the context length, but this impacts model usefulness, and so is undesirable." The authors reject this defense on UTILITY grounds, NOT safety grounds. We must engage this, not ignore it.
- DOES NOT prove epsilon > 0 for any deployed system. Empirical scaling on API-accessed 2023-era models; mitigation results on internal Claude snapshots.
- DOES NOT claim the attack works on production chat platforms. See limitations.
- DOES NOT establish a rate bound or any lower bound on expected harm. It licenses a forecast of CONTEXT LENGTH REQUIRED for elicitation — nothing about operational harm frequency. Citing it as bounding expected harm in a weapon system is a category error (frozen rule 4).
- DOES NOT make the abstention argument — routes to monitor-and-update, i.e. STRUCTURALLY THE SAME ROUTE AS NIST, from an Anthropic-authored paper.
- DOES NOT address unbounded cost or minimax structure at all. Premise B gets ZERO support here.
- Power law is "up to hundreds of shots" — bounded empirical range, not asymptotic.

=== 6. AUTHORS' OWN LIMITATIONS ===
NeurIPS Paper Checklist, limitations = [Yes]: "We highlight the most crucial two limitations of the jailbreak proposed, which are 1) this jailbreak doesn't work on chat platforms like ChatGPT or Claude.ai without bells and whistles (Section 2), 2) the jailbreak is occasionally not robust to distribution shifts between demonstration and the final query." Also discloses "we ran a responsible disclosure meeting with some of the largest large language model providers."
Section 2: "Note that MSJ without bells and whistles requires API access. Systems like ChatGPT or Claude.ai do not support inserting faux dialogue histories required for vanilla MSJ."
Sec 3.4: narrow topic-mismatch defeats the attack ("sampling the demonstrations narrowly from the 'discrimination' category fails, while sampling broadly from all categories except deception recovers the baseline performance").
Sec 5: "this solution might suffice for bounded-context models deployed in production" — the authors CONCEDE intercept-raising may be adequate in production, qualifying only that "it is unclear if mitigations that do not reduce the power law exponent are viable long-term solutions." Note "unclear," not "are not."

=== 7. HOSTILE-REVIEWER ASSESSMENT ===
Strongest objection, and it is largely right: "You cite a paper whose own checklist says the attack doesn't work on deployed chat platforms, to argue deployed systems carry an ineliminable residue — and you suppress that the same paper found a prompt defense taking success from 61% to 2%, in the very section you cite for 'mitigations fail'."
- CWD 61%->2%: FULLY RIGHT AND DANGEROUS. We MUST state it ourselves before a reviewer does. Our surviving counter: 2% != 0% (CWD reduces, does not eliminate — itself an INSTANCE of epsilon > 0); it has unevaluated costs ("Future work should evaluate the safety-capability trade-offs of Cautionary Warning Defense"); it is a PROMPT-LAYER defense, i.e. squarely inside the behavior layer whose residue Premise A concerns; and it was tested on one category at one shot-count.
- API/chat-platform limit: PARTLY RIGHT, cuts both ways. It blocks "MSJ works against deployed products." It does not rescue military AI: an integrated LAWS system is precisely where the operator/integrator HAS API-level or deeper access and CAN construct faux dialogue history. The defense is a PRODUCT-SURFACE restriction, not a model property. Defensible — but we must ARGUE it, not assume it.
- Existence theorem != rate bound (frozen rule 4): fitted NLL over <= hundreds of shots on 2023-era models. Licenses context-length forecasts only.
- Single-vendor mitigation result: the Premise-A-load-bearing Section 5 finding is Claude-only on non-public internal checkpoints. A reviewer will say the central result is unreproducible and vendor-internal. True. We cannot refute it.
- Model staleness: Claude 2.0 / GPT-3.5 / GPT-4-1106 / Llama-2 / Mistral-7B are all 2023-era. "This is fixed by now" cannot be refuted from this paper.
- SHARPEST COI OBJECTION — not the authorship, but that THIS PAPER'S OWN BROADER IMPACTS ROUTES ITS FINDING TO MONITOR-AND-UPDATE, NOT ABSTENTION. Our mandatory NIST rebuttal must be run against THIS SOURCE TOO. A reviewer will say: "Even the authors of your Premise A evidence disagree with your conclusion." That is TRUE and we should say it plainly. Our reply is the domain distinction — the authors reasoned about a bounded-cost context and SAY SO ("currently minimal" high-stakes/defense deployment). Their monitor-and-update route was scoped to a world where the defense case was hypothetical. Legitimate — but it is OUR argument, not theirs, and must not be smuggled in as if the paper endorsed it.
- AGAINST US: the paper's bounded/unbounded language is about CONTEXT LENGTH, not COST. Do not let "bounded" equivocate between the two. A sharp reviewer will catch it.

=== 8. THE HONEST, DEFENSIBLE USE (corrected) ===
1. Cite for the narrow, strongly supported claim: ALIGNMENT FINETUNING (SL AND RL) RAISES THE INTERCEPT BUT DOES NOT REDUCE THE EXPONENT of MSJ's in-context power law — quoting the "none of the finetuning-based interventions" sentence. This is the strongest empirical support in the literature for "the behavior layer leaves an adversarially-elicitable residue that training does not close." STATE THE SCOPE HONESTLY: this finding is Claude-only, on Anthropic-internal pre-RL checkpoints. The five-models/four-developers result is the ATTACK's generality (Sec 3.2), a separate claim — cite them separately, never fused.
2. Cite as the EMPIRICAL COMPANION TO WOLF, noting the authors make the link themselves (camera-ready Sec 6). Cleanest use; not our construction.
3. DISCLOSE IN OUR OWN VOICE: the CWD 61%->2% result; the API-only limitation; the 2023-era models; the single-vendor scope of the mitigation finding; and that the authors route to monitor-and-update.
4. Make NO independence claim.
5. Do NOT cite for Premise B (nothing) or for any rate bound.

=== 9. COI DISCLOSURE (frozen Seventh Work rule) ===
- Anthropic dominates authorship (affiliation 1; corresponding author @anthropic.com). Four authors carry no Anthropic affiliation (Agrawal, Schaeffer, Bashkansky, Svenningsen — Constellation/Stanford/Harvard), but all are co-authors on an Anthropic-led paper. ANTHROPIC IS A PROPONENT OF THE PARADIGM UNDER EVALUATION. NO INDEPENDENCE CLAIM CAN BE MADE.
- THE MOST IMPORTANT COI ITEM: the Section 7 heading "Independent Replication on HarmBench" IS A DISCLOSURE HAZARD. The paper's own text: "This evaluation was conducted by an independent part of our team, on an independent codebase and with subtly different design choices... In this sense, these results can be thought of as an unofficial attempt at replicating our findings." "INDEPENDENT" MEANS INDEPENDENT-WITHIN-ANTHROPIC. It is NOT third-party replication. If we cite Sec 7, the section title alone could mislead. Must be disclosed explicitly.
- REPRODUCIBILITY (upgraded from the prior report): BOTH the attack tool AND the mitigation experiments rest on non-public Anthropic assets — a non-public "model with safety interventions turned off" generated the attacks, and the Section 5 finetuning results are on non-public internal Claude snapshots. The core Premise-A result is NOT externally reproducible.
- MITIGATING FACTOR, stated fairly: the paper is ADVERSE TO THE PROPONENT'S INTEREST — it reports that its own company's alignment pipeline fails to close the scaling, on its own flagship model. Proponent-authored evidence AGAINST the proponent's paradigm is epistemically stronger than proponent-authored evidence for it. This strengthens Premise A's use without licensing any independence claim.
- AGAINST US: the framing choices (red-team/blue-team; "responsible development") are exactly what proponent-side framing predicts. CITE THE FINDING; DO NOT INHERIT THE FRAMING.

=== 10. VERDICT ON THE PRIOR SWEEP ===
PARTIALLY WRONG (scoped: only the role assignment was available, not full sweep prose).
- CONFIRMED: power-law scaling of attack effectiveness with in-context demonstrations; across five models from four developers (Sec 3.2); safety finetuning does not eliminate the scaling. The "empirical companion to Wolf" role is CONFIRMED AND STRONGER THAN ASSUMED — the authors make the Wolf link themselves.
- WRONG IF THE SWEEP SAID "mitigations fail": it shows FINETUNING-based mitigations fail to reduce the exponent, while a PROMPT-based mitigation (CWD) cut attack success 61% -> 2%. A blog-only summarizing pipeline would very likely produce this error: the blog's "merely delayed the jailbreak" line is about finetuning, and the blog reports 61%->2% POSITIVELY, as Anthropic's mitigation success. Invisible without reading Sec 5.4.
- ALSO MISSED BY ANY BLOG-ONLY SWEEP: (i) the checklist limitation that MSJ does NOT work on ChatGPT/Claude.ai without extra work; (ii) that Sec 7's "Independent Replication" is in-house; (iii) that Broader Impacts routes to monitor-and-update, i.e. AGAINST our bridge; (iv) that the mitigation finding is Claude-only on internal checkpoints. Each is material.

=== 11. CONFIDENCE AND RESIDUE ===
HIGH CONFIDENCE, verified this pass by first-hand fetch (blog + NeurIPS page) and direct line-level re-grep of both full-text extractions: all quotes above with their version attributions; author lists and inter-version discrepancies; models tested; 128-shot figure; Sec 5.1-5.4 mitigation findings and their Claude-only scope; the "none of the finetuning-based interventions" sentence (confirmed verbatim identical in both); the 61%/54%/2% figures (confirmed verbatim in both); the Wolf passage (confirmed NOT verbatim identical — lead-in differs); the NeurIPS checklist limitations answer; Broader Impacts including the defense/high-stakes sentence; affiliations; the DOI as displayed.
VERIFY BEFORE TYPESETTING: the Eq. 1 exponent symbol and the D-tilde in the matched-distribution quote (both lost to text extraction). Quote no figure-derived numbers.
NOT VERIFIED: OpenReview reviewer discussion; ACM DL record beyond a search-returned string; existence of any genuinely third-party MSJ replication. Follow-on works arXiv 2504.09604 and arXiv 2502.01925 were surfaced but NEVER FETCHED — do not cite on this record's authority.
OPEN GAP IF PREMISE A IS LOAD-BEARING: every model here is 2023-era and the mitigation result is single-vendor and internally-checkpointed. This source cannot answer "has this been fixed since?" A hostile reviewer will press exactly there. That gap needs a separate, more recent, ideally NON-PROPONENT source.

Local artifacts (auditable): C:\Users\PC\AppData\Local\Temp\claude\C--Users-PC\de004d8e-acb9-46c3-b457-0f594871974a\scratchpad\anthropic_msj.pdf / .txt (1,733 lines) and neurips_msj.pdf (2,064,274 bytes) / .txt (2,593 lines). Existence, sizes, and line counts independently confirmed this pass.

---

## 検証段が発見した過大主張・誤り（8件）

- LOAD-BEARING, MOST SERIOUS — 'Across five models from four developers' attached to the FINETUNING finding (recommended use #1). FALSE. The five-models/four-developers scope belongs to Section 3.2 (attack effectiveness). The Section 5 mitigation experiments — the actual load-bearing result for Premise A — were run on Claude only, specifically on non-public internal checkpoints ('a pre-RL snapshot of a smaller Claude 2.0 instance' in the camera-ready; 'a pre-RL snapshot of Claude Instant' in the preprint). No GPT/Llama/Mistral appears anywhere in Section 5; the authors lacked training access. The report inflates the generality of the exact sentence it tells us to build Premise A on.

- BLANKET CROSS-VERSION CLAIM IS FALSE — 'Quotes below are safe to attribute to either version.' At least four divergences found. Both substantive ones quote the STRONGER preprint wording while the report recommends citing the WEAKER camera-ready. Two-for-two in the hoped-for direction: the documented COI over-read pattern (#49/#52), even if the mechanism was innocent (quotes likely drafted off the preprint first).

- MISQUOTE vs the recommended version — 'these log-probability evaluations can RELIABLY detect changes of attack effectiveness'. 'Reliably' is in the preprint only (hyphenated 'reli-/ably', which is why a naive grep misses it). The NeurIPS camera-ready reads 'can detect changes' — 'reliably' was cut. The report presents this quote unversioned, in the passage it itself calls 'the single most important thing to get right in our citation'.

- MISQUOTE vs the recommended version — 'increasing the number of shots has a predictable AND MONOTONIC increase in the LOG-likelihood of harmful responses'. That is the preprint. The camera-ready reads: 'increasing the number of shots has a predictable increase in the likelihood of harmful responses.' Both 'and monotonic' and 'log-' were removed by the camera-ready editors. 'Monotonic' is strictly stronger than 'predictable', and monotonicity is precisely what a no-lower-bound argument wants. Do not quote the deleted word.

- WRONG FIGURE NUMBER for the recommended version — the report quotes '(Figure 5)' in the intercept/exponent sentence and cites 'Figure 5 caption'. The camera-ready says '(Figure 4)'. Figure 5 is correct for the preprint only.

- INTERNAL CONTRADICTION — the report asserts 'the Wolf et al. passage ... verbatim identical in both', then two paragraphs later documents that the preprint carries an extra lead-in sentence ('are also relevant to our findings. They show that...'). It is not verbatim identical. Substance is identical; wording is not. The report caught the difference but did not retract its own identity claim.

- QUOTED EXTRACTION ARTIFACT — 'the final query-response pairs are sampled from the same distribution as the in-context demonstrations are (that is, D = D)' and 'when D = D in Section 3.4'. The tilde/negation did not survive pdftotext (should be D = D-tilde, and the mismatch case D != D-tilde). As printed, the report's own quote is self-contradictory and would confuse a copy-editor. The report flagged symbol loss for Eq. 1 but not here.

- OMISSION on a page it claims to have fetched — the NeurIPS abstract page displays DOI 10.52202/079017-4121. The report claims it fetched that page for 'Full author list, venue, abstract' but reports only an ACM DL identifier (10.5555/3737916.3742037) obtained via search. Not dishonest; incomplete on a page it says it read.


## 取得honesty監査（5件）

- NONE MATERIAL — the fetch report is credible and survives adversarial checking. This is an unusually well-executed verification. Specifics I confirmed independently: both PDFs exist on disk at the stated scratchpad paths; neurips_msj.pdf is exactly 2,064,274 bytes as claimed; the .txt extractions are exactly 1,733 and 2,593 lines as claimed; every quote I spot-checked (nine of them) traces to real text at real line numbers in the actual extractions. The report did not fabricate.

- The author-block typos are the strongest fetch-honesty evidence and I verified them character-for-character against my OWN independent WebFetch of the NeurIPS page, not the agent's files: 'Fracesco Mosconi', 'James Sully', 'Tamera Lanhan', 'Roger Baker Grosse', 'Nina Panickssery' — all confirmed as displayed by NeurIPS. The preprint's differing forms ('Nina Rimsky', 'Francesco', 'Jamie Sully', 'Tamera Lanham') confirmed in the preprint PDF. Nobody reconstructs that pattern from memory.

- My independent WebFetch of the Anthropic blog independently confirms the report's blog-derived claims: date 'Apr 2, 2024'; the power-law sentence; the 'merely delayed the jailbreak' line; the '61% to 2%' figure; and the exact PDF URL. All match.

- Version-provenance sloppiness, NOT dishonesty — the report reads as though it was drafted against the preprint and then retrofitted to recommend the camera-ready, leaving preprint wording, figure numbers, and one deleted adverb inside quotes attributed to 'either version'. Real defect, but it is a diligence failure, not a fabrication.

- Stated gaps are honest and correctly bounded: it did not fetch OpenReview reviews, did not verify the ACM record, found no arXiv version, and explicitly refused to vouch for two follow-on works (arXiv 2504.09604, 2502.01925) it surfaced but did not fetch. It correctly declined to quote any figure-derived numbers after the axis values mangled. It labels nothing as from memory and, as far as I can check, relies on memory for nothing.


## 引用可能性の裁定

MOSTLY DEFENSIBLE — but recommended-use #1 must be narrowed before it survives a hostile reviewer, and the narrowing costs us real generality. As written ('alignment finetuning raises the intercept but does not reduce the exponent... Across five models from four developers') it fails on contact: the finetuning result is Claude-only, on non-public internal pre-RL checkpoints. Corrected, it still supports Premise A — but as a single-vendor, externally unreproducible result from the vendor itself, which sharpens rather than softens the COI problem. The report flagged the non-public helpful-only ATTACK model but missed that the MITIGATION experiments are likewise on non-public internal snapshots; that is the more serious reproducibility item and it sits directly under Premise A. Recommended uses #2 (empirical companion to Wolf, authors' own link, verified at camera-ready Section 6), #3 (self-disclose CWD/API-limit/2023-models/monitor-and-update), #4 (no independence claim), and #5 (not for Premise B, no rate bound) are all correct and verified, and #3-#5 are the report's genuinely strong work. The report's own hostile-reviewer section is honest and largely pre-empts the obvious attacks — it correctly surfaces the 61%->2% CWD result as damaging to us, correctly identifies the 'Independent Replication' heading as independent-within-Anthropic ('an independent part of our team', 'an unofficial attempt at replicating our findings' — both verified verbatim), correctly warns that Broader Impacts routes to monitor-and-update AGAINST our bridge, and correctly refuses to overread 'cannot be fully mitigated'. One further hostile lever the report missed: Section 5 explicitly names context-length constraint as an available defense ('We could also constrain the context length, but this impacts model usefulness, and so is undesirable') — the authors reject it on UTILITY grounds, not safety grounds. In an unbounded-cost domain that trade flips, which helps our domain distinction, but it also means the paper concedes a real mitigation exists that we must address rather than ignore. The report's warning against equivocating 'bounded' (context) with 'bounded' (cost) remains the sharpest self-check in the document and should be retained verbatim.
