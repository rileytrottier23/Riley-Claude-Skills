---
name: publish-skill-to-github
description: Push a new or edited Claude skill to the right one of Riley's three skills repos (riley-pm-skills, riley-coding-skills, riley-thinking-skills) and update that repo's README counts, tables, plugin marketplace, and changelog. Use whenever a skill is created, packaged, edited, or vendored from elsewhere — including right after skill-creator produces a SKILL.md or a .skill file — and whenever Riley says "push this skill", "add this to my skills repo", "sync my skills", or "update the skills README".
---

# Publish Skill to GitHub

Riley's skills live in **three repos, split by domain**, not in a chat history. This skill decides which
repo a skill belongs in, puts it there under `mine/` or `vendored/`, and keeps that repo's numbers true.

| Repo | Holds | Examples |
|---|---|---|
| [`riley-pm-skills`](https://github.com/rileytrottier23/riley-pm-skills) | Product & PM work | PRDs/specs, stakeholder decks, competitive & market research, discovery, JTBD, prioritization, roadmaps, user stories, PM career |
| [`riley-coding-skills`](https://github.com/rileytrottier23/riley-coding-skills) | Coding & engineering | TDD, debugging, code review, implementation planning, git worktrees, MCP-server building, frontend/webapp build & test, API references |
| [`riley-thinking-skills`](https://github.com/rileytrottier23/riley-thinking-skills) | Everything else | decision/reflection/practice partners, personal life (finance, chess, French), writing & comms, creative/design (art, brand, themes, GIFs), meta/tooling (this skill, Claude how-to) |

## Which repo? (routing)

1. **Is it about building software?** (code, tests, debugging, reviews, plans-for-code, dev tooling, MCP,
   frontend/webapp, API usage) → `riley-coding-skills`.
2. **Is it about product management?** (specs, discovery, strategy, roadmaps, stakeholder comms,
   competitive/market research) → `riley-pm-skills`.
3. **Anything else, or it spans domains** → `riley-thinking-skills`. This is the default and the home for
   every cross-cutting skill.

**Guess when it's obvious; ask when it isn't.** If a skill clearly fits one bucket, place it and say where
in one line. If it genuinely could sit in two (e.g. a "write a technical design doc" skill — PM or
coding?), stop and ask Riley with `AskUserQuestion`, offering the two candidate repos, before placing it.
Don't split the difference silently.

## `mine/` vs `vendored/` (placement inside a repo)

Every repo has the same two-way split:

- **Riley wrote it → `mine/<skill>/`.** Covered by that repo's MIT `LICENSE`.
- **Someone else wrote it → `vendored/<source>/`.** Group by source: `vendored/anthropic/<skill>/` for
  Anthropic skills, `vendored/<author>-<collection>/` otherwise. Keep the original `LICENSE`/`LICENSE.txt`,
  add or update a NOTICE (`vendored/<...>/README.md`) crediting the author, and record the upstream commit
  SHA and sync date. **Never relicense** — the repo's MIT covers `mine/` only.

Plugins point at whole directories (`./mine/`, `./vendored/anthropic/`), so **a skill dropped into an
existing directory needs no marketplace edit** — the next `git pull` picks it up. A brand-new vendored
*collection* needs: a new folder under `vendored/`, a NOTICE, a new plugin entry in `marketplace.json`, a
row in the vendored table, and a row in the plugin table.

## When to run this

At the end of any session that produced or changed a skill — `skill-creator` finished a draft, you
packaged a `.skill` file, you edited a `SKILL.md`, or Riley pulled a skill from someone else's repo. Say
what you're doing in one line rather than asking permission for the routine case.

Ask first when the skill carries anything that shouldn't be public: client names, internal process
detail, credentials, or personal data beyond what's already public. `riley-pm-skills` and
`riley-coding-skills` are public; `riley-thinking-skills` is public too — treat all three as public.

## Preflight: where am I running, and can I push?

`git -C <clone> push --dry-run origin main` answers both faster than guessing.

- **Local terminal (Claude Code on Riley's machine):** his credentials and working copies. If the target
  repo is already checked out locally, `git pull` and work in it directly. Do the whole job yourself.
- **Cloud/remote session:** the container can't see his machine. Read is anonymous; **write needs the repo
  in the session's authorized set.** If an `add_repo` tool exists, call it with `access: "push"` for the
  target repo. If push is still blocked, do the work locally, commit, and send `git format-patch` output
  (or a `.skill` file) with `SendUserFile`, plus the exact `git am`/push commands. Verify commits actually
  reached the remote before reporting done. Never force, never try another token, never push elsewhere.

## Steps

### 1. Validate the skill

- Folder name matches the frontmatter `name` exactly, lowercase and hyphenated
- `description` says both what it does *and* when to trigger, including casual phrasings — a skill with a
  perfect body and a vague description never fires
- No secrets, no session container paths (`/home/claude/...`, `/tmp/...`), no absolute paths at all

### 2. Copy it into the right repo and folder

```bash
cp -r <skill-folder> <repo>/mine/                 # Riley's own
cp -r <skill-folder> <repo>/vendored/<source>/    # someone else's — with its LICENSE + NOTICE
```

If the folder already exists, this is an update — `git diff` it so the changelog line can say what changed.

### 3. Update the README and marketplace

The script lives in `riley-thinking-skills/mine/publish-skill-to-github/scripts/update_readme.py` and works
on any of the three repos (they share the `mine/` + `vendored/` layout):

```bash
python3 <path-to>/update_readme.py <repo> \
  --added mine/<skill-name> \
  --desc "One line, present tense, what it does — not when it triggers." \
  --bump minor
```

It fixes the "N skills installable" line, the plugin table's Skills column, the plugin-count word, and each
vendored collection's count; appends a row for a new `mine/` skill under "## My skills (`mine/`)"; writes a
dated `CHANGELOG.md` line; and bumps `marketplace.json` version (minor for a new skill, patch for an edit).
It **never rewrites rows it did not add**. Lines starting with `!` are drift for you to fix by hand. Run
`--check` first to preview.

Then read the README yourself: does the plugin's one-line description still cover what the plugin now
contains? Fix the description if the new skill widened it; leave the rest of the prose alone.

### 4. Commit and push

```bash
cd <repo>
git add -A && git status --short
git commit -m "Add mine/<name>: <one-line summary>"      # or "Add vendored/<source>/<name>: ..."
git push origin main
```

`Add <path>: <summary>` for new skills, `Update <path>: <what changed>` for edits. No co-author trailers.
Riley's convention is straight-to-main for these repos; if the push is rejected because main moved,
`git pull --rebase` once and retry, then stop and report if it still fails. (A session whose own harness
rules require a branch + PR should follow those instead — that's a session override, not a repo rule.)

### 5. Report and hand over the file

Two sentences: which repo it landed in, the commit URL, what that README now says. Then deliver the
`.skill` file with `SendUserFile` — a push does not install anything in Riley's Claude account:

```bash
cd <parent-of-skill-folder>
zip -rq <name>.skill <name> -x '*.DS_Store'
```

The folder must sit at the archive root with `SKILL.md` inside it.

## What not to do

- Don't push to any repo but the three above.
- Don't guess when the domain is genuinely ambiguous — ask.
- Don't put a vendored skill in `mine/`, or relicense someone else's work.
- Don't hand-edit skill counts; rerun the script.
- Don't restructure a README or rewrite its prose. Update what the new skill changed.
