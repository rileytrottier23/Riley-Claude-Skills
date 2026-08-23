# The Elements of Style — Jesse Vincent

One skill from [obra/the-elements-of-style](https://github.com/obra/the-elements-of-style), packaged by
**Jesse Vincent**. Vendored at upstream `05fc4f0`, synced 2026-08-23.

Upstream ships the same skill for eleven agent harnesses along with per-harness install docs. Only the
skill itself is vendored here; grab the rest from source if you need another harness.

## License

**Public domain**, with one caveat worth stating plainly: upstream ships no `LICENSE` file. Its plugin
manifest declares `"license": "Public Domain"`, and the underlying text — William Strunk Jr.'s
*The Elements of Style*, 1918 — is public domain in the United States by age. What carries no explicit
license is Jesse Vincent's packaging: the `SKILL.md` wrapper that decides when the reference gets read.
Treated here as the public-domain declaration says. If that matters for your use, ask upstream.

This is the only folder in `third-party/` that is not Creative Commons.

## The skill

| Skill | What it does |
|---|---|
| [writing-clearly-and-concisely](./writing-clearly-and-concisely) | Applies Strunk's rules to any prose a human will read — docs, commit messages, error text, UI copy. Lists all 18 rules inline and opens the full 1918 reference only while writing or editing. |

`elements-of-style.md` is the complete 1918 text and costs roughly 12,000 tokens to read. The skill warns
about that and suggests handing a draft to a subagent when context is tight.
