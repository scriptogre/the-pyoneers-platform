/** @type {import('tailwindcss').Config} */

module.exports = {
  content: ["./**/*.{html,js,jinja}"],
  darkMode: 'class',
  theme: {
    fontFamily: {
      'sans': ['Barlow', 'ui-sans-serif', 'system-ui', '-apple-system', 'BlinkMacSystemFont'], // Add other fallback fonts as required
      'mono': ['Bebas Neue', 'ui-monospace', 'SFMono-Regular', 'Menlo', 'Monaco', 'Consolas', 'Liberation Mono', 'Courier New', 'monospace'],
    },
    extend: {
      boxShadow: {
        'custom-golden': '0 0 5px #FBBD23, 0 0 25px #FBBD23, 0 0 50px #FBBD23, 0 0 100px',
      },
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
