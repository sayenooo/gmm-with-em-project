# Reproduction audit — November 26, 2026

## Scope and provenance

OpenAI ChatGPT independently inspected the existing repository and repeated the experiment using the uploaded course CSV. Direct Git cloning was unavailable (DNS resolution), so the two Python files were reconstructed from GitHub connector contents. Git blob hashes were verified against the repository before execution:
- gmm_em.py: b2db68a0b0e1a391ace1502dc40e83361310bfcb
- test_gmm.py: cb6d1de09baf38c731dab9ce8c26eff2c8c71357
- FAA_AEDT_data.csv: 3bc12aef533304e41002385665d6f24166fac7d6

No original implementation or result files were changed. The existing PowerPoint was located but not rendered or independently inspected in this audit.

## Default experiment

Environment: Python 3.13.5, NumPy 2.3.5, Matplotlib 3.10.8, OPENBLAS_NUM_THREADS=1.

Commands: `python -m unittest -v test_gmm` and `python gmm_em.py`.

- Four unit tests passed.
- 1,000 finite observations, two features, 999 distinct rows; repeated observation retained.
- End-to-end runtime: 8.320 seconds, including plots and stricter convergence rerun (excluding installation).
- All 48/48 default starts converged.

| K | Log-likelihood | AIC | BIC | Best-run iterations |
|---:|---:|---:|---:|---:|
| 2 | -5091.697400 | 10205.394801 | 10259.380109 | 16 |
| 3 | -4955.676997 | 9945.353995 | 10028.785834 | 32 |
| 4 | -4944.994124 | 9935.988248 | 10048.866619 | 207 |
| 5 | -4939.565066 | 9937.130133 | 10079.455036 | 185 |

For K=3, the stricter relative tolerance of 1e-10 yielded 39 iterations instead of 32, increased log-likelihood by 0.000189782, and preserved 100% of hard assignments. Counts: 193, 396, 411.

## Additional seed sensitivity check

Using the same implementation and 12 starts per K, with seeds 100–111 instead of 42–53:

| K | Log-likelihood | AIC | BIC | Best-run iterations | Converged starts |
|---:|---:|---:|---:|---:|---:|
| 2 | -5091.697380 | 10205.394759 | 10259.380067 | 17 | 12/12 |
| 3 | -4955.676945 | 9945.353889 | 10028.785729 | 22 | 12/12 |
| 4 | -4944.994081 | 9935.988162 | 10048.866533 | 206 | 12/12 |
| 5 | -4941.916635 | 9941.833269 | 10084.158172 | 440 | 12/12 |

Reproduce from the repository directory:
```bash
python -c "import numpy as np; from gmm_em import fit; X=np.loadtxt('FAA_AEDT_data.csv',delimiter=',',skiprows=1); [(lambda m: print(m['k'],m['ll'],m['aic'],m['bic'],m['iterations'],sum(r['converged'] for r in m['runs'])))(fit(X,k,restarts=12,seed=100)) for k in (2,3,4,5)]"
```

BIC still prefers K=3; AIC still prefers K=4. The alternative K=5 solution has lower likelihood than the default best K=5 solution, illustrating EM's sensitivity to initialization. These are empirical checks, not a guarantee of global optimality or true operational stage-length labels.

## Remaining submission checks

- Team members must independently review the code, reproduce results on the presentation machine, verify actual contributions and complete the team and AI disclosure fields truthfully.
- Check the final presentation, names, citations, and 15-minute timing.
- Confirm course permission to redistribute the supplied dataset publicly.
- The columns are x1 and x2 without physical units or stage-length labels. Do not interpret the clusters as validated FAA operational categories.

## Additional AI disclosure

OpenAI ChatGPT assisted on November 26 with repository inspection, reproduction of the existing implementation, runtime and convergence checks, an alternate-seed experiment, and this audit document. These tasks were performed by AI and are not evidence of independent student work. This document supplements AI_DISCLOSURE.md; include this additional assistance in the final submission disclosure. Student contributions must be completed and verified by the actual team.
