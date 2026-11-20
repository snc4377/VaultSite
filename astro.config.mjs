// @ts-check
import { defineConfig } from 'astro/config';

import tailwindcss from '@tailwindcss/vite';

// https://astro.build/config
export default defineConfig({
  // GitHub Pages project site: https://snc4377.github.io/VaultSite/
  site: 'https://snc4377.github.io',
  base: '/VaultSite',
  server: {
    host: true
  },
  vite: {
    plugins: [tailwindcss()]
  }
});