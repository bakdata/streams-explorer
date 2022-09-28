package com.bakdata.kafka;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.text.SimpleDateFormat;
import java.time.Instant;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoUnit;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import java.util.Properties;
import java.util.Random;
import java.util.TimeZone;
import java.util.UUID;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.Producer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.StringSerializer;
import picocli.CommandLine;

public class TransactionAvroProducer extends KafkaProducerApplication {

    //every 51st transaction is an  fraudulent transaction
    @CommandLine.Option(names = "--real-tx",
            description = "How many real transactions must be generated before a fraudulent transaction can be "
                    + "generated?")
    private int bound = 9;
    // 1 iteration = {bound} real transactions + one fraudulent transaction
    @CommandLine.Option(names = "--iteration",
            description = "One iteration contains $BOUND real transactions and one fraudulent transaction")
    private int iterations = 20;
    // by default, a total of 200 data will be generated

    public static void main(final String[] args) {
        startApplication(new TransactionAvroProducer(), args);
    }

    public void setIterations(final int iterations) {
        this.iterations = iterations;
    }


    public void setBound(final int bound) {
        this.bound = bound;
    }


    private Map<Integer, String[]> allLocations = null;
    private static final Random randGenerator = new Random();

    public void setAllLocations() {
        this.allLocations = new HashMap<>();
    }

    public void addLocation(final int key, final String[] values) {
        this.allLocations.put(key, values);
    }

    @Override
    protected Properties createKafkaProperties() {
        final Properties kafkaProperties = super.createKafkaProperties();
        kafkaProperties.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        return kafkaProperties;
    }

    @Override
    protected void runApplication() {
        final KafkaProducer<String, Transaction> producer = this.createProducer();
        final ClassLoader classLoader = this.getClass().getClassLoader();
        final String fileName = "atm_locations.csv";
        final InputStream inputStream = classLoader.getResourceAsStream(fileName);
        InputStreamReader streamReader = null;
        if (inputStream != null) {
            streamReader = new InputStreamReader(inputStream, StandardCharsets.UTF_8);
        }
        this.allLocations = loadCsvData(streamReader);
        final int amountLocation = this.allLocations.size();
        int counter = 0;
        do {
            final int fraud_index = counter % this.bound;
            Transaction oldTransaction = new Transaction();

            for (int i = 0; i < this.bound; i++) {
                final Transaction newRealTransaction = this.createRealTimeTransaction(amountLocation);
                this.publish(producer, newRealTransaction);
                if (i == fraud_index) {
                    oldTransaction = newRealTransaction;
                }
            }
            final Transaction fraudTransaction = this.createFraudTransaction(oldTransaction, fraud_index);
            this.publish(producer, fraudTransaction);
            counter++;
        } while (counter != this.iterations);
    }

    private Transaction createRealTimeTransaction(final int amountLocation) {
        final String account_id = "a" + randGenerator.nextInt(1000);
        final String timestamp = getTimestamp();
        final int amount = AMOUNTS.randomAmount();
        final UUID uuid = UUID.randomUUID();
        final String transaction_id = uuid.toString();

        final int index = randGenerator.nextInt(amountLocation - 1);
        final String[] locationDetails = this.allLocations.get(index);
        final double lon = Double.parseDouble(locationDetails[0]);
        final double lat = Double.parseDouble(locationDetails[1]);
        final String atm_label = locationDetails[2];

        return createTransaction(account_id, timestamp, atm_label, amount, transaction_id, lon,
                lat);
    }

    static Map<Integer, String[]> loadCsvData(final InputStreamReader streamReader) {
        final Map<Integer, String[]> locations = new HashMap<Integer, String[]>();
        String line = "";
        final String splitBy = ",";
        Integer count = 0;

        final BufferedReader reader = new BufferedReader(streamReader);
        try {

            while ((line = reader.readLine()) != null)   //returns a Boolean value
            {
                final String[] row = line.split(splitBy);    // use comma as separator
                final String lon = row[0];
                final String lat = row[1];
                final String atm_label = row[2].replace("\"", "");
                locations.put(count, new String[]{lon, lat, atm_label});
                count++;
            }
        } catch (final IOException e) {
            throw new RuntimeException(e);
        } finally {
            try {
                reader.close();
            } catch (final IOException e) {
                e.printStackTrace();
            }
        }
        return locations;
    }

    private static String getTimestamp() {
        final SimpleDateFormat gmtDateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        gmtDateFormat.setTimeZone(TimeZone.getTimeZone("GMT"));
        return gmtDateFormat.format(new Date()) + " +0000";

    }

    static Transaction createTransaction(final String accoundID, final String timestamp,
            final String atm_label,
            final int amount,
            final String transaction_id, final double lon, final double lat) {
        final ZonedDateTime parsedDateTime = ZonedDateTime.parse(timestamp,
                DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss Z"));
        return Transaction
                .newBuilder()
                .setAccountId(accoundID) //string
                .setTimestamp(parsedDateTime.toInstant()) //Instant
                .setAtm(atm_label) //string
                .setAmount(amount) //int
                .setTransactionId(transaction_id) //string
                .setLocation(
                        Location
                                .newBuilder()
                                .setLatitude(lat) //double
                                .setLongitude(lon) //double
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
        final int real_amount = realTransaction.getAmount(); // must be changed
        final Instant realtimestamp = realTransaction.getTimestamp(); // must be changed
        final int dif = randGenerator.nextInt(10) + 1;

        final String accountID = realTransaction.getAccountId();  // remains the same
        final Instant fraudTimestamp = realtimestamp.minus(dif, ChronoUnit.MINUTES); // changed
        final String fraudAtm_label = newLocation[2]; // changed
        final int fraudAmount = AMOUNTS.otherAmount(real_amount); // changed
        final String fraudTransactionId = "xxx" + realTransaction.getTransactionId(); // // changed
        final double fraud_lon = Double.parseDouble(newLocation[0]); // changed
        final double fraud_lat =
                Double.parseDouble(newLocation[1]);

        return Transaction
                .newBuilder()
                .setAccountId(accountID)
                .setTimestamp(fraudTimestamp)
                .setAtm(fraudAtm_label)
                .setAmount(fraudAmount)
                .setTransactionId(fraudTransactionId)
                .setLocation(
                        Location
                                .newBuilder()
                                .setLatitude(fraud_lat)
                                .setLongitude(fraud_lon)
                                .build()
                )
                .build();

    }

    private void publish(final Producer<? super String, ? super Transaction> producer, final Transaction transaction) {
        producer.send(new ProducerRecord<>(this.getOutputTopic(), transaction.getTransactionId(), transaction));
    }

    private enum AMOUNTS {
        fifty(50), hund(100), fiftyHund(150), twoHund(200);
        private final int amount;

        AMOUNTS(final int newAmount) {
            this.amount = newAmount;
        }

        private static int randomAmount() {
            final AMOUNTS[] ams = values();
            return ams[randGenerator.nextInt(ams.length)].amount;
        }

        private static int otherAmount(final int oldAmount) {
            while (true) {
                final AMOUNTS[] ams = values();
                final int newAmount = ams[randGenerator.nextInt(ams.length)].amount;
                if (newAmount != oldAmount) {
                    return newAmount;
                }
            }
        }
    }
}
