package com.bakdata.kafka;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.IOException;
import java.io.InputStream;
import java.util.List;
import java.util.Properties;
import lombok.Setter;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.StringSerializer;

@Slf4j
@Setter
public class AccountProducer extends KafkaProducerApplication {
    private static final String FILE_NAME = "accounts.json";
    public static void main(final String[] args) {
        startApplication(new AccountProducer(), args);
    }

    @Override
    protected void runApplication() {
        final List<Account> accounts = loadJSON(FILE_NAME);
        final KafkaProducer<String, Account> producer = this.createProducer();
        for (final Account accountObj : accounts) {
            this.publishAccount(producer, accountObj);
        }
    }

    @Override
    protected Properties createKafkaProperties() {
        final Properties kafkaProperties = super.createKafkaProperties();
        kafkaProperties.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        return kafkaProperties;
    }

    public static List<Account> loadJSON(final String fileName) {
        final ClassLoader classLoader = AccountProducer.class.getClassLoader();
        final ObjectMapper objectMapper = new ObjectMapper();
        try (final InputStream inputStream = classLoader.getResourceAsStream(fileName)) {
            return objectMapper.readValue(inputStream, new TypeReference<>() {});
        } catch (final IOException e) {
            throw new RuntimeException("Error occurred while reading the JSON file.", e);
        }
    }

    private void publishAccount(final KafkaProducer<? super String, ? super Account> producer, final Account account) {
        producer.send(new ProducerRecord<>(this.getOutputTopic(), account.getAccountId(), account));
    }
}