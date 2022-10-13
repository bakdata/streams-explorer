package com.bakdata.kafka.integration;

import static net.mguenther.kafka.junit.EmbeddedKafkaCluster.provisionWith;
import static net.mguenther.kafka.junit.EmbeddedKafkaClusterConfig.defaultClusterConfig;
import static net.mguenther.kafka.junit.Wait.delay;
import static org.assertj.core.api.Assertions.assertThat;

import com.bakdata.kafka.Transaction;
import com.bakdata.kafka.TransactionAvroProducer;
import com.bakdata.schemaregistrymock.junit5.SchemaRegistryMockExtension;
import io.confluent.kafka.schemaregistry.client.SchemaRegistryClient;
import io.confluent.kafka.schemaregistry.client.rest.exceptions.RestClientException;
import io.confluent.kafka.serializers.AbstractKafkaSchemaSerDeConfig;
import io.confluent.kafka.streams.serdes.avro.SpecificAvroDeserializer;
import java.io.IOException;
import java.util.Map;
import java.util.concurrent.TimeUnit;
import net.mguenther.kafka.junit.EmbeddedKafkaCluster;
import net.mguenther.kafka.junit.ReadKeyValues;
import net.mguenther.kafka.junit.TopicConfig;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.RegisterExtension;


class TransactionAvroProducerIntegrationTest {
    private static final int TIMEOUT_SECONDS = 10;
    private static final int BOUND = 4;
    private static final int ITERATIONS = 5;
    public static final int EXPECTED = (BOUND + 1) * ITERATIONS;
    private static final int KEY_SIZE = 36;
    private static final int FRAUD_KEY_SIZE = 39;

    @RegisterExtension
    final SchemaRegistryMockExtension schemaRegistryMockExtension = new SchemaRegistryMockExtension();
    private final EmbeddedKafkaCluster kafkaCluster = provisionWith(defaultClusterConfig());

    @BeforeEach
    void setup() {
        this.kafkaCluster.start();
    }

    @AfterEach
    void teardown() {
        this.kafkaCluster.stop();
    }

    private static final String OUTPUT_TOPIC = "atm-fraud-incoming-transactions-topic";

    @Test
    void shouldRunApp() throws InterruptedException {
        this.kafkaCluster.createTopic(TopicConfig.withName(OUTPUT_TOPIC).useDefaults());
        TransactionAvroProducer producerApp = new TransactionAvroProducer() {};
        producerApp = this.setupApp(producerApp);
        producerApp.run();
        delay(TIMEOUT_SECONDS, TimeUnit.SECONDS);
        assertThat(this.kafkaCluster.read(ReadKeyValues.from(OUTPUT_TOPIC, String.class, Transaction.class)
                .with(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class)
                .with(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, SpecificAvroDeserializer.class)
                .with(AbstractKafkaSchemaSerDeConfig.SCHEMA_REGISTRY_URL_CONFIG,
                        this.schemaRegistryMockExtension.getUrl())
                .build()))
                .hasSize(EXPECTED)
                .allSatisfy(keyValue -> {
                    final String recordKey = keyValue.getKey();
                    final Transaction tx = keyValue.getValue();
                    final String txID = tx.getTransactionId();
                    final String fraudPrefix = "xxx";
                    final String regex = "^a([0-9]{1,3})";

                    assertThat(recordKey.length()).isIn(KEY_SIZE, FRAUD_KEY_SIZE);
                    assertThat(recordKey).isEqualTo(txID);
                    if (recordKey.length() > KEY_SIZE) {
                        assertThat(recordKey).contains(fraudPrefix);
                    }
                    assertThat(tx.getAccountId()).matches(regex);
                });
        final SchemaRegistryClient client = this.schemaRegistryMockExtension.getSchemaRegistryClient();
        this.cleanRunDestroy(producerApp, client);
    }

    TransactionAvroProducer setupApp(final TransactionAvroProducer producerApp) {
        producerApp.setIterations(ITERATIONS);
        producerApp.setBound(BOUND);
        producerApp.setBrokers(this.kafkaCluster.getBrokerList());
        producerApp.setSchemaRegistryUrl(this.schemaRegistryMockExtension.getUrl());
        producerApp.setOutputTopic(OUTPUT_TOPIC);
        producerApp.setStreamsConfig(Map.of(ConsumerConfig.SESSION_TIMEOUT_MS_CONFIG, "10000"));
        return producerApp;
    }

    void cleanRunDestroy(final TransactionAvroProducer producerApp, final SchemaRegistryClient client) {
        try {
            assertThat(client.getAllSubjects())
                    .contains(producerApp.getOutputTopic() + "-value");
        } catch (final IOException | RestClientException e) {
            throw new RuntimeException(e);
        }
        producerApp.setCleanUp(true);
        producerApp.run();
        try {
            delay(TIMEOUT_SECONDS, TimeUnit.SECONDS);
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
        try {
            assertThat(client.getAllSubjects())
                    .doesNotContain(producerApp.getOutputTopic() + "-value");
        } catch (final IOException | RestClientException e) {
            throw new RuntimeException(e);
        }
        assertThat(this.kafkaCluster.exists(producerApp.getOutputTopic()))
                .as("Output topic is deleted")
                .isFalse();
    }
}
