# Gjenopptak

A preregistered study of **why research gets parked**: how often authors record work they did not
get done, and which obstacles they name when they do.

The primary result is the distribution of obstacle types, not the tool used to find them.

## What was measured

100 open-access works from four purposively chosen fields — energy modelling, archaeology, clinical
epidemiology, textual scholarship — parsed into 66,833 sentences and 22,243 passages. A local model
(gemma2:9b, temperature 0, fixed seed, weight hash logged per judgment) classified every passage
against a typology locked before data collection. A stratified sample of 320 passages was then read
blind by the coder, with the key opened only after all verdicts were written.

| | |
|---|---|
| Prevalence, corrected (M1) | **0.671** |
| Judgeability (M2) | **88.0 %** |
| Obstacle distribution, 25 true hits | **H7 17, H5 3, H8 2, H2 2, H9 1** |
| Liftable share (classes H1–H6) | **5 of 25** |
| Judge precision | 16.7 % [11.6–23.4] |
| Implied judge recall | ≈ 46 % |

Seventeen of 25 surviving true hits are H7: the question was parked because the data did not exist.
Full numbers with per-number sources are in `docs/RESULTAT-PORT-v1.md`; the reasoning chain, loop by
loop, is in `docs/LAERDOM.md`.

## What is not shown

* **Not that the detector works.** Precision is 16.7 % and the implied recall about 46 %. It is
  reported as an instrument with measured error, and every prevalence figure is corrected for it.
* **Not a prevalence for science as a whole.** Four fields, chosen on purpose, with an open-access
  and retrievability filter that skews the frame toward preprint and MDPI-like channels
  (`docs/LAERDOM.md` §3).
* **Not inter-coder agreement.** One coder read the sample; κ against an independent annotator has
  not been measured.
* **Not that AI can unpark these questions.** One case was carried out in full (`docs/PS-246-RESULTAT.md`),
  using equations published in 2006. It demonstrates that the chain find → classify → falsify →
  execute can run end to end. It says nothing about how often it does.

## Reproducing the port from the frozen lists

The frame lists are frozen and hashed, so the sampling can be replayed without spending quota:

1. Fetch the frozen frame for a field from the external volume: `frames/frame-<field>-RAW.jsonl`,
   with the row count and sha256 recorded in ADDENDUM-08 §5.
2. Draw with the preregistered seed (`05988b23`) in the order fixed by ADDENDUM-09: shuffle the
   sorted frozen list with `random.Random(0x05988B23)`, test retrievability in draw order, stop at
   25 retrievable works per field. `src/gjenopptak/harvest/draw.py` implements this; the draw log
   `utvalg/trekklogg-<field>.jsonl` records every decision, including exclusions.
3. Rebuild passages: `python -m gjenopptak.classify.port_run bygg` (±2 sentences, stride 3).
4. Re-judge: `python -m gjenopptak.classify.port_run døm --felt <field>`, with the model and prompt
   hashes in `data/port/spesifikasjon.json`. Determinism was verified at 47/47 and 50/50 re-runs.
5. Re-measure: `presisjonssett-bygg` and `presisjonssett-mål` reproduce the precision set, given the
   same measurement seed (`734248`).

Writing modules require the external volume to be mounted (ADR-0009); they refuse to start without
it rather than writing to the system disk.

## Running the chain on your own works

The whole pipeline is one command. It is defined by **ADR-0012** and built to the requirements in
`docs/BYGGEPLAN.md` (B1): frame → fetch → text units → sieve → reader → register.

### Install

```
git clone <this repo> && cd gjenopptak
python3.12 -m venv .venv && .venv/bin/pip install -e .
```

Three things must be present before the chain will start, and it refuses rather than warns:

* **The external volume** (ADR-0009). `require_vault()` runs first; there is no fallback to the
  system disk.
* **Ollama** with `gemma2:9b` pulled, reachable at the host in `kjede.toml`. The weight sha256 is
  checked against the manifest before and after a batch (ADR-0008).
* **Claude Code with Opus** for the reader step, on a subscription. Sign in once —
  `claude auth login` (not `claude login`; the subcommand is under `auth`) — and check it with
  `claude auth status`. With `--leser cli` the chain says so plainly if the session has expired. One-call models are sieve-class,
  not readers (ADR-0012); the chain will not substitute one, and it holds no API key to do it with.

