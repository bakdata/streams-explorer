package com.bakdata.kafka.integration;

import static net.mguenther.kafka.junit.EmbeddedKafkaCluster.provisionWith;
import static net.mguenther.kafka.junit.EmbeddedKafkaClusterConfig.defaultClusterConfig;
import static net.mguenther.kafka.junit.Wait.delay;
import static org.assertj.core.api.Assertions.assertThat;

import com.bakdata.kafka.Account;
import com.bakdata.kafka.AccountProducer;
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


class AccountProducerIntegrationTest {
    private static final int TIMEOUT_SECONDS = 10;
    public static final int EXPECTED = 999;
    @RegisterExtension
    final SchemaRegistryMockExtension schemaRegistryMockExtension = new SchemaRegistryMockExtension();
    private final EmbeddedKafkaCluster kafkaCluster = provisionWith(defaultClusterConfig());

    private static final String OUTPUT_TOPIC = "atm-fraud-accounts-topic";

    @BeforeEach
    void setup() {
        this.kafkaCluster.start();
    }

    @AfterEach
    void teardown() {
        this.kafkaCluster.stop();
    }

    @Test
    void shouldRunApp() {
        this.kafkaCluster.createTopic(TopicConfig.withName(OUTPUT_TOPIC).useDefaults());
        AccountProducer accountProducer = new AccountProducer() {};
        accountProducer = this.setupApp(accountProducer);
        accountProducer.run();
        try {
            delay(TIMEOUT_SECONDS, TimeUnit.SECONDS);
            assertThat(this.kafkaCluster.read(ReadKeyValues.from(OUTPUT_TOPIC, String.class, Account.class)
                    .with(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class)
                    .with(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, SpecificAvroDeserializer.class)
                    .with(AbstractKafkaSchemaSerDeConfig.SCHEMA_REGISTRY_URL_CONFIG,
                            this.schemaRegistryMockExtension.getUrl())
                    .build()))
                    .hasSize(EXPECTED)
                    .allSatisfy(keyValue -> {
                        final String recordKey = keyValue.getKey();
                        final Account account = keyValue.getValue();
                        final String accountId = account.getAccountId();
                        final String regex = "^a([0-9]{1,3})";

                        assertThat(accountId).matches(regex);
                        assertThat(recordKey).isEqualTo(accountId);
                    });
        } catch (final InterruptedException e) {
            throw new RuntimeException(e);
        }

        final SchemaRegistryClient client = this.schemaRegistryMockExtension.getSchemaRegistryClient();
        this.clean_run_destroy(accountProducer, client);

    }

    AccountProducer setupApp(final AccountProducer accountProducer) {
        accountProducer.setBrokers(this.kafkaCluster.getBrokerList());
        accountProducer.setSchemaRegistryUrl(this.schemaRegistryMockExtension.getUrl());
        accountProducer.setOutputTopic(OUTPUT_TOPIC);
        accountProducer.setStreamsConfig(Map.of(ConsumerConfig.SESSION_TIMEOUT_MS_CONFIG, "10000"));
        return accountProducer;
    }

    void clean_run_destroy(final AccountProducer accountProducer, final SchemaRegistryClient client) {
        try {
            assertThat(client.getAllSubjects())
                    .contains(accountProducer.getOutputTopic() + "-value");
        } catch (final IOException | RestClientException e) {
            throw new RuntimeException(e);
        }
        accountProducer.setCleanUp(true);
        accountProducer.run();
        try {
            delay(TIMEOUT_SECONDS, TimeUnit.SECONDS);
        } catch (final InterruptedException e) {
            throw new RuntimeException(e);
        }
        try {
            assertThat(client.getAllSubjects())
                    .doesNotContain(accountProducer.getOutputTopic() + "-value");
        } catch (final IOException | RestClientException e) {
            throw new RuntimeException(e);
        }
        assertThat(this.kafkaCluster.exists(accountProducer.getOutputTopic()))
                .as("Output topic is deleted")
                .isFalse();
    }


}
