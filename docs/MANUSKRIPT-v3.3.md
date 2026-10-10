# Declared and undone: an open pipeline for finding self-reported unfinished work in research articles, with a prospective test and an exploratory case series

**Eirik Botten Nicolaysen**
EcoDeco AS, Lillehammer, Norway
Corresponding author: eirik@ecodeco.no · ORCID 0009-0001-9188-6788

---

## Abstract

Research articles often state that part of the reported work was not done and give a reason. We call
such statements parked research questions and ask whether they can be found systematically and what
obstacles they name. We built an open pipeline in which a local language model first filters
passages and a frontier language model, reading whole batches with the coding rules in view, then
reads the remaining candidates. In a development phase on 100
open-access works from four fields, the reader returned 432 candidate rows, or 276 distinct
declarations; among declarations with a majority class, 71.2 % name data that never existed. In a
prospective phase on 100 new archaeology works, with all criteria fixed before sampling, a blind
second reading confirmed 85 of 100 sampled reader positives (work-clustered 95 % interval
76.2–93.8), and the filter retained 95 of 104 statements found by reading 20 works in full
(76.9–96.7). All coders are language models, so these figures measure agreement within a model-based
instrument, not validity against human reading; a human validation study is preregistered. Two model
coders agreed closely on whether a passage is a hit (Cohen's kappa 0.812), and the same model agreed
more with the reference when reading a whole batch than when reading one passage per call (paired
difference 0.177, 0.057–0.318). Six exploratory attempts to reopen declared work, selected by
judgement, found no obstacle removed. The pipeline, registers, protocols and a manifest linking every
number to its source are openly deposited.

**Keywords:** research limitations · unfinished research · large language models · text classification ·
annotation reliability · open science

---

## 1 Introduction

Authors sometimes write that part of their own reported work was not done, and say why. For example:
"we were unable to code all data about discharge diagnosis and insurance status". We call such a
statement a *parked research question*. It is easy to recognise when quoted, but it shares neither
vocabulary nor topic with the text around it. What defines it is its form: an undone part of the
authors' own work, and a stated obstacle.

This raises three questions. Does the statement occur in published text often enough to measure? Can
the obstacles be classified so that those which new tools might remove are separated from those they
cannot? And can such statements be found systematically, with known retention and agreement? A
fourth question — whether particular obstacles have since been removed — motivated the work, but we
address it only through a small exploratory case series.

The paper makes five contributions: (i) an operational definition and a nine-class typology of
obstacles, fixed before any data were read; (ii) an open, reproducible pipeline; (iii) measurements of
how closely language-model coders agree on this task, including the effect of how the reading model
works; (iv) a prospective test of the pipeline on new material, with all criteria fixed in advance;
and (v) a public deposit in which every reported number can be traced to a file, a checksum and the
script that produced it.

## 2 Related work

The closest work concerns limitations in research articles. BAGELS is a benchmark for extracting and
generating limitations from scholarly text (Al Azher et al., 2025), and LimitGen evaluates whether
large language models can identify critical limitations in research papers, using both synthetic and
human-written limitations (Xu et al., 2025). Both deal with *limitations*: weaknesses of a study, as
reported by its authors or identified by a reviewer. Our class is narrower and different in kind. It
requires that the authors declare an *undone* part of their own work and that they give a named
obstacle as the reason, in the same passage. Many limitations do not declare undone work, and many
declarations of undone work appear outside limitations sections; in our material, 81.4 % of passages
carry no section label at all, so section-based retrieval is not possible.

Classifying the rhetorical role of sentences in scientific text is an established task. Language
models have been evaluated for sequential sentence classification against manually annotated corpora
such as biorc800 (Lan et al., 2024), and the SemEval-2021 NLPContributionGraph task structured the
contributions of research papers for a knowledge graph (D'Souza et al., 2021). These studies anchor
model output to human annotation. The present study does not yet do so, and this is its main
limitation (§6).

On language models as annotators, a recent comparison found them effective as assistants to human
annotators but not reliable as independent annotators measured against experts (Gu et al., 2026). We
therefore report agreement among model coders as a property of the instrument, not as evidence of
validity. For agreement on clustered data we use the cluster bootstrap described by Vanbelle (2019).

## 3 Design

### 3.1 Two phases and a case series

The study has two phases of different status, and we report them separately.

**Phase 1: development (100 works).** The protocol, the typology and the unit of analysis were fixed
on 12 September 2026, before any data were read, and recorded with a checksum as the first commit of
the code repository. They were not timestamped by a third party until the first public deposit on 25
September 2026. During phase 1, three rule clarifications were written after data had been seen, the
filter was revised, one acceptance test failed, and a second test was added afterwards. We therefore
report phase 1 as development and exploratory analysis, and give the timing of each test.

**Phase 2: prospective test (100 new works).** The plan for phase 2 was fixed before the sample was
drawn. It specified the sampling frame, the draw, the reference procedure, both acceptance tests and
the analysis. Phase 2 is the confirmatory test of the pipeline. Three deviations occurred; they are
reported in §5.5.

**Case series (exploratory).** Six attempts to reopen a parked question were selected by judgement
from the phase 1 output (§5.7). The criterion for calling an obstacle "lifted" was written after the
six attempts, and the series is descriptive.

### 3.2 Sampling frame and unit

Works were drawn from OpenAlex, publication years 2015–2020, open access with full text that could be
retrieved. Phase 1 drew 25 works from each of four fields — energy modelling, archaeology, clinical
epidemiology and historical textual scholarship — chosen to span the sciences and the humanities.
Phase 2 drew 100 works from the same, frozen archaeology frame, none of them used in phase 1.
Requiring retrievable full text skews the frame towards publishers whose texts can be downloaded.

The unit of reading is a *passage*: a candidate sentence with the two sentences before and after it.
Passages start every third sentence, so neighbouring passages overlap. A passage is a *hit* if it
contains both an undone part of the reported work and an obstacle, and gives the obstacle as the
reason. Because one statement can fall into more than one passage, we report results per register
row and per **distinct declaration**, formed by merging rows from the same work whose sentences
overlap.

### 3.3 Typology

Each hit is assigned to one of nine obstacle classes, fixed before data were read: reading or coding
by people at scale (H1); legibility of a damaged or handwritten source (H2); language (H3); detecting
patterns in large volumes of images or signals (H4); simulation and computing power (H5); inferring
structure from sequences (H6); data that did not exist (H7); access, law, ethics and consent (H8); and
a missing concept or theory (H9). When a passage does not say whether the obstacle was the workload or
the absence of data, the class is *undecided* (H1/H7). Three kinds of non-hit are recorded separately:
the question is answered later in the same article (N1); a claim that something is new (N2); and a
choice of scope with no named obstacle (N3). Whether a class could be lifted by current tools was set
per class in the protocol (H1–H6 liftable, H7–H9 not) and is never decided by a model; the undecided
class is reported separately.

### 3.4 Pipeline

The pipeline runs as a single command, in ten steps: retrieve texts, split into passages, judge,
extract, combine, prepare blind files, read, summarise per work, check citations, and write the
register.

- **Filter.** A small model run locally (`gemma2:9b`, temperature 0, fixed seed) judges each passage
  against the typology and, separately, extracts candidate sentences from each document. Passages
  selected by either route form the candidate set: 2 844 of 22 243 passages (12.8 %) in phase 1 and
  4 107 of 21 361 (19.2 %) in phase 2.
- **Reader.** A frontier model (`claude-opus-5`, Anthropic) reads the candidates in batches of at most
  356, as an *agentic* session: one session holds the full coding rules and the whole batch, and works
  through it with file tools. It is also given a *block list* of project documents it may not open. For
  each passage it returns a verdict, a class and a doubt flag. The verdicts are dated and cannot be
  repeated exactly, because the model has no seed and is updated by its vendor. In phase 2, the model
  identity was verified for each session from the session transcripts.
- **Register.** One row per passage the reader codes as a hit, with class, doubt flag, the filter route
  that selected it, liftability from the protocol table, and the section it came from.

### 3.5 Coders and terminology

All coders are language models. *Coder 1* produced the phase 1 reference reading. *Coder 2* is an
agentic `claude-opus-5` session given the coding rules, a *blind file* (passages without any earlier
verdicts) and the block list. *Coder 4* is a chat session with a different model from the same vendor
(product name Claude Fable 5.1; the underlying model identifier was not recorded), reading the same
blind file with the same rules; seven of its 320 passages were not coded blind.

Because there is no human reference yet, we use the following terms. A *reference-positive* is a
passage that a reference reading coded as a hit. *Agreement* is Cohen's kappa (κ), reported together
with raw agreement, the prevalence- and bias-adjusted kappa (PABAK) and Gwet's AC1. The *confirmation
rate* is the share of sampled reader hits that a separate, blind model session also codes as hits.
*Retention* is the share of reference-positives that pass the filter, and *reader agreement with the
reference* is the share that the reader also codes as hits. None of these is precision or recall
against human reading.

### 3.6 Statistics

The work (article, thesis or book) is the cluster unit. Unless stated otherwise, intervals are 95 %
percentile intervals from a bootstrap that resamples whole works (10 000 replicates, seed 734248)
(Vanbelle, 2019); shares of distinct declarations carry Wilson intervals. Where a passage-level
interval was the original report, it is also given. Differences between agreement coefficients are
tested with a paired bootstrap on the difference.

### 3.7 Use of large language models

Language models were used in two roles. As research instruments, they judged and extracted candidate
passages (local model), read candidates and served as reference coders (frontier models), and executed
steps in the case series under locked instructions; their roles, model identities and agreement are
reported in §3–§5. As writing tools, a large language model (Claude, Anthropic) assisted in drafting
and editing the manuscript text under the author's direction. The author designed the study, wrote
the protocol and every criterion, made every recorded decision, interpreted the results, and revised
and approved the final text. Every number was checked against a hash-anchored fact file, and every
reference against Crossref or a verified URL, before submission. The author takes full responsibility
for the content.

## 4 Human validation (preregistered, not yet run)

A validation study was fixed before any human coding. It specifies a stratified sample of 149
passages from 75 works, drawn after the plan was fixed. The sample covers passages that passed and
failed the filter, reader verdicts with and without doubt, all four phase 1 fields, and phase 2 hits
and misses. The study also fixes a blind file without model output, a codebook written for human
annotators from the coding rules, rules for resolving disagreements, and an analysis plan: agreement
between human annotators, between models and humans, and between models and the resolved reference,
with precision and recall against that reference. Results will be reported in a revision or a
separate paper.

## 5 Results

### 5.1 The statements occur, and most name missing data (phase 1)

The reader returned 432 rows from 60 of the 100 works. Of these, 269 share a sentence with another
row from the same work; merged, they form **276 distinct declarations**. Among declarations with a
majority class, **183 of 257 (71.2 %, 65.4–76.4)** (Wilson) name data that did not exist (H7). Among
decided declarations, **42 of 245 (17.1 %, 12.9–22.4)** (Wilson) fall in a liftable class (H1–H6).
Nineteen declarations had a tied class and are left out of class shares. Counted per row, H7 is 289
of 432 (work-clustered 58.2–79.7) and the liftable share 77 of 406 decided rows (9.0–26.5). These
intervals are wide because a single work contributes 118 rows. Class counts per row: H7 289, H5 50,
H9 29, undecided 26, H2 14, H8 11, H1 10, H3 2, H4 1, H6 0.

The share of filter candidates that the reader codes as hits differs by field: archaeology 274 of 990
(27.7 %), clinical epidemiology 53 of 347 (15.3 %), textual scholarship 37 of 378 (9.8 %) and energy
modelling 68 of 1 129 (6.0 %). The share of passages that become filter candidates also differs
(6.8–17.5 %). These are rates within the filter's output, not the frequency of such statements in each
field, because the filter's retention per field was not measured in phase 1.

### 5.2 Agreement among language-model coders

Coders 1 and 2 both read the same 320 passages, from 92 works; the largest work contributes 33
passages (Table 1).

**Table 1** Agreement on the hit decision between language-model coders, 320 passages

| pair | κ | work-clustered 95 % | raw | PABAK | AC1 | positives |
|---|---|---|---|---|---|---|
| coder 1 – coder 2 | 0.812 | 0.711–0.909 | 96.2 % | 0.925 | 0.953 | 39 / 33 |
| coder 4 – coder 2 | 0.899 | 0.833–0.974 | 98.1 % | 0.963 | 0.977 | 33 / 33 |
| coder 4 – coder 1 | 0.781 | 0.675–0.877 | 95.6 % | 0.912 | 0.945 | 33 / 39 |

Leaving out the seven passages coder 4 did not code blind lowers κ by 0.024–0.025. For the pair coder
1 – coder 2, which never saw those passages before coding, the same exclusion lowers κ by 0.018. The
drop comes from removing reference-positives from a small positive class, and the ranking of the three
pairs does not change.

Agreement on the class, among passages both coders call hits, is lower (coders 1–2: κ 0.722). The
weakest boundaries are two non-hit categories: N3 (κ 0.530) and N2 (κ 0.535). On the same passages, the
three coders recorded N3 54, 34 and 13 times. A decision rule for N3 has since been written, but its
effect has not been measured. Of the 27 phase 1 reference-positives, only 3 are coded as hits by both
coders without a doubt flag.

### 5.3 How the reader works matters

When each passage is sent to the model in a separate call with the full coding rules, agreement with
coder 1 rises with model capability: Haiku 4.5 κ 0.031, Sonnet 5 κ 0.294, Opus 5 κ 0.636
(0.503–0.744). The same Opus model working as an agentic session, with the rules and a whole batch of
passages, reaches κ 0.812. The paired difference, 0.177, has a work-clustered interval of
**0.057–0.318**, which excludes zero. A small local model (7B) working agentically reached κ 0.248, so
the way of working alone does not close the gap.

### 5.4 Acceptance tests in phase 1

The preregistered test required a third reading of the candidate set to confirm at least 22 of the 27
reference-positives. It confirmed 21, so the test failed. All six that were lost had been marked as
doubtful by the reference coder, and the threshold (81 %) had been set above the agreement between
the two reference coders themselves (19 of 27, 70.4 %). A second test, written after the first had
failed, drew 100 reader hits for blind confirmation: **85 of 100 (work-clustered 75.7–92.3; 33 works,
largest 21 rows)**. The phase 1 list is therefore called a candidate list.

### 5.5 Phase 2: prospective test

Before the filter was run, 20 of the 100 new works were read in full by twenty agentic reference
sessions, one per work, each starting with an empty context and given the coding rules and the block
list. The resulting key was stored with its checksum before the filter started. The reference reading
found **104 reference-positives in 12 of the 20 works; one work holds 51** (Table 2).

**Table 2** Prospective phase: confirmation, retention and reader agreement

| measure | value | work-clustered 95 % |
|---|---|---|
| confirmation rate (100 sampled reader hits, 38 works) | 85 / 100 | 76.2–93.8 |
| retention by the filter | 95 / 104 (91.3 %) | 76.9–96.7 |
| reader agreement with the reference | 85 / 104 (81.7 %) | 60.9–89.7 |
| retention, excluding the work with 51 hits | 45 / 53 (84.9 %) | — |
| reader agreement, excluding that work | 38 / 53 (71.7 %) | — |

Confirmation depends on the reader's doubt flag: 37 of 38 hits without doubt were confirmed, against
48 of 62 with doubt (a post hoc subgroup). The reader returned 673 rows from 73 of the 100 works, which
merge into **424 declarations**. Among declarations with a majority class, H7 is **265 of 402 (65.9 %,
61.2–70.4)** (Wilson), and among decided declarations the liftable share is **53 of 375 (14.1 %,
11.0–18.0)** (Wilson). The reader used 118 185 context tokens per hit (phase 1: 164 805).

The confirmation test (threshold 0.70) was passed, and the phase 2 list is called a worklist under a
prospective test. Retention and reader agreement were reported without a threshold, as planned. Three
deviations occurred. The order "reference before filter" was enforced by procedure when the filter
started and by code from later the same day. The register step was corrected after the plan was
fixed; the content of the rows did not change, checksum for checksum. Two reader sessions reached a
usage limit and were completed in a second session without rewriting any verdict.

### 5.6 A secondary estimate of how often the statements occur (phase 1)

Weighting the strata of the 320-passage reading — filter-flagged passages by field and judged class,
and unflagged passages by judged non-hit category — gives 760 expected reference-positive passages,
**3.42 % of all passages (work-clustered 1.3–7.5)**. The estimate rests on 2 positives among 100
unflagged passages that were read, and on one assumption: strata with no read passages take the rate
of their field. It describes reference-positive passages in this sampling frame, not frequency in the
literature at large.

### 5.7 Exploratory case series

**Selection.** Case A was chosen on 21 September 2026 from the four phase 1 reference-positives in a
liftable class, as the only one whose input data were available. Cases B–F were chosen on 27 September
from the 50 phase 1 rows in a liftable or undecided class without a doubt flag. These rows were grouped
into 19 cases (one per work and obstacle); 10 were set aside because they would require physical
material, fieldwork or people; and a short list was made of those for which a criterion could be fixed
in advance and the needed resource seemed to exist. Every step after the first was a judgement. The
series therefore favours cases where reopening looked feasible, and it cannot show how often any type
of obstacle prevents reopening.

**Outcomes.** "Lifted" was defined afterwards by three conditions: the resource named as missing now
exists in an open source; the original study's own numbers can first be reproduced; and a criterion
fixed before computation is met. Criteria were fixed before computation for cases A, B and C (Table 3).

**Table 3** Exploratory reopening attempts

| case | work | obstacle | outcome |
|---|---|---|---|
| A | Pring (2016) | H5, model would not accept measured density | not lifted; model inconsistency reproduced for the four horizons named |
| B | Haouachi (2016) | H3, Greek sources read only in translation | not lifted; 79 of 90 places resolved to open Greek text (87.8 %, threshold 90 %) |
| C | Rodrigues Aragao (2018) | H5, tool could not force equal partitions | not lifted by the named means; the named package (Žiberna, 2018, 2025) lacks the mechanism |
| D | Rodrigues Aragao (2018) | interview material for automatic concept-network generation | stopped: material withheld under consent |
| E | Riris (2018) | H5, model runs split for time | stopped: model code not found in six checked routes; one route unresolved |
| F | Bynum et al. (2021) | H5, full scenario enumeration | stopped: scenario set and distribution parameters not reported |

In case B, the denominator used is 90 places; a narrower citation form gives 55 of 60 (91.7 %), which
we report as a post hoc sensitivity analysis. Two of eight references that could be checked point to a
different passage from the one cited in the thesis. Both open text services returned HTTP status 200
with a different passage when the requested one did not exist; without comparing the returned address
with the requested one, all eleven misses would have been counted as resolved. In case C, the values
reported in the thesis were reproduced exactly (12 of 12), and its total error of 14 was reproduced in
two independent implementations. The thesis's own workaround is a constrained solution with a lower
error (14) than the best constrained solution found from 120 random starts (18). In case F, the
article's statement that 100 scenarios cover less than 0.001 % of the space was confirmed (C(41,7) =
22 481 940; 0.000445 %), with the 41 lines of MATPOWER's case30 (MATPOWER, n.d.; Zimmerman et al.,
2011).

