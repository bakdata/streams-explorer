import nock from "nock";
import { createMemoryHistory } from "history";
import React from "react";
import { RestfulProvider } from "restful-react";
import App from "./App";
import { Router } from "react-router";
import {
  waitForElement,
  render,
  within,
  wait,
  fireEvent,
} from "@testing-library/react";
import { useLocation } from "react-router-dom";

beforeAll(() => {
  Object.defineProperty(window, "matchMedia", {
    writable: true,
    value: jest.fn().mockImplementation((query) => ({
      matches: false,
      media: query,
      onchange: null,
      addListener: jest.fn(), // Deprecated
      removeListener: jest.fn(), // Deprecated
      addEventListener: jest.fn(),
      removeEventListener: jest.fn(),
      dispatchEvent: jest.fn(),
    })),
  });

  // disable resize observer
  (window as any).ResizeObserver = class MockResizeObserver {
    observe() {}
    unobserve() {}
    disconnect() {}
  };
});

// -- Mock GraphVisualization
jest.mock("./components/GraphVisualization", () => {
  return function DummyGraphVisualization() {
    return <div data-testid="graph"></div>;
  };
});

const LocationDisplay = () => {
  const location = useLocation();
  return (
    <div>
      <div data-testid="location-pathname">{location.pathname}</div>
      <div data-testid="location-search">{location.search}</div>
    </div>
  );
};

describe("url parameters", () => {
  it("should update focus-node param", async () => {
    jest.setTimeout(30000);

    // -- Mock backend endpoints
    const nockGraph = nock("http://localhost")
      .persist()
      .get("/api/graph")
      .reply(200, {
        directed: true,
        multigraph: false,
        graph: {},
        nodes: [
          {
            id: "test-app",
            label: "test-app",
            node_type: "streaming-app",
            icon: null,
            x: 0,
            y: 0,
          },
          {
            id: "test-topic",
            label: "test-topic",
            node_type: "topic",
            icon: null,
            x: 10,
            y: 0,
          },
        ],
        edges: [
          {
            source: "test-app",
            target: "test-topic",
          },
        ],
      });

    const nockPipelineGraph = nock("http://localhost")
      .persist()
      .get("/api/graph?pipeline_name=test-pipeline")
      .reply(200, {
        directed: true,
        multigraph: false,
        graph: {},
        nodes: [
          {
            id: "test-app",
            label: "test-app",
            node_type: "streaming-app",
            icon: null,
            x: 0,
            y: 0,
          },
          {
            id: "test-topic",
            label: "test-topic",
            node_type: "topic",
            icon: null,
            x: 10,
            y: 0,
          },
        ],
        edges: [
          {
            source: "test-app",
            target: "test-topic",
          },
        ],
      });

    const nockPipelines = nock("http://localhost")
      .persist()
      .get("/api/pipelines")
      .reply(200, {
        pipelines: ["test-pipeline"],
      });

    const nockMetrics = nock("http://localhost")
      .persist()
      .get("/api/metrics")
      .reply(200, [
        {
          node_id: "test-app",
          messages_in: null,
          messages_out: null,
          consumer_lag: null,
          consumer_read_rate: null,
          topic_size: null,
          replicas: null,
          connector_tasks: null,
        },
        {
          node_id: "test-topic",
          messages_in: null,
          messages_out: null,
          consumer_lag: null,
          consumer_read_rate: null,
          topic_size: null,
          replicas: null,
          connector_tasks: null,
        },
      ]);

    const nockNode = nock("http://localhost")
      .get("/api/node/test-app")
      .reply(200, {
        node_id: "test-app",
        node_type: "streaming-app",
        info: [],
      });

    const history = createMemoryHistory();
    history.push({ pathname: "/", search: "?pipeline=test-pipeline" });

    const { getByTestId, asFragment } = render(
      <RestfulProvider base="http://localhost">
        <Router history={history}>
          <LocationDisplay />
          <App />
        </Router>
      </RestfulProvider>
    );
    expect(getByTestId("location-pathname")).toHaveTextContent("/");
    expect(getByTestId("location-search")).toHaveTextContent(
      "?pipeline=test-pipeline"
    );

    await waitForElement(() => getByTestId("loading"));
    expect(asFragment()).toMatchSnapshot();

    await waitForElement(() => getByTestId("graph"));
    expect(asFragment()).toMatchSnapshot();

    const currentPipeline = getByTestId("pipeline-current");
    expect(
      within(currentPipeline).getByText("test-pipeline")
    ).toBeInTheDocument();
    expect(nockPipelineGraph.isDone()).toBeTruthy(); // specific graph endpoint was called
    expect(nockGraph.isDone()).toBeFalsy();

    // const pipelineOptions = within(pipelineSelect).getAllByTestId(
    //   "pipeline-option"
    // );
    // expect(pipelineOptions).toHaveLength(1);

    const nodeSelect = getByTestId("node-select");
    const input = within(nodeSelect).getByRole("combobox") as HTMLInputElement;
    expect(input).toHaveValue("");

    // -- set focus-node through UI
    await wait(() => {
      expect(nockNode.isDone()).toBeFalsy();
      fireEvent.change(input, { target: { value: "test-app" } });
      fireEvent.submit(input);
      expect(input).toHaveValue("test-app");
      // let options = getAllByTestId("node-option");
      // expect(options).toHaveLength(2);

      // -- check result
      expect(getByTestId("location-search")).toHaveTextContent(
        "?pipeline=test-pipeline&focus-node=test-app"
      );
      expect(nockNode.isDone()).toBeTruthy();
    });
  });

  it("should update pipeline param", async () => {
    // -- set pipeline through URL
    // window.location.search = "?pipeline=test-pipeline";
    // expect(window.location.search).toEqual("?pipeline=test-pipeline");
    // -- set focus-node through URL
    // history.push("/static?focus-node=test-app");
    // window.location.search = "?focus-node=test-app";
    // expect(window.location.search).toEqual("?focus-node=test-app");
  });
});

// -- first approach
// add focus-node
// instance is null on stateless functional components (React 16+)
// wrapper.instance().pushHistoryFocusNode("test-node-id");

// -- pipeline kept
// expect(window.location.search).toEqual(
//   "?pipeline=test-pipeline&focus-node=test-node-id"
// );

export {};
