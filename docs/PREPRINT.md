# Preprint — MetaArXiv

| | |
|---|---|
| **URL** | https://osf.io/preprints/metaarxiv/zvc34_v1/ |
| **OSF-ID** | `zvc34_v1` |
| **Status** | **pending** — MetaArXiv kjører pre-moderering; innsendt, ikke publisert |
| Innsendt | 2026-09-26T09:09:59Z |
| **DOI** | **ikke tildelt ennå.** OSF oppretter preprint-DOI først ved godkjenning |
| Lisens | CC-By Attribution 4.0 International |
| Fagområder | Library and Information Science; Scholarly Communication (begge under Social and Behavioral Sciences) |
| Nøkkelord | metascience · preregistration · research limitations · obstacle typology · self-admitted technical debt · open access |
| Fil | `gjenopptak-manuskript-v0.1.pdf`, 8 sider A4, sha256 `5e0cf29b663217cbbe8477302d9f23e007e21c0c3d318568b1b338b6ce64392d` |

## Datatilgang

Konsept-DOI **10.5281/zenodo.22959326** (protokoll, data, register, kode) er ført i feltet
`custom_publication_citation` med formuleringen «supplemented by». **OSFs preprint-API har ikke et
felt for vilkårlige relaterte identifikatorer**; «supplemental materials» er i OSF en lenke til en
egen OSF-node, ikke en DOI. Å opprette en slik node ville laget enda et offentlig objekt, og er
ikke gjort. DOI-en står også i manuskriptets egen tekst.

**Versjons-DOI, oppdatert 2026-09-26.** Depositumets gjeldende versjon er nå **0.2.1**, versjons-DOI
**10.5281/zenodo.22975301** (før: 22965761 for 0.2.0). Endringen er ren metadata — en foreldet
`CITATION.cff` ble byttet, jf. `docs/ZENODO.md`. **Det som er ført på preprinten, og det som står i
manuskriptet, er konsept-DOI-en**, og den er uendret: den peker alltid til nyeste versjon. Ingen
endring i PDF-en eller i preprintens felt er derfor nødvendig. Merk at 22975301 svarte HTTP 404 ved
publisering — DataCite-registreringen henger etter — så den versjons-DOI-en bør ikke oppgis videre
før et ferskt oppslag gir 302.

**Datert tillegg 28.09.2026:** gjeldende versjon er nå **0.3.0**, versjons-DOI **10.5281/zenodo.22976464**
(publisert 26.09, `docs/ZENODO.md`). Avsnittet over gjelder tilstanden før den. Konsept-DOI-en er uendret,
og det som er ført på preprinten, trenger fortsatt ingen endring.

## Åpne poster

1. **ORCID er koblet til kontoen — rettelse 2026-09-26.** Den forrige oppføringen her sa at ORCID
   ikke var knyttet til profilen. Det var feil, og feilen var min: jeg sluttet fra at API-feltet
   `social.orcid` var tomt til at koblingen manglet. OSF lagrer ORCID som en **tilkoblet identitet**
   (OAuth), ikke i `social`. Kontrollert i nettleseren 2026-09-26: Settings → Account → **Connected
   Identities** viser «ORCID: 0009-0001-9188…», og profilsiden osf.io/vxm64 viser
   **https://orcid.org/0009-0001-9188-6788** med ORCID-ikonet. Ingenting måtte kobles.
   **Men ORCID-en vises ikke på preprintposten** zvc34_v1 — ingen orcid.org-lenke eller -ikon
   finnes på siden mens den ligger til moderering. Om den dukker opp ved godkjenning, eller må
   legges til per bidragsyter, er ikke avklart. Sjekkes på nytt når modereringen er ferdig.
2. **Modereringsutfallet er ikke kjent.** Ved avslag eller endringsønske kommer det som en
   `review_action` på preprintet. Statusen her må oppdateres når den endrer seg.
3. **DOI føres inn her og i CITATION.cff når den tildeles.**

## Hva som ble sendt

Manuskriptet er utkast v0.1, bygget fra `docs/MANUSKRIPT-v0.1.md`. Abstraktet (240 ord) er skrevet
fra manuskriptets egne tall og kontrollert mot `data/koder2-sammenlikning.json` og
`docs/RESULTAT-PORT-v1.md` — null avvik på tretten tallpåstander. Fem porter grønne før innsending:
ingen tallavvik, ingen uverifiserte referanser, ingen påstand om verktøyets nytte utover det målte,
tidsstemplingsforbeholdet står i teksten, og ingen e-postadresser eller stedsnavn.
