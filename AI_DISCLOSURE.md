# AI usage disclosure — complete and review before submission

This document is intended to accompany the team's submitted code and presentation. **The statements about AI-generated work below describe the actual history of this draft; fields for independent student work must be filled in by the people who did that work.**

## 1. Which AI tool was used?

**OpenAI ChatGPT**, used on **November 24, 2026**. The exact underlying model/version was not independently verified and is therefore **not asserted**.

## 2. Which parts did AI assist with?

- Interpreting the three-page course handout and extracting submission requirements.
- Drafting the NumPy-based Gaussian mixture model and EM implementation, the Python tests, command-line workflow and project README.
- Running the provided FAA CSV through the draft implementation in the assistant's execution environment and generating clustering, model-selection and convergence plots and CSV summaries.
- Drafting the storyline, English presentation slides and presenter notes.
- Auditing the GitHub repository against the assignment and identifying work to complete before submission.

## 3. How was AI used?

ChatGPT suggested designs, drafted code and explanatory text, executed development tests/experiments, inspected results, and helped check that requested deliverables were present. **These artifacts should be treated as AI-assisted drafts unless the students have reviewed, modified and verified them.** The project intentionally does not import a ready-made GMM/EM estimator; the E- and M-step formulas are implemented in `gmm_em.py` using NumPy arithmetic and linear algebra.

## 4. Which parts did students complete independently?

**To be completed truthfully by the team before submitting.** Do not copy sample duties as facts. Use the following format:

| Student full name / ID | Independently completed and verified work | Evidence (commit, test, calculations, slide, rehearsal) |
|---|---|---|
| [Member 1] | [Exact tasks actually done] | [Evidence] |
| [Member 2] | [Exact tasks actually done] | [Evidence] |
| [Member 3, if applicable] | [Exact tasks actually done] | [Evidence] |

If the AI-assisted code or slides were submitted unchanged, disclose that plainly; **do not misstate the independent contribution**. Additional team members may be added or the rows adjusted to the real team size.

## 5. Actual prompts (recommended by the handout)

Original prompt with `GMM_with_EM_project_description.pdf` and `FAA_AEDT_data.csv`:

> бро нам задали задание групповой проект плиз помоги нам сделать этот проект

Further requests in the same ChatGPT discussion included committing the resulting project to `https://github.com/sayenooo/gmm-with-em-project`, checking its correspondence with the assignment and refining final-submission materials. These paraphrased follow-up descriptions should not be presented as exact verbatim quotes. Add any other tools and exact prompts used by team members, where relevant.

## References

1. Course assignment handout, *Gaussian Mixture Model (GMM) with Expectation-Maximization (EM)*, Fall 2026, pages 1–3 (source of the FAA/AEDT problem statement and formal assignment constraints).
2. `FAA_AEDT_data.csv`, course-supplied data file.
3. OpenAI ChatGPT, AI-assisted draft development session, November 24, 2026 (as documented above).

**Final checklist:** Add this disclosure to the final submission package, ensure slide 15 matches it, complete the verified independent contributions, and cite any additional sources actually consulted.
