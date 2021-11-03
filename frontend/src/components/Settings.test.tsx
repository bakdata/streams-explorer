import React, { useState } from "react";
import { fireEvent, render, waitForElement } from "@testing-library/react";
import Settings from "./Settings";

const StateDisplay = ({ id, state }: { id: string; state: any }) => {
  return <div data-testid={id}>{state}</div>;
};

const TestSettings = () => {
  const [animate, setAnimate] = useState<boolean>(true);
  return (
    <>
      <Settings
        animate={animate}
        setAnimate={(checked: boolean) => setAnimate(checked)}
      />
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

      await waitForElement(() => getByTestId("animate"));
      const checkbox = getByTestId("animate");
      // HACK: needed as a workaround until we update react-testing library & react-scripts
      // because .toBeChecked() doesn't work with role 'switch'
      expect(checkbox).toHaveAttribute("aria-checked", "true");
    });
  });

  describe("should restore from local storage", () => {
    it("animate disabled", async () => {
      window.localStorage.setItem("animate", "false");

      const { getByTestId, findByTestId } = render(<TestSettings />);
      await findByTestId("settings-button");
      const settings = getByTestId("settings-button");
      fireEvent.click(settings);

      await waitForElement(() => getByTestId("animate"));

      const checkbox = getByTestId("animate");
      expect(checkbox).toHaveAttribute("aria-checked", "false"); // HACK
    });

    it("animate enabled", async () => {
      window.localStorage.setItem("animate", "true");

      const { getByTestId, findByTestId } = render(<TestSettings />);
      await findByTestId("settings-button");
      const settings = getByTestId("settings-button");
      fireEvent.click(settings);

      await waitForElement(() => getByTestId("animate"));
      const checkbox = getByTestId("animate");
      expect(checkbox).toHaveAttribute("aria-checked", "true"); // HACK
    });
  });
});
