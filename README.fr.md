<div align="center">

<img src="docs/assets/kiln-logo.svg" alt="Le logo de kiln : un four qui rit, en pixel art" width="168">

# kiln

*L'atelier de Claude Code*

**Chaque nouveau projet démarré, et chaque vieux repo repris, comme le ferait un ingénieur expérimenté — même sans l'être soi-même.**

kiln donne à Claude Code de quoi construire des repos de qualité production, remettre les vôtres à ce niveau, et les garder ainsi.

[![PyPI](https://img.shields.io/pypi/v/kiln-cli.svg?color=c2551f)](https://pypi.org/project/kiln-cli/)
[![CI](https://github.com/antoine-tena/kiln/actions/workflows/kiln.yml/badge.svg?branch=develop)](https://github.com/antoine-tena/kiln/actions/workflows/kiln.yml)
[![Licence : MIT](https://img.shields.io/badge/licence-MIT-4c4c4c.svg)](LICENSE)

[**Référence**](docs/reference.fr.md) · [Journal des versions](CHANGELOG.md) · [Contribuer](CONTRIBUTING.md) · [English](README.md)

<img src="docs/assets/kiln-new.gif" alt="kiln new my-app pose trois questions (ce que l'on construit, sa taille, la langue de l'équipe), crée une application Django et Nuxt avec son premier commit, puis kiln check passe ruff, mypy, pytest, ESLint, les types et charter" width="820">

<i>Une vraie exécution, jouée en 1,5× et coupée pendant les attentes : <code>kiln new</code>, puis <code>kiln check</code> dans le nouveau repo.</i>

</div>

Claude Code écrit vite. Un repo a besoin de plus pour rester sain : une stack à jour, des règles
qu'un agent ne peut pas contourner à force d'arguments, une façon de travailler avec git qui
résiste à un mauvais après-midi, et quelqu'un pour l'empêcher de vieillir au quatre-vingt-dixième
jour. kiln apporte les quatre à un nouveau repo en trois questions, et à celui que vous avez
déjà, si vieux et si sale soit-il : il pose les règles, liste ce qui n'y est pas, et Claude Code
le résorbe. Puis il tient chaque repo à jour, version après version. kiln lui-même n'appelle
aucune IA et ne demande aucune clé d'API.

## Points forts

- Un nouveau repo en trois questions (ce que vous construisez, sa taille, la langue de
  l'équipe) : code, tests, linters, CI, crochets pre-commit, conteneurs et les consignes que
  Claude lit en premier.
- Un repo que vous avez déjà, si vieux soit-il : `kiln adopt` le fait suivre kiln sur une
  branche de travail, sans toucher à aucun fichier existant. Les règles sont vérifiées après
  chaque modification de Claude, le passif qu'elles relèvent est listé pour que Claude le
  résorbe, et `kiln check`, `kiln dev` et `kiln status` le servent comme un repo créé par kiln.
- `kiln update` rejoue le modèle, prend les mises à jour compatibles des dépendances, convertit
  ce qu'une version a renommé et lance vos contrôles avant que vous ne commitiez. `--rehearse`
  l'essaie d'abord sur un clone jetable, `--all` met à jour chaque repo du dossier de code.
- `charter`, le contrôleur de règles de kiln, vérifie chaque fichier que Claude modifie en
  0,15 s environ : outils bannis, noms, tailles de fichiers, données personnelles dans les logs.
  Des compteurs qui ne peuvent que baisser (cliquets) et des seuils de couverture tiennent à
  chaque commit et en CI. Une dérogation demande une raison et une date de fin.
- `kiln grid` liste les pratiques que kiln défend, chacune avec sa raison, ses sources
  (vérifiées et datées) et sa façon d'être détectée. `kiln score` y mesure n'importe quel repo
  en une seconde environ, sans jeton : une note sur 100, une par pilier, et les écarts à
  combler d'abord.
- Des skills pour les worktrees, les fusions, les versions et les relectures ; des hooks qui
  tiennent Claude à l'écart de `main` et `develop` ; une status line qui montre la CI, les
  tickets et la production.
- La CI d'un repo privé tourne sur votre poste (`kiln ci`, son verdict gardé en note git) et ne
  coûte aucune minute GitHub ; celle d'un repo public tourne sur GitHub, où c'est gratuit.

## Installation

```sh
uv tool install kiln-cli     # la commande est kiln ; uv installe Python 3.14 s'il manque
```

Ou pour essayer sans rien installer : `uvx kiln-cli new mon-app` pour un nouveau repo,
`uvx kiln-cli adopt` dans un repo que vous avez déjà. macOS, Linux et Windows par WSL ;
[pnpm](https://pnpm.io/) pour les fronts JavaScript, [podman](https://podman.io/) pour les
conteneurs.

## Démarrage

Un nouveau repo :

```console
$ kiln new mon-app            # trois questions, puis un dépôt GitHub privé (--no-github : local)
$ cd mon-app && kiln dev      # les serveurs de la stack, sorties préfixées par service
$ kiln check                  # ruff, mypy, pytest, ESLint, types, puis charter
$ claude                      # Claude Code, avec les règles, skills et hooks de kiln
```

Un repo que vous avez déjà, sur une branche de travail :

```console
$ git switch -c chore/kiln-adopt
$ kiln adopt                  # les règles et un backlog, aucun fichier touché ; puis le passif
$ claude                      # Claude Code le résorbe, avec les règles, skills et hooks de kiln
```

## Ce que vous obtenez

| Vous construisez | Backend | Frontend |
|---|---|---|
| Une application complète (`app`) | Django + Django Ninja | Nuxt + Vue |
| Une API (`api`) | FastAPI | — |
| Un site de contenu (`site`) | — | Astro |
| Un tableau de bord de données (`dashboard`) | polars, marimo, Plotly | Streamlit |
| Une analyse de données (`analysis`) | polars, marimo, Plotly | — |
| Un outil en ligne de commande (`cli`) | Python, installable | — |

Next.js, Dash et Java 25 + Maven sont là aussi, et les tests de kiln génèrent et vérifient chaque
combinaison. Django et Nuxt sont complets ; les autres stacks sont figées mais entretenues : les
nouvelles règles de la grille vont d'abord à Django et Nuxt.

Chaque repo reçoit aussi uv, pnpm et podman (jamais pip, npm ni docker), une CI qui appelle les
workflows réutilisables de kiln, des branches `main` et `develop` protégées, un `docs/backlog/`
de tickets typés, et une taille (`spark`, `ember`, `flame` ou `blaze`) qui règle le cérémonial
qu'il porte. Une application Django peut partir sur un VPS durci (Caddy, conteneurs en lecture
seule, retour arrière automatique, sauvegardes restaurées), un front Nuxt sur Vercel.

## Tenu à jour

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/assets/kiln-flow-dark.svg">
    <img src="docs/assets/kiln-flow-light.svg" alt="Une version, tous les repos à jour : kiln, puis une candidate essayée sur les repos de kiln, la version sur PyPI, une répétition sur un clone de votre repo, puis kiln update la fusionne seulement si les contrôles passent" width="820">
  </picture>
</p>

Une version de kiln sort d'abord en candidate, taguée seulement quand sa CI est verte sous Linux
et macOS, y compris une mise à jour depuis chaque version depuis la v0.3.0, par un outil
installé. Elle est promue quand la candidate suivante est prête, puis répétée sur un clone de
chaque repo avant que `kiln update --all` la fusionne, un worktree par repo. Les repos citent les
workflows de kiln à la version exacte qu'ils suivent : rien ne leur arrive entre deux versions,
et `kiln update` montre les nouveautés de chaque version qu'il traverse. Un repo repris par
`kiln adopt` suit les workflows de kiln à la dernière version, que `kiln update` fait avancer
aussi.

## La grille

<p align="center">
  <img src="docs/assets/kiln-rule.svg" alt="kiln grid pinned-actions : pourquoi la règle tient, son thème, sa portée et son niveau, sa détection et sa correction, sa source vérifiée à une date, et comment y déroger" width="820">
</p>
<p align="center"><i><code>kiln grid &lt;ID&gt;</code> : une règle en entier, avec sa raison, une source vérifiée à une date, et la façon pour un repo d'y déroger.</i></p>

Un petit fichier TOML par règle, sur deux axes : son thème (chaîne d'approvisionnement,
conteneurs, tests…) et sa portée (universelle, un langage, un framework, un outil). Chacune dit
pourquoi, cite des sources pesées dans un ordre fixe (documentation officielle, alertes de
sécurité, études mesurées, données d'adoption, blogs) et porte un niveau du Technology Radar de
Thoughtworks : adopter, essayer, évaluer, abandonner. Seules les règles adoptées comptent :
40 (chaîne d'approvisionnement, CI, conteneurs, tests, normes de code, sécurité de Django et de
Vue), chacune passée sur deux vrais repos pour traquer les faux positifs ; 95 brouillons
attendent derrière `kiln grid --level assess`.
Chaque règle notée a un repo qui la respecte et un qui l'enfreint.

## Comparé à Copier et cookiecutter

kiln repose sur [Copier](https://copier.readthedocs.io) : chaque projet garde son
`.copier-answers.yml`, et Copier seul fonctionne toujours dessus. kiln ajoute ce qui vient
après le premier jour, et y laisse un peu d'étendue.

| | cookiecutter | Copier | **kiln** |
|---|:---:|:---:|:---:|
| Générer un projet | ✅ | ✅ | ✅ |
| N'importe quel langage ou framework | ✅ | ✅ | ❌ |
| Des modèles de la communauté pour démarrer | ✅ | ✅ | ❌ |
| Appliquer les évolutions du modèle aux projets existants | ❌ | ✅ | ✅ |
| Choisir la stack d'après ce que l'on construit | ❌ | ❌ | ✅ |
| Changer de stack plus tard (`kiln set frontend=nuxt`) | ❌ | en partie | ✅ |
| Mettre à jour les dépendances et lancer les contrôles d'un coup | ❌ | ❌ | ✅ |
| Répéter, puis mettre à jour tous ses repos d'un coup | ❌ | ❌ | ✅ |
| Des workflows de CI partagés, cités à une version | ❌ | ❌ | ✅ |
| Un moteur de règles aux dérogations datées (`charter`) | ❌ | ❌ | ✅ |
| Skills, hooks et consignes pour Claude Code | ❌ | ❌ | ✅ |

kiln a des opinions, exprès. Pour un moteur de gabarits neutre, prenez Copier ; pour une façon
de travailler qui reste entretenue, prenez kiln, ou forkez-le et faites vôtres ses opinions.

## Référence

Chaque commande et chaque option, chaque clé de `kiln set`, les workflows réutilisables, les
plugins Claude Code, le moteur de charte et la façon dont kiln sort ses versions :
[**docs/reference.fr.md**](docs/reference.fr.md). Dans un terminal, `kiln <commande> --help`.

## État

kiln fait tourner chaque jour une poignée de vrais repos, dont un en production. Un seul
mainteneur l'écrit avec Claude Code, sous les règles mêmes qu'il donne à vos repos. Il numérote
ses versions comme Claude Code : en `0.x`, chaque version monte le correctif, les changements
cassants viennent en tête du [journal](CHANGELOG.md) et `kiln update` les convertit ; la mineure
marque une étape. Le semver strict commence à la 1.0. La suite est pour les repos que vous avez
déjà : n'importe quel repo Django ou Nuxt noté face à la grille en quelques secondes, puis mis à
niveau par script partout où un script le peut (v0.5.0).

## Contribuer

Les issues et les pull requests sont bienvenues : voir [CONTRIBUTING.md](CONTRIBUTING.md), le
[code de conduite](CODE_OF_CONDUCT.md), et l'étiquette
[`good first issue`](https://github.com/antoine-tena/kiln/labels/good%20first%20issue) pour
commencer. Dans un repo kiln, `/kiln:report` transforme un défaut de kiln en issue ou en pull
request prête à poster, envoyée seulement avec votre accord. Si kiln vous fait gagner du temps,
une étoile aide d'autres à le trouver.

## Licence

[MIT](LICENSE)
