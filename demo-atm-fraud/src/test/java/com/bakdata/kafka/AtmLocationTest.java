package com.bakdata.kafka;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.Test;

class AtmLocationTest {
    @Test
    void shouldReturnAnotherAmount (){
        int oldAmount = 50;
        Amounts amounts = new Amounts();
        int newAmount = amounts.otherAmount(oldAmount);
        assertThat(newAmount).isNotEqualTo(oldAmount);
    }

}
