import React from 'react';
import { NameTitleChildrenProps } from '../types/props';

const ActorSelectorList: React.FC<NameTitleChildrenProps> = ({
  children,
  title,
  name,
}) => (
  <div className="m-2 w-1/2">
    <div>
      <h3 className="font-bold text-center text-lg text-gray-900 dark:text-gray-100">
        <label htmlFor={name}>{title}</label>
      </h3>
    </div>

    <div>{children}</div>
  </div>
);

export default ActorSelectorList;
