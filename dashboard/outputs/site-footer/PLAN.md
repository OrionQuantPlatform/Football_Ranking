# Footer and compact navbar logo E2E

Setup: actual production Next/Bun application with canonical local football JSON and official STATARENA assets. No provider credentials needed.

Rerun:

```sh
cd dashboard
PATH=/Users/lemonnierhugo/.bun/bin:$PATH bun run build
ORION_EVIDENCE_DIR=outputs/site-footer/application bun run verify
PORT=3013 API_PORT=8773 bun start
```

Browser inputs: http://127.0.0.1:3013/?season=2026%2F2027&league=l_3FJFUl; test desktop and 390×844 mobile. Use the navbar theme button to inspect both schemes; scroll to the footer with keyboard End, follow its Joueurs and Classement joueurs links, then use its logo to return home.

Expected / failure modes:
- One contentinfo footer outside main, with full original logo, four useful link columns and a separated copyright/license row matching the reference hierarchy.
- Navbar uses only the smaller original symbol in both schemes, retaining an accessible STATARENA home link and a minimum 44px click target. Theme button remains at the far right.
- Footer links target existing pages/documents, retain season/competition context for internal navigation, and show the current page. No empty or invented social/legal links.
- The footer remains visible on the data-loading shell and rendered pages, without duplicate landmarks. Its brand mark uses the approved horizontal variants; no added tagline.
- At 390px the columns reflow, text remains legible, keyboard focus is visible and the document does not overflow horizontally.
- Existing route/data/archive E2E continues to pass. No settings route is restored.

Actual: passed; see README.md, browser-evidence.json, application/http-evidence.json and the seven screenshots. First build/setup failures are retained separately.
