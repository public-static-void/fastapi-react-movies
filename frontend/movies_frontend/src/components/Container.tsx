import React from 'react';
import { ChildrenProps } from '../types/props';

const Container: React.FC<ChildrenProps> = ({ children }) => (
  <main className="bg-white container mx-auto my-4 p-4">{children}</main>
);

export default Container;
