# Step-by-step validation and instructor compliance audit

**Scope:** The course handout requires (1) GMM/EM from scratch, (2) the course FAA CSV, (3) K=2,3,4,5 scatterplots, (4) evidence of enough iterations, (5) justified optimal K; code must finish in <5 min; deliverables are 15-minute slides and source code. The 3-page handout additionally requires shared team work, citations and AI disclosure.

**Source of evidence:** `FAA_AEDT_data.csv`, `gmm_em.py`, `test_gmm.py`, `results/`, and the deck. Statements below are checks of project files/assistant-environment results, not a claim that students independently performed them.

| Step | Reproducible check | What to record/expect |
|---|---|---|
| 1 | `python -m pip install -r requirements.txt` | Dependencies install without error; record Python version. |
| 2 | `python -m unittest -v test_gmm` | All four unit tests pass. |
| 3 | `python gmm_em.py` | Produces fitted models K=2,3,4,5, figures and tables in `results/`; time it on your machine. |
| 4 | Inspect `gmm_em.py` | E-step/M-step/likelihood/covariance updates implemented in NumPy; no sklearn GaussianMixture call. |
| 5 | Open `results/clusters_all.png` | Four labeled scatter plots, one each for K=2,3,4,5, with fitted ellipses. |
| 6 | Open `results/convergence.png` and `results/convergence_validation.csv` | Likelihood plateau and stricter threshold; compare iteration counts, likelihood and label agreement. |
| 7 | Open `results/model_selection.csv` | BIC minimal at K=3 (10,028.79); AIC minimal at K=4 (9,935.99). |
| 8 | Open deck and rehearse | Timed **15-minute** team storyline. Bibliography on slide 15; explicit AI disclosure on slide 16. |
| 9 | Compare sources with claims | EM: Dempster et al., Bishop; AIC: Akaike; BIC: Schwarz; aviation context: FAA AEDT site; dataset: course CSV. |
| 10 | Team signoff and submission | Replace placeholders with truthful names/work, preserve AI help details, submit by November 30 via e-campus. |

## Interpretation and qualification

- `x1` and `x2` have no physically interpretable units in the provided file. **Don't assert that the statistical clusters are actual stage lengths or thrust levels**.
- A convergence plateau, multi-start runs, and stricter tolerance justify enough iterations for a local stable result; they **do not prove the global MLE**.
- The 300-second requirement applies to the device used for the final run; earlier assistant-environment runtimes do not guarantee another machine's performance.
- The course allows AI assistance **only with transparent disclosure**. Draft code generated with AI is not independent student authorship, even though its EM arithmetic is written without a prebuilt GMM library.
