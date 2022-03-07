import { fireEvent, render, waitFor } from "@testing-library/react";
import nock from "nock";
import React, { useState } from "react";
import Settings from "../components/Settings";

const StateDisplay = ({ id, state }: { id: string; state: any }) => {
  return <div data-testid={id}>{state}</div>;
};

const TestSettings = () => {
  const [animate, setAnimate] = useState<boolean>(true);
  return (
    <>
      <Settings animate={animate} setAnimate={setAnimate} />
      <StateDisplay id="animate-state" state={animate} />
    </>
  );
};

describe("Settings", () => {
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

  describe("should set state", () => {
    it("animate enabled by default", async () => {
      const { findByTestId } = render(<TestSettings />);
      const settings = await findByTestId("settings-button");
      fireEvent.click(settings);

      const checkbox = await findByTestId("animate");
      expect(checkbox).toBeChecked();
    });
  });

  describe("should restore from local storage", () => {
    it("animate disabled", async () => {
      window.localStorage.setItem("animate", "false");

      const { findByTestId } = render(<TestSettings />);
      const settings = await findByTestId("settings-button");
      fireEvent.click(settings);

      const checkbox = await findByTestId("animate");
      expect(checkbox).not.toBeChecked();
    });

    it("animate enabled", async () => {
      window.localStorage.setItem("animate", "true");

      const { getByTestId, findByTestId } = render(<TestSettings />);
      await findByTestId("settings-button");
      const settings = getByTestId("settings-button");
      fireEvent.click(settings);

      const checkbox = await findByTestId("animate");
      expect(checkbox).toBeChecked();
    });
  });

  it("should display version", async () => {
    const nockVersion = nock("http://localhost")
      .get("/api/version")
      .reply(200, "0.0.1")
      .persist();

    const { findByTestId, getByText } = render(<TestSettings />);
    const settings = await findByTestId("settings-button");
    fireEvent.click(settings);

    expect(nockVersion.isDone()).toBeTruthy();
    // const version = await findByTestId("version");
    // await waitFor(() =>
    //   expect(version).toHaveTextContent("Streams Explorer 0.0.1")
    // );
    await waitFor(() => {
      expect(getByText("Streams Explorer 0.0.1")).toBeInTheDocument();
    });
  });
});
