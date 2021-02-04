import React, { useState, useRef, useEffect } from "react";
import "./App.css";
import useDimensions from "react-cool-dimensions";
import {
  usePipelinesApiPipelinesGet,
  useGraphPositionedApiGraphGet,
  useMetricsApiMetricsGet,
} from "./api/fetchers";
import {
  Layout,
  Menu,
  Dropdown,
  Button,
  Row,
  Spin,
  message,
  Alert,
} from "antd";
import { DownOutlined } from "@ant-design/icons";
import { graphConfig } from "./graphConfiguration";
import DetailsCard from "./components/DetailsCard";
import GraphVisualization from "./components/GraphVisualization";
import { useMutate } from "restful-react";

const { Header, Content } = Layout;

const App: React.FC = () => {
  const ALL_PIPELINES = "all pipelines";
  const [currentPipeline, setCurrentPipeline] = useState(ALL_PIPELINES);
  const [selectedNodeID, setSelectedNodeID] = useState<string | null>(null);
  const ref = useRef<HTMLDivElement>(null!);
  const { width, height } = useDimensions({ ref });
  const defaultRefreshInterval = 30;
  const refreshIntervals: Record<number, string> = {
    0: "off",
    60: "60s",
    30: "30s",
    10: "10s",
  };
  const [refreshInterval, setRefreshInterval] = useState(
    defaultRefreshInterval
  );

  const { mutate: update, loading: isUpdating } = useMutate({
    verb: "POST",
    path: "/api/update",
  });

  const {
    data: graph,
    loading: isLoadingGraph,
    error: graphError,
  } = useGraphPositionedApiGraphGet({
    queryParams:
      currentPipeline !== ALL_PIPELINES
        ? { pipeline_name: currentPipeline }
        : undefined,
  });

  const {
    data: pipelines,
    loading: isLoadingPipelines,
    error: pipelineError,
  } = usePipelinesApiPipelinesGet({});

  const { data: metrics, refetch: refetchMetrics } = useMetricsApiMetricsGet(
    {}
  );

  useEffect(() => {
    if (refreshInterval && refreshInterval > 0) {
      const interval = setInterval(refetchMetrics, refreshInterval * 1000);
      return () => clearInterval(interval);
    }
  }, [refetchMetrics, refreshInterval]);

  if (graphError) {
    message.error(graphError.message);
    return <Spin spinning={false} tip="Failed to load graph" />;
  }
  if (pipelineError) {
    message.error(pipelineError?.message);
  }

  // graphConfig.height =
  //   height > window.screen.height
  //     ? window.screen.height * 0.66 - 64
  //     : height * 0.66 - 64;
  graphConfig.height = height - 64;
  graphConfig.width = width;

  const menuPipeline = (
    <Menu
      onClick={(e) => {
        setCurrentPipeline(e.key.toString());
      }}
    >
      <Menu.Item key={ALL_PIPELINES}>
        <i>{ALL_PIPELINES}</i>
      </Menu.Item>
      {pipelines?.pipelines.map((name: string) => (
        <Menu.Item key={name}>{name}</Menu.Item>
      ))}
    </Menu>
  );

  const menuRefresh = (
    <Menu
      onClick={(e) => {
        setRefreshInterval(Number(e.key));
      }}
    >
      {Object.keys(refreshIntervals).map((key: any) => (
        <Menu.Item key={key}>{refreshIntervals[key]}</Menu.Item>
      ))}
    </Menu>
  );

  if (!isLoadingGraph && !isLoadingPipelines && !isUpdating) {
    return (
      <div ref={ref} className="application">
        <Layout className="layout">
          <Header className="header">
            <Menu theme="dark" mode="horizontal" selectable={false}>
              <Menu.Item key="1">
                Pipeline:&nbsp;
                <Dropdown overlay={menuPipeline} placement="bottomLeft" arrow>
                  <Button>{currentPipeline}</Button>
                </Dropdown>
              </Menu.Item>
              <Menu.Item
                onClick={() => {
                  update({})
                    .then(() => window.location.reload())
                    .catch(() => message.error("Failed to update!"));
                }}
              >
                <Button type="dashed" ghost={true}>
                  Update Graphs
                </Button>
              </Menu.Item>
              <Menu.Item style={{ float: "right" }}>
                Metrics refresh:&nbsp;
                <Dropdown overlay={menuRefresh}>
                  <a>
                    {refreshIntervals[refreshInterval]} <DownOutlined />
                  </a>
                </Dropdown>
              </Menu.Item>
            </Menu>
          </Header>
          <Content
            style={{
              minHeight: "100vh",
              paddingTop: "64px",
              // overflow: "auto",
              // position: "fixed",
            }}
          >
            <Row>
              {graph ? (
                <GraphVisualization
                  id="topology-graph"
                  data={graph}
                  config={graphConfig}
                  metrics={metrics}
                  refetchMetrics={() => refetchMetrics()}
                  onClickNode={(nodeId: string) => setSelectedNodeID(nodeId)}
                />
              ) : (
                <Alert
                  message="Error"
                  description="Could not load graph"
                  type="error"
                  showIcon
                />
              )}
            </Row>
            <Row
              style={{
                position: "fixed",
                top: "66%",
                padding: "0 50px",
                // top: 0,
                // bottom: 0,
                // left: 0,
                // right: 0,
                width: width,
                zIndex: 999,
                maxHeight: "100%",
                overflowY: "auto",
              }}
            >
              <DetailsCard nodeID={selectedNodeID} />
            </Row>
          </Content>
        </Layout>
      </div>
    );
  }

  return (
    <div ref={ref} className="application">
      <div className="spinningContainer">
        <Spin tip={isUpdating ? "Updating Pipelines..." : "Loading..."} />
      </div>
    </div>
  );
};

export default App;