For three further parked items (Hansen et al., 2019; Karatas, 2018; Mecking et al., 2017), the citation
graph since publication shows no later work doing what was declared undone.

## 6 Discussion

**What the evidence supports.** Statements of undone work can be retrieved at scale with an open
pipeline, and the pipeline behaved consistently in two applications: confirmation rates of 85 of 100
in both phases, filter retention above 90 % against full reading in phase 2, and close agreement
between model coders on the hit decision. Among declarations with a majority class, between 66 % and
71 % in the two phases name data that never existed — an obstacle that later analytical tools cannot
supply. In the exploratory series, no obstacle was shown to have been lifted.

**What it does not support.** None of these figures establishes validity against human reading. Every
coder and reference reader is a language model; the phase 2 reference and the reader share vendor and
coding rules; and model coders can agree while sharing the same errors (Gu et al., 2026). The phase 2
retention estimate is dominated by one work and has a wide interval. The case series was selected by
judgement and favours feasible cases. That three of the six stopped because input was unavailable is
an observation about these six, not an estimate of how often access prevents reopening, and the series
contains no comparison with model capability.

**The reader.** The gap between batch reading and one-passage-per-call reading by the same model,
together with the poor result of a small local model working the same way, suggests that for this task
the reader must be both capable and given the rules and the context together. Anyone reproducing the
pipeline faces this constraint.

