package com.bakdata.kafka;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;
import java.util.Properties;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.common.serialization.StringSerializer;

public class AccountProducer extends KafkaProducerApplication {
    public static void main(final String[] args) {
        startApplication(new AccountProducer(), args);
    }

    @Override
    protected void runApplication() {
        final ClassLoader classLoader = this.getClass().getClassLoader();
        final String filename = "accounts.txt";
        final InputStream inputStream = classLoader.getResourceAsStream(filename);
        assert inputStream != null;
        final InputStreamReader streamReader = new InputStreamReader(inputStream, StandardCharsets.UTF_8);
        final Map<Integer, String[]> allAccounts = this.loadCsvData(streamReader);
        final KafkaProducer<String, Account> producer = this.createProducer();

        final int len = allAccounts.size();
        for (int i = 0; i < len; i++) {
            final String[] accountData = allAccounts.get(i);
            final String account_id = accountData[0];
            final String first_name = accountData[1];
            final String last_name = accountData[2];
            final String email = accountData[3];
            final String phone = accountData[4];
            final String address = accountData[5];
            final String country = accountData[6];

            final Account account = createAccount(account_id, first_name, last_name, email, phone, address, country);
            this.publishAccount(producer, account);
        }
    }

    @Override
    protected Properties createKafkaProperties() {
        final Properties kafkaProperties = super.createKafkaProperties();
        kafkaProperties.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        return kafkaProperties;
    }

    public static Map<Integer, String[]> loadCsvData(final InputStreamReader streamReader) {
        final Map<Integer, String[]> accounts = new HashMap<Integer, String[]>();
        String line = "";
        final String splitBy = ",";
        Integer count = 0;

        BufferedReader reader = null;
        try {
            reader = new BufferedReader(streamReader);

            while ((line = reader.readLine()) != null)   //returns a Boolean value
            {
                final String[] row = line.split(splitBy);    // use comma as separator
                final String account_id = getContent(row[0]);
                final String first_name = getContent(row[1]);
                final String last_name = getContent(row[2]);
                final String email = getContent(row[3]);
                final String phone = getContent(row[4]);
                String address = "";
                String country = "";
                if (row.length == 8) {
                    address = getContent(row[5] + row[6]);
                    country = getContent(row[7]);
                } else {
                    address = getContent(row[5]);
                    country = getContent(row[6]);
                }
                accounts.put(count,
                        new String[]{account_id, first_name, last_name, email, phone, address, country});
                count++;
            }
        } catch (final IOException e) {
            throw new RuntimeException(e);
        } finally {
            if (reader != null) {
                try {
                    reader.close();
                } catch (final IOException e) {
                    e.printStackTrace();
                }
            }
        }
        return accounts;
    }

    private static String getContent(final String rawData) {
        String data = rawData.split(":")[1];
        data = data.replace("\"", "");
        data = data.replace(" ", "");
        return data;
    }

    protected static Account createAccount(final String account_id, final String first_name, final String last_name,
            final String email, final String phone,
            final String address, final String country) {
        return Account.newBuilder()
                .setAccountId(account_id)
                .setFirstName(first_name)
                .setLastName(last_name)
                .setEmail(email)
                .setPhone(phone)
                .setAddress(address)
                .setCountry(country)
                .build();
    }

    private void publishAccount(final KafkaProducer<? super String, ? super Account> producer, final Account account) {
        producer.send(new ProducerRecord<>(this.getOutputTopic(), account.getAccountId(), account));
    }
}