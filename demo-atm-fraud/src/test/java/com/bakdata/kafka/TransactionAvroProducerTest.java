package com.bakdata.kafka;

import static org.assertj.core.api.Assertions.assertThat;

import com.bakdata.fluent_kafka_streams_tests.TestTopology;
import io.confluent.kafka.serializers.AbstractKafkaAvroSerDeConfig;
import java.time.Instant;
import java.util.List;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.Serdes;
import org.jooq.lambda.Seq;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;

class TransactionAvroProducerTest {

  private static final String INPUT_TOPIC = "INPUT";
  private static final String OUTPUT_TOPIC = "OUTPUT";
  private static final String ERROR_TOPIC = "ERROR";
  private final TransactionAvroProducer TransactionAvroProducer = createApp();
  private TestTopology<String, String> topology = null;

  private static TransactionAvroProducer createApp() {
    final TransactionAvroProducer TransactionAvroProducer = new TransactionAvroProducer();
    TransactionAvroProducer.setInputTopics(List.of(INPUT_TOPIC));
    TransactionAvroProducer.setOutputTopic(OUTPUT_TOPIC);
    TransactionAvroProducer.setErrorTopic(ERROR_TOPIC);
    return TransactionAvroProducer;
  }

  @AfterEach
  void tearDown() {
    if (this.topology != null) {
      this.topology.stop();
    }
  }

  @Test
  void shouldConvertToAvro() {
    this.start();

    final String json =
        "{"
            + "  \"account_id\": \"a305\","
            + "  \"timestamp\": \"2020-12-07 11:15:42 +0000\","
            + "  \"atm\": \"Sainsbury's\","
            + "  \"amount\": 200,"
            + "  \"location\": { \"lat\": \"53.7009145\", \"lon\": \"-1.7779015\" },"
            + "  \"transaction_id\": \"29611f28-3875-11eb-8aa9-a45e60d000a3\""
            + "}";

    this.topology.input()
        .withValueSerde(Serdes.String())
        .add("key", json);

    final List<ProducerRecord<String, Transaction>> output = getOutput();
    final List<ProducerRecord<String, ProcessingError>> errors = getErrors();

    assertThat(errors)
        .isEmpty();
    assertThat(output)
        .hasSize(1)
        .allSatisfy(record ->
            assertThat(record.value()).isEqualTo(
                Transaction
                    .newBuilder()
                    .setAccountId("a305")
                    .setTransactionId("29611f28-3875-11eb-8aa9-a45e60d000a3")
                    .setTimestamp(Instant.ofEpochMilli(1607339742000L))
                    .setAtm("Sainsbury's")
                    .setAmount(200)
                    .setLocationBuilder(
                        Location
                            .newBuilder()
                            .setLatitude(53.7009145)
                            .setLongitude(-1.7779015))
                    .build()
            ));
  }

  private void start() {
    this.topology = new TestTopology<>(p -> {
      this.TransactionAvroProducer.setSchemaRegistryUrl(p.getProperty(AbstractKafkaAvroSerDeConfig.SCHEMA_REGISTRY_URL_CONFIG));
      return this.TransactionAvroProducer.createTopology();
    }, this.TransactionAvroProducer.getKafkaProperties());
    this.topology.start();
  }

  private List<ProducerRecord<String, Transaction>> getOutput() {
    return Seq.seq(this.topology.streamOutput(this.TransactionAvroProducer.getOutputTopic())
        .withValueType(Transaction.class))
        .toList();
  }

  private List<ProducerRecord<String, ProcessingError>> getErrors() {
    return Seq.seq(this.topology.streamOutput(this.TransactionAvroProducer.getErrorTopic())
        .withValueType(ProcessingError.class))
        .toList();
  }
}