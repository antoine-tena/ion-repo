# kiln : la grille de référence

> Partie de [l'idée de projet](README.md). Brouillon interne du 17 octobre 2026.

## Le cœur difficile : la grille de référence

Pour chaque pratique, la grille dit :
- ce qu'elle est et comment la détecter ;
- **pour qui** : profil solo ou association, PME, université, grande entreprise ;
- **quand l'adopter** : critères de bascule ;
- la conversion à appliquer et la preuve à fournir.

Les niveaux reprennent ceux du Technology Radar de Thoughtworks : adopter, essayer, évaluer,
abandonner.

**Le meilleur n'est pas le plus récent.** Exemples mesurés le 17 octobre 2026 :
- **Python 3.15** est sorti le 9 octobre, mais Django 6.1 ne va que jusqu'à 3.14, et onnxruntime
  n'a pas encore de version pour 3.15 : attendre est le bon choix.
- **ty**, le vérificateur de types d'Astral, est encore en bêta : mypy reste le meilleur choix.
- **Vue 3.6** n'est qu'en version candidate.
- **Node 26** ne devient LTS que le 28 octobre.
- **SLO et drapeaux de fonctionnalité** sont des méthodes de grande entreprise, peut-être de trop
  pour une association.

Tenir cette grille à jour pour le monde entier est un travail permanent : notes de version,
endoflife.date, registres, Technology Radar, études. **C'est là qu'est la valeur**, et c'est ce
qu'un agent seul ne fait pas.

## Classer toutes les règles : thèmes et portées

Quatre niveaux ne suffisent pas : où ranger les skills de Claude, les conteneurs, les workers,
l'asynchronisme ? Chaque règle se range sur **deux axes**, et porte quelques attributs.

**Axe 1 : le thème**, c'est-à-dire de quoi parle la règle. Liste de départ, tirée du repo d'association :

| Thème | Exemples dans le repo d'association |
|---|---|
| Structure du repo | carte du repo, une app Django par domaine, un dossier par domaine côté Nuxt |
| Normes de code | [TAILLE-FONCTION], [NOMS-INTERDITS], [CASSE], [ZERO-MAGIE] |
| API, contrats et typage | [TYPAGE-STRICT], [CONTRAT-FIGE], piliers III (contrats), IX (évolution de l'API) et XV (contrat front/back) |
| Architecture | piliers I (isolation des couches) et VI (domaine) |
| Données et migrations | piliers II (persistance) et XI (migrations) |
| Tâches de fond | pilier XII (outbox transactionnelle), Celery, planificateur |
| Concurrence et asynchronisme | pilier VII (concurrence) |
| Cache | pilier XIII (cache) |
| Erreurs et journaux | pilier V (erreurs sémantiques), logs structurés |
| Sécurité applicative | piliers IV (zero-trust) et XIV (cryptographie), [CSP-NONCE], [COOKIES], [SECRETS] |
| Données personnelles | [DONNEES-PERSO], export et anonymisation RGPD |
| Chaîne d'approvisionnement | [DEPENDANCES-FIGEES], [AUDIT-VULNERABILITES], [SBOM] |
| Tests | pilier X, [FUZZING-API], [TESTS-MUTATION], [E2E-PARCOURS] |
| Performance | [CORE-WEB-VITALS], [BUDGET-JS], [LATENCE-API] |
| Front et accessibilité | règles de `frontend/CLAUDE.md`, [ACCESSIBILITE-AUTO] |
| Conteneurs | [CONTENEUR-DURCI], [IMAGES-PAR-EMPREINTE] |
| Exploitation | déploiement réversible, sauvegardes restaurées, santé, alertes, autoréparation |
| Observabilité | pilier VIII, [OPENTELEMETRY], [SLO], [ALERTE-SUR-SYMPTOME] |
| CI/CD | workflows réutilisables de kiln, [CI-RAPIDE] |
| Git et versions | [BRANCHES], [COMMITS], [VERSIONS], notes de version |
| Documentation et suivi | `docs/a-faire/`, archives des campagnes |
| Développement assisté par IA | `CLAUDE.md`, skills (worktree, merge, release…), hooks, [IA-RESPONSABLE], [IA-CONFIDENTIALITE] |
| Domaine métier | [ARGENT], [FUSEAU] |

**Axe 2 : la portée**, c'est-à-dire à qui s'applique la règle :

| Portée | Exemples |
|---|---|
| Universelle | tailles de fichier et de fonction, noms parlants, secrets hors du dépôt, dates stockées en UTC |
| Langage | Python moderne (PEP 695), TypeScript strict |
| Framework | Django (ORM, migrations), Nuxt et Vue 3.5 (`defineModel`, `useFetch` avec une clé) |
| Outil | Celery, PostgreSQL, Redis, Podman, Caddy, Stripe, GitHub Actions, Claude Code |
| Domaine métier | argent en centimes, données personnelles et RGPD, calendrier |
| Projet | fuseau Europe/Paris, vocabulaire de l'association, noms internes des applications |

**Les attributs de chaque règle :**
- le profil (taille de structure) ;
- le niveau (évaluer, essayer, adopter, abandonner) ;
- le régime (strict, cliquet, revue) ;
- le détecteur et le correcteur, s'ils existent ;
- le pourquoi, la source et la date.

**Une règle peut couvrir deux portées.** « Stocker les dates en UTC » est universel, alors que
« Europe/Paris » est un réglage de projet. La règle vit à la portée la plus large, et le projet ne
fournit que ses réglages.

**Ce qu'il faut classer dans le repo d'association :**
- les 108 règles nommées de la charte : 52 dans `CLAUDE.md`, 44 dans `backend/CLAUDE.md`, 12 dans
  `frontend/CLAUDE.md` ;
- les 15 piliers du backend ;
- tout ce qui vit hors de la charte : skills et hooks de Claude Code, workflows de CI, scripts
  d'exploitation (déploiement, sauvegardes, restauration testée, autoréparation, alertes),
  configuration des conteneurs et de Caddy.
