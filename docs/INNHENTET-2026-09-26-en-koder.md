# INNHENTET 2026-09-26 — «Én koder» i låste filer (utvidet 28.09.2026)

**PREREG-v1.md er uendret, og var riktig på sin dato.** Protokollen ble låst **12.09.2026**, og da var
det én koder. Utsagnet er **innhentet** av ADDENDUM-11 (**25.09.2026**), som målte en uavhengig
omkoding — det er **ikke rettet**, fordi det ikke var galt da det ble skrevet. En låst fil endres
aldri; det som er innhentet, føres i en datert fil ved siden av. Funnet av
`python -m gjenopptak.kryssjekk`, som siden 2026-09-26 leser også de låste filene og rapporterer
treff i dem for seg.

## 1 PREREG-v1.md § 9, punkt 1 — **innhentet 25.09.2026**

> 1. **Én koder.** Designets hovedsvakhet. Hører i sammendraget, ikke i vedlegg.

**Status:** utdatert siden **2026-09-25**. ADDENDUM-11 lot en separat instans med tom kontekst kode de
samme 320 tekstbitene på nytt. **κ = 0,81 [0,70–0,91]** på treffbeslutningen, rå enighet 96,2 %.
Hovedfunnet står i begge lesninger (H7 17 av 25 mot 12 av 19).

**Det som fortsatt står:** **ingen menneskelig annotør** har kodet materialet, og begge kodere deler
modellfamilie og regelsett. Enigheten er dessuten ujevn: κ = 1,00 i klinisk epidemiologi mot **0,39** i
energimodellering. Svakheten er altså flyttet, ikke fjernet — fra «én leser» til «to lesere av samme
slag».

**Innhentet 28.09.2026:** de 320 har nå **tre LLM-kodere** — koder 1 og 2 (Opus) og koder 4 (Fable 5.1, en
annen modellfamilie). Forbeholdet om felles modellfamilie gjelder derfor ikke lenger alle tre; **ingen
menneskelig annotør** står uendret. Avsnittet over er tilstanden 25.09.2026.

**Gjeldende formulering:** § 3 under. *(Rettet 28.09.2026: pekte til manuskriptets § 7 punkt 1 og
`docs/RESULTAT-PORT-v1.md` forbehold 1, som begge sto med to kodere av samme modellfamilie.)*

## 2 ADDENDUM-06 § 1.6 — **sant som skrevet, men om et annet materiale**

> * **Én koder.** Fasiten er markert av samme koder som skrev markørene.

**Status:** **fortsatt sant.** Setningen gjelder **recall-fasiten** (sett 1 og 2, 55 ekte treff), som
ADDENDUM-11 ikke rørte. Den uavhengige omkodingen gjaldt **presisjonssettet** — de 320 tekstbitene fra
porten.

**Presiseringen en leser av depositumet trenger:** utsagnet er ikke en påstand om studien som helhet.
Recall-fasiten har én koder; presisjonssettet har tre (to til 28.09.2026), med κ målt, jf. § 3. Den som leser ADDENDUM-06 alene, kan
ellers lese punktet som den generelle svakheten PREREG § 9 beskrev.

## 3 ADDENDUM-02 § 5 — **innhentet 25.09.2026** *(føyd til 28.09.2026, frys-lesningen før v0.4.0)*

> M1 er prevalens av parkerte spørsmål i **åpent tilgjengelig litteratur innenfor fire formålsvalgte
> emnerammer, 2015–2020** — ikke i litteraturen. Designet har én koder. Begge forholdene begrenser hva
> tallet kan brukes til.

**Status:** første halvdel står; **«Designet har én koder» er innhentet** av ADDENDUM-11 (25.09.2026), på
samme måte som PREREG § 9 over. § 5 pålegger at formuleringen skal stå i sammendraget av enhver
rapportering; den skal derfor **ikke** gjengis ordrett lenger. Siden 28.09.2026 har de 320 passasjene
tre LLM-kodere: koder 1 mot koder 2 κ = 0,812 [0,697–0,906]; koder 4 (Fable 5.1, en annen modellfamilie)
0,899 [0,808–0,969] mot koder 2 og 0,781 [0,659–0,883] mot koder 1 (`docs/METODE.md` «Koder 4»; 7 av 320
rader eksponert). **Ingen menneskelig annotør** har kodet noe.

**Gjeldende formulering for sammendraget:** «M1 er prevalens av parkerte spørsmål i åpent tilgjengelig
litteratur innenfor fire formålsvalgte emnerammer, 2015–2020 — ikke i litteraturen. Kodingen er gjort av
LLM-kodere, ikke av mennesker; κ mot menneskelig lesning er ikke målt.»

**ADDENDUM-04 § 2** (linje 58) viser til «én-koder-svakheten (PREREG §9)» som noe som skal stå ved siden av
rammeformuleringen. Henvisningen innhentes med PREREG § 9 (§ 1 over); rammeformuleringen selv står.
Det samme gjelder **ADDENDUM-08** (linje 27), forbehold 2 i sammendragslisten: «Én-koder-svakheten
(PREREG §9). Designet har én koder.» Forbehold 1, 3 og 4 i samme liste står.

## 4 ADDENDUM-06 § 1 og § 3 — «for hånd» og «menneskelig leser» *(føyd til 28.09.2026)*

> … markert for hånd, med spenn, klasse og begrunnelse per treff. (linje 18)

> … det andre er hvor ofte en menneskelig leser fant de to delene spredt. (linje 118)

**Status:** **feil som skrevet.** Recall-fasiten er kodet av «samme koder som skrev markørene» (§ 1.6), og
den koderen var en Claude-økt, ikke et menneske (`docs/METODE.md` § 11, ADDENDUM-11 § 3.1 og § 8). «For
hånd» betyr her «ved lesning, uten markørliste og uten søk», og «menneskelig leser» skal leses som
«LLM-koderen». **Slutningen i § 3 står** — nesten en femtedel av de parkerte spørsmålene i recall-fasiten
ville falt ut av et setningskrav — men den er et funn om én LLM-koders lesning, ikke om menneskelig
lesning.

## 5 Hva som ikke er gjort

Ingen av de låste filene er endret. Sha256 er uendret, og `securerepo`s kontroll av låste filer
(`LOCKED_SHA256`) står grønn. Denne filen er pekt til fra README.
