# Skills Cheat Sheet

Every skill across the hub and the three domain repos, plus the ones that live only in the Claude
account. Pick a skill by what you're trying to do. You never have to name a skill: say something like the
phrase in the last column and Claude loads the matching one.

## Six kinds of skills

| Kind | What happens when it fires | Examples |
|---|---|---|
| 🛠️ **Makes it** | Produces the deliverable itself: a PRD, a deck, a report, a spec, an artifact | `prd-spec-writer`, `stakeholder-deck-builder`, `competitive-research-report`, `fdd-writer` |
| 🧭 **Guides it** | Walks you through a process step by step and drafts the pieces along the way | `discovery-process`, `roadmap-planning`, `writing-plans`, `test-driven-development` |
| 🔍 **Checks it** | Reviews something that already exists and reports gaps, risks, or slop | `checker-agent`, `avoid-ai-writing`, `requesting-code-review`, `antislop` |
| 🤔 **Questions you** | Asks you the hard questions instead of giving an answer | `decision-partner`, `decision-review`, `reflection-partner`, `practice-partner` |
| 🎓 **Coaches you** | Teaches a skill over time and adapts to your level | `chess-coach`, `french-tutor`, `canadian-financial-modeler` |
| ⚙️ **Runs the setup** | Maintains the skills library, settings, routines, and memory | `publish-skill-to-github`, `backup-claude-setup`, `self-improve`, `riley-context` |

