# ADR-001: Observability Tool Selection

**Status:** Superseded (revised after hands-on testing)
**Date:** 2026-04-05 (original), 2026-04-05 (revised)
**Decision makers:** Daniel Herman

---

## Context

This project runs a multi-agent research workflow: Opus ideation/critic, Sonnet developer/literature, and a verify-math agent. Sessions can run for hours, dispatching sub-agents in chains (ideation → critic → developer → verify-math → critic re-review). When something goes wrong — a critic loop that doesn't converge, a derivation that silently produces nonsense, a cost spike from a runaway agent — we need to understand what happened.

Two distinct consumers need this observability data:

1. **Human (post-hoc debugging):** Reviews traces after a research session completes. Needs to see agent dispatch chains, tool timelines, cost breakdowns, and where things went wrong. Works hours or days after the session.

2. **Agent (self-optimization):** Queries its own past performance programmatically. Needs to answer: which critic cycles converged fastest? Which prompts produced the best results? Where did costs spike? Uses this data to adjust its own approach in future sessions.

---

## Options Considered

### Option A: Claude Code Native OTEL + Grafana (ColeMurray/claude-code-otel)

- **Approach:** Set env vars to export OTEL from Claude Code, pipe to Prometheus + Loki + Grafana via Docker Compose.
- **Pros:** Zero code changes. Pre-built Grafana dashboards. Battle-tested stack. Cost/token/tool metrics out of the box.
- **Cons:** Human-only (Grafana has no Python query API suitable for agents). No agent dispatch chain visibility (no `agent.name` attribute in OTEL). No evaluations or prompt management. Batch export intervals, not real-time.
- **Verdict:** Good baseline for human cost monitoring but fails the agent self-optimization requirement.

### Option B: aleksblago/claude-code-observability (Session File Reader)

- **Approach:** Reads `~/.claude/projects/` JSONL session transcripts directly. Live Vue dashboard with WebSocket streaming. Optional hooks for richer event capture.
- **Pros:** Only tool that shows agent dispatch chains natively (reads `AgentDelegation` events). Agent swim lanes. Real-time. No OTEL needed. Shows actual prompts, tool inputs/outputs, and conversation flow.
- **Cons:** Local only, no historical aggregation. No programmatic query API for agents. No evaluations. Single machine.
- **Verdict:** Best for human debugging of multi-agent workflows — shows what other tools cannot.

### Option C: Langfuse (24.3k stars)

- **Approach:** Full observability platform. 6 Docker Compose services (PostgreSQL, ClickHouse, Redis, MinIO, web, worker).
- **Pros:** Largest community. Richest feature set (evals, playground, datasets, prompt management). Python SDK with `api.trace.list()`, `api.observations.get_many()`, metrics aggregation endpoint. Agent can query traces and write scores back. Unlimited history on Pro.
- **Cons:** Heaviest infrastructure (8-16 GB RAM). ~50+ env vars to configure. UTC timezone requirement (silent bugs if violated). Anthropic integration is community-maintained, not first-party. Must call `flush()` or lose data. Docker Compose is "not recommended for production."
- **Verdict:** Strongest ecosystem but infrastructure overhead is disproportionate for a research project.

### Option D: Opik by Comet (18.6k stars)

- **Approach:** Full platform. 8+ Docker Compose services (MySQL, ClickHouse, ZooKeeper, Redis, MinIO, backend, frontend, init).
- **Pros:** First-party Anthropic wrapper (simpler than Langfuse). Agent execution graph visualization. `search_traces()` with expressive OQL filter language. Full OSS feature parity. Cheapest Pro tier ($19/mo). MCP server for agent access.
- **Cons:** Even heavier than Langfuse (8+ services, MySQL + ZooKeeper). Java backend (heavier cold starts). 60-day cloud retention on Pro. Younger community.
- **Verdict:** Strong query language but heaviest self-hosting of all options.

### Option E: Arize Phoenix (9.2k stars)

