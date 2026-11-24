# FAA AEDT clustering — GMM with EM

Working draft for the Fall 2026 group assignment, due November 30, 2026. The team must review, understand, independently verify and document its actual contributions before submission.

## Run
Python 3.10+; use a terminal in this folder.

```sh
python -m pip install -r requirements.txt
python -m unittest -v test_gmm
python gmm_em.py
```

No scikit-learn, SciPy or built-in GMM/EM is used. NumPy handles arrays and linear algebra; Matplotlib handles plots. Default 12 restarts per K (seeds 42–53), full covariance, regularization 1e-6, relative log-likelihood tolerance 1e-7, maximum 1000 EM updates. Best converged run selected by maximum likelihood. The script generates all tables and figures under `results/`. Time measured includes plotting and stricter convergence check; it varies by machine.

## Findings (provided CSV)
1000 rows, two numeric features, no missing/non-finite values; 999 unique rows (one repeated observation retained). No physical feature meanings or units confirmed by the CSV. BIC selects K=3 among K=2–5, AIC selects K=4. K=3 has 193, 396, 411 hard-assigned observations. All 48 starts converged. Strict tolerance 1e-10 produced identical assignments; log-likelihood improved by 0.000190. This supports practical convergence, not a proof of global optimality. Runtime in the authoring environment 7.934 seconds. Results are exploratory and cannot establish actual stage lengths without operational metadata or ground truth.

## Team work (proposed; record actual work)
- Member A: verify the derivation, initialization, E-step and M-step, write independent checks.
- Member B: reproduce experiments, investigate sensitivity to seeds/tolerance and compare BIC/AIC.
- Member C: explain AEDT background, figures, limitations, presentation and rehearsal.
- All: review code, interpret results, rehearse Q&A, and document actual contributions. Adapt roles to team size. One member submits on behalf of the team; peer assessment is individual.

## Sources & AI disclosure (must be finalized)
- Course handout: *Gaussian Mixture Model (GMM) with Expectation-Maximization (EM)*, Fall 2026, pp. 1–3. Dataset: FAA_AEDT_data.csv, supplied through the course.
- OpenAI ChatGPT (GPT-6.2), used on November 24, 2026 to interpret requirements, draft the NumPy EM implementation, run experiments and tests in its environment, generate visualizations, interpret the model-selection and convergence results, and draft slides and speaker notes. AI-generated code and materials are included in this draft. Prompt: “бро нам задали задание групповой проект плиз помоги нам сделать этот проект” with the handout and CSV attached.
- Independent student work: [replace with specific verified tasks performed by each member; do not claim work not completed].
- Add any other external sources actually used by team members; preserve the disclosure in the final deck and code documentation.
