"""Names that changed when kiln went English (0.4.0): each old French name → its new name; the
sizes, named after the fire of the kiln until 0.4.10 (`ember` → `small`); and kiln's own names,
when it became ion-repo in the Ion family (31 October 2026: `/kiln:merge` → `/repo:merge`).

ion-repo keeps reading the old names wherever a project may still carry them: an adopted repo that
`ion repo update` never converts (its `charte.toml`), a waiver written before 0.4.0, a comment
that cites a rule. `ion repo update` rewrites them in the projects it generated.
"""

from collections.abc import Mapping

# Rule identifiers of the charter under their current names: ion-score holds them, for its grid
# and for the charter.
from ion_score.rule_ids import RULE_IDS as RULE_IDS
from ion_score.rule_ids import rule_id as rule_id

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
STACK_PLUGINS = ("django", "nuxt", "stripe", "serena")
# The `vps` plugin left for ion-host, the family's hosting tool (2 November 2026): its skills are
# `/host:deploy`, `/host:prod-logs`, `/host:prod-dump`.
HOST_PLUGIN = "host@ion-host"
HOST_SKILLS = ("deploy", "prod-logs", "prod-dump")
ION_PLUGINS: Mapping[str, str] = {
    "kiln@kiln": "repo@ion-repo",
    "base@kiln": "repo@ion-repo",
    "repo@kiln": "repo@ion-repo",
    "ion-repo@ion-repo": "repo@ion-repo",  # the family's repos, renamed by hand first
    **{f"{name}@kiln": f"{name}@ion-repo" for name in STACK_PLUGINS},
    "vps@kiln": HOST_PLUGIN,
    "vps-podman@kiln": HOST_PLUGIN,
    "vps@ion-repo": HOST_PLUGIN,
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
# The Ion family's former repo names (each redirects on GitHub), cited in its backlogs as
# `hearth's T-07`; `ion repo tickets` reads them in the family's repos only.
FAMILY_TOOLS: Mapping[str, str] = {
    "kiln": "ion-repo",
    "keramos": "ion",
    "grog": "ion-learn",
    "hearth": "ion-host",
    "cone": "ion-score",
    "slake": "ion-render",
    "seal": "ion-deal",
    "saggar": "ion-secure",
    "glaze": "ion-design",
    "wedge": "ion-media",
    "stylus": "ion-words",
    "raku": "ion-launch",
}
LEGACY_RULES_DIR = ".claude/rules/kiln"
RULES_DIR = ".claude/rules/ion-repo"
