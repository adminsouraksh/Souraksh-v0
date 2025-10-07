/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'soft-blue': '#4C8BF5',
        'vibrant-green': '#4CAF50',
        'dark-gray': '#333333',
        'light-gray': '#F2F2F2',
        'muted-orange': '#FF9800',
        'light-blue': '#E3F2FD',
        'cool-purple': '#9C27B0',
        'white': '#FFFFFF',
        'dark-slate-gray': '#2F4F4F',
      }
    },
  },
  plugins: [],
};