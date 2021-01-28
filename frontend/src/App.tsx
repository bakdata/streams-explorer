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
  const refreshIntervals = [0, 10, 30, 60];
  const [currentRefreshInterval, setCurrentRefreshInterval] = useState(
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
    if (currentRefreshInterval && currentRefreshInterval > 0) {
      const interval = setInterval(
        refetchMetrics,
        currentRefreshInterval * 1000
      );
      return () => clearInterval(interval);
    }
  }, [refetchMetrics, currentRefreshInterval]);

  if (graphError) {
    message.error(graphError.message);
    return <Spin spinning={false} tip="Failed to load graph" />;
  }
  if (pipelineError) {
    message.error(pipelineError?.message);
  }

  graphConfig.height =
    height > window.screen.height
      ? window.screen.height * 0.66 - 64
      : height * 0.66 - 64;
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
      {pipelines?.pipelines.map((name: any) => (
        <Menu.Item key={name}>{name}</Menu.Item>
      ))}
    </Menu>
  );

  const menuRefresh = (
    <Menu
      onClick={(e) => {
        setCurrentRefreshInterval(Number(e.key));
      }}
    >
      {refreshIntervals.map((interval: number) => (
        <Menu.Item key={interval}>{interval}s</Menu.Item>
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
              <Menu.Item>
                Refresh:&nbsp;
                <Dropdown overlay={menuRefresh} placement="bottomRight" arrow>
                  <Button>{currentRefreshInterval}s</Button>
                </Dropdown>
              </Menu.Item>
            </Menu>
          </Header>
          <Content style={{ minHeight: "100vh", paddingTop: "64px" }}>
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
            <Row style={{ padding: "0 50px", width: width }}>
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
