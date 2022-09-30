package com.bakdata.kafka;

import java.io.FileReader;
import java.io.IOException;
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
    private String fileName = "src/main/resources/accounts.json";

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
        try (final FileReader reader = new FileReader(fileName)) {
            final Object obj = jsonParser.parse(reader);
            return (JSONArray) obj;
        } catch (final IOException | ParseException e) {
            throw new RuntimeException(e);
        }
    }


    public static Account parseAccount(final JSONObject accountJSON) {
        return Account.newBuilder()
                .setAccountId(accountJSON.get("account_id").toString())
                .setFirstName(accountJSON.get("first_name").toString())
                .setLastName(accountJSON.get("last_name").toString())
                .setEmail(accountJSON.get("email").toString())
                .setPhone(accountJSON.get("phone").toString())
                .setAddress(accountJSON.get("address").toString())
                .setCountry(accountJSON.get("country").toString())
                .build();
    }

    private void publishAccount(final KafkaProducer<? super String, ? super Account> producer, final Account account) {
        try {
            producer.send(new ProducerRecord<>(this.getOutputTopic(), account.getAccountId(), account));
        } catch (final RuntimeException e) {
            log.error(
                    "Some Error occurred  while producing an account <{}> into the topic <{}>. With error message: {}",
                    account.getAccountId(), this.getOutputTopic(), e);
        }
    }
}