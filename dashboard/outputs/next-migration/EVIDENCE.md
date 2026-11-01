# Next.js + Bun acceptance — 1 November 2026

## Implementation

The real Next.js16.4.3 App Router application lives in `dashboard/frontend/app/`, with seven `page.jsx` routes, a server layout and metadata, client provider, loading/error/404 states, and Next links. URL state uses Next's search parameter hook and supported History integration. No manual HTML entries, Vite dependency, static hosting Worker or HTML packaging generator remain in the active application.

Bun.serve remains the data backend. Next transport handlers stream API/data responses to the server-only local origin. Canonical JSON data remains in root `data/`. Archived fixtures, identities, thirteen match families, ranking history, zeros and missing values retain their contracts. The UI uses one shared neutral token stylesheet inspired by https://nextjs.org/showcase, with restrained green for observed data.

## Exact rerun

Setup: macOS, Bun1.4.4, existing canonical data, no live provider key needed. From the repository root:

```sh
cd dashboard
export PATH="/Users/lemonnierhugo/.bun/bin:$PATH"
bun install --frozen-lockfile
bun run test > outputs/next-migration/regressions-final.log 2>&1
bun run format:check > outputs/next-migration/format-check.log 2>&1
# test builds production Next and invokes the HTTP E2E; standalone rerun:
bun run verify
# Start user preview:
bun run dev
```

Preview:http://127.0.0.1:3000. Bun health:http://127.0.0.1:8765/api/health. `bun start` runs Next production plus Bun after `bun run build`.

## Expected and actual

- Expected: actual Next production routes, unknown-page404, proxied real JSON/archive records, private-path isolation, no credentials in public assets. Actual: passed; `http-evidence.json` and `http-runtime.log` record all seven routes, complete2026/2027 and2025/2026 datasets, byte equality for a match partition in each of six seasons, a real match observation and player profile, health, private paths and a scan against local secret values. Test servers run on ephemeral ports and terminate afterward.
- Existing regressions:27 Python and53 JavaScript passed, including the production HTTP E2E. No new unit tests written. Static-package and Worker-only tests retired alongside their implementations; the two static frontend server checks were replaced with API-only boundary checks and the real Next HTTP E2E.
- Formatting passed. Final source/structure checks passed; no data changes. `final-checks.json` records package version, source hashes, seven route files, zero authored HTML entries and absent dist. Next's ignored `.next` production build and `.next-dev` development cache are standard framework artifacts, retained for local operation.

## Browser rerun and results

Open http://127.0.0.1:3000/.

1. Navigate to Joueurs, select Aaron Collins and Tobias Heintz, open Comparer. Verify79/84minutes,9.88notes, observed zero and missing metrics. Close and navigate to Clubs. The same comparison tray persists across navigation, verifying the shared Next layout state.
2. Change season to2025/2026. Verify690clubs and URLseason. SearchBayern and open its48-match card. Reload and verify the same detail, season and UEFA history.
3. Open Bayern–Köln16May2026. Verify5–1,22plotted starters and archived Manuel Neuer profile. Browser Back from rankings restores the match/season. Mobile390×844 has document width390.
4. Classements: choose FIFA2022-02-10, searchFrance. Verify rank3,1786.150points and previous rank3. All four columns and controls fit390px.
5. Compétitions: searchBundesliga, filterGER, open Bundesliga. Select2024/2025. Verify first fixture23August2024Mönchengladbach2–3Leverkusen. Switch2025/2026 and verify22August2025Bayern6–0Leipzig, then switch back2024/2025 and verify correct original fixture. Method remains available.
6. Return overview, select2025/2026. Verify393593filtered appearances,12742matches,44competitions and328056shots. Inspect desktop/full-mobile screenshots; no document overflow at390px. Reset viewport and leave preview open.

`browser-evidence.json` retains actual states and steps; no captured browser console warnings/errors. Screenshots include overview desktop/mobile, comparison, club catalog, match/profile, competition history and FIFA ranking. `preview.jpg` is the final user-facing view.

## Failures retained and resolved

- `build-first.log`: Next correctly detected the old `src/pages` component folder as a second router. Renamed it `src/views`; only App Router remains.
- `metadata-regression.log` and `http-metadata-failure.json`: the root page overrode the root layout's title; set its explicit Orion title and reran the unchanged HTTP identity assertion. Final production suite passes.
- `competition-cache-failure.jpg`: an empty fixture result persisted across season/client transitions. Scoped the fixture resource cache to the active data client; clean loading and2024→2025→2024 passed in the browser.
- A browser performance probe was unavailable; persistent selection state supplied observable navigation evidence instead.

Live authenticated provider calls, public deployment, full CSV browser downloads and an exhaustive assistive technology audit were not repeated. Existing provider/CSV/escaping/null contracts passed. The public hosting target is not deployed or modified.
