from streams_explorer.models.node_types import NodeTypesEnum

nodes = [
    (
        "atm-fraud-transactionavroproducer",
        {
            "node_type": NodeTypesEnum.STREAMING_APP,
            "consumerGroup": "streams-explorer-transactionavroproducer-atm-fraud-incoming-transactions-topic",
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
    (
        "demo-sink",
        {
            "node_type": NodeTypesEnum.CONNECTOR,
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
            "metric": {"group": "connect-demo-sink"},
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
    "replicas": [
        {
            "metric": {"deployment": "atm-fraud-transactionavroproducer"},
            "value": [1611674899.53, "1"],
        },
    ],
    "consumer_read_rate": [
        {
            "metric": {
                "group": "streams-explorer-transactionavroproducer-atm-fraud-incoming-transactions-topic"
            },
            "value": [1608115880.752, "64.977769"],
        },
    ],
    "connector_tasks": [
        {
            "metric": {"connector": "demo-sink"},
            "value": [1613560970.102, "3"],
        },
    ],
}