### Configure

Everything that decides a number lives in one file, `kjede.toml`: model, seed, `num_ctx`, session
size, thresholds and paths. **No path is hardcoded in the code.** Paths in the file are resolved
against the directory the file sits in, so a checkout elsewhere needs no edits except the volume
root.

Check what the chain can see before running anything:

```
gjenopptak kvote
```

It prints the reader quota, the volume, and verifies the sha256 of every locked file the chain reads — the judge prompt, the extraction
prompt, the non-prose rule, the reader's rule file and the reader's assignment template. If one
differs, the chain stops.

### A field is a file

Everything that makes a field a field lives in `felt/<name>.yaml` — the OpenAlex topic ids, the year
span, the frozen frame list with its sha256, and the thresholds. **Adding a field takes no code
change:** drop the file in and `--felt <name>` finds it.

```yaml
felt: arkivvitenskap
topics: [T11657]
ar: [2015, 2020]
ramme:
  fil: frames/frame-arkivvitenskap-RAW.jsonl
  sha256: 0000…                 # zero until the frame is frozen
  rader: 149061
terskler:
  n_verk: 25
  gulv: 0
```

The topic ids come from the **query** recorded in the frozen raw manifest, not from the works' own
`primary_topic` — those are the query's *result*, hundreds per field, and cannot define it. The frame's
sha256 is what proves the list has not moved: if the file is there and the hash differs, the field is
refused. If the frame does not exist yet, the field is **plannable but not runnable** — `--torr` costs
out building it, a real run requires it.

### Run

Put one OpenAlex work id per line in a file:

```
W2781414149
W7165238126
```

Then, in order — the dry run first, because it reports cost before anything is fetched:

```
gjenopptak run --verk verk.txt --navn min-kjoring --torr
gjenopptak run --verk verk.txt --navn min-kjoring
```

The dry run reports passages, reader sessions, context tokens, harness tokens and hours, computed
from measured consumption (25 034 context tokens per passage, 287 533 harness tokens and 29.5
minutes per session of 356). **The quota gate is a gate, not a warning:** a phase it cannot finish
is refused, and the message says how much is missing.

**The reader quota cannot be read from code, and that is not an oversight.** The weekly plan limit
lives in Claude Code's own account state: there is no `claude usage` subcommand, no documented API for
it, and no settings file that carries it — only the in-session usage card. So the chain cannot read it,
and it refuses a reader phase rather than guessing. Write it once per week, from what the usage card
shows:

```
gjenopptak kvote --skriv-harness 55
```

**The tool makes no calls to the Anthropic API.** The reader is a Claude Code instance on the Max
subscription — nothing else. There is no key path in the chain, so there is no key to leak, and the
quota gate refuses any phase that would call the API rather than reporting missing credit (ADR-0012,
dated addition 27.09.2026). `falsify` calls Europe PMC and Crossref; those are not Anthropic.

### The ten steps

Each step can be run alone with `--from`/`--to`, and each resumes: an interruption costs time, not
work. Further reading: [`docs/METODE.md`](docs/METODE.md) is the method in full — its stated stopping
condition is that an outsider can run the port on a new field from it alone.
[`docs/FELTGUIDE.md`](docs/FELTGUIDE.md) is how to add a field and what the numbers mean for it.
[`docs/UTGANG.md`](docs/UTGANG.md) explains one output row field by field.

| step | does | output |
|---|---|---|
| `hent` | resolves or fetches full text to the volume, one manifest row per file | `1-hentet.jsonl` |
| `tekstbiter` | sentence ± 2, stride 3; refuses if any sentence is uncovered | `2-tekstbiter.jsonl` |
| `dommer` | `gemma2:9b`, explicit `num_ctx`, signature per verdict, canary first | `3-dommer.jsonl` |
| `ekstraksjon` | the ADDENDUM-16 prompt, `num_ctx` 8192, all-matches coupling | `4-ekstraksjon.jsonl` |
| `union` | A ∪ B; non-prose marked with the versioned rule, never removed | `5-union.jsonl` |
| `blind` | blind files (`id` and `tekst` only, shuffled), assignment from template, generated blocklist, key to the volume | `blind/` |
| `les` | starts reader sessions **serially**, one at a time, own scratch dir, verifies id order and fields, logs consumption | `7-verdikter-okt-N.jsonl` |
| `verksniva` | material access per work, criterion ported verbatim from the locked script | `7b-verksniva.jsonl` |
| `falsify` | citation coverage per DOI, self-arming — an unarmed zero is not an answer | `7c-falsifisering.json` |
| `register` | claims-2 rows with `tvil`, `sil`, `verksniva` and coverage, plus a header naming the gate | `8-register.jsonl` |

