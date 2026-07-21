import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

const djangoApiUrl = process.env.VITE_API_URL || 'http://127.0.0.1:8000'

export default defineConfig({
  plugins: [react()],
  publicDir: '../html',
  server: {
    proxy: {
      '/api': {
        target: djangoApiUrl,
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
})
