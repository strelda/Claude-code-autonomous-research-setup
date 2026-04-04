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
│   │   ├── proposal.md         # The direction described (includes feasibility scorecard)
│   │   ├── literature_check.md # What existing work says about it
│   │   └── criticism.md        # Adversarial self-critique (includes "what would save this?" for killed directions)
│   └── summary.md          # Ranked comparison of all directions
├── math/                   # Derivations (LaTeX Markdown, produced by Gemini)
├── src/                    # Python code (NumPy/SciPy/SymPy)
│   └── scripts/
│       ├── arxiv_download.py   # Download PDFs from arxiv
│       └── gemini_check.sh     # Pipe a file to Gemini for verification
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
3. The agent will:
   - Search the literature via Scite MCP
   - Propose **at least 4** directions in `directions/option_X/` (3 is too few — aim for 5)
   - Perform a **literature reality check** per direction (has it been done? contradicted? trivial?)
   - Self-criticize each direction adversarially
   - Cross-check with Gemini
   - For each direction, include a **feasibility scorecard**:
     - Mathematical difficulty (1-10)
     - Computational cost (1-10)
     - Expected time to first result (weeks)
     - Probability of meaningful result (%)
   - For killed directions, include a **"What would save this?"** section documenting what would need to change for the direction to survive — prevents revisiting the same dead ends
   - Write a ranked `directions/summary.md`
4. **Brainstorm retrospective:** After initial directions are proposed, the agent does a second pass: "Given the directions we proposed, what other angles did we miss?" This guards against tunnel vision from the initial literature search framing.
5. Read `directions/summary.md`. Read individual `proposal.md` and `criticism.md` files as needed.
6. Tell Claude which direction to develop (or combine elements from multiple).

### Phase 2 — Development

1. The main session (Opus) reads the chosen direction and writes `notes/plan.md` with numbered tasks.
2. Tasks are dispatched by type:
   - **Derivations** → Gemini CLI. The main session pipes a task prompt to Gemini, saves output to `math/`.
   - **Code** → `developer` agent (Sonnet). Implements in `src/`. Must be runnable and tested.
   - **Writing** → `developer` agent (Sonnet). Drafts report sections in `report/`.
3. After each piece of work, the `critic` agent reviews it (writes to `notes/active_criticism.md`).
4. The criticism loop runs until no FATAL or HIGH issues remain:
   ```
   work produced → critic reviews → issues logged → fixes dispatched
   → critic re-reviews → issues marked resolved → repeat
   ```
5. The `literature` agent is invoked whenever a claim needs verification against published work.
6. All changes are logged in `notes/edit_history.md`.

---

## Agents

| Agent | Model | Role |
|-------|-------|------|
| `ideation` | Opus | Brainstorm + literature check + self-criticize research directions |
| `critic` | Opus | Hostile referee. Finds real flaws. Searches literature. Cross-checks with Gemini. |
| `developer` | Sonnet | Code (src/) and writing (report/) tasks only |
| `literature` | Sonnet | Search Scite/bioRxiv, download arxiv papers |

---

## External Tools

**Gemini CLI** (primary derivation engine + math verifier):
```bash
cat math/task.md | gemini -p "Derive..."
cat math/result.md | bash src/scripts/gemini_check.sh -
```
- Gemini is strong at mathematics and cheap — use it freely.
- One self-contained prompt per call. No multi-turn. If a derivation is too long for one prompt, break it into independent steps.

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

## Conventions

- **Equations**: LaTeX in Markdown files (inline `$...$`, display `$$...$$`). Stored in `math/`.
- **Code**: Python 3, NumPy/SciPy/SymPy. Stored in `src/`. Must run from project root.
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
```

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
