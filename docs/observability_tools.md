# Observability Tools for LLM Agent Workflows

*Survey date: April 2026*

This document compares open-source tools for monitoring and debugging multi-agent LLM workflows, with a focus on Claude Code and Anthropic API compatibility.

---

## Table of Contents

1. [Claude Code Native Telemetry](#1-claude-code-native-telemetry)
2. [Claude Code-Specific Tools](#2-claude-code-specific-tools)
3. [Full Observability Platforms](#3-full-observability-platforms)
4. [Lightweight Libraries](#4-lightweight-libraries)
5. [Gateway / Proxy Approaches](#5-gateway--proxy-approaches)
6. [Agent-First Tools](#6-agent-first-tools)
7. [Comparison Matrix](#7-comparison-matrix)
8. [Approach Comparison: Pros and Cons](#8-approach-comparison-pros-and-cons)
9. [Setup Recommendations](#9-setup-recommendations)

---

## 1. Claude Code Native Telemetry

Claude Code has built-in OpenTelemetry export. No code changes to your project required.

### Environment Variables

**Core (minimum viable):**
```bash
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_LOGS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

**Traces (beta, opt-in):**
```bash
export CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1
export OTEL_TRACES_EXPORTER=otlp
```

**Content capture (off by default — privacy-sensitive):**
```bash
export OTEL_LOG_USER_PROMPTS=1        # prompt text in events
export OTEL_LOG_TOOL_DETAILS=1        # tool params (bash cmds, MCP names, skill names)
export OTEL_LOG_TOOL_CONTENT=1        # full tool I/O in trace spans (truncated 60KB)
```

**Tuning:**
```bash
export OTEL_METRIC_EXPORT_INTERVAL=10000     # default 60000ms
export OTEL_LOGS_EXPORT_INTERVAL=5000        # default 5000ms
export OTEL_TRACES_EXPORT_INTERVAL=5000      # default 5000ms
export OTEL_RESOURCE_ATTRIBUTES="team.id=myteam"
```

### What Gets Exported

**Metrics (time-series counters):**

| Metric | Description | Attributes |
|--------|-------------|------------|
| `claude_code.session.count` | Sessions started | — |
| `claude_code.cost.usage` | Cost in USD | `model` |
| `claude_code.token.usage` | Tokens consumed | `type` (input/output/cacheRead/cacheCreation), `model` |
| `claude_code.lines_of_code.count` | Lines modified | `type` (added/removed) |
| `claude_code.commit.count` | Git commits | — |
| `claude_code.pull_request.count` | PRs created | — |
| `claude_code.code_edit_tool.decision` | Accept/reject of Edit/Write | `tool_name`, `decision` |
| `claude_code.active_time.total` | Active seconds | — |

**Events (via OTEL logs):**

| Event | Key Attributes |
|-------|---------------|
| `claude_code.user_prompt` | `prompt_length`, `prompt` (if enabled) |
| `claude_code.tool_result` | `tool_name`, `success`, `duration_ms`, `tool_parameters` (if enabled) |
| `claude_code.api_request` | `model`, `cost_usd`, `duration_ms`, `input_tokens`, `output_tokens` |
| `claude_code.api_error` | `model`, `error`, `status_code` |

All events share: `session.id`, `prompt.id` (correlates a prompt to all its child events).

**Traces (beta):** Distributed spans linking each user prompt to API requests and tool executions.

### What You Can and Cannot See

| Capability | Status |
|-----------|--------|
| Per-model cost breakdown (Opus vs Sonnet) | Yes |
| Token usage by type per API call | Yes |
| Tool names, durations, success/failure | Yes |
| Tool parameters (bash cmds, MCP names) | Yes (with `OTEL_LOG_TOOL_DETAILS=1`) |
| Full tool I/O content | Yes (with `OTEL_LOG_TOOL_CONTENT=1`, 60KB limit) |
| User prompt text | Yes (with `OTEL_LOG_USER_PROMPTS=1`) |
| Explicit sub-agent dispatch chains | **No** — no `agent.name` attribute; `prompt.id` is the closest correlation |
| Model reasoning / chain-of-thought | **No** |
| Per-sub-agent cost breakdown | **No** — `api_request` has `model` + `cost_usd` but no agent identifier |

---

## 2. Claude Code-Specific Tools

### ColeMurray/claude-code-otel (332 stars)

- **Architecture:** Claude Code → OTEL Collector (4317) → Prometheus (metrics) + Loki (logs) → Grafana
- **Setup:** `git clone` + Docker Compose + set env vars
- **Dashboards:** Cost by model, API request counts, token efficiency, tool performance, session analytics, error analysis, DAU/WAU/MAU
- **Ports:** Grafana on 3000, Prometheus on 9090
- **Strengths:** Most polished Grafana dashboards of the Claude Code-specific tools, good executive overview panels
- **Limitations:** Only shows what Claude Code exports via OTEL. No agent-level swim lanes or dispatch chain visibility.

### acreeger/claude-code-metrics-stack (8 stars)

- **Architecture:** Same as above — OTEL Collector → Prometheus + Loki → Grafana (port 8000)
- **Setup:** `git clone` + `make up` + set env vars
- **Dashboard:** Pre-provisioned Grafana dashboard under "Claude Code" folder
- **Strengths:** Simpler setup with Makefile
- **Limitations:** Same as ColeMurray — limited to OTEL data

### aleksblago/claude-code-observability (live dashboard)

- **Architecture:** Reads `~/.claude/projects/` JSONL session transcripts directly — **no OTEL needed**
- **Tech:** Bun + Vue 3, WebSocket-based live streaming
- **Key differentiator:** Sees things OTEL cannot:
  - **Agent swim lanes** — compares activity across multiple agents side-by-side
  - **Agent delegation events** (`AgentDelegation` type) — tracks when sub-agents are spawned
  - **Chat transcript viewer** — full conversation replay
  - **HITL notifications** — when agents ask questions or request permissions
  - **Pulse chart** — visual heartbeat with heat levels
- **Setup:** `./setup.sh` installs a `/Observability` slash command and hook
- **Ports:** 52870 (API), 52871 (Dashboard)
- **Limitations:** Local only, no historical aggregation

### lifegenieai/claude-code-observability (OTEL → Langfuse bridge)

- **Architecture:** Claude Code → OTEL → Node.js bridge (localhost:4318) → Langfuse Cloud
- **Features:** Per-session/per-model cost breakdown, token analysis, tool profiling, **multi-agent trace correlation** via `prompt.id`
- **Known quirk:** Input tokens underreported (shows `input_tokens: 1` sometimes); output tokens and `cost_usd` are accurate
- **Security note:** Bridge sees all telemetry in cleartext — pin to audited commit

---

## 3. Full Observability Platforms

### Langfuse (24,352 stars)

- **Architecture:** Full platform — UI + server + instrumentation + evaluations
- **Self-hosting:**
  - 6 Docker Compose services: langfuse-web, langfuse-worker, PostgreSQL, ClickHouse, Redis, MinIO
  - RAM: 8-16 GB realistically (ClickHouse alone wants 4+ GB)
  - Docker Compose is dev only — production requires Kubernetes/Helm or Terraform
  - **Gotcha:** All infra must run UTC or queries return wrong results
- **Anthropic integration:**
  - OTel-based via community `AnthropicInstrumentor` package
  - Also supports OpenAI-compatible endpoint wrapper
  ```python
  from opentelemetry.instrumentation.anthropic import AnthropicInstrumentor
  AnthropicInstrumentor().instrument()
  client = anthropic.Anthropic()  # auto-traced
  ```
- **Multi-agent tracing:** Nested observations via `@observe()` decorator. Traces group into Sessions. Integrations with CrewAI, AutoGen, smolagents.
- **Storage:** PostgreSQL (transactional) + ClickHouse (analytical) + S3/MinIO (objects) + Redis (queue/cache)
- **Pricing (cloud):** Free 50k units/mo, Core $29/mo, Pro $199/mo (unlimited history), Enterprise $2,499/mo
- **Self-hosted:** Free (MIT). Some Enterprise features gated behind license key.
- **Strengths:** Largest community, most integrations, mature data model (v4 observation-centric), prompt playground, evaluations
- **Weaknesses:** Heavy infrastructure, ~50+ env vars to configure, Anthropic integration is community-maintained (not first-party), `langfuse.flush()` required for short-lived apps or data is lost

### Opik by Comet (18,642 stars)

- **Architecture:** Full platform — UI + server + instrumentation + evaluations
- **Self-hosting:**
  - 8+ Docker Compose services: MySQL, Redis, ClickHouse, ZooKeeper, MinIO, clickhouse-init, backend (Java), frontend (nginx)
  - RAM: 8-16 GB (ZooKeeper adds JVM overhead capped at 512MB)
  - `./opik.sh` setup script simplifies launch
  - Docker Compose is dev only — production requires Kubernetes/Helm
- **Anthropic integration:**
  - First-party wrapper function — simpler than Langfuse
  ```python
  from opik.integrations.anthropic import track_anthropic
  client = track_anthropic(anthropic.Anthropic(), project_name="my-project")
  ```
- **Multi-agent tracing:** `@track` decorator for nested spans. Agent execution graph visualization. Integrations with AutoGen, CrewAI, Google ADK, LangGraph.
- **Storage:** MySQL (transactional) + ClickHouse (analytical) + MinIO (objects) + Redis (cache) + ZooKeeper
- **Pricing (cloud):** Free 25k spans/mo (60-day retention), Pro $19/mo (60-day retention), Enterprise custom
- **Self-hosted:** Free (Apache 2.0). Claims full OSS feature parity — no gating.
- **Strengths:** First-party Anthropic wrapper (simpler setup), friendlier `opik.sh` setup script, agent execution graph visualization, cheaper Pro tier ($19 vs $199), full OSS parity
- **Weaknesses:** More services (8+ vs 6), MySQL instead of PostgreSQL (less common in this space), ZooKeeper dependency, Java backend (heavier cold starts), 60-day cloud retention even on Pro, younger community

### Arize Phoenix (9,164 stars)

- **Architecture:** Full platform — UI + server + instrumentation + evaluations
- **Self-hosting:**
  - **Lightest option:** `pip install arize-phoenix` then `python -m phoenix.server.main serve` — runs locally with SQLite
  - **Docker:** Single container: `docker run -p 6006:6006 -p 4317:4317 arizephoenix/phoenix:latest`
  - PostgreSQL optional for production (concurrent access)
  - No ClickHouse, Redis, or MinIO required
- **Anthropic integration:**
  - Dedicated `openinference-instrumentation-anthropic` package
  - Also has **Claude Agent SDK** instrumentation (Python + TypeScript)
  ```python
  from phoenix.otel import register
  tracer_provider = register(project_name="my-app", auto_instrument=True)
  client = anthropic.Anthropic()  # auto-traced
  ```
- **Multi-agent tracing:** Dedicated instrumentors for Claude Agent SDK, OpenAI Agents SDK, CrewAI, LangGraph, Autogen, Pydantic AI, Agno, Smolagents
- **Storage:** SQLite (default, zero config) or PostgreSQL (production). No ClickHouse.
- **Pricing:** Free, no feature limitations. Arize AX is the paid enterprise offering.
- **Strengths:** Lightest self-hosting of any full platform (single `pip install` or single Docker container), Claude Agent SDK support, completely free, no feature gating, prompt playground + evaluations included
- **Weaknesses:** Single-tenant per instance (no multi-org without enterprise), SQLite doesn't support concurrent access well, web analytics telemetry on by default (opt-out with `PHOENIX_TELEMETRY_ENABLED=false`), smaller community than Langfuse

---

## 4. Lightweight Libraries

### OpenLLMetry by Traceloop (6,975 stars)

- **Type:** Instrumentation library only — **not a platform**. Generates OTEL traces, you bring your own backend.
- **Install:** `pip install traceloop-sdk` — zero infrastructure
- **Anthropic integration:**
  ```python
  from opentelemetry.instrumentation.anthropic import AnthropicInstrumentor
  AnthropicInstrumentor().instrument()
  ```
  No Claude Agent SDK support (only raw Anthropic SDK).
- **Multi-agent tracing:** Decorators `@workflow`, `@task`, `@agent`, `@tool` for span hierarchy. Works with CrewAI, LangChain, LangGraph, LlamaIndex, OpenAI Agents, Agno, MCP.
- **Supported backends:** 20+ tested — Datadog, Honeycomb, Grafana/Tempo, Jaeger, SigNoz, New Relic, Splunk, Axiom, etc.
- **Strengths:** Maximum flexibility (any OTEL backend), minimal footprint, OTEL-native (follows GenAI Semantic Conventions), multi-language (Python, Node.js, Go)
- **Weaknesses:** No UI included — must pick and run your own backend. No evaluations, prompt management, or datasets. Traceloop SaaS dashboard is separate paid product.

### OpenLIT (2,339 stars)

- **Type:** OTEL-native SDK with optional self-hosted dashboard
- **Install:** `pip install openlit` + `openlit.init()` — 2 lines
- **Self-hosting:** Docker Compose with ClickHouse + Grafana (simpler stack than Langfuse/Opik)
- **Anthropic integration:** Auto-instruments Anthropic SDK. Also has explicit **Claude Agent SDK** integration.
- **Multi-agent tracing:** OTEL distributed tracing. Broadest framework coverage: CrewAI, LangChain, LlamaIndex, LangGraph, AG2, Pydantic AI, Agno, OpenAI Agents, Claude Agent SDK, Google ADK, Smolagents, Strands Agents, MS Agent Framework.
- **Beyond observability:** 11 built-in evaluation types, guardrails, prompt hub, secrets vault, playground, rule engine
- **Strengths:** Vendor-neutral (sends to any OTEL backend), most framework integrations, Claude Agent SDK support, multi-language (Python, TypeScript, Go), feature-rich beyond tracing
- **Weaknesses:** Smaller community, dashboard UI less polished than Langfuse, OTEL complexity can leak through, LLM-as-Judge evaluations add cost

---

## 5. Gateway / Proxy Approaches

### Helicone (5,447 stars)

- **Type:** AI Gateway + observability proxy. Routes all LLM traffic through Helicone.
- **Self-hosting:** Docker Compose with 5 services — NextJS web, Cloudflare Workers proxy, Express server, Supabase, ClickHouse, MinIO. Helm chart for enterprise (contact required).
- **Anthropic integration:** Change `baseURL` to Helicone gateway + add auth header. Zero SDK code.
  ```python
  client = anthropic.Anthropic(base_url="https://ai-gateway.helicone.ai")
  ```
  Note: dedicated Anthropic SDK page is "maintained but no longer actively developed" — they push the unified gateway.
- **Multi-agent tracing:** Sessions feature for multi-step workflows. Integrations with CrewAI, MetaGPT, LangGraph, LangChain.
- **Beyond observability:** Routing, fallbacks, caching, rate limiting, prompt management with versioning.
- **Strengths:** Zero SDK code (just change URL), full gateway with routing/caching, largest open-source LLM cost API (300+ models)
- **Weaknesses:** Adds latency to every request (proxy hop), heavy self-host (5+ services), Anthropic integration being de-prioritized for unified gateway, no agent-level decorators/annotations

---

## 6. Agent-First Tools

### AgentOps (5,435 stars)

- **Type:** SDK-based, purpose-built for AI agents
- **Self-hosting:** Open source (MIT). Full app in `app/` directory. Self-host guide available but relatively new.
- **Anthropic integration:** `agentops.init()` auto-instruments all Anthropic SDK calls (Python only).
  ```python
  import agentops
  agentops.init()
  client = anthropic.Anthropic()  # auto-traced
  ```
- **Multi-agent tracing:** Core strength. Decorators: `@session`, `@agent`, `@operation`, `@task`, `@workflow`. Session replay with step-by-step agent execution graphs. Native support for CrewAI, AG2, OpenAI Agents SDK, Camel AI, LangChain, LlamaIndex, Agno, SwarmZero.
- **Strengths:** Best agent-specific visualization (session replay, execution graphs), widest agent framework support, ergonomic decorator API
- **Weaknesses:** Python-centric (TypeScript alpha), no proxy/gateway, no prompt management or cost optimization, self-hosting maturity unclear, no JS/TS Anthropic integration

---

## 7. Comparison Matrix

### Architecture Approaches

| Approach | Tools | How It Works |
|----------|-------|-------------|
| **Native OTEL** | Claude Code built-in | Set env vars, export to any OTEL backend |
| **Session file reading** | aleksblago observability | Parse JSONL transcripts from `~/.claude/projects/` |
| **OTEL SDK (auto-instrument)** | Phoenix, OpenLLMetry, OpenLIT, AgentOps | Monkey-patch LLM SDK, emit OTEL spans |
| **OTEL SDK (wrapper)** | Opik, Langfuse | Wrap client or decorate functions |
| **Proxy / Gateway** | Helicone | Route traffic through gateway, log at proxy |

### Feature Comparison

| Feature | CC OTEL | aleksblago | ColeMurray | Langfuse | Opik | Phoenix | OpenLLMetry | OpenLIT | Helicone | AgentOps |
|---------|---------|------------|------------|----------|------|---------|-------------|---------|----------|----------|
| **Stars** | built-in | — | 332 | 24.3k | 18.6k | 9.2k | 7.0k | 2.3k | 5.4k | 5.4k |
| **Self-hostable** | N/A | Yes | Yes | Yes | Yes | Yes | Library | Yes | Yes | Yes (new) |
| **Setup complexity** | Env vars | Script | Docker | Docker (6 svc) | Docker (8+ svc) | pip or Docker (1 svc) | pip | pip or Docker | Docker (5 svc) | pip |
| **RAM needed** | N/A | Low | 2-4 GB | 8-16 GB | 8-16 GB | Low | N/A | 2-4 GB | 4-8 GB | Low |
| **Anthropic native** | Yes | N/A | N/A | OTEL (community) | First-party wrapper | OTEL (dedicated) | OTEL | Auto-instrument | Proxy | Auto-instrument |
| **Claude Agent SDK** | N/A | N/A | N/A | No | No | **Yes** | No | **Yes** | No | No |
| **Agent dispatch chains** | No | **Yes** | No | Via decorators | Via decorators | Via instrumentors | Via decorators | Via OTEL | Sessions | **Yes (core)** |
| **Per-agent cost** | No | Inferred | No | Via spans | Via spans | Via spans | Via backend | Via OTEL | No | Via sessions |
| **Live real-time view** | No | **Yes** | No | No | No | No | No | No | No | No |
| **Evaluations** | No | No | No | **Yes** | **Yes** | **Yes** | No | **Yes** | No | No |
| **Prompt management** | No | No | No | **Yes** | No | **Yes** | No | **Yes** | **Yes** | No |
| **Web UI included** | No | **Yes** | Grafana | **Yes** | **Yes** | **Yes** | No | **Yes** | **Yes** | **Yes** |
| **Code changes needed** | None | None | None | Decorator/wrapper | Wrapper | 2 lines | 2 lines | 2 lines | URL change | 2 lines |
| **Vendor lock-in** | None | None | None | Medium | Medium | Low | **None** | **Low** | Medium | Medium |
| **License** | — | — | — | MIT | Apache 2.0 | Apache 2.0 | Apache 2.0 | Apache 2.0 | Apache 2.0 | MIT |

---

## 8. Approach Comparison: Pros and Cons

### Approach A: Native OTEL Only (Claude Code → Grafana)

Tools: Claude Code env vars + ColeMurray/acreeger metrics stack

**Pros:**
- Zero code changes to your project
- Captures all Claude Code metrics and events automatically
- Grafana is battle-tested, extensible, alerting-capable
- Lightest integration effort (just set env vars and `docker-compose up`)

**Cons:**
- Cannot see agent dispatch chains (no `agent.name` attribute in OTEL)
- Cannot see per-sub-agent costs (no agent identifier on `api_request` events)
- Content redacted by default — must opt-in with 3 separate env vars
- No evaluations, prompt management, or experiment tracking
- Batch export intervals (not real-time)

**Best for:** Cost tracking, token usage monitoring, basic tool profiling. Good starting point.

### Approach B: Session File Reading (aleksblago)

Tools: aleksblago/claude-code-observability

**Pros:**
- **Only tool that shows agent dispatch chains natively** (reads `AgentDelegation` events from session files)
- Agent swim lanes for comparing activity across agents
- Real-time WebSocket streaming (sub-second updates)
- No OTEL setup required — reads native files
- HITL notification when agents need input

**Cons:**
- Local only — no historical aggregation or dashboards
- No cost/token analytics (different data source)
- No evaluations
- Single machine only (can't aggregate across team)

**Best for:** Live debugging of multi-agent workflows. Essential for seeing which agent is doing what in real-time.

### Approach C: Full Platform (Langfuse / Opik / Phoenix)

**Langfuse pros:**
- Largest community, most battle-tested
- Richest feature set (evals, playground, datasets, prompt management)
- Most integrations
- Unlimited history on Pro

**Langfuse cons:**
- Heaviest infrastructure (6 services, 8-16 GB RAM)
- ~50+ env vars to configure
- UTC timezone requirement (silent bugs if violated)
- Anthropic integration is community-maintained, not first-party
- Must call `flush()` or lose data

**Opik pros:**
- First-party Anthropic wrapper (simpler)
- Agent execution graph visualization
- Friendlier setup script (`./opik.sh`)
- Full OSS feature parity (no gating)
- Cheaper Pro tier ($19/mo vs $199/mo)

**Opik cons:**
- More services (8+ with ZooKeeper)
- MySQL instead of PostgreSQL
- Java backend (heavier)
- 60-day cloud retention even on Pro
- Younger community

**Phoenix pros:**
- **Lightest full platform** — single `pip install` or single Docker container
- **Claude Agent SDK support** (Python + TypeScript)
- Completely free, no feature gating
- PostgreSQL or SQLite (no ClickHouse needed)
- Evaluations, prompt playground, datasets included

**Phoenix cons:**
- Single-tenant per instance
- SQLite doesn't handle concurrent access
- Smaller community than Langfuse
- Web analytics telemetry on by default

**Best for:** Teams needing evaluations, prompt management, and rich trace visualization. Phoenix if you want lightweight; Langfuse if you want the ecosystem.

### Approach D: OTEL Library + Existing Backend (OpenLLMetry / OpenLIT)

**Pros:**
- Maximum flexibility — send traces to any OTEL backend you already run (Datadog, Grafana, Jaeger, etc.)
- No vendor lock-in
- Minimal footprint (just a pip package)
- OpenLIT has Claude Agent SDK support

**Cons:**
- Must bring your own backend (setup + maintain)
- No built-in UI with OpenLLMetry
- OTEL configuration can be complex
- Need OTEL expertise for custom dashboards

**Best for:** Teams already running an OTEL-compatible observability stack (Datadog, Grafana Tempo, Jaeger).

### Approach E: Proxy Gateway (Helicone)

**Pros:**
- Zero SDK code changes (just change base URL)
- Gets routing, caching, rate limiting, and fallbacks for free
- Cost tracking across 300+ models
- Prompt management with versioning

**Cons:**
- Adds latency to every LLM request (proxy hop)
- Heavy self-host (5 services including Cloudflare Workers, Supabase)
- Anthropic integration being de-prioritized
- No agent-level instrumentation (only LLM call level)

**Best for:** Teams wanting a unified AI gateway with built-in observability. Less useful for agent workflow debugging.

### Approach F: Agent-First (AgentOps)

**Pros:**
- Purpose-built for multi-agent workflows
- Best session replay and execution graph visualization
- Ergonomic decorator API (`@agent`, `@task`, `@workflow`)
- Widest agent framework support

**Cons:**
- Python-only for Anthropic
- Self-hosting maturity unclear (recently open-sourced)
- No gateway/proxy features
- No prompt management

**Best for:** Heavy multi-agent orchestration where session replay and execution graphs are primary debugging tools.

---

## 9. Setup Recommendations

### For This Project (Claude Code Multi-Agent Research Workflow)

**Tier 1 — Start here (zero code changes):**

Enable Claude Code native OTEL + Grafana dashboards:
```bash
# Add to shell profile or .env
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_LOGS_EXPORTER=otlp
export OTEL_TRACES_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
export OTEL_LOG_USER_PROMPTS=1
export OTEL_LOG_TOOL_DETAILS=1
```
Then run ColeMurray/claude-code-otel (`docker-compose up`). Gets you cost tracking, token usage, and tool profiling in Grafana.

**Tier 2 — Add agent visibility:**

Install aleksblago/claude-code-observability alongside Tier 1. Gets you real-time agent swim lanes, dispatch chain tracking, and conversation replay. Complements Grafana's historical metrics with live debugging.

**Tier 3 — Add evaluations and rich tracing (if needed):**

Deploy Phoenix (`pip install arize-phoenix`) as the lightest full platform. Claude Agent SDK support means you can instrument your Python scripts for deeper tracing. Evaluations and prompt playground included. Single container, no ClickHouse.

### Decision Flowchart

```
Do you need to see agent dispatch chains?
├── No → Tier 1 (OTEL + Grafana)
└── Yes → Add aleksblago (Tier 2)
         │
         Do you need evaluations or prompt management?
         ├── No → Stay at Tier 2
         └── Yes → Do you already run an OTEL backend?
                   ├── Yes → Add OpenLLMetry or OpenLIT
                   └── No → Add Phoenix (Tier 3)
                            │
                            Need enterprise scale (40M+ traces/day)?
                            ├── No → Phoenix is fine
                            └── Yes → Langfuse or Opik
```

---

## References

- [Claude Code Telemetry Docs](https://code.claude.com/docs/en/monitoring-usage)
- [Langfuse GitHub](https://github.com/langfuse/langfuse)
- [Opik GitHub](https://github.com/comet-ml/opik)
- [Arize Phoenix GitHub](https://github.com/Arize-ai/phoenix)
- [OpenLLMetry GitHub](https://github.com/traceloop/openllmetry)
- [OpenLIT GitHub](https://github.com/openlit/openlit)
- [Helicone GitHub](https://github.com/helicone/helicone)
- [AgentOps GitHub](https://github.com/AgentOps-AI/agentops)
- [ColeMurray/claude-code-otel](https://github.com/ColeMurray/claude-code-otel)
- [acreeger/claude-code-metrics-stack](https://github.com/acreeger/claude-code-metrics-stack)
- [aleksblago/claude-code-observability](https://github.com/aleksblago/claude-code-observability)
- [lifegenieai/claude-code-observability](https://github.com/lifegenieai/claude-code-observability)
