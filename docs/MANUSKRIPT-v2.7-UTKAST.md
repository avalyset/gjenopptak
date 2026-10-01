# Declared and undone: an open tool for finding work that researchers report leaving unfinished, and a test of whether the named obstacles can be lifted

**Manuscript v2.7 — draft of 30 September 2026, revised after the sixth fact-check (`d118f50`).**
Written from `docs/MANUSKRIPT-FAKTA-2026-09-28.md` as at commit `f4fb54a`, whose §9 carries the
phase 3 numbers with path and sha; earlier sections were revised after fact-checks `136d025`,
`b084ba2`, `faaaddc`, `c4d645c` and `ffeaccf`. Numbers the fact file does not carry are
marked *(source: …)* where they first occur, each naming the project document it comes from. Those
documents are in the repository, on the project's archive volume, or in a deposited version as
stated at each mark and in §7; the currently deposited version (v0.3.0) does not contain all of
them, and v0.4.0 is not yet published. Not for circulation until the fact-check pass (CC) has been
run against this file, including the phase 3 numbers.

**Author:** Eirik Botten Nicolaysen, EcoDeco AS, Lillehammer, Norway. ORCID 0009-0001-9188-6788.
**Code and materials:** https://github.com/avalyset/gjenopptak · concept DOI 10.5281/zenodo.22959326
(cite the concept DOI; version DOIs identify a specific state). Protocol PREREG-v1 locked internally
12 September 2026 (sha256 `05988b23…`; *source: PREREG-v1 header and repository history*); see §6 on
timestamping.

---

## Abstract

Researchers routinely write down work they did not do and name the obstacle: data that were never
collected, a manuscript they could not collate, a model that would not accept a measured parameter. We
ask whether such passages can be found systematically in published text, what kinds of obstacle they
name, and whether any of those obstacles can be lifted today. We preregistered a protocol, drew 100
open-access works (2015–2020) from four purposively chosen fields, split them into 22 243 passages,
and built an open pipeline: a local sieve (a 9B-parameter judge and a per-document extractor, taken in
union), an agentic frontier-model reader, and a register. A blind reading of 320 passages by a second
coder gave κ = 0.812 [0.697–0.906] on the hit decision; a third coding by a model of a different family
gave κ = 0.899 [0.808–0.969] against the second coder. Among candidate rows, roughly two thirds name
an obstacle the protocol classes as not liftable by current tools: the data never existed (H7 = 289
of 432 candidate rows, 66.9 % [62.3–71.2]); liftability is a dated assessment. The pipeline produced a candidate list of 432 rows from 60 works
that a separate blind reading agreed with in 85 of 100 sampled rows [76.7–90.7]; a preregistered gate
on 27 known hits was not met (21 of 27 against a threshold of 22) and that list is therefore a
candidate list. A second run on 100 new archaeology works, with the chain as locked before the draw
and both gates fixed before anything was read, met its precision gate (85 of 100 [76.7–90.7] against 0.70) and gave
the first measured recall: the sieve retained 95 of 104 hits found by reading 20 of the works
cover-to-cover before the run (91.3 % [84.4–95.4]), and the reader confirmed 85 of the 104 (81.7 %
[73.2–88.0]); that list is a worklist under a prospective gate. We then attempted to reopen six candidates: reproduce the source's
own numbers first, then execute the undone step against a criterion fixed in advance. Three cases
reached a locked criterion; three stopped earlier because the input needed was not available to us:
interview profiles withheld under consent, model code not found in six checked routes, a scenario
set not reported. None of the six obstacles was lifted. Only one case reached a numerical threshold:
79 of 90 Greek source passages cited only in translation were resolved to open Greek text
(87.8 % [79.4–93.0], threshold 90 %); of the 11 places where the thesis gives its own French
rendering, 9 could be read against the original, and two of eight checkable citations point to a
different passage than the one cited.
On this material, what limits the reopening of declared-undone work is access and consent, not
model capability. All coders are language models; no human annotator has read the material, and the
reader's verdicts are dated and not repeatable. We report the tool, the negative result, and the
measurement properties of LLM coders as the contribution.

---

## 1 Introduction

A parked research question is a specific speech act: an author states that a part of the reported
work was not done, and gives a reason. The sentence is easy to recognise when quoted — "we were
unable to code all data about discharge diagnosis and insurance status", "these manuscripts came to
my attention too late to be examined and collated" — and hard to find at scale, because it shares no
vocabulary and no topic with its neighbours. The class is defined by form, not by subject.

Three claims are worth testing about this class. First, that it exists in printed text in
measurable quantity. Second, that some fraction of the named obstacles have since been removed — by
new data, new instruments, or new computational capability, including language models. Third, that
the subset can be found systematically rather than by chance.

The study reported here was preregistered (PREREG-v1, 12 September 2026) with a nine-class typology
of obstacles fixed before any article was read: human reading or coding at scale (H1), legibility of
a damaged or handwritten source (H2), a language barrier (H3), pattern detection in images or signals
at volume (H4), simulation and compute (H5), structural inference from sequence (H6), data that did
not exist (H7), access, law, ethics and consent (H8), and a missing concept or theory (H9). Three
non-hit forms that resemble hits are counted separately: a question answered in the same article
(N1), a novelty claim (N2), and a scope choice with no named obstacle (N3). Liftability by current
tools was assigned per class in the protocol, before data, and is never derived from a model.

