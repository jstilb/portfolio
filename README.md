# Portfolio

[![GitHub](https://img.shields.io/badge/GitHub-jstilb-181717.svg?logo=github)](https://github.com/jstilb)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

Data science and AI engineering portfolio spanning traditional machine learning foundations through modern AI systems. Projects demonstrate end-to-end skills from statistical inference and NLP research to production RAG pipelines, agentic orchestration, and LLM evaluation.

## Technology Map

```
                        Portfolio Skill Coverage

    Traditional ML & Data Science          Modern AI Engineering
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~          ~~~~~~~~~~~~~~~~~~~~~~

    Statistical Inference                  RAG Pipelines
      - hypothesis testing                   - hybrid retrieval (semantic + BM25)
      - causal regression                    - chunking strategies
      - experiment design                    - evaluation metrics

    NLP & Text Analysis                    Agentic Systems
      - bias detection (DeBERTa)             - state machine orchestration
      - knowledge graphs + LLMs              - multi-agent coordination
      - fake news classification             - quality review loops

    ML Engineering                         Context Engineering
      - big data (Spark/MapReduce)           - MCP server implementation
      - model deployment (AKS)               - tool/resource/prompt primitives
      - structured ML projects               - provider dependency injection

    Evaluation & Governance                LLM Evaluation
      - human-centered metrics               - 9 custom metrics
      - responsible AI playbooks             - LLM-as-judge pattern
      - ethical measurement design           - faithfulness verification
```

## Featured Repositories

### Modern AI Engineering

| Repository | Description | Stack | Tests |
|------------|-------------|-------|-------|
| [modern-rag-pipeline](https://github.com/jstilb/modern-rag-pipeline) | Production RAG with hybrid search (semantic + BM25 + RRF), 4 chunking strategies, and IR evaluation | Python, ChromaDB, FastAPI | 109 tests |
| [mcp-toolkit-server](https://github.com/jstilb/mcp-toolkit-server) | MCP server with 5 tools, 3 resources, 3 prompts, and provider DI | TypeScript, MCP SDK, Zod | 64 tests |
| [agent-orchestrator](https://github.com/jstilb/agent-orchestrator) | Multi-agent system with state machine coordination and quality review loop | Python, LangGraph, FastAPI | 31 tests |
| [llm-eval-framework](https://github.com/jstilb/llm-eval-framework) | LLM evaluation with 9 metrics, LLM-as-judge, pairwise comparison | Python, FastAPI, Hypothesis | 102 tests |

### AI Governance & Evaluation

| Repository | Description | Stack |
|------------|-------------|-------|
| [meaningful_metrics](https://github.com/jstilb/meaningful_metrics) | Open-source evaluation frameworks, human-centered metrics, AI evaluation playbooks | Python, Responsible AI |

### Traditional ML & Data Science

| Project | Domain | Techniques |
|---------|--------|------------|
| [chatgpt-knowledge-graph-query-qa](chatgpt-knowledge-graph-query-qa/) | NLP | Knowledge graphs, ChatGPT, WikiData Q&A |
| [sentence-level-bias-detection-nlp-paper](sentence-level-bias-detection-nlp-paper/) | NLP | DeBERTa fine-tuning, bias detection |
| [covid-hypothesis-testing-statistical-analysis](covid-hypothesis-testing-statistical-analysis/) | Statistics | Hypothesis testing, survey analysis |
| [vax-travel-causal-regression-analysis](vax-travel-causal-regression-analysis/) | Statistics | Causal inference, regression |
| [flight-prediction-using-big-data](flight-prediction-using-big-data/) | Big Data | Spark, MapReduce, flight prediction |
| [fake-news-proliferation-analysis](fake-news-proliferation-analysis/) | NLP | Network analysis, misinformation |
| [fake-news-simulation-ooo-programming](fake-news-simulation-ooo-programming/) | Simulation | OOP design, agent-based modeling |
| [ml-sysems-engineering](ml-sysems-engineering/) | MLOps | AKS deployment, model serving |
| [job-bot-nlp-project](job-bot-nlp-project/) | NLP | Web scraping, skill extraction |
| [info-consumption-research-design-proposal](info-consumption-research-design-proposal/) | Research | Experiment design, research methodology |

## Portfolio Balance

| Category | Repositories | Coverage |
|----------|-------------|----------|
| Traditional ML & Data Science | 10 projects | 40% |
| Modern AI Engineering | 5 projects (306 tests) | 40% |
| AI Governance & Evaluation | 1 project (spans both) | 20% |
| **Effective Split** | **Traditional: 40% / Modern: 60%** | **Target: 40/60** |

All modern AI repos include CI/CD pipelines, Docker support, architecture documentation, ADRs, and mock mode for zero-dependency demos.

## Skills Matrix

| Skill | Demonstrated In | Level |
|-------|----------------|-------|
| Python | All repos | Advanced |
| TypeScript | mcp-toolkit-server | Advanced |
| RAG Pipelines | modern-rag-pipeline | Production |
| Vector Databases | modern-rag-pipeline (ChromaDB) | Production |
| Agentic Systems | agent-orchestrator | Production |
| MCP / Context Engineering | mcp-toolkit-server | Production |
| LLM Evaluation | llm-eval-framework, meaningful_metrics | Production |
| NLP / Transformers | bias-detection, knowledge-graph-qa | Research |
| Statistical Inference | covid-hypothesis, vax-travel | Research |
| Big Data (Spark) | flight-prediction | Applied |
| ML Deployment | ml-sysems-engineering (AKS) | Applied |
| FastAPI | 4 repos | Production |
| Docker / CI/CD | All modern repos | Production |
| TDD / Testing | 306 tests across modern repos | Production |

## Education

**UC Berkeley** -- Master of Information and Data Science (MIDS)

## License

All original code in this portfolio is MIT licensed unless otherwise noted. See individual repository LICENSE files for details.
