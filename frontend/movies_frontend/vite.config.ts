/// <reference types="vitest" />
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';
import checker from 'vite-plugin-checker';

const isCI = process.env.CI === 'true' || process.env.NODE_ENV === 'production';

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
    // Only enable checker in dev/CI, not in Docker production build
    !isCI &&
      checker({
        typescript: true,
        eslint: {
          lintCommand: 'eslint "./src/**/*.{ts,tsx}"',
          useFlatConfig: true,
        },
      }),
  ].filter(Boolean),

  resolve: {
    alias: { '@': '/src' },
    dedupe: ['react', 'react-dom'],
  },

  cacheDir: './node_modules/.vite',
  build: {
    emptyOutDir: true,
    sourcemap: false,
    chunkSizeWarningLimit: 1500,
    commonjsOptions: {
      include: [/node_modules/],
      transformMixedEsModules: true,
    },
    cssCodeSplit: true,
    // rollupOptions: {
    //   output: {
    //     manualChunks: {
    //       react: ['react', 'react-dom'],
    //       router: ['react-router-dom'],
    //     },
    //   },
    // },
  },

  optimizeDeps: {
    include: ['react', 'react-dom', 'react-router-dom'],
    exclude: ['msw'],
    esbuildOptions: {
      loader: { '.js': 'jsx' },
    },
  },

  esbuild: {
    jsx: 'automatic',
    jsxDev: false,
    jsxImportSource: 'react',
  },

  server: {
    watch: {
      ignored: ['**/mocks/**'],
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
    environment: 'jsdom',
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
