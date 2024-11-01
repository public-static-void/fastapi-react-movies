import React from 'react';
import { TitleChildrenProps } from '../types/props';

const MovieSection: React.FC<TitleChildrenProps> = ({ children, title }) => (
  <section className="p-2 border-2 border-solid rounded-xl border-gray-400 dark:border-gray-600">
    <div className="p-2 my-2 border border-solid rounded-lg border-gray-400 dark:border-gray-600">
      <h2 className="text-center text-2xl font-bold text-gray-900 dark:text-gray-100">{title}</h2>
    </div>
    <div className="p-2 my-2 border border-solid rounded-lg border-gray-400 dark:border-gray-600">
      {children}
    </div>
  </section>
);

export default MovieSection;
