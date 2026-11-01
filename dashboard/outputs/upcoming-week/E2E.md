# Upcoming fixtures: verification

## Setup and rerun

- Repository: OrionQuantPlatform/Football_Ranking; canonical fixture tables from data commit `36a8151b42de017fc90433fe0f135d3cc26acff5`, unchanged by this feature.
- Next.js 16.4.3 / React 19.2, Bun 1.4.4, Python 3 with `zoneinfo`; Europe/Paris calendar weeks.
- Local browser run: `http://127.0.0.1:3000`, Next development server and Bun API on port 8765.
- Start the same local application from `dashboard`: `PATH="$HOME/.bun/bin:$PATH" bun run dev`.
- Run production build and existing regressions from `dashboard`: `PATH="$HOME/.bun/bin:$PATH" ORION_EVIDENCE_DIR=outputs/upcoming-week bun run test`.
- Check source formatting from `dashboard`: `PATH="$HOME/.bun/bin:$PATH" bun run format:check`.
- Reconcile the saved browser observations independently from the repository root: `python3 dashboard/outputs/upcoming-week/verify_browser.py`.

The oracle reads the canonical fixture tables, verifies their manifest hashes, selects the requested season/scope/competition/week/search, and independently converts timestamps using Python's Europe/Paris zone database. Simultaneous kickoffs may have different opaque-ID collation in Python and JavaScript; the oracle verifies their membership and chronology, and reconciles all four pagination pages together.

## Expected and observed

| Workflow | Expected / observed |
| --- | --- |
| Overview → Calendrier | Six real upcoming fixtures before 19:00 Paris on November 1; crests, competition, kickoff and fixture links; no fabricated scores. |
| Next week | November 2–8: all 127 Europe-focus fixtures reachable on four pages (40/40/40/7), unique and chronological. |
| Competition and search | Champions League: 18. Search `atletico`: one Atlético Madrid–Bayern fixture. |
| Detail and return | Upcoming kickoff shown instead of a score; breadcrumb preserves November 2 week, Champions League and search. |
| All competitions | 403 next-week fixtures; Ligue 2 filter returns 11. Europe toggle clears the excluded Ligue 2 selection and restores ten competitions. |
| Calendar controls | Playing-time filter and appearance export absent. |
| Mobile and keyboard | 390×844: document and main width 390, no document overflow; Tab from search focuses competition with visible outline. |
| Old season | 2024/2025 produces an empty upcoming week; current-season action returns to 2026/2027. |
| Time exclusion | Current-week Europe selection becomes four after the two 19:00 kickoffs. |
| Unknown time | Hoffenheim II–Saarbrücken, December 5: “Horaire à confirmer”, no invented midnight. |
| Year boundary | December 28–January 3 contains 20 Premier League fixtures; next-week navigation selects January 4–10 with ten. |
| Daylight saving | March 28, 2027 Eibar–FC Andorra at 13:00 UTC displays 15:00 Paris; Monday–Sunday bounds remain March 22–28. |
| Invalid week | Invalid February 30 falls back to the current valid week with four upcoming fixtures. |

Screenshots and DOM observations are adjacent to this file. `oracle-results.json` records per-scenario canonical counts. `regression-final.log` records a successful production build, 27 Python tests and 53 Node tests; the existing HTTP E2E verifies all nine Next routes, the Bun API/data/archive boundary and private-file isolation. `http-evidence.json` and `http-runtime.log` retain its actual results. `format-final.log` passes.

## Timing and limits

Client selection refreshes every 30 seconds and when the document regains visibility. An observation eight seconds after 19:00 still showed six fixtures within that refresh window; it remains in `browser-evidence.json` as an observation, excluded from the exact-time oracle comparisons. A subsequent current-season load showed four and passed the canonical oracle. The natural in-place transition at the next kickoff and actual Monday midnight were not separately waited for. Provider changes remain subject to the existing daily collection.

No synthetic duplicates, malformed source dates or simulated browser clock were injected. Duplicate IDs and invalid/ambiguous dates are guarded in the selector and reviewed; no new isolated tests were added after implementation.

## Preserved failed attempts

- `regression.log`: initial shell lacked Bun on PATH; corrected explicit PATH in the successful retry and final logs.
- `format.log`: CSS formatting warning, corrected by Prettier; final check passes.
- `oracle.log` / `oracle-first-failure.json`: initial oracle incorrectly required Python ASCII ordering within simultaneous kickoffs.
- `oracle-retry.log`: oracle did not handle null `time_utc`; corrected the oracle's missing-time parsing, then reran successfully.
- Browser automation first addressed the scope control as a DOM checkbox. It is a native button with `aria-pressed` (exposed as a checkbox by macOS AX); selecting its visible text worked.

These failures are retained and are not represented as successful runs.

## Original production release

Feature commit `c2ae7ea74f869b4b62d2a6ba19b36094e310b7c2` deployed automatically from Git as `dpl_Hf6fRb9gMQHJw5kwiawbxZwEeMeX`, READY. `deployment-feature.json` retains the connector readback. The project is currently named football-analytics; the established orion-football-ranking.vercel.app alias remains attached.

Live browser verification covered overview → calendar → next week → Champions League → Paris search → upcoming detail → selected-week return → reset. The independent oracle passes 28 checks including complete 127-fixture pagination. `cloud-evidence.json` passes nine routes, Bun health/configuration, six seasons, thirteen archive families, private-file isolation and an immutable no-store redirect to this exact commit. Rerun from `dashboard`: `PATH="$HOME/.bun/bin:$PATH" ORION_VERIFY_URL=https://orion-football-ranking.vercel.app ORION_CLOUD_EVIDENCE=outputs/upcoming-week/cloud-evidence.json bun scripts/verify_cloud.mjs`.

The user subsequently requested merging calendar/results into Matchs and removing Calendar/Method from the topbar. This folder preserves the original release's evidence; the refinement is verified separately in outputs/matches-unified.
