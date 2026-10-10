# INNHENTET 2026-10-07 — Fase 4-dataene: «slettet» eller «i papirkurven»

**`docs/RESULTAT-ADDENDUM-26.md` er uendret.** Fila sier to ting om fase 4-dataene som ikke kan stå sammen, og
den ene var riktig på sin dato. Den er **innhentet**, ikke rettet; det som er innhentet, føres i en datert fil ved
siden av (samme regel som `INNHENTET-2026-09-26-en-koder.md`).

## 1 Motsigelsen

Statuslinjen (linje 3):

> **Status 03.10.2026: avbrutt og ryddet etter eierens beslutning, før noen port var målt. Data slettet; ramme og protokoll bevart.**

§ 0 (linje 22 og 27):

> Ingenting er slettet.

> … Alt er flyttet til papirkurven og er borte når den tømmes. **Kjøringen kan ikke lenger gjenopptas.**

Statuslinjen sier at dataene er slettet. § 0 sier at de er flyttet til papirkurven («ikke slettet før papirkurven
tømmes», jf. opprydningsnotatet i `MANIFEST-VAULT.md`). «Ingenting er slettet» på linje 22 gjelder stoppøyeblikket
03.10.2026 kl. 11:04 UTC, før opprydningen, og er riktig for det øyeblikket.

## 2 Hva som gjelder

**Papirkurven er tømt per 07.10.2026, bekreftet av eier.** De 366 MB på Vault og de 11 MB øktutskrifter på
systemdisken finnes ikke lenger. **Statuslinjen («Data slettet») er derfor den gjeldende, og påstanden i § 0 om
at dataene ligger i papirkurven er innhentet fra 07.10.2026.** Avsnittet i § 0 er tilstanden 03.10.2026.

Det som er bevart, står som i § 0: protokollen (`ADDENDUM-26.md`, låst `7ebf7aa`), den frosne rammelista
`frames/frame-haandskrift-RAW.jsonl` (807 rader, sha256 `6e444a0837d6559906096b15ff6371ee6b630391d387702cc4171410225eaf75`),
`RESULTAT-ADDENDUM-26.md`, manifestradene og de små sporfilene i `fase4/` (trekkspesifikasjon, trekklogg,
utvalgslista uten tekst, OpenAlex-svarene i `raw/`, logger og driveren). Manifestradene for de slettede filene
står som opprydningsnotatet forklarer. Konsekvensen er uendret: fase 4 har ikke gitt noe resultat, og
kjøringen kan ikke gjenopptas (`kjede/gjenoppta.py` avviser `--fase fase4`).

## 3 Zenodo v0.5.0

`RESULTAT-ADDENDUM-26.md` i Zenodo v0.5.0 (versjons-DOI 10.5281/zenodo.23120143, md5
`d6725b2943dc4e4e7495321f61d552da`, byte-lik repoets fil) **bærer motsigelsen og rettes ikke.** En deponert fil
endres ikke; denne fila er rettelsen ved siden av. Den deponeres første gang i v0.6.0.
