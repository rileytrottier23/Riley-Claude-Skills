#!/usr/bin/env python3
"""Keep a Riley skills repo's README and marketplace.json honest after a skill lands.

Works on any of the three skill repos, which all share the same layout:

    <repo>/
      .claude-plugin/marketplace.json   plugins, each pointing at ./mine/ or ./vendored/<collection>/
      README.md                          a "## My skills (`mine/`)" table + a "## Vendored ..." table
      CHANGELOG.md                       newest first
      mine/<skill>/SKILL.md              Riley's own skills
      vendored/<collection>/**/SKILL.md  vendored collections, each with its own LICENSE

Usage:
    python3 update_readme.py <repo-root> [--added mine/my-skill]
                            [--added vendored/anthropic/foo]
                            [--updated mine/chess-coach]
                            [--desc "one-line description for the README table"]
                            [--bump patch|minor|major] [--check]

What it maintains:
  * skill counts   - the "N skills installable" line, the plugin table's Skills column,
                     the plugin-count word, and each vendored collection's count
  * mine table     - appends a row for a new mine/ skill under "## My skills (`mine/`)"
  * CHANGELOG.md   - one dated line per run, newest first
  * marketplace.json - optional version bump

It never rewrites rows it did not add, and reports drift rather than silently "fixing" it.
--check reports without writing. Descriptions for vendored collections are hand-written; a new
vendored *collection* needs its table row and a new marketplace plugin entry added by hand.
"""
import argparse
import datetime as dt
import json
import pathlib
import re
import sys

MINE_HEADING = "## My skills (`mine/`)"
NUMBER_WORDS = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five",
                6: "Six", 7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten"}

problems = []


def warn(msg):
    problems.append(msg)
    print(f"  ! {msg}", file=sys.stderr)


