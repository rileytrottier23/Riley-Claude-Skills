---
name: publish-skill-to-github
description: Push a new or edited Claude skill to Riley's skills repo (rileytrottier23/Riley-Claude-Skills) and update the README counts, category table, plugin marketplace, and changelog. Use whenever a skill is created, packaged, edited, or vendored from elsewhere — including right after skill-creator produces a SKILL.md or a .skill file — and whenever Riley says "push this skill", "add this to my skills repo", "sync my skills", or "update the skills README".
---

# Publish Skill to GitHub

New skills belong in **`rileytrottier23/Riley-Claude-Skills`**, not in a chat history. This skill puts them there and keeps the README's numbers true.

## When to run this

Run it at the end of any session that produced or changed a skill — `skill-creator` finished a draft, you packaged a `.skill` file, you edited a `SKILL.md`, or Riley pulled a skill from someone else's repo. Say what you're doing in one line rather than asking permission for the routine case.

Ask first when the skill carries anything that shouldn't be public: client names, internal process detail, credentials, or personal data beyond what `personal/` already holds. The repo is public.

## Preflight: where am I running?

Two environments, and they fail in completely different ways. Work out which one you are in **first** —
`git -C <clone> push --dry-run origin main` answers it faster than guessing.

### Local terminal (Claude Code on Riley's machine)

The normal case, and the one to prefer. Bash is Riley's own shell: his git credentials, his network,
his working copy. If `C:\Users\riley\Riley-Claude-Skills` already exists, work in it directly —
`git pull` first — rather than cloning a second copy somewhere else.

```bash
cd /c/Users/riley/Riley-Claude-Skills   # adjust for the shell in use
git pull
git push --dry-run origin main
```

A clean dry run means you can do the whole job yourself: copy the skill in, run the script, commit, push.
No patches, no handing Riley commands to paste.

### Cloud session (Cowork sandbox)

Bash runs in a container that cannot see Riley's machine. Read access to the repo works anonymously;
**write access requires the repo to be in the session's authorized set**, and usually it is not.

```bash
cd /tmp && rm -rf rcs
git clone https://github.com/rileytrottier23/Riley-Claude-Skills.git rcs
cd rcs && git push --dry-run origin main
```

If that fails with *"not in this session's authorized repository set"*, and an `add_repo` tool exists,
call it with `access: "push"`. Otherwise fall back, in this order:

1. **If Riley's repo folder is connected** (or he will connect it — offer `device_request_folder_access`),
   write the changes straight into his working copy and let him run `git add/commit/push`. Note the
   limits of that bridge: no network from the device side, no deleting files, and git itself cannot run
   there — `.git/index.lock` is not writable. So fetching anything from another repo is Riley's step,
   not yours. Preserve the file's existing line endings; his checkout is CRLF and a whole-file ending
   flip buries the real diff.
2. **Otherwise** do the work in the container, commit locally, and send `git format-patch` output with
   `SendUserFile`. Tell him where the file lands and give the exact `git am` line. Verify afterwards that
   the commits actually reached the remote — a `git push` reporting "everything up-to-date" means the
   patch never applied, not that the work is done.

Either way, package the skill as a `.skill` file and deliver it with `SendUserFile`: a push does not
install anything in Riley's Claude account.

Never force, never try another token, never push to a different repo.

## Repo layout

```
Riley-Claude-Skills/
├── .claude-plugin/marketplace.json   five plugins, each pointing at a directory
├── README.md                          counts + per-category tables
├── CHANGELOG.md                       newest first
├── pm/<skill>/SKILL.md                Riley's PM skills          → riley-pm-skills
├── personal/<skill>/SKILL.md          Riley's personal skills    → riley-personal-skills
├── anthropic/<skill>/                 vendored, Apache 2.0       → anthropic-example-skills
└── third-party/<collection>/          vendored, CC BY-NC-SA 4.0  → pm-skills-*
```

Choosing a home:

- **Riley's own skill, product work** → `pm/`
- **Riley's own skill, everything else** — personal life, or tooling written for his setup specifically → `personal/`
- **Someone else's skill** → `third-party/<author>-<collection>/`, with the original LICENSE, a NOTICE crediting the author, and the upstream commit recorded. Never relicense it; the repo's MIT covers Riley's own skills only.

Plugins point at whole directories, so **a skill dropped into an existing category needs no marketplace edit** — Riley's next `git pull` picks it up with no reinstall. A brand-new category needs a new plugin entry in `marketplace.json`, a new README section with a table, and a row in the plugin table under Install. Prefer an existing category; a sixth plugin for one skill is not worth the install step.

## Steps

### 1. Validate the skill

- Folder name matches the frontmatter `name` exactly, lowercase and hyphenated
- `description` says both what it does *and* when to trigger, including casual phrasings — the README says it plainly: a skill with a perfect body and a vague description never fires
- No secrets, no session container paths (`/home/claude/...`, `/tmp/...`), no absolute paths at all

### 2. Copy it in

```bash
cp -r <skill-folder> <repo>/<category>/     # <repo> = his working copy locally, /tmp/rcs in a cloud session
```

If the folder already exists, this is an update — `git diff` it so the changelog line can say what actually changed.

### 3. Update the README and marketplace

```bash
python3 <repo>/personal/publish-skill-to-github/scripts/update_readme.py <repo> \
  --added <category>/<skill-name> \
  --desc "One line, present tense, what it does — not when it triggers." \
  --bump minor
```

The script:

- fixes the "N skills installable" line, the Skills column in the plugin table, the plugin-count word, and the anthropic and third-party counts
- appends a row for the new skill under its category heading
- writes a dated `CHANGELOG.md` line, newest first
- bumps `marketplace.json` `metadata.version` — minor for a new skill, patch for an edit

It **never rewrites rows it did not add**: those descriptions are hand-written and better than raw frontmatter. Lines starting with `!` are drift it found but would not touch — a skill listed in the README that is gone from disk, a plugin path that no longer resolves. Fix those by hand.

Run `--check` first if you want to see the state without writing.

Then read the README yourself for what a script cannot judge: does the plugin's one-line description in `marketplace.json` and in the plugin table still cover what the plugin now contains? Adding a repo-ops skill to `riley-personal-skills` makes "Canadian personal finance, chess coaching, French tutoring" incomplete. Fix the description; leave the rest of the README's voice alone.

### 4. Commit and push to main

```bash
cd <repo>
git add -A
git status --short
git commit -m "Add <category>/<name>: <one-line summary>"
git push origin main
```

GitHub prints `Bypassed rule violations for refs/heads/main` on every push here. That is expected, not an error: the repo carries a branch protection rule requiring pull requests, and Riley has decided skills go straight to main anyway. Don't switch to a PR because of that warning.

`Add <path>: <summary>` for new skills, `Update <path>: <what changed>` for edits. No co-author trailers in this repo. If the push is rejected because main moved, `git pull --rebase` once and retry; if it fails again, stop and report.

### 5. Report and hand over the file

Two sentences: what landed, the commit URL, what the README now says. Then deliver the `.skill` file with `SendUserFile` — a push does not install anything in Riley's Claude account:

```bash
cd <parent-of-skill-folder>
zip -rq /home/claude/<name>.skill <name> -x '*.DS_Store'
```

The folder must sit at the archive root with `SKILL.md` inside it.

## What not to do

- Don't push to any repo but `rileytrottier23/Riley-Claude-Skills`.
- Don't open a branch or PR — this repo commits straight to main.
- Don't hand-edit skill counts; rerun the script.
- Don't restructure the README or rewrite its prose. Update what the new skill changed.
