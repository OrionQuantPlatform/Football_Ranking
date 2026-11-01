# Rankings E2E acceptance

- Keep SportsAPI credentials only in ignored .env; never in frontend, assets, logs or saved responses.
- Retain exact sources, provider timestamps, ranking period and retrieval time separately.
- SportsAPI latest-only responses must never be labelled as historical editions.
- Enumerate official FIFA ranking dates since 2022 and download each; validate date, nonempty rows, ranks and unique entity IDs.
- Download UEFA overall club and association coefficients for season-end years from 2022 through the current season; follow all pages and reconcile counts.
- UEFA associations measure club competition coefficients, not national-team strength.
- Link club IDs across providers only with reviewed/unambiguous identity evidence and country checks. Unmatched and ambiguous clubs remain explicit.
- Verify real HTTP + browser workflow: new national/association ranking page, date/period changes, search, club coefficient history, source dates and missing mappings.
- Rerun build and existing regression checks; preserve failures and machine-readable collection/verification evidence.
