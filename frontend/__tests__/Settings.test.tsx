import { fireEvent, render } from "@testing-library/react";
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
      const { getByTestId, findByTestId } = render(<TestSettings />);
      await findByTestId("settings-button");
      const settings = getByTestId("settings-button");
      fireEvent.click(settings);

      const checkbox = await findByTestId("animate");
      expect(checkbox).toBeChecked();
    });
  });

  describe("should restore from local storage", () => {
    it("animate disabled", async () => {
      window.localStorage.setItem("animate", "false");

      const { getByTestId, findByTestId } = render(<TestSettings />);
      await findByTestId("settings-button");
      const settings = getByTestId("settings-button");
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
});
