package com.bakdata.kafka;

import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.time.temporal.ChronoUnit;
import java.util.List;
import java.util.Random;
import java.util.UUID;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
public class TransactionFactory {

    private final List<AtmLocation> locations;
    private static final Random RAND_GENERATOR = new Random();

    public Transaction createRealTimeTransaction() {
        final String accountId = "a" + RAND_GENERATOR.nextInt(1000);
        LocalDateTime parsedDateTime = LocalDateTime.now();
        final int amount = Amounts.randomAmount();
        final UUID uuid = UUID.randomUUID();
        final String transactionId = uuid.toString();

        final int index = RAND_GENERATOR.nextInt(this.locations.size() - 1);
        final AtmLocation locationDetails = this.locations.get(index);
        final double lon = locationDetails.getLon();
        final double lat = locationDetails.getLat();
        final String atmLabel = locationDetails.getAtmLabel();

        return Transaction
                .newBuilder()
                .setAccountId(accountId)
                .setTimestamp(parsedDateTime.toInstant(ZoneOffset.UTC))
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

    /*Note: the fraudulent transaction will have the same account ID as the original transaction but different
    location and amount.
     - The timestamp will be randomly different, in a range between one minute and ten minutes earlier than the
     'real' txn.*/
    Transaction createFraudTransaction(final Transaction realTransaction, final int newLocationIndex) {
        final AtmLocation newLocation = this.locations.get(newLocationIndex);
        final int realAmount = realTransaction.getAmount();
        final Instant realTimeStamp = realTransaction.getTimestamp();
        final int dif = RAND_GENERATOR.nextInt(10) + 1;

        final String accountID = realTransaction.getAccountId();
        final Instant fraudTimestamp = realTimeStamp.minus(dif, ChronoUnit.MINUTES);
        final String fraudAtmLabel = newLocation.getAtmLabel();
        final int fraudAmount = Amounts.otherAmount(realAmount);
        final String fraudTransactionId = "xxx" + realTransaction.getTransactionId();
        final double fraudLon = newLocation.getLon();
        final double fraudLat = newLocation.getLat();

        return Transaction
                .newBuilder()
                .setAccountId(accountID)
                .setTimestamp(fraudTimestamp)
                .setAtm(fraudAtmLabel)
                .setAmount(fraudAmount)
                .setTransactionId(fraudTransactionId)
                .setLocation(
                        Location
                                .newBuilder()
                                .setLatitude(fraudLat)
                                .setLongitude(fraudLon)
                                .build()
                )
                .build();
    }
}
