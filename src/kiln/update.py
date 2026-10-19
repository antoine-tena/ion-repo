"""`kiln update` : rapporte les évolutions du modèle, puis met à jour les dépendances."""

import re
import subprocess
import tempfile
from collections.abc import Mapping
from pathlib import Path

import copier
from copier.errors import UserMessageError
from plumbum import ProcessExecutionError

from kiln import ui
from kiln.backlog import migrate_legacy_backlog
from kiln.check import check_project
from kiln.contract import generate_api_contract
from kiln.deps import lock_dependencies, sync_dependencies, update_dependencies
from kiln.frozen import frozen_files, report_frozen_drift
from kiln.rules import write_unverified_rules
from kiln.shell import KilnError, capture, require_tools, run, step
from kiln.stack import ANSWERS_FILE, load_stack, read_answers
from kiln.template import DEFAULT_TEMPLATE_SOURCE, template_revision
from kiln.versions import (
    follows_candidates,
    latest_release,
    notes_between,
    read_changelog,
    release_version,
    tag_of,
    tool_release_tag,
    upgrade_command,
)

PROTECTED_BRANCHES = ("main", "develop")
# Début d'un conflit laissé par Copier (`git merge-file`).
CONFLICT_MARKER = "<<<<<<< before updating"
# Un workflow réutilisable de kiln cité à un tag : `antoine-tena/kiln/….yml@v0.3.1`.
KILN_WORKFLOW_REF = re.compile(r"(antoine-tena/kiln/\S+?)@(\S+)")
# Ancienne adresse du modèle (init-repo, renommé kiln) : GitHub redirige, mais on la remplace.
LEGACY_TEMPLATE_SOURCES = ("https://github.com/antoine-tena/init-repo.git",)


def update_project(
    root: Path,
    *,
    should_update_template: bool,
    should_update_deps: bool,
    allow_major: bool,
    should_check: bool = True,
) -> None:
    require_tools("git", "uv")
    check_working_branch(root)
    if should_update_template:
        check_tool_not_older(root)
        step("Architecture : évolutions du modèle")
        previous = template_commit(root)
        apply_template(root)
        show_release_notes(previous, template_commit(root))
        report_frozen_drift(root, _template_source(root), previous, template_commit(root))
        mention_newer_release()
    stack = load_stack(root)
    if should_update_deps:
        update_dependencies(root, stack, allow_major=allow_major)
    elif should_update_template:
        lock_dependencies(root, stack)
        sync_dependencies(root, stack)
    generate_api_contract(root, stack)
    write_unverified_rules(root, stack)
    report_changes(root)
    if should_check:
        check_project(root)


def check_tool_not_older(root: Path) -> None:
    """Refuse de ramener un repo à une version de kiln plus ancienne que celle dont il part
    (mis à jour par un équipier qui a un kiln plus récent) : il faut d'abord monter l'outil."""
    if _template_source(root) != DEFAULT_TEMPLATE_SOURCE:
        return
    project_ref = template_commit(root)
    tool_tag = tool_release_tag()
    project, tool = release_version(project_ref), release_version(tool_tag or "")
    if project is not None and tool is not None and project > tool:
        raise KilnError(
            f"ce repo suit kiln {project_ref}, plus récent que l'outil installé ({tool_tag}) : "
            f"{upgrade_command(tag_of(project_ref) or project_ref)}"
        )


def mention_newer_release() -> None:
    """Une version de kiln plus récente que l'outil est sortie : le dire, avec la commande."""
    tool = release_version(tool_release_tag() or "")
    latest = latest_release()
    newer = release_version(latest or "")
    if tool is not None and newer is not None and newer > tool and latest is not None:
        ui.note(f"kiln {latest} est sorti : {upgrade_command(latest)}, puis kiln update.")


def apply_template(root: Path, answers: Mapping[str, object] | None = None) -> None:
    """Modèle réappliqué (révision la plus récente, réponses éventuellement changées), sans
    écraser les modifications locales : les conflits sont marqués dans les fichiers. Les
    fichiers figés (`kiln-waivers.toml`) sont laissés tels quels."""
    try:
        copier.run_update(
            root,
            data=dict(answers or {}),
            vcs_ref=template_revision(_template_source(root)),
            use_prereleases=follows_candidates(),
            exclude=frozen_files(root),
            defaults=True,
            skip_answered=True,
            overwrite=True,
            conflict="inline",
            unsafe=False,
        )
    except UserMessageError as error:
        raise KilnError(f"mise à jour du modèle refusée : {error}") from error
    except ProcessExecutionError as error:
        raise KilnError(git_failure(error)) from error
    # Après Copier, qui exige un arbre propre et réécrit le fichier de réponses.
    resolve_kiln_ref_conflicts(root)
    replace_legacy_source(root)
    if migrate_legacy_backlog(root):
        ui.note("Suivi déplacé de docs/a-faire/ vers docs/backlog/ (tickets T-NN, en anglais).")


