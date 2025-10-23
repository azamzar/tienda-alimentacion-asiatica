import { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useAuthStore } from './store';

// Pages
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';

// Components
import ProtectedRoute from './components/ProtectedRoute';

import './App.css';

function App() {
  const { checkAuth, isLoading } = useAuthStore();

  // Verificar autenticación al cargar la app
  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  // Mostrar loading mientras se verifica la autenticación
  if (isLoading) {
    return (
      <div style={styles.loading}>
        <p>Cargando...</p>
      </div>
    );
  }

  return (
    <Router>
      <Routes>
        {/* Rutas públicas */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />

        {/* Rutas protegidas (requieren autenticación) */}
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <HomePage />
            </ProtectedRoute>
          }
        />

        {/* Ruta por defecto - redirigir al home */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

const styles = {
  loading: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    minHeight: '100vh',
    fontSize: '18px',
    color: '#666'
  }
};

export default App;
