/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    '../templates/**/*.html',       // Global templates folder
    '../**/templates/**/*.html',    // App-specific templates
    '../static/js/*.js'
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('daisyui'),
  ],
}

