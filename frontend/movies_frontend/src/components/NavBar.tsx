import NavLink from './NavLink';
import { RootState } from '../state/store';
import { toggleTheme, setTheme } from '../state/ThemeSlice';
import { useDispatch, useSelector } from 'react-redux';
import { useEffect } from 'react';

const NavBar = () => {
  const dispatch = useDispatch();
  const isDarkMode = useSelector((state: RootState) => state.theme.isDarkMode);
  useEffect(() => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
      dispatch(setTheme(savedTheme));
    }
    document.documentElement.classList.toggle('dark', isDarkMode);
  }, [isDarkMode, dispatch]);
  return (
    <nav className="flex justify-center items-center my-4 mx-8">
      <div>
        <NavLink title="Main" href="/" />
        <NavLink title="Admin" href="/admin" />
      </div>
      <button
        onClick={() => dispatch(toggleTheme())}
        className="nav-bar-button"
      >
        {isDarkMode ? 'Light Mode' : 'Dark Mode'}
      </button>
    </nav>
  );
};

export default NavBar;
