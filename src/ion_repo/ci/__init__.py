"""`ion repo ci`: the CI of `ci.yml` replayed on this machine, verdict as a git note on the
commit."""

from ion_repo.ci.runner import require_known_jobs, run_local_ci, show_verdict

__all__ = ["require_known_jobs", "run_local_ci", "show_verdict"]
