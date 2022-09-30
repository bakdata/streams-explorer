package com.bakdata.kafka;

import com.opencsv.CSVReader;
import com.opencsv.exceptions.CsvException;
import com.opencsv.exceptions.CsvValidationException;
import java.io.IOException;
import java.io.Reader;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.text.SimpleDateFormat;
import java.time.Instant;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Properties;
import java.util.Random;
import java.util.TimeZone;
import java.util.UUID;
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


    private List<String[]> allLocations = null;
    private static final Random randGenerator = new Random();

    public void setAllLocations() {
        this.allLocations = new ArrayList<>();
    }

    public void addLocation(final String[] values) {
        this.allLocations.add(values);
    }

    final Amounts amounts = new Amounts();

    @Override
    protected Properties createKafkaProperties() {
        final Properties kafkaProperties = super.createKafkaProperties();
        kafkaProperties.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        return kafkaProperties;
    }

    @Override
    protected void runApplication() {
        final KafkaProducer<String, Transaction> producer = this.createProducer();
        log.debug("Bound = {} and Iteration= {}", this.bound, this.iterations);
        log.debug("Expected amount of transactions: {}", (this.bound + 1) * this.iterations);
        log.info("Producing data into output topic  <{}>...", this.getOutputTopic());
        //final ClassLoader classLoader = this.getClass().getClassLoader();
        final String fileName = "src/main/resources/atm_locations.csv";

        try {
            this.allLocations = loadCsvData(fileName);
        } catch (final IOException | CsvValidationException e) {
            throw new RuntimeException(e);
        }

        final int amountLocation = this.allLocations.size();
        log.debug("Amount of locations information loaded from the csv file: {}", amountLocation);
        for (int counter = 0; counter < this.iterations; counter++) {
            final int fraudIndex = counter % this.bound;
            Transaction oldTransaction = new Transaction();

            for (int i = 0; i < this.bound; i++) {
                final Transaction newRealTransaction = this.createRealTimeTransaction(amountLocation);
                this.publish(producer, newRealTransaction);
                if (i == fraudIndex) {
                    oldTransaction = newRealTransaction;
                }
            }
            final Transaction fraudTransaction = this.createFraudTransaction(oldTransaction, fraudIndex);
            this.publish(producer, fraudTransaction);
            log.debug("Current iteration step: {}", counter);
        }
    }

    private Transaction createRealTimeTransaction(final int amountLocation) {
        final String accountId = "a" + randGenerator.nextInt(1000);
        final String timestamp = getTimestamp();
        final int amount = this.amounts.randomAmount();
        final UUID uuid = UUID.randomUUID();
        final String transactionId = uuid.toString();

        final int index = randGenerator.nextInt(amountLocation - 1);
        final String[] locationDetails = this.allLocations.get(index);
        final double lon = Double.parseDouble(locationDetails[0]);
        final double lat = Double.parseDouble(locationDetails[1]);
        final String atmLabel = locationDetails[2];

        return createTransaction(accountId, timestamp, atmLabel, amount, transactionId, lon,
                lat);
    }

    public static List<String[]> loadCsvData(final String fileName) throws IOException, CsvValidationException {
        final Path filePath = Paths.get(fileName);

        try (final Reader reader = Files.newBufferedReader(filePath)) {
            try (final CSVReader csvReader = new CSVReader(reader)) {
                return csvReader.readAll();
            }
        } catch (final IOException | CsvException e) {
            throw new RuntimeException(e);
        }

    }

    private static String getTimestamp() {
        final SimpleDateFormat gmtDateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        gmtDateFormat.setTimeZone(TimeZone.getTimeZone("GMT"));
        return gmtDateFormat.format(new Date()) + " +0000";

    }

    static Transaction createTransaction(final String accoundID, final String timestamp,
            final String atmLabel,
            final int amount,
            final String transactionId, final double lon, final double lat) {
        final ZonedDateTime parsedDateTime = ZonedDateTime.parse(timestamp,
                DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss Z"));
        return Transaction
                .newBuilder()
                .setAccountId(accoundID)
                .setTimestamp(parsedDateTime.toInstant())
                .setAtm(atmLabel)
                .setAmount(amount)
                .setTransactionId(transactionId)
                .setLocation(
                        Location
                                .newBuilder()
                                .setLatitude(lat)
                                .setLongitude(lon)
                                .build()
                )
                .build();
    }

    /*Note: the fraudulent transaction will have the same account ID as the original transaction but different
    location and amount.
     - The timestamp will be randomly different, in a range between one minute and ten minutes earlier than the
     'real' txn.*/
    Transaction createFraudTransaction(final Transaction realTransaction, final int newLocationIndex) {
        final String[] newLocation = this.allLocations.get(newLocationIndex);
        final int realAmount = realTransaction.getAmount();
        final Instant realtimestamp = realTransaction.getTimestamp();
        final int dif = randGenerator.nextInt(10) + 1;

        final String accountID = realTransaction.getAccountId();
        final Instant fraudTimestamp = realtimestamp.minus(dif, ChronoUnit.MINUTES);
        final String fraudAtmLabel = newLocation[2];
        final int fraudAmount = this.amounts.otherAmount(realAmount);
        final String fraudTransactionId = "xxx" + realTransaction.getTransactionId();
        final double fraudLon = Double.parseDouble(newLocation[0]);
        final double fraudLat =
                Double.parseDouble(newLocation[1]);

        return Transaction
                .newBuilder()
                .setAccountId(accountID)
                .setTimestamp(fraudTimestamp)
                .setAtm(fraudAtmLabel)
                .setAmount(fraudAmount)
                .setTransactionId(fraudTransactionId)
                .setLocation(
                        Location
                                .newBuilder()
                                .setLatitude(fraudLat)
                                .setLongitude(fraudLon)
                                .build()
                )
                .build();

    }

    private void publish(final Producer<? super String, ? super Transaction> producer, final Transaction transaction) {
        try {
            producer.send(new ProducerRecord<>(this.getOutputTopic(), transaction.getTransactionId(), transaction));
        } catch (final RuntimeException e) {
            log.error("Some Error occurred  while producing the transaction <{}> into the topic <{}>.",
                    transaction.getTransactionId(), this.getOutputTopic());
            throw new RuntimeException(e);
        }
    }

    private static class Amounts {
        private final int[] amountList = {50, 100, 150, 200};


        private int randomAmount() {
            return this.amountList[randGenerator.nextInt(this.amountList.length)];
        }

        private int otherAmount(final int oldAmount) {
            while (true) {
                final int newAmount = this.amountList[randGenerator.nextInt(this.amountList.length)];
                if (newAmount != oldAmount) {
                    return newAmount;
                }
            }

        }
    }
}