def parse_frontmatter(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return {}
    out, key = {}, None
    for line in m.group(1).split("\n"):
        km = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if km:
            key = km.group(1)
            out[key] = km.group(2).strip()
        elif key and line.strip():
            out[key] = (out[key] + " " + line.strip()).strip()
    for k, v in out.items():
        if len(v) > 1 and v[0] == v[-1] and v[0] in "\"'":
            out[k] = v[1:-1]
    return out


def mine_dirs(repo):
    root = repo / "mine"
    if not root.is_dir():
        return []
    return sorted(d for d in root.iterdir() if d.is_dir() and (d / "SKILL.md").is_file())


def count_skills(root):
    return len(list(root.rglob("SKILL.md"))) if root.is_dir() else 0


def load_marketplace(repo):
    path = repo / ".claude-plugin" / "marketplace.json"
    if not path.is_file():
        warn("no .claude-plugin/marketplace.json — plugin table left untouched")
        return path, None
    return path, json.loads(path.read_text(encoding="utf-8"))


def plugin_counts(repo, market):
    counts = {}
    for p in (market or {}).get("plugins", []):
        total = 0
        for rel in p.get("skills", []):
            root = (repo / rel.lstrip("./")).resolve()
            if not root.is_dir():
                warn(f"plugin '{p['name']}' points at missing path {rel}")
                continue
            total += count_skills(root)
        counts[p["name"]] = total
    return counts


def table_bounds(lines, heading):
    try:
        h = next(i for i, l in enumerate(lines) if l.strip() == heading)
    except StopIteration:
        return None
    i = h + 1
    while i < len(lines) and not lines[i].lstrip().startswith("|"):
        if lines[i].startswith("## "):
            return None
        i += 1
    if i >= len(lines):
        return None
    start = i
    while i < len(lines) and lines[i].lstrip().startswith("|"):
        i += 1
    return start, i


def row_slugs(lines):
    return {m.group(1).rstrip("/").split("/")[-1]
            for l in lines for m in re.finditer(r"\]\((\./[^)]+)\)", l)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo")
    ap.add_argument("--added", action="append", default=[], metavar="mine/NAME | vendored/COLL/NAME")
    ap.add_argument("--updated", action="append", default=[], metavar="PATH")
    ap.add_argument("--desc", action="append", default=[],
                    help="README table description, in the same order as --added")
    ap.add_argument("--bump", choices=["patch", "minor", "major"])
    ap.add_argument("--check", action="store_true", help="report drift, write nothing")
    ap.add_argument("--date", default=dt.date.today().isoformat())
    args = ap.parse_args()

    repo = pathlib.Path(args.repo).expanduser().resolve()
    readme = repo / "README.md"
    if not readme.is_file():
        print("No README.md at repo root — wrong path?", file=sys.stderr)
        return 1

    text = readme.read_text(encoding="utf-8")
    mpath, market = load_marketplace(repo)
    counts = plugin_counts(repo, market)
    total = sum(counts.values())

    # --- 1. counts ------------------------------------------------------
    text, n = re.subn(r"—\s*\d+\s+skills installable", f"— {total} skills installable", text)
    if not n:
        warn('could not find the "N skills installable" line')

    for name, c in counts.items():
        text, n = re.subn(rf"(\|\s*`{re.escape(name)}`\s*\|\s*)\d+(\s*\|)", rf"\g<1>{c}\g<2>", text)
        if not n:
            warn(f"plugin '{name}' has no row in the README plugin table")

    word = NUMBER_WORDS.get(len(counts), str(len(counts)))
    text = re.sub(r"^(One|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten|\d+) plugins,",
                  f"{word} plugins,", text, flags=re.M)

    # vendored collection counts (rows like: | [anthropic](./vendored/anthropic) | Author | N | License |)
    vroot = repo / "vendored"
    if vroot.is_dir():
        for coll in sorted(d for d in vroot.iterdir() if d.is_dir()):
            c = count_skills(coll)
            pat = rf"(\[{re.escape(coll.name)}\]\([^)]*\)\s*\|[^|]*\|\s*)([^|]*?)(\s*\|)"

            def sub(m):
                note = m.group(2)
                extra = note[note.index("("):] if "(" in note else ""
                return m.group(1) + (f"{c} {extra}".strip()) + m.group(3)

            text = re.sub(pat, sub, text)

    # --- 2. mine table --------------------------------------------------
    descs = dict(zip(args.added, args.desc))
    lines = text.split("\n")
    found = {d.name for d in mine_dirs(repo)}
    bounds = table_bounds(lines, MINE_HEADING)
    if bounds:
        start, end = bounds
        listed = row_slugs(lines[start:end])
        for missing in sorted(listed - found):
            warn(f"{MINE_HEADING}: '{missing}' is in the README but not on disk")
        for new in sorted(found - listed):
            key = f"mine/{new}"
            desc = descs.get(key) or parse_frontmatter(repo / "mine" / new / "SKILL.md").get("description", "")
            desc = re.sub(r"\s+", " ", desc).replace("|", "\\|").strip()
            if len(desc) > 200:
                desc = desc[:197].rstrip() + "..."
            if not desc:
                warn(f"{key} has no description — README row will be thin")
            row = f"| [{new}](./mine/{new}) | {desc} |"
            lines.insert(end, row)
            end += 1
            print(f"  + {MINE_HEADING}: added row for {new}")
    elif found:
        warn(f"no table under '{MINE_HEADING}' — add rows for {sorted(found)} by hand")
    text = "\n".join(lines)

    # --- 3. write -------------------------------------------------------
    entries = ([f"Added `{n}`" for n in args.added] +
               [f"Updated `{n}`" for n in args.updated])
    if args.check:
        print(f"check only — {total} skills across {len(counts)} plugins; {len(problems)} problem(s)")
        return 1 if problems else 0

    readme.write_text(text, encoding="utf-8")

    if entries:
        chpath = repo / "CHANGELOG.md"
        head = "# Changelog\n\nNewest first.\n\n"
        body = chpath.read_text(encoding="utf-8") if chpath.is_file() else head
        if not body.startswith("# Changelog"):
            body = head + body
        line = f"- {args.date} — " + ", ".join(entries) + f". {total} skills total.\n"
        marker = "Newest first.\n\n"
        idx = body.find(marker)
        body = (body[:idx + len(marker)] + line + body[idx + len(marker):]) if idx >= 0 else body + line
        chpath.write_text(body, encoding="utf-8")
        print(f"  + CHANGELOG.md: {line.strip()}")

    if args.bump and market:
        raw = mpath.read_text(encoding="utf-8")
        cur = market.get("metadata", {}).get("version", "0.0.0")
        v = [int(x) for x in (cur.split(".") + ["0", "0", "0"])[:3]]
        i = {"major": 0, "minor": 1, "patch": 2}[args.bump]
        v[i] += 1
        for j in range(i + 1, 3):
            v[j] = 0
        nxt = ".".join(str(x) for x in v)
        raw2, n = re.subn(rf'("version"\s*:\s*)"{re.escape(cur)}"', rf'\g<1>"{nxt}"', raw, count=1)
        if n:
            mpath.write_text(raw2, encoding="utf-8")
            print(f"  + marketplace.json version -> {nxt}")
        else:
            warn("could not bump marketplace.json version — edit it by hand")

    print(f"README updated: {total} skills across {len(counts)} plugins")
    if problems:
        print(f"{len(problems)} thing(s) need a human look — see the ! lines above")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
