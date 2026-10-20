# kiln : notre idée de projet

> Brouillon du 17 octobre 2026. Il réunit une longue conversation de recherche, des mesures faites
> le jour même sur deux repos réels (le repo d'association et un repo d'université) et des recherches
> web (sources à la fin de chaque document). Il sert de base de travail, pas de vitrine. Le détail
> des deux mesures n'est pas publié : il reste sur une branche locale (voir `CLAUDE.md`, « Repos
> d'entraînement »).

## Les documents

| Document | Contenu |
|---|---|
| Ce fichier | L'idée en une phrase, le problème, les cinq piliers en bref, la cible, le périmètre, nos atouts |
| [La doctrine](doctrine.md) | La façon unique de faire, et ses onze principes |
| [Les cinq piliers](piliers.md) | Méthodes et outils, normes de code, lisibilité par Claude, allègement, versions |
| [Comment ça marche](fonctionnement.md) | Le script trouve, Claude juge ; le circuit des mises à jour et des remontées ; les tests au moindre coût |
| [La grille de référence](grille.md) | Le cœur du produit : ce que contient une règle, et le classement par thème et par portée |
| [Le marché et la concurrence](marche.md) | Le paysage, ce qui nous protège, ce qui fait percer un outil, les besoins des utilisateurs de Claude |
| [Le nom](nom.md) | Qui répond à « kiln », ce qu'un changement de nom touche, trois noms libres (T-143) |
| [Risques, validation et prochaines étapes](plan.md) | Pistes écartées, idées en réserve, risques, plan de validation, prochaines étapes |

## En une phrase

**kiln garde un repo à jour par rapport au meilleur du monde (méthodes, structure, outils,
conteneurs, sécurité, normes de code) et le rend facile à lire pour Claude.**

Les numéros de version comptent, mais Dependabot et Renovate s'en chargent déjà : kiln s'occupe
de tout le reste. L'image la plus juste est celle d'une **distribution**, comme Ubuntu pour un
ordinateur. Elle choisit les meilleurs outils et les meilleures méthodes, vérifie qu'ils marchent
ensemble, et fait passer chaque repo à la version suivante.

**Objectif :** que kiln devienne l'outil de référence sur ce problème, ce qui se mesure à
l'adoption (étoiles, installations).

Accroches possibles :
- « Ce que Dependabot fait pour les versions, kiln le fait pour les méthodes. »
- « Le Tech Radar qui s'applique tout seul à ton code. »
- « Ton repo, à jour avec le meilleur du monde, pas seulement ses versions. »
- « Tu n'as plus à choisir : kiln choisit le meilleur, preuves à l'appui, et le tient à jour. »

## Le problème

1. **Le monde avance plus vite que les repos.** uv a remplacé pip, ruff a remplacé
   flake8, black et isort. Les conteneurs sont devenus rootless, la quarantaine des dépendances
   est apparue en 2025, les passkeys s'imposent. Personne ne prévient un repo qu'une meilleure
   méthode existe.
2. **Les outils existants s'arrêtent aux versions** (Dependabot, Renovate), **ou visent les grandes
   entreprises** (AWS Transform, Moderne : voir [le marché](marche.md)).
3. **Le code écrit par les agents accélère la dette.** 90 % des développeurs professionnels
   utilisent un agent chaque semaine, et environ 47 % de leur code est écrit entièrement par un
   agent (JetBrains, 2026). Dans le même temps, la part de refactoring est tombée de 21 % des
   lignes modifiées en 2022 à 3,8 % en 2026 (GitClear).
4. **Personne n'a plus le temps de tout relire.**
   - La production de code par développeur a doublé, mais le nombre de relecteurs n'a été
     multiplié que par 1,5 (CMU et Stanford, 196 000 PR).
   - La part des PR qui reçoivent un vrai commentaire humain est tombée de 39 % à 21 %, et le
     temps médian de relecture a augmenté de 441 % (Faros).
   - 96 % des développeurs ne font pas pleinement confiance au code généré, mais 48 % seulement
     le vérifient toujours.
   - LinearB constate que les équipes se *sentent* 20 % plus rapides alors qu'elles sont 19 %
     plus lentes.

   D'où le principe « rien sans preuve ».
