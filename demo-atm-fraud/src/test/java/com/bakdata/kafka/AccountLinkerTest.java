package com.bakdata.kafka;

import static org.assertj.core.api.Assertions.assertThat;

import com.bakdata.fluent_kafka_streams_tests.TestTopology;
import io.confluent.kafka.serializers.AbstractKafkaAvroSerDeConfig;
import java.util.List;
import java.util.Map;
import org.apache.avro.specific.SpecificRecord;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.jooq.lambda.Seq;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;

class AccountLinkerTest {

  private static final String INPUT_TOPIC = "INPUT";
  private static final String OUTPUT_TOPIC = "OUTPUT";
  private static final Map<String, String> EXTRA_INPUT_TOPICS = Map.of(
      "accounts", "ACCOUNTS"
  );
  private final AccountLinker accountLinker = createApp();
  private TestTopology<String, SpecificRecord> topology = null;

  private static AccountLinker createApp() {
    final AccountLinker accountLinker = new AccountLinker();
    accountLinker.setInputTopics(List.of(INPUT_TOPIC));
    accountLinker.setExtraInputTopics(EXTRA_INPUT_TOPICS);
    accountLinker.setOutputTopic(OUTPUT_TOPIC);
    return accountLinker;
  }

  @AfterEach
  void tearDown() {
    if (this.topology != null) {
      this.topology.stop();
    }
  }

  @Test
  void shouldCreateJoinedAccountTransaction() {
    this.start();

    final Account account = Account.newBuilder()
        .setAccountId("ac_03")
        .setFirstName("Foo")
        .setLastName("Bar")
        .setEmail("foo@bar.io")
        .setPhone("+123456789")
        .setAddress("123 Town Road")
        .setCountry("Atlantis")
        .build();

    this.topology
        .input(EXTRA_INPUT_TOPICS.get("accounts"))
        .add("", account);

    final Map<String, Transaction> transactions = TransactionBuilder.buildTestTransactionsMap();

    final JoinedTransaction joinedTransaction = JoinedTransaction
        .newBuilder()
        .setTransaction1(transactions.get("04"))
        .setTransaction2(transactions.get("X05"))
        .build();

    this.topology.input(INPUT_TOPIC).add("joinedTransaction", joinedTransaction);

    final List<ProducerRecord<String, JoinedAccountTransaction>> output = getOutput();
    assertThat(output)
        .hasSize(1)
        .allSatisfy(record -> {
          assertThat(record.value().getAccountId()).isEqualTo("ac_03");
          assertThat(record.value().getMinutesDifference()).isEqualTo(3);
        });
  }

  private void start() {
    this.topology = new TestTopology<>(p -> {
      this.accountLinker.setSchemaRegistryUrl(p.getProperty(AbstractKafkaAvroSerDeConfig.SCHEMA_REGISTRY_URL_CONFIG));
      return this.accountLinker.createTopology();
    }, this.accountLinker.getKafkaProperties());
    this.topology.start();
  }

  private List<ProducerRecord<String, JoinedAccountTransaction>> getOutput() {
    return Seq.seq(this.topology.streamOutput(this.accountLinker.getOutputTopic())
        .withValueType(JoinedAccountTransaction.class))
        .toList();
  }
}