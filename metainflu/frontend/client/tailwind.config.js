// File: frontend/client/tailwind.config.cjs

/** @type {import('tailwindcss').Config} */
module.exports = {
  // The 'content' array is crucial. It tells Tailwind which files to scan
  // for class names. If this array is empty or incorrect, no CSS will be generated.
  content: [
    "./index.html",
    // This line tells Tailwind to look inside all .vue, .js, .ts, etc. files
    // within the 'src' directory and its subdirectories.
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'dark-slate-gray': '#2F4F4F',
        'soft-blue': '#60A5FA',
        'cool-purple': '#8B5CF6',
        'light-blue': '#BFDBFE',
      },
    },
  },
  plugins: [
    // You can add Tailwind plugins here if needed
  ],
};
