# Project skills

These skills load automatically in **cloud sessions run against this repository** —
Claude Code loads a repo's `.claude/skills/` at session start, so no account upload
or `/plugin` step is needed for them to trigger here.

**Scope:** this covers cloud sessions on `Riley-Claude-Skills` only. To make these
skills available *everywhere* (Cowork, other repos, all sessions), enable them for
your **claude.ai account** (Customize → Skills, or the skills settings on claude.ai) —
see [`../../config/README.md`](../../config/README.md).

| Skill | What it does |
|---|---|
| [decision-partner](./decision-partner) | A skeptical questioner for a decision you're facing. |
| [decision-review](./decision-review) | Reviews a decision you already made — reasoning vs. outcome. |
| [practice-partner](./practice-partner) | Turns "I want to get better at X" into a deliberate-practice plan. |
| [reflection-partner](./reflection-partner) | Runs your weekly/monthly/annual reflection. |
| [publish-skill-to-github](./publish-skill-to-github) | Routes a new/edited skill to the right domain repo and updates its README/marketplace/changelog. |
| [backup-claude-setup](./backup-claude-setup) | Backs up routines + settings to this hub and restores them. |

`publish-skill-to-github` and `backup-claude-setup` are duplicated from their canonical
homes (the domain repo and `control-plane/`) so they load as project skills here; the
canonical copies remain the source of truth.
