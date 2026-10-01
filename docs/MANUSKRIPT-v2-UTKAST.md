# Declared and undone: an open tool for finding work that researchers report leaving unfinished, and a test of whether the named obstacles can be lifted

**Manuscript v2 — draft of 28 September 2026.** Written from `docs/MANUSKRIPT-FAKTA-2026-09-28.md`;
every number below is anchored there with a path and a sha256. Sections marked *[pending]* depend on
ADDENDUM-25 (phase 3) and are to be filled from its outcome file. Not for circulation until the
fact-check pass (CC) has been run against this file.

**Author:** Eirik Botten Nicolaysen, EcoDeco AS, Lillehammer, Norway. ORCID 0009-0001-9188-6788.
**Code and materials:** https://github.com/avalyset/gjenopptak · concept DOI 10.5281/zenodo.22959326
(cite the concept DOI; version DOIs identify a specific state). Protocol PREREG-v1 locked internally
12 September 2026 (sha256 `05988b23…`); see §6 on timestamping.

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
gave κ = 0.899 [0.808–0.969] against the second coder. Among confirmed hits, roughly two thirds name
an obstacle of the kind that cannot be lifted by anyone: the data never existed (H7 = 289 of 432
candidate rows, 66.9 % [62.3–71.2]). The pipeline produced a candidate list of 432 rows from 60 works
that a separate blind reading agreed with in 85 of 100 sampled rows [76.7–90.7]; a preregistered gate
on 27 known hits was not met (21 of 27 against a threshold of 22) and the list is therefore named a
candidate list, not a worklist. We then took six candidates through a locked reopening procedure
(reproduce the source's own numbers first, then execute the undone step against a criterion fixed in
advance). None of the six obstacles was lifted. In three of five new cases the procedure stopped
before any threshold because the input — interview profiles under consent, model code, a scenario set
— was never published; in the one case that reached its threshold, 79 of 90 Greek source passages
cited only in translation could be retrieved and read against the original (87.8 % [79.4–93.0],
threshold 90 %), and the exercise located two citations in the thesis that point to the wrong place.
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

We report (i) the class distribution on 100 works, (ii) the reliability of language-model coders on
this task, (iii) the pipeline and its measured properties, (iv) six reopening attempts under a locked
procedure, and (v) what the results say about the second claim. The third claim is answered
prospectively only by phase 3, whose outcome is pending at the time of this draft.

---

## 2 Materials

### 2.1 Frame and sample

The frame is OpenAlex, publication years 2015–2020, open access with retrievable full text, in four
fields chosen to span the natural sciences and the humanities: energy modelling, archaeology,
clinical epidemiology, and historical textual scholarship. Twenty-five works were drawn per field
(100 in total), by sequential draw in seed order (ADDENDUM-09). The retrievability requirement makes
the frame skewed by delivery format rather than by business model: works delivered as structured XML
are almost always retrievable, works delivered as PDF in about half the cases, and large publishers
that block download fall almost entirely out of the frame.

### 2.2 Unit of observation

The unit is the passage: a candidate sentence with two sentences of context on each side, at a stride
of three sentences (ADDENDUM-03). A hit requires that the undone and the obstacle both lie inside the
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
separately) and 12 anchor passages with known status from earlier recall sets, which belong to the
seed material and are excluded from recall measurements.

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
established on three independent grounds and it is deposited with v0.4.0. **Coder 4** (28 September)
is Claude Fable 5.1 in a chat interface — a different model family — reading the same 320 passages
with the same rule file in the same order. Seven of the 320 rows had been seen by coder 4 with the
reader's class labels the day before; the sensitivity to this exposure is reported in §4.2.

No human annotator has read the material.

---

## 3 Methods

### 3.1 Preregistration and locks

The protocol was locked internally on 12 September 2026 with a sha256 as its first commit. It was
corrected through numbered addenda, each locked as a single-file commit that triggers an archived
bundle of the full git history. Two rule clarifications were written after data (ADDENDUM-10) and
moved one of 48 doubtful cases. The protocol was not timestamped by a third party before data were
read; the lock order rests on the repository history, which is deposited, and on OpenTimestamps
receipts on the bundles (complete from 28 September 2026).

### 3.2 The pipeline

The tool runs as one command in eight steps: retrieve → passages → judge → extract → union → blind
files and reader assignment → read → register (ADR-0012).

- **Judge.** `gemma2:9b`, temperature 0, seed 734248, `num_ctx` 8192, one call per passage, output
  constrained to the typology, a signature per verdict. It flagged **2 173** of 22 243 passages.
