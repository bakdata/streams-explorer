package com.bakdata.kafka;

import java.util.Random;

public class Amounts {
    private static final int[] amounts = {50, 100, 150, 200};
    private static final Random RAND_GENERATOR = new Random();

    public static int randomAmount() {
        return amounts[RAND_GENERATOR.nextInt(amounts.length)];
    }

    public static int otherAmount(final int oldAmount) {
        int newAmount = 0;
        for (final int amount : amounts) {
            if (newAmount != oldAmount) {
                newAmount = amount;
            }
        }
        return newAmount;
    }
}
