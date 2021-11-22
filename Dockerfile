FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

ENV PIP_NO_CACHE_DIR=1 NODE_ENV=production

RUN apt-get -y update && \
    apt-get --no-install-recommends -y install gcc curl && \
    curl -sL https://deb.nodesource.com/setup_14.x | bash - && \
    apt-get --no-install-recommends -y install nodejs python3-dev graphviz libgraphviz-dev pkg-config && \
    rm -rf /var/lib/apt/lists/*

COPY ./backend/pyproject.toml ./backend/poetry.lock /app/
RUN pip install -U pip poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction
COPY ./backend /app

COPY ./frontend/package.json ./frontend/package-lock.json /frontend_build/
RUN npm ci --prefix /frontend_build

COPY ./frontend /frontend_build
RUN npm run build --prefix /frontend_build && \
    mkdir -p /app/static && \
    mv /frontend_build/out/* /app/static/ && \
    rm -rf /frontend_build

RUN apt-get -y purge --auto-remove -o APT::AutoRemove::RecommendsImportant=false
