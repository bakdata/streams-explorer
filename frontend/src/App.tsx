import "./App.css";
import {
  usePipelinesApiPipelinesGet,
  useGraphPositionedApiGraphGet,
  useMetricsApiMetricsGet,
} from "./api/fetchers";
import DetailsCard from "./components/DetailsCard";
import GraphVisualization from "./components/GraphVisualization";
import { graphConfig } from "./graphConfiguration";
import { DownOutlined } from "@ant-design/icons";
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
import { AutoComplete } from "antd";
import React, { useState, useRef, useEffect, useCallback } from "react";
import { useResizeDetector } from "react-resize-detector";
import { useMutate } from "restful-react";
import { useHistory, useLocation } from "react-router-dom";

const { Option } = AutoComplete;

const { Header, Content } = Layout;

const App: React.FC = () => {
  const ALL_PIPELINES = "all pipelines";
  const [currentPipeline, setCurrentPipeline] = useState(ALL_PIPELINES);
  const [detailNode, setDetailNode] = useState<string | null>(null);
  const [focusedNode, setFocusedNode] = useState<string | null>(null);
  const [searchWidth, setSearchWidth] = useState<number>(300);
  const history = useHistory();

  const location = useLocation();
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

  // find longest node name and multiply string length by char width 8
  // doesn't cause long delays as builtin function
  useEffect(() => {
    if (graph) {
      setSearchWidth(
        Math.max(...graph.nodes.map((node) => node.label.length)) * 8
      );
    }
  }, [graph]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const pipeline = params.get("pipeline");
    if (pipeline) {
      setCurrentPipeline(pipeline);
    }
    const focusNode = params.get("focus-node");
    if (focusNode) {
      setFocusedNode(focusNode);
      setDetailNode(focusNode);
    }
  }, [location]);

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
        history.push(`/?pipeline=${e.key.toString()}`);
        setCurrentPipeline(e.key.toString());
        setFocusedNode(null);
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
              <Menu.Item>
                <AutoComplete
                  style={{
                    width: searchWidth,
                    maxWidth: 480,
                  }}
                  placeholder="Search Node"
                  allowClear={true}
                  defaultActiveFirstOption={true}
                  listHeight={512}
                  dropdownStyle={{
                    minWidth: searchWidth,
                  }}
                  filterOption={(inputValue, option) =>
                    option?.value
                      .toUpperCase()
                      .indexOf(inputValue.toUpperCase()) !== -1
                  }
                  defaultValue={focusedNode ? focusedNode : undefined}
                  onSelect={(nodeId: string) => {
                    setFocusedNode(nodeId);
                    setDetailNode(nodeId);
                    history.push(`/?focus-node=${nodeId}`);
                  }}
                >
                  {graph?.nodes.map((node) => (
                    <Option value={node.id} key={node.id}>
                      {node.id}
                    </Option>
                  ))}
                </AutoComplete>
              </Menu.Item>
              <Menu.Item style={{ float: "right" }}>
                Metrics refresh:&nbsp;
                <Dropdown overlay={menuRefresh}>
                  <a href={"/#"}>
                    {refreshIntervals[refreshInterval]} <DownOutlined />
                  </a>
                </Dropdown>
              </Menu.Item>
              <Menu.Item
                style={{ float: "right" }}
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
                  data={graph}
                  config={graphConfig}
                  metrics={metrics}
                  refetchMetrics={() => refetchMetrics()}
                  onClickNode={(nodeId: string) => setDetailNode(nodeId)}
                  width={width}
                  height={height! - 64}
                  focusedNode={focusedNode}
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
              <DetailsCard nodeID={detailNode} />
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
