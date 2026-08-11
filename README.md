# Riley Claude Skills

A collection of custom [Claude Skills](https://docs.claude.com) I use day-to-day for product management, personal finance, and learning. Each file below is a `SKILL.md` — the instruction set Claude loads when the skill is triggered.

## Skills

| Skill | What it does |
|---|---|
| [`prd-spec-writer.md`](./prd-spec-writer.md) | Writes PRDs, product specs, feature briefs, and technical design docs with clear problem framing, success metrics, and requirements. Tuned for agentic AI infrastructure work. |
| [`stakeholder-deck-builder.md`](./stakeholder-deck-builder.md) | Builds executive and stakeholder presentation decks — narrative arc, exec-ready framing, data-backed storytelling. Outputs slide outlines or full `.pptx` files. |
| [`competitive-research-report.md`](./competitive-research-report.md) | Produces structured competitive analysis, market research, and technology landscape reports for senior PM/exec audiences. |
| [`canadian-financial-modeler.md`](./canadian-financial-modeler.md) | Builds financial models and answers Canada-specific personal finance questions — mortgages, TFSA/RRSP/RESP/FHSA, RSU tax treatment, HELOC math, rental property analysis. |
| [`chess-coach.md`](./chess-coach.md) | Practical chess coaching for a ~700 Elo player targeting 1000 Elo — tactics, openings, endgames, and game analysis. |
| [`french-tutor.md`](./french-tutor.md) | French language practice and instruction, with an emphasis on Quebec French, for an anglophone parent learning French to support a bilingual household. |

## Usage

These are designed for [Claude Projects / Claude Skills](https://docs.claude.com). To use one:

1. Copy the contents of the relevant `.md` file
2. Add it as a Skill in your Claude Project (or reference it directly in a conversation)
3. Claude will automatically trigger the skill based on the `description` in its frontmatter

## Note

Some of these skills contain personal context (career, family, location) used to tailor Claude's responses. Feel free to fork and strip that out for your own use.

---
*Backed up from Claude on August 10, 2026.*
