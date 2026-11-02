# Interface cleanup verification contract

Final scope: the user cancelled the sidebar/topbar experiment. Retain existing horizontal navigation, four filter controls and the focus button. Remove the provider configuration status and filter-footer appearance/match count. Reduce horizontal margins across header, main and footer to 24px desktop and 12px mobile, with no maximum content width. Preserve data, routes, themes and logo.

Expected / failure modes before final implementation:
- No sidebar, drawer, global season selector or extra shell components remain.
- Header has existing six page links and the moon/sun. No PitchAPI configuration/collection status.
- Filter footer has no appearance/match tally. Focus toggle, filter chips, reset and all four controls still work.
- Header/main/footer align at 24px on desktop, 12px on mobile, with no document horizontal overflow. Mobile navigation stays horizontally scrollable.
- Both themes, navigation, league filtering and player/match details remain functional with actual data.
- Existing production HTTP E2E passes, including all eight routes, data/archive access and file isolation.

Setup: canonical local JSON and installed Bun/Next dependencies; no provider key needed.

```sh
cd dashboard
PATH=/Users/lemonnierhugo/.bun/bin:$PATH bun run build
PATH=/Users/lemonnierhugo/.bun/bin:$PATH ORION_EVIDENCE_DIR=outputs/interface-cleanup/application bun run verify
PATH=/Users/lemonnierhugo/.bun/bin:$PATH PORT=3015 API_PORT=8775 bun start
```

Browser: http://127.0.0.1:3015/?season=2026%2F2027&focus=europe. Check 1502x1031 light/dark, 1920px, 860px and 390x844; save screenshots, measured geometry and interaction results. The cancelled experiment and its earlier E2E artifacts were moved outside the repository to /tmp/statarena-sidebar-cancelled-20261102, and are not evidence for this final revision.

Actual: pending final build and E2E.
