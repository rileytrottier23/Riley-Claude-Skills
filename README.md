# Riley Claude Skills

> **This library has moved.** It was one repo; it's now three, split by domain. This page is an index —
> the skills themselves live in the repos below. Nothing installs from here anymore.

Each skill is a folder containing a `SKILL.md`: an instruction set Claude loads when its description
matches what you're asking for. They work in Claude Projects, Claude Code, and Cowork. Every repo below is
also a plugin marketplace, so you can install a whole domain in one step and `git pull` picks up updates.

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

Pick the domain you want:

```
/plugin marketplace add rileytrottier23/riley-pm-skills
/plugin marketplace add rileytrottier23/riley-coding-skills
/plugin marketplace add rileytrottier23/riley-thinking-skills
```

Then `/plugin install <plugin>@<marketplace>` — see each repo's README for its plugin list. In the Claude
desktop app / Cowork: Customize → Plugins → Personal plugins → **+** → Add marketplace → Add from a
repository.

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
