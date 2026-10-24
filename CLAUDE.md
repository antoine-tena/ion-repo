# kiln — consignes de travail

L'atelier de Claude Code : savoir, garde-fous, façons de travailler et mise à jour des repos
(modèle Copier, commande `kiln`, moteur `charte`, plugins Claude Code, workflows
réutilisables). Tout ce qui est générique aux repos vit ici : un défaut d'un fichier
généré se corrige dans `template/`, puis `kiln update` dans le repo. Présentation dans
[`README.fr.md`](README.fr.md) (vitrine en anglais : [`README.md`](README.md)), tout le détail
dans [`docs/reference.fr.md`](docs/reference.fr.md) ([`docs/reference.md`](docs/reference.md)).

## Carte du repo

Où chercher, pour ne pas explorer ; à tenir à jour dans le commit qui ajoute, déplace ou retire
un dossier ou un module.

- `src/kiln/` : la commande. `cli.py` (arguments ; anciens noms de 0.3 acceptés par `modernize`) ; une commande par module : `new.py` (questions de `questions.py`),
  `adopt.py` (`kiln adopt`, repo existant), `install.py`, `dev/` (`kiln dev` : `processes.py` serveurs de la stack et `Procfile.dev`, `backing.py` bases du compose dans podman, `menu.py` quoi lancer et journaux proposés, `background.py` arrière-plan, `status`, `logs`, `stop`, `foreground.py` `--foreground`, `containers.py` `--containers`), `check.py`, `settings.py` (`kiln set`, clés réglables), `machine.py` (`kiln set` hors d'un repo : réglages du poste), `waive.py` (`kiln waive`), `update.py`,
  `contract.py`, `release.py` (`kiln version`), `shipping.py` (`kiln version cut` et `promote`), `github_ci.py` (verdict de la CI de GitHub sur un commit, attendu par `cut` et `promote`), `doctor.py` (diagnostic du poste et du repo), `tool_update.py` (mise à jour de l'outil proposée après une commande tapée hors de Claude Code), `fleet.py` (`status`, `update --all`), `adopted.py` (repo adopté : le tag des workflows de kiln avancé à la dernière version publique), `adopted_names.py` (repo adopté : ses noms de kiln 0.3 convertis par `kiln update`), `rehearsal.py` (`kiln update --rehearse`, la mise à jour sur un clone jetable) ; socle : `stack.py` (stack lue dans
  `.copier-answers.yml`), `template.py`, `deps.py`, `github.py`, `rules.py` (règles non
  vérifiées), `statusline.py`, `versions.py` (tags, journal des versions), `frozen.py` (fichiers figés par `kiln-waivers.toml`, épargnés par `update`), `renames.py` (noms d'avant 0.4.0 et leurs noms anglais), `banner.py` (bannière, écran d'accueil), `ui.py` (palette pierre et feu, étapes,
  roue animée, bilan, succès, erreurs), `shell.py`, `config.py` (`~/.config/kiln/config.toml`).
- `src/kiln/grid/` : la grille (T-123) : `rules/<thème>/<ID>.toml` une règle par fichier, `model.py` (format, listes fermées, validation), `facts.py` (de quoi est fait un repo), `detectors.py` (détecteurs déclaratifs, contrôles Python), `fixers/` (convertisseurs de `kiln fix` : `ci.py`, `python.py`, `containers.py`, `resolve.py` pour les SHA et empreintes en ligne), `fix.py` (`kiln fix`), `show.py` (`kiln grid`), `score.py` (`kiln score`, note d'un repo face à la grille), `roadmap.py` (`kiln score --roadmap`, `--rule`, `--write` : ce qui demande du jugement, pour Claude) ; chaque règle a un exemple qui passe et un qui échoue dans `tests/test_grid.py`.
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
  fusion, dépôt entier avant une version), `backlog`, `update`, `adopt`, `modernize` (écarts de la feuille de route comblés un à un), `report` (défaut de kiln
  remonté en issue ou PR), `token` (jeton d'un service dans `.<service>/`), `contribution` (PR
  d'un contributeur extérieur), `good-first-issues` ; `hooks/` (dont `reminders.py`, espacement
  des questions de mise à jour, et `first_prompt.py`, logo de kiln et nouveautés au-dessus de la
  question) ; `scripts/statusline.py`), `django/`, `nuxt/`, `vps/`,
  `stripe/`, `serena/` ; `base/` : renvois des anciens chemins des hooks et scripts (sessions ouvertes, status line).
- `.github/workflows/` : workflows réutilisables appelés par les repos générés, plus ceux de
  kiln (`kiln.yml` contrôles, `pypi.yml` publication du paquet `kiln-cli` au tag promu) ;
  `actions/` : actions composites (`charter`, son ancien nom `charte`, `services`).
