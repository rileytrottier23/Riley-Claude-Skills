# Routines

Backups of Riley's **routines** — the scheduled triggers that run Claude sessions
on a cadence (e.g. the weekday *Weekly rollup dashboard refresh*). Routines live
in the Claude account, not in git; if one is deleted or an account is lost, there
is nothing to restore *from* unless it was captured here.

This folder is that capture. Each `<slug>.json` is one routine, and
[`INDEX.md`](./INDEX.md) is the generated table of what's backed up.

## How a backup is made

The [`backup-claude-setup`](../control-plane/backup-claude-setup/) skill (or you,
by hand) calls the `list_triggers` tool, pipes its JSON through the formatter, and
commits the result:

```bash
# Claude runs list_triggers, saves its JSON to triggers.json, then:
python3 scripts/format_routines.py triggers.json
git add routines/ && git commit -m "Back up routines" && git push
```

The formatter writes one file per routine plus a regenerated `INDEX.md`. It never
calls a tool or the network — it only shapes JSON Claude already fetched.

## What each file holds

- `id`, `name`, `enabled`, schedule (`cron_expression` **or** `run_once_at`),
  `created_at`, `notifications`
- `prompt` — the full message the routine fires each time
- `restore` — the exact arguments for a `create_trigger` call

Volatile runtime fields (`next_run_at`, `last_fired_at`) are intentionally **not**
stored — they move on every fire, so keeping them would make the backup churn a
commit every run even when nothing meaningful changed.

## Restoring a routine

Routines can only be recreated through the Claude account (the JSON here is a
record, not a live object). Ask Claude:

> "Recreate the routine in `routines/weekly-rollup-dashboard-refresh.json`."

Claude reads the file and calls `create_trigger` with the `restore` block —
`name`, `prompt`, `initiation`, the schedule, and `create_new_session_on_fire`
when the routine fires a fresh session. The new routine gets a **new** `trig_…`
id; back up again so this folder reflects it.

`cron_expression` is in **UTC**. The weekly rollup's `0 14 * * 1-5` is 7:00 AM
Pacific on weekdays (UTC−7 in summer). If you edit a schedule, convert from local
time to UTC first.

## What not to commit here

A routine's prompt can name private resource IDs (calendar/Notion/Drive handles).
Those aren't credentials — they're inert without Riley's authenticated
connectors — so they're fine in this public repo. **Secrets are not:** never
commit a routine whose prompt contains a token, API key, or password. If one
does, redact it in the backup and rotate the secret.
