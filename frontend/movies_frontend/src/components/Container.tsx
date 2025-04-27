import React from 'react';
import type { ChildrenProps } from '../types/props';

const Container: React.FC<ChildrenProps> = ({ children }) => (
  <main className="container mx-auto my-4 p-4 rounded-xl text:gray-900 bg-slate-100 dark:text-gray-100 dark:bg-slate-900">
    {children}
  </main>
);

export default Container;
