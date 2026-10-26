"""kiln: Claude Code's workshop. Generates a project, tunes its settings and keeps it up to date."""

import argparse
import re
import sys
import time
from collections.abc import Sequence
from pathlib import Path
from typing import TYPE_CHECKING, NoReturn

from kiln import banner, tool_update, ui
from kiln.config import load_config
from kiln.shell import KilnError, repo_root
from kiln.versions import installed_version

if TYPE_CHECKING:
    from kiln import new

EXIT_FAILURE = 1
EXIT_INTERRUPTED = 130  # 128 + SIGINT, as shells report it
PROJECT_NAME = re.compile(r"[a-z][a-z0-9-]*")
SIZES = ("spark", "ember", "flame", "blaze")
PROJECT_TYPES = ("app", "api", "site", "dashboard", "analysis", "cli")
BACKENDS = ("django", "fastapi", "data", "cli", "java", "none")
FRONTENDS = ("nuxt", "next", "astro", "vite-react", "streamlit", "dash", "none")
LANGUAGES = ("en", "fr")


# Home screen: commands by section; the role of each comes from its argparse help.
COMMAND_GROUPS = (
    ("Project", ("new", "adopt", "install", "publish", "update", "set", "waive")),
    ("Day to day", ("dev", "check", "ci", "contract", "doctor", "pause", "completion")),
    ("The grid", ("grid", "score", "fix")),
    ("All repos", ("status", "update --all", "version")),
)
FLEET_UPDATE_ROLE = "update every kiln repo, merged straight away"
EXAMPLES = (
    "kiln new atelier --size ember --backend fastapi",
    "kiln update --major",
    "kiln set podman=true",
    "kiln set --global             # this machine's settings",
)
# French names of kiln 0.3, still accepted with a warning until the next minor release.
LEGACY_COMMANDS = {"contrat": "contract"}
LEGACY_OPTIONS = {
    "ci": {
        "--sauter": "--skip",
        "--sans-pousser": "--no-push",
        "--garder": "--keep",
        "--statut": "--status",
    },
    "set": {"--poste": "--global"},
}
NO_RECAP_COMMANDS = frozenset(
    {"dev", "ci", "status", "doctor", "version", "waive", "grid", "score", "fix", "pause"}
)
HELP_FLAGS: tuple[list[str], ...] = ([], ["-h"], ["--help"])


class _VersionAction(argparse.Action):
    """`--version` (`-V` as uv and ruff have it, `-v` as typed by habit), computed only when
    asked: `installed_version()` runs git on an install from a folder, a cost the other commands
    need not pay."""

    def __init__(self, option_strings: Sequence[str], dest: str, **_: object) -> None:
        super().__init__(option_strings, dest, nargs=0, help="show the version of kiln")

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: object,
        option_string: str | None = None,
    ) -> NoReturn:
        print(installed_version())
        parser.exit()


class _KilnParser(argparse.ArgumentParser):
    """A command's `--help` drawn like the home screen (banner, sections) instead of argparse's
    plain text, its usage short as uv has it (`kiln new [options] [directory]`)."""

    def print_help(self, file: object = None) -> None:
        self.color = False  # Python 3.14 paints argparse's help, which ours paints itself
        formatter = self._get_formatter()
        groups: list[banner.OptionGroup] = []
        for title, positional in (("Arguments", True), ("Options", False)):
            options = [
                (formatter._format_action_invocation(action), _sentence(formatter, action))
                for action in self._actions
                if bool(action.option_strings) != positional
                and not isinstance(action, argparse._HelpAction)
                and action.help != argparse.SUPPRESS
            ]
            if options:
                groups.append((title, options))
        positionals = [
            formatter._format_args(action, formatter._get_default_metavar_for_positional(action))
            for action in self._actions
            if not action.option_strings
        ]
        usage = " ".join([self.prog, "[options]", *positionals])
        banner.show_command_help(_sentence(formatter, self), usage, groups)


