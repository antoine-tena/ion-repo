"""Accès au modèle Copier : source par défaut et révision suivie."""

import os

from kiln.versions import tool_release_tag

DEFAULT_TEMPLATE_SOURCE = "https://github.com/antoine-tena/kiln.git"
TEMPLATE_SOURCE_VARIABLE = "KILN_TEMPLATE"
# Révision d'un modèle local ou explicite (développement de kiln) : son dernier commit.
LOCAL_TEMPLATE_REVISION = "HEAD"


def template_source(explicit_source: str | None) -> str:
    """Source du modèle : option, puis variable d'environnement, puis dépôt GitHub."""
    if explicit_source:
        return explicit_source
    return os.environ.get(TEMPLATE_SOURCE_VARIABLE, DEFAULT_TEMPLATE_SOURCE)


def template_revision(source: str) -> str | None:
    """Le modèle publié se prend à la version de l'outil installé, jamais plus récent : les
    conversions d'une version à l'autre vivent dans le code de l'outil. Si l'outil ne se situe
    pas, la dernière version (None : Copier choisit le tag le plus récent). Un modèle local ou
    explicite se prend à son dernier commit."""
    if source != DEFAULT_TEMPLATE_SOURCE:
        return LOCAL_TEMPLATE_REVISION
    return tool_release_tag()
