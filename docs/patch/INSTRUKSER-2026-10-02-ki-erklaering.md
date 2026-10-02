# Patch til instruksfila — KI-bruk erklæres som verktøy, aldri som forfatterskap

**Skrevet 02.10.2026.** Gjelder `docs/INSTRUKSER-v1.3.md` (sha256 `ececde4b…`) og påføres ved neste v-bump
(v1.4). Instruksfila er ikke redigert.

## Erstatter avsnittet «Attribusjon (F2)» (l. 460–461)

**Attribusjon (F2):** author og committer er Eirik. `Co-authored-by` for AI-verktøy er ærlig og greit.
**KI-bruk erklæres som verktøy under forfatterens styring, aldri som forfatterskap.** Den skal aldri skjules:
modellene som forskningsinstrument (koding, ekstraksjon, lesning, sakssteg) rapporteres i metoden med rolle,
modell-ID og reliabilitet, og modellen som skriveverktøy erklæres i en egen seksjon. Erklæringen sier hva
forfatteren gjorde og står ansvarlig for. Den sier ikke at en modell «skrev» utkastet. **Malen er § 8 i
`docs/PREPRINT-v2.md`, ordrett:**

> Language models were used in two roles. As research instruments, they coded passages, extracted
> candidate sentences, read batches and executed case steps under locked instructions; their roles,
> model identities and reliability are reported as part of the method (§2.4, §3.2, §4.2–4.3). As
> writing tools, a large language model (Claude, Anthropic) assisted in drafting and editing the
> manuscript text under the author's direction. The author designed the study, wrote the protocol and
> every criterion, made every decision recorded in the decision records, interpreted the results, and
> revised and approved the final text. Every number and reference was checked against a hash-anchored
> fact file before submission. The author takes full responsibility for the content.

Seksjonsnumrene i malen tilpasses dokumentet den står i. Påstandene i den må være sanne for det dokumentet:
står det at hvert tall og hver referanse er kontrollert, skal kontrollen finnes.

**Bakgrunn:** OSF Preprints' moderasjonsregler sier at innhold som helt eller mest er generert av
språkmodeller, ikke passer på tjenesten (help.osf.io, «Preprint moderation policies»). Preprinten zvc34 ble
avvist 30.09.2026 uten kommentar i OSF. Manus v2.8 § 8 beskrev utkastet som skrevet av en språkmodell. LAERDOM § 49.
