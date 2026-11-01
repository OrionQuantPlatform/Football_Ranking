# Annotation redesign — verification evidence

Date: 2026-11-01. Scope: overview filters, the player performance dialog, and match analysis. The existing Next.js App Router frontend and native Bun API remain in use. No new unit tests were added. Canonical `data/` is unchanged against HEAD, including no new untracked data files.

## Setup and exact commands

Existing local JSON records are required. No provider key or new provider request is required for these checks. Runtime: Bun 1.4.4, Next.js 16.4.3. Run from the repository checkout:

```sh
cd "/Users/lemonnierhugo/Desktop/Coding Project/Football_ranking/dashboard"
env PATH="/Users/lemonnierhugo/.bun/bin:$PATH" ORION_EVIDENCE_DIR=outputs/annotation-redesign /Users/lemonnierhugo/.bun/bin/bun run test > outputs/annotation-redesign/regressions-final.log 2>&1
env PATH="/Users/lemonnierhugo/.bun/bin:$PATH" /Users/lemonnierhugo/.bun/bin/bun run format:check > outputs/annotation-redesign/format-check.log 2>&1
```

The test command builds the actual production Next app, runs the existing Python/Node regressions, and invokes the production Next → Bun → canonical JSON HTTP E2E. Its servers use ephemeral ports and are cleaned up automatically.

For the browser workflow, start the local application:

```sh
cd "/Users/lemonnierhugo/Desktop/Coding Project/Football_ranking/dashboard"
env PATH="/Users/lemonnierhugo/.bun/bin:$PATH" /Users/lemonnierhugo/.bun/bin/bun run dev
```

The observed browser used frontend `127.0.0.1:3000` and Bun API `127.0.0.1:8765`. An additional production frontend was verified with the same API using:

```sh
cd "/Users/lemonnierhugo/Desktop/Coding Project/Football_ranking/dashboard"
env NEXT_TELEMETRY_DISABLED=1 /Users/lemonnierhugo/.bun/bin/bun --bun next start frontend --hostname 127.0.0.1 --port 3001 > outputs/annotation-redesign/production-browser.log 2>&1
```

That temporary production server was stopped after verification; the development preview remains running. Browser actions used the Codex in-app browser through `cua_repl`, at 1740×1031 and 390×844. The temporary viewport override was reset afterward.

## Browser inputs, expected outcomes and actual results

1. Open `http://127.0.0.1:3000/?season=2026%2F2027&league=l_3FJFUl`. Expected/actual: labeled controls, Ligue 1 chip, 2,375 appearances and 76 matches. Search, remove the search chip and immediately choose 90 minutes. Expected/actual: empty search, minutes=90 in URL, 964 appearances and 76 matches. Reset yields 133,882 appearances and 4,339 matches with only the season in the URL. Reselecting Ligue 1 restores the original scope. Input focus is retained.
2. On that overview, open Achraf Hakimi from observed performances. Expected/actual: portrait and team identity, PitchAPI rating 9.84, 71 minutes, 3 goals, 2 assists, 6 shots; remaining observations grouped by purpose. Zero remains zero and unavailable keeper fields remain dashes. Comparison toggles successfully. Escape closes the dialog, restores the originating button focus and unlocks body scrolling. Reopen and use its Explorer le match link: the dialog closes and navigates to Le Havre 1–5 PSG (`m_49qvGz`).
3. Open `http://127.0.0.1:3000/matchs?season=2026%2F2027&league=l_3FJFUl&id=m_4XOc3a`. Expected/actual: Troyes 2–0 Le Mans, team xG 1.70–0.28, shots 14–3, shots on target 8–1, possession 39%–61%. No global filter panel or season-wide appearance export appears on an individual match. Six analysis tabs are available.
4. Select Statistiques. Expected/actual: all 37 collected source statistics in four named groups, explicit team columns, and source percentages (12 percentage annotations). Missing or zero-total observations do not create invented comparison shares.
5. Select Tirs & xG, switch map/timeline, and filter Le Mans. Expected/actual: three listed shots and three plotted shot controls. Player controls still open the performance dialog.
6. Select Compositions. Expected/actual: both recorded formations, 22 starters and player profile controls. Select Joueurs: 32 records with playing time; Tous les joueurs exposes all 40 source records. CSV download emits a browser download event for the chosen match scope.
7. Select Données complètes and choose each collected family. Expected/actual: all 13 archive families load, each with its JSON download control: match, events, players, stats, lineups, shots, momentum, h2h, players/halves, advanced, advanced/players, advanced/network and heatmaps. See `archive-checks.json`.
8. Repeat the three surfaces at 390px. Expected/actual: document width remains 390px, the modal stays within the viewport, its body scrolls while background scrolling is locked, and tabs remain operable. ArrowRight selects the next tab; Home/End select first/last; Tab enters the analysis panel.
9. Inspect upcoming fixture `m_3TQyRq` (Young Boys–FC Zürich). Expected/actual: À venir, kickoff time and unavailable statistics as dashes, with no invented 0–0 result. See `upcoming-mobile.jpg` and `upcoming-fixture.json`.
10. Repeat match overview, statistics, lineups and an archived player profile on production port 3001. Expected/actual: 2–0, zero global filter panels, six tabs, 37 stats with 12 source percentages, 22 starters and a working Hillel Konaté profile dialog. Both development and production tabs report no captured console warnings or errors.

