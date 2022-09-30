package com.bakdata.kafka;

import static org.assertj.core.api.Assertions.assertThat;

import com.opencsv.exceptions.CsvValidationException;
import java.io.IOException;
import java.time.Instant;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
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
        transactionAvroProducer.addLocation(new AtmLocation("Atm ServiRed", 3.1328488, 39.8417162));
        transactionAvroProducer.addLocation(new AtmLocation("Atm TeleBanco", 3.1334979, 39.8416612));
        transactionAvroProducer.addLocation(new AtmLocation("Atm TeleBanco\"", 3.13515, 39.8410749));
        transactionAvroProducer.addLocation(new AtmLocation("Atm Sa Nostra", 3.1347859, 39.8411439));
        transactionAvroProducer.addLocation(new AtmLocation("Atm Santander", 3.1345255, 39.8412161));
        transactionAvroProducer.addLocation(new AtmLocation("Atm Banco Popular", -0.413975, 38.3685657));

        return transactionAvroProducer;
    }


    @Test
    void shouldLoadCsv() {
        final String filename = "test_atm_locations.csv";

        final List<AtmLocation> locations;
        try {
            locations = com.bakdata.kafka.TransactionAvroProducer.loadCsvData(filename);
        } catch (final IOException | CsvValidationException e) {
            throw new RuntimeException(e);
        }
        assertThat(EXPECTED).isEqualTo(locations.size());
    }


    @Test
    void shouldCreateTransaction() {
        assertThat(this.transaction1.getAccountId()).isEqualTo(accountId);
        assertThat(this.transaction1.getTimestamp()).isEqualTo(this.timestampInstant);
        assertThat(this.transaction1.getAtm()).isEqualTo(atmLabel);
        assertThat(this.transaction1.getAmount()).isEqualTo(amount);
        assertThat(this.transaction1.getTransactionId()).isEqualTo(this.transactionId);
        assertThat(this.transaction1.getLocation().getLatitude()).isEqualTo(lat);
        assertThat(this.transaction1.getLocation().getLongitude()).isEqualTo(lon);
    }

    @Test
    void shouldCreateFraudTransaction() {
        final Transaction fraudTransaction = this.TransactionAvroProducer.createFraudTransaction(this.transaction1, 5);
        assertThat(fraudTransaction.getAccountId()).isEqualTo(this.transaction1.getAccountId());
        assertThat(fraudTransaction.getTimestamp()).isNotEqualTo(this.transaction1.getTimestamp());
        assertThat(fraudTransaction.getAtm()).isNotEqualTo(this.transaction1.getAtm());
        assertThat(fraudTransaction.getAmount()).isNotEqualTo(this.transaction1.getAmount());
        assertThat(fraudTransaction.getTransactionId()).isNotEqualTo(this.transaction1.getTransactionId());
        assertThat(fraudTransaction.getLocation().getLongitude()).isNotEqualTo(
                this.transaction1.getLocation().getLongitude());
        assertThat(fraudTransaction.getLocation().getLatitude()).isNotEqualTo(
                this.transaction1.getLocation().getLatitude()
        );

    }
}