import React, { useState, useEffect } from "react";
import {
  useNodeSchemaVersionsApiNodeNodeIdSchemaGet,
  useNodeSchemaApiNodeNodeIdSchemaVersionGet,
} from "../api/fetchers";
import {
  Spin,
  Alert,
  Descriptions,
  Button,
  message,
  Menu,
  Dropdown,
} from "antd";
import ReactJson from "react-json-view";
import { DownOutlined } from "@ant-design/icons";

interface SchemaProps {
  nodeID: string;
}

const Schema = ({ nodeID }: SchemaProps) => {
  const [schemaVersion, setSchemaVersion] = useState<number>(0);
  const {
    data: versionsData,
    loading: versionsLoading,
    error: versionsError,
  } = useNodeSchemaVersionsApiNodeNodeIdSchemaGet({
    node_id: nodeID,
  });
  if (versionsData) {
    console.log(versionsData[versionsData.length - 1]);
  }

  function handleMenuClick(e: any) {
    message.info("Click on menu item.");
    console.log("click", e);
    setSchemaVersion(e.key);
  }

  const menu = (
    <Menu onClick={handleMenuClick}>
      {versionsData?.map((version: number) => (
        <Menu.Item key={version}>{version}</Menu.Item>
      ))}
    </Menu>
  );

  const { data, loading, error } = useNodeSchemaApiNodeNodeIdSchemaVersionGet({
    node_id: nodeID,
    version: schemaVersion,
  });

  useEffect(() => {
    if (versionsData) {
      setSchemaVersion(versionsData[versionsData.length - 1]);
    }
  }, [versionsData]);

  if (loading) {
    return (
      <div className="loadingSpinnerContainer">
        <Spin tip="Loading..." />
      </div>
    );
  }

  if (!versionsData || versionsError) {
    return (
      <Alert
        data-testid="no-node-info"
        message="No schema available"
        type="warning"
      />
    );
  }
  // if (!data || error) {
  //   return (
  //     <Alert
  //       data-testid="no-node-info"
  //       message="Error loading schema"
  //       type="error"
  //     />
  //   );
  // }
  return (
    <Descriptions layout="horizontal" bordered column={1} size="small">
      <Descriptions.Item
        className="descItem"
        label="Schema version"
        key="schema-version"
      >
        <Dropdown overlay={menu}>
          <Button>
            {schemaVersion} <DownOutlined />
          </Button>
        </Dropdown>
      </Descriptions.Item>
      {data ? (
        <Descriptions.Item className="descItem" label="Schema" key="schema">
          <div className="jsonDetail">
            <ReactJson src={data} displayDataTypes={false} collapsed={false} />
          </div>
        </Descriptions.Item>
      ) : null}
    </Descriptions>
  );
};

export default Schema;
