# Handoff: Make Claude's replies less text-heavy

**From:** Claude Code → **To:** Cowork
**Date:** 2026-09-29
**Why the switch:** The review of Claude Code replies is done. The next steps are reviewing Cowork chats and saving reply preferences, and both happen in the Claude app.

## Paste this to start
> I want Claude's replies to be less text-heavy. Claude Code already reviewed my coding sessions, and the findings are in this handoff file. Read the whole file before doing anything. Then do the tasks under "Tasks for Cowork", in order.

## Goal
Replies from Claude, in Cowork and in Code, should lead with the decision or my next action, stay short, and use tables, checklists or artifacts in place of long paragraphs.

## Context
- Full review: `code-output-review.md` in `rileytrottier23/Riley-Claude-Skills`, branch `claude/code-output-review-h831r7` (draft PR #12)
- Related skills I already have: `better-writing`, `writing-clearly-and-concisely`, `avoid-ai-writing`, `self-improve`

## Findings from the Code review (31 sessions)
- **Most common final reply:** a "your turn" handoff, where Claude was blocked on a manual step I had to do.
- **Hardest to read:**
  - The decision came last, in a notes section.
  - Commit hashes and IDs were mixed into sentences.
  - Handoffs said "see the prompt above", so I had to scroll back.
  - Recaps ran long.
- **What worked for me:**
  - Dashboards and other artifacts I kept coming back to.
  - Single tables.
  - One-line status summaries.
  - Numbered steps.

## Suggested defaults (not yet saved anywhere)
1. Start with the decision, or the one thing I need to do.
2. If I need to act, put the action in the reply itself, never "see above".
3. Put IDs, commands and paths in code blocks, not in sentences.
4. Keep a recap to 3 bullets or a table of 3 rows at most.
5. Use a checklist for work with 3 or more steps, and update it as the work goes.
6. If a reply is longer than one screen, offer an artifact instead.

## Tasks for Cowork
1. [ ] Review my last 2–4 weeks of Cowork chats the same way. For each chat, note the type of work and the shape of the final reply. Then note where replies were hard to read and where I pushed back on length.
2. [ ] Add a short "Cowork" section to the findings above. Don't repeat anything the Code review already covers.
3. [ ] Draft the defaults above as a short reply-style instruction I can paste into my Claude profile preferences. Show me the draft before saving anything.
4. [ ] Once I approve, add the defaults as one entry under `## Learnings` in `config/global-learnings.md` using the `self-improve` skill, so Code sessions pick them up too.

## Constraints
- Summaries only. No secrets, tokens, file contents, or anything work- or employer-specific.
- The skills repo is public, so treat anything written there as public.
- Keep every output to one page or less.

## How to verify
- The Cowork findings fit on one screen.
- The preference text is 6 lines or fewer, and I've approved it.

## Open questions for Riley
- Should the defaults go into profile preferences (applies everywhere), `global-learnings.md` (Code sessions), or both?

## Hand back when
Once I've approved a `global-learnings.md` entry, write a handoff back to Claude Code to commit it to PR #12.
