---
name: self-improve
description: Capture a durable lesson from this session — a mistake Riley corrected, a preference he stated, a non-obvious fact about a tool or workflow, or a technique that worked — and route it to the right place so Claude doesn't relearn it next time. Global truths go in Riley's account-wide `~/.claude/CLAUDE.md`; recurring domain patterns get promoted into a real skill (handed to `publish-skill-to-github` / skill-creator); one-off, project-specific facts are left alone. Use whenever Riley says "remember this," "don't make that mistake again," "note that for next time," "learn from this," or "add that to memory" — and proactively at the end of a session where Claude was corrected, guessed wrong about a preference, or found a non-obvious workaround worth keeping. Also covers the periodic tidy-up: "review my global learnings," "prune old learnings," "clean up my CLAUDE.md."
---

# Self-improve, globally

The blog-post version of this idea (a plugin that reflects at the end of a
session and appends lessons to a project's `CLAUDE.md`) is scoped to one repo
on purpose — project `CLAUDE.md` is loaded only in that project, so a bad
lesson stays contained. Riley wants the compounding to work **everywhere**,
which means picking a home for each lesson deliberately instead of dumping
everything in one growing file.

## The three destinations

| Lesson looks like | Goes to | Why there |
|---|---|---|
| A universal preference or habit ("prefer rebase over merge," "always confirm before force-push," "keep replies under 3 sentences unless asked") | Riley's **`~/.claude/CLAUDE.md`** (user memory — loaded in every session, every project) | It's true regardless of what he's working on |
| A pattern that has now shown up **2+ times** in a specific domain (a recurring coding fix, a PM-doc structure he keeps asking for) | A real **skill** — new (via `skill-creator`) or an edit to an existing one, then `publish-skill-to-github` | Skills load **on demand** by description match, so the lesson only enters context when it's actually relevant — no bloat on unrelated sessions |
| A fact true of *this* codebase/project only (a schema quirk, a local script name, a client's naming convention) | That project's own `CLAUDE.md` | It would be noise — or a leak — anywhere else |

**Default to the narrowest destination that fits.** Global memory is loaded
unconditionally into every single session regardless of relevance; every line
added there is a permanent tax on every future conversation, including ones
where it doesn't apply. A skill costs nothing when it doesn't match.

## Step 1 — classify before writing anything

Ask: would this be true and useful in a completely unrelated session (French
practice, a chess review, a client codebase)? If no, it is not global — it's
either a skill-domain pattern or project-local. Don't write it to
`~/.claude/CLAUDE.md` "just in case."

If unsure whether something has recurred before, check: `grep -ri "<topic>"
~/.claude/CLAUDE.md` and skim `config/global-learnings.md` in this repo (the
versioned mirror, see below) for a prior note on the same thing — don't add a
near-duplicate.

## Step 2 — write the global lesson

1. Append one short, dated bullet to `~/.claude/CLAUDE.md` under a `##
   Learnings` heading (create the heading if it doesn't exist):
   ```
   - 2026-09-12: Riley wants push confirmations even when a prior push was approved — approval doesn't carry across sessions.
   ```
   One line. No transcript excerpts, no code blocks, no names of clients or
   companies, no repo-specific detail — see **Never write** below.
2. If the file's `## Learnings` section is past ~40 lines, this is a prune
   pass, not just an append (see Step 4) — don't let it grow unbounded.
3. Mirror the same section into **`config/global-learnings.md`** in this hub
   repo, so it's versioned and diffable the same way `settings.baseline.json`
   is. Commit and push (see **Commit and push** below) — this is what makes a
   bad global lesson catchable and revertible instead of silently changing
   every future session forever.

**Never write:** secrets, tokens, client/company names, proprietary business
logic, anything from a confidential codebase, or a lesson that's only true
because of one project's setup. This repo is **public** — `config/` is
exactly as visible as `README.md`. When in doubt, leave it out of the global
file and put it in the project's own `CLAUDE.md` instead.

## Step 3 — promote a recurring pattern into a skill instead

If the same domain-specific correction has come up before, don't add a second
global bullet — hand it off:

- New pattern, no existing skill fits → `skill-creator` to scaffold one.
- An existing skill is just missing this case → edit its `SKILL.md` directly.
- Either way, finish with `publish-skill-to-github` so it lands in the right
  domain repo (`riley-pm-skills` / `riley-coding-skills` /
  `riley-thinking-skills`) and the README/changelog/marketplace update with
  it.

This is the actual "continuously self-improving" mechanism for anything
domain-shaped — it's versioned, it's reviewable in a diff, and it only loads
when relevant, which a global memory dump can't offer.

## Step 4 — periodic review (when asked, or if `## Learnings` is getting long)

1. Read `~/.claude/CLAUDE.md`'s `## Learnings` section.
2. Drop anything stale, superseded, or contradicted by a newer line.
3. Anything that's really a recurring domain pattern hiding in the global
   file → run Step 3 to promote it out, then delete the global bullet.
4. Flag contradictions out loud rather than silently picking one — e.g. a
   "be terse" lesson from coding work and a "be thorough" lesson from FDD
   writing are both correct in context; a global bullet that states either
   as a blanket rule is wrong and should be scoped or removed.
5. Re-sync `config/global-learnings.md` with the cleaned-up file and push.

## Preflight, commit, and push

Same convention as `backup-claude-setup`: read is anonymous, writing to this
repo from a cloud/remote session needs it in the session's authorized set
(`add_repo` with `access: "push"` for `rileytrottier23/Riley-Claude-Skills"`
if that tool exists). If push is blocked, do the work locally and hand back
the diff plus exact push commands instead of guessing further.

```bash
cd <repo>
git add config/global-learnings.md
git commit -m "Add global learning: <one line>"   # or "Prune global learnings"
git push origin main
```

Straight-to-main is the convention here, same as the rest of the control
plane — unless a session's own harness rules require a branch + PR, in which
case follow those instead.

## Report

One or two sentences: what was captured and where it went (global memory,
promoted to skill `X`, or left project-local and why), or — for a review
pass — what was pruned or promoted and what's left.