```
gjenopptak run --verk verk.txt --navn min-kjoring --from dommer --to union
```

The reader step has two modes. `--leser cli` starts the session headlessly with `claude -p`; it needs
`claude login` to have been run once, and says so plainly if the session has expired. `--leser subagent`
is for running the chain from inside a Claude Code session: it lays out the assignment and the output
path and waits, so the orchestrating session spawns the reader with its own subagent tool. **Sessions
are serial in both modes** — seven parallel Opus instances hit the provider's session limit at 87 %
coverage, and that is why.

Steps 3, 4 and 7 accept a cache, so a re-run does not repeat work already done:
`--cache-dommer data/port`, `--cache-ekstraksjon <log>`, `--cache-leser <dir>`.

### Read the output

`8-register.jsonl` has one row per confirmed hit. Each row carries its own uncertainty: the sieve
source and that source's measured precision (`begge` 34.5 %, `dommer` 14.3 %, `ekstraksjon` 7.2 %),
the reader's `tvil` flag with the precision that applies to it (97.6 % without doubt, 75.9 % with),
the non-prose mark, and liftability with the date it was assessed (ADR-0010).

**Two registers exist, and they are not versions of each other.** `register/claims.jsonl` on the
volume is the original: 30 rows built from coder 1's gold set, `schema_version` `claims-2`, untouched.
`kandidat432/8-register.jsonl` is the candidate list the chain produced: 432 rows from the reader's
verdicts over the sieve union, same schema plus the `tvil`, `sil` and `leser` fields. The first is a
reference set; the second is a candidate list that passed a post-hoc gate. Cite them separately.

The 50 rows with a liftable or unresolved class and no doubt flag — the combination where blind
precision measured 98 % — are written out for case work in
`docs/SAKBEHANDLING-2026-09-27-kandidater.md`.

`8-register-header.json` names the gate. **Without a passed gate it says `ubekreftet
kandidatliste`, and that is not a bug.** A list is only a work list after a prospective gate on new
material; a post-hoc gate gives `kandidatliste (post hoc port)`. The header also carries the global
caveats: the gold set's stable core is 3 of 27, and the N3 boundary carries coder identity
(5.8–13.6 % between coders).

## History, and what to cite

**This repository starts at a single root commit.** The full development history — 143 commits, each
locked file committed alone with its own sha256 — is **not** here. It is in the git bundles deposited on
Zenodo: `git bundle --all`, one per release, listed with sha256 in `MANIFEST-VAULT.md` on the external
volume. Clone the bundle from the Zenodo record to get the history:

```
git clone gjenopptak-<date>-<sha>.bundle gjenopptak-full
```

**Reproducibility is anchored in the DOI and the ADR number, not in commit hashes.** A commit sha in
this repository does not correspond to anything in the deposits, and no document cites one. What the
documents cite instead:

* **the concept DOI `10.5281/zenodo.22959326`** for the record as a whole, and a version DOI for a
  specific state — `10.5281/zenodo.22976464` is v0.3.0;
* **ADR numbers** (`docs/decisions/`) for the decisions the method rests on — ADR-0012 is the chain,
  ADR-0009 the external volume, ADR-0010 that liftability is dated, ADR-0003 the model signature;
* **addendum numbers and their sha256** for the preregistered measurements, with the locked files
  copied verbatim into `repo/laste-filer/` in each bundle.

Any of those three can be checked without this repository's history. That is deliberate: the audit
trail lives in the deposits, which are immutable, rather than in a branch that can be rewritten.

## Publication policy — the `offentlig` branch

This repository publishes **states, not history**. The rule is fixed (ADR-0012, dated addition
2026-09-28) so that it does not have to be decided under pressure:

* **`main` is never pushed.** It carries the full working history — one author, hundreds of commits,
  every wrong turn and every correction. That history is preserved in the canonical `git bundle --all`
  archives on the project volume and in the Zenodo deposits.
