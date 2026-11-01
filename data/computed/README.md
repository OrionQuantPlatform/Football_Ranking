# Données dérivées

`dashboard/` contient les vues de lecture du site, générées sans perte depuis les tables de `data/raw/`. Une archive compressée regroupe les huit tables de chaque compétition-saison ; un petit manifeste référence ces archives.

Régénération : `python3 dashboard/scripts/build_dashboard_views.py`. Les publications de données quotidiennes et historiques le font automatiquement. Le contenu des tables brutes reste la référence ; aucune métrique Orion n'est calculée par cette optimisation.
