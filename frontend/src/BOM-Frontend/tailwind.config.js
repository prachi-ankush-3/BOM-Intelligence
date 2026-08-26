/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        primaryBlue: '#145487',
        primaryBlueDark: '#0E3F66',
        sidebarBg: '#E9EDF5',
        mainBg: '#F4F5F7',
        inputBg: '#FFFFFF',
        borderGray: '#C8CDD3',
        textDark: '#222222',
        textSecondary: '#555555',
        progressOrange: '#F7931E',
      },
      fontFamily: {
        sans: ['Segoe UI', 'Tahoma', 'Geneva', 'Verdana', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
