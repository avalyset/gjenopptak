# Faktasjekk av MANUSKRIPT-v2.6-UTKAST — sjette runde, bare de endrede linjene — 30.09.2026

**Manuskript:** `docs/MANUSKRIPT-v2.6-UTKAST.md`, sha256 `ea9677e480943c947488d37cd9715f34696559df262a63443ef55bbf422d05b8`.
**Fasit:** faktafila § 9 «Fase 3 / ADDENDUM-25» fra `0d72813` (sha256 `bce68e13f4da269c…`), og kildene den peker på.
**Ingen prosa er omskrevet.**

**Mandat (eierens avgjørelse 30.09.2026):** bare linjene som er endret fra v2.5 — sammendraget (l. 36–41), § 1 (l. 82–83),
silavsnittet (l. 178–180), § 4.7 (l. 429–478), begrensning 7 (l. 542–544) og headeren (l. 3–12) — mot den nye seksjonen.
Radfil på Vault: `manuskript/faktasjekk-v2.6/rest.jsonl` (sha256 `01629797dafe15b4…`). Ingen nettkall.

## Stemmer

Hvert tall i de endrede linjene står i faktafila § 9 med samme verdi: port (1) 85/100 [76,7–90,7] mot 0,70; recall
95/104 = 91,3 % [84,4–95,4] og 85/104 = 81,7 % [73,2–88,0]; 104 treff i 20 verk; tap 9 i silen og 10 hos leseren;
21 361 tekstbiter, 2 188 flagget, 1 923 vinduer, 1 357 byte-identiske (RESULTAT § 0.5); union 4 107 = 19,2 % mot
12,8 %; 14 leserøkter, alle `claude-opus-5`; 673 treff = 16,4 % i 73 av 100 verk; 97,4 % / 77,4 % etter leserens
tvil; H7 63,2 %; løftbar 101/628 = 16,1 % og uavklart 45/673 = 6,7 % mot 19,0 % og 6,0 %; 6,73 mot 10,96 per verk;
31,5 mot 40,6 per 1 000 korpus-tekstbiter; 79,5 M kontekst-tokens; 139 053 per bekreftet treff; OpenAlex 985 etter.
Påstander uten tall, kontrollert mot kildene: **låst før trekkingen** (`f19a3e3` 11:04:36, utvalget skrevet 11:14:53,
28.09); **ingen av de 100 blant de første 100** (overlapp 0 mot `kandidat432`); **referanseutvalget med samme frø**
(`random.Random(734248).sample`, `draw_fase3.py:152`); **oppdraget byte-identisk med malen** (RESULTAT § 1.1);
**samme tall som den post hoc porten** (85/100, faktafila § 3).

## Rest — 9 rader

| linje | manuskriptet sier | riktig | kilde | status |
|---|---|---|---|---|
| 37, 434 | «with the chain unchanged» / «applied the unchanged chain» | ADDENDUM-25 § 4: eneste kodeendring i kjeden er `--utvalg` (før låsen); etter låsen rettes registerleddet (v0.4.0-bygget, RESULTAT-ADDENDUM-25 § 0.8) | ADDENDUM-25 § 4; RESULTAT § 0.7–0.8 | **upresist** |
| 437 | «read cover-to-cover by an agentic Opus instance» | 20 instanser, én per verk (R01–R20) | Vault `fase3/referanse/bruk/R01–R20.json`; FAKTA § 9, kostnadstabellen (referansesett, 20 økter) | **feil** |
| 439–440 | «the resume routine refuses to start the sieve until the reference set is complete» | rekkefølgen holdt — nøkkelen sikret 10:20:05 UTC, kjeden opprettet 10:20:34 UTC — men porten kom i kode 13:04 UTC (`6d905cd`), etter at silen startet; ved silstart var den prosa | MANIFEST-VAULT (NOKKEL-rad), `tilstand.json` `opprettet`, `git log 6d905cd`, RESULTAT § 0.3 | **upresist** |
| 445 | «the run was interrupted once by a session crash» | kjøringen ble avbrutt fire ganger: krasj 29.09 (ekstraksjon), sandkasseblokkering 30.09 (12 leserøkter, 0 dømt), øktgrensen i økt 3 og i økt 7; sandkasseblokkeringen nevnes ikke i utkastet | RESULTAT § 0.5, § 0.6, § 0.7 | **ufullstendig** |
| 462–463 | «it replaces “not measured” in the register header for this run only» | registerhodets skjema tillater bare «ikke målt» (`forbehold.silrecall`, enum med én verdi); uten skjemaendring sier hodet for fase 3 «ikke målt». Skjemaendring er ikke autorisert (registerleddet er eneste kodeendring etter lås) | `src/gjenopptak/schemas/registerhode.schema.json` | **feil — eier avgjør: skjema eller setning** |
| 470 | «(31.5 per 1 000 passages against 40.6)» | nevneren er korpus-tekstbiter; per 1 000 dømte er 163,9 mot 276,8. § 7 gir ingen nevner; faktafila fører begge og velger ingen | FAKTA § 9, felt-tetthet | **upresist — nevneren må navngis** |
| 471–472 | «139 053 per confirmed hit, against about 165 000 on the first material» | 164 805 i ADDENDUM-22 § 10 er per leser-treff, ikke per bekreftet treff. Samme enhet: 118 185 per leser-treff mot 164 805 | FAKTA § 9, kostnad; ADDENDUM-22 § 10 | **feil — ulike enheter** |
| 472–477 | «Three deviations are recorded» | RESULTAT-ADDENDUM-25 fører flere: modell-ID fra konfigurasjonen (§ 0.2, nå verifisert fra utskrift), referanseporten var prosa og gjenopptak fra worktree (§ 0.3), ekstraksjonsavbruddet (§ 0.5), sandkasseblokkeringen (§ 0.6), øktgrensen og registeret (§ 0.7), feltnavnet `ekte_treff`/`treff` (§ 1.1), OpenAlex før-verdi (§ 1.5) | RESULTAT-ADDENDUM-25 § 0.2–0.7, § 1.1, § 1.5 | **ufullstendig** |
| 5–7 | «written from `docs/MANUSKRIPT-FAKTA-2026-09-28.md` (commit `acfd915`)» | fase 3-seksjonen (§ 9) står i `0d72813`; etter denne runden er § 4.7 kontrollert mot den | `git log` | **utdatert etter denne runden** |

Fordelt: **3 feil** (l. 437, 462–463, 471–472), 3 upresise, 2 ufullstendige, 1 utdatert etter denne runden.
**Én av dem krever en avgjørelse, ikke en omskriving:** l. 462–463 kan bare bli sann hvis registerhodets skjema får
en målt verdi for `silrecall`. Det er en kodeendring ut over registerleddet, og den er ikke gjort.

**Observert utenfor mandatet** (uendret linje, ikke kontrollert som del av runden): l. 584 sier at utkastet er
revidert «four times against fact-check reports», mens l. 5–6 nå nevner fem (`136d025`, `b084ba2`, `faaaddc`,
`c4d645c`, `ffeaccf`); med denne blir de seks.
