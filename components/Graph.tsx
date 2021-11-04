import G6 from "@antv/g6";
import React, { useEffect, useRef } from "react";
import ReactDOM from "react-dom";

const Graph = () => {
  const ref = useRef(null);
  let graph = null;

  useEffect(() => {
    if (!graph) {
      let data = {
        nodes: [
          {
            id: "node1",
            x: 100,
            y: 100,
          },
          {
            id: "node2",
            x: 200,
            y: 100,
          },
        ],
        edges: [
          {
            source: "node1",
            target: "node2",
          },
        ],
      };

      graph = new G6.Graph({
        container: ReactDOM.findDOMNode(ref.current),
        width: "100%",
        height: "100%",
        renderer: "svg",
        modes: {
          default: ["zoom-canvas", "drag-node", "drag-canvas"],
        },
        minZoom: 0.5,
        maxZoom: 3,
      });
      graph.data(data);
      graph.render();
    }
  }, []);
  return (
    <div
      ref={ref}
      style={{ width: 1000, height: 1000, border: "1px solid #ccc" }}
    >
    </div>
  );
};

export default Graph;
