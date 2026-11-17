# ion-repo#T-413 · Django template: double bookings refused by the database
- **Type**: improvement
- **Priority**: 🟠 important
- **Status**: todo
- **Opened**: 2026-11-02
- **Effort**: S · **Owner**: — · **Due**: —
- **Origin**: `studio/docs/business/fabrication/reservation.md`, "Ce qui va dans un outil Ion" (booking)

Two requests for the same slot, a few milliseconds apart: only the database can refuse the second.
A PostgreSQL exclusion constraint (`ExclusionConstraint` on a `tstzrange` and the resource,
`btree_gist`), and the `IntegrityError` turned into a clear refusal (409 with an error code), not
a 500. annski has no such constraint (its seats are counted under a lock): the pattern comes
from booking and serves any reservation.
