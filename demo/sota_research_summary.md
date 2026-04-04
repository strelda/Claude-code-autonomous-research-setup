# SOTA Approaches to Agentic Academic Research

*Compiled: 2026-04-05*

## 1. The AI Scientist — Sakana AI / Oxford / UBC

**Key innovation:** First end-to-end automated scientific discovery pipeline that generates ideas, writes code, runs experiments, produces full papers, and self-reviews in a loop.

Generates complete ML research papers for ~$15 each. Uses an automated peer reviewer (near-human accuracy) to iteratively improve output. Open-ended: previous ideas feed the next generation of research. *(arxiv:2408.06292, Aug 2024)*

## 2. AI Co-Scientist — Google DeepMind (Gemini)

**Key innovation:** Multi-agent "generate, debate, and evolve" architecture with tournament-style hypothesis evolution, scaling quality via test-time compute.

Built on Gemini 2.0, it formulates novel research hypotheses aligned to scientist-provided objectives. Uses asynchronous task execution and a tournament evolution process for self-improving hypothesis generation. *(arxiv:2502.18864, Feb 2025)*

## 3. Deep Research — OpenAI

**Key innovation:** Extended autonomous web browsing and synthesis — the agent spends minutes to hours reading hundreds of sources before producing a comprehensive research report with citations.

Built on an o3-class reasoning model fine-tuned for browsing and analysis. Designed for literature review and multi-source synthesis rather than running experiments. *(Launched Jan 2025)*

## 4. PaSa (Paper Search Agent) — Peking University / Tsinghua / ByteDance

**Key innovation:** RL-trained agent that autonomously chains search, paper reading, and reference-following to achieve comprehensive academic paper retrieval far surpassing Google Scholar.

PaSa-7B exceeds the best Google-based baseline by ~38% recall@20. Trained on 35k fine-grained academic queries. Demonstrates that small RL-tuned models can outperform GPT-4o at agentic literature search. *(arxiv:2501.10120, Jan 2025)*

## 5. Search-o1 — Renmin University of China

**Key innovation:** Integrates agentic retrieval-augmented generation directly into chain-of-thought reasoning, with a "Reason-in-Documents" module that distills retrieved content before injection.

Addresses knowledge insufficiency in extended reasoning by dynamically retrieving external knowledge at uncertain reasoning steps, then deeply analyzing retrieved documents to minimize noise. Strong results across science, math, and coding tasks. *(arxiv:2501.05366, Jan 2025)*

---

## Common Themes

- **Multi-agent architectures** with specialized roles (generation, critique, retrieval)
- **Test-time compute scaling** — spending more inference cycles improves research quality
- **Closed-loop iteration** — generate, evaluate, refine rather than single-pass output
- **RL-based tool use** — training agents to autonomously decide when and how to search
- **Literature grounding** — all top systems integrate real paper retrieval to reduce hallucination