- **Approach:** Full platform in a single process. `pip install arize-phoenix` or single Docker container. SQLite (default) or PostgreSQL for production.
- **Pros:** Lightest full platform (no ClickHouse, Redis, or MinIO). **Pandas DataFrame-native query API** — `client.get_spans_dataframe()` returns DataFrames an agent can immediately analyze with groupby/sort/aggregate. SpanQuery DSL for filtering. **Claude Agent SDK support** (Python + TypeScript). Built-in evaluations (LLM-as-Judge, hallucination, QA correctness). Prompt playground. Completely free, no feature gating. MCP server available.
- **Cons:** Single-tenant per instance. SQLite doesn't handle concurrent access (use PostgreSQL for multi-user). Smaller community than Langfuse.
- **Verdict (original):** Best balance of capability vs. complexity.
- **Verdict (revised after testing):** **Phoenix's UI does not usefully display Claude Code OTEL data.** See "Lessons Learned" below.

### Option F: OpenLLMetry by Traceloop (7.0k stars)

- **Approach:** OTEL instrumentation library only. No platform — bring your own backend.
- **Pros:** Maximum flexibility. Vendor-neutral. Minimal footprint.
- **Cons:** No UI, no evaluations, no query API (depends entirely on backend). Adds a layer of indirection without solving the core requirements.
- **Verdict:** Good if we already ran an OTEL backend. We don't.

### Option G: OpenLIT (2.3k stars)

- **Approach:** OTEL-native SDK with optional self-hosted dashboard (ClickHouse + Grafana).
- **Pros:** Claude Agent SDK support. Broadest framework coverage. Multi-language. Evaluations, guardrails, prompt hub.
- **Cons:** Smaller community. Dashboard less polished. OTEL complexity leaks through.
- **Verdict:** Interesting but Phoenix covers the same ground with a simpler setup.

### Option H: Helicone (5.4k stars)

- **Approach:** AI Gateway proxy. Route all LLM traffic through Helicone.
- **Pros:** Zero SDK code (change URL). Gets routing, caching, rate limiting for free.
- **Cons:** Adds latency to every request. Heavy self-host (5 services). No agent-level instrumentation. Anthropic integration deprioritized.
- **Verdict:** Wrong tool for this use case. Gateway overhead is unjustified for a research workflow.

### Option I: AgentOps (5.4k stars)

- **Approach:** Agent-first SDK. Session replay with execution graphs.
- **Pros:** Best agent visualization. Purpose-built for multi-agent workflows.
- **Cons:** No search/list traces endpoint — only per-ID lookup. Agent cannot discover its own past traces without knowing IDs. No bulk export. Python-only for Anthropic. Self-hosting maturity unclear.
- **Verdict:** Fails the agent self-optimization requirement due to missing search API.

---

## Lessons Learned: Phoenix + Claude Code OTEL (Tested and Found Insufficient)

Phoenix was initially selected as the primary platform. After deploying it (Docker Compose with PostgreSQL) and running a full demo session with Claude Code OTEL enabled, we found:

1. **No prompts visible.** Claude Code OTEL emits custom span types (`claude_code.llm_request`, `claude_code.tool`) that Phoenix renders as generic OTEL spans. The `input` and `output` columns show `--` for every span. Even with `OTEL_LOG_USER_PROMPTS=1` and `OTEL_LOG_TOOL_DETAILS=1` enabled, the data is in custom attributes that Phoenix doesn't map to its UI columns.

2. **No tool content.** You can see `tool_name: Write` and `file_path: /path/to/file` in the attributes, but not what was written. The actual tool inputs and outputs are not surfaced.

3. **No agent dispatch chains.** All 126 captured spans appear as a flat list. There is no parent-child hierarchy showing prompt → tool calls → sub-agent flows. Spans are correlated only by `session.id`, not by agent identity.

4. **Cost shows $0.** Claude Code OTEL provides `input_tokens`, `output_tokens`, `cache_read_tokens` per span, but Phoenix doesn't calculate cost from these custom attributes. The "Total Cost" dashboard shows $0.

