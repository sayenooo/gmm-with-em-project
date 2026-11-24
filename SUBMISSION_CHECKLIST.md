# Final submission checklist — Fall 2026 GMM/EM group project

**Deadline: Monday, November 30, 2026. No late submissions are accepted.** The handout requires two main deliverables (1) a ~15-minute presentation file and (2) executable simulation code. One person submits on the team's behalf; members may have individual peer assessments.

## Technical — verified on November 24 in the assistant's environment

- [x] The dataset is 1,000×2 and matches the provided CSV.
- [x] E-step and M-step are independently implemented; sklearn GMM is not used.
- [x] Model estimates and scatter plots are generated for K=2,3,4,5.
- [x] Log-likelihood histories, termination criterion and stricter-tolerance sensitivity are documented.
- [x] AIC and BIC comparison is included, with K=3 selected by BIC and K=4 preferred by AIC.
- [x] Four unit tests passed; full analysis completed within five minutes on the assistant's environment.
- [x] A 15-slide PPTX exists with an approximately 15-minute storyline and notes.

## Must be completed by students before handing in

- [ ] Fill in real team members' names on slide 1, plus actual specific independent contributions in `TEAM_CONTRIBUTIONS.md` and `AI_DISCLOSURE.md`.
- [ ] Confirm AI disclosure is present at the end of the final submitted materials; also check it is consistent with slide 15.
- [ ] Rerun `python -m unittest -v test_gmm` and `python gmm_em.py` in the environment used to demonstrate the assignment; verify runtime <300 seconds.
- [ ] Rehearse the presentation at ~15 minutes; divide actual slide speaking assignments fairly.
- [ ] Confirm only the permitted final deliverables and any required supporting files are submitted through the course portal by the deadline.
- [ ] If the course dataset is not permitted to be publicly redistributed, make the GitHub repo private or remove data from its full history, and keep the dataset in the submitted materials only as permitted by the course.
- [ ] Complete individual peer assessments according to the instructor's directions.

## Commands

```bash
python -m pip install -r requirements.txt
python -m unittest -v test_gmm
python gmm_em.py
```

Do not replace the from-scratch EM code with a library mixture model. **Do not label statistical Gaussian groups as verified operational stage lengths**: the supplied CSV contains only `x1`,`x2` with no units or ground-truth stage-length labels.
