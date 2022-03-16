# Streams Explorer

> Explore Data Pipelines in Apache Kafka.

![streams-explorer](https://github.com/bakdata/streams-explorer/blob/main/screens/overview.png?raw=true)

## Contents

- [Streams Explorer](#streams-explorer)
  - [Features](#features)
  - [Overview](#overview)
  - [Installation](#installation)
    - [Docker Compose](#docker-compose)
    - [Deploying to Kubernetes cluster](#deploying-to-kubernetes-cluster)
    - [Standalone](#standalone)
      - [Backend](#backend)
      - [Frontend](#frontend)
  - [Configuration](#configuration)
    - [Kafka](#kafka)
    - [Kafka Connect](#kafka-connect)
    - [Kubernetes](#kubernetes)
    - [Schema Registry / Karapace](#schema-registry--karapace)
    - [Prometheus](#prometheus)
    - [AKHQ](#akhq)
    - [Kowl](#kowl)
    - [Grafana](#grafana)
    - [Kibana](#kibana)
    - [Elasticsearch](#elasticsearch)
    - [Plugins](#plugins)
  - [Demo pipeline](#demo-pipeline)
  - [Plugin customization](#plugin-customization)

## Features

- Visualization of streaming applications, topics, and connectors
- Monitor all or individual pipelines from multiple namespaces
- Inspection of Avro schema from schema registry
- Integration with [streams-bootstrap](https://github.com/bakdata/streams-bootstrap) and [faust-bootstrap](https://github.com/bakdata/faust-bootstrap), or custom streaming app config parsing from Kubernetes deployments using plugins
- Real-time metrics from Prometheus (consumer lag & read rate, replicas, topic size, messages in & out per second, connector tasks)
- Linking to external services for logging and analysis, such as Kibana, Grafana, Loki, AKHQ, Kowl, and Elasticsearch
- Customizable through Python plugins

## Overview

Visit our introduction [blogpost](https://medium.com/bakdata/exploring-data-pipelines-in-apache-kafka-with-streams-explorer-8337dd11fdad) for a complete overview and demo of Streams Explorer.

## Installation

### Docker Compose

1. Forward the ports to Prometheus. (Kafka Connect, Schema Registry, and other integrations are optional)
2. Start the container

```sh
docker compose up
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

1. Install dependencies using [Poetry](https://python-poetry.org)

```sh
poetry install
```

2. Forward the ports to Prometheus. (Kafka Connect, Schema Registry, and other integrations are optional)
3. Configure the backend in [settings.yaml](backend/settings.yaml).
4. Start the backend server

```sh
poetry run start
```

#### Frontend

1. Install dependencies

```sh
npm ci
```

2. Start the frontend server

```sh
npm run build && npm run prod
```

Visit <http://localhost:3000>

## Configuration

Depending on your type of installation set the configuration for the backend server in this file:

- **Docker Compose**: [docker-compose.yaml](docker-compose.yaml)
- **Kubernetes**: [helm-chart/values.yaml](helm-chart/values.yaml)
- **standalone**: [backend/settings.yaml](backend/settings.yaml)

In the [helm-chart/values.yaml](helm-chart/values.yaml) configuration is done either through the `config` section using double underscore notation, e.g. `K8S__consumer_group_annotation: consumerGroup` or the content of [backend/settings.yaml](backend/settings.yaml) can be pasted under the `settings` section. Alternatively all configuration options can be written as environment variables using double underscore notation and the prefix `SE`, e.g. `SE_K8S__deployment__cluster=false`.

The following configuration options are available:

#### General

- `graph.update_interval` Update the graph every X seconds (integer, **required**, default: `300`)
- `graph.layout_arguments` Arguments passed to graphviz layout (string, **required**, default: `-Grankdir=LR -Gnodesep=0.8 -Gpad=10`)
- `graph.pipeline_distance` Increase/decrease vertical space between pipeline graphs by X pixels (int, **required**, default: `500`)

#### Kafka

- `kafka.enable` Enable Kafka (bool, default: `false`)
- `kafka.config` librdkafka configuration properties ([reference](https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md)) (dict, default: `{"bootstrap.servers": "localhost:9092"}`)
- `kafka.displayed_information` Configuration options of Kafka topics displayed in the frontend (list of dict)

#### Kafka Connect

- `kafkaconnect.url` URL of Kafka Connect server (string, default: None)
- `kafkaconnect.displayed_information` Configuration options of Kafka connectors displayed in the frontend (list of dict)

#### Kubernetes

- `k8s.deployment.cluster` Whether streams-explorer is deployed to Kubernetes cluster (bool, **required**, default: `false`)
- `k8s.deployment.context` Name of cluster (string, optional if running in cluster, default: `kubernetes-cluster`)
- `k8s.deployment.namespaces` Kubernetes namespaces (list of string, **required**, default: `['kubernetes-namespace']`)
- `k8s.containers.ignore` Name of containers that should be ignored/hidden (list of string, default: `['prometheus-jmx-exporter']`)
- `k8s.displayed_information` Details of pod that should be displayed (list of dict, default: `[{'name': 'Labels', 'key': 'metadata.labels'}]`)
- `k8s.labels` Labels used to set attributes of nodes (list of string, **required**, default: `['pipeline']`)
- `k8s.pipeline.label` Attribute of nodes the pipeline name should be extracted from (string, **required**, default: `pipeline`)
- `k8s.consumer_group_annotation` Annotation the consumer group name should be extracted from (string, **required**, default: `consumerGroup`)

#### Schema Registry / Karapace

- `schemaregistry.url` URL of Confluent Schema Registry or Karapace (string, default: None)

#### Prometheus

- `prometheus.url` URL of Prometheus (string, **required**, default: `http://localhost:9090`)

The following exporters are required to collect Kafka metrics for Prometheus:

- [Kafka Exporter](https://github.com/danielqsj/kafka_exporter)
- [Kafka Lag Exporter](https://github.com/lightbend/kafka-lag-exporter)
- [Kafka Connect Exporter](https://github.com/wakeful/kafka_connect_exporter)

#### AKHQ

- `akhq.enable` Enable AKHQ (bool, default: `false`)
- `akhq.url` URL of AKHQ (string, default: `http://localhost:8080`)
- `akhq.cluster` Name of cluster (string, default: `kubernetes-cluster`)
- `akhq.connect` Name of connect (string, default: None)

#### Kowl

Kowl can be used instead of AKHQ. (mutually exclusive)

- `kowl.enable` Enable Kowl (bool, default: `false`)
- `kowl.url` URL of Kowl (string, default: `http://localhost:8080`)

#### Grafana

- `grafana.enable` Enable Grafana (bool, default: `false`)
- `grafana.url` URL of Grafana (string, default: `http://localhost:3000`)
- `grafana.dashboards.topics` Path to topics dashboard (string), sample dashboards for topics and consumer groups are included in the [`./grafana`](https://github.com/bakdata/streams-explorer/tree/main/grafana) subfolder
- `grafana.dashboards.consumergroups` Path to consumer groups dashboard (string)

#### Kibana

- `kibanalogs.enable` Enable Kibana logs (bool, default: `false`)
- `kibanalogs.url` URL of Kibana logs (string, default: `http://localhost:5601`)

#### Loki

Loki can be used instead of Kibana. (mutually exclusive)

- `loki.enable` Enable Loki logs (bool, default: `false`)
- `loki.url` URL of Loki logs (string, default: `http://localhost:3000`)

#### Elasticsearch

for Kafka Connect Elasticsearch connector

- `esindex.url` URL of Elasticsearch index (string, default: `http://localhost:5601/app/kibana#/dev_tools/console`)

#### Plugins

- `plugins.path` Path to folder containing plugins relative to backend (string, **required**, default: `./plugins`)
- `plugins.extractors.default` Whether to load default extractors (bool, **required**, default: `true`)

## Demo pipeline

![demo-pipeline](https://github.com/bakdata/streams-explorer/blob/main/screens/demo-pipeline.png?raw=true)

[ATM Fraud detection with streams-bootstrap](https://github.com/bakdata/streams-explorer/blob/main/demo-atm-fraud/README.md)

## Plugin customization

It is possible to create your own config parser, linker, metric provider, and extractors in Python by implementing the `K8sConfigParser`, `LinkingService`, `MetricProvider`, or `Extractor` classes. This way you can customize it to your specific setup and services. As an example we provide the [`DefaultLinker`](https://github.com/bakdata/streams-explorer/blob/main/backend/streams_explorer/defaultlinker.py) as `LinkingService`. The default [`MetricProvider`](https://github.com/bakdata/streams-explorer/blob/main/backend/streams_explorer/core/services/metric_providers.py) supports Prometheus. Furthermore the following default `Extractor` plugins are included:

- [`ElasticsearchSink`](https://github.com/bakdata/streams-explorer/blob/main/backend/streams_explorer/core/extractor/default/elasticsearch_sink.py)
- [`JdbcSink`](https://github.com/bakdata/streams-explorer/blob/main/backend/streams_explorer/core/extractor/default/jdbc_sink.py)
- [`S3Sink`](https://github.com/bakdata/streams-explorer/blob/main/backend/streams_explorer/core/extractor/default/s3_sink.py)
- [`GenericSink`/`GenericSource`](https://github.com/bakdata/streams-explorer/blob/main/backend/streams_explorer/core/extractor/default/generic.py)

If your streaming application deployments are configured through environment variables, following the schema of [streams-bootstrap](https://github.com/bakdata/streams-bootstrap) or [faust-bootstrap](https://github.com/bakdata/faust-bootstrap), the Streams Explorer works out-of-the-box with the default deployment parser.
For streams-bootstrap deployments configured through CLI arguments a separate parser can be loaded by creating a Python file (e.g. `config_parser.py`) in the plugins folder with the following import statement:

```python
from streams_explorer.core.k8s_config_parser import StreamsBootstrapArgsParser
```

For other setups a custom config parser plugin can be created by inheriting from the [`K8sConfigParser`](https://github.com/bakdata/streams-explorer/blob/main/backend/streams_explorer/core/k8s_config_parser.py) class and implementing the `parse` method. In this example we're retrieving the streaming app configurations from an external REST API. In order for a deployment to be indentified as streaming app, input and output topics are required.

```python
import httpx

from streams_explorer.core.k8s_config_parser import K8sConfigParser
from streams_explorer.models.k8s_config import K8sConfig


class CustomConfigParser(K8sConfigParser):
    def get_name(self) -> str:
        name = self.k8s_app.metadata.name
        if not name:
            raise TypeError(f"Name is required for {self.k8s_app.get_class_name()}")
        return name

    def parse(self) -> K8sConfig:
        """Retrieve app config from REST endpoint."""
        name = self.get_name()
        data = httpx.get(f"url/config/{name}").json()
        return K8sConfig(**data)
```
