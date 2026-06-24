// Optional: configure or set up a testing framework before each test.
// If you delete this file, remove `setupFilesAfterEnv` from `jest.config.js`

// Used for __tests__/testing-library.js
// Learn more: https://github.com/testing-library/jest-dom
import "@testing-library/jest-dom/extend-expect";
import "jest-fix-undefined";
import "whatwg-fetch";

// Stub HTMLCanvasElement.getContext so jsdom doesn't require the canvas native
// module. No tests exercise real canvas rendering — GraphVisualization is mocked.
HTMLCanvasElement.prototype.getContext = () => null;
