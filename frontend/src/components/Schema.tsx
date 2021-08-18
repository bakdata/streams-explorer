import React, { useState, useEffect } from "react";
import {
  useNodeSchemaVersionsApiNodeNodeIdSchemaGet,
  useNodeSchemaApiNodeNodeIdSchemaVersionGet,
} from "../api/fetchers";
import { Spin, Space, Alert, Button, Menu, Dropdown } from "antd";
import ReactJson from "react-json-view";
import { DownOutlined } from "@ant-design/icons";

interface SchemaProps {
  nodeID: string;
}

const Schema = ({ nodeID }: SchemaProps) => {
  const [schemaVersion, setSchemaVersion] = useState<number | null>(null);
  const {
    data: versions,
    loading: versionsLoading,
    error: versionsError,
  } = useNodeSchemaVersionsApiNodeNodeIdSchemaGet({
    node_id: nodeID,
  });

  const menu = (
    <Menu
      onClick={(e: any) => {
        setSchemaVersion(e.key);
      }}
    >
      {versions?.map((version: number) => (
        <Menu.Item key={version}>v{version}</Menu.Item>
      ))}
    </Menu>
  );

  const {
    data: schema,
    refetch: schemaFetch,
    loading: schemaLoading,
    error: schemaError,
  } = useNodeSchemaApiNodeNodeIdSchemaVersionGet({
    node_id: nodeID,
    version: schemaVersion!,
    lazy: true,
  });

  useEffect(() => {
    if (versions) {
      setSchemaVersion(versions[versions.length - 1]);
    }
  }, [versions]);

  useEffect(() => {
    if (schemaVersion) {
      schemaFetch();
    }
  }, [schemaVersion]); // eslint-disable-line react-hooks/exhaustive-deps

  if (schemaLoading || versionsLoading) {
    return (
      <div className="loadingSpinnerContainer">
        <Spin tip="Loading..." />
      </div>
    );
  }

  if (!versions || !versions.length || versionsError) {
    return (
      <Alert
        data-testid="no-schema-versions"
        message="No schema available"
        type="warning"
        style={{ width: "14em", textAlign: "center" }}
      />
    );
  }
  if (!schema || schemaError) {
    return (
      <Alert
        data-testid="no-schema"
        message="Error loading schema"
        type="error"
      />
    );
  }
  if (schemaVersion && schema) {
    return (
      <Space direction="vertical">
        <Dropdown overlay={menu} disabled={versions.length < 2}>
          <Button>
            v{schemaVersion} <DownOutlined />
          </Button>
        </Dropdown>
        <div className="jsonDetail">
          <ReactJson
            name={false}
            src={schema}
            displayDataTypes={false}
            collapsed={false}
          />
        </div>
      </Space>
    );
  }
  return null;
};

export default Schema;
