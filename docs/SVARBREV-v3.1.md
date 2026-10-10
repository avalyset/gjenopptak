# Response to the review

In addition to the changes below, the manuscript now follows the journal's format: abstract within
250 words, keywords, numbered tables with captions, use of language models documented in the Methods
(§3.7), and a Statements and Declarations section.

We thank the reviewer for a detailed and accurate report. Every point was addressed; changes are
quoted or located below. All new numbers come from a reanalysis script deposited with the code, and
a number manifest in the deposit links each number in the manuscript to its file, hash and script.

## Major issues

**1. No external validation of the instrument.** We agree. Model–model agreement cannot establish
validity. (a) Terminology is changed throughout: "true", "confirmed hits", "precision" and "recall"
are replaced by *reference-positive*, *confirmation rate*, *retention* and *reader agreement with the
reference*, defined in §3.5. (b) The abstract, §6 and §7 state that the figures measure agreement
within a model-based instrument. (c) A human validation study has been preregistered and locked
before any human coding (§4): 149 passages from 75 works stratified by sieve status, reader doubt,
field and phase, two annotators, blind adjudication, and the analyses the reviewer lists. It has not
been run; we report it as planned rather than delay the record. (d) The claim that results "survive a
change of model family" is withdrawn: coder 4 is a different model from the same vendor, and its
underlying model identifier was not recorded (§3.5).

**2. Preregistration language and the "lifted" outcome.** We agree. The study is now presented as two
phases of different status (§3.1): phase 1 is development and exploratory analysis, with the
post-data clarifications and the second gate described with their timing; phase 2, locked before the
draw, is the confirmatory test of the pipeline. The case series is reported as exploratory, and §5.7
states that "lifted" was defined after the six attempts and that criteria were locked before
computation for three of them only.

**3. Clustering and denominators.** We agree. All intervals are now work-clustered (§3.6; Vanbelle,
2019). Clustering widens the intervals for class shares and phase 2 retention substantially (e.g.
reader agreement 60.9–89.7) and changes κ intervals little (92 works). Overlapping passages are now
merged into distinct declarations (§3.2): 432 rows are 276 declarations in phase 1, 673 are 424 in
phase 2, and class shares are reported per declaration. The field comparison is renamed "share of
reader positives among sieve candidates" and reported with the share of passages reaching the sieve,
with an explicit statement that these are not prevalences (§5.1).

**4. The 3.43 % estimate.** The estimator is now written out (§5.6): a cell-weighted sum over the
strata of the 320-passage reading, with one stated assumption. The point estimate is 3.42 %; the
previous interval (2.12–7.95) omitted the uncertainty of the precision term and clustering and is
replaced by 1.3–7.5 (work-clustered). The estimate is moved out of the main results and the word
"floor" is removed. The full stratum table is in the deposit.

**5. The case series cannot support "access and consent, not model capability".** We agree and have
removed the claim. §5.7 now states the selection procedure as it happened, from the documents written
at the time: one deterministic step followed by judgement favouring feasible cases, with no known
inclusion probabilities. The finding is stated descriptively.

**6. Related literature.** A related-work section is added (§2), placing the class relative to
limitation extraction and generation (BAGELS; LimitGen), sequential sentence classification against
manual annotation (LLM-SSC/biorc800; NLPContributionGraph), and evidence on LLM annotators (Gu et al.).
All references were verified against Crossref and the ACL Anthology. The novelty claim is restated
relative to these: the class requires a declared undone component of the authors' own work and a
stated reason, and is distributed outside limitations sections (81.4 % of passages carry no section
label).

**7. Reproducibility and the undeposited register.** (Data availability statement.) The phase 1 register is now deposited as an
index without third-party text (work identifier, span, text hash, class, doubt, sieve provenance), as
the reviewer suggests, together with the number manifest. Model identity is documented per session
for phase 2; the limit for coder 4 is stated. We note the reviewer's access problems with Zenodo and
GitHub; both are public, and the deposit version accompanying the manuscript is given in the data availability statement.

## Minor issues

1. "Second coder" is now "a second language-model coder" at first mention; the model-family claim is
   removed.
2. Terminology standardised (§3.5).
3. "Independent" is replaced by an operational description (empty context, separate instance, same
   vendor and rule file).
4. H6 = 0 is shown in the class counts (§5.1).
5. Field "hit rate" renamed (§5.1).
6. The per-source sieve figures are removed; they were mutually exclusive provenance strata, not
   marginal precision of each source.
7. "Frontier reads per confirmed hit" is removed; cost is now per reader positive.
8. 85/100 is called a confirmation rate.
9. Case B's denominators are reported with their status (90 used; 60 post hoc sensitivity); the
   parser history is in the case file.
10. Cases, parked items and source documents are distinguished; cases C and D come from the same
    thesis and are labelled as such.
11. The citation-graph checks are reported separately from the case series.
12. The κ difference is now tested with a paired bootstrap: 0.177, work-clustered 0.057–0.318. The
    previous statement that it was not established was wrong and is corrected (§5.3).
13. Raw agreement, PABAK and Gwet's AC1 are reported with every κ (§5.2).
14. The two 85/100 results are described as consistent point estimates with their intervals.
15. Version naming is aligned: the manuscript cites the concept DOI and the version DOI of the
    deposit that accompanies it.
16. Project-internal identifiers (addendum, decision-record and case numbers) are removed from the text;
    cases are labelled A–F and described in words.

## Questions

1. Reference-positives are no longer called true hits; a human-adjudicated sample would change the
   validity claims, not the agreement figures, and the study to test this is locked (§4).
2. Yes; see Major 1(c).
3. The estimator is in §5.6 and the deposit.
4. Rows sharing sentences are merged into declarations; the rule and counts are in §3.2 and §5.1.
5. See Major 5 and §5.7.
6. The hypothesis is no longer described as tested; see Major 2.
7. It cannot be documented beyond the product name; the claim is withdrawn.
8. The 100-row samples cover 33 (phase 1) and 38 (phase 2) works, largest 21 and 20 rows; intervals
   are work-clustered.
9. Yes; all κ intervals are work-clustered and change little.
10. The denominator issue is resolved by renaming; field prevalence is not estimated.
11. The register is deposited as an index without text.
12. See Major 6 and §2.
13. H7 shares are now stated as shares of decided declarations returned by this pipeline version.
14. The conclusion is withdrawn; see Major 5.