We report (i) the class distribution on the 60 of 100 works that yielded candidate rows, (ii) the
reliability of language-model coders on this task, (iii) the pipeline and its measured properties,
(iv) six reopening attempts, three of them against a criterion locked before computation, and (v)
what the results say about the second claim. The third claim — that the subset can be found
systematically — is answered prospectively in §4.7.

---

## 2 Materials

### 2.1 Frame and sample

The frame is OpenAlex, publication years 2015–2020, open access with retrievable full text, in four
fields chosen to span the natural sciences and the humanities: energy modelling, archaeology,
clinical epidemiology, and historical textual scholarship. Twenty-five works were drawn per field
(100 in total), by sequential draw in seed order (ADDENDUM-09). The retrievability requirement makes
the frame skewed by delivery format rather than by business model: publishers that block download
fall almost entirely out of the frame regardless of their access model (ADDENDUM-08; the per-format
retrievability shares are reported in ADDENDUM-03 and are not restated here).

### 2.2 Unit of observation

The unit is the passage: a candidate sentence with two sentences of context on each side
(ADDENDUM-03); the stride of three sentences between passages is a property of the pipeline code,
in place from 16 September 2026 *(source: repository history)*, not of the protocol. A hit requires that the undone and the obstacle both lie inside the
passage *and* are linked — the obstacle must be given as the reason, not merely be nearby — and that
the undone belongs to the work the article reports (ADDENDUM-04). The 100 works yield **22 243
passages** (`data/port/spesifikasjon.json`).

### 2.3 Reference readings and the "known hits"

Three numbers are easy to confuse and are kept apart throughout.

- **25** true hits were found by a blind reading of 320 passages, among the **150 judge-flagged**
  passages that were read. This is the reference set for recall loss *relative to the judge*.
- **27** known hits in the port material: the 25 plus two (PS-257, PS-300) that the extractor found
  and the judge did not. This is the denominator of the preregistered gate (§4.4).
- **30** rows in register v1, the first coder's confirmed hits.

The 320 also carried two true hits among non-flagged strata (the judge's own misses, measured
separately) and 20 anchor passages with known status from earlier recall sets (12 hits, 8 non-hits;
*source: METODE §2*), which belong to the seed material and are excluded from recall measurements.

What this reference set can measure is recall loss for a new method relative to the judge, comparably
between methods because the 25 are the same. What it cannot measure is (a) precision of a new method
— the 25 were found among the judge's flags and are not a random sample; (b) absolute recall — both
numerator and denominator are judge-conditioned; (c) prevalence. Wherever we write "21 of 25" it
means 21 of the 25 the judge found and we confirmed, not 21 of all hits in the material.

### 2.4 Coders

All coders in this study are language models. **Coder 1** produced the reference readings. **Coder 2**
was an agentic Claude Code instance on `claude-opus-5`, given a rule file assembled verbatim from six
protocol sections (9 805 bytes, sha256 `234695dd…`) and a blind file of 320 passages with only an
identifier and the text, in a shuffled order, with an explicit block list. The rule file was not
versioned at the time and was recovered from the session transcript on 27 September; its identity was
established by three independent checks *(source: ADDENDUM-11 §8)* and it is prepared for deposit
with v0.4.0. **Coder 4**
(28 September) is Fable 5.1 in a chat interface — a different model family; no model identifier
beyond the product name was recorded — reading the same 320 passages with the same rule file in the
same order. Seven of the 320 rows were not coded blind *(source: METODE, coder-4 note and
`koder4/eksponerte-rader.json`)*: one had been seen verbatim with the reader's class label the day
before, four shared two sentences with a labelled passage, and two were known to coder 4 by
identifier from the project's own documents; the sensitivity is reported in §4.2.

No human annotator has read the material.

---

## 3 Methods

### 3.1 Preregistration and locks

The protocol was locked internally on 12 September 2026 with a sha256 as its first commit. It was
corrected through numbered addenda, locked as separate commits; from ADDENDUM-05 onward each lock
triggers an archived bundle of the full git history (the protocol and ADDENDUM-01 to -04 predate the
bundle mechanism; one lock commit, `e92620b`, carries two files; *source: repository history and
the bundle directory listing*). Three rule clarifications were written after data (ADDENDUM-10) and
moved one of 48 doubtful cases. The protocol was not timestamped by a third party before data were
read. The first third-party guarantee of any lock is the Zenodo deposit of 25 September 2026
*(source: ZENODO.md)*; OpenTimestamps attestations obtained on 28 September 2026 *(source:
TIDSSTEMPEL.md)* prove that the bundles existed by that date, not earlier, and are prepared for
deposit with v0.4.0.

### 3.2 The pipeline

The tool runs as one command in ten steps: retrieve → passages → judge → extract → union → blind
files and reader assignment → read → work-level assessment → citation falsification → register
(ADR-0012, ADR-0014).

- **Judge.** `gemma2:9b`, temperature 0, seed 734248, `num_ctx` 8192, one call per passage, output
  constrained to the typology, a signature per verdict. It flagged **2 173** of 22 243 passages.
