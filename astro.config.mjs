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
  markdown: {
    // Shiki's default github-dark ships a #24292e background, which reads
    // grey-blue against this palette. Vesper is near-black with mint/peach.
    shikiConfig: {
      theme: 'vesper',
      wrap: true
    }
  },
  vite: {
    plugins: [tailwindcss()]
  }
});