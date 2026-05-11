/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      fontFamily: {
        mono: ['"JetBrains Mono"', "ui-monospace", "SFMono-Regular", "monospace"],
      },
      colors: {
        forensic: {
          bg: "#0a0e14",
          panel: "#0f1620",
          line: "#1e2a3a",
        },
      },
    },
  },
  plugins: [],
};
