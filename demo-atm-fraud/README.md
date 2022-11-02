# Demo: ATM Fraud detection with streams-bootstrap

![demo-pipeline](https://github.com/bakdata/streams-explorer/blob/main/screens/updated-demo-pipeline.png?raw=true)

> This is an adaption of the example pipeline for ATM fraud detection using [streams-bootstrap](https://github.com/bakdata/streams-bootstrap). The original by Confluent is written in KSQL and can be found in the [ksql-atm-fraud-detection](https://github.com/confluentinc/demo-scene/tree/master/ksql-atm-fraud-detection) repo. Details can be found in their [blogpost](https://www.confluent.io/blog/atm-fraud-detection-apache-kafka-ksql/)
>
> This version differs slightly from the original in that the test accounts are generated using a producer application.
> In addition, we turned the transactionavroproducer application into a producer application, eliminating the need to consume transactions data from an external producer.
> These minor changes allow us to have an automated deployment with no external intervention or manual data production.

## Usage

`cd demo-atm-fraud`

### Build containers using jib

```
gradle jib -Djib.to.image=url-to-container-registry.com/streams-explorer-demo-transactionavroproducer -Djib.container.mainClass=com.bakdata.kafka.TransactionAvroProducer
gradle jib -Djib.to.image=url-to-container-registry.com/streams-explorer-demo-accountproducer -Djib.container.mainClass=com.bakdata.kafka.AccountProducer
gradle jib -Djib.to.image=url-to-container-registry.com/streams-explorer-demo-transactionjoiner -Djib.container.mainClass=com.bakdata.kafka.TransactionJoiner
gradle jib -Djib.to.image=url-to-container-registry.com/streams-explorer-demo-frauddetector -Djib.container.mainClass=com.bakdata.kafka.FraudDetector
gradle jib -Djib.to.image=url-to-container-registry.com/streams-explorer-demo-accountlinker -Djib.container.mainClass=com.bakdata.kafka.AccountLinker
```

### Deploy in Kubernetes

```
helm repo add bakdata-common https://raw.githubusercontent.com/bakdata/streams-bootstrap/master/charts/
helm repo update
helm upgrade --debug --install --force --values values-transactionavroproducer.yaml demo-transactionavroproducer bakdata-common/streams-app
helm upgrade --debug --install --force --values values-accountproducer.yaml demo-accountproducer bakdata-common/streams-app
helm upgrade --debug --install --force --values values-transactionjoiner.yaml demo-transactionjoiner bakdata-common/streams-app
helm upgrade --debug --install --force --values values-frauddetector.yaml demo-frauddetector bakdata-common/streams-app
helm upgrade --debug --install --force --values values-accountlinker.yaml demo-accountlinker bakdata-common/streams-app
```
> port-forward leader Kafka broker and Schema Registry to localhost

> You can find the leader Kafka broker for a given topic by executing `kafka-topics --zookeeper localhost:2181 --describe --topic atm-fraud-accounts-topic`

### Generate test accounts

The account producer application publishes accounts data (stored in a `.txt` file)  into the expected topic. 


### Generate test transactions

To generate our incoming transactions (legitimate or fraudulent) we are using the `transactionavroproducer` application inspired by the [gess](https://github.com/rmoff/gess) tool. This project's data is derived entirely from the same gess project.

The number of incoming transactions is configurable using the variables `REAL_TX` and `ITERATION` in our `values-transactionavroproducer.yaml` file.
The first variable specifies how many legitimate incoming transactions must be produced before producing one fraudulent incoming transaction.
One iteration contains `REAL_TX` legitimate transactions and one fraudulent transaction.

