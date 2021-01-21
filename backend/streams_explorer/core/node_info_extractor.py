from typing import Dict, List, Optional

from loguru import logger

from streams_explorer.core.config import settings
from streams_explorer.core.k8s_app import K8sApp
from streams_explorer.models.node_information import NodeInfoListItem, NodeInfoType


def find(element: str, json: dict):
    keys = element.split(".")
    key_value = json
    for key in keys:
        key_value = key_value[key]
    return key_value


def get_info(key: str, config: dict) -> Optional[object]:
    if config.get(key):
        return config.get(key)
    else:
        try:
            return find(key, config)
        except KeyError:
            return None


def get_type(value):
    if type(value) is dict:
        return NodeInfoType.JSON
    return NodeInfoType.BASIC


def get_displayed_info(
    displayed_info_settings: List[Dict[str, str]], config: dict
) -> List[NodeInfoListItem]:
    node_infos = []
    for item in displayed_info_settings:
        name: Optional[str] = item.get("name")
        key: Optional[str] = item.get("key")
        if key is None:
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


def get_displayed_information_connector(config: dict) -> List[NodeInfoListItem]:
    connector_settings = settings.kafkaconnect.displayed_information
    return get_displayed_info(connector_settings, config)


def get_displayed_information_deployment(k8s: K8sApp) -> List[NodeInfoListItem]:
    k8s_settings = settings.k8s.displayed_information
    return get_displayed_info(k8s_settings, k8s.to_dict())
