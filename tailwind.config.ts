import type { Config } from "tailwindcss";

export default {
  content: ["./frontend/src/**/*.{ts,tsx}"],
  corePlugins: {
    preflight: false,
  },
  theme: {
    extend: {
      colors: {
        "info-blue": "#003E7E",
        "info-cyan": "#058ED0",
        "info-surface": "#F8FBFD",
      },
    },
  },
  plugins: [],
} satisfies Config;
