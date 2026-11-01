# Player ranking placeholder

Written before implementation.

- A new Classement joueurs navbar link opens /classement-joueurs with an active navigation state and matching page title/metadata.
- Display exactly thirty ordered positions, numbered 01–30, each visibly marked À venir. No real or invented player names, rankings, scores, profiles or collection work.
- User refinement and correction: add a small golden Ballon d’Or symbol only in the page heading for the future algorithmic top 30. Keep the navbar text-only. Use a crisp SVG with a unique gradient ID and decorative accessibility semantics; keep the thirty placeholders empty.
- Latest user correction: completely delete the old standalone FIFA/UEFA Classements page, its route, navbar entry, page components and dedicated styles. Keep club UEFA history in a separate component, and preserve Joueurs, Matchs, footer, analytics and canonical data. The empty player ranking must not trigger the full season-data download.
- E2E: enter through the actual navbar; verify thirty visible rows and their rank/placeholder content, first and last row, active link, mobile layout without document overflow and keyboard access. Verify the old /classements route returns 404, its files are gone and club UEFA history still renders. Save DOM/screenshot evidence and exact rerun commands, production build/HTTP E2E and deployment readback. No new isolated tests after implementation.
