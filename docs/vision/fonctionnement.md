# kiln : comment ça marche

> Partie de [l'idée de projet](README.md). Brouillon interne du 17 octobre 2026.

## Comment ça marche : le script trouve, Claude juge

On ne peut pas tout vérifier en dur. Savoir si un nom dit vraiment ce qu'il contient, ou si une
architecture convient au métier, demande du jugement. Et il est même prouvé qu'aucun programme
ne peut décider si un autre programme est correct (théorème de Rice). À l'inverse, confier toute
la vérification à Claude coûterait une fortune : lire une seule fois le code Python du repo d'association
(48 616 lignes hors tests) représente environ 500 000 jetons (environ 2 $ au tarif d'Opus 5.5, rien que pour la lecture). D'où un fonctionnement en cinq
temps, où l'essentiel ne coûte rien :

1. **Audit déterministe (aucun jeton).** Des scripts, des linters et des API publiques mesurent le
   repo face à la grille : présence des pratiques, normes de code, fins de vie, vulnérabilités.
   C'est ce qui a mesuré le repo d'association et le repo d'université le 17 octobre, en quelques secondes chacun. On
   obtient un score par pilier et la liste des écarts ; pour chaque écart, pourquoi c'est mieux,
   pour qui, et l'effort à prévoir. La commande s'appelle `kiln score` (décidé le 17 octobre
   2026 : elle dit ce qu'on obtient, un chiffre à partager ; « audit » appartient aux outils de
   vulnérabilités), et les corrections du temps 2 `kiln fix`.
2. **Corrections mécaniques (aucun jeton).** Ce qui se corrige par un programme est corrigé par un
   programme, sur une branche : `ruff --fix`, quarantaine des versions, actions épinglées par
   empreinte, utilisateur non-root, passage à uv… Ce sont les conversions de `kiln update`.
3. **Feuille de route pour Claude (jetons ciblés).** Reste ce qui demande du jugement : découper
   un fichier de 3 000 lignes, renommer avec sens, écrire des tests, corriger un typage strict.
   Claude reçoit une liste courte, avec pour chaque point l'emplacement, la règle et son pourquoi.
   Il n'ouvre que ces endroits. C'est là que se fait l'essentiel de l'économie : la
   plupart des jetons d'un agent partent dans l'exploration, c'est-à-dire lire le repo pour
   trouver quoi faire. La feuille de route la supprime : Claude ne paie plus pour chercher,
   seulement pour réfléchir.
4. **Vérification par le script.** Les mêmes scripts repassent : un écart n'est clos que s'il
   disparaît de la mesure et que tests, types et CI restent au vert.
5. **En continu.** Chaque version de kiln met la grille à jour, et `kiln update` y fait passer les
   repos ; les candidates tournent d'abord sur le canal `internal`. Les corrections que Claude a
   faites plusieurs fois deviennent de nouvelles conversions écrites en dur.

**Pour un repo que kiln n'a pas créé :** d'abord `kiln adopt`, puis un filet de tests qui fige le
comportement actuel, avant toute modernisation.

**Répartition des contrôles :**

| Type de contrôle | Exemples | Qui le fait | Coût en jetons |
|---|---|---|---|
| Détection mécanique | lockfile absent, conteneur en root, actions non épinglées, Node en fin de vie, fonction de plus de 30 lignes, module hors snake_case, annotation manquante | script | aucun |
| Correction mécanique | imports triés, syntaxe modernisée, quarantaine, épinglage, utilisateur non-root, passage à uv | script (conversion) | aucun |
| Détection approximative | nom générique, fichier qui fait plusieurs choses, SQL construit par chaînes | le script signale, Claude confirme | faible, ciblé |
| Jugement | découper, nommer, choisir une structure, écrire des tests, typage strict | Claude, guidé par la feuille de route | moyen à fort, mais ciblé |
| Décision | adopter une méthode, accorder une exception, choisir un profil | humain, selon la doctrine | aucun |

## Le circuit : les mises à jour descendent, les manques remontent

**Vers le bas.** Chaque version de kiln (grille, conversions, skills) descend vers tous les repos
par `kiln update`, en passant d'abord par les candidates du canal `internal`.

**Vers le haut.** Quand kiln tourne chez un utilisateur, l'audit repère deux choses : ce que la
grille ne connaît pas (un outil, une structure, une pratique non classée) et les règles qui gênent
à tort (faux positifs, dérogations fréquentes). Claude rédige alors la remontée vers le repo de
kiln avec la skill `/kiln:report`, qui fait déjà ce travail pour les défauts de kiln.

C'est ce circuit qui tient la grille à jour « par rapport au monde entier » : chaque installation
devient un capteur.

**Règles du circuit (décidées ici, à valider) :**
1. **Jamais sans accord.** L'utilisateur voit exactement ce qui part, et dit oui. Aucune remontée
   silencieuse : les développeurs rejettent la télémétrie cachée.
2. **Anonymisée.** Ni code, ni chemins, ni noms internes, ni secrets : seulement la signature du
   manque, par exemple « Django + django-q : planificateur non couvert par la grille ».
3. **Une issue par manque, pas une par utilisateur.** Avant d'en créer une, kiln cherche la
   signature parmi les issues ouvertes ; si elle existe, il y ajoute une voix de plus. L'issue est
   la règle. Une PR n'est ouverte que si la correction est évidente et locale, comme le fait déjà
   `/kiln:report`. Toute PR venue de l'extérieur passe par `/kiln:contribution` (contrôle de
   sécurité, relecture).
4. **Un signal, pas une décision.** Le nombre de remontées ne suffit pas à faire entrer une
   pratique dans la grille, sinon on pourrait l'empoisonner à coups de fausses remontées. C'est
   la doctrine qui décide : maturité, sources.
5. **Du signal au backlog.** Les manques remontés deviennent des tickets de `docs/backlog/`, et
   les plus fréquents passent en premier.

## Les tests : un maximum de tests pour un minimum de jetons

Demander tous les tests à Claude coûte cher en jetons. La doctrine s'applique donc ici aussi :
1. les générateurs sans modèle d'abord ;
2. Claude seulement sur les trous ;
3. un filtre automatique qui ne garde que les tests utiles.

C'est l'approche de Meta : avec son outil ACH, les ingénieurs ont accepté 73 % des tests générés.

**Les générateurs sans modèle (aucun jeton) :**

| Outil | Ce qu'il génère | Cible dans Django et Nuxt |
|---|---|---|
| Schemathesis | Des milliers de cas de test tirés du contrat OpenAPI | L'API Django Ninja, déjà couverte ainsi dans le repo d'association |
| Hypothesis (`hypothesis write`) | Des tests de propriétés, à partir des signatures de fonctions | Les calculs purs : prix, remises, dates. D'après une étude publiée, 18 % de ses tests sont utilisables tels quels, 30 % à adapter, 52 % inutilisables |
| CrossHair | Par exécution symbolique, les entrées qui passent par chaque chemin d'une fonction | Mêmes cibles. Sert aussi de moteur à Hypothesis |
| Pynguin | Des tests pytest complets, trouvés par recherche automatique | Le code pur. Peu adapté à Django, à cause de la base de données et des effets de bord |
| Keploy | Des tests d'API et des simulacres, tirés du trafic réel enregistré | Rejouer de vrais parcours contre chaque nouvelle version |
| Tests d'instantané (syrupy, Vitest) | Le comportement actuel, figé | Les tests de caractérisation, avant de moderniser un vieux repo |
| Enregistreur de Playwright | Un test de bout en bout, enregistré en cliquant dans le navigateur | Les parcours Nuxt |

**Les générateurs avec un LLM :**
- **CoverUp**, outil de recherche guidé par la couverture : 89 % de couverture des lignes et des
  branches sur son banc d'essai, contre 77 % pour MuTAP ;
- **Qodo Cover** (open source, peu actif depuis avril 2026) et **Qodo Gen** (payant) ;
- **ACH, chez Meta**, guidé par des mutants (des bugs introduits volontairement) ;
- **Claude Code** lui-même.

Les meilleurs filtrent : un test n'est gardé que s'il passe de façon fiable et qu'il couvre du
code nouveau ou détecte un mutant.

**La recette de kiln, en cinq temps :**
1. **Générer sans modèle** (aucun jeton) : Schemathesis pour l'API, Hypothesis et CrossHair pour
   les calculs, instantanés pour figer l'existant, Playwright pour les parcours.
2. **Mesurer les trous** (aucun jeton) : couverture des lignes et des branches, tests de mutation
   (mutmut pour Python, Stryker pour TypeScript). On obtient la liste exacte des lignes non
   couvertes et des mutants qui survivent.
3. **Claude écrit seulement les tests manquants**, à partir de cette liste. Il n'explore pas le
   repo, donc les jetons restent ciblés.
4. **Filtrer automatiquement** (aucun jeton) : un test n'est gardé que s'il passe cinq fois de
   suite, et qu'il améliore la couverture ou tue un mutant. Le reste est jeté sans relecture.
5. **Cliquet** : la couverture et le nombre de mutants survivants ne peuvent que s'améliorer.

**La limite qu'aucun outil ne lève :** un test généré vérifie ce que le code *fait*, pas ce qu'il
*devrait* faire, et un instantané fige aussi les bugs. Pour les règles métier, quelqu'un doit dire
ce qui est attendu. C'est là que les tests de propriétés valent le plus : ils écrivent
l'invariant, pas un exemple. C'est aussi pourquoi on juge les tests au nombre de mutants tués
plutôt qu'à la couverture : on peut gonfler une couverture avec des tests qui ne vérifient rien.

## Sources

**Tests :**
- [CoverUp (ACM)](https://dl.acm.org/doi/10.1145/3729398)
- [Meta, génération de tests guidée par les mutants](https://arxiv.org/pdf/2501.12862)
- [Hypothesis, `hypothesis write`](https://hypothesis.readthedocs.io/en/latest/ghostwriter.html)
- [Étude sur les tests générés par Hypothesis](https://homepages.dcc.ufmg.br/~mtov/pub/2027-esem-pbt-python.pdf)
- [hypothesis-crosshair](https://github.com/pschanely/hypothesis-crosshair)
- [Pynguin](https://arxiv.org/pdf/2007.14049)
- [Keploy](https://keploy.io/docs/concepts/what-is-keploy.md)
- [Outils de génération de tests en 2026](https://dev.to/rahulxsingh/best-ai-test-generation-tools-in-2026-complete-guide-4o2p)