def resolve_kiln_ref_conflicts(root: Path) -> None:
    """Conflits nés du seul `@<tag>` des workflows de kiln : refusionnés sans lui.

    Un tag promu pose sur le commit de sa dernière candidate (`v0.3.1` = `v0.3.1-rc.1`) ; Copier
    rend l'ancienne version sous le nom que lui donne `git describe`, le promu, et ne retrouve
    plus le `@v0.3.1-rc.1` du projet : conflit à chaque promotion, sans rien à arbitrer. Copier
    laisse les trois versions dans l'index (1 : ancien rendu, 2 : projet, 3 : nouveau rendu) ;
    la fusion est refaite avec l'ancien rendu au tag du projet, et gardée si elle passe."""
    for name in conflicted_files(root):
        stages = [_index_stage(root, stage, name) for stage in (1, 2, 3)]
        if None in stages:
            continue
        base, ours, theirs = (str(text) for text in stages)
        project_refs = _kiln_refs(ours)
        rendered_refs = _kiln_refs(base)
        if len(project_refs) != 1 or len(rendered_refs) != 1 or project_refs == rendered_refs:
            continue
        # Le tag revient ailleurs que dans les `uses:` (commentaire de tête de ci.yml) : il est
        # remplacé partout, sans toucher un tag plus long qui le prolonge.
        rendered_tag = re.escape(rendered_refs.pop())
        aligned_base = re.sub(rf"{rendered_tag}(?![\w.-])", project_refs.pop(), base)
        merged = _merge_cleanly(aligned_base, ours, theirs)
        if merged is not None:
            (root / name).write_text(merged)
            # Plus de conflit dans l'index : une modification du modèle comme les autres.
            run(["git", "reset", "-q", "--", name], root)


def _kiln_refs(text: str) -> set[str]:
    return {match.group(2) for match in KILN_WORKFLOW_REF.finditer(text)}


def _index_stage(root: Path, stage: int, name: str) -> str | None:
    shown = subprocess.run(
        ["git", "show", f":{stage}:{name}"], cwd=root, capture_output=True, text=True, check=False
    )
    return shown.stdout if shown.returncode == 0 else None


def _merge_cleanly(base: str, ours: str, theirs: str) -> str | None:
    """Fusion à trois de `git merge-file`, ou None si elle laisse un conflit."""
    with tempfile.TemporaryDirectory() as directory:
        paths = [Path(directory) / name for name in ("ours", "base", "theirs")]
        for path, text in zip(paths, (ours, base, theirs), strict=True):
            path.write_text(text)
        merged = subprocess.run(
            ["git", "merge-file", "-p", *map(str, paths)],
            capture_output=True,
            text=True,
            check=False,
        )
    return merged.stdout if merged.returncode == 0 else None


def conflicted_files(root: Path) -> list[str]:
    """Fichiers où Copier a laissé un conflit à résoudre à la main."""
    found = subprocess.run(
        ["git", "grep", "-l", "--untracked", CONFLICT_MARKER],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    return found.stdout.split()


# Ce que git écrit quand le réseau ou GitHub ne répond pas.
UNREACHABLE_MARKERS = ("could not resolve host", "unable to access", "connection timed out")


def git_failure(error: ProcessExecutionError) -> str:
    """Une ligne pour un git lancé par Copier (tags, clone du modèle) qui a échoué."""
    stderr = str(error.stderr or "")
    if any(marker in stderr.lower() for marker in UNREACHABLE_MARKERS):
        return "GitHub injoignable : vérifier le réseau, puis relancer"
    last_line = next((line for line in reversed(stderr.splitlines()) if line.strip()), "")
    return f"git a échoué pendant la mise à jour du modèle : {last_line.strip() or error}"


def _template_source(root: Path) -> str:
    source = str(read_answers(root).get("_src_path", ""))
    return DEFAULT_TEMPLATE_SOURCE if source in LEGACY_TEMPLATE_SOURCES else source


def template_commit(root: Path) -> str:
    """Révision du modèle dont part le repo : `v3`, ou un commit avant la première version."""
    return str(read_answers(root).get("_commit", ""))


def show_release_notes(previous: str, current: str) -> None:
    """Encadré des nouveautés de chaque version passée, d'après le journal de kiln."""
    notes = notes_between(previous, current, read_changelog())
    if not notes:
        return
    lines: list[str] = []
    for release in notes:
        lines += [f"{release.tag}  {release.date}".rstrip(), *release.lines, ""]
    ui.panel(f"Nouveautés de kiln : {previous or '?'} → {current}", lines[:-1])


def check_working_branch(root: Path) -> None:
    if not (root / ANSWERS_FILE).exists():
        raise KilnError(f"pas de {ANSWERS_FILE} : ce dépôt n'a pas été généré par kiln")
    branch = capture(["git", "branch", "--show-current"], root)
    if branch in PROTECTED_BRANCHES:
        raise KilnError(f"sur {branch} : créer d'abord une branche (ex. chore/kiln-update)")
    if capture(["git", "status", "--porcelain"], root):
        raise KilnError("arbre non propre : commiter ou mettre de côté les modifications")


def report_changes(root: Path) -> None:
    step("Fichiers modifiés")
    run(["git", "status", "--short"], root, live=True)
    print()
    ui.note(
        "Relire le diff (conflits marqués <<<<<<<), commiter, puis fusionner dans develop "
        "(skill base:fusion)."
    )


def replace_legacy_source(root: Path) -> None:
    answers_path = root / ANSWERS_FILE
    text = answers_path.read_text()
    for legacy_source in LEGACY_TEMPLATE_SOURCES:
        text = text.replace(f"_src_path: {legacy_source}", f"_src_path: {DEFAULT_TEMPLATE_SOURCE}")
    answers_path.write_text(text)