def _sentence(formatter: argparse.HelpFormatter, source: object) -> str:
    if isinstance(source, argparse.Action):
        text = formatter._expand_help(source) if source.help else ""
    else:
        text = getattr(source, "description", None) or ""
    return text[:1].upper() + text[1:]


def modernize(arguments: Sequence[str]) -> list[str]:
    """The arguments with the names of kiln 0.3 replaced by today's, each one flagged."""
    modern = list(arguments)
    if modern and modern[0] in LEGACY_COMMANDS:
        modern[0] = _flag_legacy(modern[0], LEGACY_COMMANDS[modern[0]])
    options = LEGACY_OPTIONS.get(modern[0], {}) if modern else {}
    for index, argument in enumerate(modern[1:], start=1):
        name, equals, value = argument.partition("=")
        if name in options:
            modern[index] = _flag_legacy(name, options[name]) + equals + value
    return modern


def _flag_legacy(old: str, new: str) -> str:
    print(
        f"kiln: `{old}` is now `{new}`; the old name goes away at the next minor release.",
        file=sys.stderr,
    )
    return new


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="kiln", description=__doc__)
    parser.add_argument("-V", "-v", "--version", action=_VersionAction)
    commands = parser.add_subparsers(dest="command", parser_class=_KilnParser)
    _add_new_command(commands)
    adopt_parser = commands.add_parser("adopt", help="bring an existing repo under kiln")
    adopt_parser.add_argument("--size", choices=SIZES, help="size of the project (default: ember)")
    adopt_parser.add_argument("--template", help="template source (path or git URL)")
    install_parser = commands.add_parser("install", help="set up this machine after a clone")
    install_parser.add_argument(
        "--machine",
        action="store_true",
        help="kiln for the whole machine (command, Claude plugin, settings), even from a repo",
    )
    commands.add_parser("publish", help="create the private GitHub repo and protect its branches")
    _add_update_command(commands)
    _add_dev_command(commands)
    check_parser = commands.add_parser("check", help="run the project's checks")
    check_parser.add_argument(
        "--tests", action="store_true", help="the test suites too (the release runs them)"
    )
    check_parser.add_argument(
        "--all", action="store_true", help="the whole repo, not only the branch's changes"
    )
    _add_ci_command(commands)
    commands.add_parser("contract", help="regenerate openapi.json and the frontend types")
    version_parser = commands.add_parser(
        "version", help="versions of kiln: public, candidates, next"
    )
    version_parser.add_argument(
        "action",
        nargs="?",
        choices=["cut", "promote"],
        help="cut: release branch, then candidate; promote: the candidate ready, made public",
    )
    version_parser.add_argument("number", nargs="?", help="promote: the version (vX.Y.Z)")
    version_parser.add_argument(
        "--urgent", action="store_true", help="promote: no soak nor repo, the CI green only"
    )
    version_parser.add_argument(
        "--minor", action="store_true", help="the next one is a milestone: bump the minor"
    )
    commands.add_parser("doctor", help="diagnose this machine and the repo, with the fixes")
    _add_grid_command(commands)
    _add_score_command(commands)
    _add_fix_command(commands)
    _add_pause_command(commands)
    status_parser = commands.add_parser("status", help="state of the kiln repos of the code folder")
    status_parser.add_argument("--all", action="store_true", help="every repo (the default)")
    set_parser = commands.add_parser(
        "set", help="show or change the repo's settings (outside a repo: this machine's)"
    )
    set_parser.add_argument("assignments", nargs="*", metavar="key=value")
    set_parser.add_argument(
        "--global",
        dest="machine",
        action="store_true",
        help="this machine's settings, even from a repo",
    )
    _add_waive_command(commands)
    completion_parser = commands.add_parser(
        "completion", help="shell completion script (eval it in ~/.bashrc)"
    )
    completion_parser.add_argument(
        "shell", nargs="?", default="bash", choices=["bash"], help="target shell (default: bash)"
    )
    for choice in commands._choices_actions:
        commands.choices[choice.dest].description = choice.help
    return parser


