import React from 'react';
import { TitleChildrenProps } from '../types/props';

const MoviePropertyFormSelector: React.FC<TitleChildrenProps> = ({
  children,
  title,
}) => (
  <div className="border border-solid rounded-lg border-gray-400 dark:border-gray-600 text-center mt-1 p-2">
    <div>
      <h3 className="font-semibold text-lg">{title}</h3>
    </div>

    <div className="flex justify-center">{children}</div>
  </div>
);

export default MoviePropertyFormSelector;
