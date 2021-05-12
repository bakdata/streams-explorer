import nock from "nock";
import React from "react";
import { RestfulProvider } from "restful-react";
import App from "./App";
import { Router } from "react-router";
import { waitForElement, render } from "@testing-library/react";

// disable resize observer
(window as any).ResizeObserver = class MockResizeObserver {
  observe() {}
  unobserve() {}
  disconnect() {}
};

describe("url parameters", () => {
  const mockLocation = new URL("http://localhost");

  beforeEach(() => {
    delete window.location;
    window.location = mockLocation;
  });

  it("should update focus-node param", async () => {
    // set pipeline
    window.location.search = "?pipeline=test-pipeline";
    expect(window.location.search).toEqual("?pipeline=test-pipeline");

    nock("http://localhost")
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

    nock("http://localhost")
      .get("/api/pipelines")
      .reply(200, {
        pipelines: ["test-pipeline"],
      });

    nock("http://localhost")
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

    const historyMock = { push: jest.fn(), location: {}, listen: jest.fn() };

    const { getByTestId, asFragment } = render(
      <Router history={historyMock as never}>
        <RestfulProvider base="http://localhost">
          <App />
        </RestfulProvider>
      </Router>
    );

    await waitForElement(() => getByTestId("loading"));
    expect(asFragment()).toMatchSnapshot();

    // add focus-node
    // instance is null on stateless functional components (React 16+)
    // wrapper.instance().pushHistoryFocusNode("test-node-id");

    // pipeline kept
    // expect(window.location.search).toEqual(
    //   "?pipeline=test-pipeline&focus-node=test-node-id"
    // );
  });
});

export {};
