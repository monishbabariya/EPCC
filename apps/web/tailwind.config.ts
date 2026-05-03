import type { Config } from "tailwindcss";

export default {
  content: [
    "./index.html",
    "./src/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // X9 v0.3 dual-encoded palette extends here once locked
        rag: {
          green: "#16a34a",
          amber: "#d97706",
          red: "#dc2626",
        },
      },
    },
  },
  plugins: [],
} satisfies Config;
