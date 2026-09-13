# Throughline

Riley's daily dashboard. Formerly "First Light Brief" — same artifact, same URL, renamed 13 Sep 2026.

**Live at** https://claude.ai/code/artifact/428a6851-8f8f-4bbb-bdff-f1cedb5f694c

Installed as a pinned app window on Windows and a home-screen app on Android. The URL never changes,
so both installs survive every republish.

---

## What it is

A dashboard that organises the day and compounds week over week — not a morning digest. Two tabs:

- **Today** — a narrow rail (greeting, schedule, counters, Ask Claude) beside a board of all five
  Google Task lists, a "Done today" strip, and a mail section.
- **Week** — the rail becomes an archive picker; the body shows last week's counters, Claude's
  advice, and what was completed, what rolled over, and what was written down.

## Identity

- **Name** Throughline
- **Mark** a continuous rule stitching seven uprights, today's taller and in amber
- **Palette** cyanotype `#0A2A5E`, paper `#F2F4F6`, amber `#FFB000` as the *only* signal colour
- **Type** Archivo / Archivo Narrow
- **Background** engraved instrument plates — gear, dividers and ripples on the rail; prism,
  hourglass, pendulum, sextant, flywheel, moon phases and paper plane on the board
- **Favicon** 📶 — the artifact favicon only accepts emoji, so the real mark can't be the browser-tab
  icon. It is used everywhere else.

Rule that holds the whole thing together: **if it's amber, it's now.**

---

## Architecture — two layers

### Live layer (in the page)
Registers `watchTool` against the viewer's connectors:

| What | Tool | Interval |
|---|---|---|
| Five task lists, open | `list_tasks` | 60s |
| Five task lists, completed today | `list_tasks` (`completedMin` = local midnight) | 60s |
| Primary unread mail | `search_threads` | 60s |
| Calendar | `list_events` | 30 min |

Watches re-register at local midnight (the completed-today and calendar windows are absolute) and
whenever `briefing/current.lists` changes.

### Judgement layer (scheduled)
`Throughline — hourly` · `trig_01UGimbrAf3miYHyVDQQv744` · cron `0 0-5,13-23 * * *` UTC
(06:00–22:00 Pacific). Supplies the headline, per-task notes, triage, the reading pick — and
auto-files service errors. It is **not** the source of truth for list membership.

`Throughline — weekly review` · `trig_015hXDZZKqzKJRieMbGs57dq` · cron `0 4 * * 1` UTC
(Sunday 21:00 Pacific). Writes `reviews/<ISO week>` and updates `reviews/index`.

---

## Capabilities declared

```json
{"db": {}, "sample": {},
 "mcp": {"servers": [
   {"server": "Google Tasks MCP", "tools": ["patch_task","list_tasks","insert_task","delete_task"]},
   {"server": "Gmail",            "tools": ["search_threads"]},
   {"server": "Google Calendar",  "tools": ["list_events"]}]}}
```

`sample` powers Ask Claude. The viewer pays for it and consents on first use; there is no memory
between questions, so the page sends the day's context with every one.

## db documents

| Doc | Written by | Holds |
|---|---|---|
| `briefing/current` | hourly run | `generatedAt`, `dateKey`, `dateLabel`, `headline`, `footNote`, `footStatus[]`, `lists{}`, `timeline[]`, `tasks[]`, `completed[]`, `review[]`, `waiting[]`, `reading{}`, `passage{}` |
| `briefing/checks` | the page | `{date, done:{}, reopened:{}}` — optimistic tick overlay |
| `reviews/index` | weekly run | `{weeks:[{key,label,range,completed}]}`, newest first, ≤52 |
| `reviews/<ISO week>` | weekly run | `key`, `label`, `range`, `counts{}`, `advice`, `completed[]`, `rolled[]`, `events[]`, `journal[]` |

## Google Task list ids — load-bearing

```
Today       MDE4MDA5MzE3NjczNzcxODExNjc6MDow
Short-term  ajdxN3hkdzdsNEZzdUtJOA
AI          TGphaktHczdaSmxDZkhScA
Waiting     OGVMNHJwUkRINGc2QUE1Ng
Claude      UVVBaHEyZk45NDVzUFU3YQ
```

They are hardcoded in the page as a fallback **and** written into `briefing/current.lists` each hour.
The db value wins where the labels match, so a list rebuilt in Google is fixed by the next hourly run
rather than a republish.

---

## Behaviours worth knowing

**Ticking** calls `patch_task` straight from the page, with per-row failure copy branched on the
McpError code. `server_unavailable` / `rate_limited` / `upstream_error` are *ambiguous* for a write —
the call may have landed — so they are never auto-retried; the "Try again" button is a fresh gesture.

**Moving between lists.** Google Tasks has no cross-list move: `move_task` only reorders within a
list. So a move is `insert_task` into the destination + `delete_task` from the source. Consequences,
all deliberate and all surfaced in the UI:
- the task comes back with a **new id** and **no completion history**
- title, notes and due date carry; nothing else does
- `delete_task` returns an empty 204 body, which the connector's JSON parser reports as
  `Unexpected end of JSON input` **even though the delete succeeded** — verified by re-listing. The
  page treats exactly that message as success. If the delete genuinely fails, the card says the task
  was copied but not removed, and names the list to clean up.
- every move offers **Undo** for 12 seconds, which performs the same operation in reverse

**Error auto-filing.** The hourly run checks Railway and GitHub, and files each genuine failure as a
task in the **Claude** list with a dedupe key on the first line of `notes`
(`auto:railway:<service>:<deployment>` / `auto:github:<repo>:<run>`). The page renders that list as
its Claude column and flags anything whose notes start with `auto:`, which also drives the amber Error
counter. This step runs **every hour regardless of weekday**. A recovered service does **not**
auto-complete its task — Riley closes those.

**Mail** is primary inbox only (`category:primary`), always. Never Promotions, Social or Updates.

**Weekend shape.** No GitHub, Railway or deep-work framing in the headline on Sat/Sun. Error
auto-filing still runs; it just doesn't drive the narrative.

---

## Open items

- The cron is fixed UTC. When BC leaves daylight time on **1 Nov 2026** the hourly window shifts an
  hour early — change to `0 1-6,14-23 * * *`, and the weekly to `0 5 * * 1`. Back again in March.
- Slack is authorised on the account but its tools would not load; not wired in.
- `routines/weekly-rollup-dashboard-refresh.json` backs up a routine no longer on the account — Riley
  hasn't said whether it was retired deliberately.
- The routine JSON backups regenerate from `scripts/format_routines.py`; after this rename the old
  `first-light-brief-*.json` files retire on the next backup run.
