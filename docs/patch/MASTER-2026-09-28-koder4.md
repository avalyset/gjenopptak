# Patch til MASTER — koder 4, Fable 5.1, inn i reliabilitetsmålingen

> **Datert merknad 28.09.2026 (frys-lesning 2) — to steder påføres ikke slik de står.** Patchen er
> ikke omskrevet. **§ 4 «M1 og M2 for koder 4»** (l. 47–54 før merknaden: kolonnen «koder 1» og
> «tettere plassert og oftere bedømbare») er trukket av `docs/METODE.md` 28.09.2026 (l. 415–423): høyre
> kolonne er dommerens felt fra oppfølgingskallet, ikke koder 1s koding (14 av 39 ikke dømt), og
> slutningen er trukket. **§ 7 «Nytt forbehold», siste setning** (l. 77–78 før merknaden: «75,8 % … mot
> langt lavere hos koder 1», og slutningen om kalibrering) står ikke i METODE, som fører 75,8 % uten
> sammenligning, og holder ikke: koder 1 har `tvil` på 25 av sine 39 treff = 64,1 %
> (`data/port-presisjonssett-ADDENDUM10.jsonl`). Ved neste v-bump hentes ordlyden for disse to stedene fra
> METODE, ikke herfra.

**Skrevet 28.09.2026.** Påføres ved neste v-bump. MASTER er urørt.
Grunnlag: `docs/METODE.md`, seksjonen «Koder 4 — Fable 5.1, chat, ikke menneske».
Inndata: `koder4/koder4-fable51-verdikter.jsonl` på Vault, sha256
`36a3465acd195355c2ad0bf5fca9d4c305c04b8cd977f9ac043a9c34d26b1798`, **uredigert**.

---

## § 0 · statusblokk, linjen som skal inn

* **En tredje koding finnes, og den er en annen modellfamilie.** Koder 4 (Fable 5.1, chat) leste de
  samme 320 passasjene blindt, i PS-rekkefølge, mot samme regelfil og blindfil som koder 2.
  **κ mot koder 2 = 0,899** [0,808–0,969] — **høyere enn κ mellom koder 1 og koder 2 (0,812)**.
  Modellfamilie-forbeholdet peker dermed motsatt vei av det som ble antatt, men **ingen av de tre er
  et menneske**, så κ mot menneskelig lesning er uendret ukjent.

## § 4 · resultater, ny tabell

**Treffbeslutningen, tre par.** Cohens κ, paret bootstrap, 10 000 gjentak, frø 734248.

| par | n | rå enighet | κ | bootstrap 95 % |
|---|---|---|---|---|
| koder 4 mot koder 2 | 320 | 0,981 | **0,899** | 0,808–0,969 |
| koder 1 mot koder 2 | 320 | 0,963 | 0,812 | 0,697–0,906 |
| koder 4 mot koder 1 | 320 | 0,956 | 0,781 | 0,659–0,883 |

Uten de 20 ankerne: 0,875 · 0,774 · 0,711. **Rekkefølgen holder, intervallene overlapper**, og
**koder 1 er den av de tre som avviker mest** fra de to andre.

**Klasse er svakere enn treff for alle tre par:** koder 1–2 κ 0,732 (n = 30), koder 4–2 κ 0,683
(n = 30), koder 4–1 κ **0,501** (n = 29).

## § 4 · det nye hovedfunnet om N3

**Koder 4 satte `INGEN` der koder 1 satte `N3` 40 ganger** — største enkeltcelle utenfor diagonalen.
Koder 4 brukte `N3` 13 ganger, koder 1 54. Det er en **definisjonsforskjell**: N3 krever et ugjort
uten navngitt hindring, og koder 4 leser de samme passasjene som at det ikke finnes noe ugjort.
Med koder 1 mot koder 2 var klasse-κ for N3 **0,530**. **Tre kodere, tre ulike tellinger av samme
klasse** — den mest direkte bekreftelsen sporet har på at N3-grensen ikke var avgjort av reglene, og
grunnen til at `docs/REGEL-N3-v1.md` finnes.

## § 4 · M1 og M2 for koder 4

Oppgitt hver for seg, aldri sammenslått (ADDENDUM-03 § 1.2, PREREG § 6).

| mål | koder 4 | koder 1 |
|---|---|---|
| treff av 320 | 33 | 39 |
| M1-streng | **27 av 33 = 81,8 %** [65,6–91,4]; 8,44 % av 320 | 23 av 39 = 59,0 % |
| M1-passasje | 33 av 33; 10,31 % av 320 [7,44–14,13] | — |
| M2 `ja` / `usikker` / `nei` | **17 / 15 / 1** = 51,5 / 45,5 / 3,0 % | 4 / 15 / 6 |

**Koder 4 flagger færre passasjer, men de den flagger er tettere plassert og oftere bedømbare.**

## § 4 · de 27 kjente treffene

