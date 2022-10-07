package com.bakdata.kafka;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import org.junit.jupiter.api.Test;

class TransactionAvroProducerTest {
    public static final int EXPECTED = 11;
    private static final String FILENAME = "test_atm_locations.csv";

    @Test
    void shouldLoadCsv() {
        final List<AtmLocation> locations = TransactionAvroProducer.loadCsvData(FILENAME);
        assertThat(locations.size()).isEqualTo(EXPECTED);
        for (final AtmLocation loc : locations) {
            assertThat(loc.getAtmLabel()).contains("Atm");
        }
    }
}