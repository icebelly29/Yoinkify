/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
      './templates/**/*.html'
    ],
    theme: {
      extend: {
        colors: {
          spotify: {
            green: '#1DB954',
            black: '#191414',
            gray: '#282828'
          }
        },
        fontFamily: {
          'spotify': ['Spotify Circular', 'sans-serif']
        }
      },
    },
    plugins: [],
  }