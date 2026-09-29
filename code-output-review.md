# Claude Code output review

_29 Sep 2026. Covers 31 sessions from 16 Aug to 26 Sep._

**Sources:** `~/.claude/projects/` holds only the current session, because each cloud container starts fresh. This review therefore draws on three other sources: the account's session list (titles plus Claude's end-of-turn summaries), 11 PR descriptions and comments in this repo, and the commit history. None of these include your messages word for word, so section 4 is inferred and section 5 is estimated.

## 1. Sessions reviewed: 31

| Type | Count | Examples |
|---|---|---|
| Building | 9 | skills, cheat sheet, app UI, chess tool, API integration |
| Setup / config | 7 | MCP servers, domain migration, skills setup |
| Debugging | 6 | plugin manifest conflicts (4 sessions on one night), repo failure |
| Research | 1 | whether a banking MCP exists |
| Other | 8 | task planning (3), 4 empty or abandoned |

## 2. Most common final replies

1. **"Your turn" handoff:** blocked on a manual step you have to do, such as creating repos, pasting a prompt into Cowork, testing an email, or running a slash command. This appears in about 7 sessions.
2. **Done-and-verified recap:** lists what changed and how it was checked.
3. **PR write-up:** a Summary, Changes, Notes and Test plan, often 300 to 450 words.
4. **Recommendation:** a verdict first, then a caveat.
5. **Walkthrough:** numbered steps for an install or setup.

## 3. Where replies were hardest to read

- **Decisions buried at the end.** Two PR write-ups saved the real questions ("want a routine for this?", "should this skill move?") for a final "Notes / open questions" section.
- **Walls of text.** One PR had a design-notes section that was a single paragraph of about 150 words covering four separate trade-offs.
- **IDs mixed into prose.** Full 40-character commit hashes, repo paths and internal IDs sat inside sentences instead of in code blocks or a table.
- **Handoffs that point back up the page.** Replies such as "paste the prompt above" made you scroll up to find the thing you had to do.
- **Long recaps.** The single longest session produced about 640k output tokens. Its final ask (create 3 repos) came after long progress reports.

## 4. Pushback on length or format (inferred)

- You had Claude build a skill for short status updates: result first, action items only, no filler.
- You added three more anti-verbosity skills: Strunk's rules, avoid-ai-writing and antislop.
- You asked for every skill in one table instead of spread across four READMEs.
- You narrowed a cleanup: fix the settings but leave the folders alone.
- You started four separate sessions for one plugin error in about 20 minutes, which suggests replies weren't getting to the fix fast enough.
- This review itself.

## 5. Task lists vs. multi-step work (estimated)

- **Sessions with 3 or more steps:** about 20 of the 27 that weren't empty.
- **Visible task or progress list:** can't be measured from summaries. The PRs show 2 test-plan checklists across 11 PR write-ups, and none show a progress checklist.
- **Takeaway:** checklists were rare and appeared only at the end, never as a running status.

## 6. Formats you responded well to

| Format | Signal |
|---|---|
| **Artifacts / dashboards** | You kept iterating on the daily dashboard: installed it as an app, renamed it, added a weekly review. The weekly chess review was pinned to a stable URL. |
| **Tables** | You asked for the skills cheat sheet as one table. The PRs with a gap/fix table got merged. |
| **One-line "needs action" status** | Most summaries fit on one line, e.g. "Clerk removed, Resend live; need password-reset test". |
| **Numbered steps** | Install walkthroughs finished without follow-up questions. |

**Suggested defaults:** start with the decision or your next action. Put IDs and commands in code blocks. Keep recaps to a 3-row table or less. Offer an artifact for anything longer than a screen.
