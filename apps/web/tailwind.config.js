/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        cyber: {
          bg: "#050505",
          card: "#0a0a0a",
          border: "#333333",
          accent: "#00ff41",
          danger: "#ff003c",
          warning: "#ffb000",
          success: "#00ff41",
          text: "#e0e0e0",
          muted: "#666666"
        }
      },
      fontFamily: {
        mono: ['var(--font-share-tech-mono)', 'monospace'],
      },
    },
  },
  plugins: [],
}