- **Extractor.** The same model reads each document in windows of about 3 000 tokens *(source:
  ADDENDUM-16)* and quotes sentences in
  which the authors state their own undone work with a reason. **884** quoted lines from 598
  windows, 124 windows returning none.
- **Union.** Flagged passages ∪ passages containing a quoted line, with an all-hits join between
  quotes and overlapping windows: **2 844** candidates, covering **27 of 27** known hits. The join
  rule was a correction: a first-hit join gave 2 581 and 26 of 27, because one quote lay in two
  overlapping windows. On the first 100 works, recall of the sieve beyond the 27 is *not measured*
  — the 27 are the sieve's own output — and the register schema admits only the value "not
  measured" for it. The first measured recall is reported in §4.7.
- **Reader.** An agentic Opus instance per batch of at most 356 passages *(source: ADDENDUM-22)*,
  with the coder-2 rule file
  and block list, run serially with its own scratch directory. Reader verdicts are dated and not
  repeatable: the reader has no seed and is updated by its vendor; each verdict carries a model
  signature.
- **Register.** One row per hit with class, doubt flag, sieve source and its measured precision,
  dated liftability from the protocol table, section provenance, and a non-prose flag. The schema
  reserves fields for the work-level assessment and for citation-falsification coverage; in the
  candidate list reported here the work-level field is absent and citation coverage is recorded as
  "not measured" on all rows. The header carries the gate the list has passed and a naming policy:
  evaluative statements address the work, not the person.

### 3.3 Reliability

Cohen's κ with paired bootstrap, 10 000 replications, seed 734248, on the hit decision over all 320
passages and over the 300 non-anchor passages; class κ among passages both coders call hits.

### 3.4 Gates

Two gates were set. The **preregistered gate** (ADDENDUM-22): a third, independent coder reading the
union must confirm at least 22 of the 27 known hits. The **post hoc gate** (ADDENDUM-23, written after
the first fell): 100 random rows the reader called hits (seed 734248) read blind by a separate
instance, threshold 70 %. The list is named by the gate it passed.

### 3.5 Reopening procedure

"Lifted" had no definition before 28 September 2026. ADR-0013, written after the six cases, gives
three conditions and maps the cases onto them retrospectively: (i) the named resource exists in an
open source on date D; (ii) the source's own numbers can be reproduced first; (iii) a criterion
locked before computation is met. Three of the six cases (PS-246, SAK-14, SAK-09b) reached condition
(iii) and have a criterion file whose sha256 was fixed before computation; the other three were
closed at condition (i) or (ii) and never had a criterion locked, because a criterion that cannot be
run is not locked. A case that fails to reproduce the source's own numbers is stopped and recorded;
substituting our own data would replace the source's numbers with ours.

---

## 4 Results

### 4.1 The class exists, and the obstacles are skewed

On the 100 works the base rate can be stated three ways, and only one should be used. Confirmed hits
over all passages, 25/22 243 = 0.112 % (one per 890), measures the reading sample, not the material.
Judge precision times flagged over all passages, 0.1667 × 2 173 = 362, gives 1.63 % [1.13–2.29], a
floor. Dividing the floor by the implied recall of the judge, 362/0.475 = 763, gives **3.43 % [2.12–
7.95]**, one hit per 29 passages — the best estimate, with a wide interval that is dominated by the
uncertainty in the judge's misses.

Of the 432 candidate rows, **289 are H7** — the data did not exist — 66.9 % [62.3–71.2]; H7–H9
together, the classes the protocol marks as not liftable, are **329 of 432 = 76.2 % [71.9–79.9]**.
The liftable classes H1–H6 are **77 of 406 decided rows = 19.0 % [15.4–23.1]**; the undecided share
(class `H1/H7-uavklart`, the passage does not say whether the obstacle was workload or missing data)
is **26 of 432 = 6.0 % [4.1–8.7]**, reported separately and never folded into either. Class counts: H7
289, H5 50, H9 29, undecided 26, H2 14, H8 11, H1 10, H3 2, H4 1. ADDENDUM-22 §9.3 reports
69/374 = 18.4 % for the liftable share and 253/374 = 67.6 % for H7 on the 2 481 of 2 844 passages
judged when it was written; the figures here are from the finished register (432 rows), and the
liftable share additionally uses decided hits as its denominator (ADDENDUM-05 §4).

The hit rate differs by field by a factor of 4.6 over the 2 844 judged passages, and the intervals
for the extremes do not come near each other: archaeology 274/990 = 27.7 % [25.0–30.5], clinical
epidemiology 53/347 = 15.3 % [11.9–19.4], textual scholarship 37/378 = 9.8 % [7.2–13.2], energy
modelling 68/1 129 = 6.0 % [4.8–7.6].

### 4.2 Reliability of language-model coders

| comparison | n | raw agreement | κ | 95 % CI |
|---|---|---|---|---|
| coder 1 vs coder 2, all 320 | 320 | 96.2 % | **0.812** | 0.697–0.906 |
| coder 1 vs coder 2, non-anchor | 300 | 96.7 % | 0.774 | 0.623–0.898 |
| coder 1 (first reading) vs coder 2 | 320 | 96.6 % | 0.826 | 0.712–0.917 |
| coder 4 vs coder 2, all 320 | 320 | — | **0.899** | 0.808–0.969 |
| coder 4 vs coder 1, all 320 | 320 | — | 0.781 | 0.659–0.883 |

