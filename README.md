# Gaussian Mixture Model with EM

Application of AI in Aerospace · Sejong University · Fall 2026

Team: Maisha, Zhansaya, Chaewon

## Run

Python 3.10 or later.

```bash
python -m pip install -r requirements.txt
python gmm.py
```

The script implements GMM with EM from scratch using NumPy. Matplotlib draws the plots. No prebuilt clustering model is used.

- E-step: calculate posterior probabilities (responsibilities).
- M-step: update mixture weights, means and covariance matrices.
- Repeat until the relative log-likelihood change is at most 1e-7, or 2,000 iterations.
- Run 12 initializations per K (seeds 42–53); retain the converged run with the highest likelihood.
- Compare K=2, 3, 4, 5 using AIC and BIC.

The dataset contains 1,000 observations and two features (x1, x2). The script creates `results/` with four scatter plots, convergence and model-selection plots, likelihood histories, metrics and a summary.

## Results

Reference run on the supplied CSV:

| K | Log-likelihood | AIC | BIC | Iterations |
|---:|---:|---:|---:|---:|
| 2 | -5091.70 | 10205.39 | 10259.38 | 13 |
| 3 | -4955.68 | 9945.35 | **10028.79** | 36 |
| 4 | -4944.99 | 9935.99 | 10048.87 | 131 |
| 5 | -4937.71 | **9933.41** | 10075.74 | 525 |

BIC selects K=3; AIC selects K=5. BIC applies a stronger complexity penalty for this dataset. All 48 starts converged in the reference run. For K=3, tightening the tolerance to 1e-10 increased iterations from 36 to 43, improved log-likelihood by approximately 0.000133 and preserved all 1,000 cluster assignments for the same seed. This supports practical convergence, not a guaranteed global optimum.

Reference runtime: 3.45 seconds (single-threaded OpenBLAS, headless Matplotlib); runtime varies by computer. The CSV does not specify physical feature units or actual FAA stage lengths.

## Sources and disclosure

Course-provided FAA_AEDT_data.csv and GMM with EM project description; see [AI disclosure](AI_DISCLOSURE.md). Team members must review, reproduce and explain the code and record their actual contributions before submission. The presentation is a separate deliverable and must use the results above, not the archived experiment.