- Vitrine publique : `README.md` (et sa traduction `README.fr.md`), `CONTRIBUTING.md`,
  `CODE_OF_CONDUCT.md` (Contributor Covenant 2.1), `SECURITY.md`, `LICENSE` (MIT),
  `.github/ISSUE_TEMPLATE/`, `.github/pull_request_template.md` ; référence complète
  `docs/reference.md` et `docs/reference.fr.md` ; images `docs/assets/` (dessinées par
  `scripts/screenshots.py`, vérifiées par `test_docs.py`), dont la démo animée
  `kiln-new.gif` enregistrée par VHS depuis `kiln-new.tape` et l'image de partage
  `social-preview.png` (déposée à la main dans les réglages de GitHub).
- `docs/backlog/` : suivi du travail, en anglais (skill `/kiln:backlog`), dont la prochaine
  promotion de version ; `docs/assets/` : images de la vitrine ; `docs/vision/` : l'idée de
  projet, brouillon en français, un fichier par sujet (`README.md` sert d'index).
- `scripts/screenshots.py` : dessine les images du README à partir des vraies sorties de kiln
  (et le logo, l'image de partage) ; `scripts/social_preview.py` : l'image de partage en PNG
  (Playwright) ; `scripts/demo_shell.sh` : le shell des démos enregistrées (kiln de ce dossier,
  sans numéro de version, dans un dossier jetable sur le disque) ; `scripts/refresh_images.py` :
  images de base du modèle épinglées au digest de leur tag (avant chaque candidate).
- `tests/` : `test_template.py` (rendu du modèle pour chaque stack), `test_cli.py` (la commande :
  accueil, erreurs, bilan, sorties hors terminal, anciens noms), `test_questions.py` (questions de `kiln new`), `test_new.py` (ce que `kiln new` dit à la fin), `test_grid.py` (la grille), `test_score.py` (`kiln score`), `test_fix.py` (`kiln fix` et ses conversions), `test_adopted.py` (repos adoptés), `test_unites.py`,
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
dépendent, alors qu'il change beaucoup ; d'où une version qui tourne d'abord en candidate sur
ses propres repos (`-rc`, comme Python ou Linux) et ne sort qu'une fois qu'elle a fait ses
preuves, mesurées et non supposées (amendé par antoine le 21 octobre 2026 : « la suivante
prête » ne mesurait pas le rodage, retenait les correctifs derrière les nouveautés, et le
16 octobre avait vu quatre promotions en une journée), et le 0.x du semver, prévu pour un début où tout peut casser (comme uv ou ruff), plutôt
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
   de `CHANGELOG.md`, `version = "X.Y.Z"` dans `pyproject.toml`, digests des images du modèle
   rafraîchis (`uv run python scripts/refresh_images.py`), contrôle complet (les trois
   commandes ci-dessous), branche poussée, **CI de GitHub attendue sur son commit** (macOS et
   tests de bout en bout, qui ne tournent que là : la rc.1 de la v0.4.0 était sortie sur un rouge
   que personne n'avait lu), tag `vX.Y.Z-rc.1` poussé seulement au vert. Les postes au canal `internal` (`kiln set
   channel=internal`) la suivent : `kiln update --all` y fait passer tous les repos
   générés. Le poste d'antoine est au canal **`beta`** (son choix du 21 octobre 2026 : en pleine
   amélioration de kiln, une nouveauté doit servir tout de suite) : l'outil est le checkout
   `~/code/kiln` installé en éditable, donc `develop` lu en direct, sans version ni mise à jour ;
   les versions restent ce qui part chez les autres. Un correctif de la candidate : commit `fix:` sur sa branche, tag `-rc.N+1`.
2. **Promotion**, quand `kiln version` la dit prête, sur des faits (`release.py`) : la CI de
   GitHub de la candidate est verte, **24 heures de rodage** depuis son tag (chaque `-rc.N`
   relance le compte), et **au moins un repo du dossier de code mis à jour vers elle** (`kiln
   update` y a fait passer les contrôles du repo). **Voie rapide** : une candidate qui ne contient
   que des correctifs depuis la dernière version publique (aucun `feat`, rien de cassant) sort
   après **2 heures**, sans repo exigé ; une faille de sécurité sort tout de suite. Alors : tag
   `vX.Y.Z` sur le commit exact de sa dernière candidate, fusion dans `main`, reversement dans `develop`, puis `kiln update --all --rehearse` (chaque repo répété sur un clone) et, au vert, `kiln update --all`.
   Le canal `public` (par défaut) ne voit que ces versions.

Chaque version, correctif compris, finit par `kiln update --all` : les repos générés citent leurs
workflows au tag exact dont ils partent (`ci.yml`), et `kiln update` le fait avancer. Les
workflows de kiln prennent leurs actions et la commande `charte` à leur propre commit
(`job.workflow_sha`). Un dépôt adopté par `kiln adopt` est au niveau de `kiln new` (choix
d'antoine, 24 octobre 2026, #59, qui renverse celui du 19 octobre) : le modèle y est rendu sans
écraser ses fichiers, notés sous `kept` dans `.copier-answers.yml` et que `kiln update` n'écrit
jamais, puis rejoué par `kiln update` comme ailleurs. Un dépôt adopté avant la 0.4.6 (une charte,
sans réponses) ne voit que le tag de ses workflows avancé (`adopted.py`, T-146) jusqu'à ce que
`kiln adopt` le complète. Modules : `versions.py` (tags, canaux, journal, version de
l'outil), `release.py` (`kiln version`), `shipping.py` (`kiln version cut`, `kiln version promote`).

## Le README, entièrement à jour

Demande d'antoine (19 octobre 2026) : le README, « le mieux au monde », entièrement à jour
d'une version à l'autre. Il montre kiln en peu de mots et en vraies images (sur le modèle d'uv,
ruff, Bun) ; la référence (`docs/reference.md`, `docs/reference.fr.md`) contient tout le
reste. `tests/test_docs.py` échoue si :
- la référence d'une langue oublie une commande, une option, un réglage de `kiln set`, un
  plugin, une skill, un hook ou un workflow réutilisable ;
- un README cite une commande qui n'existe pas, ne renvoie pas à sa référence, ou ne suit plus
  l'autre langue (mêmes sections, puces, images, tableaux) ;
- une image de `docs/assets/` diffère de ce que dessine `scripts/screenshots.py` à partir des
  vraies sorties de kiln (l'accueil, `kiln grid`, une règle, la note de `kiln update`, le schéma
  d'une version en clair et en sombre) ;
- les docs citent kiln à une autre version que celle de `pyproject.toml` ;
- une démo enregistrée tape une commande ou une option qui n'existe plus, ou pèse 5 Mo et plus ;
- le README que publie PyPI garde une image ou un lien relatifs (le build les fait pointer vers
  le tag de la version sur GitHub, `hatch-fancy-pypi-readme` dans `pyproject.toml`) ;
- un README porte les marques d'un texte d'IA que les lecteurs de Hacker News relèvent : tiret
  cadratin, puce ouverte en gras ou par un emoji, mot de vendeur (*seamless*, *powerful*…).
`kiln version cut` fait avancer cette version citée, et refuse de taguer la première candidate
d'une version dont ni le README ni la référence d'une langue n'ont changé (sauf
`<!-- readme: unchanged, pourquoi -->` dans son entrée). Un changement met donc à jour la doc
dans sa branche, pas à la release. Les images se regardent dans un vrai navigateur avant de les
commiter (`textLength` et les espaces ne se rendent bien que là).

La démo animée (`docs/assets/kiln-new.gif`) se réenregistre avant chaque candidate, quand ce
qu'elle montre a changé : `vhs docs/assets/kiln-new.tape` (vhs, ttyd et ffmpeg). Une seule
promesse partout (README, « About » de GitHub, résumé PyPI, image de partage), choisie par
antoine le 20 octobre 2026 : « Claude Code's workshop », puis « Start every new project, and
rescue every old one, like a senior engineer would — even if you're not one. », et sous elle
« Make Claude Code build production-grade repos, bring yours up to that grade, and keep them
that way. » Un vieux repo à remettre à niveau compte autant qu'un nouveau (`kiln adopt`, puis le
score et la correction de la v0.5.0). Le texte posté
sur Hacker News, titre et réponses compris, est écrit à la main par antoine (règle du forum).

## Contrôles

À la fusion dans `develop` : `uv run ruff check` et `uv run ruff format --check` sur les seuls
fichiers modifiés par la branche, rien d'autre ; ni mypy, ni test, ni CI de GitHub (choix
d'antoine, 21 octobre 2026). La CI de GitHub (`kiln.yml`) ne tourne que sur `release/**`,
avant `main`, et à la main. `uv run pytest -q` (réparti sur tous les cœurs par pytest-xdist ; `-n 0` pour un seul
processus, au débogage) tourne en entier à la release (`kiln version cut`), qui joue tout. Le crochet pre-commit de kiln (`.pre-commit-config.yaml`, posé par
`kiln install`) lance ruff à chaque commit, rien avant un push. Le catalogue étant déclaré en dossier local sur le poste
d'antoine, les sessions ouvertes appellent les hooks et la status line **dans l'arbre principal**
(`~/code/kiln/plugins/…`) : un fichier retiré ou renommé casse aussitôt chaque session (hook
introuvable = outil bloqué). Un chemin de plugin qui change garde donc un renvoi à l'ancien
(`plugins/base/`, vérifié par `test_plugins.py`).
