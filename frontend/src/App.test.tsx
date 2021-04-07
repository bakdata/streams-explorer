import React from "react";
import ReactDOM from "react-dom";
import { HashRouter } from "react-router-dom";
import App from "./App";

(window as any).ResizeObserver = class MockResizeObserver {
  observe() {}
  unobserve() {}
};

it("renders without crashing", () => {
  const div = document.createElement("div");
  ReactDOM.render(
    <HashRouter>
      <App />
    </HashRouter>,
    div
  );
});
