# Project: ML Pipeline Toolkit

## Skill Tier: 1
## Skills Demonstrated: MLOps, Data Engineering, CI/CD for ML, Model Serving, Pipeline Orchestration, Experiment Tracking
## Priority Score: 8

## Summary
An end-to-end machine learning pipeline toolkit that takes data from raw ingestion through feature engineering, model training, evaluation, and serving. Demonstrates production MLOps practices including versioned datasets, experiment tracking, automated retraining, and model deployment behind an API. Built around a real-world prediction task to show practical value rather than toy examples.

## Technical Approach

**Core Libraries & Tools:**
- **Pipeline:** DVC (Data Version Control) for data/model versioning, or Prefect for workflow orchestration
- **Training:** scikit-learn for baseline, PyTorch for advanced models
- **Experiment Tracking:** MLflow for metrics, parameters, and artifacts
- **Serving:** FastAPI for model API, with optional BentoML packaging
- **Data Quality:** Great Expectations for data validation
- **CI/CD:** GitHub Actions for automated pipeline runs
- **Infrastructure:** Docker for reproducibility

**Architecture:**
```
Raw Data -> DVC Versioning -> Data Validation (Great Expectations)
    |
    v
Feature Engineering -> Feature Store (local parquet files)
    |
    v
Training Pipeline -> Experiment Tracking (MLflow) -> Model Registry
    |
    v
Evaluation Pipeline -> Metrics Dashboard -> Promotion Decision
    |
    v
Serving (FastAPI) -> Health Checks -> Monitoring
```

**Real-World Task:**
- Predict housing prices, customer churn, or credit risk (well-understood domains)
- Use publicly available dataset (UCI, Kaggle)
- Focus is on the pipeline, not the model complexity

**Key Features:**
1. Data versioning with DVC (track datasets alongside code)
2. Automated data quality checks before training
3. Experiment tracking with MLflow (parameters, metrics, artifacts)
4. Model registry with staging/production promotion
5. FastAPI serving endpoint with input validation
6. GitHub Actions CI that runs full pipeline on PR
7. Makefile with standard targets: `make data`, `make train`, `make serve`, `make test`

## Success Criteria
- Pipeline runs end-to-end with single command (`make all`)
- Data changes trigger automatic retraining via CI
- MLflow dashboard shows experiment history with comparable runs
- Model API responds in <100ms for single predictions
- Data validation catches schema violations and drift
- Pipeline recovers gracefully from failures (idempotent stages)
- Documentation includes pipeline diagram and operational runbook

## Estimated Effort
- **Week 1:** Data pipeline (ingestion, validation, feature engineering), training loop, MLflow integration
- **Week 2:** Serving API, CI/CD pipeline, Docker, documentation
- **Total:** 2 weeks

## Repository Structure
```
ml-pipeline-toolkit/
├── README.md                    # Overview, pipeline diagram, quickstart
├── LICENSE                      # MIT
├── Makefile                     # Standard pipeline targets
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml           # MLflow server + API
├── .github/
│   └── workflows/
│       ├── ci.yml               # Lint, test
│       └── pipeline.yml         # Full pipeline run on data changes
├── dvc.yaml                     # DVC pipeline definition
├── dvc.lock                     # DVC pipeline lock file
├── params.yaml                  # Hyperparameters (tracked by DVC)
├── src/
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── ingest.py            # Data download/ingestion
│   │   ├── validate.py          # Great Expectations checks
│   │   └── features.py          # Feature engineering
│   ├── training/
│   │   ├── __init__.py
│   │   ├── train.py             # Training script
│   │   ├── evaluate.py          # Evaluation metrics
│   │   └── registry.py          # Model promotion logic
│   ├── serving/
│   │   ├── __init__.py
│   │   ├── app.py               # FastAPI application
│   │   ├── schemas.py           # Request/response models
│   │   └── health.py            # Health check endpoints
│   └── monitoring/
│       ├── __init__.py
│       └── drift.py             # Data drift detection
├── tests/
│   ├── test_data.py
│   ├── test_training.py
│   ├── test_serving.py
│   └── test_pipeline.py         # Integration test (full pipeline)
├── data/
│   ├── raw/                     # Raw data (DVC tracked)
│   ├── processed/               # Feature-engineered (DVC tracked)
│   └── .gitignore               # Ignore large data files
├── models/                      # Trained models (DVC tracked)
├── notebooks/
│   └── exploration.ipynb        # EDA notebook
└── docs/
    ├── pipeline.md              # Pipeline architecture
    └── runbook.md               # Operational guide
```
