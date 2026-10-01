# Why research gets parked: obstacle types behind authors' own statements of undone work in four fields

**Draft v0.1, 2026-09-25 (references verified 2026-09-25).** Every numeric claim carries a source.
Sources are repository files unless stated otherwise; `LAERDOM §n` refers to sections of
`docs/LAERDOM.md`, which records what was measured, when, and what was concluded. Every literature
reference has been checked against Crossref or the arXiv metadata API; full details are listed in
§8. Claims that could not be substantiated have been removed rather than hedged.

---

## 1 Introduction

Researchers regularly write down what they did not get done, and why. A critical edition notes that
three manuscripts were not collated; a cohort study notes that a subgroup could not be analysed; a
simulation study notes that the full time series was not used. These are not failures hidden in
correspondence — they are printed, in the work itself, in the author's own words, usually with a
stated cause.

This paper asks two questions of that material. **How often does it occur?** And, more importantly,
**what kinds of obstacles are named?** The second question is the point of the study. A parked question whose stated obstacle is that the data never existed is a different object from
one whose stated obstacle is a shortage of time for reading sources, and the difference determines
what could ever unpark it.

We measure both on 100 open-access works drawn from four fields, and we report the distribution of
obstacle classes as the primary result. The detection tool used to locate candidate passages is
reported in full, including its error rates, but it is an instrument and not a finding.

## 2 Positioning against existing work

**Prematurity.** Stent's *premature discovery* is one that cannot be connected to canonical
knowledge at the time it is made — an obstacle located in the field's interpretive apparatus rather
than in its materials (Stent 1972; the case literature is collected in Hook 2002). Our axis runs the
other way: in this material the dominant obstacle is missing data, not missing concepts (§4).
Prematurity and parked questions are two answers to the same question about why knowledge waits, and
they sit at opposite ends of it.

**Sleeping beauties.** That literature identifies delayed recognition from citation trajectories — an
external signal measured on the community's behaviour rather than on the author's account (van Raan
2004). Ke et al. (2015) showed that such delay is not a distinct class: the distribution of their
"beauty coefficient" is continuous and follows a power law, "suggesting a common mechanism behind
delayed but intense recognition at all scales". Our unit is the author's own dated admission, which
exists whether or not the work is ever cited, and which names a cause. The two approaches are
complementary: one finds work the field ignored, the other finds work the author declared unfinished.

**Self-admitted technical debt.** Software engineering has a mature literature on developers
annotating their own shortcuts in source comments; Sutoyo and Capiluppi (2024) review a decade of
detection approaches, and Melin et al. (2026) carry the construct into scientific software, tracking
prioritisation, sentiment and propagation across artefacts. Methodologically this is our closest
analogue: a self-reported, machine-findable admission embedded in the artefact itself. We borrow the
framing and apply it to the research record.

**Limitations extraction.** Extracting limitations and future-work statements from papers is
established. LimTopic models the topics of stated limitations (Al Azhar et al. 2025); FutureGen
generates future-work sections by retrieval (Al Azher et al. 2025); LimitGen evaluates whether
language models can identify the limitations of a paper at all (Xu et al. 2025); REAL ML approaches
the same material from the author's side, as a method for recognising and articulating limitations
(Smith et al. 2022). Our addition is not extraction but **classification of the stated cause**,
against a typology fixed before data collection, together with a measured error rate for that
classification.

**Agents that generate gaps.** A growing line of work asks models to propose research directions:
SciMON optimises generated inspirations for novelty (Wang et al. 2023), Chain of Ideas develops ideas
through an agent chain (Li et al. 2024), ResearchAgent iterates idea generation over the literature
(Baek et al. 2024), PaSa searches the literature as an agent (He et al. 2025), and InternAgent closes
the loop from hypothesis to experiment (InternAgent Team 2025). ForeSci evaluates such forward-looking
judgment directly (Tian et al. 2026). All of it points forward, into what has not been written. We
point backwards, at a dated admission that already exists and can be checked against the text that
contains it.

## 3 Method

**Preregistration.** The protocol was written and locked before data collection (`PREREG-v1.md`,
sha256 `05988b23…`) and corrected through dated addenda (ADDENDUM-01–25 at the time of deposit v0.4.0), each committed separately with its own
sha256. Addenda written after data were seen say so in their own text; ADDENDUM-10 §0 is explicit
about this, and reports how much it moved the numbers (§7).

