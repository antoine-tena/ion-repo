"""Suivi du travail : conversion de l'ancien `docs/a-faire/` en `docs/backlog/`, et de l'ancien
`backlog.md` unique en tickets ouverts et `done.md`."""

import subprocess
from pathlib import Path

from ion_repo.backlog import add_after_update_ticket, migrate_legacy_backlog, split_backlog
from ion_repo.versions import ReleaseNotes

TEMPLATE_BACKLOG = (
    Path(__file__).parent.parent / "template/docs/backlog/backlog.md.jinja"
).read_text()

LEGACY = """# À faire

Tout ce qu'il reste à faire sur Demo, en une seule liste rangée par criticité. Créée le
**2026-01-02**. Ce qui est fait est dans la section « ✅ Fait » en bas.

La boussole est **la démo en ligne**.

---

## Mode d'emploi (humains et agents)

- **Identifiant** `AF-NN` : stable. **Prochain libre : AF-04.**

---

## 🔴 Critique

### AF-01 · Livrer la démo
- **État** : en cours — branche feat/demo, depuis le 3 janvier
- **Effort** : S · **Qui** : Claude · **Échéance** : —
- **Origine** : réunion

Après AF-03.
- [ ] Une étape.

## ⚪ Fond — chantiers longs et dette

### AF-03 · Nettoyer
- **État** : bloqué — attend antoine
- **Effort** : XS · **Qui** : — · **Échéance** : —
- **Origine** : —

---

## ✅ Fait

### Journal

- **2026-01-02** · AF-02 · Démarrer — fait (feat/init)
"""


def git(root: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True)


def test_legacy_tracker_becomes_an_english_backlog(tmp_path: Path) -> None:
    legacy = tmp_path / "docs/a-faire"
    legacy.mkdir(parents=True)
    (legacy / "a-faire.md").write_text(LEGACY)
    (legacy / "ecarte.md").write_text("# Écarté\n\n## Sans suite\n\n- AF-09 · Abandonné\n")
    (legacy / "urgent.md").write_text("# Urgent\n\nTexte.\n\n- [ ] Payer — antoine\n  suite\n")
    (legacy / "audit-api-2026-01-03.md").write_text("# Audit\n")
    git(tmp_path, "init", "-q")
    git(tmp_path, "add", ".")
    git(
        tmp_path,
        "-c",
        "user.name=t",
        "-c",
        "user.email=t@t",
        "commit",
        "-qm",
        "init",
        "--date=2026-01-02T10:00:00",
    )
    backlog = tmp_path / "docs/backlog"
    backlog.mkdir(parents=True)
    (backlog / "backlog.md").write_text(TEMPLATE_BACKLOG)
    (backlog / "urgent.md").write_text("# Urgent\n\nWhat only a human can do.\n")

    assert migrate_legacy_backlog(tmp_path)

    text = (backlog / "backlog.md").read_text()
    assert "North star: **la démo en ligne**." in text
    assert "Next free: T-04." in text
    assert "**2026-01-02**" in text
    assert "### T-01 · Livrer la démo" in text
    assert "- **Status**: in progress — branch feat/demo, since 3 janvier" in text
    assert text.count("- **Opened**: 2026-01-02") == 2
    assert "- **Effort**: S · **Owner**: — · **Due**: —" in text
    assert "- **Status**: blocked — waiting for antoine" in text
    assert "## ⚪ Background — long-running work, debt and ideas" in text
    assert "Après T-03." in text
    assert "- **2026-01-02** · T-02 · Démarrer" in text
    assert "AF-" not in text and "État" not in text and "Mode d'emploi" not in text
    assert "## Dropped" in (backlog / "rejected.md").read_text()
    assert "T-09" in (backlog / "rejected.md").read_text()
    urgent = (backlog / "urgent.md").read_text()
    assert urgent.startswith("# Urgent\n\nWhat only a human can do.\n")
    assert "- [ ] Payer — antoine\n  suite\n" in urgent
    assert (backlog / "audit-api-2026-01-03.md").exists()
    assert not legacy.exists()


def test_nothing_to_migrate(tmp_path: Path) -> None:
    assert not migrate_legacy_backlog(tmp_path)


def test_tracker_deleted_by_copier_is_read_back_from_the_last_commit(tmp_path: Path) -> None:
    legacy = tmp_path / "docs/a-faire"
    legacy.mkdir(parents=True)
    (legacy / "a-faire.md").write_text(LEGACY)
    git(tmp_path, "init", "-q")
    git(tmp_path, "add", ".")
    git(tmp_path, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "init")
    (legacy / "a-faire.md").unlink()  # Copier retire un fichier que le modèle n'a plus
    legacy.rmdir()
    (tmp_path / "docs/backlog").mkdir()
    (tmp_path / "docs/backlog/backlog.md").write_text(TEMPLATE_BACKLOG)

    assert migrate_legacy_backlog(tmp_path)

    assert "### T-01 · Livrer la démo" in (tmp_path / "docs/backlog/backlog.md").read_text()


BACKLOG_WITH_CRITICAL = """# Backlog

- **ID** `T-NN`: stable. **Next free: T-07.**

## 🔴 Critical

### T-03 · Something else
"""
NOTES = [
    ReleaseNotes("v0.4.1", "", ["- **After updating**: give each owner's @login"]),
    ReleaseNotes("v0.4.0", "", ["- kiln doctor", "- **After updating**: rename the bucket"]),
]


