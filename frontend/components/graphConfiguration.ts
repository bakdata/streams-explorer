import { GraphOptions } from "@antv/g6";

export const graphConfig: GraphOptions = {
  container: "",
  width: 0,
  height: 0,
  minZoom: 0.2,
  maxZoom: 3,
  modes: {
    default: ["drag-canvas", "zoom-canvas", "click-select"],
  },
  defaultNode: {
    type: "GenericNode",
  },
  defaultEdge: {
    type: "cubic-horizontal",
    style: {
      stroke: "#000",
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
      fillOpacity: 1,
    },
    click: {
      fill: "#fff",
      lineWidth: 2.5,
      fillOpacity: 1,
    },
  },
};
