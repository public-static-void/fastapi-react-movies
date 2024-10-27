import { Formik } from 'formik';
import React, { ReactNode } from 'react';
import { mainPageFormInitialValues } from '../../state/formik';

interface Props {
  children: ReactNode;
}

const MockFormikContext: React.FC<Props> = ({ children }) => (
  <Formik initialValues={mainPageFormInitialValues} onSubmit={jest.fn()}>
    {children}
  </Formik>
);

export default MockFormikContext;
