"""ion-repo: generates a complete project and keeps it up to date."""

from ion_repo import resync

# Before any other import: an install from the checkout may lag behind its dependencies.
resync.ensure()