**Where each skill lives:** **Hub** = this repo · **PM** = [riley-pm-skills](https://github.com/rileytrottier23/riley-pm-skills) · **Coding** = [riley-coding-skills](https://github.com/rileytrottier23/riley-coding-skills) · **Thinking** = [riley-thinking-skills](https://github.com/rileytrottier23/riley-thinking-skills) · **Account** = in the Claude account only, not yet in any repo. A † after the name marks a vendored skill (someone else's work, pinned upstream).

---

## 🚀 Quick Reference

| What you're doing | Use this skill | Kind | Say something like... |
|---|---|---|---|
| **Product docs & specs** | | | |
| Write a PRD, spec, feature brief, or one-pager | `prd-spec-writer` · PM | 🛠️ Makes it | "Help me write up this feature" · "Spec out this idea" |
| Write or revise a Workday FDD or PRD section in house style | `fdd-writer` · Account | 🛠️ Makes it | "Write the FDD" · "Draft the Develop section" · "Create a Topic 101" |
| Turn a standalone business rule into a decision table and Given/When/Then criteria | `deterministic-logic-spec` · Account | 🛠️ Makes it | "Spec this rule" · "Decision table for X" · "Edge cases for this rule" |
| Write user stories with Gherkin acceptance criteria | `user-story`† · PM | 🛠️ Makes it | "Write a user story for…" · "Convert this requirement into a story" |
| Co-author a doc, proposal, or decision doc in structured rounds | `doc-coauthoring`† · Thinking | 🧭 Guides it | "Help me write a proposal" · "Let's draft this spec together" |
| **Strategy & planning** | | | |
| Run a full strategy arc: positioning, discovery, roadmap | `product-strategy-session`† · PM | 🧭 Guides it | "We have a backlog but no direction" · "Run a strategy session" |
| Build a roadmap from competing initiatives | `roadmap-planning`† · PM | 🧭 Guides it | "Build a Q2 roadmap exec will approve" · "Sequence work across 3 teams" |
| Pick a prioritization framework (RICE, ICE, value/effort) | `prioritization-advisor`† · PM | 🧭 Guides it | "Which prioritization framework should we use?" · "RICE or value/effort?" |
| Decide whether an AI product idea deserves investment | `recommendation-canvas`† · PM | 🧭 Guides it | "Is this AI feature worth building?" · "Compare these AI options" |
| Assess whether your team is AI-first or AI-shaped | `ai-shaped-readiness-advisor`† · PM | 🧭 Guides it | "How AI-mature is my team?" · "Which AI capability do we build next?" |
| Diagnose SaaS metrics, critique a PRD, plan PLG growth, PM career moves | `product-manager-skills`† · PM | 🧭 Guides it | "Critique this PRD" · "Why is our NRR dropping?" · "PLG strategy for…" |
| **Discovery & validation** | | | |
| Run a discovery cycle from hypothesis to validated solution | `discovery-process`† · PM | 🧭 Guides it | "Validate this before we build" · "Activation dropped — find out why" |
| Uncover customer jobs, pains, and gains | `jobs-to-be-done`† · PM | 🧭 Guides it | "What job are customers hiring us for?" · "JTBD for this segment" |
| Pick the cheapest validation method for a risky idea | `pol-probe-advisor`† · PM | 🧭 Guides it | "Which PoL probe should I run?" · "How do I test demand cheaply?" |
| Define a disposable Proof of Life probe | `pol-probe`† · PM | 🛠️ Makes it | "Write a PoL probe for this pricing hypothesis" |
| **Research & comms** | | | |
| Competitive, market, or technology landscape report | `competitive-research-report` · PM | 🛠️ Makes it | "Who are the players in X?" · "Build vs. buy for…" · "Deep dive on MCP" |
| Research brief on one company (strategy, execs, org) | `company-research`† · PM | 🛠️ Makes it | "Brief me on Company X before the meeting" · "Prep me for this interview" |
| Build an exec deck, briefing, or QBR | `stakeholder-deck-builder` · PM | 🛠️ Makes it | "Put together slides for leadership" · "QBR deck for…" |
| Write a status report, leadership update, FAQ, or incident report | `internal-comms`† · Thinking | 🛠️ Makes it | "Write the weekly update" · "Draft the incident report" |
| **Writing quality** | | | |
| Tighten any prose with Strunk's rules | `writing-clearly-and-concisely`† · Thinking | 🔍 Checks it | "Make this clearer" · "Tighten this up" |
| Strip AI-isms from a draft | `avoid-ai-writing` · Account | 🔍 Checks it | "Make this sound less like AI" · "Audit this for AI tells" |
| Remove generic AI patterns from headlines, CTAs, and copy | `antislop-copywriting`† · Coding | 🔍 Checks it | "Rewrite this landing copy" · "This headline sounds generic" |
| **Review before shipping** | | | |
| Second pass on any artifact for gaps, errors, and risk | `checker-agent` · Account | 🔍 Checks it | "Check this" · "Is this ready to send?" · "What could go wrong?" |
| Add follow-up questions that help you verify an answer | `discernment-nudge`† · Thinking | 🔍 Checks it | *(fires on its own after substantive advice or drafts)* |
| **Decisions & reflection** | | | |
| Pressure-test a decision you're facing | `decision-partner` · Thinking | 🤔 Questions you | "Should I…?" · "I'm torn between…" · "Thinking about taking the offer" |
| Look back at a past decision: reasoning vs. luck | `decision-review` · Thinking | 🤔 Questions you | "That didn't work out" · "Was that the right call?" · "Quarterly decision review" |
| Weekly, monthly, or annual reflection | `reflection-partner` · Thinking | 🤔 Questions you | "Weekly review" · "I feel scattered" · "Am I working on the right things?" |
| Turn "I want to get better at X" into a practice plan | `practice-partner` · Thinking | 🤔 Questions you | "I've plateaued at…" · "I want to get better at presenting" |
| **Personal life** | | | |
| Canadian mortgages, TFSA/RRSP/FHSA, RSU tax, rental property | `canadian-financial-modeler` · Thinking | 🎓 Coaches you | "How much would I net on my RSUs?" · "Does this mortgage make sense?" |
| Improve at chess (700 → 1000+ Elo) | `chess-coach` · Thinking | 🎓 Coaches you | "Why did I lose this game?" · "Teach me an opening" |
| Practice Quebec French | `french-tutor` · Thinking | 🎓 Coaches you | "How do I say X in French?" · "Let's do some French practice" |
| **Creative & design** | | | |
| Generative art with p5.js | `algorithmic-art`† · Thinking | 🛠️ Makes it | "Make generative art" · "Flow field of…" |
| Animated GIF sized for Slack | `slack-gif-creator`† · Thinking | 🛠️ Makes it | "Make me a GIF of X for Slack" |
| Apply a preset or custom theme to slides, docs, or pages | `theme-factory`† · Thinking | 🛠️ Makes it | "Theme this deck" · "Give this a different look" |
| Apply Anthropic brand colors and type | `brand-guidelines`† · Thinking | 🛠️ Makes it | "Use Anthropic branding on this" |
| Find a Claude Academy course for a how-to question | `claude-academy-guide`† · Thinking | 🎓 Coaches you | "How do I use Claude Projects?" · "Getting started with Claude Code" |
| **Coding: plan & build** | | | |
| Explore intent and design before building anything | `brainstorming`† · Coding | 🧭 Guides it | "I want to add a feature that…" · "Let's build X" |
| Write an implementation plan from a spec | `writing-plans`† · Coding | 🧭 Guides it | "Plan this out before we code" |
| Execute a written plan with review checkpoints | `executing-plans`† · Coding | 🧭 Guides it | "Execute the plan in plan.md" |
| Execute a plan by handing tasks to subagents in this session | `subagent-driven-development`† · Coding | 🧭 Guides it | "Run the plan with subagents" |
| Split 2+ independent tasks across parallel agents | `dispatching-parallel-agents`† · Coding | 🧭 Guides it | "Do these three things in parallel" |
| Write the test first, then the code | `test-driven-development`† · Coding | 🧭 Guides it | "Fix this bug" · "Implement this function" |
| Work in an isolated git worktree | `using-git-worktrees`† · Coding | 🧭 Guides it | "Start this on a separate branch" |
| **Coding: debug, review & finish** | | | |
| Find the root cause before proposing a fix | `systematic-debugging`† · Coding | 🧭 Guides it | "This test is failing" · "Why is this broken?" |
| Figure out why an automation, sync, or token stopped working | `diagnose-broken-integration` · Account | 🧭 Guides it | "X stopped working" · "Why is the build failing?" · "Token expired" |
| Ask for a code review before merging | `requesting-code-review`† · Coding | 🔍 Checks it | "Review my changes" · "Ready to merge?" |
| Handle review feedback with verification, not blind agreement | `receiving-code-review`† · Coding | 🔍 Checks it | "Address these review comments" |
| Prove work passes before claiming it's done | `verification-before-completion`† · Coding | 🔍 Checks it | *(fires before any "done" or "fixed" claim)* |
| Decide how to integrate a finished branch (merge, PR, clean up) | `finishing-a-development-branch`† · Coding | 🧭 Guides it | "I'm done with this branch" · "Wrap this up" |
| **Coding: frontend & tooling** | | | |
| Distinctive visual design for new UI | `frontend-design`† · Coding | 🛠️ Makes it | "Design a landing page" · "This UI looks generic" |
| Multi-component React + Tailwind + shadcn artifact | `web-artifacts-builder`† · Coding | 🛠️ Makes it | "Build a dashboard artifact with routing" |
| Test a local web app with Playwright | `webapp-testing`† · Coding | 🔍 Checks it | "Test the login flow" · "Screenshot the page" |
| Build an MCP server | `mcp-builder`† · Coding | 🧭 Guides it | "Build an MCP server for the X API" |
| Claude API and SDK reference: models, pricing, tool use, caching | `claude-api`† · Coding | 🎓 Coaches you | "Which Claude model should I use?" · "Add prompt caching" |
| Core anti-slop rules for any AI-built UI, copy, or code | `antislop`† · Coding | 🔍 Checks it | *(loads with any antislop sub-skill)* |
| Anti-slop for color, layout, components, motion | `antislop-ui`† · Coding | 🔍 Checks it | "Build the settings page" · "Clean up this UI" |
| Anti-slop for layouts that reflow phone to desktop | `antislop-layoutmobile`† · Coding | 🔍 Checks it | "Make this work on mobile" · "Fix the overflow" |
| Contrast, keyboard, focus, and state accessibility | `antislop-human`† · Coding | 🔍 Checks it | "Check accessibility" · "Is this contrast OK?" |
| Remove generic AI comments without touching code | `antislop-code`† · Coding | 🔍 Checks it | "Clean up the comments in this file" |
| **Skills & setup** | | | |
| Load your Workday role, projects, and preferences | `riley-context` · Account | ⚙️ Runs the setup | "Load my context" · *(fires on Workday, Revenue Center, FDD topics)* |
| Publish a new or edited skill to the right repo | `publish-skill-to-github` · Thinking | ⚙️ Runs the setup | "Push this skill" · "Sync my skills" · "Update the skills README" |
| Back up or restore routines and settings | `backup-claude-setup` · Hub | ⚙️ Runs the setup | "Back up my Claude setup" · "Restore my routines" |
| Capture a lesson so Claude doesn't repeat a mistake | `self-improve` · Hub | ⚙️ Runs the setup | "Remember this" · "Don't make that mistake again" |
| Learn how to find and use skills (loads at conversation start) | `using-superpowers`† · Coding | ⚙️ Runs the setup | *(fires at the start of every conversation)* |
| Write or edit a skill and test that it works | `writing-skills`† · Coding | ⚙️ Runs the setup | "Create a skill for…" · "Why isn't this skill triggering?" |

---

## Housekeeping notes from this review

- **Six skills exist only in the Claude account**, with no copy in git: `riley-context`, `fdd-writer`,
  `deterministic-logic-spec`, `checker-agent`, `diagnose-broken-integration`, `avoid-ai-writing`. If the
  account lost them, nothing would restore them. Run `publish-skill-to-github` on each.
- **`riley-thinking-skills` `main` is missing `mine/` and `vendored/`.** Only the four partner skills
  (under `.claude/skills/`) are on `main`. The full 17-skill layout sits on the unmerged
  `claude/split-into-thinking-skills` branch, so the hub marketplace, which reads `main`, can't install
  `riley-thinking-skills` or `anthropic-example-skills` until that branch merges.
- **README counts are stale.** Coding now holds 25 skills (19 plus the six `antislop` skills added
  2026-09-13), not 19. Thinking holds 17 on its split branch, not 18.
- **The hub marketplace has no `antislop` entry.** `riley-coding-skills` lists it as its own plugin, but
  this repo's `marketplace.json` doesn't source it, so installing from the hub skips all six antislop skills.
