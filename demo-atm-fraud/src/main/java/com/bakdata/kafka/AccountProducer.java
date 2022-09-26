package com.bakdata.kafka;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
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

public class AccountProducer extends KafkaProducerApplication {
    public static void main(final String[] args) {
        startApplication(new AccountProducer(), args);
    }

    private String filename = "accounts.txt";

    private Map<Integer, String[]> allAccounts;

    @Override
    protected void runApplication() {
        ClassLoader classLoader = getClass().getClassLoader();
        InputStream inputStream = classLoader.getResourceAsStream(this.filename);
        InputStreamReader streamReader = new InputStreamReader(inputStream, StandardCharsets.UTF_8);
        this.allAccounts = this.loadCsvData(streamReader);
        final KafkaProducer<String, Account> producer = this.createProducer();

        int len = this.allAccounts.size();
        for (int i = 0; i < len; i++) {
            String[] accountData = this.allAccounts.get(i);
            String account_id = accountData[0], first_name = accountData[1], last_name = accountData[2], email =
                    accountData[3], phone = accountData[4],
                    address = accountData[5], country = accountData[6];

            Account account = this.createAccount(account_id, first_name, last_name, email, phone, address, country);
            this.publishAccount(producer, account);
        }
    }

    @Override
    protected Properties createKafkaProperties() {
        final Properties kafkaProperties = super.createKafkaProperties();
        kafkaProperties.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, Serdes.StringSerde.class);
        return super.createKafkaProperties();
    }

    public Map<Integer, String[]> loadCsvData(InputStreamReader streamReader) {
        Map<Integer, String[]> accounts = new HashMap<Integer, String[]>();
        String line = "";
        String splitBy = ",";
        Integer count = 0;

        BufferedReader reader = null;
        try {
            reader = new BufferedReader(streamReader);

            while ((line = reader.readLine()) != null)   //returns a Boolean value
            {
                String[] row = line.split(splitBy);    // use comma as separator
                String account_id = this.getContent(row[0]), first_name = this.getContent(row[1]),
                        last_name = this.getContent(row[2]),
                        email = this.getContent(row[3]), phone = this.getContent(row[4]);
                String address, country = "";
                if (row.length == 8) {
                    address = this.getContent(row[5] + row[6]);
                    country = this.getContent(row[7]);
                } else {
                    address = this.getContent(row[5]);
                    country = this.getContent(row[6]);
                }
                accounts.put(count,
                        new String[]{account_id, first_name, last_name, email, phone, address, country});
                count++;
            }
        } catch (FileNotFoundException e) {
            throw new RuntimeException(e);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        return accounts;
    }

    private String getContent(String rawData) {
        String data = rawData.split(":")[1];
        data = data.replace("\"", "");
        data = data.replace(" ", "");
        return data;
    }

    protected Account createAccount(String account_id, String first_name, String last_name, String email, String phone,
            String address, String country) {
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

    private void publishAccount(KafkaProducer<String, Account> producer, Account account) {
        producer.send(new ProducerRecord<>(this.getOutputTopic(), account.getAccountId(), account));
    }
}