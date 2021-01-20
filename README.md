# Streams Explorer

> Explore Data Pipelines in Apache Kafka.

![streams-explorer](screens/streams-explorer.png)

## Features

- Visualization of streaming applications and topics
- Monitor all or individual pipelines from namespace
- Inspection of Avro schema from schema registry
- Real-time metrics from Prometheus (consumer lag, topic size, messages in/out per second)
- Integration with external services for logging and analysis like Kibana or Grafana
- Customizable through Python plugins

## Installation

### Docker

```sh
docker-compose up
```

- Once the container is started visit <http://localhost:3000>

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

2. Forward the ports to Schema Registry, Confluent Control Center, and Kafka Connect.
3. Configure the backend in `settings.yaml`.
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

**TODO**

- Configuration of the backend is done either through `settings.yaml` (standalone), `helm-chart/values.yaml` (Kubernetes) or environment variables (all).

or

- Depending on your type of installation use these methods to configure the backend server:
  - **Docker Compose**: `docker-compose.yaml`
  - **Kubernetes**: `helm-chart/values.yaml`
  - **standalone**: `backend/settings.yaml`
