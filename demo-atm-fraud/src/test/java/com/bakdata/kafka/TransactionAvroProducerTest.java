package com.bakdata.kafka;

import static org.assertj.core.api.Assertions.assertThat;

import com.opencsv.exceptions.CsvValidationException;
import java.io.IOException;
import java.util.List;
import org.junit.jupiter.api.Test;

class TransactionAvroProducerTest {
    public static final int EXPECTED = 11;

    @Test
    void shouldLoadCsv() {
        final String filename = "test_atm_locations.csv";

        final List<AtmLocation> locations;
        try {
            locations = com.bakdata.kafka.TransactionAvroProducer.loadCsvData(filename);
        } catch (final IOException | CsvValidationException e) {
            throw new RuntimeException("Error occurred while loading the CSV.", e);
        }
        assertThat(EXPECTED).isEqualTo(locations.size());
    }
}