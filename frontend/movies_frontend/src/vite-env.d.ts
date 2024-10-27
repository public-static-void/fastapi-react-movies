/// <reference types="vite/types/importMeta.d.ts" />
/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_BACKEND: string;
  // add more types for env vars here
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
