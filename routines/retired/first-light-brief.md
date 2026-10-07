# First Light Brief

A briefing dashboard. One page, installed as an app on Riley's Windows laptop and
Android phone.

It runs on two layers. The page polls Google Tasks, Gmail and Google Calendar itself
and re-renders within a minute of anything changing. An hourly Claude scheduled task
supplies the judgement the page cannot do for itself — the headline, each task's note,
why an email matters, service and review triage, the article pick.

Ticking a task on the page completes it in Google Tasks.

Last updated: 12 September 2026

---

## How to open it

**URL:** https://claude.ai/code/artifact/428a6851-8f8f-4bbb-bdff-f1cedb5f694c

Also stored in [`first-light-brief-artifact.json`](./first-light-brief-artifact.json),
so the routine can read it rather than carrying a hardcoded link.

The page is private to the account. Nobody else can open it unless it's shared from the
page's own share menu.

### Windows — install it as an app

1. Open the URL in Edge or Chrome.
2. **Edge:** `···` menu → **Apps** → *Install this site as an app*.
   **Chrome:** `⋮` menu → **Cast, save and share** → *Install page as app*.
3. Name it "First Light Brief" and confirm. You get a standalone window with its own
   taskbar icon — no address bar, no tabs.
4. Pin it: right-click the taskbar icon → **Pin to taskbar**.
5. Launch it at login: press `Win` + `R`, type `shell:startup`, press Enter. Drag the
   app's desktop shortcut into the folder that opens.

### Android — add it to your home screen

1. Open the same URL in Chrome on the phone.
2. `⋮` menu → **Add to Home screen** (on some builds it appears as *Install app*).
3. Confirm the name. It gets its own launcher icon and opens without browser chrome.

### Note

Opening the artifact from inside the Claude desktop app gives you Claude's own viewer,
which has no browser menu and therefore no install option. Use Chrome or Edge for the
install steps above. The artifact is also listed in the gallery at
claude.ai/code/artifacts.

*Installed on both devices, 12 September 2026.*

---

## What's on the page

| Card | What it shows | When it appears |
|---|---|---|
| **Schedule** | Today's events on a time rail, past items struck through, a red now-marker | Always |
| **Today** | Open tasks, tickable, ordered by what to do first | Always |
| **What matters** | The dark card — one sentence naming the most important thing right now | Always |
| **Completed today** | Everything finished since local midnight, wherever it was ticked | Always |
| **Mail** | Unread primary-inbox mail only | Always (shows "Inbox is clear" when empty) |
| **Waiting** | Held items, with age in days | Always |
| **Services** | Railway services that are failing or have undeployed changes | Only when something is wrong |
| **Review queue** | GitHub PRs and issues waiting on him | Only when non-empty |
| **Worth reading** | One article from the Readwise Reader queue | Only when one fits |
| **Highlight** | The glass panel — one Readwise highlight worth re-reading | Always |

Ticking a task moves it from **Today** to **Completed today** *and completes it in
Google Tasks*. The page calls the Google Tasks connector directly — the row shows
"Updating Google Tasks…", then "Saved to Google Tasks". Unticking reopens it the same
way. The move also saves to the page's own database, so laptop and phone agree
immediately.

If the write fails, the row says why and offers **Try again** where retrying is safe.
The tick still stands locally either way, and the live layer re-reads Google Tasks
within the minute — so a missed write corrects itself almost immediately.

**Completed today** is filled from Google Tasks — anything completed since local
midnight, wherever it was ticked.

### How the two layers merge

Live decides membership; the hourly brief decides presentation.

- **Tasks** — Google Tasks says which tasks exist and which are done. The brief supplies
  each task's tags and note, matched on task id, and its ordering is kept for the tasks
  it ranked. A task added since the last run appears within a minute, bare, and gets its
  note at the next hourly run.
- **Mail** — the live unread count is authoritative. The brief supplies the "why it
  matters" lines. When more have arrived than the brief describes, the card appends
  *"+N more since the last brief"* rather than showing an unexplained number.
