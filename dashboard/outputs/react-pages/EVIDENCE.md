# Complete React multipage migration evidence

Setup: Bun1.4.4, Node.js for the retained regression runner, Python3 and tracked data/raw+data/sources. Install with `cd dashboard && bun install --frozen-lockfile`. Credentials are optional for local browsing. The existing local credential was checked against public outputs without exposing its value. No authenticated provider calls or public deployment were performed.

Exact rerun sequence from dashboard:

```sh
bun run test
bun run build:hosting
bun scripts/verify_application.mjs
python3 scripts/verify_rankings.py
bun run format:check
bun run dev
```

The optional rankings-source verifier uses the existing ignored SportsAPI key to check its absence from public assets. The application/HTTP verifier also works without an env file. To reproduce browser checks, open Vite5173 after bun run dev, or `PORT=8890 bun start` after the build, then follow browser-evidence.json.

Expected: seven real HTML/page entries, JSX components with React events/state, no HTML generator/parser/DOM controller, full direct navigation and reload, unchanged source data and preserved football workflows. Actual: all28 Python and56 Node checks passed (regression-final.log); the retained renderer fixtures now exercise actual JSX through React SSR. Native Bun and the actual generated hosting module both served all7 pages, plus404 for an unknown route; public assets, archive match/player responses and one compressed match table per season were verified (http-evidence.json). The original data tree has no changes relative to committed HEAD. Public asset credential scan and the47-edition rankings reconciliation passed. Formatting passed.

Browser: overview season2025/2026 → players and comparison/removal → clubs → Bayern direct URL/refresh and6 UEFA seasons →5–1 Köln match with22 starters →Manuel Neuer archived profile →detailed player metrics →FIFA2022 searchFrance →competition2024/2025 with2024 fixtures →complementary Ukrainian results →method page. All eleven recorded steps passed. Separate dev page verified UEFA selection, FIFA2022 and search. Both console captures have zero warnings/errors. Screenshot: react-multipage.jpg.

Initial failures are retained in node-first.log, node-second.log and http-first-packaged-failure.log. They exposed SVG title serialization, large-array spread limits, changed React attribute casing, stale test entry names and a duplicate gateway import in the actual hosting artifact. All were fixed. Browser verification also resolved fixture-query prototype preservation and historical season metadata selection. No old rendering implementation is retained to keep tests green.

Not exercised: mobile viewport, authenticated live provider requests, browser download of the full CSV and public deployment. CSV formatting and sanitization remain covered by existing regressions. Native document navigation reloads the page; the selected season and filters are retained in query parameters. The largest dataset cache retains only the current season.

After validation, all application dist directories are removed; build-cleanup.json records checksums and actual removal. Rebuilding regenerates these outputs. The dev command runs without dist.
