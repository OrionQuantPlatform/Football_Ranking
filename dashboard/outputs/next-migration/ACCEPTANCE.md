# Next.js + Bun migration acceptance

Replace Vite/manual HTML entry documents and static hosting generator with Next.js App Router routes. Keep native Bun.serve for archive/provider API and canonical JSON files. Next rewrites /api and /data to Bun. No data changes, secrets in browser, old HTML wrappers or legacy static export pipeline. Preserve seven sections, direct entity URLs, seasons, filters, comparisons, exports, thirteen match detail families and safe missing values.

Design: Next.js Showcase-inspired neutral surfaces, precise grid, thin borders, restrained type, minimal decorative copy; retain Orion identity and football visualizations. Responsive and accessible labeled controls.

Expected E2E: built Next server + Bun API start together, / and six named pages respond with Next runtime, unknown route404, raw JSON and archives return real records, sensitive paths remain inaccessible, provider unconfigured fallback works. Browser navigation uses Next links without full-document reload; season/search/back/refresh retain URL state; rankings need no whole-season performance download. Search/player dialog/comparison/match/club/FIFA histories still work. Desktop/mobile screenshots and console logs retained.

Before implementation: adapt existing HTTP/bootstrap E2E to the new API-only backend and real Next frontend. Remove only obsolete static-hosting fixture tests with their retired implementation. Retain data and provider contract regressions. Record exact commands, failures, reruns and generated-build cleanup.
