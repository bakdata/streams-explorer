package com.bakdata.kafka;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import org.junit.jupiter.api.Test;

class TransactionAvroProducerTest {
    public static final int EXPECTED = 11;

    @Test
    void shouldLoadCsv() {
        final String filename = "test_atm_locations.csv";
        List<AtmLocation> locations = TransactionAvroProducer.loadCsvData(filename);
        assertThat(locations.size()).isEqualTo(EXPECTED);
        for (AtmLocation loc: locations){
            assertThat(loc.getAtmLabel()).contains("Atm");
        }
    }
}