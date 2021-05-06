import React from "react";
import App from "./App";
import { HashRouter } from "react-router-dom";
import { configure, shallow, mount } from "enzyme";
import Adapter from "enzyme-adapter-react-16";
import { createMemoryHistory } from "history";

configure({ adapter: new Adapter() });

// jest.mock("react-router-dom", () => ({
//   useLocation: jest.fn().mockReturnValue({
//     pathname: "/another-route",
//     search: "",
//     hash: "",
//     state: null,
//     key: "5nvxpbdafa",
//   }),
// }));

describe("url parameters", () => {
  const mockLocation = new URL("http://localhost");

  beforeEach(() => {
    delete window.location;
    window.location = mockLocation;
  });

  // const AppRender = mount(
  //   <HashRouter>
  //     <App />,
  //   </HashRouter>
  // ).children();

  it("should update focus-node param", () => {
    // set pipeline
    window.location.search = "?pipeline=test-pipeline";
    expect(global.window.location.search).toEqual("?pipeline=test-pipeline");

    // const history = createMemoryHistory("/static");
    const wrapper = shallow(<App />);

    // add focus-node
    wrapper.instance().pushHistoryFocusNode("test-node-id");

    // pipeline kept
    expect(global.window.location.search).toEqual(
      "?pipeline=test-pipeline&focus-node=test-node-id"
    );
  });
});

export {};
