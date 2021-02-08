import React from "react";
import {
  useNodeInfoApiNodeNodeIdGet,
  NodeInfoListItem,
  useLinkingApiNodeLinkingNodeIdGet,
} from "../api/fetchers";
import { Spin, Alert, Descriptions, Button, Space, message } from "antd";
import ReactJson from "react-json-view";
import { CopyOutlined } from "@ant-design/icons";
import copy from "copy-to-clipboard";

interface DetailsProps {
  nodeID: string;
}

const Details = ({ nodeID }: DetailsProps) => {
  const { data, loading, error } = useNodeInfoApiNodeNodeIdGet({
    node_id: nodeID,
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
          <NodeInfoDetail infoListItem={nodeInfoListItem} nodeID={nodeID} />
        </Descriptions.Item>
      ))}
    </Descriptions>
  );
};

interface NodeInfoDetailProps {
  infoListItem: NodeInfoListItem;
  nodeID: string;
}

const NodeInfoDetail = ({ infoListItem, nodeID }: NodeInfoDetailProps) => {
  switch (infoListItem.type) {
    case "json":
      return (
        <div className="jsonDetail">
          <ReactJson
            src={infoListItem.value}
            displayDataTypes={false}
            collapsed={false}
          />
        </div>
      );

    case "link":
      return <LinkInfo nodeID={nodeID} infoListItem={infoListItem} />;
    default:
      return <React.Fragment>{infoListItem.value}</React.Fragment>;
  }
};

const LinkInfo = ({ infoListItem, nodeID }: NodeInfoDetailProps) => {
  let linkType =
    infoListItem.value !== "" && typeof infoListItem.value == "string"
      ? infoListItem.value
      : undefined;
  const { data: linkToService, loading } = useLinkingApiNodeLinkingNodeIdGet({
    node_id: nodeID,
    queryParams: { link_type: linkType },
  });

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
