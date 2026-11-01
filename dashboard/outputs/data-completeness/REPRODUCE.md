# Match/player completeness and dark dropdown verification

## Setup and exact commands

- Repository: Football_Ranking, Next.js 16.4.3, Bun 1.4.4, canonical JSON under data/raw. No new provider collection or database migration.
- Start the real frontend/Bun backend from dashboard with `bun run dev` (ports 3000/8765). No API key is needed to read the archived fixtures used below.
- From the repository root: `python3 dashboard/outputs/data-completeness/verify_sources.py`.
- From dashboard, with Bun on PATH: `ORION_EVIDENCE_DIR=outputs/data-completeness bun run test` and `ORION_EVIDENCE_DIR=outputs/data-completeness bun run verify`.
- Cloud HTTP: from dashboard, `ORION_VERIFY_URL=https://orion-football-ranking.vercel.app ORION_CLOUD_EVIDENCE=outputs/data-completeness/cloud-evidence.json bun scripts/verify_cloud.mjs`.

The Python verifier independently reconstructs records from the canonical observation shards and compares them with actual HTTP responses and saved JSON extracted from the rendered browser. It does not import frontend transformations. `source-inventory.json` lists source hashes, periods, counts and results. The global inventory covers the family names in all 2,655 observation shards; the deep browser comparison covers the fixtures below, rather than claiming every match was manually opened.

## Browser rerun

Use the Codex in-app browser through cua_repl, after its required initialization/documentation call. Keep the default desktop viewport. Replace BASE below with the local or public site. Run each phase separately so UI/network waits remain bounded; take a fresh AX state after actions. Save screenshots and JSON in this directory. These are real HTTP/browser workflows, not component mocks.

```js
var BASE = 'http://127.0.0.1:3000';
var out = '/Users/lemonnierhugo/Desktop/Coding Project/Football_ranking/dashboard/outputs/data-completeness';
var fs = await import('node:fs/promises');
var tab = await cua.createBrowserTab('2', BASE + '/?season=2026%2F2027&league=l_3FJFUl&focus=europe', {visible:false});
```

Open #league-filter, #season-filter and #minutes-filter separately, observe AX state, save a screenshot with each menu open, then Escape. Expected: dark picker/options, readable pale text, visible selected item, no clipping. Open minutes, Down, Return: the control selects 30 minutes et plus and URL gains minutes=30. Escape must dismiss without changing the selection. At width 390 repeat the open minutes picker and player statistics; document width must stay 390. Reset the viewport afterwards. Native fallback colors are defined, but Safari/Firefox were not executed in this run.

Match statistics: navigate to `/matchs?season=2026%2F2027&focus=europe&id=m_49qvGz&view=stats`. Select All, FirstHalf and SecondHalf through #team-stats-period. Expected and observed: seven source groups and 43 metric rows per period, including repeated Top stats entries in their original group context. Store `.comparison-stat` labels/home/away values in browser-statistics.json under team.

Capture all match families through the visible source UI:

```js
await tab.playwright.getByRole('tab',{name:'Données complètes',exact:true}).click();
await tab.getAXState({emit:false});
await tab.playwright.getByRole('button',{name:'Données sources',exact:true}).click();
await tab.getAXState({emit:false});
var payloads = {};
var sections = await tab.playwright.locator('#match-data-section').evaluate(s => [...s.options].map(o => o.value));
for (var section of sections) {
  await tab.playwright.locator('#match-data-section').selectOption(section);
  await tab.getAXState({emit:false});
  await tab.playwright.getByRole('button',{name:'JSON',exact:true}).click();
  await tab.getAXState({emit:false});
  payloads[section] = JSON.parse(await tab.playwright.locator('[data-source-json]').textContent({timeoutMs:15000}));
}
await fs.writeFile(out+'/browser-match-json.json',JSON.stringify(payloads,null,2));
```

Expected and observed: thirteen original families plus Archive complète; all parsed JSON equals canonical source data, including precision, null, zero, false, empty arrays, unknown fields, statuses and observation metadata. See browser-match-json.json and source-inventory.json.

Player: select the Joueurs match tab, click Achraf Hakimi, then the Statistiques button in his dialog. Select All, FirstHalf, SecondHalf with #player-stat-period. Save each `[data-metric-key]` key/label/dd value under player in browser-statistics.json. Expected and observed: four full-match groups/38 rows (without deduplication), 23 rows per half. The group/key sequences match the canonical source. The fractional display remains in French; exact values remain in JSON.

