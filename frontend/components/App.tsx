import { DownOutlined, LoadingOutlined } from "@ant-design/icons";
import {
  Alert,
  Button,
  Dropdown,
  Layout,
  Menu,
  message,
  Row,
  Spin,
} from "antd";
import { useRouter } from "next/router";
import React, { useCallback, useEffect, useRef, useState } from "react";
import { useResizeDetector } from "react-resize-detector";
import { useMutate } from "restful-react";
import {
  HTTPValidationError,
  useGetMetricsApiMetricsGet,
  useGetPipelinesApiPipelinesGet,
  useGetPositionedGraphApiGraphGet,
} from "./api/fetchers";
import DetailsCard from "./DetailsCard";
import GraphVisualization from "./GraphVisualization";
import Node from "./Node";
import Search from "./Search";
import Settings from "./Settings";

const { Header, Content } = Layout;

const App: React.FC = () => {
  const ALL_PIPELINES = "all pipelines";
  const [currentPipeline, setCurrentPipeline] = useState(ALL_PIPELINES);
  const [detailNode, setDetailNode] = useState<Node>();
  const [focusedNode, setFocusedNode] = useState<Node>();
  const router = useRouter();
  const { query } = router;
  const ref = useRef<HTMLDivElement>(null);
  const onResize = useCallback(() => {}, []);
  const { width, height } = useResizeDetector({
    targetRef: ref,
    refreshMode: "debounce",
    refreshRate: 100,
    onResize,
  });
  const DEFAULT_REFRESH_INTERVAL = 30;
  const refreshIntervals: Record<number, string> = {
    0: "off",
    60: "60s",
    30: "30s",
    10: "10s",
  };
  const REFRESH_INTERVAL = "metrics-interval";
  const [refreshInterval, setRefreshInterval] = useState(0);
  const [animate, setAnimate] = useState(true);

  // on initial page load
  useEffect(() => {
    const storedRefreshInterval = Number(
      localStorage.getItem(REFRESH_INTERVAL) || DEFAULT_REFRESH_INTERVAL
    );
    setRefreshInterval(storedRefreshInterval);
    if (storedRefreshInterval) {
      refetchMetrics();
    }
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    localStorage.setItem(REFRESH_INTERVAL, refreshInterval.toString());
  }, [refreshInterval]);

  const { mutate: update, loading: isUpdating } = useMutate({
    verb: "POST",
    path: "/api/update",
  });

  const {
    data: graph,
    loading: isLoadingGraph,
    error: graphError,
    refetch: graphRefetch,
  } = useGetPositionedGraphApiGraphGet({
    queryParams: currentPipeline !== ALL_PIPELINES
      ? { pipeline_name: currentPipeline }
      : undefined,
  });

  const {
    refetch: retryPipelineGraph,
    error: retryPipelineGraphError,
    data: retryPipelineGraphData,
  } = useGetPositionedGraphApiGraphGet({
    queryParams: { pipeline_name: currentPipeline },
    lazy: true,
  });

  const {
    data: pipelines,
    loading: isLoadingPipelines,
    error: pipelineError,
  } = useGetPipelinesApiPipelinesGet({});

  const {
    data: metrics,
    loading: isLoadingMetrics,
    refetch: refetchMetrics,
    error: metricsError,
  } = useGetMetricsApiMetricsGet({ lazy: true });

  useEffect(() => {
    if (refreshInterval && refreshInterval > 0) {
      const interval = setInterval(refetchMetrics, refreshInterval * 1000);
      return () => clearInterval(interval);
    }
  }, [refreshInterval]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    if (!graph) return;

    const pipeline = query.pipeline as string;
    if (pipeline) {
      setCurrentPipeline(pipeline);
    }

    const focusNode = query["focus-node"] as string;
    if (focusNode) {
      const node = graph?.nodes.find((node) => node.id === focusNode);
      if (node) {
        setDetailNode(node);
        setFocusedNode(node);
      }
    }
  }, [graph, query]);

  useEffect(() => {
    if (graphError) {
      let errorMessage: string | undefined;
      if ("data" in graphError) {
        // specific pipeline was not found
        const data = graphError["data"] as HTTPValidationError;
        if (data.detail) {
          errorMessage = data.detail.toString();
        }
      }
      message.error(errorMessage || "Failed loading graph", 5);

      if (graphError.status === 404 && currentPipeline !== ALL_PIPELINES) {
        // check if a re-scrape solves it
        const hideMessage = message.warning("Refreshing pipelines", 0);
        update({})
          .then(() => {
            retryPipelineGraph();
          })
          .catch(() => {
            redirectAllPipelines();
          })
          .finally(() => {
            hideMessage();
          });
      }
    }
  }, [graphError]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    if (
      retryPipelineGraphError
      && retryPipelineGraphError.status === 404
      && currentPipeline !== ALL_PIPELINES
    ) {
      // pipeline still not found
      redirectAllPipelines();
    } else if (retryPipelineGraphData) {
      message.success("Found pipeline!");
      graphRefetch();
    } // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [retryPipelineGraphError, retryPipelineGraphData]);

  const redirectAllPipelines = () => {
    message.info("Redirecting to all pipelines");
    setCurrentPipeline(ALL_PIPELINES);
    router.push("/");
  };

  useEffect(() => {
    if (metricsError) {
      message.warning("Failed fetching metrics");
    }
  }, [metricsError]);

  useEffect(() => {
    if (pipelineError) {
      message.error("Failed loading pipeline names");
    }
  }, [pipelineError]);

  const menuPipeline = (
    <Menu
      data-testid="pipeline-select"
      onClick={(e) => {
        let pipeline = e.key.toString();
        if (pipeline === ALL_PIPELINES) {
          router.push("/");
        } else {
          router.push(`/?pipeline=${e.key.toString()}`);
        }
        setCurrentPipeline(e.key.toString());
        setFocusedNode(undefined);
      }}
    >
      <Menu.Item key={ALL_PIPELINES}>
        <i>{ALL_PIPELINES}</i>
      </Menu.Item>
      {pipelines?.pipelines.map((name: string) => (
        <Menu.Item data-testid="pipeline-option" key={name}>
          {name}
        </Menu.Item>
      ))}
    </Menu>
  );

  const menuRefresh = (
    <Menu
      data-testid="metrics-select"
      onClick={(e) => {
        setRefreshInterval(Number(e.key));
      }}
    >
      {Object.keys(refreshIntervals).map((key: any) => (
        <Menu.Item key={key}>{refreshIntervals[key]}</Menu.Item>
      ))}
    </Menu>
  );

  if (
    typeof window !== undefined
    && !isLoadingGraph
    && !isLoadingPipelines
    && !isUpdating
  ) {
    return (
      <div ref={ref} className="application">
        <Layout className="layout">
          <Header className="header" style={{ zIndex: 2 }}>
            <Menu theme="dark" mode="horizontal" selectable={false}>
              <Menu.Item key="1">
                Pipeline:&nbsp;
                <Dropdown overlay={menuPipeline} placement="bottomLeft" arrow>
                  <Button data-testid="pipeline-current">
                    {currentPipeline}
                  </Button>
                </Dropdown>
              </Menu.Item>
              <Menu.Item key="2">
                <Search
                  nodes={graph?.nodes}
                  focusedNode={focusedNode}
                  setFocusedNode={setFocusedNode}
                  setDetailNode={setDetailNode}
                />
              </Menu.Item>
              <Menu.Item
                key="3"
                style={{ float: "right", marginLeft: "auto" }}
                onClick={() => {
                  update({})
                    .then(() => router.reload())
                    .catch(() => message.error("Failed to update!"));
                }}
              >
                <Button type="dashed" ghost={true}>
                  Update Graphs
                </Button>
              </Menu.Item>
              <Menu.Item key="4" style={{ float: "right" }}>
                <Settings animate={animate} setAnimate={setAnimate} />
              </Menu.Item>
              <Menu.Item key="5" style={{ float: "right" }}>
                Metrics refresh:&nbsp;
                <Dropdown overlay={menuRefresh}>
                  <a href={"/#"} onClick={(e) => e.preventDefault()}>
                    {refreshIntervals[refreshInterval]} <DownOutlined />
                  </a>
                </Dropdown>
              </Menu.Item>
            </Menu>
            <Spin
              style={{
                position: "fixed",
                top: "1.5em",
                right: "1em",
              }}
              indicator={<LoadingOutlined spin />}
              spinning={isLoadingMetrics}
            />
          </Header>
          <Content
            style={{
              minHeight: "100vh",
              paddingTop: "64px",
              position: "relative",
            }}
          >
            <Row style={{ position: "fixed" }}>
              {graph
                ? (
                  <GraphVisualization
                    data-testid="graph"
                    data={graph}
                    metrics={metrics}
                    refetchMetrics={() => refetchMetrics()}
                    onClickNode={(node: Node) => setDetailNode(node)}
                    width={width ? width : window.innerWidth}
                    height={height ? height - 64 : window.innerHeight - 64}
                    focusedNode={focusedNode}
                    animate={animate}
                  />
                )
                : (
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
                top: height ? height - 147 : 400,
                position: "absolute",
              }}
            >
              <DetailsCard node={detailNode} />
            </Row>
          </Content>
        </Layout>
      </div>
    );
  }

  return (
    <div ref={ref} className="application">
      <div className="spinningContainer">
        <Spin
          data-testid="loading"
          tip={isUpdating ? "Updating Pipelines..." : "Loading..."}
        />
      </div>
    </div>
  );
};

export default App;
