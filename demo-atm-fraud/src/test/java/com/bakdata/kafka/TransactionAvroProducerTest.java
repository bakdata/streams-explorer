package com.bakdata.kafka;

import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.time.Instant;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

class TransactionAvroProducerTest {

    static final String timestamp_str = "2022-09-23 14:25:14 +0000";
    public static final int EXPECTED = 11;
    private final ZonedDateTime parsedDateTime =
            ZonedDateTime.parse(timestamp_str, DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss Z"));
    private final Instant timestampInstant = this.parsedDateTime.toInstant();
    private static final String accoundID = "a11";
    private static final String atm_label = "Atm ServiRed";
    private static final int amount = 50;
    private final UUID uuid = UUID.randomUUID();
    private final String transaction_id = this.uuid.toString();
    private static final double lon = 3.1328488;
    private static final double lat = 39.8417162;
    private final TransactionAvroProducer TransactionAvroProducer = createApp();
    private final Transaction transaction1 =
            com.bakdata.kafka.TransactionAvroProducer.createTransaction(accoundID, timestamp_str, atm_label,
                    amount,
                    this.transaction_id,
                    lon, lat);

    private static TransactionAvroProducer createApp() {
        final TransactionAvroProducer transactionAvroProducer = new TransactionAvroProducer();
        transactionAvroProducer.setAllLocations();
        final List<String[]> locations = new ArrayList<>();
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


    @Test
    void shouldLoadCsv() {
        final String filename = "test_atm_locations.csv";
        final ClassLoader classLoader = this.getClass().getClassLoader();
        final InputStream inputStream = classLoader.getResourceAsStream(filename);
        assert inputStream != null;
        final InputStreamReader streamReader = new InputStreamReader(inputStream, StandardCharsets.UTF_8);

        final Map<Integer, String[]> locations = com.bakdata.kafka.TransactionAvroProducer.loadCsvData(streamReader);
        Assertions.assertEquals(EXPECTED, locations.size(), "Comparing size of the created map with size of csv");
    }


    @Test
    void shouldCreateTransaction() {
        Assertions.assertEquals("a11", this.transaction1.getAccountId(), "Comparing created Transactions accountID");
        Assertions.assertEquals(this.timestampInstant, this.transaction1.getTimestamp(),
                "Comparing created Transactions timestamp");
        Assertions.assertEquals(atm_label, this.transaction1.getAtm(), "Comparing created Transactions atm label");
        Assertions.assertEquals(amount, this.transaction1.getAmount(), "Comparing created Transactions amount");
        Assertions.assertEquals(this.transaction_id, this.transaction1.getTransactionId(),
                "Comparing created Transactions ID");
        Assertions.assertEquals(lat, this.transaction1.getLocation().getLatitude(),
                "Comparing created Transactions locations lat");
        Assertions.assertEquals(lon, this.transaction1.getLocation().getLongitude(),
                "Comparing created Transactions locations lon");
    }

    @Test
    void shouldCreateFraudTransaction() {
        final Transaction fraudTransaction = this.TransactionAvroProducer.createFraudTransaction(this.transaction1, 5);

        Assertions.assertEquals(this.transaction1.getAccountId(), fraudTransaction.getAccountId(),
                "Verifying that both transactions have the same accountID");
        Assertions.assertNotEquals(this.transaction1.getTimestamp(), fraudTransaction.getTimestamp(),
                "Verifying that both transactions have different Timestamps");
        Assertions.assertNotEquals(this.transaction1.getAtm(), fraudTransaction.getAtm(),
                "Verifying that both transactions have different atms");
        Assertions.assertNotEquals(this.transaction1.getAmount(), fraudTransaction.getAmount(),
                "Verifying that both transactions have different amounts");
        Assertions.assertNotEquals(this.transaction1.getTransactionId(), fraudTransaction.getTransactionId(),
                "Verifying that both transactions have different transactionIDs");
        Assertions.assertNotEquals(this.transaction1.getLocation().getLatitude(),
                fraudTransaction.getLocation().getLatitude(),
                "Verifying that both transactions have different lat-values");
        Assertions.assertNotEquals(this.transaction1.getLocation().getLongitude(),
                fraudTransaction.getLocation().getLongitude(),
                "Verifying that both transactions have different lon-values");
    }
}