/** @type {import('tailwindcss').Config} */
export default {
  corePlugins: {
    //preflight: false,
  },
  important: '#root',
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {},
  },
  plugins: [],
};
