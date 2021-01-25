# Streams Explorer

> Explore Data Pipelines in Apache Kafka.

![streams-explorer](screens/streams-explorer.png)

## Contents

- [Features](#features)
- [Installation](#installation)
  - [Docker Compose](#docker-compose)
  - [Deploying to Kubernetes cluster](#deploying-to-kubernetes-cluster)
  - [Standalone](#standalone)
- [Configuration](#configuration)
- [Demo pipeline](#demo-pipeline)
- [Plugin customization](#plugin-customization)

## Features

- Visualization of streaming applications and topics
- Monitor all or individual pipelines from multiple namespaces
- Inspection of Avro schema from schema registry
- Integration with [streams-bootstrap](https://github.com/bakdata/streams-bootstrap) and [faust-bootstrap](https://github.com/bakdata/faust-bootstrap) for deploying Kafka Streams applications
- Real-time metrics from Prometheus (consumer lag, topic size, messages in/out per second)
- Linking to external services for logging and analysis, such as Kibana, Grafana, AKHQ, Elasticsearch
- Customizable through Python plugins

## Installation

### Docker Compose

1. Forward the ports to Kafka Connect, Schema Registry, and Prometheus. (other integrations are optional)
2. Start the container

```sh
docker-compose up
```

Once the container is started visit <http://localhost:3000>

### Deploying to Kubernetes cluster

1. Add the Helm chart repository

```sh
helm repo add streams-explorer https://raw.githubusercontent.com/bakdata/streams-explorer/master/helm-chart/
```

2. Install

```sh
helm upgrade --install --values helm-chart/values.yaml streams-explorer
```

### Standalone

#### Backend

1. Install dependencies

```sh
pip install -r requirements.txt
```

2. Forward the ports to Kafka Connect, Schema Registry, and Prometheus. (other integrations are optional)
3. Configure the backend in [settings.yaml](backend/settings.yaml).
4. Start the backend server

```sh
uvicorn main:app
```

#### Frontend

1. Install dependencies

```sh
npm install
```

2. Start the frontend server

```sh
npm start
```

Visit <http://localhost:3000>

## Configuration

Depending on your type of installation set the configuration for the backend server in this file:

- **Docker Compose**: [docker-compose.yaml](docker-compose.yaml)
- **Kubernetes**: [helm-chart/values.yaml](helm-chart/values.yaml)
- **standalone**: [backend/settings.yaml](backend/settings.yaml)

All configuration options can be written as environment variables using underscore notation and the prefix `SE`, e.g. `SE_K8S__deployment__cluster=false`.

The following configuration options are available:

#### Kafka Connect

- `kafkaconnect.url` URL of Kafka Connect server (string, **required**, default: `http://localhost:8083`)
- `kafkaconnect.displayed_information` Configuration options of Kafka connectors displayed in the frontend (list of dict, **required**, default: `[{'name': 'Transformer', 'key': 'transforms.changeTopic.regex'}]`)

#### Kubernetes

- `k8s.deployment.cluster` Whether streams-explorer is deployed to Kubernetes cluster (bool, **required**, default: `false`)
- `k8s.deployment.context` Name of cluster (string, optional if running in cluster, default: `kubernetes-cluster`)
- `k8s.deployment.namespaces` Kubernetes namespaces (list of string, **required**, default: `['kubernetes-namespace']`)
- `k8s.containers.ignore` Name of containers that should be ignored/hidden (list of string, default: `['prometheus-jmx-exporter']`)
- `k8s.displayed_information` Details of pod that should be displayed (list of dict, default: `[{'name': 'Labels', 'key': 'metadata.labels'}]`)
- `k8s.labels` Labels used to set attributes of nodes (list of string, **required**, default: `['pipeline']`)
- `k8s.independent_graph.label` Attribute of nodes the pipeline name should be extracted from (string, **required**, default: `pipeline`)

#### Schema Registry

- `schemaregistry.url` URL of Schema Registry (string, **required**, default: `http://localhost:8081`)

#### Prometheus

- `prometheus.url` URL of Prometheus (string, **required**, default: `http://localhost:9090`)

#### AKHQ

- `akhq.url` URL of AKHQ (string, default: `http://localhost:8080`)
- `akhq.cluster` Name of cluster (string, default: `kubernetes-cluster`)

#### Grafana

- `grafana.url` URL of Grafana (string, default: `http://localhost:3000`)
- `grafana.dashboard` Path to dashboard (string)

#### Kibana

- `kibanalogs.url` URL of Kibana logs (string, default: `http://localhost:5601`)

#### Elasticsearch

for Kafka Connect Elasticsearch connector
- `esindex.url` URL of Elasticsearch index (string, default: `http://localhost:5601/app/kibana#/dev_tools/console`)

#### Plugins

- `plugins.path` Path to folder containing plugins relative to backend (string, **required**, default: `./plugins`)
- `plugins.extractors.default` Whether to load default extractors (bool, **required**, default: `true`)

## Demo pipeline

[ATM Fraud detection with streams-bootstrap](https://github.com/bakdata/streams-explorer/blob/main/demo-atm-fraud/README.md)

## Plugin customization

It is possible to create your own linker and extractors in Python by implementing the `LinkingService` or `Extractor` classes. This way you can customize it to your specific setup and services. As an example we provide the [DefaultLinker](https://github.com/bakdata/streams-explorer/blob/main/backend/streams_explorer/defaultlinker.py) and [ElasticsearchSink](https://github.com/bakdata/streams-explorer/blob/main/backend/streams_explorer/core/extractor/default/elasticsearch_sink.py) classes which are used by default.