**Koder 4 fant 18 av 27 = 66,7 %** [47,8–81,4]. **Alle ni tapte var merket `tvil` av koder 1**, og sju
av ni ble også mistet av koder 2: PS-010, PS-031, PS-117, PS-133, PS-148, PS-202, PS-226, PS-292,
PS-315. Tapene ligger i nøyaktig den ustabile delen av fasiten. **Tredje uavhengige kilde til at den
stabile kjernen er tre av 27.**

## § 7 · forbehold, to som skal endres

**Forbehold 1 skal skrives om.** Det sier i dag «To kodere, begge LLM-baserte, ingen menneskelig
annotør». Ny ordlyd, ordrett:

> **«Tre kodinger, tre LLM-er, to modellfamilier, ingen menneskelig annotør; koder 4 delvis eksponert
> for 7 av 320 passasjer, følsomhet oppgitt.»**

Endringen er verdt å gjøre presis: forbeholdet ble svakere på **modellfamilie**, står uendret på
**menneske**, og fikk et nytt ledd om **eksponering**.

**Nytt forbehold:** **`tvil` er den mest overførbare enkeltopplysningen i kjeden.** Presisjonen mot
koder 1 blant koder 4s treff er **8 av 8 = 100 %** der `tvil` er `false` og **21 av 25 = 84,0 %** der
den er `true` — samme retning som ADDENDUM-23 § 7.2 fant for koder c (97,6 mot 75,9 %), nå i en annen
modellfamilie. **Det gjelder også motsatt: 75,8 % av koder 4s treff bærer tvil**, mot langt lavere hos
koder 1, så flagget er ikke kalibrert på tvers av kodere — bare retningen er.

## § 4 · eksponering og følsomhet — datert 28.09.2026

**Koder 4 var delvis eksponert.** Den leste `docs/SAKBEHANDLING-2026-09-27-kandidater.md` dagen før
kodingen og kjente PS-246, PS-257 og PS-300 på id. **7 av 320 rader er ikke blindt kodet:** PS-246,
PS-257, PS-266 (eksakt tekstmatch), PS-288, PS-289, PS-300, PS-319. Matchregelen er NFC og samlet
mellomrom; en romsligere grense fant ingen nye, og **ingen av de sju er anker**.

**Begge tallsett, side om side.** Samme bootstrap, 10 000 gjentak, frø 734248.

| par | alle 320 | 320 − eksponerte (313) | 300 uten ankere | 300 − eksponerte (293) |
|---|---|---|---|---|
| koder 4 mot koder 2 | **0,899** | **0,874** | 0,875 | 0,819 |
| koder 1 mot koder 2 *(kontroll)* | 0,812 | 0,794 | 0,774 | 0,727 |
| koder 4 mot koder 1 | **0,781** | **0,757** | 0,711 | 0,645 |

**Kontrollparet avgjør tolkningen.** κ faller for **alle tre par**, også for koder 1 mot koder 2, som
aldri var eksponert — fordi de sju radene inneholder **6 av de 27 kjente treffene**, og å fjerne dem
krymper den positive klassen. Fall på 320-grunnlaget: koder 4–1 −0,024, koder 4–2 −0,025, kontrollen
−0,018. **Differansen mot kontrollen er 0,006 og 0,007, altså inne i støyen.** Rekkefølgen
koder 4–2 > koder 1–2 > koder 4–1 **holder i alle fire radutvalg**.

**De 27 kjente:** 6 av de 18 funne var eksponerte, **0 av de 9 tapte**. Recall 18/27 = 66,7 %
[47,8–81,4] med alt inne, **12/21 = 57,1 %** [36,5–75,5] på de ueksponerte. **To lesninger står:**
eksponeringen hjalp, eller de eksponerte var de lettest kodbare — de kom i kandidatfila fordi leseren
flagget dem med `tvil: false`, der blind presisjon er 98 %. **Dataene skiller dem ikke**, og
intervallene overlapper i hele sin lengde.

**Konklusjonen om modellfamilie står.** Hovedfunnet — at en annen modellfamilie gjenskaper koder 2s
treffbeslutning bedre enn koder 1 gjør — er ikke drevet av eksponeringen: det holder på 313 rader
(0,874 mot 0,794) og på 293 (0,819 mot 0,727).

## § 9 · åpne poster

* **«Uavhengig menneskelig annotør» står uendret som åpen post.** Koder 4 flyttet
  modellfamilie-forbeholdet, ikke menneskeforbeholdet.
* **`tvil`-flagget er ikke kalibrert på tvers av kodere.** Retningen overføres, nivået ikke. En
  terskel på `tvil` vil derfor virke ulikt per koder, og det bør måles før noen bruker flagget som
  filter.
* **Eksponeringen er målt, ikke fjernet.** Koder 4s kodinger av de sju radene står uredigert i fila
  og inngår i alle tall merket «alle 320». Skal en fremtidig koding være helt blind, må kodingen skje
  **før** kandidatfila leses — rekkefølgen er det eneste som kan gjøre den blind.
* **Klasse-κ på 0,501 mellom koder 4 og koder 1** er den laveste parvise klasseenigheten i sporet.
  Etter REGEL-N3-v1 bør den måles om på nytt materiale — men **ikke på de 320**, som er kodet uten
  regelen.
