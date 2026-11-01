# Vercel, Settings and daily season refresh

Date: 2026-11-01. Live site: [Orion](https://orion-football-ranking.vercel.app). Implementation and configuration: [DEPLOYMENT.md](../../../docs/DEPLOYMENT.md). Acceptance was written before the worker implementation in `ACCEPTANCE.md`; no new unit tests were added.

## Delivered configuration

- Vercel project `prj_DhaqrVkH3Gi4uysT7IRsm9fB2bjR`, Hugo team `team_IYt7KqupdSTtMuQuMvNa9wiJ`.
- Connected repository `OrionQuantPlatform/Football_Ranking`, production branch `main`. Root `dashboard/frontend`, Next.js, Bun 1.4.x, Paris region `cdg1`. Frozen install from the parent Bun workspace. Source files outside the root enabled; skipping builds for changes outside the frontend disabled.
- Production domain is public; preview authentication remains enabled. The provider key is a GitHub Actions secret and a Vercel **Production Secret**. No key value belongs in these artifacts. The connector refused environment creation (403), and CLI credentials had expired; authenticated browser configuration succeeded after the user signed in.
- GitHub Actions schedule `0 0 * * *`, timezone `Europe/Paris`; DST-aware, plus manual dispatch. This is a scheduled start, not a guarantee to the second; GitHub can delay queued runs. No DB or paid resource was provisioned.
- Cloud data reads are pinned to the deployment commit. Redirects are `no-store`, and frontend data URLs include the public build revision. Raw JSON/gzip data stays in GitHub, not in a Function bundle. Local development retains the native Bun server.

## Exact rerun commands

Prerequisites: the checked-out canonical data; Bun 1.4.4, Python 3, Node for existing regressions. Server credentials are needed only for the real provider/worker, never for the fixture worker E2E.

```sh
cd "/Users/lemonnierhugo/Desktop/Coding Project/Football_ranking/dashboard"
bun scripts/verify_daily_refresh.mjs
ORION_EVIDENCE_DIR=outputs/vercel-daily bun run test
bun run format:check
ORION_VERIFY_URL=https://orion-football-ranking.vercel.app bun scripts/verify_cloud.mjs
```

The complete production test runs a Next production build, the existing 27 Python and 53 Node checks, and Next → native Bun → canonical data HTTP E2E on ephemeral ports. Actual shell runs used `/Users/lemonnierhugo/.bun/bin/bun` and added that directory to PATH. `regressions-published-data.log` additionally set `VERCEL_GIT_COMMIT_SHA=36a8151b42de017fc90433fe0f135d3cc26acff5` to exercise compiled revision URLs against the refreshed data.

Cloud-mode local browser setup was a built Next server on port 3001 with `ORION_EMBEDDED_API=1`, `ORION_REMOTE_DATA=1`, `ORION_DATA_REVISION=36a8151b42de017fc90433fe0f135d3cc26acff5`; the normal local app remains on ports 3000/8765. Temporary production test servers are stopped after verification.

To reproduce the real worker (performs collection and a data commit):

```sh
gh workflow run daily-data.yml --repo OrionQuantPlatform/Football_Ranking --ref main
gh run view 41328922932 --repo OrionQuantPlatform/Football_Ranking --log
```

The second command reads this run's immutable historical logs. A new dispatch receives a new run ID. Credential values must stay in the configured secrets.

## Expected and actual outcomes

| Workflow | Expected | Actual / proof |
| --- | --- | --- |
| Fixture worker process + local HTTP provider + temporary JSON | Import 13 families, normalize rows/nulls, preserve history, deduplicate reruns, retry 429, fail 401 before publishing | Passed, 42 fixture requests; `worker-evidence.json`, `worker-runtime.log` |
| Existing regressions against refreshed data | Build and all 80 existing checks pass | Passed; `regressions-published-data.log`, `http-evidence.json`, `http-runtime.log` |
| Cloud transport | Eight real routes, Bun runtime, six seasons, 13 archived families, player profile, safe private paths, noncached redirect to a full Git SHA | Passed; `cloud-http.json`, `live-http.json` |
| Real provider through deployed gateway | The server secret actually authenticates without exposing it | HTTP 200, 77 leagues; `provider-live.json` |
| Function tracing | No canonical data or secret files included | 118 traced files, 1,701,350 bytes; zero data/env files. Public revision string present in compiled JS; `function-footprint.json` |
| Formatting and whitespace | Clean source | Passed; `format-check.log`, final `git diff --check` |

## Real daily worker → GitHub → Vercel proof

[Run 41328922932](https://github.com/OrionQuantPlatform/Football_Ranking/actions/runs/41328922932) completed successfully from source commit `96ec74c3eda75a8f7ea26288259ef4e7102f2728`. It collected **44 ongoing European competition-seasons**, updated **238 matches**, **89 upcoming fixture details** and **48 profiles**, using **3,454 requests** with no retries. The current season increased from 4,339 to **4,394 matches**.

Validation passed across **6 seasons, 189 partitions, 46,475 matches and 1,038,004 appearance records**. Checksums, references and unique IDs were checked before pushing. The comparison below returned zero: every file under older season folders was unchanged.

```sh
git diff --quiet 96ec74c3..36a8151b -- ':(glob)data/raw/seasons/202[1-5]-*/**'
```

The bot pushed data commit `36a8151b42de017fc90433fe0f135d3cc26acff5`; Vercel automatically created `dpl_6VgThCK6qtD4pX3He4kXZKhQa2jd`, production **READY**, without a manual deployment or deploy hook. Source push `adf70d110fcafa38de78674ccbaab25312fc33cd` likewise automatically created READY deployment `dpl_qwf8hiFnZsBsmANub93Abjho4Ngk` (`source: git`). `deployment-code.json`, `github-worker.json`, `github-worker.log`, `live-http-data-revision.json` and tracked `data/raw/sync.json` provide readbacks.

## Browser procedures and observations

The Codex in-app browser exercised the local cloud-mode production build and the public domain. Default desktop widths were 1280px/1502px; responsive checks used 390×844. The temporary viewport override was reset.

1. Open Settings; enable Top 7 Europe + UEFA, choose default season 2025/2026, reload, then enter `/reglages` without a query. Actual: saved preference and default season apply. Restore default season to the ongoing season.
2. Navigate to the overview. Actual: exactly ten selectable competitions (seven first divisions plus Champions/Europa/Conference League), 745 matches in the initial pre-refresh snapshot. The competition directory also shows exactly ten cards. Turn focus off, select LaLiga2, then turn focus on: the excluded league is removed from the URL and selection. Focus is preserved across links/reload.
3. At 390px, inspect filters and Settings. Actual document width stays 390px; controls and the schedule remain operable. See `focus-mobile.jpg`, `settings-mobile.jpg` and `browser-evidence.json`.
4. Public Settings shows the configured provider, 00:00 Paris, successful collection at 18:04 local, 238 updated matches, and the deployed revision. See `settings-live.jpg`, `live-settings.json`, and final browser evidence.
5. Keyboard verification found that changing focus reloaded a catalog-only resource and returned focus to BODY. The final fix reuses that catalog resource. Production-build Space and Enter checks now leave focus on the button with the correct false/true pressed state; `settings-keyboard.json` records the before/after.

Other screenshots: `settings-desktop.jpg`, `focus-desktop.jpg`, `vercel-build-settings.jpg`, `vercel-git-connected.jpg`, `vercel-secret-configured.jpg`. Saved secret screenshots show its name/type/environment only. Browser checks are scoped evidence, not full WCAG or screen-reader certification.

## Earlier failures and corrections

The pre-implementation run failed because the worker did not exist (`worker-before.log`). The first worker fixture had the wrong player envelope; correcting it preserved the original expected rows. The publisher then exposed a string/bytes mismatch in bundle credential checking; the key is now passed as bytes. Both failures are retained in first/second run logs. The first Next build rejected tracing globs outside the inferred root; setting the repository tracing/Turbopack root fixed it. A legacy filesystem tracing warning was removed with a targeted local-only tracing annotation. No data was published by failed runs.

An initial manual HTTP probe accidentally overwrote its numeric HTTP status with the health payload's `status: ok`; the durable E2E script keeps `httpStatus` separate and passed. GitHub's completed real run logs a Node 20 action deprecation warning (the platform ran those pinned actions on Node 24); the worker and data validation still passed. Future scheduled starts and external provider availability are not claimed as observed.

## Final live readback

Commit `adb9ee79a28828b13d5aba97d68374e45af8135b` automatically deployed as `dpl_TLxNXfsrdgX2yci1ywCF32xFqHZK`, production READY. `deployment-final-code.json` and `live-http.json` record the exact revision, actual Bun runtime, configured key, noncached GitHub redirect and complete route/archive/profile pass.

The public-browser rerun confirmed Space/Enter both leave focus on the Settings button. The focused date calendar for 2026-10-31 rendered 29 fixture links, all within the ten allowed competitions; date selection required native keyboard commit after the generic fill had not committed the native date control. Final mobile width was 390px with document width 375px (no overflow). The overview shows ten competitions, 755 matches and 23,595 played appearances after the real refresh. Captured browser warnings/errors: none. See `browser-final.json`, `overview-live.jpg`, `settings-live.jpg`, and `settings-live-mobile.jpg`.

The final evidence-only publication can create another automatic Git deployment. Its terminal readback is saved locally under ignored `dashboard/outputs/daily-refresh/` so recording that deployment does not create a recursive series of evidence commits.
