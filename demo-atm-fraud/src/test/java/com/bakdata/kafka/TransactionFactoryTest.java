package com.bakdata.kafka;

import static org.assertj.core.api.Assertions.assertThat;

import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import org.junit.jupiter.api.Test;

class TransactionFactoryTest {

    private static final String accountId = "a11";
    private static final String atmLabel = "Atm ServiRed";
    private static final int amount = 50;
    private final UUID uuid = UUID.randomUUID();
    private final String transactionId = this.uuid.toString();
    private static final double lon = 3.1328488;
    private static final double lat = 39.8417162;
    private final TransactionFactory transactionFactory = createApp();

    private final Transaction transaction1 = Transaction
            .newBuilder()
            .setAccountId(accountId)
            .setTimestamp(LocalDateTime.now().toInstant(ZoneOffset.UTC))
            .setAtm(atmLabel)
            .setAmount(amount)
            .setTransactionId(this.transactionId)
            .setLocation(
                    Location
                            .newBuilder()
                            .setLatitude(lat)
                            .setLongitude(lon)
                            .build()
            )
            .build();

    private static TransactionFactory createApp() {
        final List<AtmLocation> atmLocations = new ArrayList<>();
        atmLocations.add(new AtmLocation(39.8417162, 3.1328488, "Atm ServiRed"));
        atmLocations.add(new AtmLocation(3.1334979, 39.8416612, "Atm TeleBanco"));
        atmLocations.add(new AtmLocation(3.13515, 39.8410749, "Atm TeleBanco"));
        atmLocations.add(new AtmLocation(3.1347859, 39.8411439, "Atm Sa Nostra"));
        atmLocations.add(new AtmLocation(3.1345255, 39.8412161, "Atm Santander"));
        atmLocations.add(new AtmLocation(-0.413975, 38.3685657, "Atm Banco Popular"));

        return new TransactionFactory(atmLocations);
    }

    @Test
    void shouldCreateTransaction() {
        assertThat(this.transaction1.getAccountId()).isEqualTo(accountId);
        assertThat(this.transaction1.getTimestamp()).isExactlyInstanceOf(Instant.class);
        assertThat(this.transaction1.getAtm()).isEqualTo(atmLabel);
        assertThat(this.transaction1.getAmount()).isEqualTo(amount);
        assertThat(this.transaction1.getTransactionId()).isEqualTo(this.transactionId);
        assertThat(this.transaction1.getLocation().getLatitude()).isEqualTo(lat);
        assertThat(this.transaction1.getLocation().getLongitude()).isEqualTo(lon);
    }

    @Test
    void shouldCreateRealTransaction() {
        Transaction transaction = this.transactionFactory.createRealTimeTransaction();
        final String regex = "^a([0-9]{1,3})";
        assertThat(transaction.getAccountId()).matches(regex);
        assertThat(transaction.getTransactionId()).hasSize(36);
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