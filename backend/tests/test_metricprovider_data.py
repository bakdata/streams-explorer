from streams_explorer.models.node_types import NodeTypesEnum

nodes = [
    (
        "atm-fraud-transactionavroproducer",
        {
            "node_type": NodeTypesEnum.STREAMING_APP,
            "consumer_group": "streams-explorer-transactionavroproducer-atm-fraud-incoming-transactions-topic",
        },
    ),
    (
        "atm-fraud-incoming-transactions-topic",
        {
            "node_type": NodeTypesEnum.TOPIC,
        },
    ),
    (
        None,
        {
            "node_type": NodeTypesEnum.ERROR_TOPIC,
        },
    ),
    (
        "atm-fraud-raw-input-topic",
        {
            "node_type": NodeTypesEnum.TOPIC,
        },
    ),
]

prometheus_data = {
    "messages_in": [
        {
            "metric": {"topic": "atm-fraud-raw-input-topic"},
            "value": [1608115787.212, "0"],
        },
        {
            "metric": {"topic": "atm-fraud-incoming-transactions-topic"},
            "value": [1608115787.212, "4.80221"],
        },
    ],
    "messages_out": [
        {
            "metric": {"topic": "atm-fraud-raw-input-topic"},
            "value": [1608115787.212, "5.133333"],
        },
        {
            "metric": {"topic": "atm-fraud-incoming-transactions-topic"},
            "value": [1608115787.212, "4.80221"],
        },
    ],
    "consumer_lag": [
        {
            "metric": {
                "group": "streams-explorer-transactionavroproducer-atm-fraud-incoming-transactions-topic"
            },
            "value": [1608115880.752, "78"],
        },
        {
            "metric": {
                "group": "streams-explorer-transactionjoiner-atm-fraud-joinedtransactions-topic"
            },
            "value": [1608115880.752, "131"],
        },
        {
            "metric": {
                "group": "streams-explorer-accountlinker-atm-fraud-output-topic"
            },
            "value": [1608115880.752, "0"],
        },
        {
            "metric": {
                "group": "streams-explorer-frauddetector-atm-fraud-possiblefraudtransactions-topic"
            },
            "value": [1608115880.752, "1"],
        },
    ],
    "topic_size": [
        {
            "metric": {"topic": "atm-fraud-raw-input-topic"},
            "value": [1608117280.926, "75921"],
        },
        {
            "metric": {"topic": "atm-fraud-incoming-transactions-topic"},
            "value": [1608117280.926, "0"],
        },
    ],
}
