import {
  fireEvent,
  render,
  wait,
  waitForElement,
  within,
} from "@testing-library/react";
import { createMemoryHistory } from "history";
import nock from "nock";
import React from "react";
import { Router } from "react-router";
import { useLocation } from "react-router-dom";
import { RestfulProvider } from "restful-react";
import App from "./App";

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

// -- Mock component to display url location & search paramters
const LocationDisplay = () => {
  const location = useLocation();
  return (
    <div>
      <div data-testid="location-pathname">{location.pathname}</div>
      <div data-testid="location-search">{location.search}</div>
    </div>
  );
};

function mockBackendGraph(persist?: boolean, pipelineName?: string) {
  return nock("http://localhost")
    .persist(persist)
    .get(`/api/graph${pipelineName ? "?pipeline_name=" + pipelineName : ""}`)
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
}

describe("handles url parameters", () => {
  // -- Mock backend endpoints
  const nockGraph = mockBackendGraph(true);
  const nockPipelineGraph = mockBackendGraph(true, "test-pipeline");

  nock("http://localhost")
    .persist()
    .get("/api/pipelines")
    .reply(200, {
      pipelines: ["test-pipeline"],
    });

  nock("http://localhost")
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

  const history = createMemoryHistory();

  it("should set pipeline from url parameter", async () => {
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

    await waitForElement(() => getByTestId("graph"));
    expect(asFragment()).toMatchSnapshot();

    const currentPipeline = getByTestId("pipeline-current");
    expect(
      within(currentPipeline).getByText("test-pipeline")
    ).toBeInTheDocument();
    expect(nockPipelineGraph.isDone()).toBeTruthy(); // specific graph endpoint was called
    expect(nockGraph.isDone()).toBeFalsy();

    const nodeSelect = getByTestId("node-select");
    const input = within(nodeSelect).getByRole("combobox") as HTMLInputElement;
    expect(input).toBeEmpty();
  });

  it("should set focus-node from url parameter", async () => {
    history.push({ pathname: "/", search: "?focus-node=test-app" });

    const nockAppNode = nock("http://localhost")
      .get("/api/node/test-app")
      .reply(200, {
        node_id: "test-app",
        node_type: "streaming-app",
        info: [],
      });

    const { getByTestId } = render(
      <RestfulProvider base="http://localhost">
        <Router history={history}>
          <LocationDisplay />
          <App />
        </Router>
      </RestfulProvider>
    );

    expect(getByTestId("location-pathname")).toHaveTextContent("/");
    expect(getByTestId("location-search")).toHaveTextContent(
      "?focus-node=test-app"
    );

    await waitForElement(() => getByTestId("graph"));

    wait(() => {
      const currentPipeline = getByTestId("pipeline-current");
      expect(
        within(currentPipeline).getByText("all pipelines")
      ).toBeInTheDocument();

      const nodeSelect = getByTestId("node-select");
      const input = within(nodeSelect).getByRole(
        "combobox"
      ) as HTMLInputElement;
      expect(input).toHaveValue("test-app");
      expect(nockAppNode.isDone()).toBeTruthy();
    });
  });

  it("should render without url parameters", async () => {
    history.push({ pathname: "/", search: "" });

    // render App
    const { getByTestId } = render(
      <RestfulProvider base="http://localhost">
        <Router history={history}>
          <LocationDisplay />
          <App />
        </Router>
      </RestfulProvider>
    );

    await waitForElement(() => getByTestId("graph"));

    wait(() => {
      // check pipeline set to all
      const currentPipeline = getByTestId("pipeline-current");
      expect(
        within(currentPipeline).getByText("all pipelines")
      ).toBeInTheDocument();

      // check focus-node empty
      const nodeSelect = getByTestId("node-select");
      const input = within(nodeSelect).getByRole(
        "combobox"
      ) as HTMLInputElement;
      expect(input).toBeEmpty();
    });
  });

  it("should update focus-node & pipeline parameters", async () => {
    history.push({ pathname: "/", search: "?pipeline=test-pipeline" });

    // render App
    const { getByTestId, getAllByTestId, getByText } = render(
      <RestfulProvider base="http://localhost">
        <Router history={history}>
          <LocationDisplay />
          <App />
        </Router>
      </RestfulProvider>
    );

    await waitForElement(() => getByTestId("graph"));
    const nodeSelect = getByTestId("node-select");
    const input = within(nodeSelect).getByRole("combobox") as HTMLInputElement;
    expect(input).toBeEmpty();

    const nockAppNode = nock("http://localhost")
      .get("/api/node/test-app")
      .reply(200, {
        node_id: "test-app",
        node_type: "streaming-app",
        info: [],
      });

    const nockTopicNode = nock("http://localhost")
      .get("/api/node/test-topic")
      .reply(200, {
        node_id: "test-topic",
        node_type: "topic",
        info: [],
      });
    expect(nockAppNode.isDone()).toBeFalsy();
    expect(nockTopicNode.isDone()).toBeFalsy();

    // -- set focus-node through UI
    fireEvent.change(input, { target: { value: "test-app" } });
    wait(() => {
      expect(input).toHaveValue("test-app");
      let options = getAllByTestId("node-option");
      expect(options).toHaveLength(1);
      fireEvent.click(options[0]);

      // -- check result: pipeline should be present
      expect(getByTestId("location-search")).toHaveTextContent(
        "?pipeline=test-pipeline&focus-node=test-app"
      );
      expect(nockAppNode.isDone()).toBeTruthy();
    });

    // -- update focus-node through UI
    fireEvent.change(input, { target: { value: "test-topic" } });
    wait(() => {
      expect(input).toHaveValue("test-topic");
      let options = getAllByTestId("node-option");
      expect(options).toHaveLength(2);
      fireEvent.click(options[0]);

      // -- check focus-node updated, pipeline still present
      expect(getByTestId("location-search")).toHaveTextContent(
        "?pipeline=test-pipeline&focus-node=test-topic"
      );
      expect(nockTopicNode.isDone()).toBeTruthy();
    });

    // -- (re-)set pipeline through UI
    fireEvent.mouseOver(getByTestId("pipeline-current"));
    wait(() => {
      expect(getByTestId("pipeline-select")).toBeInTheDocument();
      const pipeline = getByText("all pipelines");
      expect(pipeline).toBeInTheDocument();
      fireEvent.click(pipeline);
      expect(getByTestId("location-search")).toHaveTextContent(
        "?pipeline=all pipelines"
      );
    });
  });
});

export {};
