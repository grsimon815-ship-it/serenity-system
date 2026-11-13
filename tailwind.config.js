/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        poly: {
          bg: '#090d16',
          card: '#0f172a',
          cardBorder: '#1e293b',
          accent: '#6366f1',
          rust: '#f97316',
          go: '#06b6d4',
          ts: '#3b82f6',
          py: '#eab308',
          java: '#ef4444',
          cpp: '#8b5cf6',
          elixir: '#a855f7'
        }
      },
      fontFamily: {
        mono: ['Fira Code', 'JetBrains Mono', 'Consolas', 'monospace'],
        sans: ['Inter', 'system-ui', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