Seven of the 320 rows were not coded blind by coder 4 (§2.4); excluding them gives 0.874 against
coder 2 and 0.757 against coder 1, and the ordering coder 4–2 > coder 1–2 > coder 4–1 holds
in every subset. The intervals overlap, so the ordering is not established; the direction is opposite
to what a model-family caveat would predict — a model from a different family reproduces coder 2's hit
decision at least as well as coder 1 does.

Agreement is high on the hit decision and much lower on the reference set's *stable* part. Coders 1
and 2 agree on hit status for 19 of 27 known hits; only 7 of 27 are without a doubt flag by coder 1
and 4 of 27 by coder 2; the set on which both agree *and* neither is in doubt is **3 of 27** (PS-044,
PS-205, PS-266). Coder 1 marked 20 of 27 with doubt. This is a property of the agreement between two
language-model coders without doubt marks, not of the passages. The consequence for design is that
the reference set can carry a finding about class distribution but cannot carry a threshold near its
own edge — which is what the preregistered gate turned out to be (§4.4).

Class agreement is weaker than hit agreement for every pair, and the weakest boundary is a non-hit
class: N3, the scope choice without a named obstacle, was counted 54, 34 and 13 times by the three
coders on the same 320 passages, with class κ for N3 between coders 1 and 2 of 0.530 and overall
class κ of 0.722 *(source: METODE, class-reliability section; REGEL-N3-v1)*.
The boundary has since been written as an explicit, versioned decision rule with anchor examples
(`REGEL-N3-v1`); the rule has not been applied to the 320 passages, so its effect on agreement is
not measured.

### 4.3 Which model can read

With the same rule file and the same call structure — one call per passage — the hit-decision κ
against coder 1 rises monotonically with model capability, and the intervals for the two ends do not
overlap:

| reader | κ vs coder 1 | 95 % CI | flagged |
|---|---|---|---|
| Haiku 4.5 | 0.031 | −0.024–0.129 | 3 |
| Sonnet 5 | 0.294 | 0.126–0.455 | 14 |
| Opus 5, one call per passage | 0.636 | 0.478–0.768 | 21 |
| Opus 5, agentic, one continuous session (coder 2) | 0.812 | 0.697–0.906 | — |

Opus in one call is precise but loses half: 20 of coder 1's 39 hits found, 19 missed, one false
positive, 280 agreed non-hits. The difference between 0.636 and 0.812 is **not statistically
established** — the intervals overlap in 0.697–0.768 — so the contribution of the session form is not
demonstrated. A local 7B model run agentically (rule file plus batches of 20 passages in one context)
reached 0.248 [0.113–0.376] (ADDENDUM-24): mode alone does not close the gap. Giving Haiku the full
rule file made it worse (κ 0.047 against 0.270 with a short excerpt; paired difference −0.222
[−0.402 – −0.044]); Opus uses the same rules to 0.636, so this is a property of the smaller model, not
of the rules. Output truncation at 300 tokens affected two earlier runs. An Opus run at κ 0.390,
with 36 of 320 answers cut and 27 of coder 1's 39 hits among them, is invalid; it is kept, marked
invalid, and not used. A Sonnet run with a short rule excerpt had 12 answers cut; those were re-run
and the corrected value, 0.297 [0.125–0.456], n = 319, is the one cited.

### 4.4 The candidate list

The reader produced **432** hit rows over the 2 844 candidate passages, covering **60** distinct works;
40 of the 100 works yielded no row. 218 rows carry no doubt flag and 214 do; 260 came from the judge
alone, 124 from both sieve sources, 48 from the extractor alone; 11 (2.5 %) are flagged non-prose.

Sieve precision is measured per source, not per obstacle class: both sources 0.345 [0.298–0.396],
judge alone 0.143 [0.128–0.160], extractor alone 0.072 [0.054–0.094]; the sieve as a whole 432/2 844
= 15.2 %. The cost unit is frontier reads per confirmed hit, about six for the judge (2 173 flagged /
362 expected true).

**The preregistered gate fell.** The reading confirmed 21 of the 27 known hits against a threshold of
22. All six losses were doubt-marked passages, four of them already among coder 2's disagreements
with coder 1. The threshold was not moved. The list is therefore a **candidate list, permanently**.
In retrospect the threshold, 22 of 27 (81 %), was set above the agreement the two reference coders
have with each other (coder 2 confirmed 19 of the 27 known hits, 70.4 %); a gate on a reference set
should be set at the set's own inter-coder agreement, not above it.

**The post hoc gate held.** Of 100 random hit rows read blind by a separate instance, **85 were
confirmed [76.7–90.7]**, with class agreement in 74 of 85 (87.1 %). The reader's own doubt flag
separates the sample sharply: 41 of 42 confirmed where the reader was not in doubt (97.6 %), 44 of 58
where it was (75.9 %). This is a post hoc subgroup; no other predictor was compared and the difference
is not tested. One deviation from the gate's text must stand: the gate specified a single separate
instance, and two were used — 85 plus 15 — after the first was interrupted; the 85 are a contiguous
prefix, not a sample.

