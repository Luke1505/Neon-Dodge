/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'neon-green': '#50ff28',
        'neon-blue': '#00dcff',
        'neon-yellow': '#ffff50',
        'neon-red': '#ff0000',
        'neon-magenta': '#ff32ff',
        'neon-cyan': '#00ffff',
        'neon-orange': '#ffb400',
        'neon-purple': '#be6eff',
        'neon-pink': '#ff64c8',
        'deep-space-black': '#0a0a1e',
        'accent-dark-blue': '#28285a',
        'bright-white': '#ffffff',
        'light-text': '#dcdcdc',
        'medium-text': '#b4b4b4',
      },
      animation: {
        'pulse-neon': 'pulse-neon 2s ease-in-out infinite',
        'float': 'float 3s ease-in-out infinite',
      },
    },
  },
  plugins: [],
}