import Container from './components/Container';
import MainPage from './pages/MainPage';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import AdminPage from './pages/AdminPage';
import NavBar from './components/NavBar';

function App() {
  return (
    <BrowserRouter>
      <Container>
        <NavBar />
        <Routes>
          <Route index path="/" element={<MainPage />}></Route>
          <Route path="/admin" element={<AdminPage />}></Route>
        </Routes>
      </Container>
    </BrowserRouter>
  );
}

export default App;
