# GMM + EM oral defense — questions and short evidence-based answers

**Q1. What exactly did you implement from scratch?**  We wrote the Gaussian log-density, stable log-sum-exp, responsibilities (E-step), weighted updates of mixture weights/means/full covariance (M-step), EM iteration and stopping, restart selection, and AIC/BIC computations using NumPy. `sklearn.GaussianMixture` was not used.

**Q2. What is the E-step?**  Given current model parameters, estimate `gamma_ij = pi_j N(x_i|mu_j,Sigma_j) / sum_m pi_m N(x_i|mu_m,Sigma_m)`, the posterior probability that observation `i` belongs to component `j`.

**Q3. What is the M-step?**  With `N_j = sum_i gamma_ij`, update `pi_j=N_j/N`, `mu_j=sum_i gamma_ij*x_i/N_j`, and covariance as the responsibility-weighted outer product around the new mean, divided by `N_j`; small diagonal regularization stabilizes numerics.

**Q4. Why full covariance rather than spherical covariance?**  The supplied scatter has clusters that are elongated/rotated. A full 2×2 covariance allows different widths, orientations and correlations; the cost is extra model parameters.

**Q5. How do we know enough iterations ran?**  All 48 restarts met the specified likelihood-change stopping rule. In the best K=3 run, tightening tolerance from `1e-7` to `1e-10` raised iterations from 32 to 39, but did not alter any of the 1,000 hard assignments; total log-likelihood improved by only about 0.000190. This supports convergence to a stable local solution, *not a global optimality proof*.

**Q6. Why K=3 if AIC prefers K=4?**  We compared all required K=2–5. BIC penalizes the number of parameters more strongly for N=1,000 and has its lowest value at K=3 (10,028.79). AIC has its minimum at K=4 (9,935.99), so we clearly report the disagreement and choose the more parsimonious 3-component model by BIC.

**Q7. What is the parameter count?**  For K components in d=2 with full covariance: `K-1` independent mixture weights, `2K` means, and `3K` covariance parameters. Thus `p=6K-1`; AIC=`2p-2LL`, BIC=`p ln(N)-2LL`.

**Q8. Does a cluster identify a flight stage length?**  No. The course CSV supplies unlabeled `x1`,`x2` without physical units or stage-length ground truth. Clustering highlights statistical structure only. Validating actual stage lengths requires separate operational annotations/domain data.

**Q9. Why are cluster counts different from mixture weights?**  Hard counts assign each point to its single largest posterior component. Mixture weights summarize expected soft membership across all points; ambiguity causes the two to differ.

**Q10. Did you use AI and what did students do?**  Describe AI usage transparently as stated in `AI_DISCLOSURE.md`, then give the **specific true student contributions actually completed**. Do not claim fully independent authorship of AI-drafted parts.

**Q11. What limitations remain?**  Local optima, covariance modeling assumptions, no external labels or domain metadata, and only four candidate values of K required by the handout.

**Q12. What were the runtime and tests?**  The original end-to-end experiment took 7.934 seconds in the authoring environment, below 300 seconds, and all four Python unit tests passed. Other hardware may differ, so each student should rerun the code.
