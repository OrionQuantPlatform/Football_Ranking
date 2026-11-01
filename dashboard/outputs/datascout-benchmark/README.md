# Evidence for the DataScout functional benchmark

Captured on 2026-11-01 through the existing Codex in-app browser free account. Scope: research and comparison; no app code changes, purchase, save, favorite, vote or export submission.

- `browser-observations.json`: ordered fifteen-step walkthrough, covering thirteen primary tools, plus current live Orion verification and explicit limits.
- `01`–`23` JPEGs: screenshots captured in the current run. Loading/blank initial captures were rejected and replaced; `06-coaches.jpg` deliberately retains the onboarding overlay. All accepted files were opened or emitted and inspected before use in the report.
- `data-readiness.json`: all current-season performance partitions, field coverage and missing prerequisites.
- `profile-field-inventory.json`: fields across all indexed player/team profile observation tables. Observation counts include versions and must not be interpreted as unique players.
- `inspect_orion_data.py`: read-only reproducible inventory. Run from the repository root with `python3 dashboard/outputs/datascout-benchmark/inspect_orion_data.py`.
- Full comparison and ordered screenshot gallery: `docs/DATASCOUT_BENCHMARK.md` at the repository root.

Browser rerun: start at https://datascout.pro/fr with the existing free session. Follow the thirteen tool links listed in the report. Search Hakimi in the player profile and select the median comparison; generate Hakimi vs Nuno Mendes in the comparison tool; choose xG/90 and xA/90 in the scatter axes picker; search PSG for team/builder/simulator and Luis Enrique for coach analysis. In scouting select DD and +60 minutes per match without saving. Read the daily player’s public projection/similarity example, without voting. Dismiss tutorials if they obscure controls, wait for data to replace loading placeholders, save and inspect each resulting screenshot. The exact player/day and data can change; dates, URLs and inputs from this run are in the journal.

Observed results: a real comparison radar and scatter rendered, ranking tables loaded, the scouting query returned 38 rows, team/coach profiles and builder/simulator loaded, and the daily example showed similarity/projection/club-fit explanations. Standard player projection was subscription-limited. No predictive model, paid workflow, download, native mobile app or complete accessibility compliance was validated.

Navigation from selected coach/builder contexts did not always leave the current state; a fresh in-app tab allowed the remaining tools to be inspected. Some initial locators were too exact for split metric labels or selected chips; subsequent targets came from fresh DOM/AX observations. These inspection failures are not reported as successful interactions.

Suggested commit: `docs: compare DataScout features with Orion`.
