---
name: backup-claude-setup
description: Back up Riley's Claude setup — routines (scheduled triggers) to the private claude-private-routines repo, and Claude Code settings to the Riley-Claude-Skills hub repo — and restore them. Use whenever Riley says "back up my Claude setup", "save my routines", "snapshot my config", "back up my settings", or "restore my routines/settings", and run it at the end of any session that created, changed, or deleted a routine or changed his settings. For backing up a SKILL itself, use publish-skill-to-github instead — that routes skills to the domain repos; this one handles routines and settings.
---

# Back up Claude setup

Riley's **skills** live in three domain repos (handled by `publish-skill-to-github`).
His **routines** and **Claude Code settings** live only in his account — nothing
versions them unless this skill does. This skill snapshots **routines** into the
private **`rileytrottier23/claude-private-routines`** repo and **settings** into the
public **`rileytrottier23/Riley-Claude-Skills`** hub repo, and restores them on request.
Run it whenever Riley asks, and at the end of any session that created, changed, or
deleted a routine or changed his settings. For backing up a SKILL itself, use
`publish-skill-to-github` instead.

**Routines never go in a public repo.** Their prompts describe which personal sources
Claude reads (mail, calendar, journal, task lists). If the private repo can't be
pushed to, stop and tell Riley — never fall back to the hub.

Scope, so the two skills don't collide:

| What changed | Skill | Goes to |
|---|---|---|
| A skill (SKILL.md, .skill file, vendored skill) | `publish-skill-to-github` | domain repo (`mine/` or `vendored/`) |
| A routine / scheduled trigger | **this skill** | private repo `claude-private-routines`, `routines/` |
| Claude Code settings / plugins / prefs | **this skill** | hub repo `config/` |

## Preflight: where am I, and can I push?

`git -C <clone> push --dry-run origin main` (or the designated branch) answers both.

- **Local terminal on Riley's machine:** if the repo is checked out, `git pull`
  and work in it directly.
- **Cloud / remote session:** the container can't see his machine. Read is
  anonymous for the public hub; the private repo and all writes need the repo in the
  session's authorized set. If an `add_repo` tool exists, call it with `access: "push"` for
  `rileytrottier23/claude-private-routines` (routines) and/or
  `rileytrottier23/Riley-Claude-Skills` (settings). If push is still blocked, do the work,
  commit, and hand back a `git format-patch` (or the changed files) with
  `SendUserFile` plus the exact push commands. Never force, never push elsewhere.

Clone if needed:

```bash
cd /tmp && rm -rf cpr && git clone https://github.com/rileytrottier23/claude-private-routines.git cpr   # routines
cd /tmp && rm -rf rcs && git clone https://github.com/rileytrottier23/Riley-Claude-Skills.git rcs      # settings
```

## Back up routines

1. Call the `list_triggers` tool (claude-code-remote MCP; load it with `ToolSearch`
   if it isn't already available). Take the **full** result — including each
   routine's complete prompt.
2. Save that JSON to a file, e.g. `/tmp/triggers.json`. Pass the raw tool envelope
   as-is; the formatter accepts either `{"data": [...]}` or a bare list.
3. Run the formatter from the **private** repo root (`cpr`):

   ```bash
   python3 scripts/format_routines.py /tmp/triggers.json
   ```

   It writes one `routines/<slug>.json` per routine (each with a `restore` block),
   regenerates `routines/INDEX.md`, and **prunes** files for routines that no
   longer exist — so a routine Riley deleted disappears from the backup too.

Do **not** hand-write routine files; always regenerate from live `list_triggers`
output so the backup matches reality, deletions included.

## Back up settings

`config/settings.baseline.json` in the hub is a portable, secret-free `settings.json`
(marketplaces, enabled plugins, preferences). It changes rarely. Refresh it only
when the real setup changed:

- New skills **marketplace** added, or a **plugin** enabled/disabled → update
  `extraKnownMarketplaces` / `enabledPlugins`. Confirm the live set with the
  `ListPlugins` tool if unsure.
- A preference Riley wants to keep (theme, notification toggles, a new
  `permissions.allow` entry) → update the matching field.

Never put a secret in this file (tokens, keys, connector credentials). Never copy
the CCR cloud-session hook scripts or `launcher-settings.json` in — those are the
remote runtime's, not Riley's config. See `config/README.md`.

## Commit and push

```bash
cd /tmp/cpr && git add routines/ && git commit -m "Back up routines" && git push origin main   # private
cd /tmp/rcs && git add config/   && git commit -m "Back up settings" && git push origin main   # public hub
```

Before pushing to the private repo, confirm it is still private
(`get_file_contents` / repo search shows `"private": true`).

Straight-to-main is the convention for these repos. If a session's own harness rules
require a branch + PR, follow those instead (session override, not a repo rule).
If the push is rejected because main moved, `git pull --rebase` once and retry.

## Restore

- **A routine:** read the target `routines/<slug>.json` in `claude-private-routines` and call `create_trigger`
  with its `restore` block (`name`, `prompt`, `initiation`, the schedule, and
  `create_new_session_on_fire` when present). The recreated routine gets a new
  `trig_…` id — back up again afterward so the file reflects it. `cron_expression`
  is UTC.
- **Settings:** copy `config/settings.baseline.json` to `~/.claude/settings.json`
  (or merge the fields Riley wants), then `/plugin marketplace update` to fetch the
  marketplaces. Or just: "apply my settings baseline."

## Report

Two sentences: what got backed up (routine count, whether settings changed), and
the commit URL. If anything was pruned or a routine looked new, say so.