Actual browser observations are saved in `browser-evidence.json`; production lineups are visible in `production-lineups.jpg`.

## Automated results

| Run | Expected | Actual | Evidence |
| --- | --- | --- | --- |
| Initial build/regressions | Preserve existing contracts | Passed before final refinements | `regressions-first.log` |
| Final build/regressions | Successful production build; all existing tests pass | 27 Python + 53 Node tests passed; zero failures | `regressions-final.log` |
| Production HTTP E2E | Seven Next routes, unknown-route 404, real canonical seasons and archives, private-path isolation | Passed; two full seasons, six exact raw partitions, archived match and profile | `http-evidence.json`, `http-runtime.log` |
| Formatting | Prettier accepts final source | Passed | `format-check.log` |
| Final structure/data | No source HTML or obsolete dist; unchanged canonical data; clean diff whitespace; live preview | Passed; Next build present; frontend and API HTTP 200 | `final-checks.json` |

## Before and after

| Surface | Before | Desktop after | Mobile after |
| --- | --- | --- | --- |
| Filters | `01-filters-before.jpg` | `01-filters-after-desktop.jpg` | `01-filters-after-mobile.jpg` |
| Player | `02-player-before.jpg` | `02-player-after-desktop.jpg` | `02-player-after-mobile.jpg` |
| Match | `03-match-before.jpg` | `match-preview.jpg`, `03-match-after-desktop.jpg` | `03-match-after-mobile.jpg` |

Additional views: `match-statistics-desktop.jpg`, `match-shots-desktop.jpg`, `match-lineups-desktop.jpg`, `match-players-desktop.jpg`.

## Findings fixed during verification and limits

- Rapid filter edits could reuse a stale render snapshot and resurrect a removed search. Filter updates now start from the current URL; the rapid sequence passes.
- Escape initially returned focus to the document body. Dialog cleanup now restores the connected opener explicitly; the originating player button receives focus after closing.
- An old development-prefetched route needed reload after replacement. Early automation also matched two Explorer le match links and read tab state before a React update; scoping to the dialog and waiting for the selected state resolved those harness issues. One final screenshot wait used `.match-overview` instead of the actual `.match-overview-grid`; the DOM and screenshot confirmed the correct overview and the capture was saved afterward. An early text-locator wait after navigation timed out while the browser accessibility representation lacked text; DOM inspection and the rendered screenshot confirmed the real content.
- The source has distinct team xG and sums of recorded shot xG (Troyes 1.70 vs 2.50; Le Mans 0.28 vs 0.29). Both are preserved and their distinction is shown on the timeline. This pass does not repair provider data.
- CSV download was observed as an emitted download event; its downloaded bytes were not independently inspected. Existing CSV escaping remains in use.
- Keyboard and mobile checks are scoped evidence, not a claim of full WCAG or screen-reader certification. No live-provider refresh, deployment, commit or push was performed for this redesign.

Suggested commit: `feat: redesign filters, player profiles and match analysis`.