* **`offentlig` is the published branch.** It consists of the **root commit plus exactly one release
  commit per MASTER version**. The tree of each release commit is the state of `main` at the moment that
  MASTER version was set; its parent is the previous release commit. No commit from `main` is ever
  carried over.
* **Each release commit is tagged `vX.Y`**, matching the MASTER version, which is also named in the
  commit message. One tag, one MASTER version, one release commit.
* **Never force-push.** Every push is a fast-forward adding exactly one commit. If it is not a
  fast-forward, something is wrong and the answer is to investigate, not to force.
* **A secret scrub runs over the release tree before every release commit** — eleven patterns covering
  API keys, private keys, bearer tokens, private and business email addresses, absolute home paths.
  Matched values are never printed, only the pattern name, file and line.
* **If a release names people other than the manuscript's authors, the owner reads those files before
  the push.** This applies to `docs/saker/*`, the case register and the triage, which name the authors
  of the works the cases are about.

**Consequence for readers:** you cannot see commit-by-commit history here, and that is deliberate. What
you can do is cite an exact state — a tag, a MASTER version, and a Zenodo DOI that all name the same
tree.

## Licensing

| What | License | File |
|---|---|---|
| Source code in `src/` and `tests/` | Apache-2.0 | `LICENSE` |
| `PREREG-v1.md`, `ADDENDUM-01..10`, `docs/**`, the register and the data | CC BY 4.0 | `LICENSE-DATA` |

Quoted passages from published works remain under their rights holders' terms; the CC BY grant
covers this project's own coding, measurement and prose.

## Where the data lives

**Data are not in git.** Frozen frame lists, samples, full texts, judgments, the precision set and
the register are held on an external volume under `gjenopptak-kilder/`, with every file listed by
sha256 in `MANIFEST-VAULT.md` there. `data/` is git-ignored; the repository carries code, protocol,
decisions and results only. Paths written as `data/...` in the protocol and the addenda refer to
that material: it now lives on the external volume under `raw/`, `frames/`, `utvalg/`, `logs/` and
`register/`, and every file is listed by sha256 in `MANIFEST-VAULT.md`.

The register (`register/claims.jsonl`) follows ADR-0010: each entry carries dated liftability
assessments, appended and never rewritten, so a class that changes over time keeps its history.

Documents are mirrored to `resultat/` on the same volume. The mirror is compared on **content**, not
on timestamps: `python -m gjenopptak.speil --check` reports any file that lags its source in the
repository, and the check runs first in `securerepo`, before the branch that writes no bundle. That
branch is how three mirrored files stood with a superseded author name for a day.

## Repository layout

```
PREREG-v1.md            protocol, locked before data collection
ADDENDUM-01..10.md      corrections and extensions, each committed alone with its own sha256
docs/decisions/         architecture decision records (ADR-0001..0011). **Numbers are unique
                        per repository, checked against all refs** — not against HEAD, not against
                        the current branch (repo discipline G1). 0005 and 0006 were burned here
                        under an earlier, mistaken convention that allocated numbers across
                        EcoDeco repositories; they are left unused rather than reassigned, so a
                        number never means two things. Corrected 2026-09-26.
docs/LAERDOM.md         findings log: what was measured, which number, which conclusion
docs/RESULTAT-PORT-v1.md    result note, source per number
docs/MANUSKRIPT-v0.1.md     manuscript draft
src/gjenopptak/         harvest, parse, extract, classify, falsify, vault
tests/                  348 tests (1 network test deselected by default), including
                        the reproduction of Saxton & Rawls Table 3 and the mirror check
```

## Statements superseded in locked files

`PREREG-v1.md` and `ADDENDUM-01..09` are locked with known sha256 and are never edited. A statement
in them that a later measurement superseded was not wrong when written; it is recorded as superseded,
in a dated file alongside:

* `docs/INNHENTET-2026-09-26-en-koder.md` — «Én koder» in PREREG-v1 §9 (locked 2026-09-12) was
  superseded on 2026-09-25 by the independent recoding in ADDENDUM-11 (κ = 0.81 [0.70–0.91]). The
  same phrase in ADDENDUM-06 §1.6 remains true, but describes the recall fasit only.

## Citation

See `CITATION.cff`. The DOI field is deliberately empty until the deposited version has one.
