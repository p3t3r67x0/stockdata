const plugin = require('tailwindcss/plugin')

const {
  colors
} = require('tailwindcss/defaultTheme')

module.exports = {
  future: {
    removeDeprecatedGapUtilities: true,
    purgeLayersByDefault: true,
  },
  purge: [],
  theme: {
    extend: {
      colors: {
        red: {
          ...colors.red,
          150: '#fdcdcd'
        },
        green: {
          ...colors.green,
          150: '#bcecc9'
        }
      }
    },
  },
  variants: {
    backgroundColor: ['responsive', 'hover', 'focus', 'even', 'odd']
  },
  plugins: [],
}
