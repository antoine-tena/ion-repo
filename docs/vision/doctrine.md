# kiln : la doctrine

> Partie de [l'idée de projet](README.md). Brouillon interne du 17 octobre 2026.

Il existe une façon de coder, de mener un repo et de mener un projet : celle que kiln tient pour
le meilleur possible. On la suit. La charte du repo d'association en est la base de départ ; ensuite, la
référence est ce qui sort dans le monde, trié par les principes ci-dessous.

Les précédents montrent que cette posture gagne :
- gofmt : « le style de gofmt n'est le préféré de personne, mais gofmt est le préféré de tous » ;
- Black, « le formateur sans compromis » ;
- Prettier, qui impose ses choix ;
- Rails, « la convention plutôt que la configuration » ;
- et à l'inverse, create-react-app, figé puis abandonné en 2025, montre ce qui arrive quand la
  façon unique cesse d'évoluer.

1. **Une seule façon de faire, par profil.** Pour chaque stack et chaque taille de structure,
   kiln choisit une façon et la tient. Pas d'options : les choix sont faits pour toi. Une
   association n'a pas besoin des SLO d'une grande entreprise.
2. **Le meilleur, pas le plus récent.** Une pratique n'entre dans la façon kiln que lorsqu'elle est
   mûre : maintenue, adoptée, compatible avec le reste de la stack. Elle passe par quatre
   niveaux : évaluer, essayer, adopter, abandonner. Python 3.15 et ty sont sortis, ce n'est pas
   encore leur heure.
3. **Chaque règle a son pourquoi, sa source et sa date.** L'autorité vient des preuves, pas des
   goûts. Les sources se pèsent dans cet ordre, du plus fiable au moins fiable :
   1. la documentation officielle et les notes de version des mainteneurs ;
   2. les alertes de sécurité (OWASP, OpenSSF, CVE) ;
   3. les études mesurées ;
   4. les données d'adoption (enquêtes, téléchargements) ;
   5. les blogs.
4. **Chaque règle a sa place sur deux axes.** Son thème (structure, normes de code, tâches de
   fond, conteneurs, développement assisté…) et sa portée (universelle, langage, framework, outil,
   domaine métier, projet). Une règle universelle peut prendre un réglage de projet : « stocker
   les dates en UTC » est universel, « Europe/Paris » est un réglage du repo d'association. Le détail est dans
   [la grille de référence](grille.md).
5. **Le script d'abord, Claude ensuite.** Tout ce qu'un programme peut vérifier ou corriger, un
   programme le fait : c'est exact, reproductible, et ça ne coûte aucun jeton. Claude ne reçoit
   que ce qui demande du jugement, avec l'emplacement exact et la règle en cause. Il ne parcourt
   jamais le repo pour chercher les problèmes.
6. **Claude invente, le script répète.** Une correction que Claude fait deux fois de la même façon
   devient une règle ou une conversion écrite en dur. Claude peut l'écrire lui-même : son coût se
   paie une fois par règle, pas une fois par repo.
7. **Une règle imprécise est pire que pas de règle.** Une règle qui signale à tort coûte des
   jetons et de la confiance. Elle ne passe en strict qu'une fois ses faux positifs maîtrisés : sur
   le repo d'association, les « caractères ambigus » signalés par ruff étaient la typographie française.
8. **Rien sans preuve.** Une correction n'est proposée qu'avec ses preuves : tests, types et CI au
   vert, mesure avant et après.
9. **Des exceptions explicites, un chemin progressif.** Une dérogation est datée et justifiée
   (`kiln waive`). Un repo existant converge par cliquets, sans tout casser d'un coup.
10. **Lisible par Claude.** Un dossier par fonctionnalité, un fichier = une idée, des noms qui
    servent de sommaire, la carte du repo dans `CLAUDE.md`.
11. **Le plus rapide, à précision égale.** Un contrôle lent finit par ne plus être lancé. On
    prend les outils les plus rapides parmi ceux qui sont assez précis et mûrs. On ne recontrôle
    que ce qui a changé (cache, fichiers modifiés, parallélisme). Nos propres règles s'écrivent
    dans un format déclaratif, exécuté par un moteur rapide comme ast-grep (écrit en Rust). On
    n'écrit du Rust soi-même que là où une mesure montre que notre code ralentit. Mesuré sur
    le repo d'association : ruff 0,4 s, notre script de normes en Python 1,1 s, mypy 22,6 s, eslint 42,3 s. Le
    temps part dans les outils, pas dans notre code. Pistes :
    - oxlint là où il couvre les règles d'eslint : 2,7 s, mais avec moins de règles, et il couvre
      mal les gabarits Vue ;
    - TypeScript 7, au compilateur natif ;
    - ty ou pyrefly à la place de mypy, quand ils seront mûrs pour Django ;
    - ast-grep pour nos propres règles.
