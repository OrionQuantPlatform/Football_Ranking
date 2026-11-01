# Scoped annotation redesign

Targets: overview data filters; Achraf Hakimi performance dialog; Troyes–Le Mans match m_4XOc3a in season2026/2027. Preserve genuine Next App Router, Bun API, canonical JSON and other sections.

Design acceptance: labeled, spacious filters and visible applied state with reset; player identity/observed provider rating and a small primary KPI row, remaining metrics grouped logically with null distinct from zero; match begins with competition/date/score, teams and key observed statistics, then purposeful sections for overview, shots, players, lineups and all13 collected data families. Remove season-wide filters/appearance export from a single-match detail. Keep navigation back to filtered list, player selection/comparison, archive download and all raw fields accessible. No invented performance scores or data.

Failure modes: filter/input focus or URL state lost; short labels obscure duplicated competitions; close/escape/focus return broken; null converts tozero; mixed team stat columns; aggregate percentages extrapolated from missing denominators; default detail causes huge vertical raw dumps; hidden tabs fetch incorrectly or drop13 families; small screen overflow.

E2E expected: select Ligue1/2026-2027 and search; verify counts/URL/reset; open Hakimi, verify71min/9.84/3goals/2assists and grouped metrics; compare/close keyboard; navigate match, see2–0, xG1.70–0.28, team-labeled stats, shot map/timeline,22 lineups, player dialog and raw JSON. Inspect desktop and390px; verify no document overflow, active controls and console. Save before/after screenshots, exact setup/commands and actual outcomes after every run. Run production build and existing affected regressions; keep data unchanged and dist absent. No new unit tests after implementation.
