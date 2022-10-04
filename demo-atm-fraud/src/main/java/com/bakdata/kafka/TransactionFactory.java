package com.bakdata.kafka;

import java.text.SimpleDateFormat;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoUnit;
import java.util.Date;
import java.util.List;
import java.util.Random;
import java.util.TimeZone;
import java.util.UUID;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
public class TransactionFactory {

    private final List<AtmLocation> allLocations;
    private static final Random randGenerator = new Random();
    private final Amounts amounts = new Amounts();

    static Transaction createTransaction(final String accoundID, final String timestamp,
            final String atmLabel,
            final int amount,
            final String transactionId, final double lon, final double lat) {
        final DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss Z");

        final LocalDateTime parsedDateTime = LocalDateTime.parse(timestamp, formatter);
        return Transaction
                .newBuilder()
                .setAccountId(accoundID)
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

    public Transaction createRealTimeTransaction() {
        final String accountId = "a" + randGenerator.nextInt(1000);
        final String timestamp = getTimestamp();
        final int amount = this.amounts.randomAmount();
        final UUID uuid = UUID.randomUUID();
        final String transactionId = uuid.toString();

        final int index = randGenerator.nextInt(this.allLocations.size() - 1);
        final AtmLocation locationDetails = this.allLocations.get(index);
        final double lon = locationDetails.getLongitude();
        final double lat = locationDetails.getLatitude();
        final String atmLabel = locationDetails.getAtmLabel();

        return createTransaction(accountId, timestamp, atmLabel, amount, transactionId, lon,
                lat);
    }

    /*Note: the fraudulent transaction will have the same account ID as the original transaction but different
    location and amount.
     - The timestamp will be randomly different, in a range between one minute and ten minutes earlier than the
     'real' txn.*/
    Transaction createFraudTransaction(final Transaction realTransaction, final int newLocationIndex) {
        final AtmLocation newLocation = this.allLocations.get(newLocationIndex);
        final int realAmount = realTransaction.getAmount();
        final Instant realTimeStamp = realTransaction.getTimestamp();
        final int dif = randGenerator.nextInt(10) + 1;

        final String accountID = realTransaction.getAccountId();
        final Instant fraudTimestamp = realTimeStamp.minus(dif, ChronoUnit.MINUTES);
        final String fraudAtmLabel = newLocation.getAtmLabel();
        final int fraudAmount = this.amounts.otherAmount(realAmount);
        final String fraudTransactionId = "xxx" + realTransaction.getTransactionId();
        final double fraudLon = newLocation.getLongitude();
        final double fraudLat = newLocation.getLatitude();

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

    private static String getTimestamp() {
        final SimpleDateFormat gmtDateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        gmtDateFormat.setTimeZone(TimeZone.getTimeZone("GMT"));
        return gmtDateFormat.format(new Date()) + " +0000";

    }

}
