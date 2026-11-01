# React/Bun migration evidence

Setup: Bun1.4.4, Node.js for the retained regression runner, Python3, dependencies installed with `cd dashboard && bun install --frozen-lockfile`, existing tracked `data/raw` and `data/sources`. No provider calls or public deployment required.

Reproduce automated checks from `dashboard/`:

```sh
bun run test
bun run build:hosting
bun scripts/verify_application.mjs
bun run format:check
bun run dev
```

Expected: compiled React application, native Bun server, existing season/archive/API contracts and data isolation remain valid. Actual:28 Python and56 Node checks passed (`regression-final.log`), build and hosting package succeeded (`hosting-build-final.log`), real HTTP/data/archive/credential checks passed (`http-evidence.json`), formatting passed (`format-check.log`). One table per season was compared byte-for-byte over HTTP and Git reports no changes under data.

The dev command starts Bun8765 and Vite5173 together; HTML, transformed React entry, health and JSON proxy checks passed (`dev-evidence.json`). Browser rerun: follow the explicit actions and outcomes in `browser-evidence.json`; screenshot `react-bun.png`. Production browser tested season2025/2026, FIFA2022 France search, Bayern UEFA history, match6–0 and Harry Kane profile, player comparison and removal, and remaining navigation.

Initial failures are retained in earlier test logs, `dev.log` and `browser-evidence.json.priorFailures`. They included moved fixture paths, React SVG property spelling, void input children, selected-option handling and a Vite/React-plugin major-version mismatch. These were corrected; the dependency lock now records compatible versions. Final browser diagnostics are recorded separately from historical failures.

Not verified: mobile viewport, authenticated live provider requests or public deployment. Existing analytical view builders remain template-based, with their escaped markup converted into elements inside one React tree; their controller is mounted/unmounted through a React effect with listener cleanup.
