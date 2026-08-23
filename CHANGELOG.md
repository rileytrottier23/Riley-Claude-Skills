# Changelog

Newest first.

- 2026-08-23 — Split this library into three domain repos. Skills now live in
  [riley-pm-skills](https://github.com/rileytrottier23/riley-pm-skills) (16),
  [riley-coding-skills](https://github.com/rileytrottier23/riley-coding-skills) (19), and
  [riley-thinking-skills](https://github.com/rileytrottier23/riley-thinking-skills) (21). Removed the
  in-repo skill folders (`pm/`, `personal/`, `anthropic/`, `third-party/`); full pre-split history
  remains in git. Rewrote `marketplace.json` as an **aggregator** that sources all 8 plugins from the
  three repos, so the existing `riley-claude-skills` marketplace keeps working as a combined hub
  (`/plugin marketplace update` to pick it up).
- 2026-08-23 — Added `third-party/obra-superpowers`. 48 skills total.
- 2026-08-23 — Added `third-party/obra-elements-of-style`, vendored from obra@05fc4f0. 34 skills total.
- 2026-08-22 — Added `personal/publish-skill-to-github`. 33 skills total.
