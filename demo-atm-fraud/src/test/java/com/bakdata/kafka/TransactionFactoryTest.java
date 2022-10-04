package com.bakdata.kafka;

import static org.assertj.core.api.Assertions.assertThat;

import java.time.Instant;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import org.junit.jupiter.api.Test;

class TransactionFactoryTest {

    static final String timestampStr = "2022-09-23 14:25:14 +0000";
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
    private final TransactionFactory transactionFactory = createApp();
    private final Transaction transaction1 =
            TransactionFactory.createTransaction(accountId, timestampStr, atmLabel,
                    amount,
                    this.transactionId,
                    lon, lat);

    private static TransactionFactory createApp() {
        final List<AtmLocation> atmLocations = new ArrayList<>();

        atmLocations.add(new AtmLocation("Atm ServiRed", 3.1328488, 39.8417162));
        atmLocations.add(new AtmLocation("Atm TeleBanco", 3.1334979, 39.8416612));
        atmLocations.add(new AtmLocation("Atm TeleBanco\"", 3.13515, 39.8410749));
        atmLocations.add(new AtmLocation("Atm Sa Nostra", 3.1347859, 39.8411439));
        atmLocations.add(new AtmLocation("Atm Santander", 3.1345255, 39.8412161));
        atmLocations.add(new AtmLocation("Atm Banco Popular", -0.413975, 38.3685657));

        return new TransactionFactory(atmLocations);
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
        final Transaction fraudTransaction = this.transactionFactory.createFraudTransaction(this.transaction1, 5);
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