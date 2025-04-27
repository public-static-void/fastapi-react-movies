import { vi } from 'vitest';
import { Formik } from 'formik';
import type { ReactNode } from 'react';
import React from 'react';
import { mainPageFormInitialValues } from '../../state/formik';

interface Props {
  children: ReactNode;
}

const MockFormikContext: React.FC<Props> = ({ children }) => (
  <Formik initialValues={mainPageFormInitialValues} onSubmit={vi.fn()}>
    {children}
  </Formik>
);

export default MockFormikContext;