- **Extractor.** The same model reads each document in ~3 000-token windows and quotes sentences in
  which the authors state their own undone work with a reason. **884** quoted lines from 598
  windows, 124 windows returning none.
- **Union.** Flagged passages ∪ passages containing a quoted line, with an all-hits join between
  quotes and overlapping windows: **2 844** candidates, covering **27 of 27** known hits. The join
  rule was a correction: a first-hit join gave 2 581 and 26 of 27, because one quote lay in two
  overlapping windows. Recall of the sieve beyond the 27 is *not measured* — the 27 are the sieve's
  own output — and the register schema admits only the value "not measured" for it. The first
  measured recall will come from phase 3 [pending].
- **Reader.** An agentic Opus instance per batch of at most 356 passages, with the coder-2 rule file
  and block list, run serially with its own scratch directory. Reader verdicts are dated and not
  repeatable: the reader has no seed and is updated by its vendor; each verdict carries a model
  signature.
- **Register.** One row per hit with class, doubt flag, sieve source and its measured precision,
  work-level assessment, citation-falsification coverage, dated liftability from the protocol table,
  section provenance, and a non-prose flag. The header carries the gate the list has passed and a
  naming policy: evaluative statements address the work, not the person.

### 3.3 Reliability

Cohen's κ with paired bootstrap, 10 000 replications, seed 734248, on the hit decision over all 320
passages and over the 300 non-anchor passages; class κ among passages both coders call hits.

### 3.4 Gates

Two gates were set. The **preregistered gate** (ADDENDUM-22): a third, independent coder reading the
union must confirm at least 22 of the 27 known hits. The **post hoc gate** (ADDENDUM-23, written after
the first fell): 100 random rows the reader called hits (seed 734248) read blind by a separate
instance, threshold 70 %. The list is named by the gate it passed.

### 3.5 Reopening procedure

"Lifted" had no definition before 28 September 2026. ADR-0013 now gives three conditions: (i) the
named resource exists in an open source on date D; (ii) the source's own numbers can be reproduced
first; (iii) a criterion locked before computation is met. Each case has its criterion in a file whose
sha256 is fixed before any computation. A case that fails to reproduce the source's own numbers is
stopped and recorded; substituting our own data would replace the source's numbers with ours.

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
289, H5 50, H9 29, undecided 26, H2 14, H8 11, H1 10, H3 2, H4 1. ADDENDUM-22 reports 69/374 =
18.4 % for the liftable share and 253/374 = 67.6 % for H7; those are the partial state at the time the
addendum was locked, mid-run, not a contradiction.

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

