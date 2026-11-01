# Unified Matchs: E2E verification

## Reproduce

From `dashboard`, start the existing local Next.js/Bun application with `PATH="$HOME/.bun/bin:$PATH" bun run dev`. The browser observations use port 3000 and the Bun API on 8765; canonical data was not changed.

- Production build and existing regressions: `PATH="$HOME/.bun/bin:$PATH" ORION_EVIDENCE_DIR=outputs/matches-unified bun run test`.
- Formatting: `PATH="$HOME/.bun/bin:$PATH" bun run format:check`.
- Saved browser observations versus canonical JSON, from repository root: `python3 dashboard/outputs/matches-unified/verify_browser.py`.

`regression-final.log` passes the production build, 27 Python and 53 Node tests. The existing HTTP E2E includes the registered Next routes, Bun data/API/archive boundary and private-file checks; inspect `http-evidence.json` / `http-runtime.log`. `format-check.log` passes. No new isolated tests were written after implementation.

## Expected and observed

- Topbar has exactly seven links: Vue d’ensemble, Compétitions, Clubs, Joueurs, Matchs, Classements, Réglages. Calendar and Method do not appear there. Method works from the footer.
- Overview upcoming link enters Matchs/À venir. Matchs without a tab defaults to À venir; the selected view is marked with `aria-current` and visually underlined.
- Mode navigation sits above filters. À venir omits playing-time controls and performance CSV export; Résultats restores them and shows thirty collected results per page.
- Next-week upcoming selection retains all 127 Europe fixtures on four pages (40/40/40/7), without duplicates or chronological omissions, verified independently from canonical fixture tables and Python Europe/Paris conversions.
- Enter activates the Résultats link. The real Union Berlin–1. FC Köln 1–1 fixture opens its existing analysis; the Statistiques tab remains selected with `view=stats` while the list mode remains `tab=results`.
- Results → detail → results preserves the selected November 2 week. Switching back to À venir returns to that week.
- Old `/calendrier?season=2026%2F2027&focus=europe&week=2026-11-02&league=l_0bfbkO&q=paris` resolves to Matchs/À venir, keeping every filter. Villarreal–Paris Saint-Germain → detail → return keeps that same week, search and competition.
- Method footer link opens the actual method page. Header Matchs returns to the default upcoming view; reset restores four current-week games at capture time.
- At 390×844, document width and scroll width both equal 390; both mode links remain visible and functional. Viewport override reset after testing.

Inspect `browser-evidence.json`, `oracle-results.json` and adjacent desktop/mobile screenshots. Fixtures are compared against source-table hashes; all four pages are reconciled as one set. Header, view state, relevant controls and detail return URLs are also asserted.

## Notes and limits

The existing calendar selector and 30-second client refresh are unchanged; earlier edge-case evidence (unknown time, year boundary, daylight saving) is retained in `outputs/upcoming-week`. This refinement does not repeat synthetic-data or simulated-clock tests.

An initial browser observation during hot reload retained result links from before the week-preservation adjustment. That observation is marked as superseded in the evidence. Reloading the final implementation confirmed the week in both fixture link and result breadcrumb; the final production build/regressions also passed.

The legacy HTTP request may return 200 with Next's streaming redirect, rather than an HTTP Location header, because redirect occurs during rendering. `legacy-http.json` records the actual response; the browser verified the final `/matchs` URL and preserved query values. Do not describe that HTTP observation as a 307.

Production verification will be appended after the Git-triggered release is ready.
