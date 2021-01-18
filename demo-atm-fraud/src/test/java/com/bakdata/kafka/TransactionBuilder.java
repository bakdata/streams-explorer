package com.bakdata.kafka;

import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class TransactionBuilder {

  public static Map<String, Transaction> buildTestTransactionsMap() {
    return buildTestTransactions()
        .stream()
        .collect(Collectors.toMap(
            Transaction::getTransactionId, transaction -> transaction)
        );
  }

  public static List<Transaction> buildTestTransactions() {
    return List.of(
        Transaction.newBuilder()
            .setTransactionId("01")
            .setAmount(20)
            .setAccountId("ac_01")
            .setAtm("Euronet")
            .setLocation(Location.newBuilder().setLatitude(50.5).setLongitude(12.4).build())
            .setTimestamp(TransactionBuilder.parseDateTimeString("2020-11-25T18:01:30"))
            .build(),
        Transaction.newBuilder()
            .setTransactionId("02")
            .setAmount(400)
            .setAccountId("ac_02")
            .setAtm("Flying Pig Bistro")
            .setLocation(Location.newBuilder().setLatitude(-30).setLongitude(120.1).build())
            .setTimestamp(TransactionBuilder.parseDateTimeString("2020-11-25T18:05:00"))
            .build(),
        Transaction.newBuilder()
            .setTransactionId("03")
            .setAmount(40)
            .setAccountId("ac_02")
            .setAtm("Flying Pig Bistro")
            .setLocation(Location.newBuilder().setLatitude(-30).setLongitude(120.1).build())
            .setTimestamp(TransactionBuilder.parseDateTimeString("2020-11-25T20:30:00"))
            .build(),
        Transaction.newBuilder()
            .setTransactionId("04")
            .setAmount(50)
            .setAccountId("ac_03")
            .setAtm("Wells Fargo")
            .setLocation(Location.newBuilder().setLatitude(45.3).setLongitude(-90.7).build())
            .setTimestamp(TransactionBuilder.parseDateTimeString("2020-11-25T20:48:00"))
            .build(),
        Transaction.newBuilder()
            .setTransactionId("X05")
            .setAmount(500)
            .setAccountId("ac_03")
            .setAtm("Barclays")
            .setLocation(Location.newBuilder().setLatitude(0.0).setLongitude(0.0).build())
            .setTimestamp(TransactionBuilder.parseDateTimeString("2020-11-25T20:51:00"))
            .build()
    );
  }

  public static Instant parseDateTimeString(String dateTimeString) {
    return LocalDateTime.parse(dateTimeString).atZone(ZoneId.systemDefault()).toInstant();
  }
}
