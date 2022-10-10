package com.bakdata.kafka;

import java.util.Random;

public final class Amounts {
    private static final int[] amounts = {50, 100, 150, 200};
    private static final Random RAND_GENERATOR = new Random();

    public static int randomAmount() {
        return amounts[RAND_GENERATOR.nextInt(amounts.length)];
    }

    public static int otherAmount(final int oldAmount) {
        int newAmount = 1;
        for (final int amount : amounts) {
            if (amount != oldAmount) {
                newAmount = amount;
                break;
            }
        }
        return newAmount;
    }
}
