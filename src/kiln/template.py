"""Access to the Copier template: default source and tracked revision."""

import os

from kiln.shell import KilnError
from kiln.versions import installed_version, latest_release, tool_release_tag, upgrade_command

DEFAULT_TEMPLATE_SOURCE = "https://github.com/antoine-tena/kiln.git"
TEMPLATE_SOURCE_VARIABLE = "KILN_TEMPLATE"
# Revision of a local or explicit template (kiln development): its last commit.
LOCAL_TEMPLATE_REVISION = "HEAD"


def template_source(explicit_source: str | None) -> str:
    """Template source: option, then environment variable, then the GitHub repo."""
    if explicit_source:
        return explicit_source
    return os.environ.get(TEMPLATE_SOURCE_VARIABLE, DEFAULT_TEMPLATE_SOURCE)


def template_revision(source: str) -> str:
    """The published template is taken at the installed tool's release, neither newer nor
    older: the conversions from one version to the next live in the tool's code. A tool that is
    not a release (a checkout ahead of its tag, a branch) is refused: no template matches its
    code, and the repo would follow kiln's `develop`. A local or explicit template is taken at
    its last commit."""
    if source != DEFAULT_TEMPLATE_SOURCE:
        return LOCAL_TEMPLATE_REVISION
    tag = tool_release_tag()
    if tag is None:
        latest = latest_release()
        install = upgrade_command(latest) if latest else "install a release of kiln"
        raise KilnError(
            f"this kiln is not a release ({installed_version()}): no template matches its code. "
            f"Install a release: {install}. To try kiln's own code on a scratch repo: "
            f"{TEMPLATE_SOURCE_VARIABLE}=<kiln checkout>."
        )
    return tag
