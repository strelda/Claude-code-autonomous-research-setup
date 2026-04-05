# CLAUDE.md — Research Project Instructions

## Research Context

**Topic:** [FILL IN — e.g., "Thermalization dynamics in periodically driven quantum spin chains"]

**Goal:** [FILL IN — e.g., "Analytical derivation of heating rates with numerical verification"]

**Initial materials:** [FILL IN — list any papers in refs/ or code in src/ you are starting with]

---

## Project Structure

```
.
├── CLAUDE.md               # This file — research context and workflow instructions
├── README.md               # Quick-reference workflow guide
├── directions/             # Phase 1 output — one subfolder per brainstormed direction
│   ├── option_A/
│   │   ├── proposal.md         # The direction described (includes feasibility scorecard) — by ideation agent
│   │   ├── literature_check.md # What existing work says about it — by ideation agent
│   │   └── criticism.md        # Adversarial critique (+ "what would save this?") — by critic agent (separate instance)
│   └── summary.md          # Head-to-head ranked comparison — by ideation agent after critic reviews
├── math/                   # Derivations (LaTeX Markdown, produced by Gemini)
├── src/                    # Python code (NumPy/SciPy/SymPy)
│   └── scripts/
│       └── arxiv_download.py   # Download PDFs from arxiv
├── notes/
│   ├── active_criticism.md     # Open issues (FATAL/HIGH/MEDIUM/SMALL) with unique IDs
│   ├── edit_history.md         # Append-only log of all changes and fixes
│   └── plan.md                 # (Created during Phase 2) Task plan for chosen direction
├── refs/                   # Reference PDFs (downloaded or user-provided)
├── figs/                   # Figures and plots (saved by code)
└── report/                 # Final report sections (Markdown)
```

---

## Workflow

### Phase 1 — Ideation

1. Fill in the Research Context above. Place any initial PDFs in `refs/`, code in `src/`.
2. Invoke the ideation agent: `Use ideation agent to brainstorm directions for this research question`
3. The ideation agent will:
   - Search the literature via Scite MCP
   - Propose **at least 4** directions in `directions/option_X/` (3 is too few — aim for 5)
   - Generate roughly half the directions with Claude Opus and half via Gemini CLI (pinned to `gemini-3.1-pro-preview`)
   - Think about each idea separately and write candid notes to `directions/option_X/my_notes.md`
   - Perform a **literature reality check** per direction (has it been done? contradicted? trivial?)
   - Cross-check with Gemini (Gemini CLI pinned to `gemini-3.1-pro-preview`)
   - For each direction, include a **feasibility scorecard**:
     - Mathematical difficulty (1-10)
     - Computational cost (1-10)
     - Expected time to first result (weeks)
     - Probability of meaningful result (%)
   - For killed directions, include a **"What would save this?"** section documenting what would need to change for the direction to survive — prevents revisiting the same dead ends
4. **Brainstorm retrospective:** After initial directions are proposed, the agent does a second pass: "Given the directions we proposed, what other angles did we miss?" This guards against tunnel vision from the initial literature search framing.
5. Invoke the **critic agent** to adversarially review each direction: `Use critic agent to review directions/option_X/proposal.md`. The critic — a separate Opus instance with no ownership of the ideas — writes `directions/option_X/criticism.md`. This separation prevents the proposer from going easy on its own ideas.
6. The ideation agent then writes `directions/summary.md` with **head-to-head comparisons**: every pair of surviving directions is compared directly ("Given A and B, which has a stronger testable prediction and fewer fatal assumptions?"). Directions are ranked by win count, not subjective ordering.
7. Read `directions/summary.md`. Read individual `proposal.md` and `criticism.md` files as needed.
8. Tell Claude which direction to develop (or combine elements from multiple).
9. If none of the directions looks good enough, explicitly decide whether to iterate:
   - Claude should ask: "Do you want me to run the ideation agent again (using what we learned from `directions/summary.md`) to generate new directions?"
10. If you choose to iterate, rerun the ideation agent (step 2), then rerun the critic for the new directions, and have the ideation agent update `directions/summary.md` to incorporate the new candidates.

### Phase 2 — Development

1. The main session (Opus) reads the chosen direction and writes `notes/plan.md` with numbered tasks. Each task is marked `[TODO]`, `[IN PROGRESS]`, or `[DONE]`.
2. Tasks are dispatched by type:
   - **`[DERIVE]`** → Gemini CLI. The main session pipes a task prompt to Gemini, saves output to `math/`.
   - **`[CODE]`** → `developer` agent (Sonnet). Implements in `src/`. Must be runnable and tested.
   - **`[VERIFY]`** → Mandatory after any `[CODE]` task that produces a numerical result. Runs the same computation a different way (analytical limit, independent implementation, or parameter sweep). The critic agent flags any numerical result without a corresponding `[VERIFY]` as HIGH.
   - **`[WRITE]`** → `developer` agent (Sonnet). Drafts report sections in `report/`.
   - **`[LIT]`** → `literature` agent. Searches for and verifies claims against published work.
3. After each piece of work, the `critic` agent reviews it (writes to `notes/active_criticism.md`). The critic **automatically invokes the literature agent** for any non-trivial quantitative claim before rating it — literature verification is in-the-loop, not optional.
4. The criticism loop runs until no FATAL or HIGH issues remain:
   ```
   work produced → critic reviews (with literature checks) → issues logged
   → fixes dispatched → critic re-reviews → issues marked resolved → repeat
   ```
