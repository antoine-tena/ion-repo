# Nouveautés de kiln

Une entrée par version, la plus récente en tête : `## vX.Y.Z — date`, puis une ligne par
changement visible (`- …`), cassants en tête. `kiln update` montre les entrées des versions
qu'un projet passe ; la skill `base:version` rédige celle de la version qu'elle sort, sur la
branche `release/vX.Y.Z`, avant sa première candidate.

## v0.3.4 — 2026-10-16
- Le modèle n'est jamais plus récent que l'outil installé : `kiln update` applique la version de kiln installée (les conversions d'une version à l'autre vivent dans l'outil), refuse de ramener un repo à une version plus ancienne que la sienne, et signale qu'une version plus récente est sortie.
- `kiln new` sans `gh`, ou hors terminal sans connexion, crée le projet en local, et `kiln publish` crée ensuite le dépôt GitHub. Le propriétaire par défaut vient des réglages du poste ou du compte connecté à gh ; un projet sans équipe n'a ni CODEOWNERS ni section « Équipe ».
- La CI générée cherche les secrets par le workflow `secrets.yml` (gitleaks figé et vérifié, sans la licence qu'exige gitleaks-action pour une organisation) ; `kiln ci` le rejoue avec le gitleaks du poste.
- `kiln` répond en 0,12 s au lieu de 0,5 s (commandes importées à la demande) ; le README généré installe kiln depuis PyPI.
- Fiabilité : tests de bout en bout (chaque framework généré, installé et contrôlé ; un projet des versions précédentes mis à jour sans conflit), joués sur chaque branche de version ; CI de kiln aussi sous macOS.

## v0.3.3 — 2026-10-16
- `kiln completion bash` : script de complétion tiré des commandes et options de kiln, à activer par `eval "$(kiln completion bash)"` dans `~/.bashrc` (#41, merci @HarshRajSinghania).
- Skill `good-first-issues` : garde ouvertes sur GitHub quelques issues pour débutants, tirées du backlog et réservées aux contributeurs extérieurs.
- Correctifs : `kiln update` ne s'arrête plus sur un conflit dans `ci.yml` après la promotion d'une version (seul le `@<tag>` des workflows de kiln différait) ; `base:worktree` ne bute plus sur un repo sans fichier `.env` ; la mise à jour d'un kiln installé depuis un dossier retire aussi l'ancien outil `kiln`.

## v0.3.2 — 2026-10-16
- `kiln adopt` fait suivre kiln à un repo existant, sans le régénérer ; le skill `adoption` trie avec l'utilisateur ce que la charte y trouve à redire, et l'ouverture de session le propose dans un repo à soi qui ne suit pas encore kiln.
- Dérogations à la charte dans `kiln-waivers.toml`, avec un motif et une échéance croissante à chaque renouvellement : `kiln waive` les ajoute, renouvelle ou liste, `kiln update` épargne les fichiers figés et dit ce qu'il y aurait changé, `kiln status` compte celles de chaque repo.
- Skill `relecture` : commits et diff d'une branche relus et rangés avant la fusion (`fusion` le lance), dépôt entier avant une version (`version` le lance) ; le hook `garde-branche` refuse un message de commit signé Claude.
- Les questions de kiln en début de session suivent une politique commune : chaque « non » espace la suivante, chaque « oui » la rapproche.
- `kiln --version` (#39, merci @SakarPaisen, première contribution extérieure).
- Correctifs : `kiln update --all` dit « GitHub injoignable » en une ligne au lieu d'une trace Python, et un passage raté ne bloque plus le suivant avec un worktree laissé vide.

## v0.3.1 — 2026-10-16
- **Cassant** : le suivi du travail passe en anglais, `docs/a-faire/` devient `docs/backlog/` (tickets `T-NN`, skill `base:backlog` à la place de `base:a-faire`) ; `kiln update` déplace l'ancien dossier.
- Numérotation comme Claude Code : en 0.x, chaque version monte le correctif, cassante comprise ; la mineure ne monte que pour une étape (`kiln version --minor`). Une version est promue dès que la suivante est prête en candidate, sans délai d'attente.
- kiln s'installe depuis PyPI : paquet `kiln-cli` (la commande reste `kiln`), publié au tag de chaque version promue ; `kiln doctor` et `maj-kiln` proposent la mise à jour par là.
- Nouveaux skills : `report-to-kiln` (un défaut de kiln rencontré dans un repo devient une issue ou une PR, publiée seulement avec l'accord de l'utilisateur), `token` (jeton d'un service dans `.<service>/`, collé sans s'afficher), `contribution` (traiter la PR d'un contributeur extérieur).
- La CI générée lance gitleaks et peut être appelée par d'autres workflows (`workflow_call`).
- Status line : quatre styles aux couleurs de kiln, en anglais (`kiln set statusline=…`), nom de session, RAM et cœurs occupés.
- Correctifs : `kiln doctor` propose la mise à jour au tag de la version, colonne du modèle de `kiln status` assez large.

## v0.3.0 — 2026-10-15
- Première version publiée. Semver en 0.x : une version sort d'abord en candidate (`-rc.N`) pour les postes au canal `interne`, puis est promue quand la suivante est prête et qu'elle a tenu trois jours ; `kiln version` dit où en sont les candidates.
- Les projets citent les workflows de kiln au tag exact dont ils partent ; `kiln update` le fait avancer et montre les nouveautés de chaque version passée. Le hook de début de session propose l'outil puis le repo à chaque version.
- `kiln status` dit de quelle version part chaque repo (`f611f82 → v0.3.0`) ; `kiln set canal=interne` (réglage du poste) fait suivre les candidates.
- Nouvelle interface : four rieur en bannière, écran d'accueil par sections, roue animée et durée pour chaque commande externe, bilan encadré des étapes ; aucune couleur hors terminal, `KILN_VERBOSE=1` pour la sortie complète.
- `kiln doctor` : diagnostic du poste et du repo, chaque problème avec la commande qui le corrige.
- `kiln dev` : sorties des serveurs entrelacées, préfixées par service en couleur.
- `kiln update --all` fusionne directement chaque repo dont les contrôles passent, sans PR.
- Backend Java (Maven), skill `maj-kiln`, lien `.claude/kiln` vers le plugin, réglages du poste par `kiln set`.
