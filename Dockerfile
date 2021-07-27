FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

ENV PIP_NO_CACHE_DIR=1

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

COPY ./frontend/package.json ./frontend/package-lock.json /frontend/
RUN npm ci --production --prefix /frontend

COPY ./frontend /frontend
RUN npm run build --prefix /frontend && \
    mkdir -p /app/static && \
    mv /frontend/build/* /app/static/ && \
    rm -rf /frontend

RUN apt-get -y purge --auto-remove -o APT::AutoRemove::RecommendsImportant=false && \
    apt-get -y purge --auto-remove python2-minimal && \
    rm -rf /usr/lib/python2.7
