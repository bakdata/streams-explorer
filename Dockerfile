# build stage 1: frontend
FROM node:16 AS frontend

WORKDIR /build
COPY ./frontend/package.json ./frontend/package-lock.json /build/
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm ci

COPY ./frontend /build
RUN npm run build

# build stage 2: backend
FROM python:3.10-slim

RUN apt-get -y update && \
    apt-get --no-install-recommends -y install gcc graphviz libgraphviz-dev pkg-config && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./backend/pyproject.toml ./backend/poetry.lock /app/
ENV PIP_NO_CACHE_DIR=1
RUN pip install -U pip poetry && \
    poetry config virtualenvs.create false && \
    poetry install --without=dev --no-interaction
COPY ./backend /app

# install streams_explorer package
RUN pip install -e .

RUN apt-get -y purge --auto-remove -o APT::AutoRemove::RecommendsImportant=false

COPY --from=frontend /build/out /app/static

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
