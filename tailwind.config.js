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
            keyframes: {
                'typewriter': {
                    '0%': { opacity: '0' },
                    '50%': { opacity: '1' },
                    '100%': { opacity: '0' }
                }
            },
            animation: {
                'typewriter': 'typewriter 1s infinite'
            },
            backgroundImage: theme => ({
                'custom-gradient': 'linear-gradient(176deg, rgb(18, 24, 27) 50%, rgb(32, 39, 55) 100%)',
            }),
            boxShadow: {
                'custom-discord': '0 0 5px #4752C5, 0 0 25px #4752C5, 0 0 50px #4752C5, 0 0 100px',
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
