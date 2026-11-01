# Stockage JSON du projet

- **`raw/`** : base de données en fichiers JSON, organisée par saison et entité : joueurs, équipes, matchs, performances, tirs et observations détaillées.
- **`computed/`** : résultats des futurs modèles, séparés des observations.
- **`sources/`** : archives originales et conditions d’utilisation, conservées pour reproduire les imports.
- **`staging/`** : intermédiaires locaux de génération, ignorés par Git.

Le backend et le frontend du dashboard lisent la base dans `raw/`. Les fournisseurs sont une provenance des observations, pas l’organisation métier de cette base.

La [documentation du schéma et des relations](../docs/JSON_DATABASE.md) décrit les identifiants, les tables, l’import et leur lecture par le dashboard. Les valeurs calculées et validées d’Orion n’existent pas encore.

Les [classements FIFA datés depuis 2022 et coefficients UEFA par saison depuis 2023/2024](../docs/RANKINGS.md) se trouvent dans `raw/rankings/`, avec leurs éditions et relations vers les clubs.
