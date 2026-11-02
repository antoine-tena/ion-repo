"""ion-score's grid against ion-repo's template: a rule cites only charter rules the template
writes."""

import re
from pathlib import Path

from ion_score import model

RULES = model.load_rules()


def test_a_rule_names_only_charter_rules_ion_repo_knows() -> None:
    template = Path(__file__).resolve().parent.parent / "template"
    known = {
        found
        for path in [
            *template.glob(".claude/rules/ion-repo/*.jinja"),
            template / "charter.toml.jinja",
        ]
        for found in re.findall(r"\[([A-Z0-9+-]{3,})\]|id = \"([A-Z0-9+-]+)\"", path.read_text())
        for found in found
        if found
    }

    assert {rule.charter_rule for rule in RULES if rule.charter_rule} <= known
