# Base Arguements to leverage across build stages
ARG APP_DIR=/app

#############
# Build (Prepare Environment) image
#############
FROM python:3.10-slim-buster AS build
ARG APP_DIR

# build dependencies from the askwiki README
RUN apt-get update && apt-get install -y \
  curl \
  build-essential \
  libffi-dev \
  && rm -rf /var/lib/apt/lists/*
  
# install poetry and add to path 
ENV POETRY_VERSION=1.3.2
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH /root/.local/bin:$PATH

# change work directory for where our app will live
WORKDIR ${APP_DIR}
COPY pyproject.toml poetry.lock ./

# Copy over the venv including any symbolic links, do not install development/testing libraries when install poetry dependencies
RUN python -m venv --copies ${APP_DIR}/venv
RUN . ${APP_DIR}/venv/bin/activate && poetry install --no-dev


#############
# Deployment image
#############
FROM python:3.10-slim-buster AS prod
ARG APP_DIR

COPY --from=build ${APP_DIR}/venv ${APP_DIR}/venv/
ENV PATH ${APP_DIR}/venv/bin:$PATH

WORKDIR ${APP_DIR}/
COPY  . ./

HEALTHCHECK --start-period=30s CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=2)"

CMD ["uvicorn", "askwiki.main:app", "--host", "0.0.0.0", "--port", "8000"]
