import { resolve } from "node:path";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react()],
  build: {
    manifest: true,
    outDir: "AlertaDengue/static/frontend",
    emptyOutDir: true,
    rollupOptions: {
      input: {
        team: resolve(__dirname, "frontend/src/entries/team.tsx"),
      },
      output: {
        entryFileNames: "[name].js",
        chunkFileNames: "chunks/[name].js",
        assetFileNames: "assets/[name][extname]",
      },
    },
  },
});
