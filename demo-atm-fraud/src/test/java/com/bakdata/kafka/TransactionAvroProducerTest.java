package com.bakdata.kafka;

import static org.assertj.core.api.Assertions.assertThat;

import com.bakdata.fluent_kafka_streams_tests.TestTopology;
import java.time.Instant;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

class TransactionAvroProducerTest {

    static final String timestamp_str = "2022-09-23 14:25:14 +0000";
    private ZonedDateTime parsedDateTime =
            ZonedDateTime.parse(timestamp_str, DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss Z"));
    private Instant timestampInstant = parsedDateTime.toInstant();
    private String accoundID = "a11";
    private String atm_label = "Atm ServiRed";
    private int amount = 50;
    private UUID uuid = UUID.randomUUID();
    private String transaction_id = uuid.toString();
    private double lon = 3.1328488;
    private double lat = 39.8417162;
    private final TransactionAvroProducer TransactionAvroProducer = createApp();
    private Transaction transaction1 =
            TransactionAvroProducer.createTransaction(accoundID, timestamp_str, atm_label, amount, transaction_id,
                    lon, lat);
    private TestTopology<String, String> topology = null;
    Transaction transaction = new Transaction();

    private static TransactionAvroProducer createApp() {
        final TransactionAvroProducer transactionAvroProducer = new TransactionAvroProducer();
        transactionAvroProducer.setAllLocations();
        List<String[]> locations = new ArrayList<>();
        locations.add(new String[]{"3.1328488", "39.8417162", "Atm ServiRed"});
        locations.add(new String[]{"3.1334979", "39.8416612", "Atm TeleBanco"});
        locations.add(new String[]{"3.13515", "39.8410749", "Atm TeleBanco"});
        locations.add(new String[]{"3.1347859", "39.8411439", "Atm Sa Nostra"});
        locations.add(new String[]{"3.1345255", "39.8412161", "Atm Santander"});
        locations.add(new String[]{"-0.413975", "38.3685657", "Atm Banco Popular"});

        for (int i = 0; i < 6; i++) {
            transactionAvroProducer.addLocation(i, locations.get(i));
        }
        return transactionAvroProducer;
    }

    @AfterEach
    void tearDown() {
        if (this.topology != null) {
            this.topology.stop();
        }
    }

    @Test
    void shouldLoadCsv() {
        String filename = "ttest_atm_locations.csv";
        Map<Integer, String[]> locations = TransactionAvroProducer.loadCsvData(filename);
        Assertions.assertEquals(11, locations.size(), "Comparing size of the created map with size of csv");
    }


    @Test
    void shouldCreateTransaction() {
        Assertions.assertEquals("a11", transaction1.getAccountId(), "Comparing created Transactions accountID");
        Assertions.assertEquals(timestampInstant, transaction1.getTimestamp(),
                "Comparing created Transactions timestamp");
        Assertions.assertEquals(atm_label, transaction1.getAtm(), "Comparing created Transactions atm label");
        Assertions.assertEquals(amount, transaction1.getAmount(), "Comparing created Transactions amount");
        Assertions.assertEquals(transaction_id, transaction1.getTransactionId(), "Comparing created Transactions ID");
        Assertions.assertEquals(lat, transaction1.getLocation().getLatitude(),
                "Comparing created Transactions locations lat");
        Assertions.assertEquals(lon, transaction1.getLocation().getLongitude(),
                "Comparing created Transactions locations lon");
    }

    @Test
    void shouldCreateFraudTransaction() {
        Transaction fraudTransaction = TransactionAvroProducer.createFraudTransaction(transaction1, 5);

        Assertions.assertEquals(transaction1.getAccountId(), fraudTransaction.getAccountId(),
                "Verifying that both transactions have the same accountID");
        Assertions.assertNotEquals(transaction1.getTimestamp(), fraudTransaction.getTimestamp(),
                "Verifying that both transactions have different Timestamps");
        Assertions.assertNotEquals(transaction1.getAtm(), fraudTransaction.getAtm(),
                "Verifying that both transactions have different atms");
        Assertions.assertNotEquals(transaction1.getAmount(), fraudTransaction.getAmount(),
                "Verifying that both transactions have different amounts");
        Assertions.assertNotEquals(transaction1.getTransactionId(), fraudTransaction.getTransactionId(),
                "Verifying that both transactions have different transactionIDs");
        Assertions.assertNotEquals(transaction1.getLocation().getLatitude(),
                fraudTransaction.getLocation().getLatitude(),
                "Verifying that both transactions have different lat-values");
        Assertions.assertNotEquals(transaction1.getLocation().getLongitude(),
                fraudTransaction.getLocation().getLongitude(),
                "Verifying that both transactions have different lon-values");

    }

}