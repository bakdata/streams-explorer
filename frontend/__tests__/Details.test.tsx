import nock from "nock";
import React from "react";
import { RestfulProvider } from "restful-react";

import {
  fireEvent,
  render,
  waitFor,
  waitForElementToBeRemoved,
} from "@testing-library/react";
import Details from "../components/Details";

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

    const { findByTestId, asFragment } = render(
      <RestfulProvider base="http://localhost">
        <Details nodeId="1" />
      </RestfulProvider>
    );

    await findByTestId("no-node-info");
    expect(asFragment()).toMatchSnapshot();
  });

  it("should handle connector info", async () => {
    nock("http://localhost").get("/api/node/2").reply(200, {
      node_id: "demo-ames-sink",
      node_type: "connector",
      info: [],
    });

    const { findByText, asFragment } = render(
      <RestfulProvider base="http://localhost">
        <Details nodeId="2" />
      </RestfulProvider>
    );

    await findByText("connector");
    expect(asFragment()).toMatchSnapshot();
  });

  it("should handle connector info", async () => {
    nock("http://localhost").get("/api/node/2").reply(200, {
      node_id: "demo-ames-sink",
      node_type: "connector",
      info: [],
    });

    const { findByText, asFragment } = render(
      <RestfulProvider base="http://localhost">
        <Details nodeId="2" />
      </RestfulProvider>
    );

    await findByText("connector");
    expect(asFragment()).toMatchSnapshot();
  });

  it("should handle streams app info", async () => {
    nock("http://localhost")
      .get("/api/node/atm-fraud-transactionavroproducer")
      .reply(200, {
        node_id: "atm-fraud-transactionavroproducer",
        node_type: "streaming-app",
        info: [
          { name: "Kibana Logs", value: "kibana", type: "link" },
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

    const nockLinking = nock("http://localhost")
      .get("/api/node/linking/atm-fraud-transactionavroproducer")
      .query({ link_type: "kibana" })
      .reply(
        200,
        "http://localhost:5601/app/kibana#/discover?_a=(columns:!(_source),query:(language:lucene,query:'kubernetes.labels.app:%20%22atm-fraud-transactionavroproducer%22'))"
      );
    const { findByText, asFragment, queryByText } = render(
      <RestfulProvider base="http://localhost">
        <Details nodeId="atm-fraud-transactionavroproducer" />
      </RestfulProvider>
    );

    await findByText("streaming-app");
    await waitForElementToBeRemoved(() => queryByText("Loading link..."));
    expect(nockLinking.isDone()).toBeTruthy();
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
            value: {},
            type: "json",
          },
        ],
      });

    nock("http://localhost")
      .get("/api/node/atm-fraud-incoming-transactions-topic/schema")
      .reply(200, [1, 2]);

    const nockSchema2 = nock("http://localhost")
      .get("/api/node/atm-fraud-incoming-transactions-topic/schema/2")
      .reply(200, {
        type: "record",
        name: "Transaction2",
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
      });

    const nockSchema1 = nock("http://localhost")
      .get("/api/node/atm-fraud-incoming-transactions-topic/schema/1")
      .reply(200, {
        type: "record",
        name: "Transaction1",
        namespace: "com.bakdata.kafka",
        fields: [
          {
            name: "transaction_id",
            type: { type: "string", "avro.java.string": "String" },
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

    const { getByText, findByText, getByTestId } = render(
      <RestfulProvider base="http://localhost">
        <Details nodeId="atm-fraud-incoming-transactions-topic" />
      </RestfulProvider>
    );

    await findByText("v2"); // get dropdown menu for schema version
    let schemaVersion = getByText("v2");
    expect(nockSchema2.isDone()).toBeTruthy();
    expect(nockSchema1.isDone()).toBeFalsy();
    const schema2 = getByTestId("schema");
    expect(schema2).toMatchSnapshot();

    fireEvent.mouseOver(getByTestId("schema-version"));
    await waitFor(() => {
      const menu = getByTestId("schema-version-select");
      fireEvent.mouseOver(menu);
      const v1 = getByText("v1");
      fireEvent.click(v1);
    });

    await waitFor(() => {
      expect(schemaVersion).toHaveTextContent("v1");
      expect(nockSchema1.isDone()).toBeTruthy();
    });

    await waitFor(() => {
      expect(schema2).not.toBeInTheDocument();
      const schema1 = getByTestId("schema");
      expect(schema1).toMatchSnapshot();
    });
  });

  it("should show error if schema versions are unavailable", async () => {
    nock("http://localhost")
      .get("/api/node/atm-fraud-incoming-transactions-topic")
      .reply(200, {
        node_id: "atm-fraud-incoming-transactions-topic",
        node_type: "topic",
        info: [
          {
            name: "Schema",
            value: {},
            type: "json",
          },
        ],
      });

    nock("http://localhost")
      .get("/api/node/atm-fraud-incoming-transactions-topic/schema")
      .reply(404);

    const { findByTestId } = render(
      <RestfulProvider base="http://localhost">
        <Details nodeId="atm-fraud-incoming-transactions-topic" />
      </RestfulProvider>
    );

    await findByTestId("no-schema-versions");
  });

  it("should show error if schema versions is empty", async () => {
    nock("http://localhost")
      .get("/api/node/atm-fraud-incoming-transactions-topic")
      .reply(200, {
        node_id: "atm-fraud-incoming-transactions-topic",
        node_type: "topic",
        info: [
          {
            name: "Schema",
            value: {},
            type: "json",
          },
        ],
      });

    nock("http://localhost")
      .get("/api/node/atm-fraud-incoming-transactions-topic/schema")
      .reply(200, []);

    const { findByTestId } = render(
      <RestfulProvider base="http://localhost">
        <Details nodeId="atm-fraud-incoming-transactions-topic" />
      </RestfulProvider>
    );

    await findByTestId("no-schema-versions");
  });

  it("should show error if schema is unavailable", async () => {
    nock("http://localhost")
      .get("/api/node/atm-fraud-incoming-transactions-topic")
      .reply(200, {
        node_id: "atm-fraud-incoming-transactions-topic",
        node_type: "topic",
        info: [
          {
            name: "Schema",
            value: {},
            type: "json",
          },
        ],
      });

    nock("http://localhost")
      .get("/api/node/atm-fraud-incoming-transactions-topic/schema")
      .reply(200, [1]);

    nock("http://localhost")
      .get("/api/node/atm-fraud-incoming-transactions-topic/schema/1")
      .reply(404);

    const { findByTestId } = render(
      <RestfulProvider base="http://localhost">
        <Details nodeId="atm-fraud-incoming-transactions-topic" />
      </RestfulProvider>
    );

    await findByTestId("no-schema");
  });
});
