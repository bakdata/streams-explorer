# build stage 1: frontend
FROM node:24 AS frontend

WORKDIR /build
COPY ./frontend/package.json ./frontend/package-lock.json /build/
ENV NEXT_TELEMETRY_DISABLED=1
# We need the libraries ,because of canvas https://github.com/Automattic/node-canvas/issues/1662
RUN apt-get -y update && \
    apt-get -y install gcc build-essential libcairo2-dev libpango1.0-dev libjpeg-dev libgif-dev librsvg2-dev
RUN npm ci

COPY ./frontend /build
RUN npm run build

# build stage 2: backend
FROM python:3.10-slim AS backend
COPY --from=ghcr.io/astral-sh/uv:0.13.4 /uv /uvx /bin/

RUN apt-get -y update && \
    apt-get --no-install-recommends -y install libc6-dev gcc libgraphviz-dev

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_DEV=1 \
    UV_PROJECT_ENVIRONMENT=/app/venv

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=backend/uv.lock,target=uv.lock \
    --mount=type=bind,source=backend/pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

COPY ./backend /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

FROM python:3.10-slim AS prod

RUN apt-get -y update && \
    apt-get --no-install-recommends -y install graphviz && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=backend /app/venv /app/venv
COPY --from=frontend /build/out /app/static
ENV PATH=/app/venv/bin:$PATH
COPY ./backend /app

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
