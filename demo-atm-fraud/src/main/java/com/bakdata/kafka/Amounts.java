package com.bakdata.kafka;

import java.util.Random;

public class Amounts {
    private static final int[] amounts = {50, 100, 150, 200};
    private static final Random RAND_GENERATOR = new Random();

    public int randomAmount() {
        return this.amounts[RAND_GENERATOR.nextInt(this.amounts.length)];
    }

    public int otherAmount(final int oldAmount) {
        int newAmount = 0;
        for (int amount : amounts) {
            if (newAmount != amount) {
                newAmount = amount;
            }
        }
        return newAmount;
    }
}
