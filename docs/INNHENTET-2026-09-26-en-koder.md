# INNHENTET 2026-09-26 — «Én koder» i to låste filer

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

**Gjeldende formulering:** manuskriptets § 7 punkt 1 og `docs/RESULTAT-PORT-v1.md`, forbehold 1.

## 2 ADDENDUM-06 § 1.6 — **sant som skrevet, men om et annet materiale**

> * **Én koder.** Fasiten er markert av samme koder som skrev markørene.

**Status:** **fortsatt sant.** Setningen gjelder **recall-fasiten** (sett 1 og 2, 55 ekte treff), som
ADDENDUM-11 ikke rørte. Den uavhengige omkodingen gjaldt **presisjonssettet** — de 320 tekstbitene fra
porten.

**Presiseringen en leser av depositumet trenger:** utsagnet er ikke en påstand om studien som helhet.
Recall-fasiten har én koder; presisjonssettet har to, med κ målt. Den som leser ADDENDUM-06 alene, kan
ellers lese punktet som den generelle svakheten PREREG § 9 beskrev.

## 3 Hva som ikke er gjort

Ingen av de to låste filene er endret. Sha256 er uendret, og `securerepo`s kontroll av låste filer
(`LOCKED_SHA256`) står grønn. Denne filen er pekt til fra README.
