# bakdata/streams-explorer-base
FROM python:3.9-slim

RUN apt-get -y update && \
    apt-get --no-install-recommends -y install gcc python3-dev graphviz libgraphviz-dev pkg-config && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get -y purge --auto-remove -o APT::AutoRemove::RecommendsImportant=false
