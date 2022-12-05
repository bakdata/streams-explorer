import { CopyOutlined } from "@ant-design/icons";
import { Alert, Button, Descriptions, message, Space, Spin } from "antd";
import copy from "copy-to-clipboard";
import React from "react";
import ReactJson from "react-json-view";
import {
  useGetLinkingApiNodeLinkingNodeIdGet,
  useGetNodeInfoApiNodeNodeIdGet,
} from "./api/apiComponents";
import { NodeInfoListItem } from "./api/apiSchemas";
import style from "./Details.module.css";
import Schema from "./Schema";

interface DetailsProps {
  nodeId: string;
}

const Details = ({ nodeId }: DetailsProps) => {
  const { data, isLoading, isError } = useGetNodeInfoApiNodeNodeIdGet({
    pathParams: { nodeId: nodeId },
  });
  if (isLoading) {
    return (
      <div className={style.loadingSpinnerContainer}>
        <Spin tip="Loading..." />
      </div>
    );
  }
  if (!data || isError) {
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
      <Descriptions.Item className={style.descItem} label="Type" key={1}>
        {data.node_type}
      </Descriptions.Item>
      {data.info.map((nodeInfoListItem) => (
        <Descriptions.Item
          className={style.descItem}
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
      return infoListItem.name === "Schema"
        ? <Schema nodeId={nodeId} />
        : (
          <div className={style.jsonDetail}>
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
  const { data: linkToService, isLoading } =
    useGetLinkingApiNodeLinkingNodeIdGet(
      {
        pathParams: { nodeId: nodeId },
        queryParams: { link_type: infoListItem.value as string },
      }
    );

  if (isLoading) {
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
