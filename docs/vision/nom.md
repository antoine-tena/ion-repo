# kiln : le nom, les faits avant la décision

> Partie de [l'idée de projet](README.md). Faits relevés le 19 octobre 2026 pour T-143.
>
> **Décision d'antoine, 19 octobre 2026 : on garde « kiln »** (paquet `kiln-cli`). Les noms
> libres ci-dessous restent pour mémoire.

## Qui répond à « kiln » aujourd'hui

**GitHub** (recherche « kiln », par étoiles, 19 octobre 2026) :

| Dépôt | Étoiles | Ce que c'est |
|---|---|---|
| Kiln-AI/Kiln | 5 204 | Évaluer et optimiser des systèmes d'IA (évaluations, RAG, agents) |
| jbruce12000/kiln-controller | 301 | Contrôleur de four sur Raspberry Pi |
| instruktlabs/kiln | 285 | Modèles 3D construits avec son agent de code |
| Fredasterehub/kiln | 226 | **Orchestration multi-modèles pour Claude Code** |
| codeofaxel/Kiln | 106 | Serveur MCP |

Deux des cinq premiers parlent déjà aux utilisateurs d'agents de code, dont un explicitement à
ceux de Claude Code : notre public exact. Un « kiln Claude Code » dans un moteur de recherche
tombe sur eux autant que sur nous.

**PyPI** : `kiln` est pris (un moteur de gabarits HTML, version 0.1, abandonné) ; nous publions
`kiln-cli`. **npm** : `kiln` est pris (un client d'API de 2013, version 0.0.1).

## Ce qu'un changement de nom touche

- le dépôt GitHub (renommé : GitHub redirige l'ancienne adresse, clones et liens compris) ;
- le paquet PyPI (un nouveau nom ; `kiln-cli` publie une dernière version qui pointe vers lui) ;
- la commande `kiln` et `charter`, gardées en alias une version mineure, comme les noms
  français de 0.3 ;
- le catalogue et les plugins Claude Code (`kiln@kiln`, skills `/kiln:*`) : le catalogue sait
  déjà porter des `renames` (`base` → `kiln`, en 0.4.0) ;
- les références `antoine-tena/kiln/.github/workflows/…@tag` des repos générés et adoptés :
  converties par `kiln update`, comme en 0.4.0 ;
- la vitrine (README, capture, About, aperçu social), le changelog et la grille.

Coût estimé : deux à trois heures de session (L), avec les conversions et leurs tests de bout en
bout. Le même changement après le lancement perdrait les étoiles, liens et articles qui
pointent vers l'ancien nom.

## Trois noms libres

Vérifiés le 19 octobre 2026 : libres sur PyPI et sur npm, sans projet notable sur GitHub.

| Nom | Sens | GitHub (le plus étoilé du même nom) |
|---|---|---|
| **trueup** | *to true up* : remettre d'équerre, aligner exactement sur une référence. C'est ce que fait l'outil : un repo ramené à la grille | vismek-solutions/trueup, 1 étoile |
| **annealer** | le recuit, qui rend le métal sain après la forge : la filiation avec kiln reste | MJGNZ/NZHS_ANNEALER, 22 étoiles |
| **kilnwork** | garde « kiln », mais un nom à soi | inogen-ai/kilnworks, 1 étoile |

**Avis de Claude** : `trueup`. Il dit le produit (un repo mis d'équerre par rapport au meilleur),
se prononce sans hésiter en anglais, et ne partage son terrain avec personne. Garder `kiln`
reste défendable : le nom est court et la marque existe déjà chez nos premiers utilisateurs,
mais il faudra se battre contre Kiln-AI et deux projets d'agents dans chaque recherche.
