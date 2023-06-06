import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { fireEvent, render, within } from "@testing-library/react";
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

describe("Search", () => {
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
    nock("http://localhost")
      .persist(true)
      .get("/api/graph")
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

    nock("http://localhost").persist().get("/api/metrics").reply(200, []);

    nock("http://localhost")
      .persist()
      .get("/api/pipelines")
      .reply(200, {
        pipelines: ["test-pipeline"],
      });

    it("node icons", async () => {
      // render App
      const { getByTestId, findByTestId, findAllByTestId } = render(<App />);

      await findByTestId("graph");
      const nodeSelect = getByTestId("node-select");

      // -- open the search dropdown
      const trigger = nodeSelect.lastElementChild;
      expect(trigger).not.toBeNull();
      fireEvent.mouseDown(trigger!);

      let options = await findAllByTestId("node-option");
      expect(options).toHaveLength(2);
      let iconApp = within(options[0]).getByTestId("node-icon");
      expect(iconApp).toBeInTheDocument();
      expect(iconApp).toHaveAttribute("src", "streaming-app.svg");
      expect(iconApp).toHaveProperty("alt", "streaming-app-icon");
      let iconTopic = within(options[1]).getByTestId("node-icon");
      expect(iconTopic).toBeInTheDocument();
      expect(iconTopic).toHaveAttribute("src", "topic.svg");
      expect(iconTopic).toHaveProperty("alt", "topic-icon");
    });
  });
});

export {};
