# Player top 30 placeholder and removal of national rankings

## Setup and rerun

Next.js 16.4.3, React 19.2 and Bun 1.4.4; local application on http://127.0.0.1:3000 with native Bun API on port 8765. Canonical JSON is unchanged.

From `dashboard`:

```sh
PATH="$HOME/.bun/bin:$PATH" ORION_EVIDENCE_DIR=outputs/player-ranking bun run test
PATH="$HOME/.bun/bin:$PATH" bun run format:check
```

Reconcile the saved browser observations from repository root:

```sh
python3 dashboard/outputs/player-ranking/verify_browser.py
```

## Final expected and actual behavior

- Navbar has seven text links including Classement joueurs. No gold icon appears in the navbar. The new page has exactly one small decorative Ballon d’Or SVG, beside its title.
- The ordered list contains exactly thirty rendered positions, numbered 01–30, each marked À venir. No player images, player links, scores, filters or fabricated player names are present.
- Enter on the actual navbar link opens the page and marks it active. Both desktop and 390px observations verify every row, heading/title, icon placement and absence of document overflow. The last-position screenshot shows the end of the list.
- Fresh ranking-page reloads request only the manifest through /data; no season partition or compressed season table is downloaded. The page uses the existing catalog-only provider mode.
- The standalone FIFA/UEFA national-ranking route and page component are deleted, along with their dedicated styles and navbar entry. `/classements` returns 404, recorded in removed-page.json. There are no remaining executable frontend/shared references to the removed route, RankingsPage, RankingTable or page-specific style classes.
- UEFA club history remains available through an independent ClubRanking component. The actual PSG profile renders six original season/rank/coefficient rows; inspect browser-evidence.json and club-uefa-local.jpg.
- The final production build and all existing 27 Python / 53 Node tests pass in regression-final-removal.log. Existing HTTP E2E verifies all nine registered routes, data/archive/API contracts and private-file isolation; http-evidence.json / http-runtime.log retain the results. Formatting passes in format-final-check.log.

## Browser procedure and evidence

Open Réglages locally, focus the Classement joueurs navbar link and press Enter. Wait for its heading, then inspect `.player-ranking-list > li`: value, displayed position, placeholder text, accessible name and rendered dimensions. Inspect `svg[data-icon="ballon-dor"]` inside h1 and confirm none in `.main-nav`. Scroll to the bottom to inspect position 30. Use a temporary 390×844 viewport for mobile, then reset it.

For loading behavior, enable the documented browser CDP Network domain, record the request-event cursor, reload the ranking page and retain only /data request URLs. No headers or request bodies are saved. Disable Network observation afterwards. Verify `/classements` returns 404 through HTTP. Visit the existing PSG profile and inspect `.club-ranking tbody tr` to ensure the extracted component still renders all six UEFA rows.

The scope changed during implementation: the user clarified that the trophy belongs only on the page, then requested full removal of the national-ranking page. Earlier observations are retained as historical observations rather than final assertions. The initial navigation capture preceded Next's transition completion; final assertions wait for the actual page heading.

An early browser verifier incorrectly required production telemetry scripts in the existing development session, where zero matching tags were observed. Its failure is retained in browser-verification.log and browser-first-failure.json. The final verifier checks production telemetry on HTTPS pages, rather than asserting production collection in local development. The application telemetry source was unchanged; production is checked separately after deployment.

The new page is a placeholder for the future algorithmic top 30. No ranking computation or player assignment is implemented or claimed.
