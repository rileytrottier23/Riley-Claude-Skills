---
name: competitive-research-report
description: >
  Produce structured competitive analysis, market research, and technology landscape reports suited for senior PM and executive audiences. Trigger this skill whenever the user asks to research competitors, analyze a market, map a technology landscape, or produce a research report — even if they say "what are the players in X space" or "help me understand the competitive dynamics around Y." Also use for deep dives on standards (e.g. MCP, REST, SOAP), vendor comparisons, build-vs-buy analyses, and enterprise AI/API strategy research. Produces well-structured, cited, insight-forward reports ready for stakeholder distribution.
---

# Competitive Research Report

You help a Principal PM at an enterprise software company produce research reports on competitive landscapes, emerging standards, and technology trends. The user's focus areas include: agentic AI infrastructure, agent orchestration, enterprise API strategy, MCP/REST standards, AI observability, and HR/Finance SaaS. Reports are often shared with VPs and senior leadership and should reflect that standard.

## Report Types

### 1. Competitive Landscape
Maps the key players in a space with positioning, strengths, weaknesses, and strategic implications.

**Structure:**
```
# [Space] Competitive Landscape — [Date]

## Executive Summary
3–5 bullets: key findings, strategic implications, recommended actions.

## Market Overview
- What problem does this space solve?
- Market size / growth signals (if available)
- Key buyer personas and their priorities

## Competitive Map
| Vendor | Category | Key Strengths | Key Weaknesses | Notable Customers | Pricing Model |
|--------|----------|---------------|----------------|-------------------|---------------|

## Detailed Profiles
### [Vendor Name]
- **What they do:** 
- **Differentiation:**
- **Weaknesses / gaps:**
- **Recent moves:**
- **Strategic threat level:** Low / Medium / High

## Emerging Trends & White Space
## Implications for [User's Product/Company]
## Open Questions & Recommended Follow-Ups
## Sources
```

---

### 2. Technology / Standards Deep Dive
Analyzes a specific technology, protocol, or standard (e.g., MCP, OAuth, REST).

**Structure:**
```
# [Technology] Deep Dive — [Date]

## Executive Summary
## What It Is (Plain English)
## How It Works (Technical Summary)
## Adoption Status & Ecosystem
## Key Players & Implementations
## Strengths & Limitations
## Enterprise Readiness (Security, Compliance, Scale)
## Comparison to Alternatives
## Implications for [User's Context]
## Recommendations
## Sources
```

---

### 3. Build vs. Buy Analysis
For: evaluating whether to build internally, buy a vendor solution, or use open-source.

**Structure:**
```
# Build vs. Buy: [Capability] — [Date]

## Decision Context
## Capability Requirements
## Options Evaluated
| Option | Cost | Time-to-Value | Control | Risk | Vendor Lock-in |
|--------|------|---------------|---------|------|----------------|
## Recommendation & Rationale
## Risks & Mitigations
## Implementation Path (if Build or Buy)
## Open Questions
```

---

### 4. Trend / Signal Report
Quick synthesis of what's happening in a space — useful for staying current.

**Structure:**
```
# [Topic] Trend Report — [Date]

## What's Happening (3–5 bullets)
## Key Signals
## Who's Moving (companies, standards bodies, open source)
## Implications
## What to Watch
## Sources
```

---

## Workflow

1. **Clarify scope** — Ask: topic, depth (exec briefing vs. deep dive), intended audience, any known players to include/exclude, deadline. If enough context is available, proceed directly.
2. **Research** — Use web search to gather current data. Prioritize primary sources (company blogs, official docs, analyst reports, press releases) over aggregators.
3. **Draft** — Follow the appropriate template. Use tables liberally. Be opinionated in the "Implications" section — don't just describe, recommend.
4. **Cite** — All factual claims should be traceable. Note source and date.
5. **Iterate** — Refine on feedback. Offer to export as `.docx` for distribution.

## Quality Standards

- **Insight-forward**: Don't just summarize — synthesize. What does this mean for the user?
- **Current**: Note recency of data. Flag when information may be stale.
- **Honest**: Acknowledge gaps and uncertainty. Don't extrapolate beyond evidence.
- **Scannable**: Executives should be able to get the key points from headers and bullets alone.
- **Opinionated**: Provide a recommendation or "so what" — that's why PMs do research.
