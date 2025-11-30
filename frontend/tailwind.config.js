/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'pottery-primary': '#C85A3A',
        'pottery-dark': '#4A3428',
        'pottery-light': '#F8F5F0',
        'pottery-accent': '#D4AF37',
        'pottery-terracotta': '#B84A2A',
        'pottery-ochre': '#E8A87C',
        'pottery-cream': '#FAF8F3',
      },
      fontFamily: {
        'display': ['Poppins', 'system-ui', 'sans-serif'],
        'body': ['Inter', 'system-ui', 'sans-serif'],
        'sans': ['Inter', 'system-ui', 'sans-serif'],
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128': '32rem',
      },
      borderRadius: {
        '4xl': '2rem',
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.5s ease-out',
        'scale-in': 'scaleIn 0.3s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        scaleIn: {
          '0%': { transform: 'scale(0.95)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
      },
      backdropBlur: {
        xs: '2px',
      },
    },
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: [
      {
        light: {
          ...require("daisyui/src/theming/themes")["light"],
          primary: "#C85A3A",
          "primary-focus": "#B84A2A",
          "primary-content": "#ffffff",
          secondary: "#4A3428",
          accent: "#D4AF37",
          neutral: "#3D3D3D",
          "base-100": "#FFFFFF",
          "base-200": "#F8F5F0",
          "base-300": "#F0EBE0",
          "base-content": "#1F1F1F",
        },
      },
    ],
  },
}