5. **Convergence tracking:** After each critic pass, a score line is appended to `notes/active_criticism.md`:
   ```
   ## Score: [date] — FATAL: N, HIGH: N, MEDIUM: N, SMALL: N
   ```
   If FATAL+HIGH is not monotonically decreasing after 3 cycles, stop and reconsider the approach — the current direction may have a structural problem.
6. All changes are logged in `notes/edit_history.md`.

### Resuming a Session

When resuming Phase 2 after a session break:
1. Read `notes/plan.md` — check task statuses (`[TODO]`, `[IN PROGRESS]`, `[DONE]`).
2. Read `notes/active_criticism.md` — check open issues and the score curve.
3. Read `notes/edit_history.md` — understand what was already done.
4. Resume from the first `[TODO]` or `[IN PROGRESS]` task. Any `[IN PROGRESS]` task should be re-evaluated — it may be partially complete.

---

## Agents

| Agent | Model | Role |
|-------|-------|------|
| `ideation` | Opus | Brainstorm + literature check research directions, hand off to critic, write ranked summary |
| `critic` | Opus | Hostile referee. Finds real flaws. Literature-in-the-loop. Dispatches verify-math. |
| `verify-math` | Sonnet | Cross-model math verification. Tries Gemini, falls back to independent Sonnet check. |
| `developer` | Sonnet | Code (src/) and writing (report/) tasks only |
| `literature` | Sonnet | Search Scite/bioRxiv, download arxiv papers |

---

## External Tools

**Gemini CLI** (primary derivation engine):
```bash
cat math/task.md | gemini -m gemini-3.1-pro-preview -p "Derive..."
```
- Gemini is strong at mathematics and cheap — use it freely.
- One self-contained prompt per call. No multi-turn. If a derivation is too long for one prompt, break it into independent steps.
- **Fallback:** If Gemini CLI is not available, use a `developer` agent (Sonnet) for derivations instead.

**`verify-math` agent** (cross-model math verification):
- Dispatched to verify any derivation or mathematical claim.
- Tries Gemini CLI first, falls back to independent Sonnet verification.
- Returns structured report: dimensional consistency, signs, limiting cases, approximations.
- Use instead of calling Gemini directly for verification — handles fallback automatically.

**Scite MCP** (`search_literature`):
- Peer-reviewed papers with Smart Citations (actual quoted text).
- Use to verify claims, find related work, check novelty.

**bioRxiv MCP** (`search_preprints`):
- Recent preprints not yet in journals.

**Arxiv download**:
```bash
python3 src/scripts/arxiv_download.py 2301.12345
python3 src/scripts/arxiv_download.py https://arxiv.org/abs/2301.12345
```
Saves PDF to `refs/`.

---

## Observability

**aleksblago/claude-code-observability** for live session debugging. Reads native Claude Code session files — shows prompts, tool I/O, agent swim lanes, HITL alerts.

```bash
# From cloned repo at /tmp/claude-code-observability
./manage.sh start-detached   # dashboard: http://localhost:52871
./manage.sh stop
```

Hooks must be configured via `./setup.sh` — adds PreToolUse, PostToolUse, Stop, SubagentStop to `~/.claude/settings.json`.

**ADR:** See `docs/ADR/001-observability-tool-selection.md` for why Phoenix and others were rejected.

---

## Conventions

- **Equations**: LaTeX in Markdown files (inline `$...$`, display `$$...$$`). Stored in `math/`.
- **Code**: Python 3, NumPy/SciPy/SymPy. Stored in `src/`. Must run from project root.
- **Python environment**: Use a project-local venv (prefer `.venv/`) for running code and installing dependencies. Do not rely on system Python.
- **Library-first coding**: Before writing new code, check Python stdlib and high-level domain libraries (e.g., qiskit). If missing, look for reputable existing repositories that already implement the topic.
- **Every approximation** must state its regime of validity explicitly.
- **Every numerical result** must include convergence or error analysis.
- **Figures**: saved to `figs/` with descriptive filenames (`figs/heating_rate_vs_omega.png`).

---

## Criticism File Format

### `notes/active_criticism.md` — living dashboard of open issues

```
**Next ID: C-NNN**   ← critic agent reads and increments this

## Criticism of [file] — [date]

### FATAL
- [ ] [C-001] Description. Why it invalidates the result. What must change.

### HIGH
- [ ] [C-002] Description. Why it weakens the argument.

### MEDIUM
- [ ] [C-003] Description.

### SMALL
- [ ] [C-004] Description.

## Score: [date] — FATAL: N, HIGH: N, MEDIUM: N, SMALL: N
```

The score line is appended after every critic pass. If FATAL+HIGH is not monotonically decreasing after 3 cycles, the approach has a structural problem — stop and reconsider.

### `notes/edit_history.md` — append-only audit trail

```
## [date] — [short description]
- Problem: [C-NNN or description of what was wrong]
- Solution: [what was done]
- Files changed: [list]
```

---

## Anti-Hype Protocol

LLMs tend to rate everything as promising. This project fights that with:
1. Per-direction literature checks before any criticism (ideation agent)
2. Every proposal must answer: "What existing paper would disprove this?"
3. Critic agent searches Scite when reviewing claims — contradiction = FATAL
4. Directions labeled honestly in summary: Genuinely novel / Incremental / Speculative / Already done / Killed
