# React design restoration — 1 November 2026

## Setup and exact commands

Repository: `/Users/lemonnierhugo/Desktop/Coding Project/Football_ranking`.
Bun: `/Users/lemonnierhugo/.bun/bin/bun`. Canonical JSON data already present; no API key required for the archive workflows exercised.

From `dashboard/`:

```sh
export PATH="/Users/lemonnierhugo/.bun/bin:$PATH"
bun run dev
# Frontend http://127.0.0.1:5173; backend http://127.0.0.1:8765
bun run test > outputs/design-restoration/regressions-final.log 2>&1
bun run format:check > outputs/design-restoration/format.log 2>&1
bun run build > outputs/design-restoration/build-final.log 2>&1
```

Expected: seven page entries compile, existing data/rendering/API regressions pass, formatted source; page links and filters retain their contracts. Actual: 28 Python and 56 Node tests passed, build and formatting passed. Source data unchanged. Generated `dashboard/dist` removed after checks; dev preview stays running. `final-checks.json` preserves compiled HTML hashes and source hashes.

## Browser rerun

Use the local frontend. Default desktop viewport in this run: 1147×1031. Mobile override:390×844, reset after checks.

1. Overview2026/2027: verify logo, featured Porto4:0Estoril,133882 appearances,4339 matches, ranked player portraits and coverage bars.
2. Players: search `Aaron Collins`, open his performance. Expect79 minutes, rating9.88, separate metric labels/values and missing values as dashes. Close dialog, return overview and reset search.
3. Select season2025/2026: expect393593 appearances,12742 matches, Málaga1:1Las Palmas and updated URL.
4. At390px verify overview has no document overflow; click `Explorer le match`. Expect Málaga–Las Palmas detail, actual score, chart controls.
5. Clubs: search `Bayern`, expect one card with48 matches; open it. Expect identity, UEFA history, match links and squad. Mobile document width remains390. The three-column UEFA table was subsequently made fluid rather than retaining the performance table's800px minimum width.
6. Competitions: verify badges, names/countries, season counts and real document links. Card rows retain consistent heights for multiline names.
7. Rankings: select edition2022-02-10 and searchFrance. Expect rank3,1786.150points, previous rank3. Check mobile controls and contained table.
8. Method: inspect readable coverage and source/interpretation limits. Return overview, reset viewport to desktop, leave preview open.

Actual results and captured console: `browser-evidence.json`. Final captured browser diagnostics: none. Screenshots include desktop overview, catalogs, player table/dialog and mobile overview, match, club and rankings. Before: `before.jpg`; after: `overview-desktop.jpg`, `preview.jpg`, `overview-mobile.jpg`.

## Corrections and limits

An initial regression run exposed the existing abbreviated accessible chart labels being changed along with the visual axis captions. Restored the original accessible contract while retaining expanded visual captions; final56/56passed. Original failed log retained as `axis-label-regression.log`. A missing H2H row key detected by the existing fixtures was corrected. Two browser waits expired at3seconds while loading the large season; following captures verified loaded results. A Bayern link locator used the wrong match count and was corrected from the visible card.

No live provider calls or deployment tested. CSV downloads and full keyboard/screen-reader audits were not repeated in this presentation pass. Existing CSV and null/zero regressions passed. Mobile navigation scrolls horizontally inside its own navigation region; wide player performance tables retain their own table scroll.
