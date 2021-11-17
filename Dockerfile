FROM node:16 AS builder

COPY ./frontend/package.json ./frontend/package-lock.json /frontend_build/
ENV NODE_ENV=production
RUN npm ci --prefix /frontend_build

COPY ./frontend /frontend_build
RUN npm run build --prefix /frontend_build && \
    mkdir -p /app/static && \
    mv /frontend_build/out/* /app/static/ && \
    rm -rf /frontend_build

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

COPY --from=builder /frontend_build/out /app/static

RUN apt-get -y update && \
    apt-get --no-install-recommends -y install gcc && \
    apt-get --no-install-recommends -y install python3-dev graphviz libgraphviz-dev pkg-config && \
    rm -rf /var/lib/apt/lists/*

COPY ./backend/pyproject.toml ./backend/poetry.lock /app/
ENV PIP_NO_CACHE_DIR=1
RUN pip install -U pip poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction
COPY ./backend /app

RUN apt-get -y purge --auto-remove -o APT::AutoRemove::RecommendsImportant=false