**Fields.** Four purposively chosen fields — energy modelling, archaeology, clinical epidemiology,
textual scholarship — selected to span biomedicine and the humanities, not sampled from science as a
whole (`PREREG-v1.md` §4).

**Frame.** Works with an OpenAlex topic in the field, published 2015–2020, `open_access.is_oa:true`,
**and** full text that could actually be retrieved (ADDENDUM-04 §1.1). Retrievability is part of the
frame, not an accident of collection: in the energy-modelling frame, 9,713 of 30,362 works were
retrievable, 32.0 % (`LAERDOM §3`).

**Unit of observation.** The passage: the candidate sentence together with the two sentences on
either side. A hit requires the undone work and the obstacle to fall inside the same passage **and**
to be linked, with the undone work belonging to the study being reported (ADDENDUM-03 §1.2). M1 is reported twice — strict (same sentence) and
passage — and never as a single number.

**Judging.** A local model (gemma2:9b, temperature 0, seed 734248, weight sha256 `ff1d1fc7…`)
classified all 22,243 passages of the 100 works; every judgment carries a model signature
(ADR-0003, ADR-0008). Determinism was verified before and after the batch: 47/47 and 50/50 identical
re-runs (`LAERDOM §13`, `data/port/determinisme-ADR0008.json`).

**Ground truth.** 320 passages were read blind by the coder: 150 judged hits, 50 judged NONE, 50
judged N3 (a scope statement with no named obstacle), all 50 judged N1/N2 (answered in the same
article, or a novelty claim), and 20 anchors from an earlier ground-truth set. The key linking
passage to judged class was opened only after all 320 verdicts were written
(`docs/RESULTAT-PORT-v1.md`; `data/port-presisjonssett-verdikter.jsonl`).

**Who did the coding, and how well it reproduces.** Both the model-based classification of all
22,243 passages and the blind reading of the 320-passage sample were carried out by an LLM-based
assistant working under the author's direction; no human annotator coded this material. To measure
whether the coding rules reproduce, the same 320 passages were coded a second time by a separate
instance with an empty context, given only the blind file and a verbatim extract of the rules, with
the first coder's verdicts, the key, the judge's output, the findings log, the result note and the
manuscript all withheld (ADDENDUM-11). Agreement on the hit decision was **κ = 0.81 (95 % CI
0.70–0.91)** across all 320 and **κ = 0.77 (0.62–0.90)** on the port material alone, with raw
agreement 96.2 % and 96.7 %; class agreement among passages both coders called hits was **κ = 0.73
(0.48–0.94)** on 30 items. Because both coders are LLM-based and share a rule set, this measures
reproducibility of the rules across independent readings, not agreement with a human reader.

## 4 Results

| Result | Value | Source |
|---|---|---|
| Material | 100 works, 66,833 sentences, 22,243 passages | `data/port/spesifikasjon.json` |
| Judged hits | 2,173 (9.8 % of passages) | `data/port/dommer-*.jsonl` |
| **M1 corrected, passage** | **0.671** | `docs/RESULTAT-PORT-v1.md`, "Etter ADDENDUM-10" |
| M1 corrected, strict | 0.667 | same |
| M1 raw, ≥1 / ≥2 / ≥3 hits per work | 0.930 / 0.850 / 0.830 | same |
| **M2 (judgeability), read true hits** | **coder 1: 88.0 % (22/25) · coder 2: 31.6 % (6/19)** | same; `ADDENDUM-11.md` §5 |
| **Obstacle distribution (25 read true hits)** | **H7 17, H5 3, H8 2, H2 2, H9 1** | same |
| **Liftable share (H1–H6)** | **5 of 25 = 20.0 %** | same |
| Judge precision | 25/150 = 16.7 % [11.6–23.4] | same |
| Miss rate among non-hits | NONE 2.0 %, N3 2.0 %, N1 0/37, N2 0/13; weighted 2.0 % | same |
| Implied judge recall | ≈ 46 % | `LAERDOM §16` |
| Anchors (drift check) | 12/12 known hits, 8/8 known non-hits, 75 % exact class | `data/port/presisjon-resultater.json` |
| **Inter-coder agreement, hit decision** | **κ = 0.81 [0.70–0.91]**, raw 96.2 % | `ADDENDUM-11.md` §4 |
| Inter-coder agreement, class | κ = 0.73 [0.48–0.94] on 30 items | same |
| Second coder: precision / M1 corrected / liftable | 12.7 % [8.3–18.9] / 0.604 / 2 of 17 resolved = 11.8 % [3.3–34.3]; unresolved 2 of 19 | same §5; liftable share per `docs/KORRIGENDUM-2026-09-28-frys-v0.4.0.md` § B |

