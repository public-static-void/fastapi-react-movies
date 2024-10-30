import { BroadcastChannel } from 'worker_threads';
// eslint-disable-next-line @typescript-eslint/no-explicit-any, @typescript-eslint/no-unsafe-member-access
(global as any).BroadcastChannel = BroadcastChannel;

import { TransformStream } from 'node:stream/web';
global.TransformStream = TransformStream as typeof globalThis.TransformStream;

import '@testing-library/jest-dom';
import { server } from './src/mocks/server.js';

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