- **Schedule** — live calendar says which events exist; the brief supplies the
  meeting-prep flags, matched on event name.
- **Everything else** — Waiting, Services, Review queue, Worth reading and the
  highlight are hourly only.

---

## Design

Built in the "Vantage" visual language:

- **Type:** Instrument Serif for the greeting, focus card and highlight; Inter for
  everything else. Both from Google Fonts.
- **Palette:** stone-50 ground (`#FAFAF9`) with a 20px dot grid, white cards, stone-900
  ink, orange-600 (`#EA580C`) as the single accent. Blue, green, purple and red appear
  only as small category markers on card icons and tags.
- **Cards:** 20px radius, hairline stone-200 borders, soft shadow that lifts on hover.
  The "What matters" card inverts to stone-900 with an orange blur glow. The highlight
  sits in a frosted glass panel.
- **Layout:** two independent columns, not a shared grid — grid rows stretch to their
  tallest card and leave dead space under the short ones.
- **Committed light theme.** It does not follow the system dark mode.

**Three libraries from the original template were replaced, deliberately:**

- *Phosphor Icons* and *AOS* load from unpkg, which published artifacts block. Icons are
  hand-drawn inline SVG in an `<svg><defs>` sprite; the scroll animations are gone
  (wrong for a dashboard — everything must be visible the moment it opens).
- *Tailwind play CDN* is allowed, but it compiles in the browser and causes a flash of
  unstyled content on every open. The design language is hand-written as plain CSS
  instead, so the page paints instantly and fetches nothing but fonts.

---

## How it updates

### The live layer — the page itself

The page holds watches on the viewer's own connectors and re-renders when a result
changes. Nothing here costs a Claude session.

| Source | Every | What it decides |
|---|---|---|
| Google Tasks — open tasks on all three lists | 60s | which tasks are in **Today** |
| Google Tasks — completed since local midnight | 60s | which are in **Completed today** |
| Gmail — unread primary, last 3 days | 60s | the Mail count |
| Google Calendar — today and tomorrow | 30 min | the Schedule strip |

Polling pauses while the window is hidden and catches up on return, so a pinned window
you are not looking at costs nothing. A **Live** chip sits beside the timestamp; it
reads *Live paused* if polling hits trouble, and the last good data stays on screen
rather than blanking.

Two windows are absolute and baked in when the watches register — the calendar range,
and `completedMin` for today's completions — so the page re-registers its watches at
local midnight, and whenever the task list ids change.

### The judgement layer — the hourly run

A Claude scheduled task named **"First Light Brief — hourly"**.

- **Trigger ID:** `trig_01UGimbrAf3miYHyVDQQv744`
- **Schedule:** cron `0 0-5,13-23 * * *` (UTC) = every hour from 06:00 to 22:00 Pacific,
  17 runs a day. Overnight is skipped — nothing changes at 03:00.
- **Runs:** in the cloud, in a fresh session. The laptop does not need to be on.

Backed up at [`first-light-brief-hourly.json`](./first-light-brief-hourly.json).

Each run reads:

- **Google Calendar** — today and tomorrow, America/Vancouver
- **Google Tasks** — open tasks from Today, Short-Term Tasks and Waiting, plus everything
  completed since local midnight
- **Gmail** — `in:inbox is:unread category:primary newer_than:3d`
- **Readwise** — daily review, for the highlight
- **Readwise Reader** — the "later" queue, for one article
- **GitHub** — open PRs and issues involving `rileytrottier23` *(weekdays only)*
- **Railway** — deployment status of every service *(weekdays only)*

It re-reads the live sources too, because it needs the same facts to judge them — and
because `lists` and the task ids come from that read. Then it judges what matters **for
the current time of day** — at 09:00 the headline is about the day ahead, at 15:00 about
what's left, at 21:00 about tomorrow — writes one sentence, and saves the result. The
page's greeting follows the viewer's clock independently (morning / afternoon /
evening).

### Weekday vs weekend

