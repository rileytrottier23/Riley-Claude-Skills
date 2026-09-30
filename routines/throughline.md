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
Registers `watchTool` against the viewer's connectors. Changed 30 Sep 2026 to cut calls from 12 to
about 7 a minute (the old rate tripped Google throttling and left the page "Live paused"):

| What | Tool | Interval |
|---|---|---|
| Five task lists, open | `list_tasks` | 60s |
| Five task lists, completed today | `list_tasks` (`completedMin` = local midnight) | 5 min |
| Primary unread mail | `search_threads` | 2 min |
| Calendar | `list_events` | 30 min |

- **Backoff** — three transient task-watch failures in a row double the open-list interval (max
  5 min); it returns to 60s after 10 healthy minutes.
- **Immediate refresh** — after every tick or move the page calls `mcp.invalidate` on `list_tasks`
  (writes use `cache:false`, which doesn't feed watches). Returning to the page with data older than
  2 min forces a refetch of Tasks and Gmail. The platform also pauses polls while the page is hidden.
- **Freshness stamp** — "Live · updated N min ago", or "Behind · last update HH:MM" in red past 5 min.
- **Scheduled-later hidden** — tasks whose `due` date is after today stay off the board; each column
  shows "N scheduled for later". Needed because a repeating task ticked through the API is moved to
  its next date in place (same id, still open) instead of being hidden like the Google Tasks app does.

Watches re-register at local midnight (the completed-today and calendar windows are absolute) and
whenever `briefing/current.lists` changes. Ticks (`briefing/checks`) are keyed to the viewer's
calendar day, not the brief's `dateKey`.

### Judgement layer (scheduled)
`Throughline — hourly` · `trig_01UGimbrAf3miYHyVDQQv744` — **moving to 07:00, 12:00 and 17:00
Pacific** (from every hour 06:00–22:00) to cut token use by ~80%. Supplies the headline, per-task
notes, triage, the reading pick — and auto-files service errors. It is **not** the source of truth
for list membership.

`Throughline — weekly review` · `trig_015hXDZZKqzKJRieMbGs57dq` · cron `0 4 * * 1` UTC
(Sunday 21:00 Pacific). Writes `reviews/<ISO week>` and updates `reviews/index`.

---

## Capabilities declared

```json
{"db": {}, "sample": {},
 "mcp": {"servers": [
   {"server": "Google Tasks MCP", "tools": ["patch_task","list_tasks","insert_task","delete_task","get_task"]},
   {"server": "Gmail",            "tools": ["search_threads"]},
   {"server": "Google Calendar",  "tools": ["list_events"]}]}}
```

Runtime contract 0.2.66. `sample` powers Ask Claude. The viewer pays for it and consents on first
use; there is no memory between questions, so the page sends the day's context with every one.

## db documents

| Doc | Written by | Holds |
|---|---|---|
| `briefing/current` | scheduled run | `generatedAt`, `dateKey`, `dateLabel`, `headline`, `footNote`, `footStatus[]`, `lists{}`, `timeline[]`, `tasks[]`, `completed[]`, `review[]`, `waiting[]`, `reading{}`, `passage{}` |
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

They are hardcoded in the page as a fallback **and** written into `briefing/current.lists` on each
scheduled run. The db value wins where the labels match, so a list rebuilt in Google is fixed by the
next run rather than a republish. (Note: in Google the "Claude" id's list is currently titled
"Weekly Review".)

---

## Behaviours worth knowing

**Ticking** calls `patch_task` straight from the page. On an ambiguous failure
(`server_unavailable` / `upstream_error` / `rate_limited`) the page waits a few seconds, re-reads the
task with `get_task`, and treats it as saved if it landed — status completed, **or its due date moved**
(a repeating task advanced). Only if it plainly didn't land does it send the write once more. Never a
blind second write: for a repeating task that would tick tomorrow's instance too. Other failures show
per-row copy with "Try again".

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

**Error auto-filing.** The scheduled run checks Railway and GitHub, and files each genuine failure as
a task in the **Claude** list with a dedupe key on the first line of `notes`
(`auto:railway:<service>:<deployment>` / `auto:github:<repo>:<run>`). The page renders that list as
its Claude column and flags anything whose notes start with `auto:`, which also drives the amber Error
counter. Kept in the scheduled run rather than the page: the page only runs while open, and the
GitHub connector available to pages has no workflow-run tool. A recovered service does **not**
auto-complete its task — Riley closes those.

**Mail** is primary inbox only (`category:primary`), always. Never Promotions, Social or Updates.

**Weekend shape.** No GitHub, Railway or deep-work framing in the headline on Sat/Sun. Error
auto-filing still runs; it just doesn't drive the narrative.

---

## Open items

- The weekly cron is fixed UTC. When BC leaves daylight time on **1 Nov 2026** change it to
  `0 5 * * 1`. Back again in March. (Set the new 3×-daily schedule in Pacific time so it doesn't drift.)
- Slack is authorised on the account but its tools would not load; not wired in.
- `routines/weekly-rollup-dashboard-refresh.json` backs up a routine no longer on the account — Riley
  hasn't said whether it was retired deliberately.
- The routine JSON backups regenerate from `scripts/format_routines.py`; after this rename the old
  `first-light-brief-*.json` files retire on the next backup run.
