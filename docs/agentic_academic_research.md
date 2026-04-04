# State of the Art: Agentic Academic Research Systems

*Survey date: April 2026*

---

## 1. Landmark Systems

### AI Scientist v1 (Sakana AI, 2024)

The first fully automated open-ended scientific discovery system [1]. Automates the complete research pipeline: idea generation, experiment execution, paper writing, and LLM-based peer review. Cost per paper is approximately $6–15 with ~3.5 hours of human involvement [1]. Now peer-reviewed and published in Nature (March 2026) [2]. Uses a single-agent pipeline with rigid template-based phases — no iterative self-critique loop [1].

### AI Scientist v2 (Sakana AI, 2025)

Replaces the rigid pipeline with **agentic tree search**, enabling flexible non-linear exploration of the research hypothesis space [3]. Removes reliance on human-authored templates. Claims workshop-level paper quality, with the first AI-generated paper accepted through peer review [3]. However, independent evaluation found **57% of AI Scientist v2 papers contain false data** [4], and 42% of proposed experiments failed due to coding errors [5].

### Google AI Co-Scientist (DeepMind, 2025)

Multi-agent collaboration framework built on Gemini 2.0 [6]. Positioned as a "co-scientist" rather than full automation, emphasizing human-AI collaboration [6]. Uses **tournament-style evaluation** where hypotheses compete against each other. Validated in biomedical domains, generating novel hypotheses for epigenetic targets in anti-fibrotic therapies [6]. Goes beyond literature summarization into integrated knowledge retrieval [6]. 412 citations as of April 2026.

### ARIS — Auto Research in Sleep (2025)

Lightweight markdown-only skills for autonomous ML research [7]. Cross-model review loops where one LLM reviews another's work. Score curves track quantitative improvement over critic→fix iterations [7]. Zero dependencies — works with Claude Code, Codex, or any LLM agent runtime. 5,479 stars on GitHub [7].

### AgentRxiv (2025)

Collaborative multi-agent framework where LLM agents work together as a research community, building on each other's work [8]. Models a population of AI researchers rather than a single research pipeline. 53 citations [8].

### VIRSCI (2025)

Multi-agent system simulating collaborative scientific research teams [9]. Demonstrated that multi-agent systems produce more novel, higher-influence ideas compared to single-agent approaches, with +13.8% to +44.1% improvement in alignment with research goals [9].

---

## 2. Emerging Systems

| System | Architecture | Key Innovation | Ref |
|--------|-------------|----------------|-----|
| **AI-Researcher** | Multi-agent | Dedicated Documentation Agent for LLM coherence across long research processes | [10] |
| **DORA** | Multi-agent virtual research team | Role-specialized agents for exploration, discovery, and report generation | [11] |
| **EvoScientist** | Multi-agent evolving | Agents continuously improve research strategies through evolution | [12] |
| **infiAgent (MLA)** | Multi-level hierarchy | Days-long continuous execution with crash recovery and persistent memory | [13] |
| **open-coscientist-agents** | Multi-agent tournament | ELO rating system for hypothesis ranking with debate transcripts | [14] |
| **AutoDidact** | RL self-improvement | Trains the agent itself via GRPO reinforcement learning; doubled accuracy 23%→59% in 1 hour | [15] |
| **Denario** | Multi-agent (AG2 + LangGraph) | Won first place at NeurIPS 2025 competition for astrophysics research | [16] |
| **PhD-Zero** | Skill-based multi-runtime | Plan→gather→experiment→review→write workflow, compatible with Claude Code and Codex | [17] |
| **ResearcherSkill** | Single markdown file | Hypothesis-driven keep/discard experimentation loop; 30+ experiments overnight | [18] |

---

## 3. Surveys and Reviews

Several comprehensive surveys have mapped the landscape:

- Ferrag et al. (2025) provide a review covering advanced reasoning strategies, failure modes in multi-agent LLM systems, and automated scientific research across 2024–2025 [19].
- Gridach et al. (2025) survey LLM-driven agents across chemistry, biology, and materials science, covering evaluation metrics, datasets, and challenges including literature review automation and system reliability [20].
- Ren et al. (2025) connect multimodal scientific data perception with agent autonomy, surveying building blocks for scientific agent systems [21].
- Zheng et al. (EMNLP 2025) categorize scientific discovery into levels of autonomy and describe virtual environments for LLM-based simplified research [22].
- Sapkota (2025) provides a multi-dimensional comparison of single-agent to multi-agent transitions, with 424 citations [23].

---

## 4. Architectural Patterns

### Single Pipeline (Template-Based)

Used by AI Scientist v1 [1]. Rigid sequential phases with no backtracking. Simple to implement but cannot recover from bad early decisions. No iterative critique — automated review is post-hoc scoring only [5].

### Agentic Tree Search

Used by AI Scientist v2 [3]. Explores the hypothesis space via branching, enabling non-linear exploration and pruning of bad directions. More structured than manual ideation but less adversarial than dedicated critic agents [3].