**Mon–Fri** is the full brief. **Sat–Sun** drops GitHub and Railway entirely, skips
meeting-prep flags, never marks a task "Deep work", and prefers errands, family and
personal items when trimming the list.

### Rules baked into the prompt

- Gmail's `category:primary` filter is mandatory. Promotions, Social, Updates and Forums
  never appear. An empty Mail card is a correct result, not a failure to fill.
- Railway reports a service **only** when its latest deployment is not `SUCCESS` or the
  environment has undeployed staged changes. A healthy project produces an empty array
  and the card stays hidden.
- Readwise highlights over ~200 characters are passed over — the page is built for low
  text density.
- **Task IDs must be the real Google Tasks identifiers.** `id`, `taskId` and `taskListId`
  come straight from the API and `id` equals `taskId`. Ticking a box calls `patch_task`
  with exactly those two values, so an invented slug breaks the write-back silently.
- Empty is always allowed. The prompt says never to invent filler to populate a card.
- The `checks` document is left alone unless the date has rolled over — overwriting it
  mid-day would undo ticks just made.

---

## Data model

The page reads two documents from the artifact's own database.

### `briefing/current`

```json
{
  "generatedAt": "2026-09-12T13:30:00Z",
  "dateKey": "2026-09-12",
  "dateLabel": "Saturday 12 September",
  "headline": "One sentence, max ~30 words.",
  "footNote": "Tasks and mail live · judgement refreshed hourly",
  "footStatus": ["5 Railway services healthy", "Review queue clear"],
  "lists": { "Today": "<list id>", "Short-term": "<list id>", "Waiting": "<list id>" },
  "timeline": [
    { "time": "09:00", "label": "Event name", "allDay": false, "past": false, "flag": "No agenda" }
  ],
  "tasks": [
    { "id": "<google task id>", "taskListId": "<google list id>", "taskId": "<google task id>",
      "title": "...", "list": "Today",
      "due": "Due today", "focus": "Deep work", "note": "..." }
  ],
  "completed": [
    { "id": "<google task id>", "taskListId": "...", "taskId": "...", "title": "..." }
  ],
  "inbox":    [ { "from": "...", "title": "...", "note": "...", "url": "..." } ],
  "services": [ { "name": "ReflectAI", "status": "Deploy failed", "note": "..." } ],
  "review":   [ { "title": "...", "repo": "owner/repo", "note": "...", "url": "..." } ],
  "waiting":  [ { "title": "...", "age": "21d", "note": "..." } ],
  "reading":  { "title": "...", "source": "...", "minutes": "3 min", "url": "...", "note": "..." },
  "passage":  { "text": "...", "cite": "Author · Title" }
}
```

Field notes:

- `timeline` — at most 4 entries, short labels, no separate note field. `past: true`
  strikes it through and places the red now-marker after it. `allDay: true` renders blue.
  `flag` is the meeting-prep warning and renders in orange. With live calendar on, only
  `flag` survives — the events themselves come from the connector.
- `lists` — the three Google Tasks list ids. **The page registers its live polling
  against these**, so a wrong or missing id silently turns live updating off and the
  page falls back to whatever the last hourly run said.
- `tasks` — at most 7 open tasks. `due` renders as an orange tag, `focus` as purple,
  `list` as grey. The three id fields drive both the write-back and the live merge.
- `completed` — tasks completed today, newest first, at most 10. Titles and ids only.
- `inbox`, `services`, `review` — empty arrays are normal. Services, Review and Reading
  hide their whole card when empty; Mail shows "Inbox is clear".
- `waiting.age` — days since the task was last touched, omitted under 2 days.
- `footStatus` — short tokens for things that were checked and had nothing to report.

### `briefing/checks`

```json
{
  "date": "2026-09-12",
  "done":     { "<google task id>": true },
  "reopened": { "<google task id>": true }
}
```

The page's optimistic overlay, written when a box is ticked. `done` marks open tasks
that were ticked; `reopened` marks completed ones that were unticked. It keeps the two
columns right on both devices in the seconds before the live layer catches up, while
Google Tasks remains the source of truth. The scheduled task resets it only when the
date rolls over.

