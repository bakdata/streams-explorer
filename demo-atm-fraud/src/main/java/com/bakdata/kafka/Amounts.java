package com.bakdata.kafka;

import java.util.Random;

public class Amounts {
    private final int[] amountList = {50, 100, 150, 200};
    private static final Random randGenerator = new Random();

    public int randomAmount() {
        return this.amountList[randGenerator.nextInt(this.amountList.length)];
    }

    public int otherAmount(final int oldAmount) {
        int newAmount = 0;
        for (int amount : amountList) {
            if (newAmount != amount) {
                newAmount = amount;
            }
        }
        return newAmount;
    }
}
