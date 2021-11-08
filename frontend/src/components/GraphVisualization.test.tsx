import G6 from "@antv/g6";
import { graphConfig } from "../graphConfiguration";
import { updateNodeMetrics } from "./GraphVisualization";

describe("visualize node metrics", () => {
  it("should differentiate node id and label", () => {
    document.body.innerHTML = '<div id="testGraph"></div>';
    graphConfig.container = "testGraph";
    const graph = new G6.Graph(graphConfig);

    graph.data({
      nodes: [
        { id: "streaming-app1", label: "app1", node_type: "streaming-app" },
      ],
      edges: [],
    });

    graph.render();

    expect(graph.findById("streaming-app1").getID()).toEqual("streaming-app1");
    expect(graph.findById("streaming-app1").getModel().label).toEqual("app1");
  });

  it("should update node metric labels", () => {
    document.body.innerHTML = '<div id="testGraph"></div>';
    graphConfig.container = "testGraph";
    const graph = new G6.Graph(graphConfig);

    graph.data({
      nodes: [
        { id: "streaming-app", node_type: "streaming-app" },
        { id: "topic", node_type: "topic" },
        { id: "connector", node_type: "connector" },
        { id: "sink", node_type: "sink/source" },
      ],
      edges: [],
    });

    graph.render();

    updateNodeMetrics(
      graph,
      [
        {
          node_id: "topic",
          messages_in: 1,
          messages_out: 1,
          consumer_lag: undefined,
          consumer_read_rate: undefined,
          topic_size: undefined,
          replicas: undefined,
          replicas_available: undefined,
          connector_tasks: undefined,
        },
        {
          node_id: "streaming-app",
          messages_in: undefined,
          messages_out: undefined,
          consumer_lag: 1,
          consumer_read_rate: undefined,
          topic_size: undefined,
          replicas: 1,
          replicas_available: undefined,
          connector_tasks: undefined,
        },
        {
          node_id: "connector",
          messages_in: undefined,
          messages_out: undefined,
          consumer_lag: 1,
          consumer_read_rate: 1,
          topic_size: undefined,
          replicas: undefined,
          replicas_available: undefined,
          connector_tasks: 1,
        },
      ],
      true
    );

    expect(graph.findById("streaming-app").getModel().metric).toEqual(
      "REPLICAS 1  LAG 1"
    );
    expect(graph.findById("topic").getModel().metric).toEqual(
      "IN 1/s  OUT 1/s"
    );
    expect(graph.findById("connector").getModel().metric).toEqual(
      "TASKS 1  LAG 1  READ 1/s"
    );
    expect(graph.findById("sink").getModel().metric).toBeUndefined();

    updateNodeMetrics(
      graph,
      [
        {
          node_id: "topic",
          messages_in: 80_000,
          messages_out: 10,
          consumer_lag: undefined,
          consumer_read_rate: undefined,
          topic_size: 1_100_000_000,
          replicas: undefined,
          replicas_available: undefined,
          connector_tasks: undefined,
        },
        {
          node_id: "streaming-app",
          messages_in: undefined,
          messages_out: undefined,
          consumer_lag: 0,
          consumer_read_rate: undefined,
          topic_size: undefined,
          replicas: 2,
          replicas_available: 1,
          connector_tasks: undefined,
        },
      ],
      true
    );

    expect(graph.findById("streaming-app").getModel().metric).toEqual(
      "REPLICAS 1/2  LAG 0"
    );
    expect(graph.findById("topic").getModel().metric).toEqual(
      "SIZE 1.1B  IN 80,000/s  OUT 10/s"
    );
    // unchanged
    expect(graph.findById("connector").getModel().metric).toEqual(
      "TASKS 1  LAG 1  READ 1/s"
    );
    expect(graph.findById("sink").getModel().metric).toBeUndefined();
  });

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
        { id: "sink-topic4", node_type: "topic" },
        { id: "sink-connector4", node_type: "connector" },
        { id: "sink4", node_type: "sink/source" },
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
        {
          id: "in-edge-sink-connector4",
          source: "sink-topic4",
          target: "sink-connector4",
        },
        {
          id: "in-edge-sink4",
          source: "sink-connector4",
          target: "sink4",
        },
      ],
    });

    graph.render();

    updateNodeMetrics(
      graph,
      [
        {
          node_id: "topic-in",
          messages_in: 1,
          messages_out: 1,
          consumer_lag: undefined,
          consumer_read_rate: undefined,
          topic_size: undefined,
          replicas: undefined,
          replicas_available: undefined,
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
          replicas_available: undefined,
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
          replicas_available: undefined,
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
          replicas_available: undefined,
          connector_tasks: undefined,
        },
        {
          node_id: "sink-topic4",
          messages_in: 0,
          messages_out: undefined,
          consumer_lag: undefined,
          consumer_read_rate: undefined,
          topic_size: 0,
          replicas: undefined,
          replicas_available: undefined,
          connector_tasks: undefined,
        },
        {
          node_id: "source-connector1",
          messages_in: undefined,
          messages_out: undefined,
          consumer_lag: 1,
          consumer_read_rate: 1,
          topic_size: undefined,
          replicas: undefined,
          replicas_available: undefined,
          connector_tasks: 1,
        },
        {
          node_id: "streaming-app1",
          messages_in: undefined,
          messages_out: undefined,
          consumer_lag: 1,
          consumer_read_rate: undefined,
          topic_size: undefined,
          replicas: undefined,
          replicas_available: undefined,
          connector_tasks: undefined,
        },
        {
          node_id: "streaming-app2",
          messages_in: undefined,
          messages_out: undefined,
          consumer_lag: 1,
          consumer_read_rate: 1,
          topic_size: undefined,
          replicas: 0,
          replicas_available: undefined,
          connector_tasks: undefined,
        },
        {
          node_id: "streaming-app3",
          messages_in: undefined,
          messages_out: undefined,
          consumer_lag: 1,
          consumer_read_rate: 0,
          topic_size: undefined,
          replicas: 1,
          replicas_available: 1,
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
          replicas_available: undefined,
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
          replicas_available: undefined,
          connector_tasks: 1,
        },
        {
          node_id: "sink-connector4",
          messages_in: undefined,
          messages_out: undefined,
          consumer_lag: 0,
          consumer_read_rate: undefined,
          topic_size: undefined,
          replicas: undefined,
          replicas_available: undefined,
          connector_tasks: 1,
        },
      ],
      true
    );

    expect(graph.findById("out-edge-source1").getModel().type).toEqual(
      "line-dash"
    );
    expect(
      graph.findById("out-edge-source-connector1").getModel().type
    ).toEqual("line-dash");
    expect(graph.findById("in-edge1").getModel().type).toEqual("line-dash");
    expect(graph.findById("out-edge1").getModel().type).toEqual("line-dash");
    expect(graph.findById("in-edge2").getModel().type).toEqual(
      "cubic-horizontal"
    );
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
    expect(graph.findById("in-edge-sink-connector4").getModel().type).toEqual(
      "cubic-horizontal"
    );
    expect(graph.findById("in-edge-sink4").getModel().type).toEqual(
      "cubic-horizontal"
    );
  });
});