5. **Les petites structures n'ont personne pour faire cette veille** : une association, une PME de
   50 personnes, une filière d'université dont l'équipe étudiante change chaque année.
6. **Les repos ne sont pas pensés pour être lus par un agent.** Chaque fichier mal découpé ou
   mal nommé se paie en jetons, en relectures et en erreurs.

## Les cinq piliers en bref

Le détail est dans [les cinq piliers](piliers.md).

1. **Méthodes et outils à jour** : une grille de référence tenue à jour, appliquée au repo.
2. **Normes de code** : nommage, typage, tailles et autres règles, appliquées et pas seulement
   conseillées. La charte du repo d'association en est la base.
3. **Lisible par Claude** : un dossier par fonctionnalité, un fichier = une idée, des noms qui
   servent de sommaire.
4. **Alléger** (piste) : retirer les dépendances et le code inutiles, avec une preuve.
5. **Versions** : déléguées à Dependabot ou à Renovate.

Le tout suit une [doctrine](doctrine.md) : une seule façon de faire, le script d'abord et Claude
ensuite, rien sans preuve.

## Pour qui

- **D'abord** les petites structures sans équipe plateforme : associations, PME d'environ
  50 personnes, universités (projets étudiants, labos), indépendants.
- **Pas au début** les grandes entreprises : AWS et Moderne les servent déjà.

## Périmètre de départ : Django et Nuxt

- **Deux stacks d'abord, celles du repo d'association** : Django pour le backend, Nuxt pour le frontend.
  L'objectif est de les amener au niveau maximal de la grille, plus à jour que le repo d'association lui-même.
- **Chaque stack compte seule** : un repo Django avec un front React profite quand même du profil
  Django.
- **Le repo d'association sert de terrain d'entraînement.** À chaque version de kiln, on mesure son score
  (18 pratiques sur 31 le 17 octobre) et on vérifie que `kiln update` le fait monter sans rien
  casser.
- **Le repo d'université et d'autres repos ordinaires servent d'épreuve** pour des repos que kiln n'a pas
  créés, toujours sur une copie locale.
- **Les autres modèles déjà dans kiln sont gelés** (décidé le 17 octobre 2026, ticket T-133) :
  FastAPI, données Python, ligne de commande, Java, Next, Astro, Streamlit et Dash restent
  générés et testés, sans nouveau travail de grille tant que Django et Nuxt ne sont pas au
  sommet ; les règles universelles les notent quand même.

## Pourquoi kiln peut le faire

**La moitié de la machinerie existe :**
- un modèle Copier par stack ;
- `kiln update` avec ses conversions ;
- des versions candidates et des canaux ;
- `kiln adopt` pour les repos existants ;
- `kiln status` et `kiln update --all` pour gérer une flotte de repos ;
- le moteur `charte` (interdictions, cliquets, dérogations) ;
- des workflows de CI réutilisables ;
- des plugins Claude Code (skills, hooks, Serena) ;
- `/kiln:report`, qui remonte déjà les défauts de kiln en issue ou en PR, avec l'accord de
  l'utilisateur.

**La charte du repo d'association fournit les normes de départ**, éprouvées en production.

**La friction est vécue** : tenir seul plusieurs repos à jour, dont un en production. C'est d'elle
que naissent les outils qu'on tient des années.

## Sources

**Marché et usages :**
- [JetBrains, adoption des agents de code en 2026](https://blog.jetbrains.com/research/2026/08/ai-coding-agent-adoption-2026/)
- [GitClear, maintenabilité à l'ère de l'IA (LeadDev)](https://leaddev.com/ai/code-maintainability-plummets-in-the-ai-coding-era)
- [Le goulot de la relecture en chiffres](https://www.flowverify.co/blog/ai-code-review-bottleneck-2026-data)
