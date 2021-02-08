import React from "react";
import ReactDOM from "react-dom";
import App from "./App";

(window as any).ResizeObserver = class MockResizeObserver {
  observe() {}
  unobserve() {}
};

it("renders without crashing", () => {
  const div = document.createElement("div");
  ReactDOM.render(<App />, div);
});
