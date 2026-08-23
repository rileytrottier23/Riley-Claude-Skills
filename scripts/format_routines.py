#!/usr/bin/env python3
"""Turn `list_triggers` output into versioned routine backups.

Routines (scheduled triggers) live in Riley's Claude account, not in git. This
script takes the JSON that the claude-code-remote `list_triggers` tool returns
and writes one readable, restorable file per routine into `routines/`, plus a
regenerated `INDEX.md` table.

Usage — pipe the tool's JSON in on stdin:

    <list_triggers JSON> | python3 scripts/format_routines.py

or point it at a saved file:

    python3 scripts/format_routines.py path/to/list_triggers.json

It accepts either the raw tool envelope (`{"data": [...]}`) or a bare list of
triggers. Each output file carries a `restore` block whose fields map exactly
onto a `create_trigger` call, so recreating a lost routine is mechanical.

The script is pure formatting — it never calls any tool and never touches the
network. Claude gathers the data (by calling `list_triggers`) and commits the
result; this only shapes it.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROUTINES_DIR = Path(__file__).resolve().parent.parent / "routines"


def slugify(name: str, fallback: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", (name or "").lower()).strip("-")
    return slug or fallback


def _first_user_message(trigger: dict) -> str:
    """Dig the fired prompt out of the trigger's job_config, tolerating shape drift."""
    try:
        events = trigger["job_config"]["ccr"]["events"]
        for ev in events:
            msg = ev.get("data", {}).get("message", {})
            if msg.get("role") == "user" and msg.get("content"):
                return msg["content"]
    except (KeyError, TypeError, IndexError):
        pass
    return ""


def normalize(trigger: dict) -> dict:
    tid = trigger.get("id", "")
    name = trigger.get("name", "") or tid or "unnamed-routine"
    prompt = _first_user_message(trigger)
    creates_new_session = bool(
        trigger.get("job_config", {})
        .get("ccr", {})
        .get("events", [{}])[0]
        .get("data", {})
        .get("isSynthetic")
    )
    restore = {
        "name": name,
        "prompt": prompt,
        "initiation": "human_request",
    }
    if trigger.get("cron_expression"):
        restore["cron_expression"] = trigger["cron_expression"]
    if trigger.get("run_once_at"):
        restore["run_once_at"] = trigger["run_once_at"]
    # A synthetic-message routine fires a fresh session each time.
    if creates_new_session:
        restore["create_new_session_on_fire"] = True
    if trigger.get("persistent_session_id"):
        restore["persistent_session_id"] = trigger["persistent_session_id"]

    # Volatile runtime fields (next_run_at, last_fired_at) are deliberately
    # omitted: they change on every fire, and a backup that churned every run
    # would defeat "only commit when something actually changed". Everything
    # needed to restore a routine is stable.
    return {
        "id": tid,
        "name": name,
        "enabled": trigger.get("enabled", True),
        "cron_expression": trigger.get("cron_expression"),
        "run_once_at": trigger.get("run_once_at"),
        "created_at": trigger.get("created_at"),
        "notifications": trigger.get("notifications"),
        "prompt": prompt,
        "restore": restore,
    }


def load(raw: str) -> list[dict]:
    data = json.loads(raw)
    if isinstance(data, dict):
        data = data.get("data", data.get("triggers", []))
    if not isinstance(data, list):
        raise SystemExit("Expected a list of triggers or a {\"data\": [...]} envelope.")
    return data


def schedule_str(r: dict) -> str:
    if r.get("cron_expression"):
        return f"`{r['cron_expression']}` (UTC)"
    if r.get("run_once_at"):
        return f"once @ {r['run_once_at']}"
    return "poke-only"


def main() -> None:
    raw = Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else sys.stdin.read()
    if not raw.strip():
        raise SystemExit("No input. Pipe list_triggers JSON in, or pass a file path.")

    triggers = load(raw)
    ROUTINES_DIR.mkdir(exist_ok=True)

    written: list[tuple[str, dict]] = []
    seen: set[str] = set()
    for t in triggers:
        r = normalize(t)
        slug = slugify(r["name"], r["id"] or "routine")
        # de-dupe slugs
        base, n = slug, 2
        while slug in seen:
            slug, n = f"{base}-{n}", n + 1
        seen.add(slug)
        path = ROUTINES_DIR / f"{slug}.json"
        path.write_text(json.dumps(r, indent=2, ensure_ascii=False) + "\n")
        written.append((slug, r))
        print(f"wrote routines/{slug}.json")

    # Prune backups for routines that no longer exist, so deletions propagate.
    current = {f"{slug}.json" for slug, _ in written}
    for stale in ROUTINES_DIR.glob("*.json"):
        if stale.name not in current:
            stale.unlink()
            print(f"pruned routines/{stale.name} (routine no longer exists)")

    # Regenerate the index table.
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = [
        "# Routines index",
        "",
        f"_Auto-generated by `scripts/format_routines.py`. Last snapshot: {stamp}._",
        "",
        f"{len(written)} routine(s) backed up. Each `.json` file carries a `restore` block that maps",
        "onto a `create_trigger` call — see [README.md](./README.md) to restore one.",
        "",
        "| Routine | Schedule | Enabled | File |",
        "|---|---|---|---|",
    ]
    for slug, r in sorted(written, key=lambda x: x[0]):
        enabled = "yes" if r["enabled"] else "no"
        lines.append(f"| {r['name']} | {schedule_str(r)} | {enabled} | [`{slug}.json`](./{slug}.json) |")
    lines.append("")
    (ROUTINES_DIR / "INDEX.md").write_text("\n".join(lines))
    print(f"wrote routines/INDEX.md ({len(written)} routines)")


if __name__ == "__main__":
    main()
