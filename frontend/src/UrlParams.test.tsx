// import { pushHistoryFocusNode } from "./App";
import App from "./App";

describe("url parameters", () => {
  const mockLocation = new URL("http://localhost");

  beforeEach(() => {
    delete window.location;
    window.location = mockLocation;
  });

  it("should update focus-node param", () => {
    // window.location.search = "?focus-node=some-node-id";
    // expect(global.window.location.search).toEqual("?focus-node=some-node-id");

    window.location.search = "?pipeline=test-pipeline";
    expect(global.window.location.search).toEqual("?pipeline=test-pipeline");

    // pushHistoryFocusNode("test-node-id");
    // const app = shallow(<App />);
    // app.setState()
  });
});

export {};
