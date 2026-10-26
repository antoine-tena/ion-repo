# Référence de kiln

Tout ce que kiln offre, à la version qu'il est : chaque commande et chaque option, chaque
réglage, les workflows réutilisables, les plugins Claude Code, le moteur de charte et la façon
dont kiln sort ses versions. Le [README](../README.fr.md) montre à quoi sert kiln ; cette page
est celle où l'on cherche. `tests/test_docs.py` échoue quand une commande, une option, un
réglage, un plugin, une skill, un hook ou un workflow y manque.

*[English](reference.md) · Français*

## Un projet généré

Un projet généré contient :

- la stack choisie, conseillée selon le type de projet (voir ci-dessous) ;
- les consignes de kiln pour Claude dans `.claude/rules/kiln/` : celles du projet et de la
  charte toujours chargées, celles de chaque stack seulement quand Claude touche ses fichiers ;
  les règles contrôlables sont décrites dans `charter.toml` et vérifiées par la commande
  `charter`. Le `CLAUDE.md` racine appartient au projet ;
- l'outillage partagé : `.claude/` (plugins et variables `KILN_*`), `.vscode/`, `.editorconfig`,
  `.gitattributes`, `.gitignore`, modèle de PR, `CODEOWNERS`, pre-commit (ruff, ESLint, charte,
  refus de commiter sur `main` et `develop`) ;
- la CI (`.github/workflows/ci.yml`), qui appelle les workflows réutilisables de kiln, épinglés au SHA du
  commit de la version (son tag en commentaire), avec un jeton qui ne fait que lire le dépôt : sur GitHub à chaque
  push pour un dépôt public (gratuit et illimité), sur le poste par `kiln ci` pour un dépôt privé
  (`ci_runner: local` : aucune minute GitHub, dont le plan gratuit ne donne que 2 000 par mois) ;
  `kiln update` choisit d'après la visibilité du dépôt, `kiln set ci_runner=github` ou `local` change ;
- le suivi du travail, d'office : `docs/backlog/` (`backlog.md`, `done.md`, `rejected.md`, `urgent.md`,
  en anglais, skill `kiln:backlog`), que la status line de Claude Code compte ;
- les réglages de la status line propres au repo (`statusline_ci`, `prod_health_url`), posés en
  `git config statusline.*` par `kiln install`, `kiln new` et `kiln set` ;
- d'office (`--no-github` pour s'en passer) : le dépôt GitHub privé, avec `main` verrouillée (seul le commit initial)
  et `develop` protégée (ni suppression ni réécriture), et les correctifs de sécurité Dependabot ;
