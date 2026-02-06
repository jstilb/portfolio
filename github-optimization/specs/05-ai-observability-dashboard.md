# Project: AI Observability Dashboard

## Skill Tier: 3
## Skills Demonstrated: AI Observability, LLM Monitoring, Compound AI Systems, Real-time Dashboards, Production AI, Metrics Design
## Priority Score: 7

## Summary
A real-time observability dashboard for LLM-powered applications that tracks latency, token usage, cost, quality scores, error rates, and drift across model calls. Designed for teams running production AI systems who need visibility into what their LLMs are actually doing. Includes a lightweight SDK for instrumenting applications and a web dashboard for visualization. This is a rare portfolio differentiator -- most engineers can build ML models, few can monitor them in production.

## Technical Approach

**Core Libraries & Tools:**
- **Language:** TypeScript (dashboard + SDK), Python bindings for ML teams
- **Runtime:** Bun for backend services
- **Dashboard:** Next.js or SvelteKit with real-time updates (SSE or WebSockets)
- **Storage:** SQLite (via Turso or local) for event storage, time-series optimized
- **Charts:** D3.js or Chart.js for visualizations
- **SDK:** Lightweight wrapper (~100 lines) that instruments LLM calls
- **Testing:** Vitest + Playwright for dashboard E2E tests

**Architecture:**
```
Your LLM App -> SDK (instruments calls) -> Event Collector API
                                              |
                                              v
                                     SQLite Event Store
                                              |
                                              v
                                     Analytics Engine
                                     (aggregations, anomaly detection)
                                              |
                                              v
                                     Web Dashboard (real-time)
                                     - Latency percentiles
                                     - Token usage / cost
                                     - Quality score trends
                                     - Error rate tracking
                                     - Model comparison
```

**Key Features:**
1. **Lightweight SDK:** 2-line integration for any LLM call (wrap existing calls)
2. **Event Collection:** Async, non-blocking event ingestion API
3. **Core Metrics Dashboard:**
   - Latency (p50, p95, p99) with time-series charts
   - Token usage and estimated cost per model/endpoint
   - Error rates with categorized failure modes
   - Quality scores (if user provides ratings/evaluations)
4. **Anomaly Detection:** Simple statistical anomaly flagging (z-score on latency, cost)
5. **Model Comparison:** Side-by-side metrics for A/B testing different models
6. **Export:** CSV/JSON export of all metrics for external analysis
7. **Self-hosted:** Runs locally, no cloud dependencies, no data leaves your machine

## Success Criteria
- SDK adds <5ms overhead per instrumented LLM call
- Dashboard renders real-time updates within 1 second of event receipt
- Handles 10,000+ events without performance degradation
- Anomaly detection correctly flags latency spikes (>2 standard deviations)
- Dashboard loads in <2 seconds on first visit
- Setup requires <5 minutes (single Docker command)
- Documentation includes screenshots of dashboard with real data

## Estimated Effort
- **Week 1:** SDK, event collector API, SQLite storage, core analytics
- **Week 2:** Web dashboard, real-time updates, anomaly detection, documentation
- **Total:** 1-2 weeks

## Repository Structure
```
ai-observability/
├── README.md                    # Overview, screenshots, quickstart
├── LICENSE                      # MIT
├── package.json
├── tsconfig.json
├── Dockerfile
├── docker-compose.yml           # One-command setup
├── .github/
│   └── workflows/
│       └── ci.yml               # Lint, test, build
├── sdk/
│   ├── typescript/
│   │   ├── package.json
│   │   ├── src/
│   │   │   ├── index.ts         # SDK entry point
│   │   │   ├── instrument.ts    # LLM call wrapper
│   │   │   ├── collector.ts     # Event batching and sending
│   │   │   └── types.ts         # Event schema types
│   │   └── tests/
│   │       └── sdk.test.ts
│   └── python/
│       ├── pyproject.toml
│       ├── ai_observability/
│       │   ├── __init__.py
│       │   ├── instrument.py    # Python SDK
│       │   └── types.py
│       └── tests/
│           └── test_sdk.py
├── server/
│   ├── src/
│   │   ├── index.ts             # Server entry point
│   │   ├── api/
│   │   │   ├── ingest.ts        # Event ingestion endpoint
│   │   │   ├── query.ts         # Analytics query endpoint
│   │   │   └── export.ts        # CSV/JSON export
│   │   ├── storage/
│   │   │   ├── schema.ts        # SQLite schema
│   │   │   ├── events.ts        # Event persistence
│   │   │   └── aggregations.ts  # Pre-computed aggregations
│   │   ├── analytics/
│   │   │   ├── metrics.ts       # Metric calculations
│   │   │   ├── anomaly.ts       # Anomaly detection
│   │   │   └── comparison.ts    # Model A/B comparison
│   │   └── realtime/
│   │       └── sse.ts           # Server-sent events for dashboard
│   └── tests/
│       ├── ingest.test.ts
│       ├── analytics.test.ts
│       └── anomaly.test.ts
├── dashboard/
│   ├── src/
│   │   ├── app/                 # Next.js/SvelteKit app
│   │   ├── components/
│   │   │   ├── LatencyChart.tsx
│   │   │   ├── CostTracker.tsx
│   │   │   ├── ErrorRate.tsx
│   │   │   ├── QualityTrend.tsx
│   │   │   └── ModelComparison.tsx
│   │   └── lib/
│   │       ├── api.ts           # Dashboard API client
│   │       └── realtime.ts      # SSE connection
│   └── tests/
│       └── dashboard.test.ts    # Playwright E2E
├── examples/
│   ├── basic-usage/             # Minimal integration example
│   ├── multi-model/             # Comparing Claude vs GPT
│   └── production-setup/        # Full production config
└── docs/
    ├── setup.md                 # Installation guide
    ├── sdk-reference.md         # SDK API documentation
    └── screenshots/             # Dashboard screenshots
```
