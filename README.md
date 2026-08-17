# Riley Claude Skills

The Claude skills I actually use for product work — versioned here rather than left in a chat history.

Each file is a `SKILL.md`: an instruction set Claude loads when the skill's description matches what you are asking for. They are written for [Claude Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) and work in Claude Projects, Claude Code, and Cowork.

## Why this repo exists

A prompt you retype every week is a routine you have not built yet. I run everything I reuse through the same progression:

```
one-off prompt -> repeated workflow -> versioned skill -> skill with evals -> shared standard
```

These are the ones that made it to stage three. Keeping them in git means I can see exactly what changed when a skill starts behaving differently — and roll back to the version that worked. Skills drift the same way code does; the difference is that most people have no diff to look at.

## PM skills

| Skill | What it does |
|---|---|
| [prd-spec-writer](./prd-spec-writer.md) | Writes PRDs, product specs, feature briefs, and technical design docs — problem framing, success metrics, requirements, open questions. Tuned for agentic AI infrastructure work. |
| [stakeholder-deck-builder](./stakeholder-deck-builder.md) | Builds executive and stakeholder decks: narrative arc, exec-ready framing, data-backed storytelling. Outputs slide outlines or full .pptx files. |
| [competitive-research-report](./competitive-research-report.md) | Produces structured competitive analysis, market research, and technology landscape reports for senior PM and exec audiences. |

## Personal skills

Kept in [`personal/`](./personal) — useful as examples of how much context a skill can carry, but written for my situation specifically. Fork and strip.

| Skill | What it does |
|---|---|
| [canadian-financial-modeler](./personal/canadian-financial-modeler.md) | Canada-specific personal finance modelling — mortgages, TFSA/RRSP/RESP/FHSA, RSU tax treatment, HEMOC math, rental property analysis. |
| [chess-coach](./personal/chess-coach.md) | Practical chess coaching for the 700–1200 Elo range — tactics, openings, endgames, game analysis. |
| [french-tutor](./personal/french-tutor.md) | French practice with an emphasis on Quebec French, for an anglophone parent in a bilingual household. |

## Using them

1. Copy the contents of the skill file you want.
2. Add it as a Skill in your Claude Project, or drop it in your `skills/` directory for Claude Code.
3. Claude triggers it automatically based on the description in its frontmatter — you do not need to invoke it by name.

## A note on writing your own

The description in the frontmatter does more work than the body. It is the only part Claude sees when deciding whether to load the skill, so it needs to name the situations that should trigger it — including the casual phrasings. A skill with a perfect body and a vague description never fires.

## License

MIT — see [LICENSE](./LICENSE).
## Related projects

- [journal-mcp-server](https://github.com/rileytrottier23/journal-mcp-server) — a reference MCP server implementation demonstrating agent tool and permissioning design, extracted from a personal journaling app.