- un repo qui passe la grille de kiln : `kiln score` donne 100 à un projet neuf (une fois ses
  dépendances verrouillées par `kiln new` ; un front sans backend n'a pas encore de test).
  Dependabot pour chaque écosystème, chaque semaine, après 7 jours de quarantaine ;
- en option : les conteneurs podman, sur Debian 13, épinglés par empreinte, en lecture seule,
  sans aucune capacité, avec leurs sondes de santé.

Les plugins Claude Code vivent dans [`plugins/`](../plugins/), catalogue `kiln`
([`.claude-plugin/marketplace.json`](../.claude-plugin/marketplace.json)) :

- `kiln`, pour tous les projets, installé au niveau utilisateur : skills `worktree`, `merge`
  (fusion dans `develop`), `release` (release/vN, contrôle complet, annonce, main tagué,
  déploiement), `cleanup` (ménage des worktrees), `review` (commits et diff d'une branche relus
  et rangés avant la fusion, dépôt entier avant une version), `backlog`, `update` (l'outil kiln
  et ses plugins, puis le repo ouvert), `adopt` (`kiln adopt` dans un repo existant, passif de la
  charte trié avec l'utilisateur), `modernize` (les écarts de `kiln score --roadmap` comblés un à un, tests d'abord, chacun prouvé par `kiln score --rule`), `report` (un défaut de kiln remonté en issue ou en PR, avec l'accord de l'utilisateur), `contribution` (la PR d'un contributeur extérieur : code relu avant d'en rien lancer, tri, revue, fusion qui le crédite, rien publié sans accord), `good-first-issues` (un petit stock d'issues `good first issue` tiré du backlog et réservé aux contributeurs extérieurs, regarni à chaque fusion), `token` (le jeton d'un service collé une fois dans un dossier `.<service>/` ignoré par git, jamais affiché) ; hooks garde de branche (`branch_guard.py`, qui refuse une ligne `Claude-Session:` dans un message de commit, et un `Co-Authored-By: Claude` sur un poste réglé `ai_trailers=never`), fichiers protégés (`protect_files.py`), contrôle du fichier
  modifié (`check_file.py`), questions à l'ouverture de session (`session_start.py`, logo et nouveautés au premier message par `first_prompt.py`, et CI rouge de la branche d'intégration signalée à Claude, une exécution que GitHub n'a jamais démarrée distinguée d'un échec du code) : dans un repo kiln, sa mise à jour (l'outil kiln s'il
  est en retard sur GitHub, puis le repo par `kiln update` ; un « non » repousse la question de
  5, 10, 30 puis 50 sessions, après quoi désinstaller kiln ou délier le repo est proposé) ; dans
  un repo à soi qui ne suit pas kiln, son adoption (« Oui », « Plus tard », « Jamais pour ce
  repo »), dès la 3e session, au plus une fois toutes les 10 sessions du poste. Toutes passent
  par `reminders.py` : une note de bienveillance du poste monte à chaque « oui » et baisse à
  chaque « non », et étire ou raccourcit tous les délais (doublés au plus méfiant, de moitié au
  plus enthousiaste) ; `git config kiln.update-check false` pour s'en passer, sorties de commandes condensées par [rtk](https://github.com/rtk-ai/rtk) (`rtk.py`) quand il
  est installé (`mise use -g github:rtk-ai/rtk`, sans `rtk init` : le hook est fourni ici) ; MCP context7 ; status line commune (`plugins/kiln/scripts/statusline.py`,
  en anglais, aux couleurs de kiln), qui montre le contexte en jetons, d'autant plus coloré qu'un message
  coûte cher, et en rouge une fois le cache expiré (le message suivant réécrit tout), posée par `kiln install` dans `~/.claude/settings.json`, relancée toutes les 5 secondes (`refreshInterval`) ; son
  style se choisit par poste : `kiln set statusline=plain|band|classic|classic-band`,
  `none` (retirée) ou `custom` (kiln ne touche plus à la `statusLine` de l'utilisateur, choix
  automatique s'il en a déjà une) ;
- `nuxt` (skills `nuxt`, `vue-best-practices`, `vue-testing-best-practices`, `vitest`, `polish`,
  `preview` — captures sur trois téléphones et un ordinateur ; MCP playwright) et `django` (skills
  `migration`, `regen-api`, `postgres-read`), activés par le `.claude/settings.json` généré
  selon la stack ;
- `vps` (skills `deploy`, `prod-logs`, `prod-dump`) et `stripe` (MCP en mode test),
  activés à la main par le repo qui en a besoin.
- `serena` (MCP [Serena](https://github.com/oraios/serena) en lecture seule : plan d'un
  fichier, définition et références d'un symbole), activé par `kiln set serena=true` sur un gros
  repo ; les éditions restent aux outils de Claude Code, où sont branchés les hooks de `kiln`.

Installation : `kiln install` hors d'un repo, ou à la main `claude plugin marketplace add antoine-tena/kiln`, puis
`claude plugin install kiln@kiln --scope user`.

Le modèle vit dans [`template/`](../template/), servi par [Copier](https://copier.readthedocs.io) :
chaque projet garde dans `.copier-answers.yml` ses réponses et la version du modèle dont il
part, ce qui permet de lui rapporter les évolutions sans écraser ses modifications locales.

## Installation

Prérequis : [uv](https://docs.astral.sh/uv/) et git ; [pnpm](https://pnpm.io/) (Node 24) pour un
front JavaScript ; un JDK 25 et `unzip` pour un backend Java ; [podman](https://podman.io/)
pour les conteneurs ; [gh](https://cli.github.com)
pour le dépôt GitHub, que `kiln new` crée d'office (si `gh` n'est pas connecté, kiln lance la
connexion et affiche le lien https://github.com/login/device).

```sh
uv tool install kiln-cli
```

Installe deux commandes, `kiln` et `charter` (`charte`, son nom d'avant 0.4.0, reste accepté),
à la dernière version publiée sur PyPI (le paquet
s'appelle `kiln-cli`, `kiln` y étant pris ; `uvx kiln-cli new mon-app` l'essaie sans
l'installer). Pour suivre les candidates (canal `internal`) ou un commit précis :
`uv tool install git+https://github.com/antoine-tena/kiln@<tag>`. macOS, Linux, et Windows par
WSL. Quand une version sort, le hook de début de session propose de mettre à jour l'outil, puis
chaque repo ; à la main : `uv tool upgrade kiln-cli`, puis `kiln update` dans le repo.
Complétion dans bash : `eval "$(kiln completion bash)"` dans `~/.bashrc`.
Python 3.14 est requis ; uv le télécharge au besoin. Au premier `kiln install`, kiln demande le
système du poste (Linux, WSL ou macOS) et le garde dans `~/.config/kiln/config.toml`, avec
`owner` et `team` par défaut si on les y ajoute.

## Commandes

<p align="center">
  <img src="assets/kiln-home.svg" alt="L'écran d'accueil de kiln : un four en pixel art au-dessus de ses commandes, rangées par projet, quotidien, grille et tous les repos" width="620">
</p>
<p align="center"><i><code>kiln</code> seul : toutes les commandes, rangées selon ce que l'on fait.</i></p>

| Commande | Rôle |
|---|---|
| `kiln new [dossier]` | Trois questions (ce qu'on construit, l'envergure, la langue de l'équipe ; `--all-questions` pour le questionnaire complet), génération, verrous, installation, premier commit sur `main`, puis `develop` où tout le travail se fait. |
| `kiln adopt` | Amène un repo existant que kiln n'a pas généré au niveau de `kiln new` (`--template` pour une autre source), sur une branche de travail (`chore/kiln-adopt`, ouverte par kiln quand il est lancé sur `main`, `master` ou `develop`) : le modèle rendu avec ce que kiln trouve dans le repo (la stack, d'après les fichiers repères de `backend/` et `frontend/`, ou de la racine quand le code y vit : une app Vite ou un `manage.py` à la racine, notés `frontend_dir = "."` ou `backend_dir = "."` dans les réponses, que suivent la CI, les crochets, les règles, la charte, Dependabot, `kiln check` et `kiln dev` ; l'envergure par `--size` ; le propriétaire, d'après le remote `origin`) et chaque fichier qui manque au repo posé : `CLAUDE.md`, `.claude/rules/kiln/`, le `charter.toml` de l'envergure, les crochets pre-commit, la CI qui appelle les workflows de kiln, `docs/backlog/`. N'écrase aucun fichier : ceux que le repo a, et ses dossiers de code, sont notés sous `kept` dans `.copier-answers.yml`, que `kiln update` n'écrit jamais non plus ; le `.gitignore` reçoit les lignes du modèle qui lui manquent. Puis le passif que la charte relève. Ensuite `kiln update` rejoue le modèle comme dans un repo généré ; un repo adopté avant la 0.4.6 se complète en relançant `kiln adopt`. |
| `kiln publish` | Crée le dépôt GitHub privé et protège ses branches, pour un projet généré sans `gh`. |
| `kiln install` | Prépare un poste après un clone : outils (pre-commit avec pre-commit-uv, podman-compose), dépendances, `backend/.env`, migrations, pre-commit. Hors d'un repo, ou avec `--machine`, kiln pour tout le poste : la commande `kiln` en outil uv, le catalogue de plugins et le plugin `kiln` au niveau utilisateur (chaque session Claude), les réglages du poste. Relançable : seul ce qui manque est fait. |
| `kiln dev` | Fait tourner le projet sur le poste, en arrière-plan. Le code qu'on modifie y tourne, rechargé à chaque changement : les serveurs de la stack et les processus que liste le `Procfile.dev` d'un dossier (`worker: uv run celery -A core worker`, au format de foreman). Un dossier que la stack ne sert pas, comme un repo adopté avec Vite et Express à la racine, lance les scripts `dev`, `dev:*`, `server`, `serve` et `watch` de son `package.json` (`start` s'il n'y en a aucun), avec le gestionnaire de paquets que nomme son verrou, ses dépendances installées d'abord quand `node_modules/` manque ou date d'avant le verrou. Le front de la stack passe aussi par le gestionnaire de son verrou : une app Nuxt adoptée restée sur npm lance `npm run dev`, pas `pnpm dev`. Ce qu'on ne modifie jamais tourne dans podman : les services `db`, `postgres` et `redis` du fichier compose, relancés avec leurs données et attendus (sonde de santé) quand un processus hors du front en a besoin. Un serveur dont un autre processus tient déjà le port ne démarre pas : kiln nomme ce processus, ou le worktree dont le `kiln dev` le tient. Un petit projet lance tout d'un coup ; à partir de trois processus, kiln demande quoi lancer (tout, comme la dernière fois, le front seul, ou un par un ; le front seul lit le `.env` de son dossier et pas son `.env.dev`, les surcharges de la pile locale complète, pour tourner sur une API distante), et `--only django,nuxt` répond sans question. Quand chaque serveur répond, kiln montre où l'ouvrir et propose de suivre les journaux (Ctrl+C les quitte, les serveurs continuent). Ensuite `kiln dev status`, `kiln dev logs [service]` (`-f`, `--follow`, pour continuer à lire) et `kiln dev stop`, bases comprises sauf si un autre worktree du repo tourne encore dessus ; `kiln dev` relancé montre ce qui tourne. `--foreground` le garde dans le terminal, sorties entrelacées et préfixées par processus en couleur (`django │ …`), jusqu'à Ctrl+C. `--containers` lance plutôt toute la pile dans podman, comme en production. Dans un repo que la stack de kiln ne sert pas, dont le fichier compose lance les services du projet lui-même alors que kiln lancerait ses scripts `package.json`, le terminal propose les services compose dans podman ou les scripts sur le poste, la dernière réponse gardée par défaut ; hors d'un terminal, les scripts tournent et le fichier compose est signalé. Hors d'un terminal (un script, une session Claude), rien n'est demandé. |
| `kiln check` | Ruff et mypy pour chaque projet Python, ESLint et les types côté front, puis la charte ; les suites de tests (pytest, tests Maven) seulement avec `--tests`, la release les joue toutes (`kiln ci`). Le typage passe par `charter types` quand la charte déclare `[types]` ; les tests d'un backend Django tournent sur les PostgreSQL et Redis jetables du job Django de `ci.yml`, avec ses variables, comme `kiln ci` les rejoue. Des `node_modules` absents ou en retard sur le lockfile sont d'abord installés, un venv déplacé avec son repo réinstallé. |
| `kiln ci [commit]` | Rejoue sur le poste la CI du `ci.yml` pour ce commit (défaut `HEAD`) et pose le verdict en note git sur origin, que le script de déploiement accepte comme une CI verte. `--status` : le verdict seul. Voir « CI rejouée sur le poste ». |
| `kiln contract` | Django + Nuxt : exporte `openapi.json` depuis le code, puis régénère les types du front (`app/types/api.d.ts`). `kiln update` le fait aussi. |
| `kiln waive [RÈGLE\|fichier]` | Déroge à une règle de kiln (`--paths`, `--reason`, `--upstream`), ou fige un fichier généré que `kiln update` ne touchera plus ; `--renew` passe au palier suivant (une semaine, un mois, trois mois, six mois), `--permanent` sans échéance. Sans argument : liste les dérogations. Voir [Moteur de charte](#moteur-de-charte). |
| `kiln set` | Dans un repo : sans argument, affiche ses paramètres ; `kiln set clé=valeur…` les change : le repo est régénéré (sur la branche `chore/kiln-set`, ouverte par kiln sur `main`, `master` ou `develop`), un framework retiré emporte ses fichiers. Clés : `name`, `title`, `description`, `project_type`, `size`, `backend`, `frontend`, `podman`, `language` (et par usage : `language_comments`, `language_commits`, `language_docs`, `language_tickets`, `language_ui`), `owner`, `team`, `java_package`, `timezone` (fuseau des notions calendaires ; les dates sont stockées en UTC), `serena`, `compact_window` (taille du contexte, en jetons, à laquelle Claude Code compacte une conversation : `400000` par défaut, puisque chaque message relit tout le contexte ; `1000000` garde celle de Claude Code ; `claude --autocompact 1M` la relève le temps d'un lancement), `deploy`, `vps_host`, `api_domain`, `site_url`, `deploy_branch`, `frontend_deploy`, `north_star`, `ci_runner`, `statusline_ci`, `prod_health_url`. Hors d'un repo, ou avec `--global` : les réglages du poste (`system`, `owner`, `team`, `code_dir`, `channel`, `statusline`, `ai_trailers` = les commits et pull requests de Claude disent-ils que Claude a aidé : `disclose`, par défaut et réponse à « choisis pour moi » au premier `kiln install`, ou `never`, qui vide l'`attribution` de Claude Code et fait refuser un `Co-Authored-By: Claude` par la garde de branche ; dans `~/.config/kiln/config.toml`) ; une clé propre au poste (`statusline`, `channel`, `system`, `code_dir`, `ai_trailers`) y va aussi depuis un repo. |
| `kiln update` | Évolutions du modèle, mises à jour compatibles des dépendances, puis contrôles. `--major` : versions majeures comprises. `--no-template`, `--no-deps` pour n'en faire qu'une partie. Lancé sur `main`, `master` ou `develop` avec un arbre propre, il ouvre lui-même sa branche de travail (`chore/kiln-update`, datée quand elle existe déjà). `--rehearse` : la mise à jour jouée d'abord sur un clone jetable, le repo intact, seul le bilan revient. Après le modèle, les conversions de `kiln fix` comblent ce qu'il laisse au repo (actions et workflows de kiln épinglés par SHA, empreintes), sans commit comme le reste ; les workflows de kiln épinglés par SHA suivent la version suivante sans conflit, puis sont épinglés de nouveau. Dans un repo adopté (`kiln adopt`), seul ce qui appartient à kiln change : ses noms de 0.3 d'abord (`charte.toml` → `charter.toml` en gardant les identifiants de règles du repo, la commande `charte` de ses hooks, les workflows `charte.yml`, `contrat-api.yml`, `securite.yml` et leurs entrées ; les fichiers dont le texte les cite encore sont listés ; un `docs/a-faire/` devient le `docs/backlog/` de kiln, tickets `AF-NN` devenus `T-NN` aux mêmes numéros), puis les références aux workflows de kiln, à la dernière version publique (le `develop` de kiln au canal `beta`), entrées vérifiées. |
| `kiln update --all` | Tous les repos kiln du dossier de code (`~/code`, réglable par `code_dir`) : pour chacun, un worktree depuis la branche d'intégration, la mise à jour, des commits de dix fichiers au plus, puis la fusion directe dans l'intégration (commit de fusion poussé) ; contrôles en échec, la branche est poussée sans être fusionnée. L'arbre principal ne change jamais de branche. `--all --rehearse` : chaque mise à jour répétée sur un clone, rien n'est touché, un bilan par repo. |
| `kiln grid [ID]` | La grille : les pratiques que kiln tient pour les meilleures aujourd'hui, un petit fichier TOML par règle, avec son pourquoi, ses sources vérifiées et datées, son niveau (adopt, trial, assess, hold), sa détection et sa correction. `--theme`, `--scope`, `--level` filtrent ; un identifiant montre la règle en entier, et comment y déroger. |
| `kiln score [CHEMIN]` | N'importe quel repo, créé par kiln ou non, mesuré face aux règles notées de la grille en une seconde environ, sans jeton : une note sur 100 et une par pilier (chaque règle qui s'applique pèse autant ; celles hors des stacks du repo, ou sans rien à regarder, sont laissées de côté), les trois écarts à combler d'abord, puis chaque écart avec sa raison, son emplacement, sa source et ce qui le comble, et la note à nouveau à la fin, pour qu'une longue liste ne la fasse pas défiler hors de vue. Les règles qui font l'objet d'une dérogation (`kiln-waivers.toml`) sont montrées à part. Ce que les fichiers ne disent pas, les réglages GitHub (la branche par défaut ni poussée de force ni supprimée, et un historique linéaire quand le repo ne fusionne pas par commits de fusion ; secret scanning et push protection ; alertes et mises à jour de sécurité Dependabot ; signalement privé des vulnérabilités sur un repo public), est lu par `gh` quand il est connecté avec les droits d'admin sur le repo, chaque écart avec le lien direct vers sa page de réglages ; kiln ne lit, ne garde ni n'affiche jamais le jeton. Sans cet accès, ces règles sont laissées de côté et la note dit que les réglages sont inconnus, jamais un échec. Une lecture est gardée un jour (`~/.cache/kiln/forge/`) et sautée en CI : le détail d'un réglage reste sur le poste du propriétaire, le badge, un signalement à kiln et un journal de CI ne portent que la note et les identifiants des règles. Les fichiers sont lus tels qu'ils sont : une source qui n'est pas en UTF-8 est décodée (sa marque d'ordre des octets, puis cp1252 ou latin-1) et listée plutôt que lue vide, un fichier binaire (un octet nul dans ses 8 premiers Ko) et une source minifiée (une ligne de plus de 1 000 caractères) sont laissés hors des règles de code. Coder sans agent n'est pas une faute : la règle des fichiers d'agent (`AI-CONTEXT`) est hors de la note, montrée en conseil au seul repo travaillé avec un agent (un dossier `.claude/`, `.cursor/`, `.codex/` ou `.gemini/`), et une carte du repo compte où qu'elle soit écrite (`README.md`, `CONTRIBUTING.md`, `ARCHITECTURE.md` comme `CLAUDE.md` ou `AGENTS.md`). Les stacks que la grille ne couvre pas encore (Java, .NET, PHP, Go…), reconnues à un manifeste ou à leurs seules sources, sont nommées ; quand elle n'en trouve aucune qu'elle couvre, la note dit qu'elle ne repose que sur les règles universelles. De même pour les paquets connus qu'aucune règle ne couvre encore (Celery, SQLAlchemy, React…) et les règles levées encore et encore par dérogation. Dans un terminal, kiln propose ensuite de le signaler à kiln, en montrant les lignes exactes qui partiraient et rien d'autre (jamais de code, de chemin ni de nom de paquet privé) : une issue par manque sur GitHub, un 👍 quand elle est déjà ouverte, un lien prérempli sans `gh` ; « jamais » vaut pour le repo, et une ligne signalée une fois n'est plus proposée. `--all` liste chaque règle et chaque emplacement, `--json` le rapport (schéma 1), `--badge` un badge pour le README, `--online` rafraîchit les dates de fin de vie depuis endoflife.date et relit les réglages GitHub. Rien n'est écrit dans le repo. `--roadmap` : ce qu'aucun convertisseur ne comble, pour Claude Code, les écarts sûrs d'abord puis les plus petits, chacun avec sa raison, ses emplacements (fichier et ligne) et sa preuve ; les emplacements d'un détecteur approximatif sont marqués « à confirmer », et un faux positif s'écarte pour de bon par une dérogation sur son chemin (`kiln waive ID --paths FICHIER --permanent`). `--roadmap --write` en fait des tickets de `docs/backlog/backlog.md`, une fois chacun. `--rule ID` : cette règle seule, en échec tant que son écart reste ouvert (la preuve qu'attend `/kiln:modernize`). |
| `kiln fix [CHEMIN]` | Chaque écart qu'un script peut combler, comblé sur une branche de travail `kiln/fix-<date>` par des conversions jouées dans un worktree jetable du dernier commit (sous `~/.cache/kiln/worktrees`, les `node_modules` installés liés et le `.env` copié pour les contrôles) : votre arbre, changements non commités compris, n'est jamais touché et seule la branche reste ; un second passage le même jour reprend sa branche quand elle ne porte que des commits de `kiln fix`, sinon ouvre `kiln/fix-<date>-2`, un commit par règle avec son pourquoi et sa source. Les contrôles du repo tournent sur tout le dépôt avant et après chaque conversion (`kiln check --all` dans un repo kiln, sinon les commandes de lint, de typage et de tests que déclarent ses manifestes, à la racine et un dossier plus bas : ruff, mypy, pytest ou le `manage.py test` d'un projet Django, les scripts `lint`, `typecheck` et `test` d'un `package.json` lancés par npm, pnpm, yarn ou bun selon son verrou), chacun avec un délai de 10 minutes. Chaque contrôle tourne une fois avant la première conversion : celui dont l'outil manque (nommé, avec comment l'installer), déjà rouge ou hors délai ne peut pas juger, et le résumé dit lequel et pourquoi ; les verts jugent chaque conversion, nommés dans chaque commit (`Checked: …`). Chaque commit est prouvé : le détecteur de la règle tourne de nouveau (`fixed` quand il passe, `partial` quand un écart reste pour le jugement), toute la grille est comparée avant et après (une conversion qui fait passer une autre règle au rouge est annulée, c'est un défaut du convertisseur), et toute erreur d'un convertisseur remet l'arbre en état sans arrêter le passage (`converter bug`). Une conversion qui fait passer les contrôles au rouge sort du lot, jamais fusionnée rouge, jamais perdue : son commit attend sur une branche à lui (`kiln/fix-<date>-<règle>`), la sortie du contrôle en échec gardée dans le dossier git, où `kiln score --roadmap` confie l'écart à Claude avec son journal et la branche. Une règle qu'une conversion fait entrer en jeu (l'audit qu'une nouvelle CI demande) rejoint le passage. Chaque commit donne les points qu'il a gagnés (`Score: 62 → 65 (+3)`), le résumé aussi. Une conversion qui touche un `Containerfile` ou un `Dockerfile` construit aussi son image avec podman (ou docker) : celle qui ne se construit plus est annulée comme un contrôle rouge, sauf si elle ne se construisait pas non plus avant. Un repo sans aucun contrôle trouvé est corrigé quand même, chaque commit marqué « unverified: no check found » (ou par la raison pour laquelle aucun de ses contrôles ne peut juger). mypy vérifie les `files` que nomme sa configuration, `.` quand elle n'en nomme aucun. Conversions : actions épinglées par SHA avec leur version exacte en commentaire, quarantaine des mises à jour, Dependabot pour chaque écosystème trouvé (actions composites comprises), jetons de workflow en lecture seule, gitleaks, une CI minimale, le lint, les tests et l'audit des dépendances (`uv audit`, pip-audit, `pnpm audit` ou `npm audit`, aussi chaque lundi) qui manquent à une CI GitHub existante, en workflows à part, le texte d'un tiers (`${{ github.event.issue.title }}`) sorti du `run:` vers l'`env:` de l'étape, un `.env` suivi sorti de git (gardé sur le disque, ignoré, ses clés dans un `.env.example` ; ses secrets restent dans l'historique, à renouveler), rétroportages obsolètes retirés, des fichiers `requirements` seuls changés en projet uv (`pyproject.toml`, `uv.lock`, les `requirements` réexportés depuis lui), sinon `requirements` lâches compilés en versions exactes par uv, ruff mis en place avec ses corrections sûres, `@ts-expect-error`, images épinglées par empreinte, Debian 13, un utilisateur non root, services compose durcis (système de fichiers en lecture seule, pas de nouveaux privilèges, capacités retirées) là où chacun démarre encore ainsi sous podman, les autres nommés et laissés tels quels, environnements d'exécution sortis de leur fin de vie. Le compresseur (règles `DEAD-CODE` et `UNUSED-DEPENDENCIES`, hors de la note tant qu'elles sont à l'essai) ne tourne que nommé : `kiln fix --rule DEAD-CODE` retire les fonctions, classes, méthodes et fichiers que rien n'appelle (vulture, knip), `--rule UNUSED-DEPENDENCIES` les dépendances que rien n'importe (deptry, knip). Des garde-fous gardent ce qu'un outil statique ne voit pas (conventions et décorateurs d'un framework, une surcharge, un nom cité dans un gabarit, une chaîne ou une config, du code que les tests ont exécuté, un plugin chargé par ses points d'entrée, les tests et les configs ; sécurité, analyse syntaxique, fuseaux horaires et encodage du texte ne sont jamais touchés) ; chaque suppression est ensuite prouvée par étapes, le vérificateur de types puis les tests comparés un à un avec un passage d'avant toute suppression, par lots coupés en deux jusqu'à isoler celle qui casse, qui reste. Sans un test qui passe, rien n'est retiré. Celles qui ont besoin du réseau le disent avant de commencer. `--dry-run` montre le plan et le diff sans rien écrire ; `--rule ID` pour une seule règle. Finit par la note avant et après, et les points de chaque règle. `kiln update` passe les mêmes conversions après le modèle, sur place, laissées sans commit avec les changements du modèle pour relecture, fichiers gelés et gardés intacts. |
| `kiln doctor` | Diagnostic du poste (git, uv, gh connecté, pnpm, podman, Java, pre-commit, version de kiln, plugin Claude, configuration) et du repo courant (version du modèle, crochet pre-commit, dépendances, venv déplacé avec son repo, `node_modules` en retard sur le lockfile, `backend/.env`) : ✓, ! à regarder ou ✗ bloquant, chaque fois avec la commande qui corrige. Ne modifie rien. |
| `kiln completion bash` | Script de complétion bash tiré des commandes et options de kiln ; l'activer par `eval "$(kiln completion bash)"` dans `~/.bashrc`. |
| `kiln status` | État des repos kiln du dossier de code : branche, arbre propre ou non, version du modèle (`v0.4.0 → v0.4.2` en retard), dérogations (`!` si l'une est échue), stack ; puis les règles dérogées, par nombre de repos. |
| `kiln version` | Dans le dépôt de kiln : dernière version publique, candidates (âge, repos qui les ont adoptées, prêtes à promouvoir), numéro de la prochaine et tickets du plan (`docs/backlog/`) qui restent avant elle. `kiln version cut` : branche `release/vX.Y.Z`, ébauche de la note de version et numéros, puis (une fois la note relue) contrôles, CI de GitHub attendue et, au vert seulement, tag `-rc.N` ; `kiln version promote` : tag public sur la dernière candidate dont la CI est verte (`--urgent` saute la décantation et le repo adoptant), fusion dans `main` et `develop` (PyPI et GitHub Release suivent). |
| `charter` | Vérifie le repo contre son `charter.toml` (`charter --detail`, `charter --unverified`, `charter types`, `charter coverage`, `charter file <chemin>`). |

`set` et `update` travaillent sur une branche, arbre propre ; les conflits entre le modèle et une
modification locale sont marqués dans le fichier (`<<<<<<<`). Relire, commiter, fusionner dans
`develop` (skill `kiln:merge`, sans PR ni approbation à attendre).

Quand une version de kiln plus récente est sortie sur le canal du poste, une commande tapée dans
un terminal finit par proposer de l'installer (GitHub interrogé au plus une fois par jour ; après
un non, la même version revient une semaine plus tard). Pas dans Claude Code, dont le début de
session pose la question, ni dans `kiln doctor`, ni pour un outil installé depuis un dossier ;
`KILN_NO_UPDATE_CHECK=1` la coupe.

`new`, `install`, `update` et `status` s'ouvrent sur une bannière : un four en pixel art, la
version de kiln, la commande, le projet (envergure, stack) et son dossier. Hors terminal ou avec
`NO_COLOR`, une seule ligne de texte à la place. `kiln` seul (ou `kiln --help`) ouvre l'écran
d'accueil : commandes par section et exemples ; `kiln <commande> --help` (ou `-h`) montre
les options d'une commande de la même façon (bannière, usage court
`kiln new [options] [directory]`, arguments, options) ; `kiln --version` (ou `-V`, `-v`) donne
la version ; les étapes, succès, erreurs et le tableau de
`status` suivent la même palette pierre et feu, sans couleur hors terminal.
Chaque commande externe (`uv sync`, `pnpm install`, contrôles…) tourne derrière une roue animée
qui montre sa dernière ligne, puis laisse `✓ commande  durée` ; sa sortie complète n'apparaît
qu'en cas d'échec. Un bilan encadré clôt la commande : verdict, durée totale et durée de chaque
étape. `KILN_VERBOSE=1 kiln …` rend la sortie complète des commandes.

Sans dossier, `kiln new` demande le nom du projet et le crée dans le dossier courant.
Options de `new` : `--size`, `--type`, `--backend`, `--frontend`, `--podman`,
`--vps <utilisateur@adresse>`, `--name`, `--title`,
`--description`, `--owner`, `--team login1,login2`, `--language en|fr`, `--goal "<boussole>"`, `--prod-url <url>`,
`--no-github` (pas de dépôt GitHub),
`--no-install`, `--all-questions`, `--template <chemin ou URL>`. Au-delà des trois questions, ce qu'aucune option ne fixe prend sa valeur conseillée, sauf avec
`--all-questions`.

<p align="center">
  <img src="assets/kiln-grid.svg" alt="kiln grid : les règles que kiln défend, par thème, chacune avec son niveau" width="680">
</p>
<p align="center"><i><code>kiln grid</code> : les règles que kiln défend aujourd'hui ; <code>kiln grid &lt;ID&gt;</code> en montre une en entier, comme dans le README.</i></p>

## Envergure

Deuxième question de `kiln new`, après ce qu'on construit : « How hot does this one burn? ». Quatre crans, nommés d'après
le feu du four :

| Cran | Projet |
|---|---|
| `spark` | un script, un outil perso, une analyse ponctuelle |
| `ember` | une petite app ou un site, une ou deux personnes, peu d'enjeu (par défaut) |
| `flame` | une app en production, de vrais utilisateurs, plusieurs contributeurs |
| `blaze` | plusieurs équipes ou services, de gros enjeux |

L'envergure est écrite dans `.claude/rules/kiln/project.md` et règle les valeurs par défaut des
questions suivantes : à partir de `flame`, les conteneurs podman sont précochés. Elle se change
par `kiln set size=…` et `kiln status` l'affiche.

## Conseil de stack

Le type de projet choisit une stack, que l'on change par `--backend` et `--frontend` (ou
`--all-questions`), ou plus tard par `kiln set backend=… frontend=…`.

| Type de projet | Backend conseillé | Frontend conseillé |
|---|---|---|
| Application complète (`app`) | Django + Django Ninja | Nuxt + Vue |
| API seule (`api`) | FastAPI | aucun |
| Site de contenu (`site`) | aucun | Astro |
| Tableau de bord de données (`dashboard`) | Données Python (polars, marimo, Plotly) | Streamlit |
| Analyse de données (`analysis`) | Données Python | aucun |
| Outil en ligne de commande (`cli`) | Outil Python (`cli` : argparse, commande installable) | aucun |

Backends : `django`, `fastapi`, `data`, `cli`, `java`, `none`. Frontends : `nuxt`, `next`, `astro`, `vite-react`,
`streamlit`, `dash`, `none`. Toutes les combinaisons sont générées et vérifiées par les tests.

**Django et Nuxt : complets. Les autres : figés, entretenus.** Toutes les piles restent générées
et testées, mais les nouvelles règles de la grille vont d'abord à Django et Nuxt, jusqu'à ce
qu'ils soient en haut de la grille ; les règles universelles (CI, conteneurs, chaîne
d'approvisionnement, secrets) les notent toutes.

`java` n'est conseillé pour aucun type : Java 25 sans framework, construit par Maven via son
wrapper `./mvnw` (version et somme SHA-256 figées), tests JUnit 6, couverture JaCoCo, enforcer
qui refuse les versions dynamiques. `kiln update` n'en monte pas les dépendances : les versions
du `pom.xml` se changent à la main.

## Déploiement sur un serveur à soi

`deploy=vps` (`kiln new --vps root@<adresse>`, ou `kiln set deploy=vps` plus tard), pour
un backend Django avec podman, ajoute une production éprouvée :

- `config/vps/` : pile de production (PostgreSQL et gunicorn, système de fichiers en lecture
  seule), Caddyfile (TLS automatique), script de bascule exécuté en root sur le serveur (une image
  par commit, migrations, retour arrière automatique si la nouvelle version ne répond pas),
  utilisateur `deploy` limité à cette commande, sauvegardes quotidiennes et d'avant bascule (copie
  restic hors du serveur en option), test de restauration hebdomadaire, relance des conteneurs
  malades (unités systemd) ;
- `scripts/ops/` : `deploy-backend.sh` (`--dry-run`, `--rollback`) et `smoke-test.sh`, depuis le
  poste ; le serveur reçoit le code en bundle git, sans accès au dépôt ;
- `docs/operations/production.md` : préparation du serveur, déploiement, retour arrière,
  sauvegardes.

Un front Streamlit ou Dash sans API (backend `data` ou aucun) y a droit aussi, à sa mesure : son
image seule derrière Caddy (websockets compris), sonde `/_stcore/health` pour Streamlit, bascule et
retour arrière par `scripts/ops/deploy-frontend.sh`, sans base ni sauvegarde. Vercel reste
réservé à Nuxt.

Réglages : `vps_host`, `api_domain`, `site_url`, `deploy_branch` (par `kiln set`). Quel
que soit le déploiement, l'image du backend Django sert gunicorn et ses fichiers statiques
(WhiteNoise) sans migrer au démarrage, et `/api/health` rend la version en service.

## Front sur Vercel

`frontend_deploy=vercel` (front Nuxt, `kiln set frontend_deploy=vercel`) ajoute
`scripts/ops/deploy-frontend.sh` : `vercel --prod` envoie les fichiers du poste, le script ne
l'autorise que depuis `develop` à jour avec `origin`, front sans modification locale et CI verte
(`SKIP_CI=1` en cas d'urgence). Le projet Vercel se lie une fois par `vercel link`.

## Mises à jour des dépendances

`kiln update` fait des mises à jour compatibles : uv reste dans les bornes du `pyproject.toml`
(même version majeure), pnpm ne monte que les dépendances qui gardent leur majeure et annonce les
autres. `kiln update --major` relève les bornes à la dernière version, prend les dernières
versions pnpm et met à jour les crochets pre-commit. Les contrôles suivent toujours : une montée
qui casse quelque chose est signalée avant le commit. Entre deux mises à jour, Dependabot propose
chaque semaine les nouvelles versions, une fois passés 7 jours de quarantaine ; les workflows de
kiln n'avancent que par `kiln update`, qui convertit ce qui change avec eux.

## Versions

kiln numérote ses versions `vMAJEUR.MINEUR.CORRECTIF`, comme Claude Code : en 0.x, chaque
version monte le correctif, changements cassants compris (`0.4.1 → 0.4.2`), signalés en tête de
leur note et convertis par `kiln update` ; la mineure ne monte que pour une étape
(`kiln version --minor`). À partir de 1.0, semver strict.
Le travail s'intègre dans `develop` ; `main` ne reçoit que des versions.

- **Candidate** (`v0.4.2-rc.1`) : tirée de `develop` sur une branche `release/v0.4.2`, avec son
  entrée en tête de [`CHANGELOG.md`](../CHANGELOG.md). Seuls les postes au canal `internal` la
  suivent (`kiln set channel=internal`).
- **Promotion** (`v0.4.2`) : une fois la candidate rodée, sur des faits : CI verte, 24 heures
  depuis son tag et au moins un repo du poste mis à jour vers elle ; 2 heures sans repo exigé
  pour une candidate de correctifs seuls. Le même commit est tagué et fusionné
  dans `main`. `kiln version` montre les candidates, leur âge, qui les a adoptées, lesquelles
  sont prêtes et le numéro de la prochaine.
- **Clients** : ils se mettent à jour à chaque version, correctif compris. Le hook de début de
  session propose l'outil puis le repo ; `kiln update` applique la version, montre ses
  nouveautés et fait avancer la version (SHA et tag) à laquelle le `ci.yml` du repo cite les
  workflows de kiln.
- **Outil** : `uv tool install kiln-cli` prend les versions promues, publiées sur PyPI par le
  workflow `pypi.yml` au tag `vX.Y.Z` ; `uv tool install git+https://github.com/antoine-tena/kiln@<tag>`
  prend aussi les candidates ; `brew install antoine-tena/kiln/kiln` prend les versions promues
  par le tap Homebrew (https://github.com/antoine-tena/kiln-homebrew), que `pypi.yml` met à jour
  au même tag, et kiln propose alors `brew upgrade kiln` ;
  `kiln status` dit de quelle version part chaque repo (`v0.4.0 → v0.4.2`), la bannière celle
  de l'outil (`v0.4.2 +3 · abc1234` : trois commits après v0.4.2, installé depuis un dossier).
  Seule une version met un repo à jour : un outil qui n'en est pas une (un dossier en avance sur
  son tag ou modifié, une branche) est refusé par `kiln update`, `kiln new` et `kiln adopt`, qui
  donnent la commande d'installation de la version ; pour essayer le code de kiln sur un repo
  jetable, `KILN_TEMPLATE=<dossier de kiln>`.

<p align="center">
  <img src="assets/kiln-update.svg" alt="kiln update : un cadre qui liste les nouveautés de chaque version traversée, lues dans le journal de kiln" width="680">
</p>
<p align="center"><i>Ce que montre <code>kiln update</code> en traversant une version, lu dans le journal de kiln.</i></p>

## Faire évoluer le modèle

Modifier `template/` sur une branche, puis la fusionner dans `develop` : les projets le
reçoivent à la version suivante, par `kiln update` (le hook de début de session le propose).
Pour essayer un modèle pas encore publié : `KILN_TEMPLATE=~/code/kiln kiln new …`.

Depuis un projet, un défaut de kiln remonte ici ([REPORT-TO-KILN] de la charte générée), par
le skill `kiln:report` :

- **pull request** vers `develop` quand la correction est claire et localisée, depuis un fork :
  kiln n'appartient qu'à antoine-tena, seul à y écrire et à fusionner ;
- **issue** quand il faut trancher entre plusieurs voies, ou qu'on ne sait pas corriger. Dans le
  doute, l'issue d'abord : une PR sur un choix pas encore fait risque d'être refaite.

Le skill vérifie d'abord que kiln est à jour et que personne ne l'a déjà signalé, rédige en
anglais sans rien de privé du projet, et ne publie qu'avec l'accord explicite de l'utilisateur :
c'est public, sous son compte GitHub.

Dans `template/`, seuls les fichiers en `.jinja` sont interprétés ; un dossier
`{% if … %}nom{% endif %}` n'existe que si la condition tient ; les questions sont dans
[`copier.yml`](../copier.yml) et les macros partagées (chaînes Python au format de ruff) dans
[`macros.jinja`](../macros.jinja).

```sh
uv run pytest            # chaque stack se génère en fichiers valides
uv run ruff check . && uv run mypy src tests
```

## Moteur de charte

`src/kiln/charter/` lit le `charter.toml` à la racine du repo. Interdictions (`[bans]` :
`django-signals`, `logging`, `django-migrations`, `constant-time`, `personal-data`, `vue-style`,
`audit-references`, `forbidden-files`, `identical-copies`, `compose-profiles`,
`forbidden-tools` : jamais pip ni docker, ni leurs fichiers), cliquets et planchers
(`[ratchets]`, `[floors]` : `file-size`, `long-routes`, `django-locks`, `occurrences`,
`test-density`), `[types]` (mypy en cliquet) et `[coverage]` (planchers de pytest-cov) ;
paramètres dans la docstring de chaque règle. Règle propre à un repo : un module listé dans
`local_rules`, avec `check(repo, params) -> list[str]`. La liste des règles non vérifiées
(`scripts/ci/unverified-rules.txt`) est recalculée par kiln à chaque `set` et `update`.

Dérogations : `kiln-waivers.toml` à la racine du repo (jamais réécrit par kiln) écarte une
règle de tout le repo ou de certains chemins (`[[waiver]]` : `rule`, `paths`, `reason`, `by`,
`since`, `until`, `renewals`). Une semaine au plus la première fois, puis un mois, trois mois,
six mois à chaque renouvellement ; `until = "never"` pour un écart permanent, toujours affiché.
`charter` liste les dérogations actives, prévient dans la seconde moitié de la période, et
échoue sur une dérogation échue, mal formée, qui ne vise plus rien, ou qui porte sur une règle
non dérogeable (`PERSONAL-DATA`, `SECRETS`, `NO-COMMIT-ON-MAIN`, `LOCKED-DEPENDENCIES`).
Une dérogation `file = "…"` (au lieu de `rule`) fige un fichier généré : `kiln update` et
`kiln set` n'y touchent plus, et `kiln update` montre ce que kiln y a changé entre les deux
versions, à reporter à la main ou à reprendre en levant la dérogation.

```toml
[[waiver]]
rule = "FILE-SIZE"
paths = ["backend/app/import_x/*.py"]
reason = "module repris tel quel du projet X, découpage prévu au T-31"
by = "antoine"
since = 2026-10-16
until = 2026-10-23
```

## Workflows réutilisables

kiln est public : ses workflows servent à n'importe quel dépôt, quel que soit son compte
(`uses: antoine-tena/kiln/.github/workflows/<nom>.yml@<tag>`, au tag exact d'une version). Jamais pip ni docker : uv pour
Python, podman pour les conteneurs (bases de test comprises), podman-compose installé par uv.

| Workflow | Rôle |
|---|---|
| `django.yml` | Backend Django : ruff, `charter types`, migrations manquantes, pytest et couverture, contre PostgreSQL et Redis lancés par podman. |
| `python.yml` | Tout projet uv (FastAPI, données, Streamlit, Dash) : ruff, mypy, pytest avec un plancher de couverture ; PostgreSQL en option. |
| `maven.yml` | Backend Java : `./mvnw verify` (compilation stricte, JUnit, plancher de couverture JaCoCo) sur un JDK Temurin. |
| `pnpm.yml` | Front pnpm (Nuxt, Next.js, Astro, Vite + React) : scripts de `package.json` dans l'ordre ; pnpm pris dans `packageManager`. |
| `charter.yml` | Règles de `charter.toml`. |
| `security.yml` | `uv audit`, `pnpm audit` et OSV-Scanner pour un projet Maven. |
| `secrets.yml` | Secrets commités (gitleaks, version figée et vérifiée). |
| `api-contract.yml` | `openapi.json` et types du front à jour du code. |
| `infra.yml` | Images (`podman build`), actionlint, shellcheck, Caddyfile, compose (podman-compose). |
| `sbom.yml` | Nomenclatures CycloneDX du back et du front. |
| `mutation.yml` | Tests par mutation (mutmut), jamais bloquants. |
| `vercel.yml` | Déploiement du front sur Vercel. |

`charte.yml`, `securite.yml` et `contrat-api.yml`, leurs noms d'avant 0.4.0, renvoient aux
nouveaux.

Actions : `actions/charter` (installe kiln et `charter` ; `actions/charte` y renvoie), `actions/services` (PostgreSQL et Redis
par podman, `DATABASE_URL` et `REDIS_URL` posées).

## CI rejouée sur le poste

Pour un dépôt dont la CI GitHub ne tourne pas (forfait épuisé, Actions coupées), `kiln ci <commit>`
la rejoue sur le poste, depuis le même `ci.yml` :

- le commit est extrait dans un worktree détaché hors du dépôt (`~/.cache/kiln/ci/`), les
  dépendances installées depuis les verrous (`uv sync --locked`, `pnpm install --frozen-lockfile`) ;
- chaque job qui appelle un workflow de kiln (`django`, `api-contract`, `charter`, `pnpm`,
  `security`) est rejoué avec ses paramètres `with:`, contre un PostgreSQL et un Redis jetables
  (podman, ports libres) ; un job écrit dans le projet l'est s'il ne fait que des `run:` ;
- le back (pytest) tourne à côté du reste ; un journal par job dans `~/.cache/kiln/ci/logs/` ;
- le verdict part en note git (`refs/notes/ci`) poussée sur origin. Sa première ligne,
  `kiln ci: success`, est ce que `scripts/ops/lib/green-ci.sh` accepte avant un déploiement ; la
  note liste aussi les jobs **non rejoués** (services propres au job, `infra`, `sbom`…).

`--skip <job>` écarte un job (noté dans le verdict), `--no-push` garde la note en local,
`--keep` laisse le worktree pour enquêter. Avec `git config statusline.ci locale`, la status
line affiche ce verdict pour la branche d'intégration. `kiln ci` ne tourne plus à chaque fusion
dans `develop` : seulement sur la branche `release/vN` d'une version (skill `kiln:release`), dont
le verdict vaut pour le commit de fusion dans `main` (mêmes fichiers). Entre deux versions, seuls
les linters rapides tournent, sur les fichiers modifiés ; la CI de GitHub (`ci.yml`) ne se
déclenche que sur les branches `release/**`.
