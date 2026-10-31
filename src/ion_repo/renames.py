"""Names that changed when kiln went English (0.4.0): each old French name → its new name; the
sizes, named after the fire of the kiln until 0.4.10 (`ember` → `small`); and kiln's own names,
when it became ion-repo in the Ion family (31 October 2026: `/kiln:merge` → `/repo:merge`).

ion-repo keeps reading the old names wherever a project may still carry them: an adopted repo that
`ion repo update` never converts (its `charte.toml`), a waiver written before 0.4.0, a comment
that cites a rule. `ion repo update` rewrites them in the projects it generated.
"""

from collections.abc import Mapping

# Rule identifiers of the charter (`[FILE-SIZE]`), cited by the instructions, `charter.toml`,
# waivers, code comments and commit messages.
RULE_IDS: Mapping[str, str] = {
    "ACCESSIBILITE": "ACCESSIBILITY",
    "ACCESSIBILITE-AUTO": "AUTOMATED-ACCESSIBILITY",
    "ALERTE-SUR-SYMPTOME": "ALERT-ON-SYMPTOMS",
    "APPELS-API": "API-CALLS",
    "ARGENT": "MONEY",
    "ASTRO-MODERNE": "MODERN-ASTRO",
    "ASYNC": "ASYNC-AWAIT",
    "AUDIT-VULNERABILITES": "VULNERABILITY-AUDIT",
    "BOOLEENS": "BOOLEANS",
    "BUDGET-JS": "JS-BUDGET",
    "CALCULS-HORS-UI": "COMPUTE-OUTSIDE-UI",
    "CASSE": "CASE",
    "CHAMPS-COMMUNS": "COMMON-FIELDS",
    "CHIFFREMENT": "ENCRYPTION",
    "CI-RAPIDE": "FAST-CI",
    "CLI-MINCE": "THIN-CLI",
    "CLIQUET": "RATCHET",
    "CODES-RETOUR": "EXIT-CODES",
    "COEUR-PUR": "PURE-CORE",
    "CONTENEUR-DURCI": "HARDENED-CONTAINERS",
    "CONTENU": "CONTENT-COLLECTIONS",
    "CONTRAT-FIGE": "FROZEN-CONTRACT",
    "COUCHES": "LAYERS",
    "DENSITE-TESTS": "TEST-DENSITY",
    "DEPENDANCES": "DEPENDENCY-INJECTION",
    "DEPENDANCES-FIGEES": "LOCKED-DEPENDENCIES",
    "DEPENDANCES-MINIMALES": "MINIMAL-DEPENDENCIES",
    "DEPLOIEMENT-REVERSIBLE": "REVERSIBLE-DEPLOYMENT",
    "DERIVE": "CONTRACT-DRIFT",
    "DEROGATIONS": "WAIVERS",
    "DESTRUCTIF": "DESTRUCTIVE-ACTIONS",
    "DOMAINE-HERMETIQUE": "SEALED-DOMAIN",
    "DONNEES-LOURDES": "LARGE-DATA",
    "DONNEES-PERSO": "PERSONAL-DATA",
    "E2E-PARCOURS": "E2E-JOURNEYS",
    "EN-TETES": "SECURITY-HEADERS",
    "ENTREES": "VALIDATED-INPUTS",
    "ERREURS": "ERRORS",
    "ERREURS-METIER": "DOMAIN-ERRORS",
    "ETAT": "SESSION-STATE",
    "ETATS-UI": "UI-STATES",
    "FICHIERS": "UPLOADS",
    "FIGURES-ACCESSIBLES": "ACCESSIBLE-FIGURES",
    "FONCTIONS-PURES": "PURE-FUNCTIONS",
    "FUSEAU": "TIME-ZONE",
    "FUSION": "MERGE",
    "FUZZING-API": "API-FUZZING",
    "HANDLER-IDEMPOTENT": "IDEMPOTENT-HANDLER",
    "HORLOGE": "CLOCK",
    "HORS-REQUETE": "OUT-OF-REQUEST",
    "IA-CONFIDENTIALITE": "AI-CONFIDENTIALITY",
    "IA-CONTEXTE": "AI-CONTEXT",
    "IA-FONCTIONNALITE": "AI-FEATURES",
    "IA-RESPONSABLE": "AI-ACCOUNTABILITY",
    "IDEMPOTENCE": "IDEMPOTENCY",
    "IDS": "COMPONENT-IDS",
    "IMAGES-MODERNES": "MODERN-IMAGES",
    "IMAGES-PAR-EMPREINTE": "IMAGES-BY-DIGEST",
    "IMPORTS-EXPLICITES": "EXPLICIT-IMPORTS",
    "INDEX": "INDEXES",
    "INJECTION": "CONSTRUCTOR-INJECTION",
    "INTEGRITE": "SUBRESOURCE-INTEGRITY",
    "JAVA-MODERNE": "MODERN-JAVA",
    "JOURNALISATION": "LOGGING",
    "LATENCE-API": "API-LATENCY",
    "MODELE-NU": "THIN-MODEL",
    "MULTI-PLATEFORME": "MULTI-PLATFORM",
    "NOMS-INTERDITS": "GENERIC-NAMES",
    "NON-REGRESSION": "REGRESSION-TEST",
    "NOUVELLE-DEPENDANCE": "NEW-DEPENDENCY",
    "NULL": "NO-NULL",
    "PAS-SUR-MAIN": "NO-COMMIT-ON-MAIN",
    "PLANCHER": "FLOOR",
    "PYTHON-MODERNE": "MODERN-PYTHON",
    "REACT-MODERNE": "MODERN-REACT",
    "REMONTER-A-KILN": "REPORT-TO-ION-REPO",
    # kiln became ion-repo (31 October 2026).
    "REPORT-TO-KILN": "REPORT-TO-ION-REPO",
    "RENVOIS-AUDIT": "AUDIT-REFERENCES",
    "REPRISE": "RETRIES",
    "REPRODUCTIBLE": "REPRODUCIBLE",
    "RESEAU": "NO-NETWORK",
    "RETOURS": "RETURN-VALUES",
    "ROUTE-PUBLIQUE": "PUBLIC-ROUTES",
    "ROUTEURS": "ROUTERS",
    "SANTE": "HEALTH-PROBES",
    "SANTE-ASYNC": "ASYNC-HEALTH",
    "SAUVEGARDE-TESTEE": "TESTED-BACKUPS",
    "SCHEMA-DONNEES": "DATA-SCHEMA",
    "SERVEUR-D-ABORD": "SERVER-FIRST",
    "SIGNAUX": "NO-SIGNALS",
    "SORTIE": "OUTPUT-STREAM",
    "SORTIE-MACHINE": "MACHINE-OUTPUT",
    "SOURCES": "DATA-SOURCES",
    "STATIQUE-D-ABORD": "STATIC-FIRST",
    "SYSTEME-A-LA-FRONTIERE": "SYSTEM-AT-THE-EDGE",
    "TAILLE-FICHIER": "FILE-SIZE",
    "TAILLE-FONCTION": "FUNCTION-SIZE",
    "TEMPS-CONSTANT": "CONSTANT-TIME",
    "TESTS-MUTATION": "MUTATION-TESTS",
    "TESTS-PERMISSIONS": "PERMISSION-TESTS",
    "TESTS-PROPRIETES": "PROPERTY-TESTS",
    "TESTS-UI": "UI-TESTS",
    "TS-STRICT": "STRICT-TS",
    "TYPAGE": "TYPING",
    "TYPAGE-STRICT": "STRICT-TYPING",
    "TYPES-BRUTS": "NO-RAW-TYPES",
    "UNE-CLASSE": "ONE-CLASS",
    "UNE-CLASSE-PUBLIQUE": "ONE-PUBLIC-CLASS",
    "VALIDATION-AUX-FRONTIERES": "VALIDATE-AT-BOUNDARIES",
    "VERROUS": "LOCKS",
    "VOCABULAIRE": "VOCABULARY",
    "VUE-15": "VIEW-15",
    "VUE-MODERNE": "MODERN-VUE",
    "ZERO-ANY": "NO-ANY",
    "ZERO-MAGIE": "NO-MAGIC-VALUES",
}

