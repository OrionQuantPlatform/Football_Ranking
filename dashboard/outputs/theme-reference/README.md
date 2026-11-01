# Navbar theme and white reference verification

The user's clarification is authoritative: use only a moon/sun icon in the navbar; no menu or Settings page. Existing preference storage and the dark palette are preserved. Source commit: `6bfc4bf7`.

Reference: https://londonstrategicedge.com/data/. The public light page was inspected in a real browser. Observed CSS neutral colors are in `reference-palette.json`; no reference artwork, layout or financial content was copied. STATARENA blue replaces the reference's accent color.

Setup, exact rerun commands, browser input URL and expected failures were recorded before implementation in `PLAN.md`. Use the existing production Next/Bun app and canonical local JSON; no provider credential is required.

Actual results:

- Production build passed (`build.log`).
- Existing full HTTP E2E passed (`application/http-evidence.json`, `application/http-runtime.log`): eight routes, two complete seasons, raw partitions, archives/profiles and private-file isolation. No unit tests were added or changed.
- Browser E2E passed at 1280×720 desktop and 390×844 mobile in both schemes. Light body/cards are rgb(255,255,255), body text rgb(22,24,29) and card borders rgb(220,223,228). Native select options have a white background and dark text. The open selector screenshot is `select-light.jpg`.
- Sun activates light; Moon activates dark. The light icon's CSS class is lucide-moon; the restored dark icon is lucide-sun. The rightmost control is a 44px target with a right edge of 370px in a 390px viewport.
- Light selection survived reload and navigation to a real match. Browser theme-color remained #FFFFFF through both; returning to dark restored #0F0F11 and the existing dark body/text rgb(15,15,17) / rgb(227,228,230).
- Real player and match details were opened: their light surfaces are white, with the player footer rgb(241,242,244). The scoreboard, detail cards, charts and shared footer remained usable. Original navbar/footer logo variants remain unchanged.
- Mobile document width was exactly 390px in both modes, without horizontal overflow. Browser console errors: none. No Settings navigation link or page was added.

Detailed observations and seven screenshots are listed in `browser-evidence.json`. Storage denial and cross-tab synchronization were not simulated. A transient working-directory typo in an edit command was corrected before the final build and E2E run; it did not affect the verified result.

After the final push, inspect the Git deployment at https://statarena-analytics.vercel.app, click its moon/sun control, verify reload persistence and compare the final deployed SHA's data URL. Public release receipts can be saved outside the repository to avoid changing application revisions merely to record them.