**Relation to research on limitations.** Declared undone work with a named obstacle overlaps with the
limitations studied in BAGELS and LimitGen, but it is neither a subset nor a superset of them: it
requires an undone component and a stated reason, and it is spread throughout articles rather than
confined to limitations sections. A direct comparison on a shared corpus is left for future work.

## 7 Limitations

1. There is no human annotation yet; a validation study is preregistered (§4).
2. All coders are language models. Coder 4's underlying model identifier was not recorded, and coders
   1 and 2 and the phase 2 reference readers share vendor and coding rules.
3. Phase 1 is development and exploratory analysis. The protocol was not timestamped by a third party
   before data were read, and three rule clarifications were written after data.
4. "Lifted" was defined after the case series, which is exploratory and selected by judgement.
5. Phase 1 covers four purposively chosen fields and phase 2 one field; both are limited to open-access
   texts that could be retrieved, which skews them by publisher.
6. Filter retention was measured only in phase 2, on 20 works, one of which holds half the
   reference-positives.
7. Reader verdicts are dated and cannot be repeated exactly.
8. Whether an obstacle can be assessed without a domain expert was not operationalised; two readings
   within the protocol's wording gave 88 % and 32 %.

## 8 Conclusion

Statements in which authors declare part of their own work undone, and name the obstacle, can be
retrieved from research articles with an open pipeline that behaved consistently across a development
phase and a prospective test. In the fields studied, most of these statements name data that were never
collected. Whether the agreement figures hold against human reading is the next question, and the
study to answer it is fixed in advance.

