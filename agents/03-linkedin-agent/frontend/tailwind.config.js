module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'forest-green': '#1a3a3a',
        'warm-ivory': '#f5f1ed',
        'dark-graphite': '#2a2a2a',
        'muted-gold': '#c9b89b',
        'soft-beige': '#ede8e3',
        'success': '#2ecc71',
        'warning': '#f39c12',
        'error': '#e74c3c',
        'info': '#3498db',
      },
      fontFamily: {
        'space-grotesk': ['var(--font-space-grotesk)', 'sans-serif'],
        'manrope': ['var(--font-manrope)', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
