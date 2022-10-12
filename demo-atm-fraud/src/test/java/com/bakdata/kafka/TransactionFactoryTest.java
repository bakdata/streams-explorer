package com.bakdata.kafka;

import static org.assertj.core.api.Assertions.assertThat;

import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import org.junit.jupiter.api.Test;

class TransactionFactoryTest {

    private final TransactionFactory transactionFactory = createApp();

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

    static Transaction createTransaction() {
        final String accountId = "a11";
        final String atmLabel = "Atm ServiRed";
        final int amount = 50;
        final UUID uuid = UUID.randomUUID();
        final String transactionId = uuid.toString();
        final double lon = 3.1328488;
        final double lat = 39.8417162;

        return Transaction
                .newBuilder()
                .setAccountId(accountId)
                .setTimestamp(LocalDateTime.now().toInstant(ZoneOffset.UTC))
                .setAtm(atmLabel)
                .setAmount(amount)
                .setTransactionId(transactionId)
                .setLocation(
                        Location
                                .newBuilder()
                                .setLatitude(lat)
                                .setLongitude(lon)
                                .build()
                )
                .build();
    }

    @Test
    void shouldCreateRealTransaction() {
        final Transaction transaction = this.transactionFactory.createRealTimeTransaction();
        final String regex = "^a([0-9]{1,3})";
        assertThat(transaction.getAccountId()).matches(regex);
        assertThat(transaction.getTransactionId()).hasSize(36);
    }

    @Test
    void shouldCreateFraudTransaction() {
        final Transaction transaction1 = createTransaction();
        final Transaction fraudTransaction = this.transactionFactory.createFraudTransaction(transaction1, 5);
        assertThat(fraudTransaction.getAccountId()).isEqualTo(transaction1.getAccountId());
        assertThat(fraudTransaction.getTimestamp()).isNotEqualTo(transaction1.getTimestamp());
        assertThat(fraudTransaction.getAtm()).isNotEqualTo(transaction1.getAtm());
        assertThat(fraudTransaction.getAmount()).isNotEqualTo(transaction1.getAmount());
        assertThat(fraudTransaction.getTransactionId()).isNotEqualTo(transaction1.getTransactionId());
        assertThat(fraudTransaction.getLocation().getLongitude()).isNotEqualTo(
                transaction1.getLocation().getLongitude());
        assertThat(fraudTransaction.getLocation().getLatitude()).isNotEqualTo(
                transaction1.getLocation().getLatitude()
        );
    }
}