**The distribution of obstacle classes is the finding.** Seventeen of the 25 true hits that survived
reading (68 %) fall in class H7, *the data did not exist*: never recorded, not preserved, or never
collected. Three fall in H5 (computation or solver), two in H8 (access, law, ethics), two in H2
(legibility of a damaged source) and one in H9 (the concept or theory was missing). No instance of
H1 (human reading or coding at scale), H3 (language barrier), H4 (pattern recognition at volume) or
H6 (structure inference) survived reading.

**M1 raw is a base rate, not a prevalence.** Ninety-three of the 100 works carry at least one judged
hit, but only 16.7 % of judged hits survive reading. The corrected estimate, 0.671, propagates the measured
precision per class; both numbers are reported, and the raw number is never reported alone
(`docs/RESULTAT-PORT-v1.md`).

**M2 cannot be reported as one number, and that is a finding about the protocol.** The two coders
returned 88.0 % (22/25) and 31.6 % (6/19) judgeability on their own true hits — a threefold gap on
the same passages under the same written rule. The reason is not carelessness on either side:
PREREG-v1 §2 defines M2 as the share of hits where "is this obstacle lifted today" can be decided
*without a domain expert*, and it never says what a domain expert is. The first coder read the
question as one about the **kind** of obstacle (a lost source is permanently lost; anyone can settle
that). The second read it as one about the **current state of the field's methods and data** (whether
this particular obstacle has been overcome needs someone who follows that literature). Both readings
sit inside the wording. **M2 is therefore not operationalised**, and we report it per coder rather
than as a single figure. Sharpening the definition is a precondition for using M2 at all; until then
the number carries a coder identity or it carries nothing.

**The rules reproduce on the hit decision, and the main finding survives independent recoding.**
Agreement between the two coders was κ = 0.81 (95 % CI 0.70–0.91) across all 320 passages and
κ = 0.77 (0.62–0.90) on the port material alone, with class agreement κ = 0.73 (0.48–0.94) among the
30 passages both called hits. More to the point than the coefficients: **the finding does not depend
on which coder you believe.** H7 accounts for 17 of 25 true hits (68 %) in the first reading and 12
of 19 (63 %) in the second, and the two precision estimates — 16.7 % [11.6–23.4] and 12.7 %
[8.3–18.9] — overlap across their whole range. A reader who prefers the second coder's stricter
reading gets a lower prevalence (M1 corrected 0.604 against 0.671) and the same conclusion.

**Agreement is uneven in a way that points at the rubric, not at the coders.** By field, κ on the hit
decision runs from **1.00 in clinical epidemiology** (n = 52) through tekstvitenskap 0.85 and
archaeology 0.75 down to **0.39 in energy modelling** (n = 101). The disagreements are not scattered:
**six of the twelve** hit/non-hit disagreements are the same dispute — whether a stated model,
method or scope limitation counts as a named obstacle or as a self-imposed simplification (the second
coder called all six N3). Of the remaining six, three turn on whether the passage answers its own
question, and in three the second coder found a hit the first did not. ADDENDUM-10 §3 was
written to settle exactly that question and does not settle it in practice. The rubric is sharp where
obstacles are concrete — a source that does not survive, an approval that was refused, a sample that
was never collected — and blurry where the obstacle is a modelling choice the authors made
themselves. Prevalence figures for computation-heavy fields inherit that blur.

**The judge is a weak instrument in both directions.** Precision is 16.7 %, and the miss rate among
non-hits is 2.0 %, which across 20,070 non-hit passages implies roughly as many missed true hits as
found ones (`LAERDOM §16`). In an earlier blind evaluation on a curated set of 110 passages — 55 known hits
and 55 negatives — the same prompt found 45 of the 55 known hits (81.8 %), and 45 of its 47 flags were
correct (95.7 %), with exact class agreement of 45.5 % (`LAERDOM §6`). These are shares of a curated set,
not recall and precision in the material; performance
on the full corpus was substantially worse, and that discrepancy is reported rather than resolved. The humanities/biomedicine
split, on the same kind of curated set, was 72.0 % of known hits found in the humanities against 90.0 %
in biomedicine (`LAERDOM §9`).

**Frame skew.** Retrievability, not open-access status, selects the frame. ScienceDirect fell from
1,994 to 30 works, IOP from 1,221 to 4, while arXiv rose from 4.7 % to 14.5 % of the frame and MDPI
from 6.8 % to 17.4 % (`LAERDOM §3`). The material is displaced toward preprint and MDPI-like
channels, and every prevalence figure inherits that displacement.