### Multi-Agent Tournament

Used by Google AI Co-Scientist [6] and open-coscientist-agents [14]. Hypotheses compete head-to-head with ELO-style ranking. Reflection agents critique, evolution agents refine. More rigorous than linear ranking but compute-heavy [6][14].

### Generate-Reflect-Evolve Loop

Used by open-coscientist (Jataware) [24] and VIRSCI [9]. Closest to the ideation→criticism→iteration pattern. One agent generates structured hypotheses, another selectively falsifies them [9][24].

### Markdown Skill Files

Used by ARIS [7], ResearcherSkill [18], and PhD-Zero [17]. Zero-framework approach — plain markdown files define workflows. Most lightweight and portable. Works across multiple LLM runtimes [7][17][18].

### Multi-Level Agent Hierarchy

Used by infiAgent [13] and Denario [16]. Hierarchical orchestration with persistent state across sessions. Handles longer tasks but requires more infrastructure [13].

### Single-Agent vs. Multi-Agent Comparison

| Feature | Single Agent | Multi-Agent |
|---------|-------------|-------------|
| Best for | Well-defined, low-complexity tasks | Complex, open-ended, multidisciplinary tasks |
| Strengths | Low latency, efficiency, lower cost | Higher innovation, critical review, robust verification |
| Weaknesses | Prone to hallucinations, limited reasoning | 4–220x higher token cost, potential groupthink |
| Examples | PaperQA, ChemCrow, GPT-Researcher | VIRSCI, Google Co-Scientist, DORA |

Multi-agent systems outperform single-agent by +13.8% to +44.1% in alignment with research goals [9]. However, as individual LLMs improve, this gap may narrow [23]. The 2025 consensus favors a **hybrid approach**: single agents for tool execution and verification, multi-agent for creative brainstorming [23].

---

## 5. Known Failure Modes

### Literature Search is Shallow

All current systems rely on simplistic keyword searches rather than deep synthesis [5]. AI Scientist v1 uses basic Semantic Scholar keyword search, widely criticized as inadequate [5]. Papers generated have a median of only 5 citations, most outdated — only 5 of 34 from 2020+ [5]. This leads to poor novelty assessments: well-known concepts like micro-batching for SGD were classified as "novel" [5].

### Code Execution is Fragile

42% of proposed experiments (5/12) failed due to coding errors in AI Scientist evaluation [5]. Experiments that ran often produced logically flawed or misleading results — one experiment claimed energy efficiency improvements while consuming more resources [5]. Code modifications were minimal, averaging ~8% more characters per iteration [5].

### Hallucinated Numerical Results

57% of AI Scientist v2 papers contain false data according to independent evaluation [4]. Writing quality across systems shows missing figures, repeated sections, placeholder text ("Conclusions Here"), and hallucinated numerical results [5]. Quality described as comparable to "an unmotivated undergraduate student rushing to meet a deadline" [5].

### LLM Self-Review is Unreliable Alone

LLM-based reviewers are overly critical on human papers, rejecting papers that human reviewers approved [5]. Near-human accuracy claims for automated review are overstated [5]. Same-model self-review suffers from confirmation bias — the model tends to approve its own output [9].

### Domain Restriction

All current systems are limited to fields reliant on data analysis and simulations [5]. No system can perform wet-lab experiments; computational-only domains are required [5].

---

## 6. Best Practices for Verification and Criticism

### Separate Generation from Criticism

Leading systems use dedicated critic/reviewer agents separate from generators [6][9][14]. Same-model self-review alone is insufficient due to confirmation bias [9]. Cross-model verification (e.g., one LLM generates, a different LLM critiques) is emerging as best practice to prevent echo-chamber effects [7].

### Iterative Loops Over Single-Pass Review

The core pattern across SOTA systems is **Generate → Review → Refine** with iteration [6][14][24]. Google AI Co-Scientist uses tournament-style evaluation where hypotheses compete [6]. AI Scientist v2 uses agentic tree search to explore multiple paths and prune failures [3]. Single-pass post-hoc review (as in AI Scientist v1) is insufficient [5].

### Deterministic Verification Where Possible

Formal verification outperforms LLM-based checking: code execution, math proof checkers, symbolic computation engines (SymPy, Mathematica) serve as verification oracles [20]. The emerging pattern is **verification-in-the-loop** where formal checkers are integrated into the agent cycle rather than applied post-hoc [20].

### Literature-Aware Novelty Checking

Best practice: use retrieval-augmented generation with citation-aware tools (Scite Smart Citations, PaperQA2) rather than keyword search [5][20]. No system reliably synthesizes literature at the level of a domain expert — this remains the weakest link [5][20].

---

## 7. How This Project Compares

### Already Well-Aligned with SOTA

- **Dedicated adversarial critic agent** matches the consensus that generation and criticism must be separated [6][9][14]
- **Cross-model verification via Gemini** follows the emerging best practice of different-model critique [7]
- **Anti-hype protocol** directly addresses the most criticized failure mode (over-claiming novelty) [5]
- **Literature reality check before criticism** follows the Beel & Kan recommendation [5]
- **Markdown-only skill approach** matches ARIS [7], ResearcherSkill [18], and PhD-Zero [17]

