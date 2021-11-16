import { CopyOutlined } from "@ant-design/icons";
import { Alert, Button, Descriptions, message, Space, Spin } from "antd";
import copy from "copy-to-clipboard";
import React from "react";
import ReactJson from "react-json-view";
import {
  NodeInfoListItem,
  useGetLinkingApiNodeLinkingNodeIdGet,
  useGetNodeInfoApiNodeNodeIdGet,
} from "./api/fetchers";
import Schema from "./Schema";

interface DetailsProps {
  nodeId: string;
}

const Details = ({ nodeId }: DetailsProps) => {
  const { data, loading, error } = useGetNodeInfoApiNodeNodeIdGet({
    node_id: nodeId,
  });
  if (loading) {
    return (
      <div className="loadingSpinnerContainer">
        <Spin tip="Loading..." />
      </div>
    );
  }
  if (!data || error) {
    return (
      <Alert
        data-testid="no-node-info"
        message="No node details available"
        type="warning"
      />
    );
  }
  return (
    <Descriptions layout="horizontal" bordered column={1} size="small">
      <Descriptions.Item className="descItem" label="Type" key={1}>
        {data.node_type}
      </Descriptions.Item>
      {data.info.map((nodeInfoListItem) => (
        <Descriptions.Item
          className="descItem"
          label={nodeInfoListItem.name}
          key={nodeInfoListItem.name}
        >
          <NodeInfoDetail infoListItem={nodeInfoListItem} nodeId={nodeId} />
        </Descriptions.Item>
      ))}
    </Descriptions>
  );
};

interface NodeInfoDetailProps {
  infoListItem: NodeInfoListItem;
  nodeId: string;
}

const NodeInfoDetail = ({ infoListItem, nodeId }: NodeInfoDetailProps) => {
  switch (infoListItem.type) {
    case "json":
      return infoListItem.name === "Schema" ? (
        <Schema nodeId={nodeId} />
      ) : (
        <div className="jsonDetail">
          <ReactJson
            name={false}
            src={infoListItem.value as object}
            displayDataTypes={false}
            collapsed={false}
          />
        </div>
      );

    case "link":
      return <LinkInfo nodeId={nodeId} infoListItem={infoListItem} />;
    default:
      return <React.Fragment>{infoListItem.value}</React.Fragment>;
  }
};

const LinkInfo = ({ infoListItem, nodeId }: NodeInfoDetailProps) => {
  let linkType =
    infoListItem.value !== "" && typeof infoListItem.value == "string"
      ? infoListItem.value
      : undefined;
  const { data: linkToService, loading } = useGetLinkingApiNodeLinkingNodeIdGet(
    {
      node_id: nodeId,
      queryParams: { link_type: linkType },
    }
  );

  if (loading) {
    return <Spin tip="Loading link..." />;
  }
  if (linkToService) {
    return (
      <Space>
        <Button href={linkToService} type="primary" target="_blank">
          {infoListItem.name}
        </Button>

        <Button
          icon={<CopyOutlined />}
          onClick={() => {
            message.success("Copied link to clipboard");
            copy(linkToService);
          }}
        />
      </Space>
    );
  }
  return <>Could not get link to service</>;
};

export default Details;