## Statements and Declarations

**Competing interests.** The author is the founder and CEO of EcoDeco AS, which developed the pipeline
as open-source software; the author has no other relevant financial or non-financial interests.

**Funding.** No funding was received for conducting this study.

**Ethics approval and consent.** Not applicable: the study analyses published text and involved no
human participants.

**Author contributions.** EBN: conceptualisation, methodology, software design, analysis, writing and
approval of the final text (use of language models is described in §3.7).

**Data and code availability.** Code is Apache-2.0 at https://github.com/avalyset/gjenopptak. Own data are CC BY 4.0; third-party text
is not redistributed. The deposit (concept DOI 10.5281/zenodo.22959326; version v0.5.0 for this
manuscript, 10.5281/zenodo.23120143) contains the protocol and all addenda with lock hashes and OpenTimestamps receipts (Todd, 2024), the
rule files and block lists every locked measurement read, blind files and both registers as indices
(work identifier, sentence span, text hash, class, doubt, sieve provenance; no passage text), the
phase 2 measurements and reference key, the reanalysis output, the case files, and a number manifest
that links each number in this paper to its file, hash and generating script.

## References

Al Azher, I., Mokarrama, M. J., Guo, Z., Ray Choudhury, S., & Alhoori, H. (2025). BAGELS:
Benchmarking the automated generation and extraction of limitations from scholarly text. In
*Findings of the Association for Computational Linguistics: EMNLP 2025* (pp. 19279–19294).
https://doi.org/10.18653/v1/2025.findings-emnlp.1050

