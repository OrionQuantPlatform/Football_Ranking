# Football Ranking

### Un classement du Ballon d’Or construit à partir des performances sur le terrain.

[![Statut : recherche](https://img.shields.io/badge/statut-recherche-blue)](#état-du-projet) [![Licence : MIT](https://img.shields.io/badge/licence-MIT-green.svg)](LICENSE)

Football Ranking est un projet de recherche qui explore une question : **comment comparer la saison d’un attaquant, d’un milieu, d’un défenseur et d’un gardien dans un même classement ?**

L’objectif est de construire un classement personnel, transparent et explicable, à partir des performances match par match, du rôle joué et du contexte de chaque rencontre.

> **État actuel : conception et recherche.** La méthode est documentée, mais le pipeline, les modèles et le classement ne sont pas encore implémentés ou validés.

## L’idée

Un buteur et un défenseur ne contribuent pas de la même manière. Le projet propose donc d’évaluer chaque joueur par rapport aux attentes de son rôle, puis de combiner ses performances sur la période choisie.

```text
Matchs et données joueurs
          ↓
Contexte des équipes avant le match
          ↓
Performance observée vs attendue pour le rôle
          ↓
Contributions par match et bilan de saison
          ↓
Classement expliqué et comparaisons par rôle
```

Cette comparaison mesure une **excellence relative au rôle**. Elle ne démontre pas que deux joueurs de postes différents ont apporté exactement le même nombre de buts ou de victoires à leur équipe.

## La méthode envisagée

| Étape | Approche proposée |
|---|---|
| **Contexte** | Estimer la force des équipes avant chaque match avec une méthode de type Elo. |
| **Rôle** | Comparer les actions du joueur à une référence adaptée à son poste et aux occasions d’agir. |
| **Gardiens** | Évaluer notamment les arrêts au regard de la difficulté des tirs, ainsi que le jeu aérien et la relance si les données le permettent. |
| **Saison** | Combiner la contribution cumulée et le niveau par 90 minutes, avec régularisation des petits échantillons. |
| **Classement** | Utiliser des percentiles par rôle et examiner la sensibilité des résultats aux choix de pondération. |

Les poids, références et règles d’éligibilité restent des hypothèses de travail. Une autre piste, fondée sur la valeur des actions comme VAEP, est également décrite dans la documentation.

**[Lire la méthode mathématique complète →](docs/METHODE_CLASSEMENT_BALLON_D_OR.md)**

## Données

Le projet vise des données de match, de composition, de performance individuelle et de tirs. [PitchAPI](https://pitchapi.dev/) est une source envisagée pour une première étude de faisabilité. Sa couverture réelle, la disponibilité des indicateurs et les droits d’utilisation des données restent à vérifier avant de construire le pipeline autour de cette source.

La licence de ce dépôt ne s’applique pas aux données de fournisseurs tiers : leurs propres conditions restent applicables.

## État du projet

- [x] Documenter les formules et les hypothèses initiales.
- [ ] Vérifier la couverture et la qualité des données disponibles.
- [ ] Définir les paramètres et les références par rôle.
- [ ] Construire le pipeline et calculer les scores par match.
- [ ] Évaluer la stabilité et les limites du classement.

Ces étapes décrivent une direction de recherche ; les résultats et les performances du modèle restent à établir.

## Explorer le dépôt

```bash
git clone https://github.com/OrionQuantPlatform/Football_Ranking.git
cd Football_Ranking
```

La documentation est accessible dans [`docs/`](docs/). Le fichier [`.env.example`](.env.example) indique le nom de la variable prévue pour une clé PitchAPI ; aucune intégration API n’est encore disponible. Si tu prépares un fichier local, garde la clé dans `.env`, qui est ignoré par Git.

## Licence

Le contenu du dépôt est distribué sous la [licence MIT](LICENSE). Les marques, données et services de tiers restent soumis à leurs conditions respectives.
