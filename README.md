# Riley Claude Skills

The Claude skills I actually use for product work — versioned here rather than left in a chat history.

Each skill is a folder containing a `SKILL.md`: an instruction set Claude loads when the skill's description matches what you are asking for. They are written for [Claude Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) and work in Claude Projects, Claude Code, and Cowork.

**This repo is also a plugin marketplace** — 48 skills installable in one step. See [Install](#install) below.

## Install

Add this repo as a plugin marketplace and the skills install themselves — no copying files, and `git pull` picks up updates.

**Claude desktop app / Cowork:** Customize → Plugins → Personal plugins → **+** → Add marketplace → Add from a repository → `rileytrottier23/Riley-Claude-Skills`

**Claude Code:**

```
/plugin marketplace add rileytrottier23/Riley-Claude-Skills
/plugin install riley-pm-skills@riley-claude-skills
```

Seven plugins, install whichever you want:

| Plugin | Skills | What's in it |
|---|---|---|
| `riley-pm-skills` | 3 | My PM skills — PRDs, stakeholder decks, competitive research |
| `riley-personal-skills` | 4 | Canadian personal finance, chess coaching, French tutoring, skill publishing |
| `anthropic-example-skills` | 13 | Anthropic's example skills (Apache 2.0) |
| `pm-skills-deanpeters` | 12 | Dean Peters' PM skills (CC BY-NC-SA 4.0) |
| `pm-skills-digidai` | 1 | Gene Dai's PM skill pack (CC BY-NC-SA 4.0) |
| `writing-skills-obra` | 1 | Strunk's Elements of Style, packaged by Jesse Vincent (public domain) |
| `superpowers` | 14 | Jesse Vincent's coding-agent methodology — TDD, debugging, planning, code review, git worktrees (MIT) |

Plugin skills are namespaced, so an installed skill is invoked as `/pm-skills-deanpeters:pol-probe` if you want to call one by name. Mostly you won't — Claude triggers them from their descriptions.

## Why this repo exists

A prompt you retype every week is a routine you have not built yet. I run everything I reuse through the same progression:

```
one-off prompt -> repeated workflow -> versioned skill -> skill with evals -> shared standard
```

These are the ones that made it to stage three. Keeping them in git means I can see exactly what changed when a skill starts behaving differently — and roll back to the version that worked. Skills drift the same way code does; the difference is that most people have no diff to look at.

## PM skills

| Skill | What it does |
|---|---|
| [prd-spec-writer](./pm/prd-spec-writer) | Writes PRDs, product specs, feature briefs, and technical design docs — problem framing, success metrics, requirements, open questions. Tuned for agentic AI infrastructure work. |
| [stakeholder-deck-builder](./pm/stakeholder-deck-builder) | Builds executive and stakeholder decks: narrative arc, exec-ready framing, data-backed storytelling. Outputs slide outlines or full .pptx files. |
| [competitive-research-report](./pm/competitive-research-report) | Produces structured competitive analysis, market research, and technology landscape reports for senior PM and exec audiences. |

## Personal skills

Kept in [`personal/`](./personal) — useful as examples of how much context a skill can carry, but written for my situation specifically. Fork and strip.

| Skill | What it does |
|---|---|
| [canadian-financial-modeler](./personal/canadian-financial-modeler) | Canada-specific personal finance modelling — mortgages, TFSA/RRSP/RESP/FHSA, RSU tax treatment, HEMOC math, rental property analysis. |
| [chess-coach](./personal/chess-coach) | Practical chess coaching for the 700–1200 Elo range — tactics, openings, endgames, game analysis. |
| [french-tutor](./personal/french-tutor) | French practice with an emphasis on Quebec French, for an anglophone parent in a bilingual household. |
| [publish-skill-to-github](./personal/publish-skill-to-github) | Pushes any new or edited skill to this repo, updates the README counts and tables, bumps the marketplace version, and logs a changelog line. |

## Vendored: Anthropic example skills

[`anthropic/`](./anthropic) holds 13 skills pulled from [anthropics/skills](https://github.com/anthropics/skills), pinned to a commit so I can diff them when upstream moves. They are folders rather than single files — `SKILL.md` plus scripts and assets — so copy the whole directory. They are Apache 2.0, not MIT; see [`anthropic/README.md`](./anthropic/README.md).

## Third-party skills

[`third-party/`](./third-party) holds skills by other people, vendored so they are pinned and available without hunting for the source. Every folder credits its author, keeps its original licence, and records the upstream commit.

| Collection | Author | Skills | License |
|---|---|---|---|
| [deanpeters-product-manager-skills](./third-party/deanpeters-product-manager-skills) | Dean Peters (Productside) | 12 | CC BY-NC-SA 4.0 |
| [digidai-product-manager-skills](./third-party/digidai-product-manager-skills) | Gene Dai | 1 (large) | CC BY-NC-SA 4.0 |
| [obra-elements-of-style](./third-party/obra-elements-of-style) | Jesse Vincent | 1 | Public domain |
| [obra-superpowers](./third-party/obra-superpowers) | Jesse Vincent | 14 | MIT |

The two PM collections are NonCommercial — that restricts how you *use* them, not this repo hosting them. The Elements of Style folder (public domain) and superpowers (MIT) carry no such restriction. See [`third-party/README.md`](./third-party/README.md).

## Using them without the marketplace

If you would rather not add a marketplace, every skill is still a plain folder. Copy the whole directory into your `skills/` directory for Claude Code, or zip it and upload it under Customize → Skills. Claude triggers it from the description in its frontmatter — you do not need to invoke it by name.

## A note on writing your own

The description in the frontmatter does more work than the body. It is the only part Claude sees when deciding whether to load the skill, so it needs to name the situations that should trigger it — including the casual phrasings. A skill with a perfect body and a vague description never fires.

## License

MIT — see [LICENSE](./LICENSE). Applies to my own skills only. [`anthropic/`](./anthropic) is Apache 2.0 and [`third-party/`](./third-party) is CC BY-NC-SA 4.0; both carry their own license files, which govern.

## Related projects

- [journal-mcp-server](https://github.com/rileytrottier23/journal-mcp-server) — a reference MCP server implementation demonstrating agent tool and permissioning design, extracted from a personal journaling app.
