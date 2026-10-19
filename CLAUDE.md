# kiln — consignes de travail

L'atelier de Claude Code : savoir, garde-fous, façons de travailler et mise à jour des repos
(modèle Copier, commande `kiln`, moteur `charte`, plugins Claude Code, workflows
réutilisables). Tout ce qui est générique aux repos vit ici : un défaut d'un fichier
généré se corrige dans `template/`, puis `kiln update` dans le repo. Présentation complète et
commandes dans [`README.fr.md`](README.fr.md) (vitrine en anglais :
[`README.md`](README.md)).

## Carte du repo

Où chercher, pour ne pas explorer ; à tenir à jour dans le commit qui ajoute, déplace ou retire
un dossier ou un module.

- `src/kiln/` : la commande. `cli.py` (arguments ; anciens noms de 0.3 acceptés par `modernize`) ; une commande par module : `new.py` (questions de `questions.py`),
  `adopt.py` (`kiln adopt`, repo existant), `install.py`, `dev.py`, `check.py`, `settings.py` (`kiln set`, clés réglables), `machine.py` (`kiln set` hors d'un repo : réglages du poste), `waive.py` (`kiln waive`), `update.py`,
  `contract.py`, `release.py` (`kiln version`), `shipping.py` (`kiln version cut` et `promote`), `github_ci.py` (verdict de la CI de GitHub sur un commit, attendu par `cut` et `promote`), `doctor.py` (diagnostic du poste et du repo), `fleet.py` (`status`, `update --all`), `rehearsal.py` (`kiln update --rehearse`, la mise à jour sur un clone jetable) ; socle : `stack.py` (stack lue dans
  `.copier-answers.yml`), `template.py`, `deps.py`, `github.py`, `rules.py` (règles non
  vérifiées), `statusline.py`, `versions.py` (tags, journal des versions), `frozen.py` (fichiers figés par `kiln-waivers.toml`, épargnés par `update`), `renames.py` (noms d'avant 0.4.0 et leurs noms anglais), `banner.py` (bannière, écran d'accueil), `ui.py` (palette pierre et feu, étapes,
  roue animée, bilan, succès, erreurs), `shell.py`, `config.py` (`~/.config/kiln/config.toml`).
- `src/kiln/ci/` : `kiln ci` (CI rejouée sur le poste, verdict en note git) ;
  `src/kiln/charter/` : moteur de `charter` (`bans.py`, `ratchets.py`,
  `python_tools.py`, `waivers.py` : dérogations de `kiln-waivers.toml`).
- `hatch_build.py` : grave dans le paquet le commit d'où il est construit (`kiln/_build.json`, lu par `versions.py`).
- `copier.yml` : questions du modèle ; `template/` : le modèle (`CLAUDE.md.jinja`, consignes
  pour Claude dans `.claude/rules/kiln/` : projet, charte, une par stack ;
  `.claude/settings.json.jinja`, CI…) ; `macros.jinja`.
- `plugins/` : plugins Claude Code, catalogue `.claude-plugin/marketplace.json` (avec
  `renames` : anciens noms `base`, `pile-django`, `pile-nuxt`, `vps-podman`) ; `kiln/` (skills
  `worktree`, `merge`, `release`, `cleanup`, `review` (commits et diff d'une branche avant la
  fusion, dépôt entier avant une version), `backlog`, `update`, `adopt`, `report` (défaut de kiln
  remonté en issue ou PR), `token` (jeton d'un service dans `.<service>/`), `contribution` (PR
  d'un contributeur extérieur), `good-first-issues` ; `hooks/` (dont `reminders.py`, espacement
  des questions de mise à jour, et `first_prompt.py`, logo de kiln et nouveautés au-dessus de la
  question) ; `scripts/statusline.py`), `django/`, `nuxt/`, `vps/`,
  `stripe/`, `serena/` ; `base/` : renvois des anciens chemins des hooks et scripts (sessions ouvertes, status line).
- `.github/workflows/` : workflows réutilisables appelés par les repos générés, plus ceux de
  kiln (`kiln.yml` contrôles, `pypi.yml` publication du paquet `kiln-cli` au tag promu) ;
  `actions/` : actions composites (`charter`, son ancien nom `charte`, `services`).
- Vitrine publique, en anglais : `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `LICENSE`
  (MIT), `.github/ISSUE_TEMPLATE/`, `.github/pull_request_template.md` ; capture de l'écran
  d'accueil `docs/assets/kiln-home.svg` (régénérée par `scripts/home_screenshot.py`, vérifiée par `test_docs.py`). Référence complète en français : `README.fr.md`.
- `docs/backlog/` : suivi du travail, en anglais (skill `/kiln:backlog`), dont la prochaine
  promotion de version ; `docs/assets/` : images de la vitrine ; `docs/vision/` : l'idée de
  projet, brouillon en français, un fichier par sujet (`README.md` sert d'index).
- `scripts/home_screenshot.py` : régénère la capture de l'écran d'accueil du README.
- `tests/` : `test_template.py` (rendu du modèle pour chaque stack), `test_cli.py` (la commande :
  accueil, erreurs, bilan, sorties hors terminal, anciens noms), `test_questions.py` (questions de `kiln new`), `test_unites.py`,
  `test_ci.py`, `test_flotte.py`, `test_waivers.py` (dérogations), `test_waive.py`, `test_charter_file.py` (`charter file`, hook après une édition), `test_shipping.py` (`kiln version cut` et `promote`), `test_rehearsal.py` (`update --rehearse`), `test_e2e.py` (de bout en bout, `-m e2e` : chaque version depuis v0.3.0 par un outil installé, et le repo-témoin `antoine-tena/kiln-rehearsal`, figé à v0.3.3-rc.2, ne jamais le mettre à jour), `test_deployment.py`, `test_statusline.py` (choix du
  poste et rendu du script), `test_plugins.py` (skills cités présents, nommés comme leur dossier), `test_docs.py` (vitrine à jour : capture d'accueil, plugins et workflows cités), `test_branch_guard.py` (hook de garde de branche), `test_adopt.py`,
  `test_reminders.py`, `test_session_start.py` ; `conftest.py` : config git du poste écartée, identité de test.

## Repos d'entraînement

kiln s'entraîne sur deux repos réels mesurés le 17 octobre 2026 : le repo d'association (la
référence Django + Nuxt, terrain d'entraînement de la grille, T-124, T-134 ; son chemin est dans
les consignes globales du poste, jamais nommé ici) et un repo d'université (repo ordinaire, épreuve pour un repo que kiln n'a pas
créé, T-131). **Le détail des mesures n'est pas public** (écarts de sécurité d'un site en production,
vulnérabilités d'un projet tiers pas encore signalées à son équipe) : il est dans le
dépôt **privé** `antoine-tena/kiln-private` (`~/code/kiln-private`,
`mesures-repos-entrainement.md`), jamais dans kiln, ni sur une branche, ni dans un commit. N'écrire
dans le repo public que des chiffres agrégés, sans rien qui identifie le projet d'université. On mesure toujours sur une copie locale, jamais dans le repo lui-même.

## Versions

**Pourquoi** (choix d'antoine, 15 octobre 2026) : kiln doit rester stable pour les repos qui en
dépendent, alors qu'il change beaucoup ; d'où une version qui ne sort que quand la suivante est
prête ici, en candidate sur ses propres repos (`-rc`, comme Python ou Linux) : pas de délai
fixe, c'est la suivante prête qui évite le correctif d'urgence (précisé par antoine le
16 octobre 2026), et le 0.x du semver, prévu pour un début où tout peut casser (comme uv ou ruff), plutôt
qu'un quatrième chiffre. Les clients se mettent à jour à chaque version, correctif compris.
Suivi de ce qui reste : `docs/backlog/backlog.md`.

**Numérotation** (choix d'antoine, 16 octobre 2026) : comme Claude Code (2.1.301 en octobre
2026), pas comme Vercel CLI (64 majeures, un numéro qui ne dit plus rien). Personne ne dépend de
kiln par une plage de versions (`^0.3`) : les repos citent ses workflows au tag exact et
n'avancent que par `kiln update`, qui convertit ce qui casse. Le numéro date une version ; c'est
la note de version qui dit ce qui change. De Next.js, on prend la discipline (candidates,
changements cassants en tête des notes, migration automatique), pas la numérotation.

**Rythme** (choix d'antoine, 17 octobre 2026) : **une version tous les deux jours**. kiln se
développe avec un seul forfait Claude Code Pro, dont le quota de la semaine repart le mardi à 8 h
(heure de Paris) : il a tenu 42 heures de session la semaine du 6 octobre et 33 celle du 13 octobre
(limite atteinte le vendredi à 14 h 03), tous projets confondus, et une fenêtre de 5 heures
s'épuise en 2 h à 3 h 30 de travail. Les efforts des tickets se comptent donc en temps de session
Claude Code (XS moins d'un quart d'heure, S une demi-heure, M une heure, L deux à trois heures),
mesuré sur kiln : le 16 octobre, 9,3 heures de session ont livré quatre promotions et le passage à
l'anglais, une vingtaine de fois les anciennes estimations en temps humain (antoine, 17 octobre
2026 : un forfait Pro, et il code très vite avec Claude Code). kiln planifie sur 25 heures de
session par semaine, soit environ 7 par version, quota lissé sur la semaine (environ 5 heures par
jour, tous projets) : épuisé le vendredi, il laisse sans budget les versions du samedi et du lundi.
Le second jour d'une version absorbe les dépassements et laisse la candidate tourner sur le canal
`internal` avant sa promotion (promue 45 minutes après sa sortie, une candidate n'a rien vérifié).
Ce qui évite de déranger les utilisateurs, c'est de grouper la question : `kiln update` passe d'un
coup toutes les versions en retard (une note par version traversée), le rappel en session ne
revient qu'au rythme réglé par `kiln set update-reminders` (une fois par semaine par défaut, T-45),
et kiln-bot (T-59) rendra la mise à jour gratuite. Les changements cassants restent groupés aux
étapes ; une faille de sécurité sort tout de suite.

`vMAJEUR.MINEUR.CORRECTIF`. En 0.x (aujourd'hui) :
- **chaque version monte le correctif**, nouveautés et changements cassants compris (`v0.3.1`,
  `v0.3.2`… `v0.3.192` s'il le faut) ;
- **la mineure ne monte que pour une étape** décidée par antoine (par exemple kiln tout en
  anglais) : `kiln version --minor` ; Claude peut la proposer quand un groupe de tickets
  forme une étape (permis par antoine le 16 octobre 2026), jamais la décider ;
- **étapes décidées** (antoine, 16 octobre 2026) : v0.5.0 lancement public, v0.6.0 Claude
  travaille seul dans le repo, v0.7.0 kiln pour les équipes et les organisations, v1.0.0 promesse
  de stabilité, juste avant les modules de la communauté (T-69) qui s'appuieront sur l'API de
  kiln ; le plan de `docs/backlog/` les porte. Leur contenu suit la vision du 17 octobre 2026
  (`docs/vision/`, brouillon en français) : v0.5.0 note n'importe quel
  repo Django ou Nuxt face à la grille et le corrige par script, v0.6.0 Claude comble seul les
  écarts que le script laisse, v0.7.0 profils de structure et flottes de repos (associations,
  universités, PME ; pas encore les grandes entreprises), v1.0.0 format de la grille stable pour
  les paquets de règles de la communauté ;
- **lancement public** (date fixée le 17 octobre 2026 à la demande d'antoine) : **mercredi
  11 novembre 2026 à 16 h** (heure de Paris), sur tous les forums le même après-midi (T-03),
  seulement si la v0.5.0 est promue et que la barre de T-03 tient le lundi 9 novembre à 20 h ;
  sinon le mercredi suivant, même heure. La date bouge, jamais la barre ;
- **ce que seul l'utilisateur peut compléter** après une mise à jour (une information que kiln
  ne devine pas, comme le login GitHub de chacun) s'écrit au commit, dans une ligne du corps
  `After updating: …` : `kiln version cut` la reprend dans la note (`- **After updating**: …`)
  et `kiln update` en fait, dans chaque repo, un ticket 🔴 « Finish the kiln update to vX.Y.Z »
  de `docs/backlog/backlog.md`, que `/kiln:update` traite avec l'utilisateur juste après la
  fusion (souhait d'antoine, 19 octobre 2026 : une tâche de la mise à jour, pas `urgent.md`) ;
- **un changement cassant** reste marqué au commit (`feat!:` ou `BREAKING CHANGE`), ouvre la
  note de version dans `CHANGELOG.md`, et livre sa conversion dans `kiln update`. Est cassant
  ce qui touche l'API publique de kiln : commandes et options de la CLI, questions de
  `copier.yml`, arborescence générée, entrées des workflows et actions réutilisables, noms des
  skills et hooks, identifiants de règles de la charte.

À partir de 1.0 (l'engagement de stabilité public, plus tard), semver strict comme Next.js :
cassant → majeure (rare et planifiée), `feat` → mineure, le reste → correctif. `kiln version`
(module `release.py`) propose le numéro et dit quelles candidates sont prêtes.

Deux temps, par la skill `/kiln:release` (pas de déploiement : le tag publie, et le tag promu
publie sur PyPI le paquet `kiln-cli` par `pypi.yml`) :
1. **Candidate** : branche `release/vX.Y.Z` tirée de `develop`, entrée `## vX.Y.Z — date` en tête
   de `CHANGELOG.md`, `version = "X.Y.Z"` dans `pyproject.toml`, contrôle complet (les trois
   commandes ci-dessous), branche poussée, **CI de GitHub attendue sur son commit** (macOS et
   tests de bout en bout, qui ne tournent que là : la rc.1 de la v0.4.0 était sortie sur un rouge
   que personne n'avait lu), tag `vX.Y.Z-rc.1` poussé seulement au vert. Les postes au canal `internal` (`kiln set
   channel=internal`, celui d'antoine) la suivent : `kiln update --all` y fait passer tous les repos
   générés. Un correctif de la candidate : commit `fix:` sur sa branche, tag `-rc.N+1`.
2. **Promotion**, quand `kiln version` la dit prête (une candidate plus récente existe, sans
   délai d'attente, et la CI de GitHub de la candidate est verte) : tag `vX.Y.Z` sur le commit exact de sa
   dernière candidate, fusion dans `main`, reversement dans `develop`, puis `kiln update --all --rehearse` (chaque repo répété sur un clone) et, au vert, `kiln update --all`.
   Le canal `public` (par défaut) ne voit que ces versions.

Chaque version, correctif compris, finit par `kiln update --all` : les repos générés citent leurs
workflows au tag exact dont ils partent (`ci.yml`), et `kiln update` le fait avancer. Les
workflows de kiln prennent leurs actions et la commande `charte` à leur propre commit
(`job.workflow_sha`). Les dépôts adoptés citent les workflows au tag
de la dernière version publique (choix d'antoine, 19 octobre 2026, T-04) et ne reçoivent pas de
`kiln update` : le tag y avance à la main tant que T-146 n'est pas fait. Modules : `versions.py` (tags, canaux, journal, version de
l'outil), `release.py` (`kiln version`), `shipping.py` (`kiln version cut`, `kiln version promote`).

## Contrôles

`uv run pytest -q` (réparti sur tous les cœurs par pytest-xdist : une vingtaine de secondes ;
`-n 0` pour un seul processus, au débogage), `uv run ruff check`
et `uv run ruff format --check`. Le crochet pre-commit de kiln (`.pre-commit-config.yaml`, posé par
`kiln install`) lance ruff à chaque commit et mypy avant chaque push. Le catalogue étant déclaré en dossier local sur le poste
d'antoine, les sessions ouvertes appellent les hooks et la status line **dans l'arbre principal**
(`~/code/kiln/plugins/…`) : un fichier retiré ou renommé casse aussitôt chaque session (hook
introuvable = outil bloqué). Un chemin de plugin qui change garde donc un renvoi à l'ancien
(`plugins/base/`, vérifié par `test_plugins.py`).
