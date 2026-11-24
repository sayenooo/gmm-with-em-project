# Verified references, claim mapping and limitations

**Verified/reviewed on:** November 24, 2026. This is a bibliography for the report and presentation, not an assertion that the student team personally read every source; team members should review and understand the ones they use. The external material provides theoretical/contextual support. **All numerical results in this project are computed from the course CSV**, not taken from these sources.

## Course-provided primary materials

**[1] Course handout.** *Gaussian Mixture Model (GMM) with Expectation-Maximization (EM).* Fall 2026, pp. 1–3. Supplied through e-campus as `GMM_with_EM_project_description.pdf`. Evidence for requirements: custom EM/GMM, K=2–5 plots, convergence evidence, optimal K explanation, <5 min code, 15-minute deck, teamwork, and explicit AI disclosure. **Not a publication by FAA.**

**[2] Course dataset.** `FAA_AEDT_data.csv`, supplied with the Fall 2026 assignment; 1,000 observations and two numerical columns `x1`, `x2`. This is the direct input to the experiments. The course handout describes a FAA/AEDT application; the CSV **does not establish** that `x1` is aircraft weight, `x2` is reduced thrust, or that any cluster corresponds to a known stage length. No original FAA database record or field dictionary was supplied.

## Scholarly references for the method and model selection

**[3] Dempster, A. P., Laird, N. M., & Rubin, D. B. (1977).** Maximum likelihood from incomplete data via the EM algorithm. *Journal of the Royal Statistical Society: Series B*, **39**(1), 1–22. https://doi.org/10.1111/j.2517-6161.1977.tb01600.x

Use for: the general expectation-maximization framework, iterative E-step/M-step reasoning and likelihood-based parameter estimation. Publisher: https://academic.oup.com/jrsssb/article/39/1/1/7027539

**[4] Bishop, C. M. (2006).** *Pattern Recognition and Machine Learning.* Springer. Chapter 9, **Mixture Models and EM**, especially §9.2 (Mixtures of Gaussians). Springer ISBN 978-0-387-31073-2. https://link.springer.com/book/9780387310732

Use for: mixture probabilities, posterior responsibilities, mean/covariance update equations, the distinction between hard and soft assignments, and likelihood convergence interpretation.

**[5] Akaike, H. (1974).** A new look at the statistical model identification. *IEEE Transactions on Automatic Control*, **19**(6), 716–723. https://doi.org/10.1109/TAC.1974.1100705

Use for: the Akaike information criterion (AIC); here AIC=2p-2log L. Publisher record: https://ieeexplore.ieee.org/abstract/document/1100705/

**[6] Schwarz, G. (1978).** Estimating the dimension of a model. *The Annals of Statistics*, **6**(2), 461–464. https://doi.org/10.1214/aos/1176344136

Use for: Schwarz's Bayesian information criterion (BIC); here BIC=p log(N)-2log L. DOI metadata: https://cir.nii.ac.jp/crid/1360292619240105088?lang=en

## Official aviation-domain source

**[7] Federal Aviation Administration (FAA), Office of Environment and Energy.** *Aviation Environmental Design Tool (AEDT) — official support website*. https://aedt.faa.gov/ (accessed November 24, 2026). Current product documentation is on https://aedt.faa.gov/4b_information.aspx (AEDT 4b, released September 16, 2026).

Use for: contextual statement that AEDT models aircraft performance and environmental effects, including fuel use, noise and emissions. This site does **not** validate the physical meaning of the unlabeled course columns or provide the course CSV.

## In-slide citation map

| Slides | Supported claim | References |
|---|---|---|
| 2 | AEDT mission and course problem scenario | [1], [7] |
| 3 | The supplied dataset and its 2D structure | [1], [2] |
| 4–7 | Gaussian mixtures, E- and M-step equations and iterative EM | [3], [4] |
| 8–10 | Clustering and convergence *numerical findings* | [2] and project-generated results |
| 11 | AIC and BIC formulas; parameter-count arithmetic done in project | [5], [6] |
| 12–14 | Interpretation and limitations | [1], [2], [4], [7] plus project-generated analysis |
| 15 | Full bibliographic references | [1], [3]–[7] |
| 16 | Actual AI assistance and unverified student-contribution placeholders | `AI_DISCLOSURE.md` |

**Academic integrity:** Cite only material actually used for factual claims. The ChatGPT contribution is a separate AI disclosure, not a peer-reviewed reference. Do not attribute original code, graphs or result tables to the published papers; they were generated in the project workflow.
