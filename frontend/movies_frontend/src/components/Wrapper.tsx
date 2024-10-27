import React from 'react';
import { Provider } from 'react-redux';
import { createNewStore } from '../state/store';
import { ChildrenProps } from '../types/props';

const Wrapper: React.FC<ChildrenProps> = ({ children }) => (
  <Provider store={createNewStore()}>{children}</Provider>
);

export default Wrapper;