Botten Nicolaysen, E. (2026). *Gjenopptak: Declared-and-undone work in research articles* (Version
0.5.0) [Data set and software]. Zenodo. https://doi.org/10.5281/zenodo.23120143

Bynum, M., Staid, A., Arguello, B., Castillo, A., Knueven, B., Laird, C. D., & Watson, J.-P. (2021).
Proactive operations and investment planning via stochastic optimization to enhance power systems'
extreme weather resilience. *Journal of Infrastructure Systems*, *27*(2), Article 04021004.
https://doi.org/10.1061/(ASCE)IS.1943-555X.0000603

D'Souza, J., Auer, S., & Pedersen, T. (2021). SemEval-2021 Task 11: NLPContributionGraph —
Structuring scholarly NLP contributions for a research knowledge graph. In *Proceedings of the 15th
International Workshop on Semantic Evaluation* (pp. 364–376). https://doi.org/10.18653/v1/2021.semeval-1.44

Gu, F., Li, Z., Colon, C. R., Evans, B., Mondal, I., & Boyd-Graber, J. L. (2026). Large language models
are effective human annotation assistants, but not good independent annotators. In *Findings of the
Association for Computational Linguistics: ACL 2026* (pp. 71–89). https://doi.org/10.18653/v1/2026.findings-acl.4

