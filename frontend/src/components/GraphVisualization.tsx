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
import INode from "@antv/g6/lib/interface/item";
import Graph from "@antv/g6/lib/graph/graph";
import "./MetricCustomNode";
import { millify } from "millify";

interface GraphVisualizationProps {
  id: string;
  data: Data | GraphData;
  config: GraphOptions;
  metrics: Metric[] | null;
  refetchMetrics: Function;
  onClickNode: Function;
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

function updateNodeMetrics(graph: Graph, metrics: Metric[]) {
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
    let node = graph.findById(metric.node_id);
    if (node) {
      graph.updateItem(node, {
        metric: metricsString,
      });
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
}: GraphVisualizationProps) => {
  const ref = useRef<HTMLDivElement>(null);

  const [graph, setGraph] = useState<Graph | null>(null);

  if (graph && metrics) {
    updateNodeMetrics(graph, metrics);
  }

  const mouseEnterCallback = useCallback(
    (e: IG6GraphEvent) => {
      const node = e.item as INode.INode;
      graph?.setItemState(node, "hover", true);
    },
    [graph]
  );

  const mouseLeaveCallback = useCallback(
    (e: IG6GraphEvent) => {
      const node = e.item as INode.INode;
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
      const node = e.item as INode.INode;
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