## 5 One parked question, carried out

PS-246, a true hit in class H5: a 2016 thesis on cropmarks could not enter its **measured matric
density** into the Saxton–Rawls soil-water equations, because the SPAW tool fixes particle density at
2.65 Mg/m³; field capacity came out above saturation, and the thesis applied a correction factor of
2.22 instead (`docs/PS-246-KRITERIUM.md`).

The success criterion was locked before computation (sha256 `137bde50…`, commit `59d4221`). The
implementation was verified against the source article's own Table 3 — all twelve texture classes
reproduced exactly — before the thesis data were touched (`tests/test_saxton_rawls.py`).

| | Result | Source |
|---|---|---|
| Inconsistency reproduced with fixed 2.65 | 8 of 29 horizons, including exactly the four the author names | `docs/PS-246-RESULTAT.md` |
| Criterion met with measured particle density | 2 of 4 horizons | same |
| Margin on the two that flip | +0.1 and +0.3 %v | same |
| Reading uncertainty (values legible only from a figure) | ±0.02 Mg/m³ | same |
| Required density for the two that do not flip | 2.98 Mg/m³ and 2.70 (measured 2.62) | same |

**Neither an AI axis nor a time axis.** Saxton and Rawls (2006) appeared ten years before the
thesis, and the equations were available throughout. What was missing was time and a tool that accepted
the measured value. The thesis also states the expected outcome without the computation; carried
out, it holds for two of the four horizons it names. The decisive limitation
was not the equations but legibility: the measured particle densities exist only as figures without a
text layer, and that reading error alone determines the sign for both marginal horizons.

## 6 Discussion

**Research is parked on missing data.** If 68 % of surviving true hits are H7, then the binding
constraint in this material is the record itself: measurements never taken, sources not preserved,
variables not reported. That is a claim about data infrastructure and data sharing, not about
analysis capacity.

**It also bounds what any tool can unpark.** Five of the 25 true hits fall in a class that the
locked table calls liftable, and of the four such candidates examined in detail only one was
practically executable with the materials at hand (`docs/LOFTBARE-VURDERING-v1.md`). The class
states what kind of obstacle was named; it does not state whether the material still exists.

**Base rate against precision.** A detector that flags 9.8 % of passages will make almost every work
look affected. The gap between M1 raw (0.930) and M1 corrected (0.671) is the size of that illusion
in this material, and it is only measurable because a stratified sample was read blind.

**The passage names the obstacle, not the resource.** All 229 judged liftable hits that the blind
sample had not already covered were scored on four signals computable without reading them: whether
the work states data availability, how heavy the material is given the judged class, how often the
passage points to a table, figure or equation, and how many works cite it. The criterion was locked
before any figure was computed (`ADDENDUM-12.md`). **205 of 229 (89.5 %) carry no reference to
material at all**, and only 17 (7.4 %) score at least one on every computable signal. Reading the
top-ranked 15 gave **2 true hits (13.3 %)** against the **16.7 % [11.6–23.4]** measured on the
stratified sample — the ranking did not beat chance. Two of the four signals turned out to be
unusable as built: the data-availability signal cannot separate the authors' own data from
third-party data merely mentioned in the text (7 of the 15 inherited a full score from phrases about
a geological survey and a weather service), and the citation signal could not be computed at all from
the frozen material. **This is a limit on the class of tool, not on this implementation:** a parked
question is written as a reason why something was not done, not as a recipe for doing it, so
feasibility cannot be ranked from the hit passage. It can only be ranked by opening the work — which
is the work the ranking was meant to save.

