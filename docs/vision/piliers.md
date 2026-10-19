# kiln : les cinq piliers

> Partie de [l'idée de projet](README.md). Brouillon interne du 17 octobre 2026.

## 1. Méthodes et outils à jour

Une **grille de référence** tenue à jour, appliquée au repo. Elle couvre six domaines :
- l'outillage ;
- la chaîne d'approvisionnement ;
- les conteneurs et l'exploitation ;
- les tests ;
- la sécurité applicative ;
- l'observabilité et la livraison.

Exemples de pratiques mesurées : lockfile et installation figée, quarantaine des nouvelles
versions, actions de CI épinglées par empreinte, conteneurs non-root en lecture seule, tests par
propriétés, fuzzing de l'API, passkeys. La façon d'obtenir un maximum de tests pour un minimum de
jetons est détaillée dans [comment ça marche](fonctionnement.md).

## 2. Normes de code

Des normes de code appliquées, et pas seulement conseillées :
- **nommage** : casse par type de symbole, pas de noms génériques (`data`, `res`, `tmp`…),
  booléens préfixés ;
- **typage** : annotations obligatoires, typage strict en cliquet ;
- **tailles** : fichier et fonction ;
- **autres règles** : une classe par fichier, pas de valeurs magiques, argent en centimes,
  fuseau horaire, données personnelles hors des logs, secrets hors du dépôt.

La charte du repo d'association en est la base : identifiants stables ([TAILLE-FICHIER], [TAILLE-FONCTION],
[UNE-CLASSE], [NOMS-INTERDITS], [BOOLEENS], [CASSE], [ZERO-MAGIE], [ARGENT], [FUSEAU],
[DONNEES-PERSO], [SECRETS], [PYTHON-MODERNE], [TYPAGE-STRICT]…), et trois régimes :
- **stricte** : zéro infraction, la CI échoue ;
- **cliquet** : un budget qui ne peut que baisser ;
- **revue** : appliquée en relecture.

Le moteur `charte` de kiln sait déjà appliquer ces trois régimes.

## 3. Lisible par Claude

**Hypothèse de départ :** beaucoup de petits fichiers bien nommés font économiser bien plus de
jetons que quelques gros, à lignes égales.

**Ce qu'on sait aujourd'hui :**
- **La direction est juste, l'extrême non.** Claude lit fichier par fichier, et les noms servent
  de sommaire. Mais chaque fichier ouvert coûte un appel d'outil, répète ses imports, et un
  enchaînement éclaté oblige à ouvrir dix fichiers l'un après l'autre.
- **Un modèle simple** (fonctionnalité de 1 500 lignes) donne l'avantage au découpage moyen :
  15 fichiers de 100 lignes font environ 5 400 jetons par tâche en moyenne, contre 8 300 pour
  5 fichiers de 300 lignes et 7 400 pour 100 fichiers de 15 lignes.
- **La seule mesure trouvée** est l'étude de Sonar (660 essais avec Claude Code) : un code propre,
  à architecture égale, fait −7 à −8 % de jetons, −34 % de fichiers relus, et le même taux de
  réussite. **Aucune étude ne compare directement 5 gros fichiers et 100 petits.**

