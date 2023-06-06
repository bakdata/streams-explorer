import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import {
  act,
  fireEvent,
  render,
  waitFor,
  within,
} from "@testing-library/react";
import mockRouter from "next-router-mock";
import singletonRouter from "next/router";
import nock from "nock";
import React from "react";
import AppComponent from "../components/App";

jest.mock("next/router", () => require("next-router-mock"));

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <AppComponent />
  </QueryClientProvider>
);

// -- Mock GraphVisualization
jest.mock("../components/graph/Visualization", () => {
  return function StubGraphVisualization() {
    return <div data-testid="graph"></div>;
  };
});

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
          label: "test-app-name",
          node_type: "streaming-app",
          icon: null,
          x: 0,
          y: 0,
        },
        {
          id: "test-topic",
          label: "test-topic-name",
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

describe("Streams Explorer", () => {
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

  describe("renders", () => {
    mockBackendGraph(true);
    it("without crashing", async () => {
      const { findByTestId } = render(<App />);
      await findByTestId("graph");
    });
  });

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

    it("should set pipeline from url parameter", async () => {
      mockRouter.setCurrentUrl("/?pipeline=test-pipeline");

      const { getByTestId, findByTestId, asFragment } = render(<App />);

      expect(singletonRouter).toMatchObject({
        asPath: "/?pipeline=test-pipeline",
      });

      await findByTestId("graph");

      expect(asFragment()).toMatchSnapshot();

      const currentPipeline = getByTestId("pipeline-current");
      expect(currentPipeline).toHaveTextContent("test-pipeline");
      expect(nockGraph.isDone()).toBeFalsy();
      expect(nockPipelineGraph.isDone()).toBeTruthy(); // specific graph endpoint was called

      const nodeSelect = getByTestId("node-select");
      const input = within(nodeSelect).getByRole(
        "combobox"
      ) as HTMLInputElement;
      expect(input).toBeEmptyDOMElement();
    });

    it("should set focus-node from url parameter", async () => {
      mockRouter.setCurrentUrl("/?focus-node=test-app");

      const nockAppNode = nock("http://localhost")
        .get("/api/node/test-app")
        .reply(200, {
          node_id: "test-app",
          node_type: "streaming-app",
          info: [],
        });

      const { findByTestId, getByTestId } = render(<App />);

      expect(singletonRouter).toMatchObject({
        asPath: "/?focus-node=test-app",
      });

      await findByTestId("graph");

      const currentPipeline = getByTestId("pipeline-current");
      expect(
        within(currentPipeline).getByText("all pipelines")
      ).toBeInTheDocument();

      const nodeSelect = getByTestId("node-select");
      const input = within(nodeSelect).getByRole(
        "combobox"
      ) as HTMLInputElement;
      expect(input).toHaveValue("test-app-name"); // shows label
      expect(nockAppNode.isDone()).toBeTruthy();
    });

    it("should render without url parameters", async () => {
      mockRouter.setCurrentUrl("/");

      const { getByTestId, findByTestId } = render(<App />);

      expect(singletonRouter).toMatchObject({
        asPath: "/",
      });

      await findByTestId("graph");

      // check pipeline set to all
      const currentPipeline = getByTestId("pipeline-current");
      expect(currentPipeline).toHaveTextContent("all pipelines");

      // check focus-node empty
      const nodeSelect = getByTestId("node-select");
      const input = within(nodeSelect).getByRole(
        "combobox"
      ) as HTMLInputElement;
      expect(input).toBeEmptyDOMElement();
    });

    it("should update focus-node & pipeline parameters", async () => {
      mockRouter.setCurrentUrl("/?pipeline=test-pipeline");

      // render App
      const { getByTestId, getByText, findByTestId, findAllByTestId } = render(
        <App />
      );

      await findByTestId("graph");
      const nodeSelect = getByTestId("node-select");
      const input = within(nodeSelect).getByRole(
        "combobox"
      ) as HTMLInputElement;
      expect(input).toBeEmptyDOMElement();

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
      act(() => {
        fireEvent.change(input, { target: { value: "test-app-name" } });
      });
      expect(input).toHaveValue("test-app-name");

      // -- open the search dropdown
      const trigger = nodeSelect.lastElementChild;
      expect(trigger).not.toBeNull();
      fireEvent.mouseDown(trigger!);

      let options = await findAllByTestId("node-option");
      expect(options).toHaveLength(2);
      act(() => {
        fireEvent.click(options[0]);
      });

      // -- check result: pipeline should be present
      expect(singletonRouter).toMatchObject({
        asPath: "/?pipeline=test-pipeline&focus-node=test-app",
      });
      await waitFor(() => {
        expect(nockAppNode.isDone()).toBeTruthy();
      });

      // -- open the search dropdown
      fireEvent.mouseDown(trigger!);

      // -- update focus-node through UI
      fireEvent.change(input, { target: { value: "test-topic-name" } });
      expect(input).toHaveValue("test-topic-name");

      options = await findAllByTestId("node-option");
      fireEvent.click(options[1]);
      await waitFor(() => {
        expect(input).toHaveValue("test-topic");

        // -- check focus-node updated, pipeline still present
        expect(singletonRouter).toMatchObject({
          asPath: "/?pipeline=test-pipeline&focus-node=test-topic",
        });
        expect(nockTopicNode.isDone()).toBeTruthy();
      });

      // -- (re-)set pipeline through UI
      const currentPipeline = getByTestId("pipeline-current");
      fireEvent.mouseOver(currentPipeline);
      await findByTestId("pipeline-select");

      await waitFor(() => {
        const pipeline = getByText("all pipelines");
        expect(pipeline).toBeInTheDocument();
        fireEvent.click(pipeline);
      });
      expect(singletonRouter).toMatchObject({
        asPath: "/",
      });
    });

    it("should redirect to all pipelines if pipeline is not found", async () => {
      const nockPipeline = nock("http://localhost")
        .persist(true)
        .get(`/api/graph?pipeline_name=doesnt-exist`)
        .reply(404);

      const nockUpdate = nock("http://localhost")
        .post(`/api/update`)
        .reply(200);

      mockBackendGraph(true);

      mockRouter.setCurrentUrl("/?pipeline=doesnt-exist");

      const { findByTestId } = render(<App />);

      expect(singletonRouter).toMatchObject({
        asPath: "/?pipeline=doesnt-exist",
      });

      await findByTestId("graph");

      const currentPipeline = await findByTestId("pipeline-current");
      expect(
        within(currentPipeline).getByText("all pipelines")
      ).toBeInTheDocument();
      await waitFor(() => {
        expect(nockPipeline.isDone()).toBeTruthy();
        expect(nockUpdate.isDone()).toBeTruthy();
      });

      expect(singletonRouter).toMatchObject({ asPath: "/" });
      await findByTestId("graph");

      singletonRouter.back(); // FIXME: currently not supported by next-router-mock
      // expect(singletonRouter).toMatchObject({
      //   asPath: "/?pipeline=doesnt-exist",
      // });
    });

    it("should update and retry if pipeline is not found", async () => {
      let nockPipeline = nock("http://localhost")
        .get(`/api/graph?pipeline_name=avail-after-scrape`)
        .reply(404);

      const nockUpdate = nock("http://localhost")
        .post(`/api/update`)
        .reply(200);

      mockBackendGraph(true);

      mockRouter.setCurrentUrl("/?pipeline=avail-after-scrape");

      const { getByTestId, findByTestId } = render(<App />);

      expect(singletonRouter.asPath).toBe("/?pipeline=avail-after-scrape");

      await waitFor(() => {
        // wait for the first pipeline request to fail
        expect(nockPipeline.isDone()).toBeTruthy();
        // pipeline becomes available
        nockPipeline = mockBackendGraph(true, "avail-after-scrape");
      });

      await findByTestId("graph");

      expect(nockUpdate.isDone()).toBeTruthy();
      expect(nockPipeline.isDone()).toBeTruthy();
      await waitFor(() => {
        const currentPipeline = getByTestId("pipeline-current");
        expect(
          within(currentPipeline).getByText("avail-after-scrape")
        ).toBeInTheDocument();
      });

      expect(singletonRouter.asPath).toBe("/?pipeline=avail-after-scrape");
    });

    it("should persist metrics refresh interval across page reloads", async () => {
      mockBackendGraph(true);

      const { findByText, findByTestId, rerender } = render(<App />);

      await findByTestId("graph");

      const metricsMenu = await findByText("Metrics refresh:");
      const anchor = metricsMenu.lastElementChild as HTMLAnchorElement;
      expect(anchor).toHaveTextContent("30s");
      expect(window.localStorage.getItem("metrics-interval")).toBe("30");

      act(() => {
        fireEvent.mouseOver(anchor);
      });

      const metricsSelect = await findByTestId("metrics-select");
      const intervalOff = within(metricsSelect).getByText("off");
      expect(intervalOff).toBeInTheDocument();
      fireEvent.click(intervalOff);
      expect(anchor).toHaveTextContent("off");

      expect(window.localStorage.getItem("metrics-interval")).toBe("0");

      // reload page: window.location.reload() doesn't work in test
      rerender(<App />);
      await findByTestId("graph");
      expect(anchor).toHaveTextContent("off");
    });

    it("should not fetch metrics if interval is set to 'off'", async () => {
      mockBackendGraph(true);
      const nockMetrics = nock("http://localhost")
        .get("/api/metrics")
        .reply(200, []);

      // set metrics refresh interval to 'off'
      window.localStorage.setItem("metrics-interval", "0");

      const { findByTestId, getByText } = render(<App />);

      await findByTestId("graph");

      const metricsSelect = getByText("Metrics refresh:");
      const anchor = metricsSelect.lastElementChild as HTMLAnchorElement;
      expect(anchor).toHaveTextContent("off");
      // verify metrics haven't been refreshed
      expect(nockMetrics.isDone()).toBeFalsy();
    });
  });
});

export {};
