import React, { useState, useRef, useEffect, useCallback } from "react";
import "./App.css";
import { useResizeDetector } from "react-resize-detector";
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
  const onResize = useCallback(() => {}, []);
  const { width, height } = useResizeDetector({
    targetRef: ref,
    refreshMode: "debounce",
    refreshRate: 100,
    onResize,
  });
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
          <Header className="header" style={{ zIndex: 2 }}>
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
                  <a href={"dummy"}>
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
              position: "relative",
            }}
          >
            <Row style={{ position: "fixed" }}>
              {graph ? (
                <GraphVisualization
                  id="topology-graph"
                  data={graph}
                  config={graphConfig}
                  metrics={metrics}
                  refetchMetrics={() => refetchMetrics()}
                  onClickNode={(nodeId: string) => setSelectedNodeID(nodeId)}
                  width={width}
                  height={height! - 64}
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
                padding: "0 50px",
                width: width,
                zIndex: 1,
                top: height! - 147,
                position: "absolute",
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
