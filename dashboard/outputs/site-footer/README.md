# Shared footer and compact logo verification

Inputs, rerun commands, expected behavior and failure modes were recorded before implementation in `PLAN.md`. The build uses the actual Next/Bun app and canonical local football JSON, without provider credentials.

Actual results:

- Production build passed (`build.log`). An initial unsupported brand-icon import failed; it was replaced with the existing external-link icon and an explicit GitHub label. The first failure is retained in `build-first-failure.log`.
- Existing full application HTTP E2E passed (`application/http-evidence.json`, `application/http-runtime.log`): eight routes, two complete seasons, raw partitions, archive/profile endpoints and private-file isolation. The attempted run before a successful build is retained in `application/first-failure.json`.
- Browser E2E passed in dark/light at 1280×720 desktop and 390×844 mobile. A single footer landmark sits outside main. It uses the full official logo, four navigation groups on desktop, two link columns on mobile, and a separated copyright/license row.
- Actual footer navigation to Players, the existing 30-place ranking and home preserved the selected season and competition. External links point to real repository files and pages. Their destinations are recorded in `browser-evidence.json`.
- Navbar artwork is only the original 32×32 symbol (both themes), with a 44×44 home target. The mobile theme button's right edge is 370px in a 390px viewport. Document width is 390px, with no horizontal overflow.
- The selected theme applies to both logos and the footer; focus rings remain visible. Console errors: none. Original brand assets and football data were not changed.
- Seven screenshots are saved here. `header-dark-desktop.jpg` shows the compact navbar; `footer-light-desktop.jpg` and `footer-dark-desktop.jpg` show the reference-style footer; the remaining images show both mobile schemes.

The loading shell imports the same footer; deliberately stalled loading was reviewed but not simulated. No unit tests were added. Code commit: `6ff6f857`; the accompanying evidence commit has no application changes. Production verification follows the final Git push and checks the deployed SHA, footer and symbol assets on https://statarena-analytics.vercel.app.