5. **Span kind is UNKNOWN.** Phoenix expects standard OTEL span kinds (LLM, RETRIEVER, CHAIN). Claude Code emits `claude_code.*` names that map to `UNKNOWN`.

**Root cause:** Phoenix is designed for **Anthropic SDK instrumentation** where it wraps `client.messages.create()` and captures the full request/response. Claude Code's OTEL export is a different, incompatible format — custom span types with data in non-standard attribute fields.

**Phoenix remains valuable for:** Instrumenting Python scripts in `src/` via the Anthropic SDK (where it works correctly). It is not useful for observing Claude Code agent sessions.

---

## Decision (Revised)

**aleksblago/claude-code-observability** as the primary human debugging tool.

**Arize Phoenix** retained for Python script instrumentation and agent self-optimization via DataFrame API (when instrumenting `src/` code directly, not Claude Code sessions).

**Claude Code native OTEL** retained as always-on baseline for metrics that can be queried programmatically via Phoenix's API.

---

## Rationale (Revised)

### Why aleksblago for human debugging

1. **Shows what other tools cannot.** Reads native Claude Code session files (`~/.claude/projects/`) directly — no OTEL translation layer. Shows actual prompts, tool inputs/outputs, agent delegation events, and conversation flow.

2. **Agent swim lanes.** Side-by-side comparison of multiple agents in real-time. When ideation dispatches critic which dispatches verify-math, you see all three lanes simultaneously.

3. **Real-time WebSocket streaming.** Sub-second updates. You can watch a multi-agent research session unfold live.

4. **HITL notifications.** Alerts when an agent asks a question or requests a permission — critical for long-running autonomous sessions.

5. **Zero OTEL dependency.** Works by reading session transcripts and optional hooks. No custom span format translation needed.

6. **Lightweight.** Bun runtime, zero npm dependencies for the server. Vue 3 client. No database to manage.

### Why keep Phoenix

Phoenix failed as a Claude Code session observer, but it remains the best option for:
- **Agent self-optimization queries** via `client.get_spans_dataframe()` on Python-instrumented code
- **Evaluations** (LLM-as-Judge) on research outputs
- **Historical storage** in PostgreSQL for data that outlives a session

### Setup

**aleksblago/claude-code-observability:**
- Cloned to `/tmp/claude-code-observability`
- `./setup.sh` installs hook file at `~/.claude/hooks/capture-events.ts` and `/Observability` slash command
- Hooks added to `~/.claude/settings.json` for `PreToolUse`, `PostToolUse`, `Stop`, `SubagentStop`
- Dashboard at `http://localhost:52871`, API at `http://localhost:52870`
- Start: `./manage.sh start-detached`, stop: `./manage.sh stop`

**Arize Phoenix (retained):**
- Docker Compose: `docker compose up -d` (Phoenix + PostgreSQL)
- UI at `http://localhost:6006`, OTLP at `localhost:4317`
- Used for Python script instrumentation via `src/tracing.py`

---

## Consequences

- aleksblago dashboard should be running during research sessions for live monitoring (`./manage.sh start-detached` or `/Observability on`)
- Phoenix Docker stack should be running for Python code instrumentation and agent self-optimization queries
- Claude Code OTEL env vars should be set in shell profile (feeds Phoenix with baseline metrics)
- Human debugging primarily uses aleksblago dashboard (prompts, tool content, agent chains)
- Agent self-optimization uses Phoenix DataFrame API (cost analysis, timing, evaluation scores)
- Both tools are local-only — no remote/team access without additional infrastructure

---

## References

- [Full tool comparison: docs/observability_tools.md](../observability_tools.md)
- [aleksblago/claude-code-observability GitHub](https://github.com/aleksblago/claude-code-observability)
- [Arize Phoenix GitHub](https://github.com/Arize-ai/phoenix)
- [Claude Code Telemetry Docs](https://code.claude.com/docs/en/monitoring-usage)
