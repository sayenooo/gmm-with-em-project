# FAA AEDT — Gaussian Mixture Model with EM

Application of AI in Aerospace · Sejong University · Fall 2026

Team: Maisha, Zhansaya, Chaewon

## Run the project

Use Python 3.10 or newer. Keep the three Python files and the dataset in the same folder.

```bash
python -m pip install -r requirements.txt
python -m unittest -v test_gmm
python gmm_em.py
```

The final command trains K=2, 3, 4, 5, prints the results, and writes figures and CSV tables to `results/`. It does not use a prebuilt GMM implementation.

## Read the code

| File | Purpose |
|---|---|
| [gmm_em.py](gmm_em.py) | Initialization, E-step, M-step, EM loop, AIC/BIC, experiment |
| [gmm_report.py](gmm_report.py) | Save tables and draw plots |
| [test_gmm.py](test_gmm.py) | Four correctness checks |
| [FAA_AEDT_data.csv](FAA_AEDT_data.csv) | 1,000 two-dimensional observations |

In EM, the E-step computes responsibilities; the M-step updates mixture weights, means, and covariance matrices. The loop stops when the relative change in log-likelihood is at most 1e-7 (maximum 1,000 iterations). Each K uses 12 starts with seeds 42–53, distance-weighted initialization and ten nearest-center updates. We retain the converged run with the highest log-likelihood. A covariance adjustment of 1e-6 and log-space calculations protect numerical stability.

## Results

| K | Log-likelihood | AIC | BIC | Iterations |
|---|---:|---:|---:|---:|
| 2 | -5091.6974 | 10205.39 | 10259.38 | 16 |
| 3 | -4955.6770 | 9945.35 | **10028.79** | 32 |
| 4 | -4944.9941 | **9935.99** | 10048.87 | 207 |
| 5 | -4939.5651 | 9937.13 | 10079.46 | 185 |

BIC favors K=3 among the four candidates; AIC favors K=4. At K=3 the hard cluster counts are 193, 396 and 411. A stricter tolerance (1e-10) changes 32 iterations to 39, improves likelihood by about 0.000190 and leaves all 1,000 assignments unchanged. This supports practical convergence, not a global optimum.

- [Scatter plots](results/clusters_all.png)
- [Convergence](results/convergence.png)
- [Model comparison](results/model_selection.png)
- [Numerical results](results/model_selection.csv)

Latest refactor check (26 November 2026): four unit tests passed; all 48 starts converged; all nine numerical CSV files matched the preceding run to absolute/relative tolerance 1e-9. End-to-end runtime was 6.098 seconds with OPENBLAS_NUM_THREADS=1, NumPy 2.3.5 and Matplotlib 3.10.8 in the review environment. Existing figures and tables remain historical outputs; run the code to regenerate them. Runtime varies by machine. The optional --data, --out and --restarts arguments remain supported; use defaults for the reported experiment.

The dataset identifies its features only as x1 and x2. Do not claim that these clusters establish actual FAA stage lengths or physical quantities without additional metadata.

## Submission and defense

Submit one 15-minute presentation and the simulation code per team by 30 November 2026. Each student completes the separate peer assessment. Check the course submission format.

- [Presentation guide](PRESENTATION_GUIDE.md) and [existing slides](FAA_GMM_EM_presentation.pptx)
- [Defense Q&A](DEFENSE_QA.md)
- [Validation steps](VALIDATION_STEPS.md) and [historical audit](REPRODUCTION_AUDIT.md)
- [References](REFERENCES.md)
- [AI disclosure](AI_DISCLOSURE.md)
- [Team contributions](TEAM_CONTRIBUTIONS.md)

AI assisted with code drafting, refactoring, experiments, validation, and presentation materials. The team must review and execute the code and accurately document independent contributions and AI use before submission.
