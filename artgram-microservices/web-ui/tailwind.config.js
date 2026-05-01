/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./templates/**/*.js",
  ],
  theme: {
    extend: {
      colors: {
        cream: '#f5f0e8',
        parchment: '#ede6d6',
        sand: '#d6c9b0',
        gold: '#b59a6a',
        brown: '#5a3e28',
        espresso: '#2b1d12',
        ink: '#1a1410',
        mist: '#8a7d6e',
        white: '#fdfaf5',
      },
      fontFamily: {
        serif: ['Playfair Display', 'Georgia', 'serif'],
        narrow: ['Cormorant Garamond', 'serif'],
        sans: ['Jost', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