### 4.5 Six reopening attempts, none lifted

| case | work | class | outcome | deciding number |
|---|---|---|---|---|
| PS-246 | Pring 2016, W2551114598 | H5 | **not lifted** (25 Sept.) | the model inconsistency (FC > θS) reproduced for exactly the four horizons the thesis names; the horizon-level outcome is in the case file |
| SAK-14 | Haouachi 2016, W2474595476 | H3 language | **not lifted** | 79 of 90 = 87.8 % [79.4–93.0] vs 90 % |
| SAK-09b | Aragao 2018, W7133020405 | H5 tool limit | **not lifted by the named means** | `blockmodeling` 1.1.8 has no mechanism to bind the two partitions; in our own implementation, unconstrained partitions were equal 0 of 120 times |
| SAK-09c | Aragao 2018, W7133020405 | H1/H7 → **H8, permanent** | closed at condition (i) | one content file in the archive; profiles withheld under consent |
| SAK-08 | Riris 2018, W2784603861 | H5 → **H8, trigger** | closed at condition (i) | model code not found in six checked routes; the publisher's supplementary material could not be reached (HTTP 403) and is recorded as unresolved |
| SAK-11 | Bynum et al. 2021 (seven authors), W4206850274 | H5 → **H8, trigger** | stopped at condition (ii) | C(41,7) = 22 481 940 scenarios; ≈ 5.03 × 10⁹ constraints |

**SAK-14.** The thesis states that Greek sources are given only in French translation because the
author does not read Greek. Ninety citation places (Dionysius 57, Plutarch 22, Appian 5, Cassius Dio
3, *Moralia* 2, Aristotle 1; 76 unique references, of which 48/19/4/3/1/1) were resolved against
open Greek editions. 79
resolved (87.8 %), 75 from Perseus and 4 from the Scaife Viewer; Perseus alone gives 75/90 = 83.3 %
[74.3–89.6], and the outcome is the same under either. The denominator is 90, the grammar as run; a
first parse gave 81 (70 resolved, 86.4 %) and the grammar was extended after locking, which is
recorded as a deviation. A denominator of 60 — only the citation form the criterion's first
clarification names literally — gives 55/60 = 91.7 % [81.9–96.4], above the threshold; it is reported
as a sensitivity, marked post hoc with the denominator chosen after the outcome, and is not the gate.
The eleven misses have three measured causes: seven are edition addressability (the French section
numbering is finer than the open Greek editions'), three are absence of an open Greek text (Cassius
Dio, books 1–35), one is a mis-citation in the thesis. Both Perseus and Scaife answer HTTP 200 with a
different passage when the requested one does not exist; had an HTTP 200 response been taken as a
hit, without level-by-level comparison of the resolved against the requested address, all eleven
would have been recorded as resolved and the retrieval step would have read 90 of 90. What the
case would then have shown is stated differently in the project's own documents: the case file and
LAERDOM §35 say the case would have stood as lifted at 100 %; LAERDOM §37 says the gate would have
had no answer, because the criterion's second element — the load-bearing terms — was unmeasurable
for 79 of the 90 places; ADR-0013, written afterwards, holds that under its three conditions the
case would not have been lifted. The three statements are reported as they stand. Only 11 of the 90 places (12.2 % [7.0–20.6]) carry the
thesis's own French rendering, and 9 of those 11 (8 unique references) could be resolved at section
level, so the comparison of original against translation was possible for those alone; for the
rest, resolution to Greek text is what was measured. Post hoc, two of eight checkable references point to the wrong place
(the passage cited as *AR* I, 40, 1 translates I, 60, 1; I, 49, 3 translates I, 59, 3), 25 % [7.1–
59.1]. Fourteen load-bearing terms were located character-for-character in the retrieved Greek with
zero errors; divergence from the LSJ gloss on the axis the thesis argues was judged 3 of 14 by a blind
sub-instance and 7 of 14 by the main reading, agreement 10 of 14 (71.4 % [45.4–88.3]); both are
reported. That a translator's contextual choice differs from a lexicon's first sense is expected; the
two mis-citations are the hard finding.

**SAK-09b.** The thesis reports that Pajek cannot force equal partitions of the intermediate mode in
two-mode blockmodelling. The thesis's own numbers were reproduced first: table D.1, 12 of 12 values
exactly; 109 constraints reconstructed (13 + 36 + 48 + 12); total error 14 reproduced in two
independent implementations, with blocks (1,7) = 3 and (1,8) = 2 from figure 8.2 as controls. Over
all 144 blocks the error is 163, a number the thesis does not report and without which 14 cannot be
checked. The named alternative, the R package `blockmodeling` (version 0.3.1 was published in June
2018, before submission; version 1.1.8, 2025, was run here), also has no mechanism to bind a row
partition to a column partition: with 50 starts and free block-type choice (the regime in which
the objective is degenerate, see below) it returned solutions whose two partitions of the
intermediate mode differed, and in our own implementation with block types fixed to the thesis's
image matrix, unconstrained partitions were equal in 0 of 120 starts. The research result is that the thesis's workaround is
itself a constrained solution: its augmented one-mode matrix has only one partition of the 34 nodes,
with error 14 against 18 for the best constrained search from 120 starts in our implementation, and
no improvement from a constrained search started at the thesis's partition. The tool limit blocked a
representation, not a result, as far as these searches reach. Two discrepancies in the thesis's
own description were found: the matrix is written as having *i + k* = 21 columns where the block
form gives *j + k* = 22 (an error), and the stated total error of 14 counts only the 32 three-mode
blocks without saying so (an omission; the total over all 144 blocks, 163, is needed to check it).
The thesis also states that block types may be given priorities or weights without reporting the
values; with free block-type choice the objective is degenerate, so all searches in our own
implementation fixed the types per position to the thesis's own image matrix, while the R-package
run reported above used free block-type choice.

