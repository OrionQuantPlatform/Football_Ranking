# Design restoration acceptance

Restore the earlier HTML dashboard's visual hierarchy in native React: logo, aligned filters, featured collected match, player portraits and ranks, clear name/club separation, readable catalog cards and match rows, and coverage bars. Retain seven real pages, current controls, all data and Bun backend. Avoid marketing copy and invented statistics.

Failure modes: filters overflow or become unlabeled; directory cards lose links; player/team names run together; match score/teams misalign; chart or modal is unusable; mobile horizontal overflow; season/filter navigation breaks.

E2E: run `cd dashboard && bun run dev`; open http://127.0.0.1:5173; switch season, filter, open featured match/player dialog, visit clubs/competitions/players/rankings; inspect desktop and narrow viewport. Expected: observable selected state and data updates, clear text hierarchy, working document navigation, no application diagnostics. Save screenshots, exact actions and actual results. Run production build and existing affected regressions; remove generated dist afterward.
