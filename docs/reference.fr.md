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
- la CI (`.github/workflows/ci.yml`), qui appelle les workflows réutilisables de kiln : sur GitHub à chaque
  push pour un dépôt public (gratuit et illimité), sur le poste par `kiln ci` pour un dépôt privé
  (`ci_runner: local` : aucune minute GitHub, dont le plan gratuit ne donne que 2 000 par mois) ;
  `kiln update` choisit d'après la visibilité du dépôt, `kiln set ci_runner=github` ou `local` change ;
- le suivi du travail, d'office : `docs/backlog/` (`backlog.md`, `rejected.md`, `urgent.md`,
  en anglais, skill `kiln:backlog`), que la status line de Claude Code compte ;
- les réglages de la status line propres au repo (`statusline_ci`, `prod_health_url`), posés en
  `git config statusline.*` par `kiln install`, `kiln new` et `kiln set` ;
- d'office (`--no-github` pour s'en passer) : le dépôt GitHub privé, avec `main` verrouillée (seul le commit initial)
  et `develop` protégée (ni suppression ni réécriture), et les correctifs de sécurité Dependabot ;
- en option : les conteneurs podman.

Les plugins Claude Code vivent dans [`plugins/`](../plugins/), catalogue `kiln`
([`.claude-plugin/marketplace.json`](../.claude-plugin/marketplace.json)) :

- `kiln`, pour tous les projets, installé au niveau utilisateur : skills `worktree`, `merge`
  (fusion dans `develop`), `release` (release/vN, contrôle complet, annonce, main tagué,
  déploiement), `cleanup` (ménage des worktrees), `review` (commits et diff d'une branche relus
  et rangés avant la fusion, dépôt entier avant une version), `backlog`, `update` (l'outil kiln
  et ses plugins, puis le repo ouvert), `adopt` (`kiln adopt` dans un repo existant, passif de la
  charte trié avec l'utilisateur), `report` (un défaut de kiln remonté en issue ou en PR, avec l'accord de l'utilisateur), `contribution` (la PR d'un contributeur extérieur : code relu avant d'en rien lancer, tri, revue, fusion qui le crédite, rien publié sans accord), `good-first-issues` (un petit stock d'issues `good first issue` tiré du backlog et réservé aux contributeurs extérieurs, regarni à chaque fusion), `token` (le jeton d'un service collé une fois dans un dossier `.<service>/` ignoré par git, jamais affiché) ; hooks garde de branche (`branch_guard.py`, et refus d'un message de commit signé Claude), fichiers protégés (`protect_files.py`), contrôle du fichier
  modifié (`check_file.py`), questions à l'ouverture de session (`session_start.py`, logo et nouveautés au premier message par `first_prompt.py`, et CI rouge de la branche d'intégration signalée à Claude, une exécution que GitHub n'a jamais démarrée distinguée d'un échec du code) : dans un repo kiln, sa mise à jour (l'outil kiln s'il
  est en retard sur GitHub, puis le repo par `kiln update` ; un « non » repousse la question de
  5, 10, 30 puis 50 sessions, après quoi désinstaller kiln ou délier le repo est proposé) ; dans
  un repo à soi qui ne suit pas kiln, son adoption (« Oui », « Plus tard », « Jamais pour ce
  repo »), dès la 3e session, au plus une fois toutes les 10 sessions du poste. Toutes passent
  par `reminders.py` : une note de bienveillance du poste monte à chaque « oui » et baisse à
  chaque « non », et étire ou raccourcit tous les délais (doublés au plus méfiant, de moitié au
  plus enthousiaste) ; `git config kiln.update-check false` pour s'en passer, sorties de commandes condensées par [rtk](https://github.com/rtk-ai/rtk) (`rtk.py`) quand il
  est installé (`mise use -g github:rtk-ai/rtk`, sans `rtk init` : le hook est fourni ici) ; MCP context7 ; status line commune (`plugins/kiln/scripts/statusline.py`,
  en anglais, aux couleurs de kiln), posée par `kiln install` dans `~/.claude/settings.json` ; son
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

