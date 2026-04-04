# Quick Reference: Research Workflow

## Phase 1 — Ideation

```
1. Edit CLAUDE.md → fill in Topic, Goal, Initial materials
2. Place PDFs in refs/, any starter code in src/
3. > Use ideation agent to brainstorm research directions
4. Ideation agent proposes ≥4 directions, each with:
   - proposal (+ feasibility scorecard)
   - literature check
5. > Use critic agent to review directions/option_X/proposal.md
   (repeat for each direction — critic is a separate agent, not the proposer)
6. Ideation agent writes summary with head-to-head comparisons
7. Agent runs a brainstorm retrospective: "what angles did we miss?"
8. Read directions/summary.md
9. Tell Claude: "Develop direction B" (or "Combine A and C")
```

The ideation agent outputs per direction:
- `directions/option_X/proposal.md` — the direction + feasibility scorecard
- `directions/option_X/literature_check.md` — what existing work says

The critic agent outputs per direction:
- `directions/option_X/criticism.md` — adversarial critique + "what would save this?" for killed directions

The ideation agent then outputs:
- `directions/summary.md` — head-to-head ranked comparison (by win count)

## Phase 2 — Development loop

```
> Use ideation agent to create a plan for direction [X]
→ plan written to notes/plan.md (tasks marked [TODO]/[IN PROGRESS]/[DONE])

For each task in the plan:
  [DERIVE] → Gemini CLI handles math → saved to math/
  [CODE]   → developer agent (Sonnet) → saved to src/
  [VERIFY] → mandatory after [CODE] with numerical results (different method)
  [WRITE]  → developer agent (Sonnet) → saved to report/
  [LIT]    → literature agent → saved to notes/literature_*.md

After each task:
  > Use critic agent to review [file]
  → critic checks literature for all claims BEFORE rating severity
  → issues written to notes/active_criticism.md
  → convergence score appended (FATAL: N, HIGH: N, MEDIUM: N, SMALL: N)

Fix FATAL and HIGH issues before proceeding:
  [DERIVE fix] → pipe revised math to Gemini
  [CODE fix]   → developer agent
  → critic re-reviews → marks resolved [x] → logs in edit_history.md

Repeat until no FATAL/HIGH issues remain.
If FATAL+HIGH not decreasing after 3 cycles → stop and reconsider approach.
```

## Resuming a session

```
1. Read notes/plan.md → find first [TODO] or [IN PROGRESS] task
2. Read notes/active_criticism.md → check open issues + score curve
3. Read notes/edit_history.md → understand what was already done
4. Resume from where you left off
```

## Key commands

```bash
# Download a paper from arxiv
python3 src/scripts/arxiv_download.py 2301.12345

# Derive with Gemini CLI (if available)
cat math/task.md | gemini -p "Derive..."

# Verify math — use the verify-math agent (handles Gemini/Sonnet fallback)
# > Use verify-math agent to verify math/derivation.md
```

## File roles at a glance

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Research context + full instructions |
| `notes/active_criticism.md` | Open issues — check here to see what is currently wrong |
| `notes/edit_history.md` | What was changed and why — append only |
| `notes/plan.md` | Task plan for Phase 2 (created by main session) |
| `math/` | Derivations from Gemini (LaTeX Markdown) |
| `src/` | Python code |
| `report/` | Report sections (Markdown) |
| `refs/` | Downloaded papers |
| `figs/` | Plots |
