"""Access to the Copier template: default source and tracked revision."""

import os

from ion_repo.shell import KilnError
from ion_repo.versions import (
    installed_build,
    installed_version,
    is_beta,
    latest_release,
    tool_release_tag,
    upgrade_command,
)

DEFAULT_TEMPLATE_SOURCE = "https://github.com/antoine-tena/kiln.git"
TEMPLATE_SOURCE_VARIABLE = "KILN_TEMPLATE"
# Revision of a local or explicit template (kiln development): its last commit.
LOCAL_TEMPLATE_REVISION = "HEAD"
# `git describe --dirty`: the checkout has uncommitted changes.
DIRTY_SUFFIX = "-dirty"


def template_source(explicit_source: str | None) -> str:
    """Template source: option, then environment variable, then the GitHub repo."""
    if explicit_source:
        return explicit_source
    return os.environ.get(TEMPLATE_SOURCE_VARIABLE, DEFAULT_TEMPLATE_SOURCE)


def template_revision(source: str) -> str:
    """The published template is taken at the installed tool's release, neither newer nor
    older: the conversions from one version to the next live in the tool's code. A tool that is
    not a release (a checkout ahead of its tag, a branch) is refused: no template matches its
    code, and the repo would follow kiln's `develop`; on the `beta` channel, that is the point,
    and the template is taken at the tool's own commit. A local or explicit template is taken
    at its last commit."""
    if source != DEFAULT_TEMPLATE_SOURCE:
        return LOCAL_TEMPLATE_REVISION
    tag = tool_release_tag()
    if tag is None and is_beta():
        return beta_revision()
    if tag is None:
        latest = latest_release()
        install = upgrade_command(latest) if latest else "install a release of kiln"
        raise KilnError(
            f"this kiln is not a release ({installed_version()}): no template matches its code. "
            f"Install a release: {install}. To try kiln's own code on a scratch repo: "
            f"{TEMPLATE_SOURCE_VARIABLE}=<kiln checkout>."
        )
    return tag


def beta_revision() -> str:
    """The commit of `develop` the tool runs (`v0.4.4-16-gf767dbf`, which git resolves), pushed:
    Copier clones the template from GitHub. Uncommitted changes match no commit: refused."""
    built = installed_build()
    if not built or built.endswith(DIRTY_SUFFIX):
        raise KilnError(
            f"beta channel: kiln's checkout has uncommitted changes ({built or 'build unknown'}); "
            "commit and push them, the template is taken at a commit of GitHub."
        )
    return built
