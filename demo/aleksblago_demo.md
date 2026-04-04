# SOTA Approaches to Agentic Academic Research (2025-2026)

*Compiled via 3 parallel search agents covering systems, methodologies, and tools.*

---

## Top Systems

| System | Builder | Key Innovation | Status |
|--------|---------|---------------|--------|
| **AI Scientist v2** | Sakana AI | Agentic tree search over hypothesis space; first AI paper accepted at workshop | Open-source, 13k stars. But 57% of papers contain false data |
| **Google AI Co-Scientist** | DeepMind | Generate-debate-evolve with tournament ranking (ELO-style) | Closed; wet-lab validated in biomedicine |
| **NovelSeek** | Shanghai AI Lab | Closed-loop hypothesis-to-verification across 12 research tasks | Open-source |
| **cmbagent** | Cosmology group | 30 specialized agents with Planning & Control; PhD-level cosmology | Open-source |
| **Coscientist** | CMU (Nature 2023) | GPT-4 controlling robotic chemistry labs autonomously | Domain-specific |
| **ARIS** | Community | Zero-framework markdown skills for autonomous ML research | 5.5k stars, cross-runtime |

## Dominant Workflow Patterns

1. **Single Pipeline** -- Rigid sequential (ideation -> experiment -> paper). Simple but brittle, no backtracking. (AI Scientist v1)
2. **Agentic Tree Search** -- Branching exploration with pruning of bad directions. (AI Scientist v2)
3. **Tournament Evolution** -- Hypotheses compete head-to-head; losers eliminated, winners evolved. (Google Co-Scientist)
4. **Role-Based Multi-Agent** -- Specialized agents (planner, researcher, critic, writer) with iterative loops. (NovelSeek, DORA, AstroAgents, this project)
5. **Markdown/Skill-Based** -- No framework lock-in; plain files define workflows across runtimes. Fastest-growing pattern. (ARIS, PhD-Zero, this project)

The consensus pipeline across all systems:

```
Ideation -> Literature Grounding -> Experiment Design ->
Code Execution -> Analysis -> Critique/Review -> Iteration -> Writing
```

The key differentiator is **single-pass vs. iterative critique loops**. 2025 consensus strongly favors iterative.

## Tool Ecosystem

| Category | Leaders |
|----------|---------|
| Literature Search | Semantic Scholar API, Elicit, Consensus, Scite |
| Paper QA/Retrieval | PaperQA2 (FutureHouse), OpenScholar |
| Report Generation | STORM (Stanford, 28k stars), GPT-Researcher |
| Multi-Agent Frameworks | LangGraph, AutoGen, CrewAI, Claude Agent SDK |
| Observability | Phoenix, Langfuse, AgentOps |

## Quality Control -- What Works

- **Separate generation from criticism** -- dedicated critic agents, not self-review (strongest consensus in the field)
- **Cross-model verification** -- different LLM for critique prevents confirmation bias (+13-44% improvement per VIRSCI)
- **Literature-in-the-loop** -- verify claims during critique cycle, not after. Use citation-aware tools (Scite, PaperQA2)
- **Deterministic verification** -- code execution, SymPy, convergence analysis >> LLM-based checking
- **Convergence tracking** -- score curves to detect structural problems (if issues don't decrease, stop and reconsider)

## Known Failure Modes

- **57% of AI Scientist v2 papers contain false data**, 42% of experiments fail from coding errors
- **Shallow literature search** -- median 5 citations in AI Scientist papers; well-known results classified as "novel"
- **LLM self-review is unreliable** -- too lenient on own output, too harsh on human papers
- **All systems limited to computational domains** -- no wet-lab capability without physical robotics

## Key Benchmarks

| Benchmark | What It Tests |
|-----------|--------------|
| **ScienceAgentBench** | Data-driven scientific discovery tasks (most rigorous) |
| **Auto-Bench** | Iterative knowledge updating, hypothesis identification |
| **LLM-SRBench** | Scientific equation discovery (guards against memorization) |
| **MLAgentBench** | ML research agent performance on real tasks |

## Emerging Trends

1. **"Co-Scientist" > "AI Scientist"** -- industry recalibrating from full autonomy to human-in-the-loop
2. **Cross-model verification becoming standard** -- Opus+Gemini, GPT-4+Claude, etc.
3. **Literature search remains the weakest link** -- no system matches domain expert contextual understanding
4. **Domain-specific agents outperform general ones** -- ChemCrow, FutureHouse (bio), Denario (astro)
5. **Observability is table stakes** -- tracing token costs, agent decisions, and verification outcomes
6. **Open-source closing the gap** -- PaperQA2 + STORM + custom critic composable into full pipelines

## How This Project Aligns

This project's architecture already implements several SOTA patterns:

| SOTA Pattern | This Project's Implementation |
|-------------|------------------------------|
| Role-based multi-agent | ideation, critic, developer, literature, verify-math agents |
| Adversarial criticism | Separate Opus critic instance with no ownership of ideas |
| Cross-model verification | Gemini for derivations, verify-math agent for checking |
| Literature-in-the-loop | Critic auto-invokes literature agent for claims |
| Convergence tracking | FATAL/HIGH score curve in active_criticism.md |
| Anti-hype protocol | Feasibility scorecards, "what would disprove this?" |
| Markdown/skill-based | Zero framework, works in Claude Code |

**Potential enhancements from SOTA:**
- Tournament evolution for hypothesis competition (Google Co-Scientist pattern)
- Agentic tree search with backtracking (AI Scientist v2 pattern)
- Evolving agent workflows that adapt tool/strategy over time (Mimosa, 2026)

---

*Sources: Web searches across arxiv, GitHub, product pages, and survey papers (Ferrag 2025, Gridach 2025, Ren 2025, Beel & Kan 2025). April 2026.*
