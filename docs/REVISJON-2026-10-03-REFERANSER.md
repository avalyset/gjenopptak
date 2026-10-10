# Referansene i fagfellevurderingen — slått opp 03.10.2026

Oppslag i arXiv (API), Crossref (API) og Europe PMC med ærlig User-Agent (`gjenopptak-refsjekk/0.1`). Råsvarene ligger på
Vault, `revisjon-2026-10/referanser/` (12 filer, sha256 i `SHA256SUMS` der). **Alle seks finnes.** Bare de som står her,
med DOI, går videre til manuskriptet.

| vurderingens navn | finnes | referanse | DOI / URL | innholdet vurderingen tillegger den |
|---|---|---|---|---|
| **BAGELS** | **ja** | Al Azher, I., Mokarrama, M. J., Guo, Z., Ray Choudhury, S. & Alhoori, H. (2025). BAGELS: Benchmarking the Automated Generation and Extraction of Limitations from Scholarly Text. *Findings of the ACL: EMNLP 2025*, 19279–19294 | 10.18653/v1/2025.findings-emnlp.1050 · arXiv 2505.18207 (22.05.2025) | stemmer: benchmark for uttrekk og generering av «limitations» fra vitenskapelig tekst (sammendraget) |
| **LimitGen** | **ja** | Xu, Z., Zhao, Y., Patwardhan, M., Vig, L. & Cohan, A. (2025). Can LLMs Identify Critical Limitations within Scientific Research? A Systematic Evaluation on AI Research Papers. *Proceedings of the 63rd Annual Meeting of the ACL*, 20652–20706 | 10.18653/v1/2025.acl-long.1009 · arXiv 2507.02694 | stemmer: LimitGen er benchmarken; LimitGen-Syn er syntetisk (sammendraget) |
| **LLM-SSC / biorc800** | **ja** | Lan, M., Zheng, L., Ming, S. & Kilicoglu, H. (2024). Multi-label Sequential Sentence Classification via Large Language Model. *Findings of the ACL: EMNLP 2024*, 16086–16104 | 10.18653/v1/2024.findings-emnlp.944 · arXiv 2411.15623 | stemmer: LLM-SSC er rammeverket; biorc800 er et manuelt annotert biomedisinsk datasett (sammendraget) |
| **Gu et al.** | **ja** | Gu, F., Li, Z., Colon, C. R., Evans, B., Mondal, I. & Boyd-Graber, J. L. (2026). Large Language Models Are Effective Human Annotation Assistants, But Not Good Independent Annotators. *Findings of the ACL 2026*, 71–89 | 10.18653/v1/2026.findings-acl.4 · arXiv 2503.06778 | stemmer: hendelsesannotering; LLM alene ikke pålitelig mot eksperter, LLM som assistent sparer tid (sammendraget) |
| **Vanbelle** (kappa, hierarkiske data) | **ja** | Vanbelle, S. (2019). Asymptotic variability of (multilevel) multirater kappa coefficients. *Statistical Methods in Medical Research*, 28, 3012–3026 (online 2018) | 10.1177/0962280218794733 · PMC6745615 | stemmer: **klynget bootstrap** (trekk klynger med tilbakelegging) beskrevet og sammenliknet med deltametoden (§ 4.2 i fulltekst, åpen) |
| | ja | Vanbelle, S. (2017). Comparing dependent kappa coefficients obtained on multilevel data. *Biometrical Journal*, 59, 1016–1034 | 10.1002/bimj.201600093 | finnes; at den beskriver klynget bootstrap, er **ikke** kontrollert (sammendraget nevner det ikke, fulltekst ikke åpen) — siter 2019-artikkelen for metoden |
| **NLPContributionGraph (SemEval)** | **ja** | D'Souza, J., Auer, S. & Pedersen, T. (2021). SemEval-2021 Task 11: NLPContributionGraph — Structuring Scholarly NLP Contributions for a Research Knowledge Graph. *Proceedings of SemEval-2021*, 364–376 | 10.18653/v1/2021.semeval-1.44 · arXiv 2106.07385 | stemmer |

**BAGELS er avgjort: publikasjonen finnes.** LAERDOM § 23 rad 1 (26.09.2026) førte den som ikke-eksisterende («ingen slik
publikasjon finnes; treffene er akseleratorfysikk og agent-bootstrapping»). Det var feil: arXiv-posten er fra 22.05.2025 og
konferanseversjonen er i ACL Anthology. Søket 26.09 ga altså et falskt nei. Rettet som datert tillegg i LAERDOM § 50; § 23
står som den ble skrevet.
