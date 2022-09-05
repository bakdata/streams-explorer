from typing import TypeVar

from loguru import logger

from streams_explorer.core.config import settings
from streams_explorer.core.k8s_app import K8sApp
from streams_explorer.models.node_information import NodeInfoListItem, NodeInfoType

V = TypeVar("V")


def find(element: str, json: dict) -> dict:
    keys = element.split(".")
    key_value = json
    for key in keys:
        key_value = key_value[key]
    return key_value


def get_info(key: str, config: dict[str, V]) -> V | dict[str, V] | None:
    if value := config.get(key):
        return value

    try:
        return find(key, config)
    except KeyError:
        return None


def get_type(value) -> NodeInfoType:
    if isinstance(value, dict):
        return NodeInfoType.JSON
    return NodeInfoType.BASIC


def get_displayed_info(
    displayed_info_settings: list[dict[str, str]], config: dict
) -> list[NodeInfoListItem]:
    node_infos = []
    for item in displayed_info_settings:
        name = item.get("name")
        key = item.get("key")
        if not name or not key:
            continue

        value = get_info(key, config)
        if value is None:
            logger.warning(f'Could not find key "{key}"')
        else:
            value_type = get_type(value)
            if value_type != NodeInfoType.JSON:
                value = str(value)
            node_infos.append(NodeInfoListItem(name=name, value=value, type=value_type))
    return node_infos


def get_displayed_information_connector(config: dict) -> list[NodeInfoListItem]:
    connector_settings = settings.kafkaconnect.displayed_information
    return get_displayed_info(connector_settings, config)


def get_displayed_information_deployment(k8s: K8sApp) -> list[NodeInfoListItem]:
    k8s_settings = settings.k8s.displayed_information
    return get_displayed_info(k8s_settings, k8s.to_dict())


def get_displayed_information_topic(config: dict) -> list[NodeInfoListItem]:
    kafka_settings = settings.kafka.displayed_information
    return get_displayed_info(kafka_settings, config)