# `charte.toml` → `charter.toml`: sections, keys (at the top or in a rule) and rule names.
CHARTER_SECTIONS: Mapping[str, str] = {
    "interdictions": "bans",
    "cliquets": "ratchets",
    "planchers": "floors",
    "couverture": "coverage",
}
CHARTER_KEYS: Mapping[str, str] = {
    "branche": "branch",
    "chemins": "paths",
    "decorateur": "decorator",
    "dossier": "directory",
    "envergure": "size",
    "exclus": "exclude",
    "fichier": "file",
    "fichiers": "files",
    "marge": "margin",
    "max_lignes": "max_lines",
    "motif": "pattern",
    "paires": "pairs",
    "paquets": "packages",
    "plancher": "floor",
    "planchers": "floors",
    "rapport": "report",
    "regle": "rule",
    "regles_locales": "local_rules",
    "regles_non_verifiees": "unverified_rules",
    "suffixes_tests": "test_suffixes",
}
CHARTER_RULES: Mapping[str, str] = {
    "compose-profils": "compose-profiles",
    "copies": "identical-copies",
    "densite-tests": "test-density",
    "donnees-perso": "personal-data",
    "fichiers-interdits": "forbidden-files",
    "journalisation": "logging",
    "migrations-django": "django-migrations",
    "outils-interdits": "forbidden-tools",
    "renvois-audit": "audit-references",
    "routes-longues": "long-routes",
    "signaux-django": "django-signals",
    "style-vue": "vue-style",
    "taille-fichier": "file-size",
    "temps-constant": "constant-time",
    "verrous-django": "django-locks",
}


def rule_id(name: str) -> str:
    """A rule identifier under its current name, whatever the name it is cited by."""
    return RULE_IDS.get(name, name)


