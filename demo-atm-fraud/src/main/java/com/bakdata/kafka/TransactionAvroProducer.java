package com.bakdata.kafka;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.text.SimpleDateFormat;
import java.time.Instant;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import java.util.Properties;
import java.util.Random;
import java.util.TimeZone;
import java.util.UUID;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.Serdes;

public class TransactionAvroProducer extends KafkaProducerApplication {

    public static void main(final String[] args) {
        startApplication(new TransactionAvroProducer(), args);
    }

    private Map<Integer, String[]> allLocations;
    private static final Random randGenerator = new Random();

    public void setAllLocations() {
        allLocations = new HashMap<>();
    }

    public void addLocation(int key, String[] values) {
        allLocations.put(key, values);
    }

    public Map<Integer, String[]> getAllLocations() {
        return this.allLocations;
    }

    private String fileName = "atm_locations.csv";

    @Override
    protected Properties createKafkaProperties() {
        final Properties kafkaProperties = super.createKafkaProperties();
        kafkaProperties.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, Serdes.StringSerde.class);
        return kafkaProperties;
    }

    @Override
    protected void runApplication() {
        //every 51st transaction is an  fraudulent transaction
        int bound = 50;
        ClassLoader classLoader = getClass().getClassLoader();
        InputStream inputStream = classLoader.getResourceAsStream(fileName);
        InputStreamReader streamReader = new InputStreamReader(inputStream, StandardCharsets.UTF_8);
        this.allLocations = this.loadCsvData(streamReader);
        int amountLocation = this.allLocations.size();

        try (final KafkaProducer<String, Transaction> producer = this.createProducer()) {
            int counter = 0;
            int fraud_index = 0;
            while (true) {
                ArrayList<Transaction> realTransactions = new ArrayList<>();
                /*decide which Transaction would use to create a fraudulent transaction*/
                int fraudIndex = counter % bound;
                Transaction oldTransaction = new Transaction();

                for (int i = 0; i < bound; i++) {
                    String accoundId = "a" + randGenerator.nextInt(1000);
                    String timestamp = getTimestamp();
                    int amount = AMOUNTS.randomAmount();
                    UUID uuid = UUID.randomUUID();
                    String transaction_id = uuid.toString();

                    int index = randGenerator.nextInt(amountLocation - 1);
                    String[] locationDetails = allLocations.get(index);
                    double lon = Double.parseDouble(locationDetails[0]), lat = Double.parseDouble(locationDetails[1]);
                    String atm_label = locationDetails[2];

                    //create transaction
                    Transaction newRealTransaction =
                            this.createTransaction(accoundId, timestamp, atm_label, amount, transaction_id, lon, lat);
                    //publish real transaction
                    this.publish(producer, newRealTransaction);
                    if (i == fraudIndex) {
                        oldTransaction = newRealTransaction;
                        //new location
                        fraud_index = index + 1;
                    }
                }

                // create fraudulent transaction
                Transaction fraudTransaction = createFraudTransaction(oldTransaction, fraud_index);

                //publish fraudulent transaction
                this.publish(producer, fraudTransaction);

                counter++;
            }
        }
    }

    protected Map<Integer, String[]> loadCsvData(InputStreamReader streamReader) {
        Map<Integer, String[]> locations = new HashMap<Integer, String[]>();
        String line = "";
        String splitBy = ",";
        Integer count = 0;

        BufferedReader reader = null;
        try {
            reader = new BufferedReader(streamReader);

            while ((line = reader.readLine()) != null)   //returns a Boolean value
            {
                String[] row = line.split(splitBy);    // use comma as separator
                String lon = row[0], lat = row[1], atm_label = row[2];
                locations.put(count, new String[]{lon, lat, atm_label});
                count++;
            }
        } catch (FileNotFoundException e) {
            throw new RuntimeException(e);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        return locations;
    }

    private String getTimestamp() {
        SimpleDateFormat gmtDateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        gmtDateFormat.setTimeZone(TimeZone.getTimeZone("GMT"));
        String currentTime = gmtDateFormat.format(new Date()) + " +0000";
        return currentTime;

    }

    protected Transaction createTransaction(String accoundID, String timestamp, String atm_label, int amount,
            String transaction_id, double lon, double lat) {
        ZonedDateTime parsedDateTime = ZonedDateTime.parse(timestamp,
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
    protected Transaction createFraudTransaction(Transaction realTransaction, int newLocationIndex) {
        String[] newLocation = allLocations.get(newLocationIndex);
        int real_amount = realTransaction.getAmount(); // must be changed
        Instant realtimestamp = realTransaction.getTimestamp(); // must be changed
        int dif = randGenerator.nextInt(10) + 1;

        String accountID = realTransaction.getAccountId();  // remains the same
        Instant fraudTimestamp = realtimestamp.minus(dif, ChronoUnit.MINUTES); // changed
        String fraudAtm_label = newLocation[2]; // changed
        int fraudAmount = AMOUNTS.otherAmount(real_amount); // changed
        String fraudTransactionId = "xxx" + realTransaction.getTransactionId(); // // changed
        double fraud_lon = Double.parseDouble(newLocation[0]), fraud_lat =
                Double.parseDouble(newLocation[1]); // changed

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

    private void publish(final KafkaProducer<String, Transaction> producer, Transaction transaction) {
        producer.send(new ProducerRecord<>(this.getOutputTopic(), transaction.getTransactionId(), transaction));
    }

    private enum AMOUNTS {
        fifty(50), hund(100), fiftyHund(150), twoHund(200);
        private int amount;

        AMOUNTS(int newAmount) {
            this.amount = newAmount;
        }

        private static int randomAmount() {
            AMOUNTS ams[] = AMOUNTS.values();
            return ams[randGenerator.nextInt(ams.length)].amount;
        }

        private static int otherAmount(int oldAmount) {
            while (true) {
                AMOUNTS ams[] = AMOUNTS.values();
                int newAmount = ams[randGenerator.nextInt(ams.length)].amount;
                if (newAmount != oldAmount) {
                    return newAmount;
                }
            }
        }
    }
}
