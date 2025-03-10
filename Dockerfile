# build stage 1: frontend
FROM node:16 AS frontend

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

RUN apt-get -y update && \
    apt-get --no-install-recommends -y install libc6-dev gcc libgraphviz-dev

WORKDIR /app

COPY ./backend/pyproject.toml ./backend/poetry.lock /app/
ENV PIP_NO_CACHE_DIR=1
RUN pip install poetry==1.8.5 && \
    python -m venv --copies /app/venv && \
    . /app/venv/bin/activate && \
    poetry install --without=dev --no-interaction

FROM python:3.10-slim AS prod

RUN apt-get -y update && \
    apt-get --no-install-recommends -y install graphviz && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=backend /app /app
COPY --from=frontend /build/out /app/static
ENV PATH=/app/venv/bin:$PATH
COPY ./backend /app

# install streams_explorer package
RUN pip install -e .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
