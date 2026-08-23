# Riley Claude Skills

> **The library is now three repos, split by domain — but this repo still works as the combined hub.**
> Its `marketplace.json` is an *aggregator*: it sources the domain plugins from the three domain repos
> below (plus one hub-native control-plane plugin), so adding this one marketplace gets you everything.
> Prefer just one domain? Add that repo's marketplace directly instead.
>
> This hub is also the **control plane**: it backs up the parts of the setup that don't live in a skill
> repo — [routines](#control-plane-keep-the-whole-setup-in-git) (scheduled triggers) and
> [Claude Code settings](./config). See [Control plane](#control-plane-keep-the-whole-setup-in-git).

Each skill is a folder containing a `SKILL.md`: an instruction set Claude loads when its description
matches what you're asking for. They work in Claude Projects, Claude Code, and Cowork. Each repo below is
also a standalone plugin marketplace, so you can install a whole domain on its own and `git pull` picks up
updates.

## The three repos

| Repo | What's in it | Skills |
|---|---|---|
| [**riley-pm-skills**](https://github.com/rileytrottier23/riley-pm-skills) | Product & PM — PRDs and specs, stakeholder decks, competitive research, plus vendored PM collections (Dean Peters, Gene Dai) | 16 |
| [**riley-coding-skills**](https://github.com/rileytrottier23/riley-coding-skills) | Coding & engineering — TDD, debugging, planning, code review, git worktrees (superpowers), MCP building, frontend/webapp tooling | 19 |
| [**riley-thinking-skills**](https://github.com/rileytrottier23/riley-thinking-skills) | Everything else — decision/reflection/practice partners, personal-life modelling, writing & comms, creative/design, and the skill-publishing tool | 21 |

Each repo splits its skills into **`mine/`** (my own work, MIT) and **`vendored/`** (other people's,
pinned to an upstream commit under their original license), so "who wrote this and under what license" is
answerable at a glance.

## Install

**Everything, from this hub** (one marketplace, all 9 plugins — the domain plugins sourced from the three
repos, plus the hub's own `riley-control-plane`):

```
/plugin marketplace add rileytrottier23/Riley-Claude-Skills
/plugin install riley-pm-skills@riley-claude-skills
/plugin install riley-control-plane@riley-claude-skills
```

**Or just one domain,** straight from its own repo:

```
/plugin marketplace add rileytrottier23/riley-pm-skills
/plugin marketplace add rileytrottier23/riley-coding-skills
/plugin marketplace add rileytrottier23/riley-thinking-skills
```

Then `/plugin install <plugin>@<marketplace>` — see each repo's README for its plugin list. In the Claude
desktop app / Cowork: Customize → Plugins → Personal plugins → **+** → Add marketplace → Add from a
repository. Already have the `riley-claude-skills` marketplace from before? Just run
`/plugin marketplace update riley-claude-skills` (or refresh in the app) — it now serves the three repos.

## Control plane: keep the whole setup in git

Skills are only part of the setup. Two other things live only in the Claude account and vanish if it's
lost — **routines** (scheduled triggers) and **Claude Code settings** (marketplaces, enabled plugins,
preferences). This hub versions both, so the entire setup is expandable, recoverable, and portable.

| Folder | Holds | Backed up / restored by |
|---|---|---|
| [`routines/`](./routines) | Every scheduled trigger, as restore-ready JSON | `backup-claude-setup` skill → `list_triggers` → `scripts/format_routines.py` |
| [`config/`](./config) | A portable, secret-free `settings.json` baseline | `backup-claude-setup` skill |
| `scripts/` | The formatter that shapes `list_triggers` output into `routines/` | — |

Three skills, one motion each — say the phrase and it happens, no clicking through menus:

- **"push this skill"** → `publish-skill-to-github` routes a new/edited skill to the right domain repo
  (`riley-pm-skills` / `riley-coding-skills` / `riley-thinking-skills`), under `mine/` or `vendored/`, and
  updates that repo's README, marketplace, and changelog.
- **"back up my routines / settings"** → `backup-claude-setup` snapshots routines and settings into this
  hub and commits them. It also **restores**: "recreate the routine in `routines/<slug>.json`."
- Everything is **git**, so `git pull` picks up updates and every change has a diff and a rollback.

### Why skills trigger without being asked for

A skill fires when Claude decides its `description` matches the request — no menu, no `/command`. Two
things make that reliable, and both are set up here: `permissions.allow: ["Skill"]` in the settings
baseline (so a matched skill runs without a permission prompt), and sharp, trigger-rich descriptions on
every skill (`publish-skill-to-github` enforces this on the way in — a skill with a vague description never
fires). See [`config/README.md`](./config/README.md).

## Why the split

One repo mixed PM, coding, and personal skills under a single marketplace. Splitting by domain lets each
audience install just what's relevant, keeps each README focused, and stops the library from becoming one
long undifferentiated list. The full pre-split history remains in this repo's git log.

## Why a skills library exists at all

A prompt you retype every week is a routine you haven't built yet. Everything reused runs through the same
progression: one-off prompt → repeated workflow → versioned skill → skill with evals → shared standard.
Keeping skills in git means the change is visible when one starts behaving differently — and rollback is
possible. Skills drift the same way code does; most people just have no diff to look at.

## License

MIT — see [LICENSE](./LICENSE). Applies to my own skills only; vendored collections in each repo carry
their own license files, which govern.

## Related projects

- [journal-mcp-server](https://github.com/rileytrottier23/journal-mcp-server) — a reference MCP server
  implementation demonstrating agent tool and permissioning design, extracted from a personal journaling app.