def generate_bash_completion() -> str:
    """Bash completion script drawn from the parser: commands, then their options and choices."""
    subparsers = next(
        action
        for action in build_parser()._actions
        if isinstance(action, argparse._SubParsersAction)
    )
    cases: list[str] = []
    for name, subparser in sorted(subparsers.choices.items()):
        words: set[str] = set()
        for action in subparser._actions:
            words.update(action.option_strings)
            if not action.option_strings and action.choices:
                words.update(str(choice) for choice in action.choices)
        cases.append(
            f"        {name})\n"
            f'            COMPREPLY=( $(compgen -W "{" ".join(sorted(words))}" -- "$cur") )\n'
            f"            ;;"
        )
    commands = " ".join(sorted(subparsers.choices))
    return f"""# kiln bash completion: eval "$(kiln completion bash)"
_kiln_completion() {{
    local cur="${{COMP_WORDS[COMP_CWORD]}}"
    COMPREPLY=()
    if [[ $COMP_CWORD -eq 1 ]]; then
        COMPREPLY=( $(compgen -W "{commands}" -- "$cur") )
        return 0
    fi
    case "${{COMP_WORDS[1]}}" in
{"\n".join(cases)}
    esac
}}
complete -F _kiln_completion kiln"""


def _dispatch_version(arguments: argparse.Namespace, root: Path) -> None:
    if arguments.action == "cut":
        from kiln import shipping

        shipping.cut(root, milestone=arguments.minor)
    elif arguments.action == "promote":
        from kiln import shipping

        shipping.promote(root, arguments.number, arguments.urgent)
    else:
        from kiln import release

        release.show_release_status(root, milestone=arguments.minor)


def _dispatch_score(arguments: argparse.Namespace) -> None:
    from kiln.grid import score

    root = arguments.path.resolve()
    if not root.is_dir():
        raise KilnError(f"no folder {arguments.path}")
    if arguments.online:
        from kiln.grid import forge

        score.refresh_end_of_life()
        forge.REFRESH = True
    report = score.score_repo(root)
    if arguments.rule or arguments.roadmap:
        from kiln.grid import roadmap

        if arguments.rule:
            roadmap.show_rule(report, score.rule_finding(report, arguments.rule), arguments.rule)
            return
        if arguments.write:
            written = roadmap.write_tickets(root, report)
            print(f"{len(written)} ticket(s) written in {roadmap.BACKLOG}: {', '.join(written)}")
        roadmap.show_roadmap(report)
    elif arguments.json:
        print(score.as_json(report))
    elif arguments.badge:
        print(score.badge(report))
    else:
        score.show(report, every=arguments.all)
        from kiln.dev.menu import is_interactive
        from kiln.grid import gap_report

        # Only a person at a terminal says yes: a script or a Claude session is never asked.
        gap_report.offer(root, report, input if is_interactive() else None)


