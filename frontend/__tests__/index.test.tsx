import { render, screen } from "@testing-library/react";
import nock from "nock";
import React from "react";
import App from "../components/App";

// -- Mock GraphVisualization
jest.mock("../components/GraphVisualization", () => {
  return function DummyGraphVisualization() {
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

  mockBackendGraph(true);

  nock("http://localhost").persist().get("/api/metrics").reply(200, []);

  nock("http://localhost").persist().get("/api/pipelines").reply(200, {
    pipelines: [],
  });

  it("renders without crashing", async () => {
    const { findByTestId } = render(<App />);
    await findByTestId("graph");
  });
});
