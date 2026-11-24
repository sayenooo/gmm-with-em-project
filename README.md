# FAA AEDT clustering — Gaussian Mixture Model with EM

**Fall 2026 group assignment · Due Monday, November 30, 2026 (no late submissions)**

**Status:** Technical draft tested and reproduced; **not ready for final submission until students fill in their true names and verify/document individual contributions**. See `TEAM_CONTRIBUTIONS.md` and `SUBMISSION_CHECKLIST.md`.

## What is included

- `gmm_em.py`: original full-covariance Gaussian mixture model trained using E-step and M-step coded in NumPy. No sklearn/SciPy GMM implementation is called.
- `FAA_AEDT_data.csv`: course-provided input data (1,000 observations, two features).
- `test_gmm.py`: unit tests for normal density, M-step, synthetic recovery, and dataset reproducibility.
- `results/`: hard and soft cluster assignments, fitted means/covariances, individual scatter plots for K=2,3,4,5, combined figure, likelihood curves, model-selection tables/plot, and runtime details.
- `FAA_GMM_EM_presentation.pptx`: 16-slide English deck (including references and AI disclosure) with speaker notes for an approximately 15-minute presentation.
- `AI_DISCLOSURE.md`: truthful five-part AI usage disclosure; requires actual student-contribution fields before submission.
- `REFERENCES.md`: checked peer-reviewed EM/GMM, AIC/BIC publications and FAA primary website, with claim-to-citation map.
- `VALIDATION_STEPS.md`: reproducible step-by-step independent review instructions and evidence log.
- `TEAM_CONTRIBUTIONS.md`: fields to complete truthfully for your actual team.
- `SUBMISSION_CHECKLIST.md` and `DEFENSE_QA.md`: final verification and presentation practice.

## Reproduce the experiments

Requires **Python 3.10+**. In the repository directory run:

```bash
python -m pip install -r requirements.txt
python -m unittest -v test_gmm
python gmm_em.py
```

The last command rewrites the `results/` outputs. You can change the dataset, output folder, or restart count with `--data`, `--out` or `--restarts` (e.g. `python gmm_em.py --restarts 12`). Run the **default command**, not a reduced-restart shortcut, when demonstrating the five-minute requirement. Record the elapsed time on the machine used for demonstration.

**Implementation:** full 2×2 covariance per component; custom log-sum-exp and multivariate Gaussian log-density; responsibility-weighted E-step/M-step; distance-weighted initialization followed by ten Lloyd iterations; 12 random restarts for each K (seeds 42–53); small covariance regularization `1e-6`; relative likelihood-change threshold `1e-7`; maximum 1,000 EM iterations. The converged run with maximum log-likelihood is selected for each K. All calculations of likelihood, weights, means, covariances, AIC and BIC are performed by project code, not a pre-built mixture model.

## Findings from supplied data

- Input shape: **1,000 × 2**, no non-finite values, 999 unique rows (one repeated observation retained).
- Model comparison, full-covariance GMM with 12 restarts per K:

| K | Log-likelihood | AIC ↓ | BIC ↓ | Best-run EM iterations |
|---|---:|---:|---:|---:|
| 2 | −5091.6974 | 10205.39 | 10259.38 | 16 |
| 3 | −4955.6770 | 9945.35 | **10028.79** | 32 |
| 4 | −4944.9941 | **9935.99** | 10048.87 | 207 |
| 5 | −4939.5651 | 9937.13 | 10079.46 | 185 |

- **K=3 is recommended by BIC** among *the four candidate values tested*. AIC prefers K=4; that disagreement is reported, not hidden.
- At K=3, the hard assignments contain **193, 396, 411** observations. Hard counts are not equal to the soft mixture weights.
- All **48/48 starts converged** with these settings. Tightening tolerance to `1e-10` changed the best K=3 run from 32 to 39 iterations, improved log-likelihood by only about `0.000190`, and produced the **same hard assignments for all 1,000 observations**. This supports practical convergence, **not a proof of a global optimum**.
- Original end-to-end runtime in the authoring environment was **7.934 seconds**, including plotting and the strict convergence rerun, which is below the **300-second** limit; runtime can vary by hardware and environment.

**Interpretation limit:** The CSV identifies columns only as `x1` and `x2`, without physical units or labels. The assignment mentions takeoff weight/reduced thrust as possible context, but the results **cannot establish actual FAA stage lengths or operational categories** without ground truth and aviation metadata.

## Team responsibilities and academic integrity

All team members must understand the EM derivation, execute or review the experiment, contribute fairly and record their own work. `TEAM_CONTRIBUTIONS.md` is a suggested division of work, **not a statement that work has already been completed**. One person submits the final presentation and code for the team; individual peer assessments are still needed per course instructions. Check the e-campus submission format.

## Sources, provenance and AI disclosure

Course handout: *Gaussian Mixture Model (GMM) with Expectation-Maximization (EM)*, Fall 2026, pp. 1–3. Dataset: course-provided `FAA_AEDT_data.csv`. Source code and draft slides were developed with **OpenAI ChatGPT** assistance, including implementation ideas, code drafting, testing, experimental interpretation and presentation drafting. See **`AI_DISCLOSURE.md`** for the full tool/scope/how/prompt disclosure and the **student contribution fields that must be completed before submission**. Consult **`REFERENCES.md`** for the authoritative sources checked on November 24, and cite only sources actually used. Do not claim independent work that was done by AI.
