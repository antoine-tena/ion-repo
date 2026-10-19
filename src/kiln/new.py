"""`kiln new` : génère un projet complet, l'installe et le publie au besoin."""

import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import copier

from kiln import github, install
from kiln.config import load_config
from kiln.contract import generate_api_contract
from kiln.deps import lock_dependencies
from kiln.rules import write_unverified_rules
from kiln.shell import KilnError, require_tools, run, step
from kiln.stack import load_stack, read_answers
from kiln.statusline import apply_statusline_settings
from kiln.template import template_revision, template_source
from kiln.versions import follows_candidates

INITIAL_COMMIT_MESSAGE = "chore: projet généré par kiln"


@dataclass(frozen=True)
class NewProjectRequest:
    destination: Path
    answers: dict[str, object]
    template: str | None
    should_install: bool
    should_publish: bool


def create_project(request: NewProjectRequest) -> None:
    if request.destination.exists() and any(request.destination.iterdir()):
        raise KilnError(f"{request.destination} existe déjà et n'est pas vide")
    require_tools("git", "uv")
    should_publish = request.should_publish and github.can_publish()
    step("Génération depuis le modèle")
    source = template_source(request.template)
    copier.run_copy(
        source,
        request.destination,
        data=request.answers,
        user_defaults=_user_defaults(should_publish=should_publish),
        vcs_ref=template_revision(source),
        use_prereleases=follows_candidates(),
        unsafe=False,
        # Hors terminal (CI, agent), les questions sans réponse prennent leur valeur par défaut.
        defaults=not sys.stdin.isatty(),
    )
    root = request.destination.resolve()
    stack = load_stack(root)
    if stack.pnpm_dir is not None:
        require_tools("pnpm")
    run(["git", "init", "-q", "-b", "main"], root)
    apply_statusline_settings(root)
    lock_dependencies(root, stack)
    write_unverified_rules(root, stack)
    if request.should_install:
        install.install_project(root)
        generate_api_contract(root, stack)
    _initial_commit(root)
    if should_publish:
        github.publish(root, repository_name(root), team_logins(root))


def _user_defaults(*, should_publish: bool) -> dict[str, object]:
    """Propriétaire et équipe par défaut : réglages du poste, sinon le compte connecté à gh
    (seulement quand on publie : pas d'appel réseau pour un projet local)."""
    config = load_config()
    defaults: dict[str, object] = {}
    owner = config.owner or (github.login() if should_publish else None)
    if owner:
        defaults["proprietaire"] = owner
    if config.team:
        defaults["equipe"] = list(config.team)
    return defaults


def _initial_commit(root: Path) -> None:
    step("Premier commit sur main")
    run(["git", "add", "-A"], root)
    # Seul commit admis sur main : celui qui crée le dépôt ([PAS-SUR-MAIN]).
    commit_env = {**os.environ, "SKIP": "no-commit-to-branch"}
    run(["git", "commit", "-q", "-m", INITIAL_COMMIT_MESSAGE], root, env=commit_env)
    # main garde ce seul commit ; tout le travail part de develop.
    run(["git", "switch", "-q", "-c", "develop"], root)


def repository_name(root: Path) -> str:
    """`propriétaire/nom` du dépôt GitHub ; sans propriétaire, le compte connecté à gh."""
    answers = read_answers(root)
    owner = str(answers.get("proprietaire") or "") or github.login()
    if not owner:
        raise KilnError("propriétaire GitHub inconnu : gh auth login, ou kiln set proprietaire=…")
    return f"{owner}/{answers['nom']}"


def team_logins(root: Path) -> list[str]:
    team = read_answers(root).get("equipe", [])
    return [str(login) for login in team] if isinstance(team, list) else []


def publish_project(root: Path) -> None:
    """`kiln publish` : le dépôt GitHub privé d'un projet créé sans (`--no-github`, gh absent)."""
    require_tools("git", "gh")
    remote = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    if remote.returncode == 0:
        raise KilnError(f"déjà publié : origin = {remote.stdout.strip()}")
    if not github.can_publish():
        raise KilnError(f"gh n'est pas connecté : gh auth login ({github.LOGIN_URL})")
    github.publish(root, repository_name(root), team_logins(root))
