import { DownOutlined } from "@ant-design/icons";
import { Alert, Button, Dropdown, Menu, Space, Spin } from "antd";
import React, { useEffect, useState } from "react";
import ReactJson from "react-json-view";
import {
  getNodeSchemaApiNodeNodeIdSchemaVersionGetResponse200,
  getNodeSchemaVersionsApiNodeNodeIdSchemaGetResponse200,
  useGetNodeSchemaApiNodeNodeIdSchemaVersionGet,
  useGetNodeSchemaVersionsApiNodeNodeIdSchemaGet,
} from "../lib/api/fetchers";
import style from "./Details.module.css";

interface SchemaProps {
  nodeId: string;
}

const Schema = ({ nodeId }: SchemaProps) => {
  const [schemaVersion, setSchemaVersion] = useState<number | null>(null);
  const {
    data: versionsResponse,
    isLoading: versionsLoading,
    error: versionsError,
  } = useGetNodeSchemaVersionsApiNodeNodeIdSchemaGet(nodeId);
  const versions =
    versionsResponse?.status === 200
      ? (
        versionsResponse as getNodeSchemaVersionsApiNodeNodeIdSchemaGetResponse200
      ).data
      : undefined;

  const menu = (
    <Menu
      data-testid="schema-version-select"
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
    data: schemaResponse,
    refetch: fetchSchema,
    isFetching: schemaLoading,
    error: schemaError,
  } = useGetNodeSchemaApiNodeNodeIdSchemaVersionGet(
    nodeId,
    schemaVersion as number,
    { query: { enabled: false } }
  );
  const schema =
    schemaResponse?.status === 200
      ? (
        schemaResponse as getNodeSchemaApiNodeNodeIdSchemaVersionGetResponse200
      ).data
      : undefined;

  useEffect(() => {
    if (versions) {
      setSchemaVersion(versions[versions.length - 1]);
    }
  }, [versions]);

  useEffect(() => {
    if (schemaVersion) {
      fetchSchema();
    }
  }, [schemaVersion]); // eslint-disable-line react-hooks/exhaustive-deps

  if (schemaLoading || versionsLoading) {
    return (
      <div className={style.loadingSpinnerContainer}>
        <Spin tip="Loading schema..." />
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
          <Button data-testid="schema-version">
            v{schemaVersion} <DownOutlined />
          </Button>
        </Dropdown>
        <div className={style.jsonDetail} data-testid="schema">
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
