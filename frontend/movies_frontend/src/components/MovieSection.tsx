import React from 'react';
import { TitleChildrenProps } from '../types/props';

const MovieSection: React.FC<TitleChildrenProps> = ({ children, title }) => (
  <section className="border-2 border-solid border-black p-2">
    <div className="border border-solid border-red-500 p-2 my-2">
      <h2 className="text-center text-2xl font-bold">{title}</h2>
    </div>
    <div className="border border-solid border-blue-500 p-2 my-2">
      {children}
    </div>
  </section>
);

export default MovieSection;
