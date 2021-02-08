import G6 from "@antv/g6";
import { graphConfig } from "../graphConfiguration";
import { updateNodeMetrics } from "./GraphVisualization";

describe("visualize node metrics", () => {
  it("should animate data processing edges", () => {
    document.body.innerHTML = '<div id="testGraph"></div>';
    graphConfig.container = "testGraph";
    const graph = new G6.Graph(graphConfig);

    graph.data({
      nodes: [
        { id: "streaming-app1", node_type: "streaming-app" },
        { id: "streaming-app2", node_type: "streaming-app" },
        { id: "streaming-app3", node_type: "streaming-app" },
        { id: "topic-in", node_type: "topic" },
        { id: "topic-out", node_type: "topic" },
      ],
      edges: [
        {
          id: "in-edge",
          source: "topic-in",
          target: "streaming-app1",
        },
        {
          id: "out-edge",
          source: "streaming-app1",
          target: "topic-out",
        },
        {
          id: "in-edge1",
          source: "topic-out",
          target: "streaming-app2",
        },
        {
          id: "in-edge2",
          source: "topic-out",
          target: "streaming-app3",
        },
      ],
    });

    graph.render();

    updateNodeMetrics(graph, [
      {
        node_id: "streaming-app1",
        messages_in: null,
        messages_out: null,
        consumer_lag: 1,
        consumer_read_rate: 1,
        topic_size: null,
        replicas: null,
      },
      {
        node_id: "topic-in",
        messages_in: null,
        messages_out: 1,
        consumer_lag: null,
        consumer_read_rate: null,
        topic_size: null,
        replicas: null,
      },
      {
        node_id: "topic-out",
        messages_in: 1,
        messages_out: 10,
        consumer_lag: null,
        consumer_read_rate: null,
        topic_size: 1,
        replicas: null,
      },
      {
        node_id: "streaming-app2",
        messages_in: null,
        messages_out: 1,
        consumer_lag: 1,
        consumer_read_rate: null,
        topic_size: null,
        replicas: null,
      },
      {
        node_id: "streaming-app3",
        messages_in: null,
        messages_out: null,
        consumer_lag: 1,
        consumer_read_rate: 1,
        topic_size: null,
        replicas: null,
      },
    ]);

    expect(graph.findById("in-edge").getModel().type).toEqual("line-dash");
    expect(graph.findById("out-edge").getModel().type).toEqual("line-dash");
    expect(graph.findById("in-edge1").getModel().type).toEqual(
      "cubic-horizontal"
    );
    expect(graph.findById("in-edge2").getModel().type).toEqual("line-dash");
  });
});