Click the dialog’s Données complètes button. Repeat the capture loop using #player-data-source and `dialog [data-source-json]`; save browser-player-json.json. Expected and observed: ten source categories. Compare every selected original player record, period, advanced object, shot, heatmap, event, lineup membership, team pass network, profile observation and normalized performance with canonical files. The pass network intentionally keeps the full team context. All comparisons pass.

Pagination: Match → Données complètes → Cartes d’activité → Données sources → Explorer. Expand Cells under the second team, Paris Saint-Germain. Follow Suivants three times. Expected and observed page ranges: 1–50 / 179, 51–100 / 179, 101–150 / 179, 151–179 / 179; Suivants disabled on the last page. The original hard cutoff at 200 has been removed in favor of paging all lengths. The representative real array used for this run has 179 elements; no real array above 200 was executed. The complete JSON also round-trips every cell.

Additional real cases:

- Unused substitute Vincent Sasso (p_0Ca3qH), match player statistics: explicit Statistiques non renseignées, zero invented metric rows.
- Upcoming Villarreal–PSG (m_0k4IES): missing statistics stay explicit, zero stat rows; scoreboard shows À venir and kickoff time. Save Archive complète to browser-upcoming-archive.json and compare with canonical data.
- Historical Union Berlin–Leverkusen (m_01FdKs): open with season=2026/2027 and sourceSeason=2024/2025 to exercise remote archive fallback. Original Bundesliga and 2024/2025 identity must appear, with 43 statistics for the selected period. Save full archive to browser-historical-archive.json; it equals canonical data. Also reconciled m_4XOc3a over real HTTP.

## Results and retained failures

- Final build and all 80 existing checks pass (27 Python, 53 Node). Logs: regression-release-final.log. No new unit tests were written after implementation.
- Real production-mode HTTP checks pass: nine Next routes, unknown route 404, backend health, two complete season payloads, six raw partitions, archived match/profile, private-path isolation and credential scan. See http-evidence.json, http-runtime.log and http-release-final.log.
- Initial regression.log retains three failures caused by changed legacy number/heading formatting. The implementation restored those contracts without changing tests. Intermediate successful runs are retained as well.
- An early full-archive browser capture timed out at three seconds while mounting the nested explorer. New explorer disclosures now render on expansion, avoiding the stall while keeping every record reachable. The complete archive capture succeeded afterwards.
- The source-audit helper initially tried a 2021/2022 observation partition that does not exist. The manifest has six season catalog entries; detailed observation shards currently cover 2024/2025, 2025/2026 and 2026/2027. The historical deep check now uses an actual 2024/2025 record. No data was collected or invented to fill earlier seasons.
- Browser capture originally used an unsupported level option on getByRole and one shell read used an incorrect dashboard-relative path. Both harness errors were corrected; neither was reported as a product pass.
- During historical testing, the breadcrumb incorrectly showed the current filter season. It now shows match.season and remote fixture normalization retains the archived competition and season. The corrected browser check passes.

UX/DX/AX: native select semantics and IDs remain stable; the browser renders the menu in the top layer. Summary views remain compact, detailed metrics keep source grouping, and generic Explorer/JSON views make new fields inspectable without a new bespoke renderer. Pagination and lazy expansion bound DOM work; full JSON can still be large and scrolls within its own keyboard-focusable panel. Canonical data and provider contracts are unchanged.

Commit names: fix: make dropdown menus readable in dark mode; feat: expose complete match and player statistics; fix: keep complete player metrics readable; docs: record match and player data completeness verification.

## Production readback

Source commit 115d08d475b6a102554789b00a19f8e823356d1b deployed READY as dpl_CEZ6Rs9djJBVJUcVJZ74929rgLYe. Public browser checks confirm a dark open native picker, all three player periods/38 full-match metric rows, 43 second-half team statistics, exact full-archive JSON equality and exact advanced-player source equality. Browser console: zero warnings/errors. Cloud HTTP passes nine routes, thirteen archive families, six season catalog entries and the Bun backend; data redirects point at this exact Git revision. See production screenshots, production-archive.json, production-player-advanced.json, browser-evidence.json and cloud-evidence.json. The final commit changes only documentation/evidence; its deployment receipt is written separately to the ignored daily-refresh outputs folder.
