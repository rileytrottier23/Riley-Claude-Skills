# First Light Brief

A briefing dashboard. One page, installed as an app on Riley's Windows laptop and
Android phone, refreshed every hour between 06:00 and 22:00 Pacific by a Claude
scheduled task that reads his calendar, tasks, inbox and reading, decides what
actually matters, and writes the result to the page.

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
The tick still stands locally either way, and the next hourly refresh re-reads Google
Tasks as the source of truth — so a missed write corrects itself within the hour.

**Completed today** is filled from Google Tasks (anything completed since local
midnight), not just from what was ticked here. Tasks completed in the Google Tasks app
show up on the next refresh.

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

## How it gets filled

A Claude scheduled task named **"First Light Brief — hourly"**.

- **Trigger ID:** `trig_01UGimbrAf3miYHyVDQQv744`
- **Schedule:** cron `0 0-5,13-23 * * *` (UTC) = every hour from 06:00 to 22:00 Pacific,
  17 runs a day. Overnight is skipped — nothing changes at 03:00.
- **Runs:** in the cloud, in a fresh session. The laptop does not need to be on.

> **Not yet backed up.** This routine has no `.json` restore block in this folder — the
> prompt lives only on the account. Back it up the next time `backup-claude-setup` runs.

Each run reads:

- **Google Calendar** — today and tomorrow, America/Vancouver
- **Google Tasks** — open tasks from Today, Short-Term Tasks and Waiting, plus everything
  completed since local midnight
- **Gmail** — `in:inbox is:unread category:primary newer_than:3d`
- **Readwise** — daily review, for the highlight
- **Readwise Reader** — the "later" queue, for one article
- **GitHub** — open PRs and issues involving `rileytrottier23` *(weekdays only)*
- **Railway** — deployment status of every service *(weekdays only)*

Then it judges what matters **for the current time of day** — at 09:00 the headline is
about the day ahead, at 15:00 about what's left, at 21:00 about tomorrow — writes one
sentence, and saves the result. The page's greeting follows the viewer's clock
independently (morning / afternoon / evening).

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
  "footNote": "Refreshed hourly, 06:00–22:00 Pacific",
  "footStatus": ["5 Railway services healthy", "Review queue clear"],
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
  `flag` is the meeting-prep warning and renders in orange.
- `tasks` — at most 7 open tasks. `due` renders as an orange tag, `focus` as purple,
  `list` as grey. The three id fields drive the write-back.
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
columns right on both devices between refreshes, while Google Tasks remains the source
of truth. The scheduled task resets it only when the date rolls over.

### Write-back

Declared on the artifact as an `mcp` capability scoped to exactly one connector and one
tool: **Google Tasks MCP → `patch_task`**. The page cannot call anything else. Calls run
with the viewer's credentials; the page never sees a token. The first tick asks to allow
the connector once.

Failures are handled per row, with the fix that actually resolves each one — reconnect,
add the connector, choose between duplicates, needs approval, or a **Try again** button
for the ambiguous cases. There is deliberately no auto-retry on writes: an unreachable
connector is not proof the write didn't land.

---

## Changing it

- **What's on the page** (layout, colours, cards): ask Claude to edit and republish the
  artifact. Same URL, so the installed app and home-screen icon keep working.
- **What goes in it** (sources, judgement rules, thresholds): ask Claude to update the
  scheduled task's prompt. The prompt is the whole specification.
- **The time it runs:** the cron is UTC.

---

## Known issues

- **Daylight time.** The cron is fixed in UTC. When BC leaves daylight time on
  1 November 2026 the window shifts an hour early, running 05:00–21:00 local. Change the
  cron to `0 1-6,14-23 * * *` then, and back to `0 0-5,13-23 * * *` in March.
- **The routine is not backed up here.** No `.json` restore block yet — see above.
- **Write-back is one-way for completion only.** Ticking completes or reopens a task.
  Editing a title, due date or list still has to happen in Google Tasks.
- **Only Google Tasks writes back.** Calendar, Gmail, Railway, GitHub and Readwise are
  read-only on this page.
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
| 12 Sep 2026 | Moved this doc into the repo. |
