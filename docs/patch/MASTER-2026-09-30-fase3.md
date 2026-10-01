# Patch til MASTER — fase 3 (ADDENDUM-25): prospektiv port, første silrecall

**Skrevet 30.09.2026.** Gjelder MASTER v0.3 (`master/arkiv/MASTER_GJENOPPTAK_v0_3_2026-09-28.md`, sha256
`46aeb328b4b04ab6…`, pekt til av `POINTER.txt`). Patchen påføres i bumpen til v0.4 med `~/bin/bump-master.sh
gjenopptak`; MASTER er ikke redigert. Hvert tall under står med sti og sha i `docs/MANUSKRIPT-FAKTA-2026-09-28.md`
§ 9 og i `docs/RESULTAT-ADDENDUM-25.md` § 1.

---

## § 0 · statusblokk, teksten som skal inn

**Statusblokk 30.09.2026.** Denne versjonen påfører `docs/patch/MASTER-2026-09-30-fase3.md`. Det som endret seg
fra v0.3:

* **Fase 3 er gjennomført og målt (ADDENDUM-25).** 100 nye arkeologiverk, porter, regelfil og kjede låst før
  trekkingen, et referansesett på 20 verk lest og sikret før silen. **Port (1) bestått: 85 av 100 = 85,0 %
  [76,7–90,7] mot 0,70.** Lista heter **«arbeidsliste (prospektiv port)»** — den første i sporet. **Første målte
  silrecall:** silen beholdt **95 av 104 = 91,3 % [84,4–95,4]** av referansetreffene, leseren bekreftet **85 av
  104 = 81,7 % [73,2–88,0]**.
* **Én endring i et ledd etter låsen** (referanseporten i `cli.py` 28.09 rører ikke noe ledd): registerleddet skrev et hode som brøt sitt eget skjema; rettet,
  radene uendret (`kjede/ledd.py` `07fc3a77…` → `39f8b9de…`, RESULTAT-ADDENDUM-25 § 0.8).
* **Leserleddet førte seg ferdig to ganger uten utdata** (sandkassen 30.09 morgen, øktgrensen to ganger).
  Gjenopptaksrutinen etterkontrollerer nå hvert ledd og fullfører delvise økter uten å skrive over dømte
  (LAERDOM § 45).
* **Zenodo v0.4.0 er bygget på nytt med utfallet: 112 filer, ikke publisert.** Manus v2.6 er det nyeste utkastet;
  sjette faktasjekk ga 9 rader rest.
* Tallene fra v0.3 står uendret for de første 100 verkene: kandidatlista 432 rader, post hoc port 85 %
  [76,7–90,7], den preregistrerte porten falt på 21 av 27.

## § 1 · ledd 3-status, linjene som skal rettes

**Erstatter** avsnittet som begynner «**Ledd 3 står uendret.**» — første setning — og «**Statusen ledd 3 skal
bære:**»:

> **Ledd 3: vist prospektivt på ett felt, 100 verk.** På 100 nye arkeologiverk, med porter, regelfil og kjede
> låst før trekkingen, bestod lista en blind presisjonsport på **85 av 100 = 85,0 % [76,7–90,7]** mot 0,70, og
> silen beholdt **95 av 104 = 91,3 % [84,4–95,4]** av treffene et referansesett lest perm til perm før silen
> fant (ADDENDUM-25, RESULTAT § 1). Avgrensningen følger statusen: **ett felt** (arkeologi, som hadde høyest
> treffrate av de fire), **100 verk**, recall mot **én LLM-lesning av 20 verk** i samme modellfamilie og med
> samme regelfil, ikke mot et menneske. De tre andre feltene er ikke prøvd prospektivt.

> **Statusen ledd 3 skal bære:** *vist prospektivt på ett felt, 100 verk.* Silen er en sil, leseren er Opus
> agentisk, og kostnadsenheten er frontier-lesninger per bekreftet treff: **139 053 kontekst-tokens per
> bekreftet treff** i fase 3 (leserens 673 treff × presisjon 0,85 = 572), **118 185 per leser-treff** mot 164 805
> på de første 100.

Resten av avsnittet — ekstraksjonen per dokumentvindu målt og død (9 av 25), kaskaden, unionen på 27 av 27 —
står uendret: det er historien til silen fase 3 brukte.

## § 4 · resultater, ny underseksjon etter «Nevneren, og hva N inneholder»

### Fase 3 — prospektiv port på 100 nye arkeologiverk (ADDENDUM-25)

