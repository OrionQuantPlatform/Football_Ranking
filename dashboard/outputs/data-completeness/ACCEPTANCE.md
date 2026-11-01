# Dropdown readability and complete match/player data

Written before implementation.

## Failure modes and expected outcomes

- Native option menus inherit light OS popup colors and pale text. Open competition, season and minutes pickers: dark background, readable text, selected/hover state, uncut menu, native keyboard navigation and escape. Keep existing select labels, IDs and URL/state behavior; verify mobile and the all-competitions scope.
- Team statistics show All while FirstHalf and SecondHalf exist. Expose every source period and every group/item; unknown future keys must remain visible. Preserve zero, percentages, fractions and original source values.
- The player modal lists selected normalized metrics but misses long passes, fouls, aerials, shot accuracy and advanced fields. Expose all original metric groups without deduplication, periods and complete player records. Keep summary, comparisons and match/profile links.
- Graphs/lineups/events/networks/heatmaps are projections and omit fields. Provide a complete Explorer and exact JSON for every family, plus the full archive with statuses/provenance and unknown families.
- Arrays over 200 are silently cut; raw numbers are rounded. All array pages must be reachable, with correct indices/counts, and exact JSON must round-trip all leaves including precision, false, zero, null and empty arrays/objects.
- Loading, missing records and endpoint errors must be explicit and retryable; no invented values or fabricated metric agreement. Archived data is primary; do not perform a new collection campaign.

## E2E procedure

Use the real running Next.js frontend and Bun backend, not mocked component rendering. Source reference: /api/archive/matches/m_49qvGz (Le Havre–PSG; player p_4QqLFm Achraf Hakimi) and m_4XOc3a; include an upcoming/missing-family match and an older season. Independently read canonical data/raw reference files for source counts/fields and the API readback. Compare rendered exact JSON with original payloads for all 13 families and full archive, then the player-scoped data and full/half metric row counts. Test a real source array exceeding 200 and its last page. Exercise native keyboard selection/Escape and responsive width 390.

Save exact setup, rerun commands, inputs, expected/actual results, browser DOM evidence/screenshots, logs and failures in this directory. Run the existing regression suite and production HTTP verifier. Confirm Git-linked production deployment and repeat critical browser checks live. No new post-implementation unit tests.
