package com.bakdata.kafka;

import static org.assertj.core.api.Assertions.assertThat;

import com.bakdata.fluent_kafka_streams_tests.TestTopology;
import io.confluent.kafka.serializers.AbstractKafkaAvroSerDeConfig;
import java.util.List;
import java.util.Map;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.jooq.lambda.Seq;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;

class TransactionJoinerTest {

  private static final String INPUT_TOPIC = "INPUT";
  private static final String OUTPUT_TOPIC = "OUTPUT";
  private final TransactionJoiner transactionJoiner = createApp();
  private TestTopology<String, Transaction> topology = null;

  private static TransactionJoiner createApp() {
    final TransactionJoiner transactionJoiner = new TransactionJoiner();
    transactionJoiner.setInputTopics(List.of(INPUT_TOPIC));
    transactionJoiner.setOutputTopic(OUTPUT_TOPIC);
    return transactionJoiner;
  }

  @AfterEach
  void tearDown() {
    if (this.topology != null) {
      this.topology.stop();
    }
  }

  @Test
  void shouldJoinTransactions() {
    this.start();

    Map<String, Transaction> transactions = TransactionBuilder.buildTestTransactionsMap();

    for (Map.Entry<String, Transaction> entry : transactions.entrySet()) {
      this.topology.input()
          .add(entry.getKey(), entry.getValue());
    }

    final List<ProducerRecord<String, JoinedTransaction>> output = getOutput();

    assertThat(output)
        .anySatisfy(record ->
            assertThat(record.value()).isEqualTo(
                JoinedTransaction
                    .newBuilder()
                    .setTransaction1(transactions.get("04"))
                    .setTransaction2(transactions.get("X05"))
                    .build()
            ));
  }

  private void start() {
    this.topology = new TestTopology<>(p -> {
      this.transactionJoiner.setSchemaRegistryUrl(p.getProperty(AbstractKafkaAvroSerDeConfig.SCHEMA_REGISTRY_URL_CONFIG));
      return this.transactionJoiner.createTopology();
    }, this.transactionJoiner.getKafkaProperties());
    this.topology.start();
  }

  private List<ProducerRecord<String, JoinedTransaction>> getOutput() {
    return Seq.seq(this.topology.streamOutput(this.transactionJoiner.getOutputTopic())
        .withValueType(JoinedTransaction.class))
        .toList();
  }
}