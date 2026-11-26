# AI disclosure — final wording to review and customize before submission

The instructor requires **(1) tool, (2) assisted portions, (3) how it assisted, (4) independently completed student work, (5) prompt record (optional but recommended)**. Do not sign/submit the document with unfilled student contribution fields.

## English disclosure for the submission (factual record of this project)

**Tool and date:** OpenAI ChatGPT, November 24, 2026. No unverified model-version claim is made.

**What it assisted with and how:** ChatGPT helped interpret the course instructions; **generated an initial Python GMM/EM implementation, tests and experiment scripts**; executed the supplied two-dimensional CSV to produce draft clustering figures, convergence/model-selection summaries and validation logs; reviewed the code and outputs against the assignment step by step; improved the presentation structure, visual formatting and speaker notes; and helped locate and verify academic/official sources. The algorithmic implementation uses project-written NumPy formulas and **does not call a ready-made GMM estimator**. 'From scratch' describes the absence of a prebuilt model in the code, **not a claim that the code was typed without AI assistance**.

**What students completed independently:** [INSERT verified specific actions by each actual member: e.g., reproduced runs, independently derived/checked EM updates, changed code, reviewed citations, validated numerical results, rehearsed slides]. For each claim provide a name and evidence (commit, calculation, local log, or rehearsal). If a draft AI-produced artifact was used without substantive revision, state that rather than calling it independently authored.

**Representative exact prompts:**
- "бро нам задали задание групповой проект плиз помоги нам сделать этот проект" (course PDF + CSV attached).
- "бро все что ты сделал закоммит в [https://github.com/sayenooo/gmm-with-em-project](https://github.com/sayenooo/gmm-with-em-project)".
- "бро проверь по соответсвию вот задание наше".
- "брооооооооооо можно плиз написать в ai disclosure что ты только помог офрмить презентацию и проверил на корректность то что мы разработала step by step бро и потом точно ли все provided кажется sources мало нам нужны достоверные информации короче бро давай переделай проверь интрукции к проекту еще раз".

**Sources:** See `REFERENCES.md` for the published EM/GMM theory, AIC/BIC foundations and official FAA AEDT context; the assignment PDF and supplied CSV are the primary project materials.

## Before submission — student fact check

1. Review `gmm_em.py` and all results; do not claim it was independently authored solely by students if it was generated with AI help.
2. Add each member's **true** contribution in `TEAM_CONTRIBUTIONS.md`, and replace the student-work placeholder above with a truthful, precise statement.
3. Ensure the final presentation's last slide and this file tell the same story.
4. Include any additional AI tools, prompts or external sources actually used by the students.

**Why not say “AI only formatted the slides and checked our code”?** That would contradict the documented chat in which ChatGPT created the initial code, ran experiments and drafted the deck. Such a statement would not satisfy the handout's requirement to accurately describe which sections AI helped with.

## Additional assistance — November 26, 2026

ChatGPT inspected the GitHub repository, verified the Python source and uploaded data against Git blob hashes, reran the four unit tests and default experiment, interpreted reproducibility results, refreshed the 16-slide presentation and speaker notes, and organized the README and presentation guide. This is additional AI-assisted work, not independently completed student work. Representative prompt: “бро давай за это время сделаем assignment по аэроспейс там говорилось вот гитхаб ... надо сделаеть 10/10 презентацию и организовать гитхаб”. The team must still document verified individual contributions and any further assistance before submission.
