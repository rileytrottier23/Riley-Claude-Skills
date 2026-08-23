# Superpowers — Jesse Vincent

Fourteen skills from [obra/superpowers](https://github.com/obra/superpowers), by **Jesse Vincent**
(same author as [`../obra-elements-of-style`](../obra-elements-of-style)). Vendored at upstream
`b36e082` (v6.3.0), synced 2026-08-23.

Superpowers is a software-development *methodology* for coding agents — TDD, systematic debugging,
planning, code review, and git-worktree discipline, written to activate from their descriptions the way
any skill does. This is a coding-agent toolkit, not PM work; it lives here because it is worth pinning
and it is by an author already vendored in this repo.

## What was and wasn't vendored

Only the `skills/` tree came across — the 14 skill folders plus their local `scripts/`, `references/`,
and `examples/` assets. Upstream also ships a **`SessionStart` hook** that force-injects the
`using-superpowers` skill into every conversation (an `<EXTREMELY_IMPORTANT>` "You have superpowers"
preamble), plus plugin manifests for a dozen agent runtimes. **None of that hook machinery is vendored**
— this repo is skills-only. Consequences worth knowing:

- **`using-superpowers`** is designed to be force-loaded every session by that hook. Without it, the
  skill still exists but only triggers from its description like any other; it will not seize every
  conversation. That is intentional here.
- The skills cross-reference each other by the **`superpowers:` plugin namespace** (e.g.
  `superpowers:test-driven-development`). The marketplace plugin is named exactly `superpowers` so those
  references resolve to the installed skills. If you copy these folders in by hand under a differently
  named plugin, the explicit `Skill` calls between them won't match — Claude will fall back to
  description matching.
- A few skills reference upstream conventions like `docs/superpowers/plans/…` and `.superpowers/sdd/…`
  as working directories. Those are just paths the skill creates in your project; nothing external is
  required.

## License

**MIT** — see [`LICENSE`](./LICENSE), preserved from upstream (Copyright (c) 2025 Jesse Vincent).
Unlike the two CC BY-NC-SA collections in `third-party/`, MIT carries no NonCommercial restriction.

## The skills

| Skill | What it does |
|---|---|
| [test-driven-development](./test-driven-development) | Enforces RED-GREEN-REFACTOR before any implementation code. |
| [systematic-debugging](./systematic-debugging) | Structured root-cause investigation before proposing fixes. |
| [verification-before-completion](./verification-before-completion) | Run verification and confirm output before claiming work is done. |
| [brainstorming](./brainstorming) | Explores intent, requirements, and design before any creative/build work. |
| [writing-plans](./writing-plans) | Turns a spec into a written, checkbox-tracked implementation plan. |
| [executing-plans](./executing-plans) | Executes a written plan in a fresh session with review checkpoints. |
| [subagent-driven-development](./subagent-driven-development) | Runs plan tasks via subagents in the current session. |
| [dispatching-parallel-agents](./dispatching-parallel-agents) | Fans out 2+ independent tasks with no shared state. |
| [requesting-code-review](./requesting-code-review) | Requests review before merging major work. |
| [receiving-code-review](./receiving-code-review) | Handles review feedback with verification, not performative agreement. |
| [using-git-worktrees](./using-git-worktrees) | Creates an isolated workspace before feature work. |
| [finishing-a-development-branch](./finishing-a-development-branch) | Decides how to integrate completed, tested work. |
| [writing-skills](./writing-skills) | How to author and test skills (TDD-for-docs). |
| [using-superpowers](./using-superpowers) | Bootstrap skill for finding and invoking the rest. Meant to be loaded first. |

Not a live mirror — a pinned snapshot. Updating means a fresh vendor commit against a newer upstream SHA,
never an edit in place, so the diff always shows what changed upstream.
