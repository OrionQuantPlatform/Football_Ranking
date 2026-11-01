# STATARENA verification

Setup: supplied brand kit, actual production Next.js/Bun app and canonical JSON football data; no provider credentials are needed by the branding checks. Original assets are preserved byte-for-byte in the paths recorded by `asset-inventory.json`.

Rerun from `dashboard/`:

```sh
PATH=/Users/lemonnierhugo/.bun/bin:$PATH bun run build
ORION_EVIDENCE_DIR=outputs/statarena-brand/application bun run verify
PORT=3012 API_PORT=8772 bun start
# In another terminal:
ORION_VERIFY_URL=http://127.0.0.1:3012 node scripts/verify_brand.mjs
ORION_VERIFY_URL=https://statarena-analytics.vercel.app node scripts/verify_brand.mjs
ORION_VERIFY_URL=https://statarena-analytics.vercel.app ORION_CLOUD_EVIDENCE=outputs/statarena-brand/production-cloud.json bun scripts/verify_cloud.mjs
```

Expected: STATARENA metadata, exact supplied logos/favicon/share image, a 404 for the removed settings route, three retained seasons and working Bun archive/profile endpoints. Browser steps and edge cases are in `theme-plan.md`.

Actual results:

- Build passed. Existing checks: 27 Python and 55 Node checks passed; see their logs. No new unit tests were added.
- Local application E2E passed: eight routes, two complete seasons, raw partitions, archives/profiles and private-file isolation. See `application/http-evidence.json` and `application/http-runtime.log`.
- Local and public branding checks passed; see `http-local.json` and `http-evidence.json`.
- Public cloud checks passed: eight routes, three seasons, all thirteen archived match families, stored profile, Bun runtime and immutable data URLs pointing at `OrionQuantPlatform/STATARENA`. See `production-cloud.json`.
- Desktop 1502×1031 and mobile 390×844 were inspected in both modes. Background/foreground match the user's reference exactly; mobile document width was 390 pixels. Theme choice survives reload, the logo changes variant, the rightmost control remains reachable and Settings has no navigation entry. See `browser-evidence.json` and the named JPGs.
- The supplied GitHub social preview was uploaded and observed in repository settings. The repository and Vercel project were renamed; production domain is `statarena-analytics.vercel.app`. Existing raw-data URLs under the former repo name also returned 200 without a redirect.
- Production browser verification on the new public domain confirmed real data, exact dark colors, light-mode persistence, and no console errors. Captures: `production-dark.jpg`, `production-light.jpg`.
- `deployment.json` records the READY Git deployment for source commit `25f403c8`. This final evidence commit changes no application code or football data.

Failures retained: `http-before.json` is the expected pre-implementation failure; `http-title-failure.json` records the root-route title defect detected and fixed during verification. A temporary mistaken negative-brand assertion was corrected before the passing run. A viewport initially applied to another selected tab was corrected; actual mobile images were recaptured and their 390×844 dimensions verified. Local-storage denial was reviewed in code but not simulated.
