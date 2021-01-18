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

class FraudDetectorTest {

  private static final String INPUT_TOPIC = "INPUT";
  private static final String OUTPUT_TOPIC = "OUTPUT";
  private final FraudDetector fraudDetector = createApp();
  private TestTopology<String, JoinedTransaction> topology = null;

  private static FraudDetector createApp() {
    final FraudDetector fraudDetector = new FraudDetector();
    fraudDetector.setInputTopics(List.of(INPUT_TOPIC));
    fraudDetector.setOutputTopic(OUTPUT_TOPIC);
    return fraudDetector;
  }

  @AfterEach
  void tearDown() {
    if (this.topology != null) {
      this.topology.stop();
    }
  }

  @Test
  void shouldFindFraudulent() {
    this.start();

    Map<String, Transaction> transactions = TransactionBuilder.buildTestTransactionsMap();

    JoinedTransaction genuineJoinedTransaction = JoinedTransaction
        .newBuilder()
        .setTransaction1(transactions.get("03"))
        .setTransaction2(transactions.get("02"))
        .build();
    this.topology.input().add("", genuineJoinedTransaction);

    JoinedTransaction fraudulentJoinedTransaction = JoinedTransaction
        .newBuilder()
        .setTransaction1(transactions.get("X05"))
        .setTransaction2(transactions.get("02"))
        .build();
    this.topology.input().add("", fraudulentJoinedTransaction);

    final List<ProducerRecord<String, JoinedTransaction>> output = getOutput();

    assertThat(output)
        .hasSize(1)
        .allSatisfy(record ->
            assertThat(record.value()).isEqualTo(
                JoinedTransaction
                    .newBuilder()
                    .setTransaction1(transactions.get("X05"))
                    .setTransaction2(transactions.get("02"))
                    .build()
            ));
  }

  private void start() {
    this.topology = new TestTopology<>(p -> {
      this.fraudDetector.setSchemaRegistryUrl(p.getProperty(AbstractKafkaAvroSerDeConfig.SCHEMA_REGISTRY_URL_CONFIG));
      return this.fraudDetector.createTopology();
    }, this.fraudDetector.getKafkaProperties());
    this.topology.start();
  }

  private List<ProducerRecord<String, JoinedTransaction>> getOutput() {
    return Seq.seq(this.topology.streamOutput(this.fraudDetector.getOutputTopic())
        .withValueType(JoinedTransaction.class))
        .toList();
  }
}