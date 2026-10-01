# Regel N3 — versjon 1

**Dato:** 2026-09-28. **Versjon:** 1. **Gjelder fra:** fase 3-kodingen.
**Hvorfor den finnes:** N3-grensen er den svakeste grensen i typologien, og det er **målt**, ikke
antatt. Uten en eksplisitt beslutningsregel avgjøres den av koderidentitet.

## Belegget for at grensen trenger en regel

| mål | tall | kilde |
|---|---|---|
| κ mellom koder 1 og koder 2 på «er dette N3» | **0,530** | regnet av `port-presisjonssett-ADDENDUM10.jsonl` og `port-presisjonssett-verdikter-koder2.jsonl` |
| koder 1 satte N3 | **54 av 320** | samme |
| koder 2 satte N3 | **34 av 320** | samme |
| enige om N3 | **26** | samme |
| spredning mellom åtte kodere på tilfeldig delt materiale | **5,8–13,6 %** | ADDENDUM-22 § 9.4 |

**To kodere med samme regelsett avvek med en faktor 1,6 på hvor ofte de brukte klassen.** Til
sammenligning er κ for `INGEN` 0,879 og for `H7` 0,820. N3 og N2 (κ 0,535) er de to klassene reglene
ikke avgjør.

## Definisjonen som gjelder, ordrett fra kilden

PREREG-v1 § 5: **«N3 omfangsvalg uten navngitt hindring.»**

ADDENDUM-02 § N3: *«N3 sier hva teksten ikke handler om, uten å navngi noe som hindret forfatteren.
Mangler hindringen, er det N3 — også når setningen ellers ser ut som en innrømmelse.»*

## Beslutningsregelen, i rekkefølge

Bruk trinnene **i denne rekkefølgen** og stopp på første som gir svar. Rekkefølgen er en del av
regelen: å bytte om trinn 2 og 3 flytter tilfeller.

**Trinn 1 — er det noe ugjort i det hele tatt?**
Nei → klassen er `INGEN`. Regelen gjelder ikke videre.

**Trinn 2 — navngir passasjen en hindring?**
En hindring er noe som **sto i veien**: manglende data, manglende verktøy, manglende tid, manglende
kompetanse, manglende tilgang, manglende prøver, manglende regnekraft. En hindring er **ikke**:
* at forfatteren valgte en annen avgrensning,
* at noe «ligger utenfor artikkelens omfang»,
* at noe «krever videre forskning» uten at det sies hvorfor det ikke ble gjort her.

Navngir den ingen hindring → **N3**, uansett hvor mye setningen ellers likner en innrømmelse.

**Trinn 3 — hører det ugjorte til det rapporterte arbeidet?**
Nei, det hører til et framtidig eller annet arbeid → **N3**.
Ja, og en hindring er navngitt → gå til H-klassene (ADDENDUM-04 § 4).

**Trinn 4 — avgjør passasjen hvilken hindring det var?**
Nei, den navngir to og velger ikke → `<klasse>/H7-uavklart` (ADDENDUM-05), **ikke** N3.

## Ankereksempler

### N3 — omfangsvalg, ingen hindring navngitt

1. «Detailed information on the annotation types is **beyond the scope of this paper**.»
   `10.1016/j.dib.2024.111152`, `Data Description`. — Avgrensning. Ingenting sto i veien.
2. Prosessen og leveringsmåten for et læreplansforslag «**are beyond the scope of this paper**».
   `10.36834/cmej.79242`. — Samme form.
3. «**Further research is needed** to establish the mechanism.» — Ugjort finnes, hindring mangler.
   Dette er formen som oftest feilkodes som treff, og den er N3.

### IKKE N3 — hindring navngitt i samme setning

4. «Pour les textes grecs, nous ne donnerons que la traduction des textes grecs **en raison de notre
   méconnaissance du grec**.» (SAK-14) — Hindringen er navngitt: manglende greskkunnskap. **H3.**
5. «Two sets of runs were carried out separately **due to prohibitively long processing times**.»
   (SAK-08) — Hindringen er navngitt: regnekraft. **H5.**
6. «Pajek **does not offer a practical option to force** that to happen.» (SAK-09b) — Hindringen er
   navngitt: verktøyet. **H5.**

### Grensetilfellene regelen faktisk avgjør

7. «**No consensus definition exists** for OMPC.» `10.3390/cancers14246194` — Det som mangler, er en
   enighet i feltet, ikke en avgrensning forfatteren valgte. Trinn 2 gir en navngitt hindring. **H9,
   ikke N3.**
8. «The annotation types are **not covered here**; see the companion paper.» — Trinn 3: det ugjorte
   hører til et annet arbeid. **N3.**
9. «We could not date the layer **because no suitable sample was preserved**.» — Hindring navngitt,
   hører til dette arbeidet. **H7, ikke N3.**

## Hva regelen ikke løser

**Trinn 2 hviler på om leseren regner en formulering som «navngir en hindring».** «Beyond the scope»
er entydig; «was not feasible within the present study» er ikke. Regelen flytter grensen fra
skjønn til et **ordnet** skjønn, og det er en forbedring som kan måles — men den fjerner ikke
skjønnet, og en ny κ-måling etter fase 3 vil vise hvor mye den var verdt.

**Regelen er ikke brukt på de 320.** Koder 1 og koder 2 kodet uten den. κ = 0,530 er derfor
**før**-tallet, og det skal ikke regnes om.

## Versjonering

| versjon | dato | endring |
|---|---|---|
| 1 | 2026-09-28 | første eksplisitte regel; fire trinn, ni ankere. Utløst av κ = 0,530 |

En ny versjon krever en ny fil (`REGEL-N3-v2.md`), ikke en redigering: en koding gjort under v1 skal
kunne peke på den regelen som gjaldt.
