import { defineConfig } from "@openapi-codegen/cli";
import {
  generateReactQueryComponents,
  generateSchemaTypes,
} from "@openapi-codegen/typescript";
export default defineConfig({
  api: {
    from: {
      relativePath: "../backend/docs/openapi.json",
      source: "file",
    },
    outputDir: "./components/api",
    to: async (context) => {
      const filenamePrefix = "api";
      const { schemasFiles } = await generateSchemaTypes(context, {
        filenamePrefix,
      });
      await generateReactQueryComponents(context, {
        filenamePrefix,
        schemasFiles,
      });
    },
  },
});
