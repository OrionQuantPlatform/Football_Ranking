# Unified Matchs navigation

Written before the refinement's implementation.

- Topbar contains Vue d’ensemble, Compétitions, Clubs, Joueurs, Matchs, Classements, Réglages. No Calendrier or Données & méthode entry. Method remains available in the footer.
- One Matchs page: À venir (default) and Résultats, real link navigation with clear active state, keyboard operation and preserved competition/season/search/scope. Mode selector sits above relevant filters.
- À venir contains the existing Monday–Sunday Paris calendar, week navigation, day groups, pagination and fixture links. Résultats preserves archived match listing, pagination, performance filters/export and analysis details.
- Overview's upcoming link opens Matchs/À venir; collected-match link opens Résultats. Detail back navigation returns to the originating mode/week/filters. Existing /calendrier links redirect to Matchs/À venir with week and filters intact.
- E2E: overview → unified Matchs → next week → Résultats → match detail → results; À venir → fixture detail → same week; footer → method; legacy calendar redirect. Desktop + 390px + keyboard. Reconcile fixture IDs/times with canonical JSON independently. Save screenshots/DOM/logs/exact rerun commands, build + existing regressions, then Git→Vercel and verify production.
