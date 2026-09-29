# Sync Riley's global Claude learnings onto this Windows machine, then keep them synced.
#
# One-time setup — paste this single line into PowerShell:
#   irm https://raw.githubusercontent.com/rileytrottier23/Riley-Claude-Skills/main/scripts/sync-claude-setup.ps1 | iex
#
# What it does (safe to re-run; it only changes what's out of date):
#   1. Replaces the "## Learnings" section of ~/.claude/CLAUDE.md with the one in
#      config/global-learnings.md on GitHub (the repo is the source of truth).
#   2. Saves a copy of this script to ~/.claude/scripts/ and registers it as a
#      Claude Code SessionStart hook in ~/.claude/settings.json, so every new local
#      session re-syncs on its own. No further manual steps.
#
# Hook mode (-Hook) prints nothing and never fails, so it can't block a session.
# Test overrides: $env:RILEY_SYNC_LEARNINGS_SRC / $env:RILEY_SYNC_SCRIPT_SRC may be a URL or a local path.

param([switch]$Hook)

$ErrorActionPreference = 'Stop'
$RawBase = 'https://raw.githubusercontent.com/rileytrottier23/Riley-Claude-Skills/main'
$LearningsSrc = if ($env:RILEY_SYNC_LEARNINGS_SRC) { $env:RILEY_SYNC_LEARNINGS_SRC } else { "$RawBase/config/global-learnings.md" }
$ScriptSrc = if ($env:RILEY_SYNC_SCRIPT_SRC) { $env:RILEY_SYNC_SCRIPT_SRC } else { "$RawBase/scripts/sync-claude-setup.ps1" }

$ClaudeDir = Join-Path $HOME '.claude'
$ClaudeMd = Join-Path $ClaudeDir 'CLAUDE.md'
$Settings = Join-Path $ClaudeDir 'settings.json'
$LocalScript = Join-Path (Join-Path $ClaudeDir 'scripts') 'sync-claude-setup.ps1'
$Utf8NoBom = New-Object System.Text.UTF8Encoding $false

function Say($msg) { if (-not $Hook) { Write-Host $msg } }

function Read-Source($src) {
    if ($src -match '^https?://') {
        [Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12
        return (Invoke-WebRequest -UseBasicParsing -Uri $src).Content
    }
    return [IO.File]::ReadAllText($src)
}

function Write-Text($path, $text) { [IO.File]::WriteAllText($path, $text, $Utf8NoBom) }

function Get-LearningsBlock($markdown) {
    $lines = @($markdown -split "\r?\n")
    $start = -1
    for ($i = 0; $i -lt $lines.Count; $i++) { if ($lines[$i].Trim() -eq '## Learnings') { $start = $i; break } }
    if ($start -lt 0) { return $null }
    $entries = @()
    for ($i = $start + 1; $i -lt $lines.Count; $i++) {
        if ($lines[$i] -match '^#{1,2} ') { break }
        if ($lines[$i] -match '^\s*\*\(empty') { continue }
        $entries += $lines[$i]
    }
    $entries = @(($entries -join "`n").Trim() -split "`n" | Where-Object { $_ -ne $null })
    if (($entries -join '').Trim() -eq '') { return $null }
    return @('## Learnings', '') + $entries
}

function Sync-Learnings {
    $block = Get-LearningsBlock (Read-Source $LearningsSrc)
    if (-not $block) { Say 'Learnings: nothing to sync yet.'; return }

    $old = if (Test-Path $ClaudeMd) { [IO.File]::ReadAllText($ClaudeMd) } else { '' }
    $lines = if ($old) { @($old -split "\r?\n") } else { @() }
    $start = -1
    for ($i = 0; $i -lt $lines.Count; $i++) { if ($lines[$i].Trim() -eq '## Learnings') { $start = $i; break } }

    if ($start -ge 0) {
        $end = $lines.Count
        for ($i = $start + 1; $i -lt $lines.Count; $i++) { if ($lines[$i] -match '^#{1,2} ') { $end = $i; break } }
        $before = if ($start -gt 0) { $lines[0..($start - 1)] } else { @() }
        $after = if ($end -lt $lines.Count) { @('') + $lines[$end..($lines.Count - 1)] } else { @() }
        $new = (@($before) + $block + @($after)) -join "`n"
    } else {
        $prefix = $old.TrimEnd()
        $new = if ($prefix) { $prefix + "`n`n" + ($block -join "`n") } else { $block -join "`n" }
    }
    $new = $new.TrimEnd() + "`n"

    if ($new -eq $old) { Say 'Learnings: already up to date.'; return }
    Write-Text $ClaudeMd $new
    Say "Learnings: updated $ClaudeMd"
}

function Install-Hook {
    New-Item -ItemType Directory -Force (Split-Path $LocalScript) | Out-Null
    Write-Text $LocalScript (Read-Source $ScriptSrc)

    $cmd = 'powershell -NoProfile -ExecutionPolicy Bypass -File "' + ($LocalScript -replace '\\', '/') + '" -Hook'
    $raw = if (Test-Path $Settings) { [IO.File]::ReadAllText($Settings) } else { '' }
    try {
        $cfg = if ($raw.Trim()) { $raw | ConvertFrom-Json } else { New-Object PSObject }
    } catch {
        Say "Auto-sync: skipped - $Settings isn't plain JSON, so it was left untouched."
        return
    }

    if (-not $cfg.PSObject.Properties['hooks']) { $cfg | Add-Member -NotePropertyName hooks -NotePropertyValue (New-Object PSObject) }
    if (-not $cfg.hooks.PSObject.Properties['SessionStart']) { $cfg.hooks | Add-Member -NotePropertyName SessionStart -NotePropertyValue @() }

    foreach ($group in @($cfg.hooks.SessionStart)) {
        foreach ($h in @($group.hooks)) {
            if ($h.command -like '*sync-claude-setup*') { Say 'Auto-sync: already on.'; return }
        }
    }

    $entry = New-Object PSObject -Property @{ hooks = @((New-Object PSObject -Property @{ type = 'command'; command = $cmd })) }
    $cfg.hooks.SessionStart = @($cfg.hooks.SessionStart) + @($entry)
    if ($raw.Trim()) { Copy-Item $Settings "$Settings.bak" -Force }
    # Windows PowerShell 5.1 can serialize arrays as {"value":[...],"Count":n}; this is the standard fix.
    if ($PSVersionTable.PSVersion.Major -lt 6) { Remove-TypeData System.Array -ErrorAction SilentlyContinue }
    Write-Text $Settings (($cfg | ConvertTo-Json -Depth 32) + "`n")
    Say 'Auto-sync: on. Every new Claude Code session on this machine re-syncs your learnings.'
}

try {
    New-Item -ItemType Directory -Force $ClaudeDir | Out-Null
    Sync-Learnings
    if (-not $Hook) { Install-Hook; Say 'Done.' }
} catch {
    if (-not $Hook) { Write-Host "Sync failed: $($_.Exception.Message)" -ForegroundColor Red }
}
