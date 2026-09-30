# Global learnings

The source of truth for the `## Learnings` section of Riley's account-wide
`~/.claude/CLAUDE.md`, the file every local Claude Code session loads regardless
of project. Each machine copies this section in automatically (see "Adopting this
on a machine" below), so a bad global lesson is visible in a diff and revertible,
the same way `settings.baseline.json` is for settings.

Kept and pruned by the **`self-improve`** skill (`control-plane/self-improve/`).
See that skill for the rules on what belongs here versus in a promoted skill
versus a project's own `CLAUDE.md` — short version: only lessons that would be
true and useful in *any* session belong in this file. Everything else either
gets promoted into a real skill (loads on demand, doesn't tax every session)
or stays local to the project it came from.

**Never put a secret, client/company name, or proprietary detail here** — this
repo is public, and this file is exactly as visible as `README.md`.

## Learnings

- 2026-09-29: **Task list for shared work:** whenever Riley and Claude work on a task with 3+ steps, create a task list before the first real step, tick items off as they finish, and make the last item checking the work. For reply layout (answer first, tables, scorecards, decisions set apart, diagrams for flows), use the `visual-output` skill.

## Adopting this on a machine

Paste one line, once per machine. It copies the section above into
`~/.claude/CLAUDE.md` and adds a hook that re-syncs at the start of every
local Claude Code session, so later learnings arrive on their own.

**Windows (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/rileytrottier23/Riley-Claude-Skills/main/scripts/sync-claude-setup.ps1 | iex
```

**Mac / Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/rileytrottier23/Riley-Claude-Skills/main/scripts/sync-claude-setup.sh | bash
```

This file is the source of truth: edits made only to a machine's `## Learnings`
section are overwritten on the next sync. Cloud sessions and the Claude app
don't read `~/.claude/CLAUDE.md`.
