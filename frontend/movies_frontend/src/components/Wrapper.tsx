import React from 'react';
import { Provider } from 'react-redux';
import { store } from '../state/store';
import { ChildrenProps } from '../types/props';

const Wrapper: React.FC<ChildrenProps> = ({ children }) => (
  <Provider store={store}>{children}</Provider>
);

export default Wrapper;
