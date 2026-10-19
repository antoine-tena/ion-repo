# kiln : le marché et la concurrence

> Partie de [l'idée de projet](README.md). Brouillon interne du 17 octobre 2026.

## Le paysage en octobre 2026

| Acteur | Ce qu'il fait | Ce qui manque pour notre cible |
|---|---|---|
| Dependabot, Renovate | Versions, quarantaine en option | Ne touche pas aux méthodes ni aux normes |
| Copier, cruft (et le gestionnaire Copier de Renovate) | Mise à jour d'un modèle de repo | Pas de grille, pas de conversions de méthodes |
| AWS Transform « Continuous Modernization » (aperçu depuis le 17 juin 2026) | Dette technique, dépendances en fin de vie et frameworks dépassés, sur des milliers de repos | Grandes entreprises, écosystème AWS |
| Moderne / OpenRewrite (30 M$ levés) | Migrations par recettes, multi-repo payant | Grandes entreprises, Java d'abord, Python depuis peu |
| GitHub Copilot (modernisation d'applications) | Montées Java et .NET | Deux écosystèmes seulement |
| Claude Code (`/doctor`, `/skill-doctor`, plugin `claude-code-setup`) | Santé de la configuration Claude | Ne touche pas au reste du repo |
| sp-repo-review (Scientific Python) | Liste de bonnes pratiques Python scientifique | Vérifie sans appliquer |
| libyear, depwatch | Retard des dépendances | Versions seulement |
| deptry, FawltyDeps, knip, vulture | Dépendances et code inutilisés | Détection seulement |
| ponytail (146 k étoiles) | Consigne aux agents d'écrire moins de code | Agit à l'écriture, pas sur l'existant |
| ECC, Superpowers | Packs de configuration pour agents | Figés à l'installation |
| Technology Radar (Thoughtworks) | Opinions publiées deux fois par an | Pas exécutable |

**Ce qui manque :** un outil ouvert et gratuit, avec une grille de méthodes et de normes tenue à
jour, qui s'applique avec preuves aux repos des petites structures et qui les rend lisibles par
Claude.

Les grandes entreprises rachètent souvent les outils de développement qui réussissent plutôt que
de les reconstruire : OpenAI a racheté Astral (uv, ruff) en mars 2026, Anthropic l'équipe de Bun
en décembre 2025.

## Ce qui nous protège des géants

Une niche ne protège pas, et elle prive aussi d'utilisateurs. Ce qui protège un petit projet,
ce sont les endroits où les grands acteurs ne peuvent pas aller, à cause de leurs propres
intérêts.

| Acteur | Pourquoi il ne le fera pas |
|---|---|
| Anthropic | C'est hors de Claude Code, fastidieux stack par stack, et un contrôle par script ne consomme pas de jetons. Seule la santé de la configuration Claude (`/doctor`) est sur son terrain |
| Dependabot, Renovate | Leur métier est de monter des versions, pas de retirer des dépendances ni de changer de méthode |
| AWS, Moderne, GitHub | Ils vendent aux grandes entreprises. Une association ou un labo n'appellera jamais leur service commercial |
| Hébergeurs | Ils hébergent, ils n'entretiennent pas le code |
| Startups financées | Les petites structures ne paient pas : pas d'argent à lever sur cette cible |

C'est une corvée que tout le monde subit, mais que personne ne veut prendre en charge. Stripe a
gagné de la même façon sur les paiements. Il ne faut pas confondre avec « personne n'en veut » :
zéro concurrence, c'est souvent zéro demande. Ici, la demande existe (mesurée sur un repo d'université).

**Le vrai risque** est une startup qui lèverait des fonds sur le même angle. La protection face à
elle : la vitesse et l'open source. Et si un grand acteur s'y intéresse, il rachète plus souvent
qu'il ne reconstruit (Astral, Bun), ce qui serait une réussite.

## Ce qui fait percer un outil : leçons d'uv et du marché

**uv n'était pas une idée nouvelle.** Poetry, pip-tools, pipx et pyenv existaient déjà, et rye
avant lui. Il a gagné par l'exécution :
- 10 à 100 fois plus rapide ;
- un seul outil à la place de plusieurs ;
- compatible avec l'existant (`uv pip`), donc adoptable sans rien migrer ;
- la crédibilité acquise avec ruff.

Et la vitesse a changé les usages : environnements jetables, `uv run`.

**Les projets qui ont explosé en 2026 autour de Claude Code** ont trois points communs :
1. une installation en une ligne, souvent pour plusieurs agents à la fois ;
2. un chiffre dans l'accroche (« −54 % de code », « 60 à 95 % de jetons en moins ») ;
3. une douleur ressentie dès la première session.

Les grosses collections marchent aussi, mais ce créneau est saturé.

**La formule pour kiln :** unifier des outils épars (Dependabot, linters, modèles, vérificateurs
comme sp-repo-review) et afficher un chiffre spectaculaire, comme le score avant/après d'un repo
(le repo d'association de 58 % à 100 %).

**La diffusion pèse autant que l'idée.** ECC a percé après une victoire en hackathon et dix mois
d'usage quotidien, Superpowers grâce à la réputation de son auteur. kiln n'a pas encore été lancé
publiquement : le lancement est fixé au mercredi 11 novembre 2026 à 16 h, une fois la v0.5.0
promue (ticket T-03), et il comptera autant que le produit.

## Annexe : les besoins des utilisateurs de Claude en octobre 2026

Synthèse d'une analyse de marché faite le 17 octobre 2026. Elle nourrit surtout le thème
« développement assisté par IA » de la grille et le pilier « lisible par Claude ». Beaucoup de
sources sont secondaires ; l'enquête JetBrains est la plus solide.

**Le contexte :**
- **Adoption.** Claude Code est utilisé au travail par 39 % des développeurs professionnels
  (18 % en janvier, 47 % aux États-Unis). 90 % utilisent un agent chaque semaine, 68 % chaque
  jour, et 70 % utilisent deux à quatre outils d'IA à la fois.
- **Modèles.** Opus 5.5 est sorti le 22 septembre (4 $/20 $ par million de jetons, 40 % moins
  cher à l'usage qu'Opus 5), Sonnet 5.5 le 28.
- **Produits.** Cowork a été fondu dans Claude le 16 septembre. Les mods de Claude Code sont
  arrivés le 1er octobre : 1 740 mods publics trois jours plus tard.
- **Complexité.** Claude Code sort une version presque chaque jour (2.1.302) et compte 243 clés
  de réglages, 391 variables d'environnement et 33 événements de hooks.

**Les besoins, du plus fort au plus faible :**
1. **Vérifier le code des agents** : voir le goulot de la relecture dans [le problème](README.md#le-problème).
2. **Maîtriser les jetons.**
   - En mars, un fil « 20x max usage gone in 19 minutes » a dépassé 330 commentaires.
   - Sur Hacker News, on reproche à Claude Code d'envoyer 33 000 jetons avant même de lire la
     demande, contre 7 000 pour OpenCode.
   - En entreprise, 62 % ont eu une facture surprise, et les chaînes multi-agents gaspillent
     44,5 % de leurs jetons.
   - C'est la catégorie qui fait le plus d'étoiles : ponytail 146 k, cc-switch 137 k, caveman
     108 k, rtk 82 k, headroom 74 k.
3. **Imposer une méthode** : Superpowers (environ 290 k étoiles), ECC (268 k). Mais l'étude de
   l'ETH Zurich montre que les fichiers de contexte n'améliorent pas la réussite et coûtent 20 à
   23 % de jetons en plus.
4. **Sécuriser la chaîne des agents.**
   - Clinejection (17 février) : un titre d'issue piégé a compromis le paquet npm de Cline.
   - Fuite du code source de Claude Code (31 mars), suivie de la découverte d'un contournement
     des règles d'interdiction.
   - 1 184 skills malveillants recensés sur ClawHub.
   - 15,4 % de 2 660 configurations d'agents publiques sont exposées, et un quart des serveurs MCP
     ne sont pas épinglés à une version.
   - Les mods ne sont pas isolés.
   - Dans le grand public, 380 000 applications « vibe-codées » sont exposées sur le web, dont
     environ 5 000 qui laissent fuir des données.
5. **Stabilité et liberté de choisir son agent.**
   - Un changement par défaut est sorti sans annonce : `AskUserQuestion` approuvait tout seul au
     bout de 60 secondes.
   - Des fonctionnalités ont été retirées (TodoWrite, Glob/Grep).
   - AGENTS.md est adopté par plus de 60 000 projets, SKILL.md est lu par plus de 32 outils, mais
     les chemins diffèrent d'un outil à l'autre.
6. **Comprendre et se souvenir** : graphify (122 k étoiles), claude-mem (95 k).
7. **Signaux plus faibles** :
   - apprendre à se servir des agents : les utilisateurs de plus de six mois réussissent mieux ;
   - orchestrer plusieurs agents : orca, 79 k étoiles ;
   - éviter l'interface qui sent l'IA : ui-ux-pro-max, 131 k ;
   - les usages hors code : career-ops, 73 k.

**La tendance de fond :** le « harness engineering », c'est-à-dire concevoir l'environnement, les
contraintes et les boucles de retour qui rendent un agent fiable. OpenAI l'a défini en février
2026. La recherche montre qu'un harness qui s'améliore à partir de mesures gagne 7 points de
réussite et économise 12 % de jetons.

**Ce que kiln en retient pour la grille :** épingler les serveurs MCP, éviter les autorisations
trop larges, garder des fichiers de contexte courts et écrits à la main, et rendre les repos
lisibles par n'importe quel agent.

## Sources

**Analyse de marché (annexe) :**
- [Pragmatic Engineer, outils d'IA en 2026](https://newsletter.pragmaticengineer.com/p/ai-tooling-2026)
- [Dépôts Claude Code par étoiles](https://githublb.vercel.app/topic/claude-code)
- [Meilleurs plugins Claude Code](https://designrevision.com/blog/best-claude-code-plugins)
- [Claude Code en octobre 2026](https://angelo-lima.fr/en/claude-code-cheatsheet-october-2026-state-of-play-en/)
- [Opus 5.5](https://www.anthropic.com/claude-opus-5-5)
- [Mods non isolés](https://www.dsebastien.net/2026-10-04-claude-code-mods-claude-code-is-now-programmable-and-mods-arent-sandboxed/)
- [The Register, quotas](https://www.theregister.com/2026/03/31/anthropic_claude_code_limits/)
- [Coûts de l'IA en entreprise](https://www.mavvrik.ai/state-of-ai-cost-governance-report/)
- [Expositions de configuration des agents](https://arxiv.org/abs/2609.07360)
- [Risques de sécurité des agents en 2026](https://blog.cyberdesserts.com/ai-agent-security-risks/)
- [Failles du vibe coding](https://vibe-eval.com/updates/2026-ai-coding-security-report/)
- [Portabilité des skills](https://codemyspec.com/blog/skill-portability)
- [Harness engineering](https://www.augmentcode.com/guides/harness-engineering-ai-coding-agents)
- [Agentic Harness Engineering](https://arxiv.org/abs/2604.25850)
- [Utilisateurs expérimentés de Claude](https://ppc.land/experienced-claude-users-succeed-10-more-and-the-gap-is-widening/)
- [CMU et Stanford, goulot de la relecture](https://www.matthewswong.com/en/blog/ai-code-review-bottleneck-cmu-stanford-silent-approvals/)

**Modernisation :**
- [AWS Transform, modernisation continue](https://aws.amazon.com/blogs/migration-and-modernization/aws-transform-from-migration-to-continuous-modernization/)
- [Moderne lève 30 M$](https://refreshmiami.com/news/moderne-raises-30m-to-continue-driving-mass-scale-code-modernization/)
- [OpenRewrite et Moderne](https://moderne.ai/blog/overview-of-openrewrite-and-moderne)
- [GitHub Copilot et la modernisation](https://theaieconomy.substack.com/p/github-copilot-modernizes-java-dotnet)
- [Catégorie Gartner](https://www.gartner.com/reviews/market/ai-augmented-code-modernization-tools)
- [Renovate, gestionnaire Copier](https://docs.renovatebot.com/modules/manager/copier/)
- [Thoughtworks Technology Radar](https://www.thoughtworks.com/radar)

**Claude Code :**
- [Ce que vérifie `/doctor`](https://improveandrepeat.com/2026/10/keep-your-claude-code-configuration-healthy/)
- [`/skill-doctor`](https://www.implicator.ai/anthropic-claude-code-skill-doctor-context-audit/)

**Outils voisins :**
- [sp-repo-review](https://pypi.org/project/sp-repo-review)
- [libyear](https://www.npmjs.com/package/libyear)
- [depwatch](https://github.com/fabiocicerchia/depwatch)
- [deptry](https://github.com/osprey-oss/deptry)
- [FawltyDeps](https://github.com/tweag/FawltyDeps)
- [ponytail](https://www.mindstudio.ai/blog/ponytail-ai-coding-minimalism-plugin)
- [ECC](https://pasqualepillitteri.it/en/news/4878/everything-claude-code-ecc-agent-harness-os)
- [Superpowers](https://emelia.io/de/hub/superpowers-claude-code-framework)

**Rachats :**
- [OpenAI rachète Astral](https://simonwillison.net/2026/Mar/19/openai-acquiring-astral)
