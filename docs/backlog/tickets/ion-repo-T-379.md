# ion-repo#T-379 · Django template: `django-stubs-ext`, so `admin.ModelAdmin[Model]` runs
- **Type**: improvement
- **Priority**: 🟡 normal
- **Status**: todo
- **Opened**: 2026-10-30
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: emberstudio session `feat/auth`, 30 October 2026

mypy `strict` with django-stubs wants `admin.ModelAdmin[Invitation]`, which raises `TypeError:
type 'ModelAdmin' is not subscriptable` at import without `django_stubs_ext.monkeypatch()`. The
session dropped its admin rather than fight it. The template adds `django-stubs-ext` and calls
`monkeypatch()` in `settings.py`, so a typed admin works from the first model.