Le modèle, avec ses hypothèses (environ 10 jetons par ligne, fichiers lus en entier, 8 lignes
d'import et environ 100 jetons de coût fixe par fichier ouvert) :

| Découpage | Modifier une fonction | Comprendre toute la fonctionnalité | Moyenne (8 tâches ciblées sur 10) |
|---|---|---|---|
| 5 fichiers de 300 lignes | ~6 400 jetons | ~16 000 | ~8 300 |
| 15 fichiers de 100 lignes | ~2 400 | ~18 000 | ~5 400 |
| 100 fichiers de 15 lignes | ~1 000 | ~33 000 | ~7 400 |

Le modèle ne compte ni les allers-retours en série, ni les erreurs, qui pénaliseraient encore
plus les 100 fichiers.

**Les règles visées :**
- un dossier par fonctionnalité ;
- un fichier = une idée (de 50 à 300 lignes environ) ;
- des noms qui disent le contenu ;
- peu de niveaux d'indirection ;
- la carte du repo dans `CLAUDE.md` ;
- des outils qui lisent fonction par fonction (Serena, LSP), pour que la taille d'un fichier
  compte moins.

## 4. Alléger (piste)

Retirer les dépendances et le code inutiles, **avec une preuve que le comportement ne change
pas** : le « compresseur ». Moins de code et moins de dépendances, c'est moins d'entretien et
moins de surface d'attaque.

**Pourquoi maintenant :** écrire du code ne coûte presque plus rien. Tout le monde en conclut
qu'il faut en produire plus. L'inverse est moins évident : le problème devient sa masse. Chaque
ligne reste à relire, à maintenir et à sécuriser, et les agents en produisent comme jamais.

**La forme visée**, dans l'esprit d'uv :
- une commande, qui répond par exemple « −22 % de lignes, −9 dépendances, comportement
  identique » et propose les suppressions ;
- Python d'abord, comme ruff et uv ;
- des preuves graduées (vérificateur de types, puis tests, puis comparaison du comportement) :
  une suppression non prouvée n'est pas appliquée ;
- le remplacement de dépendances en second temps : c'est le plus spectaculaire, mais le plus
  risqué.

**Ce qui existe déjà :**
- des détecteurs : deptry, FawltyDeps, knip, vulture ;
- SCARF, l'outil interne de Meta, qui a supprimé plus de 100 millions de lignes, mais qui n'est
  pas ouvert ;
- des recherches de 2026 :
  - TRIM (Columbia et DeepMind) : −18 à −33 % de modifications superflues dans le code des
    agents ;
  - « Software Supply Chains are Dead » (Singla et Davis) : une dépendance remplacée par le seul
    morceau utilisé, avec 99,8 % du comportement observé conservé ;
  - Lexo : la même idée, contre les attaques de la chaîne d'approvisionnement ;
- ponytail, qui agit à l'écriture : il fait écrire moins de code aux agents (−54 % annoncés).

Aucun outil ouvert ne retire du code existant avec une preuve.

**Le typage est un allié, pas un frein.**
- Le vérificateur de types est la preuve la moins chère : supprimer une fonction encore utilisée
  est signalé avant même les tests.
- Les types suppriment aussi du code défensif (vérifications de type, validations répétées).
- Ordre à suivre : typer d'abord, compresser ensuite.
- Seule la gymnastique de types (génériques imbriqués, types calculés) serait contre-productive.

**La vraie mesure n'est pas le nombre de lignes, mais la surface à relire**, c'est-à-dire le
nombre d'états possibles. Compression et typage la réduisent tous les deux.

**Compresser n'optimise pas forcément.**
- Ce qu'on gagne : retirer des dépendances allège l'installation, les bundles et le démarrage.
- Le piège : une dépendance réécrite est souvent moins optimisée que la bibliothèque éprouvée.
- Compresser n'est pas minifier : seul le code plus court *et* aussi clair a de la valeur.

**La robustesse dépend de la preuve.** Moins de code, c'est moins de bugs possibles et moins de
portes d'entrée pour un attaquant. Mais deux pièges :
- le code « mort » qui ne l'est pas : un chemin rare, une gestion d'erreur ;
- l'équivalence « observée par le repo », qui ne couvre que ce que les tests exercent.

**À ne jamais réécrire :** cryptographie, parseurs, fuseaux horaires, Unicode.

**Mesurer la charge d'entretien.** Combien de versions de dépendances un repo devra absorber par
an, combien seront cassantes, quelles fins de vie arrivent. libyear mesure le retard accumulé ;
ici, on mesure ce qui arrive, et on montre comment retirer des dépendances le fait baisser.

## 5. Versions : déléguées

Dependabot ou Renovate font ce travail. kiln vérifie seulement qu'ils sont en place et bien
réglés, quarantaine des nouvelles versions comprise.

## Sources

**Alléger (compresseur) :**
- [Meta, suppression automatique du code mort (SCARF)](https://engineering.fb.com/2023/10/24/developer-tools/automating-dead-code-cleanup/)
- [TRIM](https://arxiv.org/abs/2607.18161)
- [« Software Supply Chains are Dead »](https://arxiv.org/abs/2607.13021)
- [Lexo](https://arxiv.org/abs/2510.14522)

**Lisibilité par les agents :**
- [Étude de Sonar](https://www.developersdigest.tech/blog/code-cleanliness-affects-ai-coding-agents)
- [ETH Zurich, AGENTS.md](https://iclr.cc/virtual/2026/10021142)
- [Tranches verticales et IA](https://jeremydmiller.com/2026/06/04/the-codebase-is-the-prompt-wolverine-vertical-slices-and-ai-assisted-development/)
- [Structurer un repo pour les agents](https://deska.dev/blog/agent-friendly-codebase)

**Entretien :**
- [Build once, maintain forever](https://expressionsofchange.org/build-once-maintain-forever)
- [Designing low-upkeep software](https://lesswrong.com/posts/SAAZa8YzavnzHyGaB)
