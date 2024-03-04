import type { Config } from "tailwindcss";

export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  mode: "jit",
  theme: {
    extend: {
      colors: { 
        dark: "#0D0D0D",
        "dark-blue": "#0A0E14",
        purple: "#5D3EBE",
        "light-purple": "#7C5DFF",
        "light-blue": "#00C2FF",
      },
    },
  },
  plugins: [],
} satisfies Config;