Installation : `claude plugin marketplace add antoine-tena/kiln`, puis
`claude plugin install kiln@kiln`.

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
| `kiln adopt` | Fait suivre kiln à un repo existant qu'il n'a pas généré, sur une branche de travail : `charter.toml` (envergure par `--size`, règles valables partout, vérifiées après chaque édition), `docs/backlog/` s'il n'existe pas, puis le passif que la charte relève. Ne touche à aucun fichier existant ; le repo apparaît dans `kiln status` comme adopté, `kiln update` le laisse. |
| `kiln publish` | Crée le dépôt GitHub privé et protège ses branches, pour un projet généré sans `gh`. |
| `kiln install` | Prépare un poste après un clone : outils (pre-commit avec pre-commit-uv, podman-compose), dépendances, `backend/.env`, migrations, pre-commit. Relançable. |
| `kiln dev` | Lance les serveurs de la stack, leurs sorties entrelacées et préfixées par service en couleur (`django │ …`) ; `--containers` : toute la pile dans podman. |
| `kiln check` | Ruff, mypy et pytest pour chaque projet Python, ESLint et les types côté front, puis la charte. |
| `kiln ci [commit]` | Rejoue sur le poste la CI du `ci.yml` pour ce commit (défaut `HEAD`) et pose le verdict en note git sur origin, que le script de déploiement accepte comme une CI verte. `--status` : le verdict seul. Voir « CI rejouée sur le poste ». |
| `kiln contract` | Django + Nuxt : exporte `openapi.json` depuis le code, puis régénère les types du front (`app/types/api.d.ts`). `kiln update` le fait aussi. |
| `kiln waive [RÈGLE\|fichier]` | Déroge à une règle de kiln (`--paths`, `--reason`, `--upstream`), ou fige un fichier généré que `kiln update` ne touchera plus ; `--renew` passe au palier suivant (une semaine, un mois, trois mois, six mois), `--permanent` sans échéance. Sans argument : liste les dérogations. Voir [Moteur de charte](#moteur-de-charte). |
| `kiln set` | Dans un repo : sans argument, affiche ses paramètres ; `kiln set clé=valeur…` les change : le repo est régénéré, un framework retiré emporte ses fichiers. Clés : `name`, `title`, `description`, `project_type`, `size`, `backend`, `frontend`, `podman`, `language` (et par usage : `language_comments`, `language_commits`, `language_docs`, `language_tickets`, `language_ui`), `owner`, `team`, `java_package`, `timezone` (fuseau des notions calendaires ; les dates sont stockées en UTC), `serena`, `deploy`, `vps_host`, `api_domain`, `site_url`, `deploy_branch`, `frontend_deploy`, `north_star`, `ci_runner`, `statusline_ci`, `prod_health_url`. Hors d'un repo, ou avec `--global` : les réglages du poste (`system`, `owner`, `team`, `code_dir`, `channel`, `statusline`, dans `~/.config/kiln/config.toml`). |
| `kiln update` | Évolutions du modèle, mises à jour compatibles des dépendances, puis contrôles. `--major` : versions majeures comprises. `--no-template`, `--no-deps` pour n'en faire qu'une partie. `--rehearse` : la mise à jour jouée d'abord sur un clone jetable, le repo intact, seul le bilan revient. Dans un repo adopté (`kiln adopt`), seules les références aux workflows de kiln avancent à la dernière version publique, entrées vérifiées. |
| `kiln update --all` | Tous les repos kiln du dossier de code (`~/code`, réglable par `code_dir`) : pour chacun, un worktree depuis la branche d'intégration, la mise à jour, des commits de dix fichiers au plus, puis la fusion directe dans l'intégration (commit de fusion poussé) ; contrôles en échec, la branche est poussée sans être fusionnée. L'arbre principal ne change jamais de branche. `--all --rehearse` : chaque mise à jour répétée sur un clone, rien n'est touché, un bilan par repo. |
| `kiln grid [ID]` | La grille : les pratiques que kiln tient pour les meilleures aujourd'hui, un petit fichier TOML par règle, avec son pourquoi, ses sources vérifiées et datées, son niveau (adopt, trial, assess, hold), sa détection et sa correction. `--theme`, `--scope`, `--level` filtrent ; un identifiant montre la règle en entier, et comment y déroger. |
| `kiln score [CHEMIN]` | N'importe quel repo, créé par kiln ou non, mesuré face aux règles notées de la grille en une seconde environ, hors ligne et sans jeton : une note sur 100 et une par pilier (chaque règle qui s'applique pèse autant ; celles hors des stacks du repo, ou sans rien à regarder, sont laissées de côté), les trois écarts à combler d'abord, puis chaque écart avec sa raison, son emplacement, sa source et ce qui le comble. Les règles qui font l'objet d'une dérogation (`kiln-waivers.toml`) sont montrées à part. `--all` liste chaque règle et chaque emplacement, `--json` le rapport (schéma 1), `--badge` un badge pour le README, `--online` rafraîchit les dates de fin de vie depuis endoflife.date. Rien n'est écrit dans le repo. |
| `kiln doctor` | Diagnostic du poste (git, uv, gh connecté, pnpm, podman, Java, pre-commit, version de kiln, plugin Claude, configuration) et du repo courant (version du modèle, crochet pre-commit, dépendances, `backend/.env`) : ✓, ! à regarder ou ✗ bloquant, chaque fois avec la commande qui corrige. Ne modifie rien. |
| `kiln completion bash` | Script de complétion bash tiré des commandes et options de kiln ; l'activer par `eval "$(kiln completion bash)"` dans `~/.bashrc`. |
| `kiln status` | État des repos kiln du dossier de code : branche, arbre propre ou non, version du modèle (`v0.4.0 → v0.4.2` en retard), dérogations (`!` si l'une est échue), stack ; puis les règles dérogées, par nombre de repos. |
| `kiln version` | Dans le dépôt de kiln : dernière version publique, candidates (âge, repos qui les ont adoptées, prêtes à promouvoir), numéro de la prochaine et tickets du plan (`docs/backlog/`) qui restent avant elle. `kiln version cut` : branche `release/vX.Y.Z`, ébauche de la note de version et numéros, puis (une fois la note relue) contrôles, CI de GitHub attendue et, au vert seulement, tag `-rc.N` ; `kiln version promote` : tag public sur la dernière candidate dont la CI est verte, fusion dans `main` et `develop` (PyPI et GitHub Release suivent). |
| `charter` | Vérifie le repo contre son `charter.toml` (`charter --detail`, `charter --unverified`, `charter types`, `charter coverage`, `charter file <chemin>`). |

`set` et `update` travaillent sur une branche, arbre propre ; les conflits entre le modèle et une
modification locale sont marqués dans le fichier (`<<<<<<<`). Relire, commiter, fusionner dans
`develop` (skill `kiln:merge`, sans PR ni approbation à attendre).

`new`, `install`, `update` et `status` s'ouvrent sur une bannière : un four en pixel art, la
version de kiln, la commande, le projet (envergure, stack) et son dossier. Hors terminal ou avec
`NO_COLOR`, une seule ligne de texte à la place. `kiln` seul (ou `kiln --help`) ouvre l'écran
d'accueil : commandes par section et exemples ; les étapes, succès, erreurs et le tableau de
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

Backends : `django`, `fastapi`, `data`, `cli`, `java`, `none`. Frontends : `nuxt`, `next`, `astro`,
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
qui casse quelque chose est signalée avant le commit. Dependabot ne propose que les correctifs de
sécurité.

## Versions

kiln numérote ses versions `vMAJEUR.MINEUR.CORRECTIF`, comme Claude Code : en 0.x, chaque
version monte le correctif, changements cassants compris (`0.4.1 → 0.4.2`), signalés en tête de
leur note et convertis par `kiln update` ; la mineure ne monte que pour une étape
(`kiln version --minor`). À partir de 1.0, semver strict.
Le travail s'intègre dans `develop` ; `main` ne reçoit que des versions.

- **Candidate** (`v0.4.2-rc.1`) : tirée de `develop` sur une branche `release/v0.4.2`, avec son
  entrée en tête de [`CHANGELOG.md`](../CHANGELOG.md). Seuls les postes au canal `internal` la
  suivent (`kiln set channel=internal`).
- **Promotion** (`v0.4.2`) : dès qu'une candidate plus récente est prête (pas de délai fixe :
  c'est la suivante prête qui évite le correctif d'urgence), le même commit est tagué et fusionné
  dans `main`. `kiln version` montre les candidates, leur âge, qui les a adoptées, lesquelles
  sont prêtes et le numéro de la prochaine.
- **Clients** : ils se mettent à jour à chaque version, correctif compris. Le hook de début de
  session propose l'outil puis le repo ; `kiln update` applique la version, montre ses
  nouveautés et fait avancer le tag auquel le `ci.yml` du repo cite les workflows de kiln.
- **Outil** : `uv tool install kiln-cli` prend les versions promues, publiées sur PyPI par le
  workflow `pypi.yml` au tag `vX.Y.Z` ; `uv tool install git+https://github.com/antoine-tena/kiln@<tag>`
  prend aussi les candidates ;
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
| `pnpm.yml` | Front pnpm (Nuxt, Next.js, Astro) : scripts de `package.json` dans l'ordre ; pnpm pris dans `packageManager`. |
| `charter.yml` | Règles de `charter.toml`. |
| `security.yml` | `uv audit` et `pnpm audit`. |
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
le verdict vaut pour le commit de fusion dans `main` (mêmes fichiers). Entre deux versions, le
typage se joue avant chaque push (crochet pre-push de `.pre-commit-config.yaml`).
