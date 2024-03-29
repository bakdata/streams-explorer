import G6, { Graph, GraphData, IEdge, IG6GraphEvent, INode } from "@antv/g6";
import { message } from "antd";
import { millify } from "millify";
import React, {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";
import { Graph as Data, Metric } from "../api/fetchers";
import { graphConfig as config } from "./config";
import Node from "./Node";
import "./GenericNode";
import "./TopicNode";
import "./AppNode";
import "./DashedEdge";

export const isBrowser = typeof window !== "undefined"; // disable SSR

interface GraphVisualizationProps {
  data: Data | GraphData;
  metrics: Metric[] | null;
  refetchMetrics: Function;
  onClickNode: Function;
  width: number;
  height: number;
  focusedNode: Node | undefined;
  animate: boolean;
}

interface AppState {
  id: string;
  state: string;
  replicas: number[];
}

function createNodeFromGraphNode(graphNode: INode): Node {
  return {
    id: graphNode.getID(),
    label: graphNode.getModel().label as string,
  };
}

function formatNumber(num: number): string {
  return num < 1e6 ? num.toLocaleString("en") : millify(num);
}

function setEdgeActivity(
  graph: Graph,
  edges: IEdge | IEdge[],
  active: boolean
): void {
  edges = edges instanceof Array ? edges : [edges];
  edges.forEach((edge: IEdge) => {
    graph.updateItem(edge, {
      type: active ? "line-dash" : "cubic-horizontal",
    });
  });
}

export function updateNodeMetrics(
  graph: Graph,
  metrics: Metric[],
  animate: boolean
) {
  let unavailableStreamingApps: INode[] = [];
  metrics.forEach((metric) => {
    let metricsString: string = [
      `${
        typeof metric.topic_size === "number"
          ? `SIZE ${formatNumber(metric.topic_size)}`
          : ""
      }`,
      `${
        typeof metric.messages_in === "number"
          ? `IN ${formatNumber(metric.messages_in)}/s`
          : ""
      }`,
      `${
        typeof metric.messages_out === "number"
          ? `OUT ${formatNumber(metric.messages_out)}/s`
          : ""
      }`,
      `${
        typeof metric.replicas === "number"
          ? `REPLICAS ${
            typeof metric.replicas_available === "number"
              ? `${metric.replicas_available}/`
              : ""
          }${metric.replicas}`
          : ""
      }`,
      `${
        typeof metric.connector_tasks === "number"
          ? `TASKS ${metric.connector_tasks}`
          : ""
      }`,
      `${
        typeof metric.consumer_lag === "number"
          ? `LAG ${formatNumber(metric.consumer_lag)}`
          : ""
      }`,
      `${
        typeof metric.consumer_read_rate === "number"
          ? `READ ${formatNumber(metric.consumer_read_rate)}/s`
          : ""
      }`,
    ]
      .filter(Boolean)
      .join("  ");

    let node = graph.findById(metric.node_id) as INode;
    if (node) {
      graph.updateItem(node, {
        metric: metricsString,
      });

      if (animate) {
        // update edge animation
        const nodeType = node.getModel().node_type;
        if (nodeType === "topic" || nodeType === "error-topic") {
          setEdgeActivity(graph, node.getInEdges(), !!metric.messages_in);
          node.getOutEdges().forEach((edge: IEdge) => {
            setEdgeActivity(graph, edge, !!metric.messages_out);
          });
        } else if (metric.replicas === 0) {
          unavailableStreamingApps.push(node);
        } else if (
          nodeType === "streaming-app"
          && metric.consumer_read_rate === 0
        ) {
          // do not animate incoming edges on streaming apps with read rate 0
          setEdgeActivity(graph, node.getInEdges(), false);
        } else if (nodeType === "connector") {
          // animate edges on connector nodes if read rate and running tasks is not 0
          const active: boolean = !(
            !metric.consumer_read_rate || metric.connector_tasks === 0
          );
          setEdgeActivity(graph, node.getEdges(), active);
        }
      }
    }
  });

  // do not animate edges on streaming apps with 0 replicas
  unavailableStreamingApps.forEach((node: INode) => {
    setEdgeActivity(graph, node.getEdges(), false);
  });
}

const nodeError = (node: Node) => {
  message.error(`Node "${node.id}" doesn't exist`, 5);
};

function setFocusedNode(graph: Graph, focusedNode: Node) {
  const node = graph.findById(focusedNode.id) as INode;
  if (!node) {
    return nodeError(focusedNode);
  }

  if (graph.getZoom() < 1) {
    graph.zoomTo(1);
  }

  graph.focusItem(node, true, {
    easing: "easeCubic",
    duration: 1500,
  });
}

const GraphVisualization = ({
  data,
  metrics,
  onClickNode,
  width,
  height,
  focusedNode,
  animate,
}: GraphVisualizationProps) => {
  const ws = useMemo(() => {
    if (isBrowser) {
      const hostname = window.location.hostname;
      const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
      const port = process.env.NODE_ENV === "development"
          || process.env.NODE_ENV === "test"
        ? "8000"
        : window.location.port;
      const url = `${protocol}//${hostname}:${port}/api/graph/ws`;
      return new WebSocket(url);
    }
  }, []);
  const ref = useRef<HTMLDivElement>(null);

  const [graph, setGraph] = useState<Graph>();
  if (graph) {
    graph.changeSize(width, height);
  }

  useEffect(() => {
    if (graph && focusedNode) {
      setFocusedNode(graph, focusedNode);
    }
  }, [graph, focusedNode]);

  useEffect(() => {
    if (graph && !animate) {
      // disable all edge animations
      graph.getEdges().forEach((edge) => setEdgeActivity(graph, edge, false));
    }
  }, [animate]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    if (graph && metrics) {
      updateNodeMetrics(graph, metrics, animate);
    }
  }, [graph, metrics, animate]);

  const mouseEnterCallback = useCallback(
    (e: IG6GraphEvent) => {
      const node = e.item as INode;
      graph?.setItemState(node, "hover", true);
    },
    [graph]
  );

  const mouseLeaveCallback = useCallback(
    (e: IG6GraphEvent) => {
      const node = e.item as INode;
      graph?.setItemState(node, "hover", false);
    },
    [graph]
  );

  const clickCallback = useCallback(
    (e: IG6GraphEvent) => {
      const clickNodes = graph?.findAllByState("node", "click");
      clickNodes?.forEach((cn) => {
        graph?.setItemState(cn, "click", false);
      });
      const node = e.item as INode;
      graph?.setItemState(node, "click", true);
    },
    [graph]
  );

  const touchCallback = useCallback(
    (e: IG6GraphEvent) => {
      const node = createNodeFromGraphNode(e.item as INode);
      onClickNode(node);
    },
    [onClickNode]
  );

  const selectCallback = useCallback(
    (e: IG6GraphEvent) => {
      if (e.target && e.target.get("type") === "node") {
        let nodeId: string = e.target.get("id");
        const graphNode = graph?.findById(nodeId);
        if (graphNode) {
          const node = createNodeFromGraphNode(graphNode as INode);
          onClickNode(node);
        }
      }
    },
    [graph, onClickNode]
  );

  // register callbacks
  graph?.on("node:mouseenter", mouseEnterCallback);
  graph?.on("node:mouseleave", mouseLeaveCallback);
  graph?.on("node:click", clickCallback);
  graph?.on("node:touchstart", touchCallback);
  graph?.on("nodeselectchange", selectCallback);

  if (ws && graph) {
    ws.onmessage = function(event) {
      try {
        const data = JSON.parse(event.data) as AppState;
        const node = graph.findById(data.id) as INode;
        if (node) {
          if (data.state === "Failed" || data.state === "BackOff") {
            graph.updateItem(node, {
              style: {
                stroke: "#ff2825",
                fill: "#ff2825",
              },
              stateIcon: {
                img: "state-error.svg",
              },
            });
          } else if (!data.replicas[0]) {
            graph.updateItem(node, {
              style: {
                stroke: "#9f9f9f",
                fill: "#000",
              },
              stateIcon: {
                img: "state-paused.svg",
              },
            });
          } else {
            graph.updateItem(node, {
              style: {
                stroke: "#52c41a",
                fill: "#52c41a",
              },
              stateIcon: {
                img: "state-running.svg",
              },
            });
          }
        }
      } catch (error) {}
    };
  }

  useEffect(() => {
    if (graph) graph.destroy();
    config.container = ref.current as HTMLDivElement;
    const currentGraph = new G6.Graph(config);
    let nodes = data["nodes"];

    nodes?.forEach((node: any) => {
      switch (node.node_type) {
        case "topic":
        case "error-topic":
          node.type = "TopicNode";
          break;

        case "streaming-app":
          node.type = "AppNode";
          break;
      }
    });

    currentGraph.data(data as GraphData);
    currentGraph.render();

    setGraph(currentGraph);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [data]);

  return <div ref={ref}></div>;
};

export default GraphVisualization;
