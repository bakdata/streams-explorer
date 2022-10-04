package com.bakdata.kafka;

import com.opencsv.CSVReader;
import com.opencsv.exceptions.CsvException;
import com.opencsv.exceptions.CsvValidationException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.Properties;
import lombok.Setter;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.Producer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.StringSerializer;
import picocli.CommandLine;

@Setter
@Slf4j
public class TransactionAvroProducer extends KafkaProducerApplication {

    @CommandLine.Option(names = "--real-tx",
            description = "How many real transactions must be generated before a fraudulent transaction can be "
                    + "generated?")
    private int bound;
    @CommandLine.Option(names = "--iteration",
            description = "One iteration contains number of real transactions and one fraudulent transaction")
    private int iterations;

    public static void main(final String[] args) {
        startApplication(new TransactionAvroProducer(), args);
    }


    @Override
    protected Properties createKafkaProperties() {
        final Properties kafkaProperties = super.createKafkaProperties();
        kafkaProperties.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        return kafkaProperties;
    }

    @Override
    protected void runApplication() {
        final TransactionFactory transactionFactory;
        final KafkaProducer<String, Transaction> producer = this.createProducer();
        log.debug("Bound = {} and Iteration= {}", this.bound, this.iterations);
        log.debug("Expected amount of transactions: {}", (this.bound + 1) * this.iterations);
        log.info("Producing data into output topic  <{}>...", this.getOutputTopic());
        final String fileName = "atm_locations.csv";

        try {
            transactionFactory = new TransactionFactory(loadCsvData(fileName));
        } catch (final IOException | CsvValidationException e) {
            throw new RuntimeException("Error occurred while loading the CSV.", e);
        }

        for (int counter = 0; counter < this.iterations; counter++) {
            final int fraudIndex = counter % this.bound;
            Transaction oldTransaction = new Transaction();

            for (int i = 0; i < this.bound; i++) {
                final Transaction newRealTransaction = transactionFactory.createRealTimeTransaction();
                this.publish(producer, newRealTransaction);
                if (i == fraudIndex) {
                    oldTransaction = newRealTransaction;
                }
            }
            final Transaction fraudTransaction = transactionFactory.createFraudTransaction(oldTransaction, fraudIndex);
            this.publish(producer, fraudTransaction);
            log.debug("Current iteration step: {}", counter);
        }
    }


    public static List<AtmLocation> loadCsvData(final String fileName) throws IOException, CsvValidationException {
        final ClassLoader classLoader = AccountProducer.class.getClassLoader();
        final InputStream inputStream = classLoader.getResourceAsStream(fileName);
        String[] line = null;
        final List<AtmLocation> allLocations = new ArrayList<>();
        try (final InputStreamReader streamReader = new InputStreamReader(Objects.requireNonNull(inputStream), StandardCharsets.UTF_8);
                final CSVReader csvReader = new CSVReader(streamReader)) {
            while (((line = csvReader.readNext()) != null)) {
                final AtmLocation locationDetails =
                        new AtmLocation(line[2], Double.parseDouble(line[0]), Double.parseDouble(line[1]));
                allLocations.add(locationDetails);
            }
            final int amountLocation = allLocations.size();
            log.debug("Amount of locations information loaded from the csv file: {}", amountLocation);
            return allLocations;
        } catch (final IOException | CsvException e) {
            throw new RuntimeException(e);
        }
    }


    private void publish(final Producer<? super String, ? super Transaction> producer, final Transaction transaction) {
        producer.send(new ProducerRecord<>(this.getOutputTopic(), transaction.getTransactionId(), transaction));
    }

}
