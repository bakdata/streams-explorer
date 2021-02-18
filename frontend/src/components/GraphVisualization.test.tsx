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
        { id: "topic-out1", node_type: "topic" },
        { id: "topic-out2", node_type: "topic" },
        { id: "topic-out3", node_type: "topic" },
        { id: "source-connector1", node_type: "connector" },
        { id: "sink-connector2", node_type: "connector" },
        { id: "sink-connector3", node_type: "connector" },
        { id: "source1", node_type: "sink/source" },
        { id: "sink2", node_type: "sink/source" },
      ],
      edges: [
        {
          id: "out-edge-source1",
          source: "source1",
          target: "source-connector1",
        },
        {
          id: "out-edge-source-connector1",
          source: "source-connector1",
          target: "topic-in",
        },
        {
          id: "in-edge1",
          source: "topic-in",
          target: "streaming-app1",
        },
        {
          id: "out-edge1",
          source: "streaming-app1",
          target: "topic-out1",
        },
        {
          id: "in-edge2",
          source: "topic-out1",
          target: "streaming-app2",
        },
        {
          id: "out-edge2",
          source: "streaming-app2",
          target: "topic-out2",
        },
        {
          id: "in-edge-sink-connector2",
          source: "topic-out2",
          target: "sink-connector2",
        },
        {
          id: "in-edge-sink2",
          source: "sink-connector2",
          target: "sink2",
        },
        {
          id: "in-edge3",
          source: "topic-out1",
          target: "streaming-app3",
        },
        {
          id: "out-edge3",
          source: "streaming-app3",
          target: "topic-out3",
        },
        {
          id: "in-edge-sink-connector3",
          source: "topic-out3",
          target: "sink-connector3",
        },
      ],
    });

    graph.render();

    updateNodeMetrics(graph, [
      {
        node_id: "source-connector1",
        messages_in: undefined,
        messages_out: undefined,
        consumer_lag: 1,
        consumer_read_rate: 1,
        topic_size: undefined,
        replicas: undefined,
        connector_tasks: 1,
      },
      {
        node_id: "topic-in",
        messages_in: 1,
        messages_out: 1,
        consumer_lag: undefined,
        consumer_read_rate: undefined,
        topic_size: undefined,
        replicas: undefined,
        connector_tasks: undefined,
      },
      {
        node_id: "streaming-app1",
        messages_in: undefined,
        messages_out: undefined,
        consumer_lag: 1,
        consumer_read_rate: 1,
        topic_size: undefined,
        replicas: undefined,
        connector_tasks: undefined,
      },
      {
        node_id: "topic-out1",
        messages_in: 1,
        messages_out: 10,
        consumer_lag: undefined,
        consumer_read_rate: undefined,
        topic_size: 1,
        replicas: undefined,
        connector_tasks: undefined,
      },
      {
        node_id: "streaming-app2",
        messages_in: undefined,
        messages_out: undefined,
        consumer_lag: 1,
        consumer_read_rate: undefined,
        topic_size: undefined,
        replicas: undefined,
        connector_tasks: undefined,
      },
      {
        node_id: "topic-out2",
        messages_in: 0,
        messages_out: 0,
        consumer_lag: undefined,
        consumer_read_rate: undefined,
        topic_size: 1,
        replicas: undefined,
        connector_tasks: undefined,
      },
      {
        node_id: "streaming-app3",
        messages_in: undefined,
        messages_out: undefined,
        consumer_lag: 1,
        consumer_read_rate: 0,
        topic_size: undefined,
        replicas: undefined,
        connector_tasks: undefined,
      },
      {
        node_id: "topic-out3",
        messages_in: 1,
        messages_out: 1,
        consumer_lag: undefined,
        consumer_read_rate: undefined,
        topic_size: 1,
        replicas: undefined,
        connector_tasks: undefined,
      },
      {
        node_id: "sink-connector2",
        messages_in: undefined,
        messages_out: undefined,
        consumer_lag: 1,
        consumer_read_rate: undefined,
        topic_size: undefined,
        replicas: undefined,
        connector_tasks: 0,
      },
      {
        node_id: "sink-connector3",
        messages_in: undefined,
        messages_out: undefined,
        consumer_lag: 1,
        consumer_read_rate: 1,
        topic_size: undefined,
        replicas: undefined,
        connector_tasks: 1,
      },
    ]);

    expect(graph.findById("out-edge-source1").getModel().type).toEqual(
      "line-dash"
    );
    expect(
      graph.findById("out-edge-source-connector1").getModel().type
    ).toEqual("line-dash");
    expect(graph.findById("in-edge1").getModel().type).toEqual("line-dash");
    expect(graph.findById("out-edge1").getModel().type).toEqual("line-dash");
    expect(graph.findById("in-edge2").getModel().type).toEqual("line-dash");
    expect(graph.findById("out-edge2").getModel().type).toEqual(
      "cubic-horizontal"
    );
    expect(graph.findById("in-edge3").getModel().type).toEqual(
      "cubic-horizontal"
    );
    expect(graph.findById("out-edge3").getModel().type).toEqual("line-dash");
    expect(graph.findById("in-edge-sink-connector2").getModel().type).toEqual(
      "cubic-horizontal"
    );
    expect(graph.findById("in-edge-sink2").getModel().type).toEqual(
      "cubic-horizontal"
    );
    expect(graph.findById("in-edge-sink-connector3").getModel().type).toEqual(
      "line-dash"
    );
  });
});
