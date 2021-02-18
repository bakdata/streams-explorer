import React, { useRef, useEffect, useCallback, useState } from "react";
import ReactDOM from "react-dom";
import G6 from "@antv/g6";
import { Graph as Data, Icon as IIcon, Metric } from "../api/fetchers";
import {
  GraphOptions,
  GraphData,
  NodeConfig,
  IG6GraphEvent,
} from "@antv/g6/lib/types";
import { IEdge, INode } from "@antv/g6/lib/interface/item";
import Graph from "@antv/g6/lib/graph/graph";
import "./MetricCustomNode";
import "./DashedEdge";
import { millify } from "millify";

interface GraphVisualizationProps {
  id: string;
  data: Data | GraphData;
  config: GraphOptions;
  metrics: Metric[] | null;
  refetchMetrics: Function;
  onClickNode: Function;
  width: number | undefined;
  height: number | undefined;
}

class Icon implements IIcon {
  img: string;
  show: boolean = true;
  width: number;
  height: number;

  constructor(img: string, width: number, height: number) {
    this.img = img;
    this.width = width;
    this.height = height;
  }
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

export function updateNodeMetrics(graph: Graph, metrics: Metric[]) {
  let readingNodes = new Set();
  let outgoingEdges: IEdge[] = [];
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
        typeof metric.replicas === "number" ? `REPLICAS ${metric.replicas}` : ""
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

      // update edge animation
      const nodeType = node.getModel().node_type;
      if (nodeType === "topic" || nodeType === "error-topic") {
        setEdgeActivity(graph, node.getInEdges(), !!metric.messages_in);
        node.getOutEdges().forEach((edge: IEdge) => {
          setEdgeActivity(graph, edge, !!metric.messages_out);
          if (metric.messages_out) {
            outgoingEdges.push(edge);
          }
        });
      } else if (metric.consumer_read_rate) {
        readingNodes.add(node.getID());
      }

      // do not animate edges on streaming apps with 0 replicas
      if (metric.replicas === 0) {
        setEdgeActivity(graph, node.getEdges(), false);
      }

      // animate edges on connector nodes if read rate or running tasks is not 0
      else if (nodeType === "connector") {
        const active: boolean = !(
          metric.consumer_read_rate === 0 || metric.connector_tasks === 0
        );
        setEdgeActivity(graph, node.getEdges(), active);
      }
    }
  });

  outgoingEdges.forEach((edge: IEdge) => {
    if (!readingNodes.has(edge.getTarget().getID())) {
      setEdgeActivity(graph, edge, false);
    }
  });
}

const GraphVisualization = ({
  id,
  data,
  config,
  metrics,
  refetchMetrics,
  onClickNode,
  width,
  height,
}: GraphVisualizationProps) => {
  const ref = useRef<HTMLDivElement>(null);

  const [graph, setGraph] = useState<Graph | null>(null);
  if (graph && width && height) {
    graph.changeSize(width, height);
  }

  if (graph && metrics) {
    updateNodeMetrics(graph, metrics);
  }

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

  const selectCallback = useCallback(
    (e: IG6GraphEvent) => {
      if (e.target && e.target.get("type") === "node") {
        let nodeId: string = e.target.get("id");
        onClickNode(nodeId);
      }
    },
    [onClickNode]
  );

  useEffect(() => {
    config.container = ReactDOM.findDOMNode(ref.current) as HTMLElement;
    let currentGraph: Graph | null = graph;
    if (!currentGraph && ref) {
      currentGraph = new G6.Graph(config);
    }
    let nodes = data["nodes"];
    const defaultIconConfig = config?.defaultNode?.icon as NodeConfig["icon"];

    nodes?.forEach((node: any) => {
      if (!node.icon) {
        let icon: Icon = new Icon(
          node.img || node.node_type + ".svg",
          defaultIconConfig?.width as number,
          defaultIconConfig?.height as number
        );
        node.icon = icon;
      }
    });

    currentGraph?.data(data as GraphData);
    currentGraph?.render();

    // register callbacks
    currentGraph?.on("node:mouseenter", mouseEnterCallback);
    currentGraph?.on("node:mouseleave", mouseLeaveCallback);
    currentGraph?.on("node:click", clickCallback);
    currentGraph?.on("nodeselectchange", selectCallback);

    setGraph(currentGraph);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [graph, setGraph, config, data]);

  return <div ref={ref}></div>;
};

export default GraphVisualization;
