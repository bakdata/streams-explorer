package com.bakdata.kafka;

import com.opencsv.CSVReader;
import com.opencsv.exceptions.CsvException;
import com.opencsv.exceptions.CsvValidationException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.text.SimpleDateFormat;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
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


    private List<AtmLocation> allLocations = new ArrayList<>();
    private static final Random randGenerator = new Random();

    public void addLocation(final AtmLocation atmLocation) {
        this.allLocations.add(atmLocation);
    }

    private final Amounts amounts = new Amounts();

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
        final String fileName = "atm_locations.csv";

        try {
            this.allLocations = loadCsvData(fileName);
        } catch (final IOException | CsvValidationException e) {
            throw new RuntimeException("Error occurred while loading the CSV.", e);
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
        final AtmLocation locationDetails = this.allLocations.get(index);
        final double lon = locationDetails.getLongitude();
        final double lat = locationDetails.getLatitude();
        final String atmLabel = locationDetails.getAtmLabel();

        return createTransaction(accountId, timestamp, atmLabel, amount, transactionId, lon,
                lat);
    }

    public static List<AtmLocation> loadCsvData(final String fileName) throws IOException, CsvValidationException {
        ClassLoader classLoader = AccountProducer.class.getClassLoader();
        final InputStream inputStream = classLoader.getResourceAsStream(fileName);
        String[] line = null;
        List<AtmLocation> allLocations = new ArrayList<>();
        try (InputStreamReader streamReader = new InputStreamReader(inputStream, StandardCharsets.UTF_8);
                final CSVReader csvReader = new CSVReader(streamReader)) {
            while (((line = csvReader.readNext()) != null)) {
                AtmLocation locationDetails =
                        new AtmLocation(line[2], Double.parseDouble(line[0]), Double.parseDouble(line[1]));
                allLocations.add(locationDetails);
            }
            return allLocations;
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
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss Z");

        final LocalDateTime parsedDateTime = LocalDateTime.parse(timestamp, formatter);
        return Transaction
                .newBuilder()
                .setAccountId(accoundID)
                .setTimestamp(parsedDateTime.toInstant(ZoneOffset.UTC))
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
        final AtmLocation newLocation = this.allLocations.get(newLocationIndex);
        final int realAmount = realTransaction.getAmount();
        final Instant realtimestamp = realTransaction.getTimestamp();
        final int dif = randGenerator.nextInt(10) + 1;

        final String accountID = realTransaction.getAccountId();
        final Instant fraudTimestamp = realtimestamp.minus(dif, ChronoUnit.MINUTES);
        final String fraudAtmLabel = newLocation.getAtmLabel();
        final int fraudAmount = this.amounts.otherAmount(realAmount);
        final String fraudTransactionId = "xxx" + realTransaction.getTransactionId();
        final double fraudLon = newLocation.getLongitude();
        final double fraudLat = newLocation.getLatitude();

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
        producer.send(new ProducerRecord<>(this.getOutputTopic(), transaction.getTransactionId(), transaction));
    }

}
