# Claude Code settings

A portable, **secret-free** baseline of Riley's Claude Code configuration, so a
fresh install (new machine, reset account, teammate copy) can be brought up to
the same setup in one file — every skills marketplace registered, every plugin
enabled, and the personal preferences that make the harness feel like Riley's.

## What's here

- **`settings.baseline.json`** — a complete `settings.json` you can drop in:
  registers all four skills marketplaces, enables the nine plugins, and sets the
  preferences below.

## What the baseline configures

| Setting | Value | Why |
|---|---|---|
| `theme` | `dark` | Riley's preference |
| `autoUpdatesChannel` | `latest` | plugins pick up `git pull` updates automatically |
| `enableWorkflows` | `true` | required for the plugin/skill system |
| `permissions.allow` | `["Skill"]` | **skills invoke without a permission prompt** — central to "trigger easily, don't ask to use them" |
| `inputNeededNotifEnabled` | `false` | no nudge when input is needed |
| `agentPushNotifEnabled` | `true` | push when a background agent finishes |
| `extraKnownMarketplaces` | 4 repos | the three domain repos + this hub aggregator |
| `enabledPlugins` | 9 plugins | all of Riley's skills, on by default |

## Where it goes

Claude Code reads settings from, in increasing precedence:

- **User** — `~/.claude/settings.json` (this baseline's home; applies everywhere)
- **Project** — `.claude/settings.json` (checked in; per-repo)
- **Local** — `.claude/settings.local.json` (git-ignored; personal overrides)

To adopt the baseline on a machine:

```bash
mkdir -p ~/.claude
cp config/settings.baseline.json ~/.claude/settings.json
# then, in Claude Code, let it fetch the marketplaces:
#   /plugin marketplace update
```

Or just ask Claude: *"apply my settings baseline from config/settings.baseline.json."*

## Triggering skills without asking

Two things make a skill fire on its own, and both are covered:

1. **`permissions.allow: ["Skill"]`** (above) lets Claude invoke a matched skill
   without stopping to ask.
2. **A sharp `description`** on each skill decides *whether* it matches. This is
   the real lever — a skill with a vague description never fires. The
   `publish-skill-to-github` skill validates descriptions on the way in (they
   must say both what the skill does *and* when to trigger, including casual
   phrasings), which is why the library triggers reliably.

## What is **not** backed up here (on purpose)

- **Secrets** — tokens, API keys, connector credentials. Those never belong in a
  public repo. The baseline contains none; keep it that way.
- **CCR cloud-session scaffolding** — the `session-start-git-identity.sh`,
  `stop-hook-*.py`, and `launcher-settings.json` that appear under `~/.claude`
  in a Claude-Code-on-the-web container are injected by the remote runtime, not
  authored by Riley. They are Anthropic's plumbing and are intentionally left
  out; restoring them onto a local machine would do nothing useful.
- **Machine-local overrides** — anything you'd put in `settings.local.json`.
