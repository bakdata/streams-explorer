package com.bakdata.kafka;

import java.util.Properties;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.kstream.KStream;

public class FraudDetector extends KafkaStreamsApplication {

  public static void main(final String[] args) {
    startApplication(new FraudDetector(), args);
  }

  private static boolean isPotentiallyFraudulentTransaction(final String k, final JoinedTransaction joinedTransaction) {
    final Transaction t1 = joinedTransaction.getTransaction1();
    final Transaction t2 = joinedTransaction.getTransaction2();

    return (!t1.getTransactionId().equals(t2.getTransactionId()))
        && (!t1.getAtm().equals(t2.getAtm()))
        && (t1.getTimestamp().compareTo(t2.getTimestamp()) > 0)
        && (t1.getLocation().getLatitude() != t2.getLocation().getLatitude()
        || t1.getLocation().getLongitude() != t2.getLocation().getLongitude());
  }

  @Override
  public void buildTopology(final StreamsBuilder builder) {
    final KStream<String, JoinedTransaction> inputKStream = builder.stream(this.getInputTopics());

    final KStream<String, JoinedTransaction> possibleFraudTransactions = inputKStream
        .filter(FraudDetector::isPotentiallyFraudulentTransaction);

    possibleFraudTransactions.to(this.getOutputTopic());
  }

  @Override
  public String getUniqueAppId() {
    return "streams-explorer-frauddetector-" + this.getOutputTopic();
  }

  @Override
  protected Properties createKafkaProperties() {
    final Properties kafkaProperties = super.createKafkaProperties();
    kafkaProperties.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.StringSerde.class);
    return kafkaProperties;
  }
}
