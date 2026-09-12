#!/usr/bin/env python3
"""Turn `list_triggers` output into versioned routine backups.

Routines (scheduled triggers) live in Riley's Claude account, not in git. This
script takes the JSON that the claude-code-remote `list_triggers` tool returns
and writes one readable, restorable file per routine into `routines/`, plus a
regenerated table inside `INDEX.md`.

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

Two things this script deliberately does NOT own:

* Files in `routines/` that carry no top-level `restore` key. Those are
  companion state files (e.g. `*-artifact.json`, which hold the stable URL of
  an Artifact a routine writes to). They are never written and never pruned.
* Anything in `INDEX.md` outside the AUTO markers. The generated table is
  spliced between them; hand-written notes above and below survive.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROUTINES_DIR = Path(__file__).resolve().parent.parent / "routines"
INDEX_PATH = ROUTINES_DIR / "INDEX.md"
RETIRED_DIR = ROUTINES_DIR / "retired"

AUTO_BEGIN = "<!-- BEGIN AUTO -->"
AUTO_END = "<!-- END AUTO -->"


def slugify(name: str, fallback: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", (name or "").lower()).strip("-")
    return slug or fallback


def _events(trigger: dict) -> list:
    """The trigger's seed events, across both shapes seen from list_triggers.

    Current shape (2026-09):  trigger["session_request"]["events"]
    Legacy shape:             trigger["job_config"]["ccr"]["events"]
    """
    sr = trigger.get("session_request")
    if isinstance(sr, dict) and isinstance(sr.get("events"), list):
        return sr["events"]
    legacy = trigger.get("job_config", {})
    if isinstance(legacy, dict):
        ccr = legacy.get("ccr", {})
        if isinstance(ccr, dict) and isinstance(ccr.get("events"), list):
            return ccr["events"]
    return []


def _event_message(event: dict) -> dict:
    """The chat message inside one seed event, across both shapes.

    Current: event["payload"]["internal_anthropic_catchall"]["message"]
    Legacy:  event["data"]["message"]
    """
    payload = event.get("payload")
    if isinstance(payload, dict):
        catchall = payload.get("internal_anthropic_catchall")
        if isinstance(catchall, dict) and isinstance(catchall.get("message"), dict):
            return catchall["message"]
    data = event.get("data")
    if isinstance(data, dict) and isinstance(data.get("message"), dict):
        return data["message"]
    return {}


def _prompt(trigger: dict) -> str:
    """The message each firing sends.

    `derived_state.prompt` is a flat copy the control plane now returns and is
    the most reliable source. Fall back to walking the seed events.
    """
    derived = trigger.get("derived_state")
    if isinstance(derived, dict) and derived.get("prompt"):
        return derived["prompt"]
    for ev in _events(trigger):
        msg = _event_message(ev)
        if msg.get("role") == "user" and msg.get("content"):
            return msg["content"]
    return ""


def _is_synthetic(trigger: dict) -> bool:
    for ev in _events(trigger):
        payload = ev.get("payload")
        if isinstance(payload, dict):
            catchall = payload.get("internal_anthropic_catchall")
            if isinstance(catchall, dict) and catchall.get("isSynthetic"):
                return True
        data = ev.get("data")
        if isinstance(data, dict) and data.get("isSynthetic"):
            return True
    return False


def _creates_new_session(trigger: dict) -> bool:
    """True when each firing starts a fresh session.

    `persist_session` is the control plane's own answer and wins when present:
    a persistent-session routine (a self-bind, or an explicit
    `persistent_session_id`) wakes an existing conversation instead. The
    synthetic-message check is the fallback for older payloads.
    """
    if "persist_session" in trigger:
        return not trigger["persist_session"]
    if trigger.get("persistent_session_id"):
        return False
    return _is_synthetic(trigger)


def _notifications(trigger: dict) -> dict | None:
    """Flatten `{"channel": {...}}` to the shape `create_trigger` accepts."""
    n = trigger.get("notifications")
    if not isinstance(n, dict):
        return None
    channel = n.get("channel") if isinstance(n.get("channel"), dict) else n
    out = {k: bool(channel.get(k)) for k in ("push", "email") if k in channel}
    return out or None


def normalize(trigger: dict) -> dict:
    tid = trigger.get("id", "")
    name = trigger.get("name", "") or tid or "unnamed-routine"
    prompt = _prompt(trigger)
    notifications = _notifications(trigger)

    restore = {
        "name": name,
        "prompt": prompt,
        "initiation": "human_request",
    }
    if trigger.get("cron_expression"):
        restore["cron_expression"] = trigger["cron_expression"]
    if trigger.get("run_once_at"):
        restore["run_once_at"] = trigger["run_once_at"]
    if _creates_new_session(trigger):
        restore["create_new_session_on_fire"] = True
    if trigger.get("persistent_session_id"):
        restore["persistent_session_id"] = trigger["persistent_session_id"]
    if notifications is not None:
        restore["notifications"] = notifications

    # Volatile runtime fields (next_run_at, last_fired_at, last_run) are
    # deliberately omitted: they change on every fire, and a backup that
    # churned every run would defeat "only commit when something actually
    # changed". Everything needed to restore a routine is stable.
    return {
        "id": tid,
        "name": name,
        "enabled": trigger.get("enabled", True),
        "cron_expression": trigger.get("cron_expression"),
        "run_once_at": trigger.get("run_once_at"),
        "created_at": trigger.get("created_at"),
        "persist_session": trigger.get("persist_session"),
        "ended_reason": trigger.get("ended_reason") or None,
        "notifications": trigger.get("notifications"),
        "prompt": prompt,
        "restore": restore,
    }


def load(raw: str) -> list[dict]:
    data = json.loads(raw)
    if isinstance(data, dict):
        data = data.get("data", data.get("triggers", []))
    if not isinstance(data, list):
        raise SystemExit('Expected a list of triggers or a {"data": [...]} envelope.')
    return data


def is_routine_backup(path: Path) -> bool:
    """A file this script owns: JSON with a top-level `restore` block.

    Companion state files (`*-artifact.json` and friends) have no `restore`
    key, so they are left alone — pruning one would break the routine whose
    stable Artifact URL it holds.
    """
    try:
        with path.open() as fh:
            doc = json.load(fh)
    except (OSError, json.JSONDecodeError):
        return False
    return isinstance(doc, dict) and "restore" in doc


def existing_backups() -> dict[str, Path]:
    """Map trigger id -> the file already backing it up.

    Filenames are derived from the routine's name, so renaming a routine would
    otherwise orphan its backup and create a second one. Keying on the trigger
    id keeps a routine's file (and its git history) stable across renames.
    """
    found: dict[str, Path] = {}
    for path in sorted(ROUTINES_DIR.glob("*.json")):
        if not is_routine_backup(path):
            continue
        try:
            with path.open() as fh:
                tid = json.load(fh).get("id")
        except (OSError, json.JSONDecodeError):
            continue
        if tid:
            found.setdefault(tid, path)
    return found


def schedule_str(r: dict) -> str:
    if r.get("cron_expression"):
        return f"`{r['cron_expression']}` (UTC)"
    if r.get("run_once_at"):
        return f"once @ {r['run_once_at']}"
    return "poke-only"


def render_table(written: list[tuple[str, dict]], stamp: str) -> str:
    lines = [
        AUTO_BEGIN,
        f"_Table generated by `scripts/format_routines.py`. Last snapshot: {stamp}._",
        "",
        f"{len(written)} routine(s) backed up. Each `.json` carries a `restore` block that maps",
        "onto a `create_trigger` call — see [README.md](./README.md) to restore one.",
        "",
        "| Routine | Schedule | Enabled | File |",
        "|---|---|---|---|",
    ]
    for slug, r in sorted(written, key=lambda x: x[0]):
        enabled = "yes" if r["enabled"] else "no"
        lines.append(
            f"| {r['name']} | {schedule_str(r)} | {enabled} | [`{slug}.json`](./{slug}.json) |"
        )
    lines += ["", AUTO_END]
    return "\n".join(lines)


def splice_index(table: str) -> str:
    """Replace the AUTO block in INDEX.md, preserving everything around it."""
    if INDEX_PATH.exists():
        existing = INDEX_PATH.read_text()
        if AUTO_BEGIN in existing and AUTO_END in existing:
            head, rest = existing.split(AUTO_BEGIN, 1)
            _, tail = rest.split(AUTO_END, 1)
            return head + table + tail
        # No markers yet: keep the hand-written file and append the block, so
        # a first run after this change never destroys existing notes.
        return existing.rstrip() + "\n\n" + table + "\n"
    return "# Routines index\n\n" + table + "\n"


def main() -> None:
    raw = Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else sys.stdin.read()
    if not raw.strip():
        raise SystemExit("No input. Pipe list_triggers JSON in, or pass a file path.")

    triggers = load(raw)
    ROUTINES_DIR.mkdir(exist_ok=True)

    known = existing_backups()

    written: list[tuple[str, dict]] = []
    seen: set[str] = set()
    for t in triggers:
        r = normalize(t)
        prior = known.get(r["id"])
        if prior is not None:
            slug = prior.stem
        else:
            slug = slugify(r["name"], r["id"] or "routine")
            base, n = slug, 2
            while slug in seen or (ROUTINES_DIR / f"{slug}.json") in known.values():
                slug, n = f"{base}-{n}", n + 1
        seen.add(slug)
        path = ROUTINES_DIR / f"{slug}.json"
        path.write_text(json.dumps(r, indent=2, ensure_ascii=False) + "\n")
        written.append((slug, r))
        print(f"wrote routines/{slug}.json")

    # Retire backups for routines that no longer exist, so deletions propagate
    # without destroying a restore block someone may still want. Only files
    # this script owns are eligible — see is_routine_backup().
    current = {f"{slug}.json" for slug, _ in written}
    for stale in sorted(ROUTINES_DIR.glob("*.json")):
        if stale.name in current:
            continue
        if not is_routine_backup(stale):
            print(f"kept routines/{stale.name} (not a routine backup)")
            continue
        RETIRED_DIR.mkdir(exist_ok=True)
        stale.replace(RETIRED_DIR / stale.name)
        print(f"retired routines/{stale.name} -> retired/ (routine no longer on the account)")

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    INDEX_PATH.write_text(splice_index(render_table(written, stamp)))
    print(f"wrote routines/INDEX.md ({len(written)} routines)")


if __name__ == "__main__":
    main()
