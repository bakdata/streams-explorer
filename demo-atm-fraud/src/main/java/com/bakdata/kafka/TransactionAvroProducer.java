package com.bakdata.kafka;

import java.time.Instant;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Properties;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.kstream.Consumed;
import org.apache.kafka.streams.kstream.KStream;
import org.apache.kafka.streams.kstream.ValueTransformer;
import org.apache.kafka.streams.processor.ProcessorContext;
import org.json.JSONObject;

public class TransactionAvroProducer extends KafkaStreamsApplication {

  public static void main(final String[] args) {
    startApplication(new TransactionAvroProducer(), args);
  }

  @Override
  public void buildTopology(final StreamsBuilder builder) {
    final KStream<String, String> input = builder.stream(this.getInputTopics(), Consumed.with(Serdes.String(), Serdes.String()));

    final KStream<String, ProcessedValue<String, Transaction>> mapped =
        input.transformValues(() -> ErrorCapturingValueTransformer.captureErrors(new ValueTransformerTransaction()));

    mapped.flatMapValues(ProcessedValue::getValues)
        .to(this.getOutputTopic());

    mapped.flatMapValues(ProcessedValue::getErrors)
        .to(this.getErrorTopic());
  }

  @Override
  public String getUniqueAppId() {
    return "streams-explorer-transactionavroproducer-" + this.getOutputTopic();
  }

  @Override
  protected Properties createKafkaProperties() {
    final Properties kafkaProperties = super.createKafkaProperties();
    kafkaProperties.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.StringSerde.class);
    return kafkaProperties;
  }

  private static class ValueTransformerTransaction
      implements ValueTransformer<String, Transaction> {

    @Override
    public void init(final ProcessorContext context) {
    }

    @Override
    public Transaction transform(final String value) {
      final JSONObject input = new JSONObject(value);
      final JSONObject location = input.getJSONObject("location");
      return Transaction
          .newBuilder()
          .setAccountId(input.getString("account_id"))
          .setTimestamp(this.parseDateTimeString(input.getString("timestamp")))
          .setAtm(input.getString("atm"))
          .setAmount(input.getInt("amount"))
          .setTransactionId(input.getString("transaction_id"))
          .setLocation(
              Location
                  .newBuilder()
                  .setLatitude(location.getDouble("lat"))
                  .setLongitude(location.getDouble("lon"))
                  .build()
          )
          .build();
    }

    @Override
    public void close() {
      // do nothing
    }

    public Instant parseDateTimeString(final String dateTimeString) {
      final ZonedDateTime parsedDateTime = ZonedDateTime.parse(dateTimeString,
          DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss Z"));
      return parsedDateTime.toInstant();
    }
  }
}
