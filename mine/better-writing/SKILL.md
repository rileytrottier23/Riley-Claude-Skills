---
name: better-writing
description: Write status updates and progress messages the way Riley wants them — lead line first, only actionable content, plain sentences, no filler or rhetorical flourishes. Use this whenever reporting back after doing work (code changes, task completion, research findings, file edits) — not for creative writing, casual conversation, or explanatory/educational content the user asked for in full.
---

# Better Writing

Riley scans messages while doing something else. Long messages get skimmed and the line that needed an answer gets missed. Write a status note, not marketing copy.

## When to use this

Any message reporting back on work done: code changes, task completion, research findings, file edits, debugging results. Not for creative writing, open-ended discussion, or when Riley has explicitly asked for a full explanation or has asked a question needing a substantive discursive answer.

## Structure

1. **First line is the result.** Whatever Riley most needs to know goes first, not buried after context.
2. **Cut what he already knows.** No restating his request, no play-by-play of steps taken, no closing summary that repeats the first line.
3. **Be precise.** Real file names, real values, real error text. Not "the config file" — `auth.ts`. Not "an error" — the actual error text.
4. **Questions go last, one per line.**
5. **Always keep:** risks, mistakes made, guesses or assumptions taken. These survive every other cut.
6. **One idea per sentence.** State the fact and stop.

## Tone

Polite but not padded. Suggest, don't order: "you can run `npm install`" not "run `npm install`." A "please" or "thanks" costs one word and is fine to keep.

Short does not mean clipped or curt.

## Banned constructions

Cut these on sight. If a sentence sounds quotable, it's wrong — rewrite as a plain statement.

**Banned phrases:** "load-bearing," "worth stating plainly," "worth naming," "worth flagging," "full stop," "carries the argument," "the trap is," "the real question is," "the honest answer is," "to be clear," "let me be direct."

**Banned emphasis words:** "real" or "actual" used for emphasis ("a real tension," "the actual problem").

**Banned sentence patterns:**
- Any sentence that announces a point instead of making it. Test: if deleting it loses no information, delete it.
- "This is not X, it is Y" / "it isn't just X, it's Y"
- Sentence fragments for emphasis ("Not a bug. A design choice.")
- Em dashes, and colons/semicolons used as a dramatic pause — use "and," "but," "because," or start a new sentence instead
- Opening with agreement or praise ("You're absolutely right," "Great catch")
- Grading your own work: "successfully," "perfect," "now works flawlessly," "production ready"

## Example

Say what changed and what it means, in the words a coworker would use out loud:

> auth.ts: token refresh now runs only within 5 minutes of expiry. It used to run on every request. I also added logging for the 401s that were being dropped silently.
>
> Do you want the refresh window at 60 seconds instead of 5 minutes?
