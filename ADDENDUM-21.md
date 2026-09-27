# ADDENDUM-21 — koder 3: er κ = 0,812 reproduserbart?

**Skrevet:** 2026-09-27. **Status: PREREGISTRERT OG UKJØRT.** Kjøres ikke før eieren har avgjort
kvoten. **Gjelder:** om reliabilitetstallet sporet hviler på, er en egenskap ved regelsettet eller et
enkelttrekk.

## 1 Hvorfor

κ = 0,812 er sporets eneste reliabilitetsmåling. Den står i manuskriptet, i resultatnotatet, i to
Zenodo-versjoner og i ADDENDUM-11, og hele argumentet for at fasiten ikke er én leseres idiosynkrasi,
hviler på den. **Men den er målt én gang, av én koder.** ADDENDUM-11 §3 fører selv tre steder
uavhengigheten ikke rekker, og ADDENDUM-11 §8 la til et fjerde: regelfilen bar en `grep -n`-artefakt og
en avkuttet tabell.

Et κ målt én gang kan ikke skilles fra et heldig trekk. ADDENDUM-18 §7 viste hvor skjørt tallet er ved
denne grunnraten: **to snudde verdikter av 302 flyttet κ med 0,041.** Med 34–39 treff i nevneren er
0,812 og 0,70 ikke langt fra hverandre i antall passasjer.

Dette addendumet gjentar ADDENDUM-11 med en tredje koder og måler om tallet kommer tilbake.

## 2 Hva koder 3 får, og ingenting mer

**Én økt, tom kontekst, to filer:**

1. **Blindfilen**, uendret: `data/port-presisjonssett-blind.jsonl`, 320 rader, feltene `id` og `tekst`,
   samme stokking som koder 2 fikk. 227 287 bytes, sha256 `15ce72a7687cea57…`
2. **Regelfilen**, koder 2s gjenvunnede: `koder2/koderegler-gjenvunnet.md` på Vault, 167 linjer,
   9 805 bytes, sha256 `234695dd4e1777a958801ddf6535e6a6444436ea1d46c3121db01585a9108449`.

**Sperret, med filnavn i oppdraget, ordrett som i ADDENDUM-11 §2:** koder 1s verdiktfil, nøkkelfilen,
den sammenstilte fasiten, tvilsfilen, dommerfilene, `presisjon-resultater.json`, LAERDOM,
resultatnotatet, manuskriptet, PS-246-filene, ADDENDUM-10 i sin helhet og alt på Vault utenom
regelfilen. `git log` og `git show` forbudt. **I tillegg sperres nå:** ADDENDUM-11, ADDENDUM-18,
ADDENDUM-20, `koder2-sammenlikning.json`, og denne filen. Koder 3 skal ikke vite at κ er målt før, og
slett ikke hva det ble.

**Ingen forventet treffrate oppgis.** Samme felter som koder 1 og 2: `id`, `ekte_treff`, `min_klasse`,
`min_bedømbar`, `tvil`, `begrunnelse`. Alle 320 i blindfilens rekkefølge, i én sammenhengende økt.

## 3 Hva som endres mot koder 2 — og hvorfor det ikke er en ny test

**Inndata er identisk til byte.** Det eneste som legges til, er registrering:

* **Modellsignatur føres, som ADR-0003 krever:** modell-ID per svar, tokens inn/ut fra `usage`,
  starttid og sluttid. Koder 2 manglet dette i addendumet; det måtte gjenvinnes fra utskriften i
  ettertid (`claude-opus-5`, ADDENDUM-11 §8). Den feilen gjentas ikke.
* **Verdiktfilen skrives til Vault** under `koder3/`, ikke til scratchpad. Koder 2s regelfil gikk tapt
  fordi den lå i scratchpad. Den feilen gjentas ikke.
* **Øktutskriften sikres** med sti og sha ved slutten av kjøringen.

Ingen av de tre rører hva koder 3 leser.

## 4 Regelfilens defekter: to armer, eieren velger

Regelfilen bærer `grep -n`-prefiks på ADDENDUM-05-blokken, seks utelatte linjer i spennet 29–72, og
mangler tabellraden for de tre uavklarte parene H2/H7, H3/H7 og H5/H7.

* **Arm A — filen som den var.** Koder 3 får de samme defektene koder 2 hadde. Dette er den eneste
  armen som gir et **sammenliknbart** κ, og den eneste som svarer på spørsmålet i §1.
* **Arm B — reparert regelfil.** Grep-prefikset fjernet, de seks linjene satt inn, tabellen komplett.
  Måler hva defekten kostet. Ikke sammenliknbar med koder 2, og **ikke** en erstatning for arm A.

**Anbefaling: arm A alene.** Arm B besvarer et annet og mindre spørsmål, og kjøres bare hvis arm A
gir κ under 0,70 — da blir «var det reglene?» det neste spørsmålet, og arm B svarer på det. Kjøres
begge samtidig, er det to tall og ingen rekkefølge å tolke dem i.