| mål | tall |
|---|---|
| tekstbiter / dommer-flagget / unionen | 21 361 / 2 188 / **4 107 = 19,2 %** av korpuset (de første 100: 12,8 %) |
| leserens treff | **673 av 4 107 = 16,4 %** [15,3–17,6], i 73 av 100 verk |
| **port (1) blind presisjon** | **85 av 100 = 85,0 % [76,7–90,7]**, terskel 0,70 → «arbeidsliste (prospektiv port)» |
| presisjon, leserens `tvil: false` / `true` | 37 av 38 = 97,4 % / 48 av 62 = 77,4 % |
| **port (2) beholdt av silen** | **95 av 104 = 91,3 % [84,4–95,4]** |
| **port (2) bekreftet av leseren** | **85 av 104 = 81,7 % [73,2–88,0]**; tapene 9 i silen, 10 hos leseren |
| H7, av alle treff | 425 av 673 = 63,2 % |
| løftbar H1–H6, av avklarte / uavklart, av alle | 101 av 628 = 16,1 % / 45 av 673 = 6,7 % (de første 100: 19,0 % / 6,0 %) |
| treff per verk | 6,73 (de 25 første arkeologiverkene: 10,96) |
| modell-ID | 14 av 14 leserøkter som dømte: `claude-opus-5`, fra øktutskriftene |

**Ikke påstå:** at porten er vist for andre felt; prevalens; at «bekreftet» er menneskelig validering; at
tetthetsforskjellen mot de 25 første arkeologiverkene er et funn om feltet (FAKTA § 9, siste underseksjon).
**Registerhodet bærer `silrecall: "ikke målt"`**, fordi skjemaet bare tillater den verdien; tallet står i
RESULTAT § 1.2.

## § 9 · åpne poster

**Rettes i «Lagt til 27.09.2026»**, siste punkt («Den preregistrerte porten falt, og lista heter
kandidatliste … En arbeidsliste kan bare komme fra en prospektiv port på nytt materiale.»), med tillegget:

> **→ 30.09.2026: fase 3 ga den.** «Arbeidsliste (prospektiv port)» for 673 rader i 100 arkeologiverk
> (ADDENDUM-25). Kandidatlista på 432 er uendret kandidatliste.

**Strykes i «Lagt til 28.09.2026»:** «Fase 3 og 4 er ikke definert i denne versjonen …» → **STRØKET 30.09: fase 3
er definert (ADDENDUM-25), kjørt og målt.**

### Lagt til 30.09.2026

* **Zenodo v0.4.0: bygget, ikke publisert — eierens go.** 112 filer (`zenodo/v0.4.0-bygg/UTGIVELSE-0.4.0.json`,
  HEAD `6c3a26f`). To fase 3-nøkler er med i depositumet, mot portstatusens linje om at nøklene holdes utenfor —
  **eierens valg** (portstatus § 1.1). `CITATION.cff` og `ZENODO.md` fylles ved publisering.
* **`silrecall` i registerhodet kan bare være «ikke målt».** Manus v2.6 l. 462–463 sier at det målte tallet
  erstatter «not measured» i hodet for denne kjøringen. Enten endres skjemaet (en kodeendring ut over
  registerleddet), eller setningen. **Eierens avgjørelse.**
* **Manus v2.6: 9 rader rest** fra sjette faktasjekk (`docs/FAKTASJEKK-MANUSKRIPT-v2.6-2026-09-30.md`): 20
  referanseinstanser, ikke én; referanseporten var prosa da silen startet; fire avbrudd, ikke ett;
  kostnadssammenligningen blander per leser-treff og per bekreftet treff; flere avvik enn tre.
* **Kjent gjeld i kjeden, nå som låsen er innfridd:** `steg_les` fører seg ferdig uten fullt antall (klasse A,
  sett to ganger); ekstraksjonen fortsetter ikke et påbegynt ledd; `CCLeser` fører ikke `modelUsage`; «ferdig»
  bør nøkles på inndata-sha (LAERDOM § 44–45). Hver i egen commit.
* **Trekkingen fører ikke OpenAlex-kvoten før**, bare etter (985); ADDENDUM-25 § 6 ba om begge.
* **Kandidatlista på 432 er ikke i depositumet** (heller ikke i v0.3.0), mens README viser til den.
* **Navnekontrollens skanner skal flyttes til `src/`**, som NAVNEKONTROLL lovet «når fase 3 er ferdig».
* **Fase 3 for de tre andre feltene er ikke definert.** Ledd 3 er vist på arkeologi, feltet med høyest
  treffrate; det svakeste feltet (energimodellering, 6,0 %) er der porten er minst sikker.
* **Fase 3 hadde ingen sakbehandling.** ADR-0013 ba fase 3 rapportere vilkårsfordelingen; den finnes først når
  saker tas fra arbeidslista.

## Changelog-rad

| **0.4** | **30.09.2026** | Patch `MASTER-2026-09-30-fase3.md` påført: fase 3 målt (ADDENDUM-25), ledd 3-status «vist prospektivt på ett felt, 100 verk», ny underseksjon i § 4, § 9 à jour (to poster rettet/strøket, ni nye). |

---

**Observert, ikke del av patchen:** § 1 «Svaret på del D» i v0.3 bærer «98 % på de radene leseren ikke er i tvil
om», «164 805 kontekst-tokens per bekreftet treff» og «17,8 % [14,5–21,7] av treffene har løftbar klasse». Alle tre
er rettet i `docs/KORRIGENDUM-2026-09-28-frys-v0.4.0.md` (97,6 % i en post hoc delgruppe; 164 805 per meldt treff,
≈ 194 000 per bekreftet; 19,0 % av avklarte). De bør følge med i samme bump.
