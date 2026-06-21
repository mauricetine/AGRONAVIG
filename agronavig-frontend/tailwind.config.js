/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        primary: "#13ec49",
        "bg-light": "#f6f8f6",
        "bg-dark": "#102215",
        earth: {
          50:  "#fdf8f6",
          100: "#f2e8e5",
          200: "#eaddd7",
          500: "#8b5e3c",
          900: "#4a301f",
        },
      },
      fontFamily: {
        display: ["Inter", "sans-serif"],
      },
    },
  },
  plugins: [],
}