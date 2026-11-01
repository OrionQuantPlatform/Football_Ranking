# Theme and removed-settings E2E contract

Setup: production Next/Bun app; no provider key required. Use CUA browser at desktop and 390px mobile width. Begin in a fresh browser origin or select dark mode explicitly.

Expected outcomes / failure cases:
- Navbar has no Settings/Réglages link; GET /reglages returns 404; the route and SettingsPage source files no longer exist.
- A named theme button is the last navbar control and remains reachable on mobile.
- Switching dark to light changes page, cards, filters, native menus, charts and modal colors; logo uses the approved color variant and text stays readable.
- Reload preserves the selected theme; navigating to Matches and Players preserves it. Switching back restores neutral dark/blue, with no green accent.
- Actual player and match details, European focus and data loading still work.
- Local storage denial falls back to a working in-memory theme. No network request or credentials required by the toggle.

Rerun: cd dashboard && bun run build && PORT=3012 API_PORT=8772 bun start; open http://127.0.0.1:3012/?season=2026%2F2027&league=l_3FJFUl and click the theme control, reload, open a player, navigate to Matches; repeat at 390x844. HTTP: ORION_VERIFY_URL=http://127.0.0.1:3012 node scripts/verify_brand.mjs.

Actual results: passed for the normal browser workflows; see browser-evidence.json and the four desktop/mobile screenshots. Denied localStorage was reviewed but not simulated.