def _add_grid_command(commands: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    from kiln.grid.model import LEVELS, THEMES

    grid_parser = commands.add_parser("grid", help="the rules kiln holds as the best, with sources")
    grid_parser.add_argument("rule", nargs="?", help="one rule, in full (its ID)")
    grid_parser.add_argument("--theme", choices=THEMES, help="only this theme")
    grid_parser.add_argument(
        "--scope", help="universal, language, framework, tool, domain, or a name"
    )
    grid_parser.add_argument("--level", choices=LEVELS, help="only this level")


def _add_score_command(commands: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    score_parser = commands.add_parser(
        "score", help="any repo measured against the grid, in seconds, no token"
    )
    score_parser.add_argument(
        "path", type=Path, nargs="?", default=Path(), help="the repo (default: here)"
    )
    score_parser.add_argument("--json", action="store_true", help="the report as JSON")
    score_parser.add_argument("--all", action="store_true", help="every rule and every location")
    score_parser.add_argument("--badge", action="store_true", help="a README badge (Markdown)")
    score_parser.add_argument(
        "--online",
        action="store_true",
        help="refresh end-of-life dates from endoflife.date and the GitHub settings",
    )
    score_parser.add_argument(
        "--roadmap", action="store_true", help="what needs judgment, for Claude, with its places"
    )
    score_parser.add_argument(
        "--write", action="store_true", help="with --roadmap: the items as backlog tickets"
    )
    score_parser.add_argument("--rule", help="one rule only: fails while its gap is open")


def _add_fix_command(commands: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    fix_parser = commands.add_parser(
        "fix", help="close by script every gap a script can close, on a branch, with proof"
    )
    fix_parser.add_argument(
        "path", type=Path, nargs="?", default=Path(), help="the repo (default: here)"
    )
    fix_parser.add_argument("--dry-run", action="store_true", help="the plan and the diff only")
    fix_parser.add_argument("--rule", help="only this rule (its ID)")


def _add_pause_command(commands: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    pause_parser = commands.add_parser(
        "pause", help="keep this Claude Code session's place, listed at the next start"
    )
    pause_parser.add_argument(
        "name", nargs="?", default="", help="the session in a few words (none: names proposed)"
    )
    pause_parser.add_argument("--next", default="", help="the next step")


def _add_waive_command(commands: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    waive_parser = commands.add_parser(
        "waive", help="waive a rule of kiln, or freeze a file (no argument: list)"
    )
    waive_parser.add_argument(
        "target", nargs="?", metavar="RULE|file", help="rule identifier, or generated file"
    )
    waive_parser.add_argument("--reason", default="", help="why (required)")
    waive_parser.add_argument("--paths", nargs="+", default=[], help="git patterns covered")
    waive_parser.add_argument(
        "--renew", action="store_true", help="renew: next step, reason asked again"
    )
    waive_parser.add_argument("--permanent", action="store_true", help="waiver with no deadline")
    waive_parser.add_argument("--upstream", default="", help="issue or PR opened on kiln")


def _add_new_command(commands: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    new_parser = commands.add_parser("new", help="generate a complete new project")
    new_parser.add_argument(
        "directory", type=Path, nargs="?", help="project folder (otherwise asked: project name)"
    )
    new_parser.add_argument("--name", help="short name (default: folder name)")
    new_parser.add_argument("--title", help="displayed title")
    new_parser.add_argument("--description", help="one sentence about the project")
    new_parser.add_argument("--owner", help="owning GitHub account")
    new_parser.add_argument("--team", help="comma-separated GitHub logins")
    new_parser.add_argument("--size", choices=SIZES, help="size of the project")
    new_parser.add_argument(
        "--type", dest="project_type", choices=PROJECT_TYPES, help="what you are building"
    )
    new_parser.add_argument("--backend", choices=BACKENDS, help="backend (otherwise suggested)")
    new_parser.add_argument("--frontend", choices=FRONTENDS, help="frontend (otherwise suggested)")
    new_parser.add_argument("--podman", action="store_true", help="podman containers")
    new_parser.add_argument(
        "--vps", metavar="USER@HOST", help="deploy to this server (Django + podman)"
    )
    new_parser.add_argument("--goal", help="north star of docs/backlog/")
    new_parser.add_argument("--language", choices=LANGUAGES, help="language of the team (en, fr)")
    new_parser.add_argument("--prod-url", help="health probe of production (status line)")
    new_parser.add_argument(
        "--no-github",
        action="store_true",
        help="do not create the GitHub repo (created by default)",
    )
    new_parser.add_argument("--no-install", action="store_true", help="install nothing")
    new_parser.add_argument("--template", help="template source (path or git URL)")
    new_parser.add_argument(
        "--all-questions", action="store_true", help="ask every question of the template"
    )


def _add_ci_command(commands: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    ci_parser = commands.add_parser("ci", help="replay a commit's CI on this machine")
    ci_parser.add_argument("revision", nargs="?", default="HEAD", help="commit (default: HEAD)")
    ci_parser.add_argument(
        "--skip", action="append", default=[], metavar="JOB", help="job of ci.yml to leave out"
    )
    ci_parser.add_argument("--no-push", action="store_true", help="keep the note local")
    ci_parser.add_argument("--keep", action="store_true", help="keep the commit's worktree")
    ci_parser.add_argument("--status", action="store_true", help="verdict only, no replay")


def _add_dev_command(commands: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    dev_parser = commands.add_parser("dev", help="run the project locally")
    dev_parser.add_argument(
        "action",
        nargs="?",
        choices=["status", "logs", "stop"],
        help="what runs in the background: its state, its output, or stop it",
    )
    dev_parser.add_argument("service", nargs="?", help="logs: this process only")
    dev_parser.add_argument(
        "--foreground", action="store_true", help="in this terminal, until Ctrl+C"
    )
    dev_parser.add_argument(
        "--only", type=lambda names: names.split(","), help="these processes only (django,nuxt)"
    )
    dev_parser.add_argument("-f", "--follow", action="store_true", help="logs: keep following")
    dev_parser.add_argument("--containers", action="store_true", help="the whole stack in podman")


def _check_dev_arguments(arguments: argparse.Namespace) -> None:
    if arguments.action != "logs" and (arguments.service or arguments.follow):
        raise KilnError("a service and --follow go with kiln dev logs")
    starting = arguments.foreground or arguments.containers or arguments.only
    if arguments.action is not None and starting:
        options = "--foreground, --only and --containers"
        raise KilnError(f"{options} start the project, not kiln dev {arguments.action}")
    if arguments.containers and arguments.only:
        raise KilnError("--containers runs the whole stack: no --only")


def _add_update_command(commands: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    update_parser = commands.add_parser("update", help="update the template and dependencies")
    update_parser.add_argument("--no-template", action="store_true", help="keep the architecture")
    update_parser.add_argument("--no-deps", action="store_true", help="keep the dependencies")
    update_parser.add_argument("--major", action="store_true", help="major versions included")
    update_parser.add_argument(
        "--all", action="store_true", help="every kiln repo, merged straight away"
    )
    update_parser.add_argument(
        "--rehearse",
        action="store_true",
        help="play the update on a throwaway clone first, the repo left untouched",
    )


def _new_project_request(arguments: argparse.Namespace) -> new.NewProjectRequest:
    from kiln import new

    directory = arguments.directory or Path(arguments.name or _ask_project_name())
    answers: dict[str, object] = {"name": arguments.name or directory.name}
    if arguments.title:
        answers["title"] = arguments.title
    if arguments.description:
        answers["description"] = arguments.description
    for key, value in (
        ("size", arguments.size),
        ("project_type", arguments.project_type),
        ("backend", arguments.backend),
        ("frontend", arguments.frontend),
    ):
        if value:
            answers[key] = value
    if arguments.podman:
        answers["podman"] = True
    if arguments.vps:
        answers.update(deploy="vps", vps_host=arguments.vps)
    if arguments.goal:
        answers["north_star"] = arguments.goal
    if arguments.language:
        answers["language"] = arguments.language
    if arguments.prod_url:
        answers["prod_health_url"] = arguments.prod_url
    if arguments.owner:
        answers["owner"] = arguments.owner
    if arguments.team:
        answers["team"] = [login.strip() for login in arguments.team.split(",")]
    if not arguments.all_questions:
        from kiln import questions

        answers = questions.ask_essentials(answers)
    return new.NewProjectRequest(
        destination=directory,
        answers=answers,
        template=arguments.template,
        should_install=not arguments.no_install,
        should_publish=not arguments.no_github,
        all_questions=arguments.all_questions,
    )


def _ask_project_name() -> str:
    """`kiln new` without a folder: the name is asked, the project lands in the current folder."""
    if not sys.stdin.isatty():
        raise KilnError("kiln new <folder>: the project folder is required outside a terminal")
    while True:
        name = input("Project name (lowercase, digits, dashes): ").strip()
        if PROJECT_NAME.fullmatch(name):
            return name
        print("Lowercase letters, digits and dashes only, starting with a letter.")


BANNER_ACTIONS = {
    "new": "new project",
    "adopt": "adoption",
    "install": "install",
    "update": "update",
    "status": "state of the repos",
    "doctor": "diagnosis",
}


def dispatch(arguments: argparse.Namespace) -> list[str]:
    """Runs the command; each module is imported on demand (copier, pulled by `new` and
    `update`, costs 0.4 s on its own, which `status`, `doctor` or `--version` need not pay).
    Returns the next steps to show after the recap, if any."""
    if arguments.command == "completion":
        print(generate_bash_completion())
        return []
    _show_banner(arguments)
    if arguments.command == "new":
        from kiln import new

        request = _new_project_request(arguments)
        return new.next_steps(request, new.create_project(request))
    if arguments.command == "doctor":
        from kiln import doctor

        doctor.run_doctor(Path.cwd())
    elif arguments.command == "grid":
        from kiln.grid import show

        if arguments.rule:
            show.show_rule(arguments.rule)
        else:
            show.list_rules(theme=arguments.theme, scope=arguments.scope, level=arguments.level)
    elif arguments.command == "score":
        _dispatch_score(arguments)
    elif arguments.command == "fix":
        from kiln.grid import fix

        fix.fix(arguments.path.resolve(), dry_run=arguments.dry_run, only=arguments.rule)
    elif arguments.command == "pause":
        from kiln import pause

        pause.pause(Path.cwd(), arguments.name, arguments.next)
    elif arguments.command == "version":
        _dispatch_version(arguments, repo_root(Path.cwd()))
    elif arguments.command == "status" or (arguments.command == "update" and arguments.all):
        _dispatch_fleet(arguments)
    elif arguments.command == "install" and (arguments.machine or not _is_in_repo()):
        from kiln import install

        install.install_machine()
    elif arguments.command == "set" and (
        arguments.machine or not _is_in_repo() or _machine_keys_only(arguments.assignments)
    ):
        from kiln import machine

        machine.run_machine(arguments.assignments)
    else:
        _dispatch_in_repo(arguments, _repo_root_or_hint())
    return []


def _dispatch_in_repo(arguments: argparse.Namespace, root: Path) -> None:
    """Commands that work in the current repo."""
    command = arguments.command
    if command == "adopt":
        from kiln import adopt

        adopt.adopt_project(
            root, size=arguments.size or adopt.DEFAULT_SIZE, template=arguments.template
        )
    elif command == "install":
        from kiln import install

        install.install_project(root)
    elif command == "publish":
        from kiln import new

        new.publish_project(root)
    elif command == "update" and arguments.rehearse:
        from kiln import rehearsal

        rehearsal.rehearse_project(
            root, should_update_deps=not arguments.no_deps, allow_major=arguments.major
        )
    elif command == "update":
        from kiln import update

        update.update_project(
            root,
            should_update_template=not arguments.no_template,
            should_update_deps=not arguments.no_deps,
            allow_major=arguments.major,
        )
    elif command == "dev":
        from kiln import dev

        _check_dev_arguments(arguments)
        dev.run_dev(
            root,
            arguments.action,
            in_containers=arguments.containers,
            foreground=arguments.foreground,
            only=arguments.only,
            follow=arguments.follow,
            service=arguments.service,
        )
    elif command == "check":
        from kiln import check

        check.check_project(root, arguments.tests, arguments.all)
    elif command == "ci":
        _dispatch_ci(root, arguments)
    elif command == "contract":
        from kiln import contract
        from kiln.stack import load_stack

        contract.generate_api_contract(root, load_stack(root))
    elif command == "waive":
        _dispatch_waive(root, arguments)
    elif command == "set":
        from kiln import settings

        if arguments.assignments:
            settings.apply_settings(root, arguments.assignments)
        else:
            settings.show_settings(root)


def _machine_keys_only(assignments: list[str]) -> bool:
    from kiln import machine

    return machine.only_machine_keys(assignments)


def _is_in_repo() -> bool:
    try:
        repo_root(Path.cwd())
    except KilnError:
        return False
    return True


def _repo_root_or_hint() -> Path:
    """Root of the current repo; outside one, the error says where to go and what to run here."""
    try:
        return repo_root(Path.cwd())
    except KilnError:
        from kiln import fleet

        code_dir = load_config().code_dir
        names = (
            [str(repo.root.relative_to(code_dir)) for repo in fleet.find_repos(code_dir)]
            if code_dir.is_dir()
            else []
        )
        repos_line = f" kiln repos in {code_dir}: {', '.join(names)}." if names else ""
        raise KilnError(
            f"{Path.cwd()} is not in a repo: go into one first (cd <repo>).{repos_line} "
            "From here: kiln status, kiln update --all, kiln set (this machine's settings), "
            "kiln install (kiln for this machine), kiln new."
        ) from None


def _show_banner(arguments: argparse.Namespace) -> None:
    """Banner of the long commands; the fleet's repos are in the code folder."""
    action = BANNER_ACTIONS.get(arguments.command)
    if action is None:
        return
    if (
        arguments.command in ("new", "status", "doctor")
        or getattr(arguments, "all", False)
        or (arguments.command == "install" and (arguments.machine or not _is_in_repo()))
    ):
        banner.show_banner(action if arguments.command != "update" else "update of the repos")
        return
    banner.show_banner(action, _repo_root_or_hint())


def _dispatch_ci(root: Path, arguments: argparse.Namespace) -> None:
    from kiln import ci

    if arguments.status:
        if not ci.show_verdict(root, arguments.revision):
            sys.exit(EXIT_FAILURE)
        return
    skipped_jobs = frozenset(arguments.skip)
    ci.require_known_jobs(root, skipped_jobs)
    verdict = ci.run_local_ci(
        root,
        arguments.revision,
        skipped_jobs,
        should_push=not arguments.no_push,
        should_keep=arguments.keep,
    )
    print("\n" + verdict.render(), end="")
    if not verdict.is_success:
        sys.exit(EXIT_FAILURE)


def _dispatch_waive(root: Path, arguments: argparse.Namespace) -> None:
    from kiln import waive

    if arguments.target is None:
        waive.show_waivers(root)
        return
    waive.waive(
        root,
        waive.WaiveRequest(
            target=arguments.target,
            reason=arguments.reason,
            paths=tuple(arguments.paths),
            renew=arguments.renew,
            permanent=arguments.permanent,
            upstream=arguments.upstream,
        ),
    )


def _dispatch_fleet(arguments: argparse.Namespace) -> None:
    from kiln import fleet

    code_dir = load_config().code_dir
    fleet.require_code_dir(code_dir)
    if arguments.command == "status":
        fleet.show_status(code_dir)
    else:
        fleet.update_all(code_dir, allow_major=arguments.major, rehearse=arguments.rehearse)


def show_home(parser: argparse.ArgumentParser) -> None:
    roles = {"update --all": FLEET_UPDATE_ROLE}
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            roles |= {choice.dest: choice.help or "" for choice in action._choices_actions}
    banner.show_home(
        [
            (title, [(name, roles[name][:1].upper() + roles[name][1:]) for name in names])
            for title, names in COMMAND_GROUPS
        ],
        EXAMPLES,
    )


def main() -> None:
    try:
        parser = build_parser()
        if sys.argv[1:] in HELP_FLAGS:
            show_home(parser)
            return
        arguments = parser.parse_args(modernize(sys.argv[1:]))
        started = time.monotonic()
        try:
            steps = dispatch(arguments)
        except KilnError:
            _recap(arguments, started, succeeded=False)
            raise
        _recap(arguments, started, succeeded=True)
        if steps:
            ui.panel("Next steps", steps)
        tool_update.offer(arguments.command)
    except KilnError as error:
        ui.error(str(error))
        sys.exit(EXIT_FAILURE)
    except KeyboardInterrupt:
        # Ctrl-C: the cleanups already ran on the way out (copies, containers), no traceback.
        print()
        ui.note("Interrupted.")
        sys.exit(EXIT_INTERRUPTED)


def _recap(arguments: argparse.Namespace, started: float, *, succeeded: bool) -> None:
    """Recap of the commands with steps; `dev` runs until stopped, `ci` has its verdict."""
    if arguments.command not in NO_RECAP_COMMANDS:
        ui.recap(arguments.command, started, succeeded=succeeded)
