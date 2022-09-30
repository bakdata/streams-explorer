package com.bakdata.kafka;

import static org.assertj.core.api.Assertions.assertThat;

import com.opencsv.exceptions.CsvValidationException;
import java.io.IOException;
import java.time.Instant;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.UUID;
import org.junit.jupiter.api.Test;

class TransactionAvroProducerTest {

    static final String timestampStr = "2022-09-23 14:25:14 +0000";
    public static final int EXPECTED = 11;
    private final ZonedDateTime parsedDateTime =
            ZonedDateTime.parse(timestampStr, DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss Z"));
    private final Instant timestampInstant = this.parsedDateTime.toInstant();
    private static final String accountId = "a11";
    private static final String atmLabel = "Atm ServiRed";
    private static final int amount = 50;
    private final UUID uuid = UUID.randomUUID();
    private final String transactionId = this.uuid.toString();
    private static final double lon = 3.1328488;
    private static final double lat = 39.8417162;
    private final TransactionAvroProducer TransactionAvroProducer = createApp();
    private final Transaction transaction1 =
            com.bakdata.kafka.TransactionAvroProducer.createTransaction(accountId, timestampStr, atmLabel,
                    amount,
                    this.transactionId,
                    lon, lat);

    private static TransactionAvroProducer createApp() {
        final TransactionAvroProducer transactionAvroProducer = new TransactionAvroProducer();
        transactionAvroProducer.setAllLocations();
        final Collection<String[]> locations = new ArrayList<>();
        locations.add(new String[]{"3.1328488", "39.8417162", "Atm ServiRed"});
        locations.add(new String[]{"3.1334979", "39.8416612", "Atm TeleBanco"});
        locations.add(new String[]{"3.13515", "39.8410749", "Atm TeleBanco"});
        locations.add(new String[]{"3.1347859", "39.8411439", "Atm Sa Nostra"});
        locations.add(new String[]{"3.1345255", "39.8412161", "Atm Santander"});
        locations.add(new String[]{"-0.413975", "38.3685657", "Atm Banco Popular"});

        for (final String[] location : locations) {
            transactionAvroProducer.addLocation(location);
        }
        return transactionAvroProducer;
    }


    @Test
    void shouldLoadCsv() {
        final String filename = "src/main/resources/test_atm_locations.csv";

        final List<String[]> locations;
        try {
            locations = com.bakdata.kafka.TransactionAvroProducer.loadCsvData(filename);
        } catch (final IOException | CsvValidationException e) {
            throw new RuntimeException(e);
        }
        assertThat(EXPECTED).isEqualTo(locations.size());
    }


    @Test
    void shouldCreateTransaction() {
        assertThat(accountId).isEqualTo(this.transaction1.getAccountId());
        assertThat(this.timestampInstant).isEqualTo(this.transaction1.getTimestamp());
        assertThat(atmLabel).isEqualTo(this.transaction1.getAtm());
        assertThat(amount).isEqualTo(this.transaction1.getAmount());
        assertThat(this.transactionId).isEqualTo(this.transaction1.getTransactionId());
        assertThat(lat).isEqualTo(this.transaction1.getLocation().getLatitude());
        assertThat(lon).isEqualTo(this.transaction1.getLocation().getLongitude());
    }

    @Test
    void shouldCreateFraudTransaction() {
        final Transaction fraudTransaction = this.TransactionAvroProducer.createFraudTransaction(this.transaction1, 5);
        assertThat(this.transaction1.getAccountId()).isEqualTo(fraudTransaction.getAccountId());
        assertThat(this.transaction1.getTimestamp()).isNotEqualTo(fraudTransaction.getTimestamp());
        assertThat(this.transaction1.getAtm()).isNotEqualTo(fraudTransaction.getAtm());
        assertThat(this.transaction1.getAmount()).isNotEqualTo(fraudTransaction.getAmount());
        assertThat(this.transaction1.getTransactionId()).isNotEqualTo(fraudTransaction.getTransactionId());
        assertThat(this.transaction1.getLocation().getLongitude()).isNotEqualTo(
                fraudTransaction.getLocation().getLongitude());
        assertThat(this.transaction1.getLocation().getLatitude()).isNotEqualTo(
                fraudTransaction.getLocation().getLatitude());

    }
}