Seven of the 320 rows had been seen by coder 4 with labels before coding; excluding them gives 0.874
against coder 2 and 0.757 against coder 1, and the ordering coder 4–2 > coder 1–2 > coder 4–1 holds
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
coders on the same 320 passages (class κ for N3 between coders 1 and 2: 0.530; overall class κ 0.722).
The boundary is now an explicit, versioned decision rule with anchor examples (`REGEL-N3-v1`).

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
of the rules. Two earlier runs (κ 0.390 for Opus, 0.321 for Sonnet) were invalidated by output
truncation at 300 tokens, which cut 36 of 320 Opus answers and 27 of coder 1's 39 hits; they are kept,
marked invalid, and not used.

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
have with each other (coder 2 confirmed 19 of coder 1's 25 hits, 76 %); a gate on a reference set
should be set at the set's own inter-coder agreement, not above it.

**The post hoc gate held.** Of 100 random hit rows read blind by a separate instance, **85 were
confirmed [76.7–90.7]**, with class agreement in 74 of 85 (87.1 %). The reader's own doubt flag
separates the sample sharply: 41 of 42 confirmed where the reader was not in doubt (97.6 %), 44 of 58
where it was (75.9 %). This is a post hoc subgroup; no other predictor was compared and the difference
is not tested. One deviation from the gate's text must stand: "one separate instance" became two, 85
plus 15, after the first was interrupted; the 85 are a contiguous prefix, not a sample.

### 4.5 Six reopening attempts, none lifted

| case | work | class | outcome | deciding number |
|---|---|---|---|---|
| PS-246 | Pring 2016, W2551114598 | H5 | criterion met for 2 of 4 horizons (25 Sept.) | soil-model inconsistency reproduced for the four horizons named |
| SAK-14 | Haouachi 2016, W2474595476 | H3 language | **not lifted** | 79 of 90 = 87.8 % [79.4–93.0] vs 90 % |
| SAK-09b | Aragao 2018, W7133020405 | H5 tool limit | **not lifted by the named means** | `blockmodeling` 1.1.8 has no mechanism; unconstrained partitions equal 0 of 120 times |
| SAK-09c | Aragao 2018, W7133020405 | H1/H7 → **H8, permanent** | closed at condition (i) | one content file in the archive; profiles withheld under consent |
| SAK-08 | Riris 2018, W2784603861 | H5 → **H8, trigger** | closed at condition (i) | six routes checked, no model code deposited |
| SAK-11 | Bynum et al. 2021, W4206850274 | H5 → **H8, trigger** | stopped at condition (ii) | C(41,7) = 22 481 940 scenarios; ≈ 5.03 × 10⁹ constraints |

**SAK-14.** The thesis states that Greek sources are given only in French translation because the
author does not read Greek. Ninety citation places (76 unique references: Dionysius 57, Plutarch 22,
Appian 5, Cassius Dio 3, *Moralia* 2, Aristotle 1) were resolved against open Greek editions. 79
resolved (87.8 %), 75 from Perseus and 4 from the Scaife Viewer; Perseus alone gives 75/90 = 83.3 %
[74.3–89.6], and the outcome is the same under either. The denominator is 90, the grammar as run; a
first parse gave 81 (70 resolved, 86.4 %) and the grammar was extended after locking, which is
recorded as a deviation. A denominator of 60 — only the citation form the criterion's first
clarification names literally — gives 55/60 = 91.7 % [81.9–96.4], above the threshold; it is reported
as a sensitivity, marked post hoc with the denominator chosen after the outcome, and is not the gate.
The eleven misses have three measured causes: seven are edition addressability (the French section
numbering is finer than the open Greek editions'), three are absence of an open Greek text (Cassius
Dio, books 1–35), one is a mis-citation in the thesis. Both Perseus and Scaife answer HTTP 200 with a
different passage when the requested one does not exist; without level-by-level comparison of the
resolved against the requested address, all eleven would have been recorded as hits and the case
would stand as lifted at 100 %. Post hoc, two of eight checkable references point to the wrong place
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
checked. The named alternative, R package `blockmodeling` 1.1.8, published in June 2018, before
submission, also has no mechanism to bind a row partition to a column partition; unconstrained, its
partitions were equal 0 of 120 times. The research result is that the thesis's workaround is a
constrained solution: its augmented one-mode matrix has only one partition of the 34 nodes, with
error 14 against 18 for the best constrained search from 120 starts, and no improvement from a
constrained search started at the thesis's partition. The tool limit blocked a representation, not a
result. Two errors in the thesis's own description were found: the matrix is written as having
*i + k* = 21 columns where the block form gives *j + k* = 22, and "total error 14" counts only the 32
three-mode blocks without saying so.

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

**The pattern.** Only SAK-14 reached a threshold, and it fell short by 2.2 percentage points. In three
of five new cases the input was never published; in the fourth the named means lacks the mechanism.
The condition distribution over the six is 2–1–3 (stopped at condition i: SAK-09c, SAK-08; at
condition ii: SAK-11; reached condition iii: PS-246, SAK-14, SAK-09b). In phase 2 the gate is not what
filters; access is.

### 4.6 Has anyone done it since?

For four parked items — dating of the jewellery and metal finds from deposit pit H at the Demeter
sanctuary at Knossos (Mythos 2018, 3 citing works), the joint evaluation of pottery, artefacts and
houses at Eythra (2017, 2 citing works), further analyses of lead-processing crucibles from the
fifth-millennium Lower Danube (Pietrele 2019, 12 citing works), and the salinity term in the
soil-water model of Pring 2016 — the answer from the citation graph is no in all four, at a cost of
10 OpenAlex credits. The fields are not dormant: a broader search returns 137 hits for the Knossos
sanctuary and 81 for Eythra since publication. An obstacle is not lifted because the field keeps
working nearby. For Pring 2016 the parked term cannot be supplied from the thesis: electrical
conductivity is measured by the instruments but never reported as data (0 occurrences of dS/m, ECe,
"saturated paste" or "soluble salts" in 581 864 characters), and the one value present, 0.0 μS/cm,
is the value that was set.

### 4.7 Phase 3 — prospective gate and first measured recall *[pending]*

*[To be inserted from the ADDENDUM-25 outcome: 100 new archaeology works from the frozen frame; a
reference set of 20 works read cover-to-cover before the sieve ran; the unchanged chain; blind
precision on 100 hits against 0.70; recall of the reference set's hits through sieve and reader,
reported without threshold; density and cost per confirmed hit on fresh material; the resulting name
of the list.]*

---

## 5 Discussion

**What the tool delivers.** On this material a field enters and a candidate list leaves: rows with
class, doubt flag, sieve source, dated liftability, and a header stating which gate the list passed.
What it does not deliver is a judgement of whether a given obstacle can be lifted today. That is
casework per candidate — the six attempts above took days each — and it is dated, because an obstacle
can be reintroduced: the best AI-liftable candidate in the material, a critical edition parked for
want of time to collate three British Library manuscripts, moved from H1 to H8 without a change to
its text when the library's digitised images left the open channel in October 2023.

**The second claim.** On 100 works, zero of six attempted obstacles were lifted by a resource that did
not exist at publication. Two thirds of confirmed hits are parked on data that never existed. Where
the class is liftable in principle, what stops the attempt is unpublished input and consent. The
claim that "some obstacles have since been lifted, some by AI" has no support in this material. What
the attempts did produce is of a different kind: verified undone-ness, two mis-citations in a thesis
that could not be found without reading the Greek, an author's workaround shown to be optimal, an
undone computation shown by the authors' own arithmetic to be unnecessary.

**Language models as measurement instruments.** The reliability results are transferable to any
study that uses LLM annotation. Hit-decision agreement between two frontier instances is high
(0.812) and survives a change of model family (0.899 against coder 2); class agreement is lower
(0.722) and collapses at one boundary (N3, 0.530) until the boundary is written as a decision rule;
the set of items on which two coders agree without doubt is small (3 of 27); and a reader in one call
per item is measurably worse than the same model reading a batch with the rules in context, though
the difference is not statistically established here. Two of these results were reached only because
the gates were locked before the runs and the losses could not be re-labelled afterwards.

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
2. Assessability (M2) carries coder identity: the protocol never defined "without a domain expert",
   and two readings within its wording gave 88 % and 32 %.
3. Four purposively chosen fields; the numbers hold for these four.
4. Open-access and retrievability selection with strong publisher skew by delivery format.
5. The preregistration was not externally timestamped before data; OpenTimestamps receipts exist from
   28 September 2026 for all locks.
6. Rule clarifications were written after data (ADDENDUM-10 moved 1 of 48 doubtful cases).
7. Recall is the least-measured end: the sieve's recall is not measured, and the reference set is the
   sieve's own output. Phase 3 supplies the first measured value *[pending]*.
8. No frontier-model judge was used at passage level for the whole corpus; the local judge is the sieve.
9. Register v2 did not validate against its own schema until 28 September 2026: a sieve-precision
   interval was missing on all rows and citation coverage carried an unmeasured zero; corrected without
   new measurement (register sha256 `aa8f7c2e…` → `c6895202…`).
10. The tool is open in licence but not in practice: without an agentic frontier reader, the sieve is
    all one gets, and the sieve is 15.2 % precise (432 of 2 844).

---

## 7 Data, code and availability

Code is Apache-2.0 at https://github.com/avalyset/gjenopptak (public branch: a root commit plus one
release commit per canonical version; the full working history is in the deposited git bundles). Own
data are CC BY 4.0. Third-party text is not redistributed: full texts and the 22 243 passages stay out
of the deposit as a decision, quotations rest on the right of quotation with source attribution, and
blind files are deposited as indices (identifier, work, sentence span, sha256 of the text) from which
the text is regenerated deterministically from the open sources and verified against the hash.
Licence per work is recorded in the manifest; 13 of the 60 works in the candidate list carry NC or ND
terms. The deposit (concept DOI 10.5281/zenodo.22959326) carries the protocol, all addenda and
decision records, the lessons log, the method document, the registers, the rule file and block lists
every locked measurement read, the reader assignments, OpenTimestamps receipts, and a bundle of the
full git history. Versions through v0.3.0 lack the rule file behind κ = 0.812; v0.4.0 carries it.

## 8 Use of AI systems

All passage coding, extraction, reading and case execution were performed by language models under
locked instructions, as described in §2.4 and §3.2, with model identity recorded per verdict. This
draft was written by Claude Fable 5.1 from a fact file compiled and hash-anchored by a Claude Code
instance; every number was then checked against that file by a separate pass. The author designed the
study, set the criteria, made every decision recorded in the decision records, and is responsible for
the text.

## References

*[To be assembled from the register and case files: cited works by DOI/OpenAlex identifier
(W2551114598, W2474595476, W7133020405, W2784603861, W4206850274, W2974992769, W4317830072,
W2936215896); protocol, addenda and decision records by concept DOI and version; software (MATPOWER
case30, R `blockmodeling` 1.1.8, Perseus, Scaife Viewer, OpenTimestamps) by name and version.]*
