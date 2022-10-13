package com.bakdata.kafka;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import org.junit.jupiter.api.Test;

class TransactionAvroProducerTest {
    private static final String FILENAME = "test_atm_locations.csv";

    @Test
    void shouldLoadCsv() {
        final List<AtmLocation> locations = TransactionAvroProducer.loadCsvData(FILENAME);
        assertThat(locations).hasSize(11);
        assertThat(locations).allSatisfy(location -> assertThat(location.getAtmLabel()).contains("Atm"));
    }
}