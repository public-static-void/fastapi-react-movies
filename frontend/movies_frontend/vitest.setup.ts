import '@testing-library/jest-dom/vitest';
import { server } from './src/mocks/server.js';
import { beforeAll, afterAll, afterEach } from 'vitest';

beforeAll(() => server.listen());
afterEach(() => {
  server.resetHandlers();
  document.body.innerHTML = '<div id="root"></div>';
});
afterAll(() => server.close());

declare global {
  namespace Vi {
    interface JestAssertion {
      toBeInTheDocument(): void;
    }
  }
}
