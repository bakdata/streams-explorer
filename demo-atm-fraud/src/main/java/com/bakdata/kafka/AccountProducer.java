package com.bakdata.kafka;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.Objects;
import java.util.Properties;
import lombok.Setter;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.StringSerializer;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

@Slf4j
@Setter
public class AccountProducer extends KafkaProducerApplication {
    private String fileName = "accounts.json";

    public static void main(final String[] args) {
        startApplication(new AccountProducer(), args);
    }

    @Override
    protected void runApplication() {
        final JSONArray accountList = loadJSON(this.fileName);
        final KafkaProducer<String, Account> producer = this.createProducer();
        for (final Object accountObj : accountList) {
            final Account account = parseAccount((JSONObject) accountObj);
            this.publishAccount(producer, account);
        }
    }

    @Override
    protected Properties createKafkaProperties() {
        final Properties kafkaProperties = super.createKafkaProperties();
        kafkaProperties.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        return kafkaProperties;
    }


    public static JSONArray loadJSON(final String fileName) {
        final JSONParser jsonParser = new JSONParser();
        final ClassLoader classLoader = AccountProducer.class.getClassLoader();
        Object obj = null;
        try (final InputStream inputStream = classLoader.getResourceAsStream(fileName)) {
            obj = jsonParser.parse(new InputStreamReader(Objects.requireNonNull(inputStream)));
        } catch (final IOException | ParseException e) {
            throw new RuntimeException("Error occurred while reading the JSON file.", e);
        }
        return (JSONArray) obj;
    }


    public static Account parseAccount(final JSONObject accountJSON) {
        final ObjectMapper objectMapper = new ObjectMapper();
        final Account account;
        try {
            account = objectMapper.readValue(accountJSON.toJSONString(), Account.class);
        } catch (final JsonProcessingException e) {
            throw new RuntimeException("Error occurred while deserializing JSONObject to Account object", e);
        }
        return account;
    }

    private void publishAccount(final KafkaProducer<? super String, ? super Account> producer, final Account account) {
        producer.send(new ProducerRecord<>(this.getOutputTopic(), account.getAccountId(), account));
    }
}