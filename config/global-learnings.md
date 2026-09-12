# Global learnings

A versioned mirror of the `## Learnings` section in Riley's account-wide
`~/.claude/CLAUDE.md` — the file every Claude Code session loads regardless of
which project it's in. `~/.claude/CLAUDE.md` itself lives only on his machine
(or inside a session's container) and isn't tracked anywhere; this file is
what makes a bad global lesson visible in a diff and revertible, the same way
`settings.baseline.json` does for settings.

Kept and pruned by the **`self-improve`** skill (`control-plane/self-improve/`).
See that skill for the rules on what belongs here versus in a promoted skill
versus a project's own `CLAUDE.md` — short version: only lessons that would be
true and useful in *any* session belong in this file. Everything else either
gets promoted into a real skill (loads on demand, doesn't tax every session)
or stays local to the project it came from.

**Never put a secret, client/company name, or proprietary detail here** — this
repo is public, and this file is exactly as visible as `README.md`.

## Learnings

*(empty — nothing captured yet)*

## Adopting this on a machine

```bash
# append this section into ~/.claude/CLAUDE.md (create the file if it doesn't exist)
cat config/global-learnings.md >> ~/.claude/CLAUDE.md
```

Or just ask Claude: *"apply my global learnings from config/global-learnings.md."*
