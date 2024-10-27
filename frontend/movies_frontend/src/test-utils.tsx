import { render, RenderOptions } from '@testing-library/react';
import React from 'react';
import Wrapper from './components/Wrapper';

const customRender = (
  ui: React.ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
) => render(ui, { wrapper: Wrapper, ...options });

/* eslint-disable-next-line react-refresh/only-export-components */
export * from '@testing-library/react';
export { customRender as render };