# Answers of `.copier-answers.yml` (and keys of `kiln set`): key → new key, value → new value.
ANSWER_KEYS: Mapping[str, str] = {
    "boussole": "north_star",
    "branche_deploiement": "deploy_branch",
    "date_creation": "created",
    "deploiement": "deploy",
    "domaine_api": "api_domain",
    "envergure": "size",
    "equipe": "team",
    "front_deploiement": "frontend_deploy",
    "nom": "name",
    "proprietaire": "owner",
    "titre": "title",
    "type_projet": "project_type",
    "url_sante_prod": "prod_health_url",
    "url_site": "site_url",
    "vps_hote": "vps_host",
}
# The sizes before kiln 0.4.10, named after the fire of the kiln.
SIZES: Mapping[str, str] = {"spark": "tiny", "ember": "small", "flame": "medium", "blaze": "large"}
ANSWER_VALUES: Mapping[str, Mapping[str, str]] = {
    "size": SIZES,
    "backend": {"aucun": "none"},
    "frontend": {"aucun": "none"},
    "deploy": {"aucun": "none"},
    "frontend_deploy": {"aucun": "none"},
    "project_type": {"tableau": "dashboard", "analyse": "analysis", "outil": "cli"},
}


def answers(values: Mapping[str, object]) -> dict[str, object]:
    """Answers under today's names, whatever the release of kiln that wrote them."""
    renamed: dict[str, object] = {}
    for key, value in values.items():
        name = ANSWER_KEYS.get(key, key)
        if name in renamed and key != name:
            continue  # the current key wins over its old name
        old_values = ANSWER_VALUES.get(name, {})
        renamed[name] = old_values.get(value, value) if isinstance(value, str) else value
    return renamed


def fire_size(values: Mapping[str, object]) -> dict[str, object]:
    """Answers with the size under its name before kiln 0.4.10, to render a template of that
    time (`small` → `ember`)."""
    fire = {new: old for old, new in SIZES.items()}
    size = values.get("size")
    return (
        {**values, "size": fire[size]} if isinstance(size, str) and size in fire else dict(values)
    )


def legacy_answers(values: Mapping[str, object]) -> dict[str, object]:
    """Answers under the names of before kiln 0.4.0, to render a template of that time (frozen
    files, the conversion of `kiln update`)."""
    legacy_keys = {new: old for old, new in ANSWER_KEYS.items()}
    legacy = {}
    for key, value in answers(values).items():
        old_values = {new: old for old, new in ANSWER_VALUES.get(key, {}).items()}
        legacy_value = old_values.get(value, value) if isinstance(value, str) else value
        legacy[legacy_keys.get(key, key)] = legacy_value
    return legacy


# Machine settings of `~/.config/kiln/config.toml` (and keys of `kiln set` outside a repo).
MACHINE_KEYS: Mapping[str, str] = {
    "canal": "channel",
    "dossier_code": "code_dir",
    "equipe": "team",
    "proprietaire": "owner",
    "systeme": "system",
}
MACHINE_VALUES: Mapping[str, Mapping[str, str]] = {
    "channel": {"interne": "internal"},
    "statusline": {
        "sobre": "plain",
        "bandeau": "band",
        "classique": "classic",
        "classique-fond": "classic-band",
        "aucune": "none",
        "perso": "custom",
    },
}


def machine_value(key: str, value: str) -> str:
    """A machine setting's value under its current name (`interne` → `internal`)."""
    return MACHINE_VALUES.get(key, {}).get(value, value)


# kiln became ion-repo (31 October 2026): its plugin `kiln@kiln` is `repo@ion-repo`, the stack
# plugins move to the `ion-repo` catalogue, its skills are `/repo:…`, its variables `ION_REPO_…`,
# its rules in a project `.claude/rules/ion-repo/`.
STACK_PLUGINS = ("django", "nuxt", "vps", "stripe", "serena")
ION_PLUGINS: Mapping[str, str] = {
    "kiln@kiln": "repo@ion-repo",
    "base@kiln": "repo@ion-repo",
    "repo@kiln": "repo@ion-repo",
    **{f"{name}@kiln": f"{name}@ion-repo" for name in STACK_PLUGINS},
}
ION_SKILLS = (
    "adopt", "backlog", "cleanup", "contribution", "good-first-issues", "merge", "modernize",
    "pause", "prompt", "release", "report", "resize", "review", "token", "update", "worktree",
)  # fmt: skip
ION_VARIABLES = (
    "PROJECT", "BACKEND_DIR", "FRONTEND_DIR", "TEST_ENV", "VPS", "VPS_DIR", "VPS_BACKUPS", "SITE",
    "API_HEALTH", "PROD_DOC", "CHARTER_SCRIPT", "TEMPLATE", "VERBOSE", "NO_UPDATE_CHECK",
    "PG_CONTAINER", "PG_PORT", "PG_USER", "PG_DATABASE", "PG_READ_ROLE", "PG_IMAGE",
)  # fmt: skip
LEGACY_RULES_DIR = ".claude/rules/kiln"
RULES_DIR = ".claude/rules/ion-repo"