### Unique Features (Not Found in Surveyed Systems)

- **Feasibility scorecards** per research direction with quantified difficulty, cost, timeline, and probability
- **"What would save this?"** documentation for killed directions, preventing revisitation of dead ends
- **Structured criticism with severity levels** (FATAL/HIGH/MEDIUM/SMALL) and tracked IDs with resolution logging
- **Gemini CLI for math verification** addresses a gap most systems have — no other surveyed system has dedicated mathematical derivation verification

### Potential Improvements from SOTA

| Pattern | Source | Application |
|---------|--------|-------------|
| Tournament/ELO ranking | open-coscientist-agents [14] | Replace linear ranking in `summary.md` with head-to-head hypothesis competition |
| Agentic tree search | AI Scientist v2 [3] | Formalize branching exploration in ideation phase |
| Score curves | ARIS [7] | Track quantitative improvement metrics across critic→fix cycles |
| Crash recovery | infiAgent [13] | Resume long-running sessions after interruption |
| Hypothesis evolution | Google AI Co-Scientist [6] | Iteratively mutate and refine hypotheses rather than generating fixed set |

---

## References

[1] C. Lu, C. Lu, R.T. Lange, J. Foerster, J. Clune. "The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery." arXiv:2408.06292, 2024.

[2] C. Lu et al. "The AI Scientist." Nature, March 2026.

[3] Y. Yamada, R.T. Lange, C. Lu, S. Hu, C. Lu et al. "The AI Scientist-v2: Workshop-Level Automated Scientific Discovery via Agentic Tree Search." arXiv:2504.08066, 2025.

[4] byteiota.com. "Independent Evaluation of AI Scientist v2 Data Integrity." March 2026.

[5] J. Beel, M.Y. Kan. "Is The AI Scientist Actually Doing Science?" arXiv:2502.14297, 2025.

[6] J. Gottweis, W.H. Weng, A. Daryin, T. Tu, A. Palepu et al. "Towards an AI Co-Scientist." arXiv:2502.18864, 2025.

[7] wanshuiyin. "Auto-claude-code-research-in-sleep (ARIS)." GitHub, 2025. https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep

[8] S. Schmidgall, M. Moor. "AgentRxiv: Towards Collaborative Autonomous Research." arXiv:2503.18102, 2025.

[9] H. Su et al. "VIRSCI: Multi-Agent Collaborative Scientific Research." OpenReview, 2025.

[10] J. Tang, L. Xia, Z. Li, C. Huang. "AI-Researcher: Autonomous Scientific Innovation." arXiv:2505.18705, 2025.

[11] V. Naumov, D. Zagirova, S. Lin, Y. Xie et al. "DORA AI Scientist: Multi-Agent Virtual Research Team." bioRxiv, 2025.

[12] Y. Lyu, X. Zhang, X. Yi, Y. Zhao, S. Guo, W. Hu et al. "EvoScientist: Multi-Agent Evolving AI Scientists for End-to-End Scientific Discovery." arXiv:2603.08127, 2026.

[13] polyuiislab. "infiAgent (MLA)." GitHub, 2025. https://github.com/polyuiislab/infiAgent

[14] conradry. "open-coscientist-agents." GitHub, 2025. https://github.com/conradry/open-coscientist-agents

[15] dCaples. "AutoDidact." GitHub, 2025. https://github.com/dCaples/AutoDidact

[16] AstroPilot-AI. "Denario." GitHub, 2025. https://github.com/AstroPilot-AI/Denario

[17] TenureAI. "PhD-Zero." GitHub, 2025. https://github.com/TenureAI/PhD-Zero

[18] krzysztofdudek. "ResearcherSkill." GitHub, 2025. https://github.com/krzysztofdudek/ResearcherSkill

[19] M.A. Ferrag, N. Tihanyi, M. Debbah. "From LLM Reasoning to Autonomous AI Agents: A Comprehensive Review." arXiv:2504.19678, 2025.

[20] M. Gridach, J. Nanavati et al. "Agentic AI for Scientific Discovery: A Survey of Progress, Challenges, and Future Directions." arXiv:2503.08979, 2025.

[21] S. Ren, C. Xie, P. Jian, Z. Ren et al. "Towards Scientific Intelligence: A Survey of LLM-Based Scientific Agents." arXiv:2503.24047, 2025.

[22] T. Zheng, Z. Deng, H.T. Tsang, W. Wang et al. "From Automation to Autonomy: A Survey of LLMs in Scientific Discovery." EMNLP 2025.

[23] S. Sapkota. "AI Agents vs. Agentic AI: A Conceptual Taxonomy." ScienceDirect, 2025.

[24] jataware. "open-coscientist." GitHub, 2025. https://github.com/jataware/open-coscientist
