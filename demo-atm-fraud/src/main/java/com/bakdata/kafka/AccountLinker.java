package com.bakdata.kafka;

import java.time.Duration;
import java.util.Properties;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.KeyValue;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.kstream.KStream;
import org.apache.kafka.streams.kstream.KTable;
import org.elasticsearch.common.geo.GeoDistance;
import org.elasticsearch.common.unit.DistanceUnit;

public class AccountLinker extends KafkaStreamsApplication {

  public static void main(final String[] args) {
    startApplication(new AccountLinker(), args);
  }

  private static JoinedAccountTransaction join(final JoinedTransaction joinedTransaction, final Account account) {
    final Transaction t1 = joinedTransaction.getTransaction1();
    final Transaction t2 = joinedTransaction.getTransaction2();

    final Duration timeDifference =
        Duration.between(
            t1.getTimestamp(),
            t2.getTimestamp()).abs();

    final double distance = GeoDistance.ARC.calculate(
        t1.getLocation().getLatitude(),
        t1.getLocation().getLongitude(),
        t2.getLocation().getLatitude(),
        t2.getLocation().getLongitude(),
        DistanceUnit.KILOMETERS);

    final double hoursBetween = (double) timeDifference.toSeconds() / 3600;
    final double kmhRequired = distance / hoursBetween;

    return JoinedAccountTransaction
        .newBuilder()
        .setAccountId(account.getAccountId())
        .setCustomerName(
            String.format(
                "%s %s", account.getFirstName(), account.getLastName()
            )
        )
        .setCustomerEmail(account.getEmail())
        .setCustomerPhone(account.getPhone())
        .setCustomerAddress(account.getAddress())
        .setCustomerCountry(account.getCountry())
        .setTransaction1(t1)
        .setTransaction2(t2)
        .setDistanceBetweenTxnKm(distance)
        .setMinutesDifference(timeDifference.toMinutes())
        .setKmhRequired(kmhRequired)
        .build();
  }

  @Override
  public void buildTopology(final StreamsBuilder builder) {
    final KStream<String, JoinedTransaction> transactionsKStream = builder.stream(this.getInputTopics());
    final KStream<String, JoinedTransaction> transactionsRekeyedKStream = transactionsKStream
        .map((k, v) -> KeyValue.pair(v.getTransaction1().getAccountId(), v));

    final KStream<String, Account> accountsKStream = builder.stream(this.getInputTopic("accounts"));
    final KStream<String, Account> accountsRekeyedKStream = accountsKStream
        .map((k, v) -> KeyValue.pair(v.getAccountId(), v));

    final KTable<String, Account> accountsKTable = accountsRekeyedKStream
        .groupByKey()
        .reduce((previousValue, newValue) -> newValue);

    final KStream<String, JoinedAccountTransaction> joined = transactionsRekeyedKStream
        .join(accountsKTable, AccountLinker::join);

    joined.to(this.getOutputTopic());
  }

  @Override
  public String getUniqueAppId() {
    return "streams-explorer-accountlinker-" + this.getOutputTopic();
  }

  @Override
  protected Properties createKafkaProperties() {
    final Properties kafkaProperties = super.createKafkaProperties();
    kafkaProperties.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.StringSerde.class);
    return kafkaProperties;
  }
}