**Material access follows publication format, not discipline.** Moving the feasibility decision from
the passage to the work — 100 works against 22,243 passages — makes it answerable, because a data
availability statement, a supplement and a machine-readable table live in parts of the text no hit
passage touches. Classifying all 100 source documents on what they actually contain gives **3 open,
55 partial and 42 closed** (`ADDENDUM-13.md`). The split is not by field but by format: **all three
open works are JATS articles, no JATS work is closed, and 38 of 74 PDFs are** — because only **4 of
100 works carry a data availability statement covering the authors' own data**, 29 mention
third-party data, and **67 carry none at all**. Where a journal template forces the section it
exists; where the document is a PDF thesis it does not. Textual scholarship is 23 of 25 closed, not
because the field hides data but because it publishes PDFs without table structure. **This is the
same pattern retrievability showed** at the other end of the pipeline, where ScienceDirect fell from
1,994 works to 30 while arXiv rose from 4.7 % to 14.5 % of the frame and the split followed delivery
rather than business model (`LAERDOM §3`; `ADDENDUM-08 §2`). Two independent measurements on
different links in the chain point the same way: whether a parked question can be resumed is decided
by the infrastructure around publication, not by the content of the field. A blind test of the work
classifier on five drawn works — verdicts written before the scores were opened — was right in four,
and the one miss had a measured systematic cause: the caption patterns were English-only, which put
six works in the closed bucket for language alone (a seventh with non-English captions is correctly
closed; `ADDENDUM-13 §5`). The error is one-sided: a missing pattern can
only make a work look more closed than it is.

**Liftability is dated.** The study's positive control for H1 — a 2019 thesis outside the 100 sampled
works, whose collation of three British Library manuscripts (93 manuscript pages) was left undone — was H1 (human reading at scale) when the thesis
was written and has been H8 (access) since October 2023, because the library's digitised images have
not returned to open channels (`docs/HERON-KOLLASJON-VURDERING-v1.md`; ADR-0010). A liftability table is dated at
the moment it is written, and a register that cannot record that has recorded something false.

## 7 Limitations

1. **Two coders, both LLM-based; no human annotator.** The 320 passages were coded twice: first by
   the instance that also built the judge and the prompt, then by a separate instance with an empty
   context and no access to the first coder's output (ADDENDUM-11). Agreement on the hit decision was
   κ = 0.81 [0.70–0.91], and the main finding holds in both readings — H7 accounts for 17 of 25 true
   hits in the first and 12 of 19 in the second, with overlapping precision intervals. Two caveats
   remain. **No human annotator has coded this material**, so κ against human reading is still
   unmeasured, and both coders share a model family and a rule set. And agreement is uneven across
   fields: κ = 1.00 in clinical epidemiology against **0.39 in energy modelling**, where the readings
   diverge systematically on whether a model limitation is a named obstacle or a self-imposed
   simplification.
2. **M2 does not survive recoding.** The two coders reported 88.0 % and 31.6 % judgeability on their
   own true hits, because PREREG-v1 §2 does not define "without a domain expert" tightly enough to
   force one reading. M2 is reported here with coder identity attached, and should not be quoted as a
   single number until the definition is sharpened (ADDENDUM-11 §5).
3. **Purposive fields.** Four fields chosen to span two research cultures; the numbers describe those
   four (`PREREG-v1.md` §4).
4. **Open-access and retrievability selection.** The frame requires OA *and* successful retrieval;
   32.0 % of the energy-modelling frame was retrievable, with strong publisher skew (`LAERDOM §3`).
5. **Preregistration not externally timestamped before data.** The protocol and addenda are locked in
   git with sha256 and are unchanged, but no external timestamp (OSF or equivalent) precedes data
   collection (`docs/RESULTAT-PORT-v1.md`).
6. **Rule clarifications written after data.** ADDENDUM-10 clarifies three recurring readings after
   the data had been seen. It moved **1 of 48** doubtful cases and shifted precision from 16.0 % to
   16.7 %, within the prior confidence interval (`ADDENDUM-10.md` §4–§5, `LAERDOM §20`).
7. **Recall is the worst-measured end.** The interval on missed true hits spans 110 to 1,405
   (`LAERDOM §16`).
8. **No frontier judge.** The planned second judge was blocked by a free-tier quota, and no weaker
   model was substituted for it (`LAERDOM §6`).

9. **The gold set has a stable core of three.** Of the 27 known true hits in the port material, only
   **three** (PS-044, PS-205, PS-266) have agreement between coder 1 and coder 2 *and* no `tvil` flag
   from either. The components: the two coders agree on 19 of 27; coder 1 flagged **20 of 27** with
   doubt, leaving 7 unflagged; coder 2 leaves 4 unflagged. When a third independent coder, given the
   same rule file and the same blocklist, was asked to re-confirm the 27, it confirmed **21** — and all
   six losses were doubt-flagged passages, four of which were already among coder 2's twelve
   disagreements. Two reading patterns account for all six: "the obstacle belongs to the field or to a
   third party, not to this work" (ADDENDUM-04 §4 applied in the opposite direction) and "answered in
   the same passage", coded as a non-hit. The class distribution reported above is robust across all
   three readings; **a threshold set near the gold set's own margin is not.** This limits what the gold
   set can support: it can carry a finding about which obstacle classes dominate, but it cannot carry a
   pass/fail gate whose threshold sits close to its own stability.

