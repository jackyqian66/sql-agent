import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        background: '#0f172a',
        foreground: '#f8fafc',
        card: 'rgba(30, 41, 59, 0.7)',
        'card-hover': 'rgba(30, 41, 59, 0.9)',
        primary: '#3b82f6',
        secondary: '#8b5cf6',
        accent: '#06b6d4',
        muted: '#64748b',
        border: 'rgba(148, 163, 184, 0.2)',
      },
      backdropBlur: {
        xs: '2px',
      },
    },
  },
  plugins: [],
}
export default config
