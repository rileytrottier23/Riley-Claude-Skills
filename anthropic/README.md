# Anthropic example skills

Vendored from [anthropics/skills](https://github.com/anthropics/skills) at commit
[`f379e5a`](https://github.com/anthropics/skills/tree/f379e5ad66e2febc1616cf8d6284666fecbe514e),
synced 2026-08-18.

These are not mine. They live here so the versions I am actually running are pinned and diffable
alongside the rest of this repo — same reason everything else here is in git. Upstream moves; when
it does, this folder gets a sync commit rather than a silent drift.

Unlike the skills at the root of this repo, each of these is a **folder** — `SKILL.md` plus scripts,
references, and assets. Copy the whole directory, not just the markdown file.

## What is here

| Skill | What it does |
|---|---|
| [algorithmic-art](./algorithmic-art) | Generative art with p5.js — seeded randomness, flow fields, particle systems, interactive parameter exploration. |
| [brand-guidelines](./brand-guidelines) | Applies Anthropic's brand colors and typography to artifacts. A useful template to fork for a Workday-styled equivalent. |
| [claude-academy-guide](./claude-academy-guide) | Surfaces matching Claude Academy courses and tutorials when someone asks how to do something in Claude. |
| [claude-api](./claude-api) | Reference for the Claude API and SDKs — model ids, pricing, streaming, tool use, MCP, caching, migration. |
| [discernment-nudge](./discernment-nudge) | Appends targeted follow-up questions after substantive answers so the reader pressure-tests the output instead of accepting it. |
| [doc-coauthoring](./doc-coauthoring) | Structured workflow for co-authoring docs, proposals, and specs — context transfer, iteration, reader verification. |
| [frontend-design](./frontend-design) | Aesthetic direction for new UI — typography and visual choices that avoid reading as templated defaults. |
| [internal-comms](./internal-comms) | Status reports, leadership updates, newsletters, FAQs, incident reports, in house formats. |
| [mcp-builder](./mcp-builder) | Building MCP servers in Python (FastMCP) or Node/TypeScript, with tool design guidance. |
| [slack-gif-creator](./slack-gif-creator) | Animated GIFs sized and validated against Slack's constraints. |
| [theme-factory](./theme-factory) | Ten preset themes plus on-the-fly theme generation for slides, docs, reports, and landing pages. |
| [web-artifacts-builder](./web-artifacts-builder) | Multi-component HTML artifacts with React, Tailwind, and shadcn/ui — for artifacts needing state or routing. |
| [webapp-testing](./webapp-testing) | Playwright-driven testing of local web apps — frontend verification, screenshots, browser logs. |

## Deliberately not vendored

`docx`, `pdf`, `pptx`, and `xlsx` are source-available rather than open source, and Claude already
loads its own copies. `skill-creator` is likewise already available in Claude Code and Cowork.
Pulling any of them in here would shadow a maintained version with a stale one.

`canvas-design` is skipped for size: it bundles ~5.5 MB of fonts, which would have been roughly
three quarters of this folder. Pull it from upstream directly if a poster or static-art task ever
calls for it.

## Licensing

The rest of this repository is MIT. **This folder is not.** Everything under `anthropic/` is
licensed Apache 2.0 by Anthropic, PBC, and each skill keeps its own `LICENSE.txt` — do not strip
them. Upstream ships a `doc-coauthoring` folder with no license file; treat it as Apache 2.0 like
its siblings, but confirm before redistributing it on its own.

Upstream's [`THIRD_PARTY_NOTICES.md`](https://github.com/anthropics/skills/blob/main/THIRD_PARTY_NOTICES.md)
covers dependencies bundled inside these skills and is not reproduced here.
