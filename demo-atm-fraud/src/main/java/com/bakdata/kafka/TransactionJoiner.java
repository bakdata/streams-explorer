package com.bakdata.kafka;

import java.time.Duration;
import java.util.Properties;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.KeyValue;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.kstream.JoinWindows;
import org.apache.kafka.streams.kstream.KStream;

public class TransactionJoiner extends KafkaStreamsApplication {

    public static void main(final String[] args) {
        startApplication(new com.bakdata.kafka.TransactionJoiner(), args);
    }

    @Override
    public void buildTopology(final StreamsBuilder builder) {
        final KStream<String, Transaction> input = builder.stream(this.getInputTopics());
        final KStream<String, Transaction> mapped = input
                .map((k, v) -> KeyValue.pair(v.getAccountId(), v));

        final KStream<String, JoinedTransaction> joined = mapped
                .join(mapped,
                        (t1, t2) -> JoinedTransaction
                                .newBuilder()
                                .setTransaction1(t1)
                                .setTransaction2(t2)
                                .build(),
                        JoinWindows.of(Duration.ofMinutes(10)).before(Duration.ZERO));

        joined.to(this.getOutputTopic());
    }

    @Override
    public String getUniqueAppId() {
        return "streams-explorer-transactionjoiner-" + this.getOutputTopic();
    }

    @Override
    protected Properties createKafkaProperties() {
        final Properties kafkaProperties = super.createKafkaProperties();
        kafkaProperties.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.StringSerde.class);
        return kafkaProperties;
    }
}
