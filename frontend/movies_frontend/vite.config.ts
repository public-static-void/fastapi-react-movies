/// <reference types="vitest" />
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';
import checker from 'vite-plugin-checker';

export default defineConfig({
  plugins: [
    react({}),
    tailwindcss(),
    checker({
      typescript: true,
      eslint: {
        lintCommand: 'eslint "./src/**/*.{ts,tsx}"',
        useFlatConfig: true,
      },
    }),
  ],

  resolve: {
    alias: { '@': '/src' },
    dedupe: ['react', 'react-dom'],
  },

  build: {
    sourcemap: false,
    chunkSizeWarningLimit: 1500,
    commonjsOptions: {
      include: [/node_modules/],
      transformMixedEsModules: true,
    },
    cssCodeSplit: true,
    rollupOptions: {
      output: {
        manualChunks: {
          react: ['react', 'react-dom'],
          router: ['react-router-dom'],
        },
      },
    },
  },

  optimizeDeps: {
    include: ['react', 'react-dom', '@testing-library/react'],
    esbuildOptions: {
      loader: {
        '.js': 'jsx',
      },
    },
  },

  test: {
    passWithNoTests: true,
    exclude: [
      '**/node_modules/**',
      '**/dist/**',
      '**/cypress/**',
      '**/.{idea,git,cache,output,temp}/**',
      '**/{karma,rollup,webpack,vite,vitest,jest,ava,babel,nyc,cypress,tsup,build}.config.*',
      '**/postcss.config.js',
      '**/tailwind.config.js',
      '**/Nav*.tsx',
      '**/Container.tsx',
      '**/*.d.ts',
    ],
    include: ['**/*.{test,spec}.{js,ts,jsx,tsx}'],
    globals: true,
    environment: 'happy-dom',
    setupFiles: './vitest.setup.ts',
    typecheck: {
      include: ['**/*.test.ts', '**/*.test.tsx'],
    },
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html', 'json-summary', 'lcov'],
      thresholds: {
        branches: 50,
        functions: 50,
        lines: 50,
        statements: 50,
      },
    },
  },
});
