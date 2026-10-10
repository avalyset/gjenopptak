# Codebook for human annotators — «declared undone work with a named obstacle» (v1)

*Kodebok for den menneskelige valideringen i ADDENDUM-27. Skrevet 03.10.2026 fra regelfila `koder2/koderegler-gjenvunnet.md`
(sha256 `234695dd…`, PREREG-v1 § 2 og § 5, ADDENDUM-03 § 1.2, -04 § 4, -05, -10 § 1–3) for mennesker: samme regler, uten
prosjektinterne henvisninger. Endrer ingen regel. På engelsk fordi tekstene er engelske.*

## Your task

You will read short passages from published research articles (most in English; a few in other languages — code them if
you can read them, otherwise mark `tvil = yes` and say so in the comment). Each passage is about five sentences long.
For each passage, decide whether it contains a **parked question** as defined below, and if so, which kind of obstacle
it names.

You see only the passage. You do not see which article it comes from, how it was selected, or what anyone else —
person or software — said about it. Do not look the passage up. Decide on the text and this codebook alone.

## 1 What counts as a hit

A passage is a **hit** when all four conditions hold:

1. **Something was not done.** The authors say that something they wanted, planned or would have needed to do in
   *this* study was not done, not completed, or done only partly.
2. **An obstacle is named.** The passage states a reason why it was not done.
3. **The two are linked.** The obstacle is given *as the reason* for the undone thing — not merely mentioned nearby.
   Both must lie within the passage (they may be in different sentences).
4. **It belongs to this study.** The undone thing is part of the research the article reports.

**Not hits** (record the code in the class column):

| code | what it is | example (constructed) |
|---|---|---|
| **N1** | the undone thing is done later in the same article | «We could not measure X directly; Section 4 therefore estimates it from Y.» |
| **N2** | a novelty claim | «To the best of our knowledge, this is the first study of X.» |
| **N3** | a scope choice or simplification **without a named obstacle**, including assumptions the authors chose themselves | «We restrict the analysis to adults.» / «X cannot be assessed given our assumption of Y.» |
| **INGEN** | none of the above; no undone work is declared | ordinary description, results, references, tables |

Also **not hits**:

* **A gap in the field.** «Little is known about X», «no study has examined X» — this is about the literature, not
  about something the authors left undone.
* **Someone else's practice.** What an organisation routinely does, what other researchers did not do, or advice to a
  third party.

**But:** a **review** that says *it itself* could not do an analysis because the primary studies did not report what was
needed, **is** a hit (class H7). The difference from a field gap is who owns the undone step.

## 2 The obstacle classes (for hits only)

| class | obstacle | example (constructed) |
|---|---|---|
| **H1** | human reading or coding at scale — too much material to read or code by hand | «The remaining 3,000 letters could not be transcribed within the project.» |
| **H2** | legibility — handwriting, damaged source, poor audio | «The inscription on the base is too worn to be read.» |
| **H3** | language barrier | «Sources in Arabic were not consulted, as the author does not read the language.» |
| **H4** | pattern detection in large volumes of images or signals | «Manual inspection of all 40,000 images was not feasible.» |
| **H5** | computation, solver or tool limit — run time, memory, a parameter the software does not accept | «The model could not be run for all scenarios within available computing time.» |
| **H6** | inferring structure from sequences | «The secondary structure could not be predicted from the sequence alone.» |
| **H7** | **the data did not exist** — never collected, not recorded, not reported in the sources | «No samples were preserved, so the layer could not be dated.» |
| **H8** | access, law, ethics, consent | «The interview data cannot be shared under the consent given.» |
| **H9** | the concept, method or theory was missing | «There is no accepted way to separate the two effects.» |

**When the passage does not say which of two neighbouring classes applies, do not guess.** Code it as
`<class>/H7-uavklart` (undecided) — for example `H1/H7-uavklart` when it could be either «too much to read» or «the data
did not exist», and the passage does not say. Undecided is a coding rule, not a licence: if the text states the reason,
code the reason.

**Model and tool limits** split three ways: a named computing or software limit → **H5**; a missing method or concept →
**H9**; a simplification the authors chose without naming an obstacle → **N3** (not a hit).

## 3 The form (`skjema.csv`)

One row per passage, in the order of the file:

| column | value |
|---|---|
| `id` | as given (MV-001 …) |
| `annotator` | your initials |
| `treff` | `yes` / `no` |
| `undone_sentence` | for hits: the words that state what was not done (copy ≤ 15 words) |
| `obstacle_sentence` | for hits: the words that state the obstacle (copy ≤ 15 words) |
| `klasse` | for hits: H1–H9 or `<class>/H7-uavklart`; for non-hits: N1, N2, N3 or INGEN |
| `uavklart` | `yes` if you used an undecided value |
| `tvil` | `yes` if you were genuinely unsure whether it is a hit |
| `kommentar` | optional, one sentence |

## 4 Practice

Before the real file you get ten practice passages with the answers (not part of the sample). Read the answers only
after coding all ten. Do not discuss the real passages with the other annotator until both of you have submitted.

## 5 Time

Expect 1–3 minutes per passage; about 149 passages; plan for 4–6 hours over at least two sittings.
