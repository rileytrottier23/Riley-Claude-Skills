# Riley Claude Skills

My Claude skills, split into three repos by domain. This repo is the hub: add its marketplace once and you
get all three, plus a small plugin that backs up my Claude Code settings. See
[Control plane](#control-plane-keep-the-whole-setup-in-git).

Each skill is a folder containing a `SKILL.md`: an instruction set Claude loads when its description
matches what you're asking for. They work in Claude Projects, Claude Code, and Cowork. Each repo below is
also a standalone plugin marketplace, so you can install a whole domain on its own and `git pull` picks up
updates.

**Looking for a skill?** See the [Skills Cheat Sheet](./SKILLS.md): every skill in one table, grouped by
what you're trying to do, with its kind and the phrases that trigger it.

## The three repos

| Repo | What's in it | Skills |
|---|---|---|
| [**riley-pm-skills**](https://github.com/rileytrottier23/riley-pm-skills) | Product & PM: PRDs and specs, stakeholder decks, competitive research, plus vendored PM collections (Dean Peters, Gene Dai) | 16 |
| [**riley-coding-skills**](https://github.com/rileytrottier23/riley-coding-skills) | Coding & engineering: TDD, debugging, planning, code review, git worktrees (superpowers), MCP building, frontend/webapp tooling, anti-slop filters | 27 |
| [**riley-thinking-skills**](https://github.com/rileytrottier23/riley-thinking-skills) | Everything else: decision/reflection/practice partners, personal-life modelling, writing & comms, AI-writing cleanup, pre-ship checks, integration debugging, creative/design, and the skill-publishing tool | 22 |

Each repo splits its skills into **`mine/`** (my own work, MIT) and **`vendored/`** (other people's,
pinned to an upstream commit under their original license), so "who wrote this and under what license" is
answerable at a glance.

## Install

**Everything, from this hub** (one marketplace, all 13 plugins: the domain plugins sourced from the three
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

Then `/plugin install <plugin>@<marketplace>`. See each repo's README for its plugin list. In the Claude
desktop app / Cowork: Customize → Plugins → Personal plugins → **+** → Add marketplace → Add from a
repository. Already have the `riley-claude-skills` marketplace from before? Run
`/plugin marketplace update riley-claude-skills` (or refresh in the app) and it now serves the three repos.

## Control plane: keep the whole setup in git

Skills are only part of the setup. Two other things live only in the Claude account and vanish if it's
lost: **routines** (scheduled triggers) and **Claude Code settings** (marketplaces, enabled plugins,
preferences). Settings are versioned here. Routines are backed up to a private repo, because their
prompts describe which personal sources Claude reads.

| Folder | Holds | Backed up / restored by |
|---|---|---|
| [`config/`](./config) | A portable, secret-free `settings.json` baseline | `backup-claude-setup` skill |
| `scripts/` | Settings sync helpers | — |

Each of these skills does one job when you say the phrase:

- **"push this skill"**: `publish-skill-to-github` routes a new or edited skill to the right domain repo
  (`riley-pm-skills` / `riley-coding-skills` / `riley-thinking-skills`), under `mine/` or `vendored/`, and
  updates that repo's README, marketplace, and changelog.
- **"back up my routines / settings"**: `backup-claude-setup` snapshots settings into this hub and
  routines into the private repo, and commits them. It also restores either one.
- **"remember this" / "don't make that mistake again"**: `self-improve` captures a lesson from the
  session and routes it. A universal preference goes to `~/.claude/CLAUDE.md` (mirrored here as
  `config/global-learnings.md` so it's diffable and revertible), a recurring domain pattern gets promoted
  into a real skill instead, and a project-specific fact stays in that project's own `CLAUDE.md`.
  It's scoped narrower than "dump everything into global memory" on purpose, because global memory loads
  into every session and skills don't.
- Everything is git, so `git pull` picks up updates and every change has a diff and a rollback.

### Why skills trigger without being asked for

A skill fires when Claude decides its `description` matches the request, with no menu or `/command`. Two
things make that reliable, and both are set up here: `permissions.allow: ["Skill"]` in the settings
baseline (so a matched skill runs without a permission prompt), and specific descriptions on
every skill (`publish-skill-to-github` checks this on the way in, since a skill with a vague description never
fires). See [`config/README.md`](./config/README.md).

## Why the split

One repo mixed PM, coding, and personal skills under a single marketplace. Splitting by domain lets each
audience install just what's relevant, keeps each README focused, and stops the library from becoming one
long list. The full pre-split history remains in this repo's git log.

## Why a skills library exists at all

A prompt you retype every week is a routine you haven't built yet. Everything I reuse goes the same way:
one-off prompt, then repeated workflow, then versioned skill, then skill with evals. Keeping skills in git
means I can see what changed when one starts behaving differently, and roll it back. Skills drift the same
way code does; most people just have no diff to look at.

## License

MIT, see [LICENSE](./LICENSE). Applies to my own skills only; vendored collections in each repo carry
their own license files, which govern.

## Related projects

- [journal-mcp-server](https://github.com/rileytrottier23/journal-mcp-server): a remote MCP server with
  OAuth 2.0, pulled out of my ReflectAI journaling app.