def test_after_updating_lines_become_one_critical_ticket(tmp_path: Path) -> None:
    backlog = tmp_path / "docs/backlog/backlog.md"
    backlog.parent.mkdir(parents=True)
    backlog.write_text(BACKLOG_WITH_CRITICAL)

    assert add_after_update_ticket(tmp_path, NOTES, today="2026-10-19") == "T-07"
    assert add_after_update_ticket(tmp_path, NOTES, today="2026-10-20") is None

    text = backlog.read_text()
    assert "**Next free: T-08.**" in text
    assert text.index("### T-07 · Finish the kiln update to v0.4.1") < text.index("### T-03")
    assert "- **Opened**: 2026-10-19" in text
    assert "- [ ] rename the bucket (v0.4.0)\n- [ ] give each owner's @login (v0.4.1)" in text


def test_nothing_to_do_no_ticket(tmp_path: Path) -> None:
    backlog = tmp_path / "docs/backlog/backlog.md"
    backlog.parent.mkdir(parents=True)
    backlog.write_text(BACKLOG_WITH_CRITICAL)

    assert (
        add_after_update_ticket(tmp_path, [ReleaseNotes("v0.4.1", "", ["- x"])], today="d") is None
    )
    assert add_after_update_ticket(tmp_path / "elsewhere", NOTES, today="d") is None
    assert backlog.read_text() == BACKLOG_WITH_CRITICAL


def test_a_hand_kept_tracker_keeps_its_compass_its_numbers_and_its_notes(tmp_path: Path) -> None:
    legacy = LEGACY.replace(
        "La boussole est **la démo en ligne**.",
        (
            "La production tourne la **v1.1** (voir AF-03).\n\n"
            "La boussole est la **première sortie**, le 21 novembre."
        ),
    ).replace("**Prochain libre : AF-04.**", "le plus grand (**prochain libre : AF-02**).")
    legacy = legacy.replace("- **État** : bloqué — attend antoine", "- **État** : à faire (AF-01)")
    (tmp_path / "docs/a-faire").mkdir(parents=True)
    (tmp_path / "docs/a-faire/a-faire.md").write_text(legacy)
    (tmp_path / "docs/a-faire/urgent.md").write_text("# Urgent\n\n- [ ] Vérifier AF-01\n")
    backlog = tmp_path / "docs/backlog"
    backlog.mkdir(parents=True)
    (backlog / "backlog.md").write_text(TEMPLATE_BACKLOG)

    assert migrate_legacy_backlog(tmp_path)

    text = (backlog / "backlog.md").read_text()
    assert "North star: **première sortie**." in text
    assert "Next free: T-04." in text  # AF-03 is taken: the stale AF-02 is not reused
    assert "La production tourne la **v1.1** (voir T-03)." in text
    assert text.index("La production tourne") < text.index("## 🔴")
    assert "- **Status**: todo (T-01)" in text
    assert "Vérifier T-01" in (backlog / "urgent.md").read_text()


FORMER_BACKLOG = """# Backlog

Everything left to do on Demo, in a single list ordered by priority. Started on
**2026-01-02**. What is done is in the "✅ Done" section at the bottom; what was turned
down is in [rejected.md](rejected.md). **Nothing else is open.**

North star: **the demo online**.

---

## How to use (humans and agents)

- **ID** `T-NN`: stable, never reused. **Next free: T-09.**

---

## 🔴 Critical

### T-08 · Ship the demo
- **Status**: todo

## ⚪ Background — long-running work, debt and ideas

---

## ✅ Done

### Log

One line per closed ticket, most recent first:
`- **YYYY-MM-DD** · T-NN · Title — what was done (branch) · opened YYYY-MM-DD`.

- **2026-02-01** · T-07 · Pay the host — done (fix/host) · opened 2026-01-05
"""
DONE_INTRO = "# Done\n\nThe closed tickets of Demo, most recent first, one line each.\n"


def test_the_former_single_backlog_is_split_from_the_last_commit(tmp_path: Path) -> None:
    folder = tmp_path / "docs/backlog"
    folder.mkdir(parents=True)
    (folder / "backlog.md").write_text(FORMER_BACKLOG)
    git(tmp_path, "init", "-q")
    git(tmp_path, "add", ".")
    git(tmp_path, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "init")
    # Copier's merge of the new layout: the log left loose at the bottom.
    (folder / "backlog.md").write_text("merged by Copier\n- **2026-02-01** · T-07 · loose\n")
    (folder / "done.md").write_text(DONE_INTRO)

    assert split_backlog(tmp_path)

    backlog = (folder / "backlog.md").read_text()
    assert "How to use" not in backlog and "Done" not in backlog and "T-07" not in backlog
    assert "### T-08 · Ship the demo" in backlog
    assert "**Next free: T-09.**\n\n---\n\n## 🔴 Critical" in backlog
    assert "[done.md](done.md)" in backlog
    assert backlog.endswith("## ⚪ Background — long-running work, debt and ideas\n")
    entry = "- **2026-02-01** · T-07 · Pay the host — done (fix/host) · opened 2026-01-05"
    assert (folder / "done.md").read_text() == f"{DONE_INTRO}\n{entry}\n"
    # Already split: nothing more to do once committed.
    git(tmp_path, "add", ".")
    git(tmp_path, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "split")
    assert not split_backlog(tmp_path)


def test_the_template_backlog_needs_no_split(tmp_path: Path) -> None:
    folder = tmp_path / "docs/backlog"
    folder.mkdir(parents=True)
    (folder / "backlog.md").write_text(TEMPLATE_BACKLOG)

    assert not split_backlog(tmp_path, from_disk=True)
    assert not split_backlog(tmp_path)  # not a git repo
