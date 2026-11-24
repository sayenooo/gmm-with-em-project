# Team contributions — complete with real names and actual work

> **Not yet a factual contribution statement.** Fill this out together before the submission and peer assessments. The suggested tasks below are *proposals*, not evidence that a student performed them.

## Team roster

| Student | Full legal name | Student ID (only if required by instructor) | Assigned responsibilities | Work actually completed | Evidence reviewed by the team |
|---|---|---|---|---|---|
| 1 | [NAME] | [ID / N/A] | [ROLE] | [SPECIFIC WORK DONE] | [TEST/COMMIT/SLIDE] |
| 2 | [NAME] | [ID / N/A] | [ROLE] | [SPECIFIC WORK DONE] | [TEST/COMMIT/SLIDE] |
| 3 (remove if not applicable) | [NAME] | [ID / N/A] | [ROLE] | [SPECIFIC WORK DONE] | [TEST/COMMIT/SLIDE] |

## Suggested equitable work split (adapt to team size)

- **Method / implementation:** derive GMM E- and M-step updates; independently inspect `gmm_em.py`; verify probability normalization, covariance regularization, and unit tests.
- **Experiments / validation:** reproduce results for K=2,3,4,5; check all scatter plots and BIC/AIC calculations; review log-likelihood, restarts and strict tolerance sensitivity.
- **Presentation / context:** understand the AEDT motivation and limits of unlabeled variables; check the slide deck; prepare English speaker notes and citations; run a 15-minute rehearsal.
- **Everyone:** understand the derivation and choice of K, document any AI use and actual original work, review the final submission.

## Independent verification sign-off

- [ ] Each student ran `python -m unittest -v test_gmm` or reviewed the test results and understands their meaning.
- [ ] Each student can explain the E-step, M-step, why GMM differs from k-means, and why BIC selected K=3.
- [ ] We checked the actual 15-minute talk timing.
- [ ] The team reviewed `AI_DISCLOSURE.md` and verified its truthfulness, including individual work.
- [ ] The full names on presentation slide 1 match the people submitting the work.
- [ ] We assigned one actual team member to upload the two deliverables on behalf of the team.

**Peer assessment:** Each student submits their own peer assessment if and as instructed by the course. Do not invent or pre-fill the assessments.
