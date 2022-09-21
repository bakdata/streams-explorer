# Demo: ATM Fraud detection with streams-bootstrap

![demo-pipeline](https://github.com/bakdata/streams-explorer/blob/main/screens/demo-pipeline.png?raw=true)

> This is an adaption of the example pipeline for ATM fraud detection using [streams-bootstrap](https://github.com/bakdata/streams-bootstrap). The original by Confluent is written in KSQL and can be found in the [ksql-atm-fraud-detection](https://github.com/confluentinc/demo-scene/tree/master/ksql-atm-fraud-detection) repo. Details can be found in their [blogpost](https://www.confluent.io/blog/atm-fraud-detection-apache-kafka-ksql/)

## Usage

`cd demo-atm-fraud`

### Build containers using jib

```
gradle jib -Djib.to.image=url-to-container-registry.com/streams-explorer-demo-transactionavroproducer -Djib.container.mainClass=com.bakdata.kafka.TransactionAvroProducer
gradle jib -Djib.to.image=url-to-container-registry.com/streams-explorer-demo-transactionjoiner -Djib.container.mainClass=com.bakdata.kafka.TransactionJoiner
gradle jib -Djib.to.image=url-to-container-registry.com/streams-explorer-demo-frauddetector -Djib.container.mainClass=com.bakdata.kafka.FraudDetector
gradle jib -Djib.to.image=url-to-container-registry.com/streams-explorer-demo-accountlinker -Djib.container.mainClass=com.bakdata.kafka.AccountLinker
```

### Deploy in Kubernetes

```
helm repo add bakdata-common https://raw.githubusercontent.com/bakdata/streams-bootstrap/master/charts/
helm repo update
helm upgrade --debug --install --force --values values-transactionavroproducer.yaml demo-transactionavroproducer bakdata-common/streams-app
helm upgrade --debug --install --force --values values-transactionjoiner.yaml demo-transactionjoiner bakdata-common/streams-app
helm upgrade --debug --install --force --values values-frauddetector.yaml demo-frauddetector bakdata-common/streams-app
helm upgrade --debug --install --force --values values-accountlinker.yaml demo-accountlinker bakdata-common/streams-app
```

> port-forward leader Kafka broker and Schema Registry to localhost

> You can find the leader Kafka broker for a given topic by executing `kafka-topics --zookeeper localhost:2181 --describe --topic atm-fraud-accounts-topic`

### Generate test accounts

`python3 test-data/accounts.py`

```
kafka-avro-console-producer --broker-list localhost:9092 --topic atm-fraud-accounts-topic --property value.schema=$(cat src/main/avro/Account.avsc | tr -d '\040\011\012\015') --property schema.registry.url=http://localhost:8081 < test-data/accounts.txt
```

### Generate test transactions

To generate our incoming transactions (legitimate or fraudulent) we are using the [gess](https://github.com/rmoff/gess) tool. Once it's running we pipe the output from the UDP port to [kcat](https://github.com/edenhill/kcat) to write the individual messages to our input topic.

```
./gess.sh start
nc -v -u -l 6900 | kcat -b localhost:9092 -P -t atm-fraud-raw-input-topic
```
