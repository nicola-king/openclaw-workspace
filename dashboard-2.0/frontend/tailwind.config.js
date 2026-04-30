/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'taiyi-blue': '#1E88E5',
        'tech-blue': '#0D47A1',
        'success-green': '#43A047',
        'warning-yellow': '#FFB300',
        'error-red': '#E53935',
        'dark-bg': '#1A1A2E',
        'card-bg': '#16213E',
        'border-color': '#0F3460',
      }
    },
  },
  plugins: [],
}
