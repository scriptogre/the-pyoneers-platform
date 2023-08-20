/** @type {import('tailwindcss').Config} */
const colors = require('tailwindcss/colors')

module.exports = {
  content: ["./**/*.{html,js}"],
  darkMode: 'class',
  theme: {
    fontFamily: {
      'sans': ['Barlow', 'ui-sans-serif', 'system-ui', '-apple-system', 'BlinkMacSystemFont'], // Add other fallback fonts as required
      'mono': ['Bebas Neue', 'ui-monospace', 'SFMono-Regular', 'Menlo', 'Monaco', 'Consolas', 'Liberation Mono', 'Courier New', 'monospace'],
    },
    extend: {
      typography: {
        DEFAULT: {
          css: {
            h1: {
              'font-weight': 'normal',
              'font-size': '2.5rem',
            },
            h2: {
              'font-weight': 'normal',
              'font-size': '2rem',
            },
            h3: {
              'font-weight': 'normal',
              'font-size': '1.75rem',
            },
            h4: {
              'font-weight': 'normal',
              'font-size': '1.5rem',
            },
            h5: {
              'font-weight': 'normal',
              'font-size': '1.25rem',
            }
          },
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('daisyui'),
  ]
}
