# Claude Code settings

A portable, **secret-free** baseline of Riley's Claude Code configuration, so a
fresh install (new machine, reset account, teammate copy) can be brought up to
the same setup in one file — every skills marketplace registered, every plugin
enabled, and the personal preferences that make the harness feel like Riley's.

## What's here

- **`settings.baseline.json`** — a complete `settings.json` you can drop in:
  registers all four skills marketplaces, enables the nine plugins, and sets the
  preferences below.
- **`mcp-servers.baseline.json`** — the `mcpServers` entries for Riley's personal-account MCP
  integrations (WhatsApp, Chess.com). See [MCP servers](#mcp-servers) below.
- **`global-learnings.md`** — a versioned mirror of the `## Learnings` section in
  `~/.claude/CLAUDE.md` (Riley's account-wide memory, loaded in every session everywhere).
  Kept and pruned by the `self-improve` skill under `control-plane/`. See that file for
  what belongs here versus in a promoted skill versus a project's own `CLAUDE.md`.

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

## MCP servers

Personal-account integrations that don't fit the plugin/skill system — these are live external
tools (one talks to a real WhatsApp account, the other to Chess.com's API), not prompts, so they're
wired in via Claude Code's MCP config instead of `/plugin install`.

| Server | Source | Auth | Notes |
|---|---|---|---|
| `chess` | [pab1it0/chess-mcp](https://github.com/pab1it0/chess-mcp) | None — Chess.com's public Published Data API | Runs via Docker, no local clone needed |
| `whatsapp` | [lharries/whatsapp-mcp](https://github.com/lharries/whatsapp-mcp) | One-time QR scan from your phone; session cached locally | Needs a companion Go bridge process kept running |

`mcp-servers.baseline.json` documents both entries. The WhatsApp paths are placeholders
(`{{PATH_TO_UV}}`, `{{PATH_TO_WHATSAPP_MCP_REPO}}`) since they're machine-specific, not secrets —
safe to commit as-is.

### Setup: chess (Docker only)

```bash
claude mcp add chess -s user -- docker run --rm -i pab1it0/chess-mcp
```

Requires Docker running locally. No account or config needed — it only reads Chess.com's public
player/game data.

### Setup: WhatsApp (needs a background bridge process)

1. Install prerequisites — Go and [uv](https://astral.sh/uv) — then clone the server:
   ```bash
   git clone https://github.com/lharries/whatsapp-mcp.git ~/mcp/whatsapp-mcp
   ```
2. Start the bridge and keep it running — it holds the WhatsApp Web session:
   ```bash
   cd ~/mcp/whatsapp-mcp/whatsapp-bridge
   go run main.go
   ```
   The first run shows a QR code — scan it with WhatsApp on your phone to link the device.
3. Register the MCP server (swap in your real `uv` path from `which uv`):
   ```bash
   claude mcp add whatsapp -s user -- $(which uv) --directory ~/mcp/whatsapp-mcp/whatsapp-mcp-server run main.py
   ```

Restart Claude Code after adding either server.

**Not backed up:** the WhatsApp bridge's local session store (a SQLite db under
`whatsapp-bridge/store/`) is your device-linked auth — never commit it, and it isn't tracked here.
Re-scanning the QR code on a new machine is the intended recovery path.

## Current account state vs. this baseline (2026-08-23)

The baseline above is the **intended** post-split target: Riley's own domain plugins
(`riley-pm-skills`, `riley-coding-skills`, `riley-thinking-skills`) plus their vendored
collections and `riley-control-plane`. A live check of the account found it still on the
**pre-split** configuration, so restore-vs-reality is not yet the same thing:

| | Live account | This baseline (target) |
|---|---|---|
| PM | `riley-pm-skills`, `pm-skills-deanpeters`, `pm-skills-digidai` ✓ | same ✓ |
| Thinking | **old `riley-personal-skills`** (pre-split bundle) | `riley-thinking-skills` + `anthropic-example-skills` + `writing-skills-obra` |
| Coding | **none enabled** | `superpowers`, `anthropic-coding-skills` |
| Control plane | none | `riley-control-plane` |

Practical effect: the coding skills and the newer thinking skills
(`decision-partner`, `decision-review`, `practice-partner`, `reflection-partner`) are
**not loaded in the account** and won't trigger until the plugins are enabled. To migrate,
add the two missing marketplaces and install their plugins (see each repo's README for the
exact `/plugin install` lines), then remove the old `riley-personal-skills`.

**Anthropic Cowork plugins** (`pdf-viewer`, `design`, `product-management`, `productivity`,
`finance`, `data`, `cowork-plugin-management`) are also enabled in the account. Those come
from Anthropic's built-in Cowork marketplace, not Riley's repos, and are managed there — so
they're intentionally *not* in this baseline, which scopes to Riley's own skills.

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