Hansen, S., Montero-Ruiz, I., Rovira, S., Steiniger, D., & Toderaş, M. (2019). The earliest lead ore
processing in Europe. 5th millennium BC finds from Pietrele on the Lower Danube. *PLOS ONE*, *14*(4),
Article e0214218. https://doi.org/10.1371/journal.pone.0214218

Haouachi, D. (2016). *Les personnages féminins chez Tite-Live : idéologie et art de la mise en scène*
[Doctoral dissertation, Université de Strasbourg]. https://doi.org/10.70675/8513d3c9ze385z4b4bz910cz221c7718984d

Karatas, A.-M.-S. (2018). The significance of money for the cults and sanctuaries of Demeter and Kore:
The shaping of the cults by commercial transactions. *Mythos*, *12*, 47–88.
https://doi.org/10.4000/mythos.297

Lan, M., Zheng, L., Ming, S., & Kilicoglu, H. (2024). Multi-label sequential sentence classification via
large language model. In *Findings of the Association for Computational Linguistics: EMNLP 2024*
(pp. 16086–16104). https://doi.org/10.18653/v1/2024.findings-emnlp.944

MATPOWER. (n.d.). *case30.m* [Data set]. GitHub. Retrieved September 28, 2026, from
https://raw.githubusercontent.com/MATPOWER/matpower/master/data/case30.m