### Connector access

The page's whole connector surface is the `mcp` capability manifest, and it is the
complete list of what the page can do:

| Connector | Tool | Used for |
|---|---|---|
| Google Tasks MCP | `patch_task` | completing and reopening a task — the only write |
| Google Tasks MCP | `list_tasks` | live open and completed tasks |
| Gmail | `search_threads` | live unread primary count |
| Google Calendar | `list_events` | live schedule |

Nothing else is reachable. Calls run with the viewer's credentials; the page never sees
a token. The first use of each connector asks to allow it once.

Write failures are handled per row, with the fix that actually resolves each one —
reconnect, add the connector, choose between duplicates, needs approval, or a **Try
again** button for the ambiguous cases. There is deliberately no auto-retry on writes:
an unreachable connector is not proof the write didn't land.

Read failures degrade instead: a transient error keeps the last good data on screen and
flips the chip to *Live paused*; an authorization failure turns the live layer off and
falls back to the hourly snapshot.

---

## Changing it

- **What's on the page** (layout, colours, cards, polling intervals): ask Claude to edit
  and republish the artifact. Same URL, so the installed app and home-screen icon keep
  working.
- **What goes in it** (sources, judgement rules, thresholds): ask Claude to update the
  scheduled task's prompt. The prompt is the whole specification.
- **Adding a connector to the live layer:** it needs both a page change and a new entry
  in the `mcp` manifest — the manifest is enforced, so code alone will not do it.
- **The time it runs:** the cron is UTC.

---

## Known issues

- **Daylight time.** The cron is fixed in UTC. When BC leaves daylight time on
  1 November 2026 the window shifts an hour early, running 05:00–21:00 local. Change the
  cron to `0 1-6,14-23 * * *` then, and back to `0 0-5,13-23 * * *` in March.
- **Write-back is one-way for completion only.** Ticking completes or reopens a task.
  Editing a title, due date or list still has to happen in Google Tasks.
- **Only Google Tasks writes back.** Everything else the page touches is read-only.
- **Live covers three sources, not all of them.** Waiting ages, Railway, GitHub, the
  Reader pick and the highlight move only on the hourly run.
- **A task added since the last hourly run shows up bare** — no tags, no note — until
  the next run annotates it. That is the live layer working, not a fault.
- **The live layer needs the viewer's own connectors.** Opened by anyone else, or with
  the connectors unavailable, the page falls back to the last hourly snapshot and the
  Live chip disappears.
- **Slack.** Authorized on the account but its tools would not load in the build session,
  so it is not wired in. If reconnected, a DMs-and-mentions card can be added.
- **Waiting ages** are computed from each task's `updated` timestamp, which is when it
  was last *touched*, not when it was created. Editing a Waiting item resets its age.

---

## History

| Date | Change |
|---|---|
| 12 Sep 2026 | Built. Artifact + db + daily scheduled task. Verified end to end. |
| 12 Sep 2026 | Four UX directions explored; "Quiet Tiles" chosen. |
| 12 Sep 2026 | Dark scheme, Today / Completed today split, primary-inbox-only mail. |
| 12 Sep 2026 | Added Railway health, GitHub review queue, meeting-prep flags, Reader pick, Waiting ages, weekday/weekend shapes. |
| 12 Sep 2026 | Rebuilt in the Vantage design language. Phosphor, AOS and Tailwind CDN replaced with inline SVG and hand-written CSS. |
| 12 Sep 2026 | Two-column layout to remove grid gaps. Installed on laptop and phone. |
| 12 Sep 2026 | Hourly refresh (06:00–22:00 Pacific), time-of-day headline and greeting, Completed today sourced from Google Tasks, and tick-to-complete write-back via the Google Tasks connector. |
| 12 Sep 2026 | Moved this doc into the repo; routine backed up; `format_routines.py` drift fixed. |
| 12 Sep 2026 | Live layer: the page polls Google Tasks and Gmail every 60s and Google Calendar every 30 min through the mcp capability, with the hourly run reduced to the judgement it supplies. |
