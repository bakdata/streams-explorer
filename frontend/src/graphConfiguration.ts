import { GraphOptions } from "@antv/g6/lib/types";

export const graphConfig: GraphOptions = {
  container: "",
  width: 0,
  height: 0,
  modes: {
    default: ["drag-canvas", "zoom-canvas", "click-select"],
  },
  defaultNode: {
    type: "MetricCustomNode",
    size: [28, 28],
    style: {
      fill: "#F0F2F5",
      lineWidth: 0,
    },
    labelCfg: {
      style: {
        fill: "#000000",
        fontSize: 14,
      },
      position: "bottom",
    },
    icon: {
      show: true,
      width: 36,
      height: 36,
    },
  },
  defaultEdge: {
    type: "cubic-horizontal",
    style: {
      stroke: "#000000",
      endArrow: true,
    },
    labelCfg: {
      autoRotate: true,
      refY: 6,
    },
  },
  nodeStateStyles: {
    // highlight Nodes on hover and when selected
    hover: {
      fill: "lightsteelblue",
    },
    click: {
      fill: "#FFF",
    },
  },
};
