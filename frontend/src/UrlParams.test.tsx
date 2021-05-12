import nock from "nock";
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
import userEvent from "@testing-library/user-event";

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

const createMocks = () => {
  const historyMock: Record<string, any> = {
    push: jest.fn(),
    location: {},
    listen: jest.fn(),
  };
  const locationMock: Record<string, any> = {
    hash: "",
    key: "",
    pathname: "",
    search: "",
    state: {},
  };
  return { historyMock, locationMock };
};

jest.mock("./components/GraphVisualization", () => {
  return function DummyGraphVisualization(props: any) {
    return <div data-testid="graph"></div>;
  };
});

describe("url parameters", () => {
  // const mockLocation = new URL("http://localhost");

  // beforeEach(() => {
  //   delete window.location;
  //   window.location = mockLocation;
  // });

  it("should update focus-node param", async () => {
    jest.setTimeout(30000);
    // set pipeline
    // window.location.search = "?pipeline=test-pipeline";
    // expect(window.location.search).toEqual("?pipeline=test-pipeline");

    // TODO: remove debug
    // nock("http://localhost")
    //   .persist()
    //   .get(/.*/)
    //   .reply(404, "Nock all GET requests");

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

    const { historyMock, locationMock } = createMocks();

    const { getByTestId, asFragment, getAllByTestId } = render(
      <Router history={historyMock as never}>
        <RestfulProvider base="http://localhost">
          <App />
        </RestfulProvider>
      </Router>
    );

    await waitForElement(() => getByTestId("loading"));
    expect(asFragment()).toMatchSnapshot();

    await waitForElement(() => getByTestId("graph"));
    expect(asFragment()).toMatchSnapshot();

    await waitForElement(() => getByTestId("pipeline-select"));
    expect(asFragment()).toMatchSnapshot();

    const pipelineSelect = getByTestId("pipeline-select");
    const { getByText } = within(pipelineSelect);
    expect(getByText("all pipelines")).toBeInTheDocument();
    // const pipelineOptions = within(pipelineSelect).getAllByTestId(
    //   "pipeline-option"
    // );
    // expect(pipelineOptions).toHaveLength(1);

    const nodeSelect = getByTestId("node-select");
    const input = within(nodeSelect).getByRole("combobox") as HTMLInputElement;

    expect(input).toHaveValue("");

    // input.setAttribute("value", "test-app");

    // -- method 1: using fireEvent
    fireEvent.change(input, { target: { value: "test-app" } });
    expect(input).toHaveValue("test-app");
    // let options = getAllByTestId("node-option");
    // expect(options).toHaveLength(1);

    // -- method 2: using userEvent select
    // userEvent.selectOptions(input, "test-app");
    // expect(input).toHaveValue("test-app");
    // let nodeOptions = getAllByTestId("node-option");
    // expect(nodeOptions).toHaveLength(2);
    // expect((nodeOptions[0] as HTMLOptionElement).selected).toBeTruthy();

    // check result
    await wait(() =>
      expect(window.location.search).toEqual("?focus-node=test-app")
    );

    // await waitForElement(() => getByTestId("graph-error"), { timeout: 30000 });
    // expect(asFragment()).toMatchSnapshot();

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
