import { render } from "@testing-library/react";
import nock from "nock";
import React from "react";
import { RestfulProvider } from "restful-react";
import DetailsCard from "../components/DetailsCard";
import Node from "../components/graph/Node";

describe("display card for node details", () => {
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

  it("should show node label", async () => {
    const node: Node = { id: "test-app", label: "test-app-name" };
    nock("http://localhost").get("/api/node/test-app").reply(200, {
      node_id: "test-app",
      node_type: "streaming-app",
      info: [],
    });

    const { queryByText } = render(
      <RestfulProvider base="http://localhost">
        <DetailsCard node={node} />
      </RestfulProvider>
    );

    expect(queryByText("test-app-name - Details")).toBeInTheDocument();
  });
});
