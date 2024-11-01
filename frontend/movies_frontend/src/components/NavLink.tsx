import { Link } from 'react-router-dom';
import { NavLinkProps } from '../types/props';

const NavLink = ({ title, href }: NavLinkProps) => (
  <Link className="nav-bar-button" to={href}>
    {title}
  </Link>
);

export default NavLink;
