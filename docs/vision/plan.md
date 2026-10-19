# kiln : risques, validation et prochaines étapes

> Partie de [l'idée de projet](README.md). Brouillon interne du 17 octobre 2026.

## Pistes écartées en route, et pourquoi

| Piste | Pourquoi elle est écartée |
|---|---|
| « Harness mesuré » (mesurer la configuration d'un agent) | C'est un produit centré sur les agents, ce qui n'est pas notre sujet, et c'est en partie le terrain d'Anthropic |
| « Dependabot pour la configuration Claude Code » | `/doctor` de Claude Code le fait déjà depuis juillet 2026 |
| Simple entretien des petites applications | Élargi : entretenir *et* moderniser |
| Versions | Secondaires, Dependabot et Renovate le font |

**Idées en réserve :**
- **Les forks vivants.** On garde ses modifications sous forme d'intentions accompagnées de tests,
  et elles sont réappliquées à chaque nouvelle version amont. C'est `kiln update` généralisé à
  n'importe quel logiciel open source.
- **Une garantie financière sur le code fusionné** : la confiance devient un produit assuré.
- **Un benchmark public « Claude Code avec et sans kiln »** (CI rouges, jetons, règles
  enfreintes), qui pourrait servir de preuve au lancement.

## Risques et questions ouvertes

1. **Les géants occupent le haut du marché.** AWS a lancé la même promesse en juin, pour les
   grandes entreprises.
2. **La grille est un travail sans fin.** Le périmètre de départ (Django et Nuxt) la rend
   tenable, et le circuit de remontées la nourrit.
3. **Les agents rendent l'application d'un changement facile pour tous.** La valeur est dans le
   choix et la preuve, pas dans l'application.
4. **« Le meilleur » dépend du contexte.** Il faut des profils de structure.
5. **Les vieux repos sans tests** : les moderniser à l'aveugle les casse. Il faut d'abord un filet
   de tests.
6. **Les outils d'entretien font peu d'étoiles** (deptry tourne autour de 1 000). Il faut un chiffre
   spectaculaire, par exemple un score avant/après.
7. **Le nom** : collision avec Kiln-AI, et `kiln` est pris sur PyPI (le paquet s'appelle
   `kiln-cli`).
8. **L'hypothèse des petits fichiers** n'est pas prouvée : il faut la mesurer.
9. **Les remontées** posent des questions de vie privée, de bruit et d'empoisonnement de la
   grille. Voir les règles du circuit dans [comment ça marche](fonctionnement.md).

## Plan de validation : des preuves avant de construire

1. **La douleur.** C'est fait sur deux repos : le repo d'association (le haut du panier, 58 % des pratiques
   appliquées) et le repo d'université (repo ordinaire, en retard sur presque tout). À élargir à 5 ou
   10 repos publics typiques.
2. **La lisibilité par Claude.** Test A/B sur une fonctionnalité du repo d'association, découpée ou non : les
   dix mêmes tâches confiées à Claude Code, en comparant les jetons consommés et les réussites.
3. **La solution.** Sur une copie locale du repo d'université, appliquer cinq conversions mécaniques
   (lockfile, ruff, utilisateur non-root, images épinglées, CI minimale) et mesurer le score
   avant et après.
4. **L'intérêt.** Publier le chiffre (« X % des pratiques de référence absentes dans un repo
   d'université typique ») et mesurer les réactions.
5. **Les tests au moindre coût.** Sur une copie locale du repo d'association : `core/money.py` laisse
   3 mutants survivants sur 16. On fait écrire à Claude uniquement les tests qui les tuent, et on
   compte les jetons consommés.

On continue si chaque étape donne un chiffre net.

## Prochaines étapes

1. **Classer tout le repo d'association sur les deux axes** : les 108 règles nommées, les 15 piliers, et ce qui
   vit hors de la charte.
2. **Écrire la grille en données**, dans un format lisible par une machine : pour chaque règle,
   son thème, sa portée, ses attributs, son détecteur et son correcteur.
3. **Amener le modèle Django + Nuxt de kiln au niveau maximal de la grille**, puis faire converger
   le repo d'association par `kiln update`, en mesurant son score à chaque version.
4. **Étendre `/kiln:report` aux manques de la grille**, selon les règles du circuit ([comment ça marche](fonctionnement.md)).
5. **Mener les étapes 2 à 4 du plan de validation.**
6. **Nommer la commande d'audit.**

## Le plan daté (17 octobre 2026)

Les prochaines étapes sont devenues les tickets de `docs/backlog/backlog.md`, réécrit ce jour
d'après cette vision, avec un plan daté jusqu'au lancement :

| Étape | Tickets | Version prévue |
|---|---|---|
| 1. Classer le repo d'association | T-124 | v0.4.1, jeudi 22 octobre |
| 2. La grille en données | T-123, T-125 | v0.4.1 et v0.4.2 |
| 6. La commande d'audit | `kiln score` (T-46), `kiln fix` (T-126 à T-128) | v0.4.2 et v0.4.3 |
| La feuille de route pour Claude | `kiln score --roadmap`, `/kiln:modernize` (T-129) | v0.4.4 |
| 3. Le modèle au sommet de la grille | T-130 ; kiln lui-même : T-90 | v0.4.4 |
| En continu | kiln-bot (T-59), score du repo d'association à chaque version (T-134) | v0.4.5 |
| 4. `/kiln:report` et les manques | T-38 | v0.4.5 |
| 5. Validation, étapes 3 et 4 | T-131 (deux repos réels), T-132 (une centaine de repos publics) | v0.5.0 |
| 5. Validation, étape 2 | T-53 (test A/B de lisibilité), si le budget le permet | v0.5.1 |
| Validation, étape 5 ; tests au moindre coût | T-135, T-136 | v0.6.0 |
| Alléger (piste) | T-138, puis T-139 si le chiffre est net | v0.6.1 |

**Le lancement** : mercredi 11 novembre 2026 à 16 h (heure de Paris), sur tous les forums le
même après-midi, seulement une fois la v0.5.0 promue et la barre de T-03 tenue le lundi 9 à
20 h ; sinon le mercredi suivant. **Le budget** : kiln se développe avec un seul forfait Claude
Code Pro ; les efforts se comptent en heures de session (le quota de la semaine en a tenu 33 à
42 en octobre), et il faut environ 27 heures pour atteindre la v0.5.0.
