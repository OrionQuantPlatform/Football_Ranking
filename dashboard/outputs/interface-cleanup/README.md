# Interface cleanup E2E evidence

Result: passed on the final production build. The sidebar experiment was cancelled and removed before this run. Source scope is the two requested removals plus compact, aligned gutters in the original layout.

## Setup and exact rerun

Canonical local JSON, installed Bun/Next dependencies, no provider key required. Run from the repository root:

```sh
cd dashboard
PATH=/Users/lemonnierhugo/.bun/bin:$PATH bun run build
PATH=/Users/lemonnierhugo/.bun/bin:$PATH ORION_EVIDENCE_DIR=outputs/interface-cleanup/application bun run verify
PATH=/Users/lemonnierhugo/.bun/bin:$PATH PORT=3015 API_PORT=8775 bun start
```

Browser input: http://127.0.0.1:3015/?season=2026%2F2027&focus=europe. Resize to the sizes below using the in-app browser viewport capability. Compare the screenshots and DOM geometry in browser-evidence.json. Desktop before/after captures both use 1502x1031 in light mode. The before capture was made before the cancelled experiment; it contains the original 131px margins, provider status and tally.

## Expected and observed

| Check | Actual |
|---|---|
| Existing navbar, no sidebar/drawer | Six original page links, logo and moon/sun; zero sidebar/drawer nodes |
| Removed labels | No provider status in header; filter footer only has focus button when no filters apply; zero filter-result-count nodes |
| 1502x1031, light and dark | Header/main/footer all have 24px gutters; main usable width 1454px vs 1240px before |
| 1920x1080 and 860x1031 | All three surfaces retain 24px gutters; document width equals viewport |
| 390x844, dark and light | 12px gutters; 366px usable width; horizontal scrolling contained in navbar, not document |
| League filtering | Ligue 1 URL and chip, reset action retained |
| Focus toggle | 46 total options after async all-competition reload, 11 with Europe focus (includes the all option); focus URL preserved |
| Player detail | Achraf Hakimi dialog opens with real minutes, goals, assists, xG/xA and detailed sections; closes normally |
| Match detail | Featured Ligue 1 match opens and renders Les chiffres du match |
| Navigation | Competitions loads actual league cards; mobile Matchs opens current-week fixtures |
| Browser errors | No error-level console entries observed in local run |
| Application HTTP E2E | Eight Next routes, unknown-route 404, Bun health, full 2026/2027 and 2025/2026 data loads, partitions and archive/profile access passed |

For interaction reruns: select Ligue 1 in Compétition; turn Top 7 Europe + UEFA off, wait for filter panel to return and inspect options, then restore it; open the first observed performance and close it; use Explorer le match; follow navbar Compétitions then Vue d’ensemble and Réinitialiser; switch themes; at 390px follow navbar Matchs. This uses the existing controls rather than a replacement menu.

The initial all-competition snapshot briefly saw zero options during async loading. It was recorded as intermediate and then rechecked after load, yielding 46. No application test failed. Earlier sidebar experiments and their evidence live outside the repository in /tmp/statarena-sidebar-cancelled-20261102 and are not used to claim this revision passed.

Artifacts: PLAN.md defines outcomes before final edits; build.log; application/http-evidence.json and http-runtime.log; browser-evidence.json; before-desktop.jpg/json; desktop-light.jpg, desktop-dark.jpg, mobile-light.jpg, mobile-dark.jpg. Production release readback is recorded separately after Git deployment.

Suggested source commit: `ui: widen dashboard with consistent compact gutters`.

## Production release

- URL: https://statarena-analytics.vercel.app/?season=2026%2F2027&focus=europe
- Target/status: production / READY, Next.js, source Git main 7ff82a2f24aa68130a029fe856a4938decd97838.
- Vercel project: statarena (prj_DhaqrVkH3Gi4uysT7IRsm9fB2bjR); deployment dpl_For8yXhoy6XCDhu9UVnQ82yCmhgY.
- Post-deploy browser input: canonical URL above, 1502x1031 light. Existing six links, actual weekly fixtures, three select controls plus search, 24px aligned gutters, zero sidebar nodes and zero removed-tally nodes verified.
- Inspect production-browser.json and production-desktop.jpg; the alias orion-football-ranking.vercel.app is assigned to the same deployment.
- No production runtime-log scan or new monitoring configuration was performed; local browser error console was checked separately.
- This final receipt commit changes only worklog/evidence. Its application source is identical to the verified Git release; the normal Git integration may trigger a further build.
