# Rankings acceptance evidence

Setup: repository dependencies already installed; downloaded source responses under `data/sources/rankings/`, normalized tables under `data/raw/rankings/`. `.env` remains ignored; never pass its contents into the browser. No deployment was performed.

Rerun from the repository root:

```sh
python3 scripts/collect_rankings.py --from-year 2022
python3 scripts/build_dashboard.py
python3 scripts/verify_rankings.py
npm test
PORT=8878 node dashboard/server.js
```

The collector reuses cached responses and can still request the FIFA schedule fallback. To verify existing data entirely offline, omit the collection command.

Expected: 32 official FIFA editions, six UEFA club and six UEFA association seasons, three distinct current SportsAPI snapshots; every native row retained and every displayed coefficient reconciled. Actual: 47 editions, zero collection errors; source reconciliation and public credential scan passed (`verification.json`, `verification-final.log`, `collect-final.log`).

Expected: build includes new module and ranking JSON without credentials or private archives; existing regression suite stays green. Actual: 1,769 embedded public assets; 28 Python and 56 Node checks passed (`build-final.log`, `checks-final.log`).

Browser rerun: open http://127.0.0.1:8878, then Classements → Sélections FIFA → edition2022-02-10 → search France. Expect rank3, points1786.15. Switch to Associations UEFA →2021/2022; expect55 countries, England rank1 coefficient106.641. Under Clubs, search/open Bayern München; expect six annual rows, oldest rank1 coefficient138. Search/open Fulham; expect an explicit missing mapping. Actual browser DOM, outcomes and console capture: `browser-evidence.json`; screenshots: `nations-fifa-2022.png`, `club-bayern.png`. No browser console errors observed.

Not exercised: forced network failure/retry and mobile viewport. Historical UEFA source update timestamps do not establish the coefficient available before each match. Club mapping covers242 of830 project entities;588 remain explicitly unmatched.

Initial failed collector attempts are retained in the first/second-attempt artifacts and logs. They are superseded by the final successful collection and exhaustive reconciliation.
