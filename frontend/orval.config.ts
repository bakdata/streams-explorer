import { defineConfig } from "orval";

export default defineConfig({
  streamsExplorer: {
    input: "../backend/docs/openapi.json",
    output: {
      mode: "single",
      target: "./lib/api/fetchers.ts",
      schemas: "./lib/api/model",
      client: "react-query",
      httpClient: "axios",
      override: {
        mutator: {
          path: "./lib/api/mutator.ts",
          name: "customInstance",
        },
      },
    },
  },
});
