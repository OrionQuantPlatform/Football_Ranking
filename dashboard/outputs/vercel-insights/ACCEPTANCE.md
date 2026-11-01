# Vercel insights integration

Written before implementation.

- Install @vercel/speed-insights and @vercel/analytics as frontend runtime dependencies; update the existing Bun lockfile, without introducing another package-manager lockfile.
- Root layout renders exactly one SpeedInsights from @vercel/speed-insights/next and one Analytics from @vercel/analytics/next, covering all pages and client navigation independently of data loading. Preserve the layout as a Server Component and the existing application/data/UI.
- Failure cases: missing runtime dependency in the frontend workspace, lockfile drift under frozen installation, client-only hooks outside Suspense, duplicate injected scripts, navigation failures, production collector scripts unavailable, or development debug output confused with collected production data.
- E2E: build the production application; run the existing real HTTP route/API/data E2E and existing regressions; inspect mounted production scripts and navigation in a real browser. Confirm available public script endpoints and report any collection/dashboard behavior not directly observed. Save setup/inputs, rerun commands and actual logs/DOM evidence.
- Commit each integration separately with explanatory bullet points; push all tracked changes and verify the exact final Vercel production revision. No new isolated tests after implementation.
