# Simple GMM with EM — learning version

This alternative implementation is independent of the previous experiment in the repository. Run from the repository root:

```bash
python -m pip install -r requirements.txt
python simple/gmm.py
```

Only NumPy and Matplotlib are needed. No prebuilt clustering model is used.
The script loads the original 1000 x 2 CSV, uses random initial means, equal weights and a shared initial full covariance, then alternates E-step and M-step. Each K=2,3,4,5 uses 12 deterministic starts (42–53); the highest-likelihood converged run is retained. The relative likelihood tolerance is 1e-7, with a 2000-iteration limit and a 1e-6 covariance adjustment.

Outputs are generated in simple/simple_results: four scatter plots, likelihood histories, convergence and model-selection plots, a numerical table and summary.

## Local verification (26 November 2026)

| K | Log-likelihood | AIC | BIC | Iterations |
|---:|---:|---:|---:|---:|
| 2 | -5091.6974 | 10205.39 | 10259.38 | 13 |
| 3 | -4955.6769 | 9945.35 | 10028.79 | 36 |
| 4 | -4944.9942 | 9935.99 | 10048.87 | 131 |
| 5 | -4937.7056 | 9933.41 | 10075.74 | 525 |

All 48 starts converged. BIC selects K=3; AIC selects K=5. A strict rerun at tolerance 1e-10 changes the iteration count from 36 to 43, improves LL by 0.00013300 and preserves all 1000 labels for the same initialization. Runtime was 3.450 seconds in the local review environment (OPENBLAS_NUM_THREADS=1, MPLBACKEND=Agg); machine-dependent.

The older root README, results and slides refer to the previous experiment. Do not mix results from the two versions. Feature names are x1 and x2; physical units and actual FAA stage lengths cannot be inferred from the CSV alone.

## AI disclosure

OpenAI ChatGPT assisted with writing this alternative implementation, explaining the algorithm, generating plots and running numerical checks. Before submission, team members should independently review, run and explain the code, update the slides and document their actual contributions. Do not claim independent work that has not been completed. See also the root AI_DISCLOSURE.md and the course's disclosure requirements.
