import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  publicDir: "static",
  test: {
    environment: "jsdom",
    setupFiles: "./src/testSetup.js",
  },
});