## 8 References

| # | Reference | Verified against |
|---|---|---|
| 1 | Stent, G.S. (1972). Prematurity and Uniqueness in Scientific Discovery. *Scientific American* 227(6): 84–93. doi:10.1038/scientificamerican1272-84 | Crossref |
| 2 | Hook, E.B. (ed.) (2002). *Prematurity in Scientific Discovery: On Resistance and Neglect*. University of California Press. doi:10.1525/9780520927735 | Crossref (chapter DOIs; review in *Isis* 95: 757–758, doi:10.1086/432365) |
| 3 | van Raan, A.F.J. (2004). Sleeping Beauties in science. *Scientometrics* 59(3): 467–472. doi:10.1023/B:SCIE.0000018543.82441.f1 | Crossref |
| 4 | Ke, Q., Ferrara, E., Radicchi, F. & Flammini, A. (2015). Defining and identifying Sleeping Beauties in science. *PNAS* 112(24): 7426–7431. doi:10.1073/pnas.1424329112 | Crossref (abstract quoted) |
| 5 | Sutoyo, E. & Capiluppi, A. (2024). Self-Admitted Technical Debt Detection Approaches: A Decade Systematic Review. arXiv:2312.15020 | arXiv API |
| 6 | Melin, E.L., Eisty, N.U., Watson, G.R. et al. (2026). Self-Admitted Technical Debt in Scientific Software: Prioritization, Sentiment, and Propagation Across Artifacts. arXiv:2603.15883 | arXiv API |
| 7 | Al Azhar, I., Reddy, V.D., Alhoori, H. et al. (2025). LimTopic: LLM-based Topic Modeling and Text Summarization for Analyzing Scientific Articles limitations. arXiv:2503.10658 | arXiv API |
| 8 | Al Azher, I., Mokarrama, M.J., Guo, Z. et al. (2025). FutureGen: A RAG-based Approach to Generate the Future Work of Scientific Article. arXiv:2503.16561 | arXiv API |
| 9 | Xu, Z., Zhao, Y., Patwardhan, M., Vig, L. & Cohan, A. (2025). Can LLMs Identify Critical Limitations within Scientific Research? A Systematic Evaluation on AI Research Papers (LimitGen). arXiv:2507.02694 | arXiv API |
| 10 | Smith, J.J., Amershi, S., Barocas, S., Wallach, H. & Wortman Vaughan, J. (2022). REAL ML: Recognizing, Exploring, and Articulating Limitations of Machine Learning Research. arXiv:2205.08363; ACM FAccT '22 | arXiv API |
| 11 | Wang, Q. et al. (2023). SciMON: Scientific Inspiration Machines Optimized for Novelty. arXiv:2305.14259 | arXiv API |
| 12 | Li, L. et al. (2024). Chain of Ideas: Revolutionizing Research Via Novel Idea Development with LLM Agents. arXiv:2410.13185 | arXiv API |
| 13 | Baek, J. et al. (2024). ResearchAgent: Iterative Research Idea Generation over Scientific Literature with Large Language Models. arXiv:2404.07738 | arXiv API |
| 14 | He, Y. et al. (2025). PaSa: An LLM Agent for Comprehensive Academic Paper Search. arXiv:2501.10120 | arXiv API |
| 15 | InternAgent Team (2025). InternAgent: When Agent Becomes the Scientist — Building Closed-Loop System from Hypothesis to Verification. arXiv:2505.16938 | arXiv API |
| 16 | Tian, Q., Yin, H., Xia, Y., Kong, Y. & Liu, Z. (2026). ForeSci: Evaluating LLM Agents for Forward-Looking AI Research Judgment. arXiv:2606.00644 | arXiv API |
| 17 | Saxton, K.E. & Rawls, W.J. (2006). Soil Water Characteristic Estimates by Texture and Organic Matter for Hydrologic Solutions. *Soil Sci. Soc. Am. J.* 70(5): 1569–1578. doi:10.2136/sssaj2005.0117 | OpenAlex; archived copy sha256 `f092918b…` |

**Removed from the draft.** One system named in the outline, *BAGELS*, could not be traced to any
publication on limitations extraction; searches returned unrelated work in accelerator physics and in
agent bootstrapping. The claim it supported — that extraction of limitations statements is already
established — is carried by references 7–10 and stands without it.