Mecking, O., Hohle, I., & Wolfram, S. (2017). The development of pottery technology in Eythra from the
Early Linear Pottery culture to the Late Stroke Ornamented Pottery culture. *Archeologické rozhledy*,
*69*(2). https://doi.org/10.35686/ar.2017.12

Pring, L. J. (2016). *Soil-based analysis methods to aid the detection of cropmarks over buried
features* [Doctoral dissertation, University of Birmingham]. https://etheses.bham.ac.uk/id/eprint/7069/

Riris, P. (2018). Assessing the impact and legacy of swidden farming in neotropical interfluvial
environments through exploratory modelling of post-contact Piaroa land use (Upper Orinoco, Venezuela).
*The Holocene*, *28*(6), 945–954. https://doi.org/10.1177/0959683617752857

Rodrigues Aragao, R. (2018). *Using network theory to manage knowledge from unstructured data in
construction projects: Application to a collaborative analysis of the energy consumption in the
construction of oil and gas facilities* [Doctoral dissertation, University of Toronto].
https://hdl.handle.net/1807/92034

Todd, P. (2024). *opentimestamps-client* (Version 0.7.2) [Computer software]. Python Package Index.
https://pypi.org/project/opentimestamps-client/0.7.2/

Vanbelle, S. (2019). Asymptotic variability of (multilevel) multirater kappa coefficients.
*Statistical Methods in Medical Research*, *28*(10–11), 3012–3026. https://doi.org/10.1177/0962280218794733

Xu, Z., Zhao, Y., Patwardhan, M., Vig, L., & Cohan, A. (2025). Can LLMs identify critical limitations
within scientific research? A systematic evaluation on AI research papers. In *Proceedings of the 63rd
Annual Meeting of the Association for Computational Linguistics* (pp. 20652–20706).
https://doi.org/10.18653/v1/2025.acl-long.1009

Žiberna, A. (2018). *blockmodeling* (Version 0.3.1) [Computer software]. CRAN.
https://cran.r-project.org/src/contrib/Archive/blockmodeling/

Žiberna, A. (2025). *blockmodeling: Generalized and classical blockmodeling of valued networks*
(Version 1.1.8) [Computer software]. CRAN. https://CRAN.R-project.org/package=blockmodeling

Zimmerman, R. D., Murillo-Sanchez, C. E., & Thomas, R. J. (2011). MATPOWER: Steady-state operations,
planning, and analysis tools for power systems research and education. *IEEE Transactions on Power
Systems*, *26*(1), 12–19. https://doi.org/10.1109/TPWRS.2010.2051168
