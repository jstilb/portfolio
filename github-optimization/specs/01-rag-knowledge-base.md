# Project: RAG Knowledge Base

## Skill Tier: 2
## Skills Demonstrated: RAG, Vector Databases, Embeddings, Context Engineering, Information Retrieval, LLM Integration
## Priority Score: 10

## Summary
A production-quality Retrieval-Augmented Generation system that indexes a corpus of documents (technical documentation, research papers, or personal knowledge base), stores embeddings in a vector database, and provides an intelligent Q&A interface with source attribution. Demonstrates the full RAG pipeline from ingestion to generation with measurable retrieval quality.

## Technical Approach

**Core Libraries & Tools:**
- **Embeddings:** OpenAI `text-embedding-3-small` or Ollama local embeddings (`nomic-embed-text`)
- **Vector DB:** ChromaDB (local, easy setup) with optional Pinecone deployment
- **LLM:** Claude API via PAI inference tool (standard tier for generation)
- **Framework:** LangChain or LlamaIndex for orchestration
- **Chunking:** Recursive text splitting with overlap, semantic chunking as advanced option
- **Evaluation:** RAGAS framework for retrieval quality metrics (context precision, faithfulness, answer relevance)

**Architecture:**
```
Documents -> Chunker -> Embedder -> Vector DB (ChromaDB)
                                        |
User Query -> Embedder -> Similarity Search -> Context Assembly -> LLM -> Response + Sources
```

**Data Sources (choose one focus):**
- Option A: Technical documentation corpus (e.g., Python stdlib docs)
- Option B: Research paper collection (ArXiv subset)
- Option C: Custom knowledge base (markdown files, like PAI's own docs but sanitized)

**Key Features:**
1. Document ingestion pipeline with multiple format support (PDF, MD, TXT)
2. Configurable chunking strategies (fixed-size, recursive, semantic)
3. Hybrid search (dense + sparse retrieval)
4. Source attribution with confidence scores
5. Evaluation suite using RAGAS metrics
6. CLI interface for all operations

## Success Criteria
- Retrieval precision > 0.85 on evaluation dataset (measured by RAGAS)
- Faithfulness score > 0.90 (answers grounded in retrieved context)
- Sub-2-second query latency for local deployment
- Handles 10,000+ document chunks without performance degradation
- Clean CLI: `rag ingest ./docs`, `rag query "How does X work?"`
- All metrics reported in README with reproducible benchmark script

## Estimated Effort
- **Week 1:** Core pipeline (ingestion, embedding, retrieval, generation)
- **Week 2:** Evaluation framework, hybrid search, CLI polish, documentation
- **Total:** 2 weeks

## Repository Structure
```
rag-knowledge-base/
├── README.md                    # Project overview, architecture diagram, benchmarks
├── LICENSE                      # MIT
├── pyproject.toml               # Python project config
├── Dockerfile                   # Reproducible environment
├── .github/
│   └── workflows/
│       └── ci.yml               # Lint, test, benchmark
├── src/
│   ├── __init__.py
│   ├── cli.py                   # CLI entry point
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── loader.py            # Document loaders (PDF, MD, TXT)
│   │   ├── chunker.py           # Chunking strategies
│   │   └── embedder.py          # Embedding generation
│   ├── retrieval/
│   │   ├── __init__.py
│   │   ├── vector_store.py      # ChromaDB interface
│   │   ├── hybrid_search.py     # Dense + sparse retrieval
│   │   └── reranker.py          # Result reranking
│   ├── generation/
│   │   ├── __init__.py
│   │   ├── prompt_templates.py  # RAG prompt engineering
│   │   └── generator.py         # LLM response generation
│   └── evaluation/
│       ├── __init__.py
│       ├── metrics.py           # RAGAS metrics wrapper
│       └── benchmark.py         # Benchmark runner
├── tests/
│   ├── test_ingestion.py
│   ├── test_retrieval.py
│   ├── test_generation.py
│   └── test_evaluation.py
├── data/
│   └── sample/                  # Sample documents for demo
├── notebooks/
│   └── rag_demo.ipynb           # Interactive walkthrough
└── benchmarks/
    └── results.md               # Latest benchmark results
```
