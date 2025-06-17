/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        brass: '#b08d57',
        bronze: '#cd7f32',
        verdigris: '#40a497',
        oxidizedCopper: '#7c785a',
        burgundy: '#4b0000',
        plum: '#580f41',
        inkyBlack: '#0a0a0a',
        neonTurquoise: '#40e0d0',
        neonMagenta: '#ff00ff',
        radiationGreen: '#39ff14',
        bone: '#e3dac9',
        pumice: '#bfb8a5',
        sepia: '#704214',
      },
      fontFamily: {
        header: ['"Cinzel Decorative"', 'serif'],
        typewriter: ['"Courier New"', 'Courier', 'monospace'],
        terminal: ['VT323', 'monospace'],
        bodyMono: ['Fira Mono', 'monospace'],
      },
      animation: {
        flicker: 'flickerAnimation 3s infinite',
        typing: 'typing 2s steps(30, end) forwards',
      },
      keyframes: {
        flickerAnimation: {
          '0%, 19%, 21%, 23%, 25%, 54%, 56%, 100%': { opacity: 1 },
          '20%, 22%, 24%, 55%': { opacity: 0.4 },
        },
        typing: {
          from: { width: 0 },
          to: { width: '100%' },
        },
      },
    },
  },
  plugins: [],
}
