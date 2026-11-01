# Light/dark theme refinement E2E

User clarification: only a moon/sun icon in the navbar; no appearance menu or Settings page. Keep the existing persistent toggle and use London Strategic Edge's /data light appearance as a visual reference, with STATARENA blue accents.

Reference observed in the browser: body/background white rgb(255,255,255), foreground rgb(22,24,29), borders hsl(220,13%,88%), muted surfaces hsl(220,14%,95%), muted text hsl(220,9%,36%). No layouts, financial content or brand artwork copied.

Setup: actual production Next/Bun application with canonical local football JSON. No provider credentials needed.

Rerun from dashboard:

```sh
PATH=/Users/lemonnierhugo/.bun/bin:$PATH bun run build
ORION_EVIDENCE_DIR=outputs/theme-reference/application bun run verify
PORT=3014 API_PORT=8774 bun start
```

Browser: open http://127.0.0.1:3014/?season=2026%2F2027&league=l_3FJFUl at desktop and 390x844 mobile.

Expected / failure cases:
- The only appearance control is the rightmost icon button. Sun activates light, Moon activates dark; labels identify the next action. No new Settings link or route.
- White body/cards, thin neutral borders, subdued gray control/footer/table surfaces, dark typography, blue interactive/chart accents; native select menus remain readable.
- Charts, match detail, player dialog, tables and footer follow the selected scheme without a layout change. Original logo switches correctly; compact navbar mark and complete footer logo preserved.
- Choosing a theme persists through reload and navigation; browser theme-color metadata matches white/dark. Dark palette is unchanged.
- No mobile horizontal overflow or inaccessible theme hit target; no browser console errors.
- Existing eight-route/data E2E passes. Do not claim unavailable storage or browser policies were simulated.

Actual: passed; see README.md, browser-evidence.json, application/http-evidence.json and the seven screenshots.
