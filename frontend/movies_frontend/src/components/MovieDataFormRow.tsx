import React from 'react';
import type { NameTitleChildrenProps } from '../types/props';

const MovieDataFormRow: React.FC<NameTitleChildrenProps> = ({
  children,
  name,
  title,
}) => (
  <div className="flex my-2">
    <div className="w-1/4 text-gray-900 dark:text-gray-100">
      <label htmlFor={name}>{title}</label>
    </div>
    <div className="w-3/4">{children}</div>
  </div>
);

export default MovieDataFormRow;