**SAK-09c, SAK-08, SAK-11.** Automatic generation of a concept network from interview material
(SAK-09c) cannot be attempted: the archive record has one content file, and the thesis states that
interviewee profiles are withheld under consent — a barrier that will not fall with any model.
Continuous re-running of an agent-based model split for processing time (SAK-08) cannot be attempted:
six routes (the article, the institutional repository, CoMSES, GitHub, Crossref relations, the
author's ORCID record) hold no model code; re-implementation from a ten-page article would be a
different model. Full enumeration of the outage scenarios of a stochastic grid-hardening model
(SAK-11) cannot be reproduced: the scenario set and the parameters of its distribution are not
reported, the cross-validation result exists only as a figure, and the full problem — C(41,7) =
22 481 940 scenarios, verified against MATPOWER case30 with 41 lines, scaled linearly from the
article's table 2 to ≈ 3.28 × 10⁹ variables and ≈ 5.03 × 10⁹ constraints — has a coefficient matrix of
0.2–0.4 TB against 11 GB available. The article's own claim that 100 scenarios are "less than
0.001 %" of the space is confirmed: 0.000445 %.

**The pattern.** Three cases reached a locked criterion, but only SAK-14 had a numerical threshold,
and it fell short by 2.2 percentage points. In three of five new cases the input needed was not
available — withheld under consent, not found in six checked routes, not reported; in the fourth the
named means lacks the mechanism.
The condition distribution over the six is 2–1–3 (stopped at condition i: SAK-09c, SAK-08; at
condition ii: SAK-11; reached condition iii: PS-246, SAK-14, SAK-09b). In phase 2 the gate is not what
filters; access is.

### 4.6 Has anyone done it since?

For four parked items — dating of the jewellery and metal finds from deposit pit H at the Demeter
sanctuary at Knossos (Karatas 2018, W2974992769, 3 citing works), the joint evaluation of pottery,
artefacts and houses at Eythra (Mecking et al. 2017, W4317830072, 2 citing works), further analyses
of lead-processing crucibles from the fifth-millennium Lower Danube (Hansen et al. 2019,
W2936215896, 12 citing works) — the answer from the citation graph is no in all three, at a cost of
10 OpenAlex credits; for the fourth, the salinity term in the soil-water model of Pring 2016, the
answer is no from a search of the thesis text itself. The fields are not dormant: a broader search returns 137 hits for the Knossos
sanctuary and 81 for Eythra since publication. An obstacle is not lifted because the field keeps
working nearby. For Pring 2016 the parked term cannot be supplied from the thesis: electrical
conductivity is measured by the instruments but never reported as data (0 occurrences of dS/m, ECe,
"saturated paste" or "soluble salts" in 579 109 characters of extracted text), and the one value
present, 0.0 μS/cm, is the value that was set.

### 4.7 Phase 3 — prospective gate and first measured recall

*(Numbers in this section are from the ADDENDUM-25 run report of 30 September 2026 and are to be
anchored in the fact file's phase 3 section before circulation.)*

Phase 3 (ADDENDUM-25, locked before the draw) applied the chain as locked — the code of §3.2 with
one extension made before the lock, a work-list input for works outside the first 100 — to **100
archaeology works** drawn with seed 734248 from the frozen frame, none of them among the first 100.
Before the sieve or the reader ran, a **reference set** was built: 20 of the 100 works, drawn with
the same seed, were read cover-to-cover by twenty agentic Opus instances, one per work, each with an
empty context, the coder-2 rule file and a block list, and every hit was recorded. The key was
secured on the archive volume with its hash at 10:20:05 UTC and the sieve started 29 seconds later;
at that point the order was enforced by procedure, and it has been enforced in the resume routine's
code since 13:04 UTC the same day, which refuses to start the sieve until the reference set is
complete. Two gates were fixed in the same document: (1) blind agreement on 100
random reader hits, threshold 0.70; (2) recall of the reference set's hits through the sieve and
through the reader, reported without a threshold.

The 100 works gave **21 361 passages**. The judge flagged 2 188; the extractor produced 1 923
windows (the run was interrupted four times — a session crash during extraction, a blocked write
path that stopped twelve reader sessions before any verdict was written, and two subscription
session limits mid-batch — and resumed each time from the locked code; the 1 357 extraction windows
written before the crash were byte-identical to the re-run, hash for hash); the
union is **4 107 passages, 19.2 %** of the corpus, against 12.8 % on the first 100 works. Fourteen
reader sessions (twelve batches, two of them completed in a second instance after a session limit)
judged all 4 107; every session reports `claude-opus-5` in its transcript. The reader called **673**
passages hits (16.4 % of the union), in 73 of the 100 works.

**Gate (1) held: 85 of 100 = 85.0 % [76.7–90.7].** The 100 rows were drawn with seed 734248 and read
by a separate instance under an assignment byte-identical to the template locked in ADDENDUM-25;
the instance reports `claude-opus-5`. Agreement again separates on the reader's doubt flag: 97.4 %
without doubt, 77.4 % with. The figure is the same as the post hoc gate on the first material
(85 of 100), now under a gate fixed before the run.

**Gate (2), the first measured recall.** The reference readings found **104 hits in the 20
works**. The sieve retained **95 of 104 = 91.3 % [84.4–95.4]**; the reader confirmed **85 of 104 =
81.7 % [73.2–88.0]**. The losses are of the same size at each stage: nine reference hits fell in the
sieve, ten at the reader. This is recall against an LLM reference reading, not against a human one,
and on 20 works; it is the first value the tool has for the quantity. It is recorded in the outcome
document of the run; the register schema still admits only "not measured" for the sieve-recall field
and is to be extended, with the reference set and n as provenance, before it carries a value.

The list from this run is therefore named **worklist (prospective gate)**; the list from the first
100 works remains a candidate list.

On the new material H7 is 63.2 % of hits; the liftable classes are 101 of 628 decided hits (16.1 %)
and the undecided share 45 of 673 (6.7 %), against 19.0 % and 6.0 % on the first 100 works. Density
is 6.73 hits per work, against 10.96 in the first 25 archaeology works (31.5 against 40.6 per
1 000 passages of the corpus). Reader cost was 79.5 million context tokens over the 14 sessions:
**118 185 per reader hit**, against 164 805 on the first material, and 139 053 per hit confirmed
at the measured 85 % agreement. The deviations recorded in the outcome document include: the locked
register step writes a header that fails the schema strengthened before the lock, so the register
for this run is written by the corrected step, the one code change after the lock, with the row
content unchanged hash for hash; the OpenAlex credit balance before the draw was not recorded (only
after: 985); the reference gate existed as procedure, not code, when the sieve started; two reader
sessions hit the subscription's session limit mid-batch and were completed in a second instance
without rewriting any existing verdict; and the twelve sessions blocked by the write path consumed
tokens without producing a verdict. The full list is in the outcome document, §0.

---

## 5 Discussion

**What the tool delivers.** On this material a field enters and a candidate list leaves: rows with
class, doubt flag, sieve source, dated liftability, and a header stating which gate the list passed.
What it does not deliver is a judgement of whether a given obstacle can be lifted today. That is
casework per candidate — the five new attempts took about 5.5 hours of tool-assisted work in
total by commit times, from about 20 minutes (SAK-08) to about 2 hours 10 minutes (SAK-14), over
27–28 September — and
it is dated, because an obstacle can be reintroduced: the protocol's H1 control case, a critical
edition outside the 100 works that was parked for want of time to collate three British Library
manuscripts, moved from H1 to H8 without a change to its text when the library's digitised images
left the open channel in October 2023 (ADR-0010).

**The second claim.** On 100 works, zero of six attempted obstacles were lifted by a resource that did
not exist at publication. Two thirds of candidate rows are parked on data that never existed. Of
the six attempts — five in liftable classes and one (SAK-09c) in the undecided class, whose
liftability the protocol sets to "undecided" (ADDENDUM-05 §3) — three stopped on input we could
not obtain — withheld under consent, not found where it would be expected, not reported — and three
reached a locked criterion and stopped at its threshold or at the named means. The protocol's second claim, that a share of
the named obstacles are lifted today and a share of those by AI (PREREG §1.2, our paraphrase), has
no support in this material. What
the attempts did produce is of a different kind: verified undone-ness, two mis-citations in a thesis
that could not be found without reading the Greek, a thesis's workaround for which no better
constrained solution was found, and an undone enumeration whose sampled fraction the authors had
already reported as below 0.001 % — confirmed here as 0.000445 %.

**Language models as measurement instruments.** The reliability results bear on studies that use
LLM annotation. Hit-decision agreement between two frontier instances is high (0.812) and survives a
change of model family (0.899 against coder 2); class agreement is lower (0.722) and weakest at two
non-hit boundaries (N3 0.530, N2 0.535); a decision rule now exists for N3 but is untested, and
none for N2; the
set of items on which two coders agree without doubt is small (3 of 27); and a reader in one call
per item has a lower point estimate than the same model reading a batch with the rules in context, a
difference that is not statistically established here. The gates were locked before the runs, so
the losses could not be re-labelled afterwards.

**Five words.** The manuscript uses words that carry less than a reader will hear, and for each there
is a measured number saying how much less. *Lifted* had no definition until ADR-0013; the six cases
stopped at three different places and were all called "not lifted". *Reference set* is judge-
conditioned and measures recall loss relative to the judge, not precision, absolute recall or
prevalence. *Confirmed* means a post hoc gate at 85 of 100, not the preregistered one, and 15 of the
100 were coded by a second instance. *Stable* (3 of 27) is a property of two LLM coders' agreement
without doubt marks. *Independent* means an empty context and a separate scratch directory, not
independent judgement: every coder is a language model. Three words carry their weight and are used
instead where possible: *candidate list*, *not measured*, *dated assessment*.

---

## 6 Limitations

1. Three codings of the 320 passages, all by language models, none by a human. Coders 1 and 2 are
   Opus instances; coder 4 is a different family, with 7 of 320 rows exposed. κ against human reading
   is unknown.
2. Assessability (M2) carries coder identity: the protocol never defined what counts as assessable
   without a domain expert, and two readings within its wording gave 88 % and 32 % *(source:
   MASTER §4, ADDENDUM-11)*.
3. Four purposively chosen fields; the numbers hold for these four.
4. Open-access and retrievability selection with strong publisher skew by delivery format.
5. The preregistration was not externally timestamped before data; OpenTimestamps receipts exist from
   28 September 2026 for all locks.
6. Rule clarifications were written after data (ADDENDUM-10 moved 1 of 48 doubtful cases).
7. On the first 100 works the sieve's recall is not measured, because the reference set is the
   sieve's own output. Phase 3 supplies one measured value — 91.3 % for the sieve, 81.7 % through
   the reader — against an LLM reference reading of 20 works, in one field.
8. No frontier-model judge was used at passage level for the whole corpus; the local judge is the sieve.
9. Register v2 did not validate against its own schema until 27 September 2026: a sieve-precision
   interval was missing on all rows and citation coverage carried an unmeasured zero; corrected without
   new measurement (register sha256 `aa8f7c2e…` → `6caabaff…`; the register cited in this draft,
   `c6895202…`, is the state after four later case updates).
10. The tool is open in licence but not in practice: without an agentic frontier reader, the sieve is
    all one gets, and the sieve is 15.2 % precise (432 of 2 844).

---

## 7 Data, code and availability

Code is Apache-2.0 at https://github.com/avalyset/gjenopptak (public branch: a root commit plus one
release commit per canonical version; the working history up to the v0.3.0 lock on 26 September
2026 is in the git bundles deposited with versions v0.1.0–v0.3.0; locks made later that day and
since — ADDENDUM-12 onward — are in no deposited bundle). Own data are CC BY 4.0. Third-party text is not redistributed: full texts and
the 22 243 passages stay out of the deposit as a decision (licence audit, 28 September 2026),
quotations rest on the right of quotation with source attribution, and blind files will be deposited
as indices (identifier, work, sentence span, sha256 of the text) from which the text is regenerated
deterministically from the open sources and verified against the hash. Licence per work is recorded
in `LISENS-PER-VERK.md`; 13 of the 60 works in the candidate list carry NC or ND terms. Deposited
versions v0.1.0–v0.3.0 (concept DOI 10.5281/zenodo.22959326) carry the protocol, the addenda and
decision records then current, the lessons log, register v1 and a bundle of the git history; they
lack the rule file behind κ = 0.812, and the candidate list (register v2) is not in any deposited
version. Version v0.4.0, prepared but not yet published at the time of this draft, is to add that
rule file, the block lists and reader assignments every locked measurement read, the blind-file
indices, the case files, the licence table and the OpenTimestamps receipts. The prepared v0.4.0
build does not include the candidate list (register v2); whether a bundle of the history after the
v0.3.0 lock is included is a decision of the author, open at the time of this draft.

## 8 Use of AI systems

All passage coding, extraction, reading and case execution were performed by language models under
locked instructions, as described in §2.4 and §3.2. Model identity is recorded per verdict for the
local judge (weight hash and signature) and, for the readers, from the pipeline configuration rather
than from each response; the reference coders' verdict files carry no model identifier, and coder
2's model is known from the session transcript. This draft was written in a chat interface by a
language model (the interface product is recorded in the project's instruction file as Fable 5.1;
no model identifier was logged for the drafting itself) from a fact file compiled and hash-anchored
by a Claude Code instance, and revised four times against fact-check reports produced by separate
instances (`136d025`, `b084ba2`, `faaaddc`, `c4d645c`); a fifth check (`ffeaccf`) recorded the
residual.
The author designed the study, set the criteria, made every decision recorded in the decision
records, and is responsible for the text.

## References

*[To be assembled from the register and case files. Works, by OpenAlex identifier and Crossref
DOI where one exists: Pring 2016 (W2551114598, thesis, no DOI); Haouachi 2016 (W2474595476, thesis,
10.70675/8513d3c9ze385z4b4bz910cz221c7718984d); Aragao 2018 (W7133020405, thesis, handle
1807/92034); Riris 2018
(W2784603861, 10.1177/0959683617752857); Bynum et al. 2021 (W4206850274, seven authors,
10.1061/(asce)is.1943-555x.0000603); Karatas 2018 (W2974992769, 10.4000/mythos.297); Mecking et al.
2017 (W4317830072, 10.35686/ar.2017.12); Hansen et al. 2019 (W2936215896,
10.1371/journal.pone.0214218). Protocol, addenda and decision records by concept DOI and version.
Software by name and version: MATPOWER case30; R `blockmodeling` 0.3.1 (2018) and 1.1.8 (2025);
Perseus Digital Library; Scaife Viewer / First1KGreek; OpenTimestamps client 0.7.2.]*
