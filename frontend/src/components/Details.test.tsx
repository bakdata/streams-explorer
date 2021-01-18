import nock from "nock";
import React from "react";
import { RestfulProvider } from "restful-react";

import Details from "./Details";
import { waitForElement, render } from "@testing-library/react";
import { act } from "react-dom/test-utils";

describe("display node information", () => {
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
  });

  it("should handle node not found error", async () => {
    nock("http://localhost").get("/api/node/1").reply(404, {
      detail: 'Could not find information for node with name "fake-node"',
    });

    const { getByTestId, asFragment } = render(
      <RestfulProvider base="http://localhost">
        <Details nodeID="1" />
      </RestfulProvider>
    );

    await waitForElement(() => getByTestId("no-node-info"));
    expect(asFragment()).toMatchSnapshot();
  });

  it("should handle connector info", async () => {
    nock("http://localhost").get("/api/node/2").reply(200, {
      node_id: "demo-ames-sink",
      node_type: "connector",
      info: [],
    });

    const { getByText, asFragment } = render(
      <RestfulProvider base="http://localhost">
        <Details nodeID="2" />
      </RestfulProvider>
    );

    await waitForElement(() => getByText("connector"));
    expect(asFragment()).toMatchSnapshot();
  });

  it("should handle connector info", async () => {
    nock("http://localhost").get("/api/node/2").reply(200, {
      node_id: "demo-ames-sink",
      node_type: "connector",
      info: [],
    });

    const { getByText, asFragment } = render(
      <RestfulProvider base="http://localhost">
        <Details nodeID="2" />
      </RestfulProvider>
    );

    await waitForElement(() => getByText("connector"));
    expect(asFragment()).toMatchSnapshot();
  });

  it("should handle streams app info", async () => {
    nock("http://localhost")
      .get("/api/node/atm-fraud-transactionavroproducer")
      .reply(200, {
        node_id: "atm-fraud-transactionavroproducer",
        node_type: "streaming-app",
        info: [
          { name: "Kibana Logs", value: "", type: "link" },
          {
            name: "Labels",
            value: {
              app: "atm-fraud-transactionavroproducer",
              "app.kubernetes.io/managed-by": "Helm",
              chart: "streams-app-0.1.0",
              pipeline: "streams-explorer",
              release: "demo-transactionavroproducer",
            },
            type: "json",
          },
        ],
      });

    nock("http://localhost")
      .get("/api/node/linking/atm-fraud-transactionavroproducer?")
      .reply(
        200,
        "http://localhost:5601/app/kibana#/discover?_a=(columns:!(_source),query:(language:lucene,query:'kubernetes.labels.app:%20%22atm-fraud-transactionavroproducer%22'))"
      );
    const { getByText, asFragment } = render(
      <RestfulProvider base="http://localhost">
        <Details nodeID="atm-fraud-transactionavroproducer" />
      </RestfulProvider>
    );

    await waitForElement(() => getByText("streaming-app"));
    expect(asFragment()).toMatchSnapshot();
  });

  it("should handle topic info", async () => {
    nock("http://localhost")
      .get("/api/node/atm-fraud-incoming-transactions-topic")
      .reply(200, {
        node_id: "atm-fraud-incoming-transactions-topic",
        node_type: "topic",
        info: [
          { name: "Topic Monitoring", value: "grafana", type: "link" },
          {
            name: "Schema",
            value: {
              type: "record",
              name: "Transaction",
              namespace: "com.bakdata.kafka",
              fields: [
                {
                  name: "transaction_id",
                  type: { type: "string", "avro.java.string": "String" },
                },
                {
                  name: "account_id",
                  type: { type: "string", "avro.java.string": "String" },
                },
                { name: "amount", type: "int" },
                {
                  name: "atm",
                  type: { type: "string", "avro.java.string": "String" },
                  default: "",
                },
                {
                  name: "timestamp",
                  type: { type: "long", logicalType: "timestamp-millis" },
                },
                {
                  name: "location",
                  type: {
                    type: "record",
                    name: "Location",
                    fields: [
                      { name: "latitude", type: "double" },
                      { name: "longitude", type: "double" },
                    ],
                  },
                },
              ],
            },
            type: "json",
          },
        ],
      });

    nock("http://localhost")
      .get(
        "/api/node/linking/atm-fraud-incoming-transactions-topic?link_type=grafana"
      )
      .reply(
        200,
        "http://localhost:3000/d/path/to/dashboard?var-topics=atm-fraud-incoming-transactions-topic"
      );
    const { getByText, asFragment } = render(
      <RestfulProvider base="http://localhost">
        <Details nodeID="atm-fraud-incoming-transactions-topic" />
      </RestfulProvider>
    );

    await waitForElement(() => getByText("topic"));
    expect(asFragment()).toMatchSnapshot();
  });
});
