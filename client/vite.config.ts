import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import mkcert from 'vite-plugin-mkcert'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  server: {},
  plugins: [vue(), tailwindcss(), mkcert()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
