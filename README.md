# Streams Explorer

Backend and Frontend to explore Data Pipelines in Apache Kafka.

## Getting Started

### How to use it locally

#### Backend

Install dependencies:
`pip install requirements.txt`

Forward ports for the Schema Registry, the Confluent Control Center, and Kafka Connect.

Configure the backend in `settings.yaml`.

Start the backend server with:

```
uvicorn main:app
```

#### Frontend

Install dependencies:

`npm install`

Start the server:

`npm start`

### How to deploy it to a Kubernetes cluster

```
helm repo add streams-explorer https://raw.githubusercontent.com/bakdata/streams-explorer/master/helm-chart/
helm install --values helm-chart/values.yaml streams-explorer
```