## 5 Terskler, fastsatt før kjøring

Koder 2 fikk κ = **0,812** mot koder 1 etter ADDENDUM-10, bootstrap-intervall **0,712–0,917**
(ADDENDUM-11 §4). Alle mål under: paret bootstrap, 10 000 gjentak, frø 734248.

| utfall for κ(koder 3, koder 1) | slutning |
|---|---|
| **innenfor 0,712–0,917** | 0,812 replikerer. Reliabilitetspåstanden står styrket, og «målt én gang» faller bort som svakhet. |
| **≥ 0,70 men under 0,712** | replikerer på klasse, ikke på verdi. Tallet som skal siteres blir spennet over tre kodere, ikke 0,812 alene. |
| **under 0,70** | **0,812 var ikke reproduserbart.** Reliabilitetspåstanden i manuskriptet må svekkes til å gjelde den enkelte kjøringen, og §1s bekymring er bekreftet. Dette er et publiserbart negativt funn, ikke en feil å rette. |

**Rapporteres ved siden av, ikke i stedet for:** κ(koder 3, koder 2); trevegs rå enighet; κ per felt,
med `energimodellering` særskilt, siden det var den svake sømmen hos koder 2 (κ 0,390 mot 0,943 i
biomed); klasseenighet; M2 — koder 1 fikk 88,0 %, koder 2 31,6 %, og hvilken side koder 3 lander på
avgjør om M2 er et mål eller et artefakt av ledeteksten.

**Én ting til, som bare tre kodere kan gi:** de tolv uenighetene mellom koder 1 og 2 er i dag uavgjort,
fordi ADDENDUM-11 §6 slår fast at en avgjørende stemme fra samme orkestrator ikke er en stemme.
**Koder 3 er ikke en avgjørende stemme heller** — samme innvending gjelder — men fordelingen 3-mot-0 /
2-mot-1 over de tolv rapporteres som et *mønster*, uttrykkelig ikke som en avgjørelse.

## 6 Hva dette ikke kan vise

* **Ingenting om menneskelig lesning.** Ingen menneskelig annotør har lest materialet, og koder 3 blir
  ikke den første. Tre LLM-kodere av samme familie måler om **regelsettet** er entydig — ikke om det er
  riktig.
* **Samme orkestrator, tredje gang.** Oppdraget formuleres av den samme instansen som var koder 1.
  ADDENDUM-11 §3.2 gjelder uendret: sperrelisten er verifiserbar, formuleringen er det ikke.
* **Et høyt κ beviser ikke at fasiten er sann.** Tre lesere kan dele samme systematiske feil. ADDENDUM-18
  §7 viste presist det: Haiku og Sonnet var enigere med hverandre (κ 0,512) enn med koder 1.
* **Rekkefølgeeffekt er ikke kontrollert.** Koder 3 får samme stokking som koder 2. Å stokke på nytt
  ville målt noe annet og gjort κ-ene usammenliknbare på passasjenivå.

## 7 Kostnadsgrunnlag, målt

Koder 2s kjøring, fra utskriften (ADDENDUM-11 §8): **61 API-kall, 20 minutter**
(25.09.2026 17:14:53–17:35:26), **9 019 781 tokens inn** — 122 ubufret, 457 398 buffer skrevet,
8 562 261 buffer lest — og **103 373 tokens ut**, på `claude-opus-5`. Arm A koster i samme
størrelsesorden. Arm B koster det samme igjen.

Til sammenlikning: ADDENDUM-18 kostet 235 326 + 300 672 tokens inn for to kandidater på 320 kall hver,
altså en tjuendedel — fordi ett kall per passasje ikke bygger kontekst. **Prisen på én sammenhengende
økt er akkurat det som gjør koder 2 og kandidatene usammenliknbare**, og det er ikke en kostnad som kan
kuttes uten å endre målingen.

## 8 Dødsbetingelser

* **Kjøres én gang.** Ingen ny ledetekst, ingen ny regelfil, ingen andre runde hvis κ blir lavt. Blir
  det lavt, er det utfallet, og det skrives.
* **Åpner koder 3 en sperret fil, er kjøringen ugyldig** og rapporteres som ugyldig. Sluttrapporten
  skal bekrefte at ingen ble åpnet, slik koder 2s gjorde, og bekreftelsen kontrolleres mot utskriften.
* **Verdiktene til koder 1 og 2 endres ikke** uansett utfall. Tre fasiter står ved siden av hverandre.
* **Ingen avgjørende stemme.** Koder 3 avgjør ikke de tolv uenighetene.
* Blir økten avbrutt midt i, rapporteres antall dømte passasjer, og κ regnes bare på de dømte — ikke
  på et sett fylt ut i ettertid.

## 9 Status

**UKJØRT.** Arm A anbefales; eieren avgjør kvoten. Ingen kjøring før det.
