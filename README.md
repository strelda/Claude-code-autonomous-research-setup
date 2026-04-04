# Quick Reference: Research Workflow

## Phase 1 — Ideation

```
1. Edit CLAUDE.md → fill in Topic, Goal, Initial materials
2. Place PDFs in refs/, any starter code in src/
3. > Use ideation agent to brainstorm research directions
4. Read directions/summary.md
5. Tell Claude: "Develop direction B" (or "Combine A and C")
```

The ideation agent outputs per direction:
- `directions/option_X/proposal.md` — the direction
- `directions/option_X/literature_check.md` — what existing work says
- `directions/option_X/criticism.md` — adversarial self-critique
- `directions/summary.md` — ranked comparison

## Phase 2 — Development loop

```
> Use ideation agent to create a plan for direction [X]
→ plan written to notes/plan.md

For each task in the plan:
  [DERIVE] → Gemini CLI handles math → saved to math/
  [CODE]   → developer agent (Sonnet) → saved to src/
  [WRITE]  → developer agent (Sonnet) → saved to report/
  [LIT]    → literature agent → saved to notes/literature_*.md

After each task:
  > Use critic agent to review [file]
  → issues written to notes/active_criticism.md

Fix FATAL and HIGH issues before proceeding:
  [DERIVE fix] → pipe revised math to Gemini
  [CODE fix]   → developer agent
  → critic re-reviews → marks resolved [x] → logs in edit_history.md

Repeat until no FATAL/HIGH issues remain.
```

## Key commands

```bash
# Download a paper from arxiv
python3 src/scripts/arxiv_download.py 2301.12345

# Send a file to Gemini for math verification
cat math/derivation.md | bash src/scripts/gemini_check.sh -

# Custom question to Gemini
bash src/scripts/gemini_check.sh math/derivation.md "Check the second-order term."
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
