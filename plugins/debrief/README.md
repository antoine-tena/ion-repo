# debrief

The `debrief` output style of ion-repo's `repo` plugin, alone: no skills, hooks or status line.
The message that closes a piece of work opens with the real git state in bold, then **◆ Done**,
**◆ Critical**, **◆ To do** and **◆ Blocked:**, titled in your language, a part with nothing in it
left out.

```
/plugin install debrief --marketplace antoine-tena/ion-repo
```

Pick it with `/output-style` (`debrief:debrief`); it never replaces the style you chose. With
ion-repo's `repo` plugin installed, you already have it as `repo:debrief`.
