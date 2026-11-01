# Vercel Analytics and Speed Insights

## Setup and rerun

Next.js 16.4.3 / React 19.2 / Bun 1.4.4. The frontend workspace declares @vercel/speed-insights 2.0.0 and @vercel/analytics 2.0.1; dashboard/bun.lock preserves the resolved versions. The shared root layout remains a Server Component and renders the requested /next components outside the football data-loading boundary. Both SDK Next wrappers supply their own Suspense boundary.

Commands from `dashboard`:

```sh
PATH="$HOME/.bun/bin:$PATH" bun install --frozen-lockfile
PATH="$HOME/.bun/bin:$PATH" ORION_EVIDENCE_DIR=outputs/vercel-insights bun run test
PATH="$HOME/.bun/bin:$PATH" bun run format:check
PATH="$HOME/.bun/bin:$PATH" ORION_VERIFY_URL=https://orion-football-ranking.vercel.app ORION_CLOUD_EVIDENCE=outputs/vercel-insights/cloud-evidence.json bun scripts/verify_cloud.mjs
```

Reconcile the saved real-browser evidence from the repository root:

```sh
python3 dashboard/outputs/vercel-insights/verify_browser.py
```

## Expected and actual

- Frozen installation passes, with no lockfile change. Production build, all existing 27 Python / 53 Node tests and the real HTTP route/API/data E2E pass. See install.log, regression.log, http-evidence.json and http-runtime.log. Formatting passes in format.log.
- Integration commit `062539f52b9c9b767e04e0636c1f2f22ff546c79` automatically deployed from Git as `dpl_4NbB6HTsnRkstJ1YDqPjfdXU1QdX`, READY; connector receipt in deployment-integration.json.
- Public HTTP E2E passes all nine registered routes, the Bun runtime, six seasons, thirteen archive families, private-file isolation and the immutable canonical-data redirect. Inspect cloud-evidence.json / cloud.log.
- The real browser shows exactly one `@vercel/speed-insights/next` 2.0.0 script and one `@vercel/analytics/next` 2.0.1 script, including while football data is still loading. Both are deferred and use Vercel's generated same-origin collection paths.
- Overview → Matchs → footer Method navigation works, retaining the seven-link navigation and a single copy of each script. Speed Insights route attributes update from `/` to `/matchs` to `/methode`.
- Chrome DevTools network observations confirm both script GETs returned 200, a real Speed Insights `/vitals` POST returned 200, and three Analytics `/view` POSTs returned 200. No synthetic collector request was sent. No warning/error console messages were recorded.
- The independent saved-evidence verifier passes seven checks. browser-evidence.json includes timestamped DOM and filtered network records with request IDs for request/response correlation; no headers, cookies or request bodies are retained.
- The Vercel Speed Insights UI changed from onboarding/no events to five collected events. Web Analytics shows one visitor and four page views, with `/`, `/matchs` and `/methode` represented. Dashboard text and screenshots retain the observed state. No paid upgrade or Vercel configuration change was performed.

## Browser capture procedure

In cua_repl, create a fresh background browser tab at `https://orion-football-ranking.vercel.app/?season=2026%2F2027&focus=europe`. Get its documented `cdp` capability, send `Network.enable`, and call `readEvents` to capture the starting cursor. Reload normally. Inspect `script[data-sdkn]` in the DOM; record src, data-sdkn, data-sdkv, data-route and defer. Use the visible Matchs link, then the footer Données & méthode link, reading state after each action. Repeat script inspection to check uniqueness and route updates.

Read Network.requestWillBeSent and Network.responseReceived events from the saved cursor, paging while hasMore is true. Keep only the observed script-prefix paths and retain URL/method/status/requestId. Capture warning/error console entries, then send `Network.disable`. `verify_browser.py` correlates the stored request IDs and asserts real 200 script and telemetry responses. Inspect the project Analytics/Speed Insights UI to confirm ingestion separately.

## Limits and failed inspection attempts

An initial connector Analytics-count request failed because its schema marks `until` optional while the endpoint requires it. Correcting that input returned “Web Analytics not found” before the SDK deployment/first events. Those responses were not treated as passing collection checks; the subsequent real browser 200 POSTs and Vercel UI ingestion provide the runtime evidence. No claim is made that the legacy count API was repaired or successfully queried.

Observed metrics reflect a small verification session, not a representative performance benchmark. No additional browser/unit test suite or application behavior was introduced.

Official integration references: [Speed Insights](https://vercel.com/docs/speed-insights/quickstart) and [Web Analytics](https://vercel.com/docs/analytics/quickstart).

## Commits

- `29fd1f64` — feat: add Vercel Speed Insights: frontend dependency, Bun lockfile, root-layout component.
- `062539f5` — feat: add Vercel Web Analytics: frontend dependency, lockfile and companion root-layout component.
- `docs: record Vercel insights verification` — build/HTTP/browser evidence and final worklog. This changes no application source; the final Git deployment is checked separately, with its receipt kept in ignored outputs/daily-refresh to avoid recursively committing deployment receipts.
