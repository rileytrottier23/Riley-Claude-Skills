#!/usr/bin/env bash
# Sync Riley's global Claude learnings onto this Mac/Linux machine, then keep them synced.
#
# One-time setup — paste this single line into a terminal:
#   curl -fsSL https://raw.githubusercontent.com/rileytrottier23/Riley-Claude-Skills/main/scripts/sync-claude-setup.sh | bash
#
# Same behaviour as sync-claude-setup.ps1 (the Windows version):
#   1. Replaces the "## Learnings" section of ~/.claude/CLAUDE.md with the one in
#      config/global-learnings.md on GitHub (the repo is the source of truth).
#   2. Saves a copy of this script to ~/.claude/scripts/ and registers it as a
#      Claude Code SessionStart hook in ~/.claude/settings.json (needs python3).
#
# --hook mode prints nothing and always exits 0, so it can't block a session.
# Test overrides: RILEY_SYNC_LEARNINGS_SRC / RILEY_SYNC_SCRIPT_SRC may be a URL or a local path.

HOOK=0
[ "${1:-}" = "--hook" ] && HOOK=1

RAW_BASE="https://raw.githubusercontent.com/rileytrottier23/Riley-Claude-Skills/main"
LEARNINGS_SRC="${RILEY_SYNC_LEARNINGS_SRC:-$RAW_BASE/config/global-learnings.md}"
SCRIPT_SRC="${RILEY_SYNC_SCRIPT_SRC:-$RAW_BASE/scripts/sync-claude-setup.sh}"

CLAUDE_DIR="$HOME/.claude"
CLAUDE_MD="$CLAUDE_DIR/CLAUDE.md"
SETTINGS="$CLAUDE_DIR/settings.json"
LOCAL_SCRIPT="$CLAUDE_DIR/scripts/sync-claude-setup.sh"

say() { [ "$HOOK" = 1 ] || echo "$*"; }

read_source() {
  case "$1" in
    http://*|https://*) curl -fsSL "$1" ;;
    *) cat "$1" ;;
  esac
}

sync_learnings() {
  local src block tmp
  src="$(read_source "$LEARNINGS_SRC")" || { say "Sync failed: couldn't read $LEARNINGS_SRC"; return 1; }

  # Entries under "## Learnings", up to the next level-1/2 heading, minus the empty placeholder.
  block="$(printf '%s\n' "$src" | awk '
    /^[[:space:]]*## Learnings[[:space:]]*$/ { on=1; next }
    on && /^##? / { exit }
    on && /^[[:space:]]*\*\(empty/ { next }
    on { print }
  ' | sed -e '/./,$!d' | sed -e ':a' -e '/^\n*$/{$d;N;ba' -e '}')"
  if [ -z "$(printf '%s' "$block" | tr -d '[:space:]')" ]; then say "Learnings: nothing to sync yet."; return 0; fi

  mkdir -p "$CLAUDE_DIR"; touch "$CLAUDE_MD"
  tmp="$(mktemp)"
  BLOCK="$block" awk '
    BEGIN { blk = "## Learnings\n\n" ENVIRON["BLOCK"] }
    /^[[:space:]]*## Learnings[[:space:]]*$/ && !done { print blk; skip=1; done=1; next }
    skip && /^##? / { skip=0; print "" }
    !skip { print }
    END { if (!done) { if (NR > 0) print ""; print blk } }
  ' "$CLAUDE_MD" | sed -e ':a' -e '/^\n*$/{$d;N;ba' -e '}' > "$tmp"

  if cmp -s "$tmp" "$CLAUDE_MD"; then rm -f "$tmp"; say "Learnings: already up to date."
  else mv "$tmp" "$CLAUDE_MD"; say "Learnings: updated $CLAUDE_MD"; fi
}

install_hook() {
  mkdir -p "$(dirname "$LOCAL_SCRIPT")"
  read_source "$SCRIPT_SRC" > "$LOCAL_SCRIPT.tmp" && mv "$LOCAL_SCRIPT.tmp" "$LOCAL_SCRIPT" && chmod +x "$LOCAL_SCRIPT" \
    || { say "Auto-sync: skipped - couldn't save the script locally."; return 0; }
  command -v python3 >/dev/null || { say "Auto-sync: skipped - needs python3."; return 0; }

  SETTINGS="$SETTINGS" CMD="bash \"$LOCAL_SCRIPT\" --hook" python3 - <<'PY'
import json, os, shutil
path, cmd = os.environ["SETTINGS"], os.environ["CMD"]
raw = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
try:
    cfg = json.loads(raw) if raw.strip() else {}
except ValueError:
    print(f"Auto-sync: skipped - {path} isn't plain JSON, so it was left untouched."); raise SystemExit
groups = cfg.setdefault("hooks", {}).setdefault("SessionStart", [])
if any("sync-claude-setup" in h.get("command", "") for g in groups for h in g.get("hooks", [])):
    print("Auto-sync: already on."); raise SystemExit
groups.append({"hooks": [{"type": "command", "command": cmd}]})
if raw.strip():
    shutil.copyfile(path, path + ".bak")
with open(path, "w", encoding="utf-8") as f:
    json.dump(cfg, f, indent=2); f.write("\n")
print("Auto-sync: on. Every new Claude Code session on this machine re-syncs your learnings.")
PY
}

if [ "$HOOK" = 1 ]; then
  sync_learnings >/dev/null 2>&1
  exit 0
fi
sync_learnings && install_hook && say "Done."
