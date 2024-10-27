import { ReactNode } from 'react';

export interface NavLinkProps extends TitleProps {
  href: string;
}

export interface NameTitleChildrenProps extends TitleChildrenProps {
  name: string;
}

export interface TitleChildrenProps extends ChildrenProps {
  title: string;
}

export interface TitleProps {
  title: string;
}

export interface ChildrenProps {
  children: ReactNode;
}
