package com.bakdata.kafka;

import com.opencsv.CSVReader;
import com.opencsv.bean.CsvToBean;
import com.opencsv.bean.CsvToBeanBuilder;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
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
    static final String FILE_NAME = "atm_locations.csv";
    private static final ClassLoader CLASS_LOADER = AccountProducer.class.getClassLoader();

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
        final TransactionFactory transactionFactory = new TransactionFactory(loadCsvData(FILE_NAME));
        final KafkaProducer<String, Transaction> producer = this.createProducer();
        log.debug("Bound = {} and Iteration= {}", this.bound, this.iterations);
        log.debug("Expected amount of transactions: {}", (this.bound + 1) * this.iterations);
        log.info("Producing data into output topic  <{}>...", this.getOutputTopic());
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

    public static List<AtmLocation> loadCsvData(final String fileName) {
        try (final InputStream inputStream = CLASS_LOADER.getResourceAsStream(fileName);
                final InputStreamReader streamReader = new InputStreamReader(Objects.requireNonNull(inputStream),
                        StandardCharsets.UTF_8);
                final CSVReader csvReader = new CSVReader(streamReader)) {

            final CsvToBean<AtmLocation> csvToBean = new CsvToBeanBuilder<AtmLocation>(csvReader)
                    .withType(AtmLocation.class)
                    .withSeparator(',')
                    .withIgnoreLeadingWhiteSpace(true)
                    .withIgnoreEmptyLine(true)
                    .build();
            final List<AtmLocation> allLocations = csvToBean.parse();
            log.debug("Amount of locations information loaded from the csv file: {}", allLocations.size());
            return allLocations;
        } catch (final IOException e) {
            throw new RuntimeException("Error occurred while loading CSV file", e);
        }
    }

    private void publish(final Producer<? super String, ? super Transaction> producer, final Transaction transaction) {
        producer.send(new ProducerRecord<>(this.getOutputTopic(), transaction.getTransactionId(), transaction));
    }

}
