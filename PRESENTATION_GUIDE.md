# Presentation and defense guide

**Application of AI in Aerospace · Fall 2026 · GMM with EM**  
Deadline: November 30, 2026. Target duration: 15 minutes.

## Start here

- [Existing repository PowerPoint](FAA_GMM_EM_presentation.pptx) — 16-slide draft.
- [Model selection results](results/model_selection.csv) and [all four clustering plots](results/clusters_all.png).
- [Convergence curves](results/convergence.png) and [strict tolerance check](results/convergence_validation.csv).
- [Reproduction audit](REPRODUCTION_AUDIT.md), [defense questions](DEFENSE_QA.md), [references](REFERENCES.md), and [submission checklist](SUBMISSION_CHECKLIST.md).
- [AI disclosure](AI_DISCLOSURE.md) and [actual team contribution record](TEAM_CONTRIBUTIONS.md).

A refreshed light-blue 16-slide PowerPoint, PDF and speaker notes were prepared in ChatGPT on November 26 and supplied as downloadable artifacts in the chat. The revised binary presentation is **not** uploaded by this documentation commit; the existing repository PowerPoint remains intact. Use the refreshed file for rehearsal, and ensure the actual file submitted contains the final truthful names and contributions.

## Suggested 15-minute storyline

| Time | Slides | Story |
| --- | --- | --- |
| 0:00–2:35 | 1–3 | Objective, AEDT context, supplied data and limitations |
| 2:35–7:10 | 4–7 | GMM density, E-step, M-step, numerical implementation |
| 7:10–9:25 | 8–9 | Compare K=2/3 and K=4/5 on common axes |
| 9:25–11:55 | 10–11 | Convergence and BIC/AIC trade-off |
| 11:55–14:10 | 12–14 | Cluster interpretation, runtime, conclusion |
| 14:10–15:00 | 15–16 | References and explicit AI disclosure |

Divide speaking responsibilities fairly; the timings are rehearsal targets, not measured performance.

## Evidence by requirement

| Assignment requirement | Evidence |
| --- | --- |
| GMM with EM from scratch | [gmm_em.py](gmm_em.py), [unit tests](test_gmm.py) |
| Apply to FAA data | 1,000 × 2 observations; [outputs](results/) |
| Plot K=2,3,4,5 | [Combined scatter plots](results/clusters_all.png) |
| Demonstrate sufficient iterations | [Likelihood curves](results/convergence.png), [validation table](results/convergence_validation.csv) |
| Select suitable K | [AIC/BIC table](results/model_selection.csv): BIC selects 3, AIC selects 4 |
| Finish in under 5 minutes | [Audit](REPRODUCTION_AUDIT.md): latest rerun 6.496 s, environment-specific |
| Cite all sources and disclose AI | [References](REFERENCES.md), [disclosure](AI_DISCLOSURE.md) |

## Before submission

Confirm the course permits public redistribution of the supplied data (the repository is currently public). Verify all names and contributions, rehearse the talk, rerun the complete default experiment on the presentation machine, and submit the required files by the deadline. The CSV lacks verified physical units, ground-truth labels and actual stage lengths; do not claim operational validation. AI assistance includes the initial implementation and experiments as well as slides and repository documentation.
