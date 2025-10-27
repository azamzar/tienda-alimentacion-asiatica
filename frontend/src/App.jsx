import React, { useEffect } from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { useAuthStore } from './store/useAuthStore';
import { useCartStore } from './store/useCartStore';
import Header from './components/layout/Header';
import Footer from './components/layout/Footer';
import AppRouter from './routes/AppRouter';
import Spinner from './components/common/Spinner';
import './App.css';

/**
 * Main App component
 * Sets up routing, layout, and initializes stores
 */
function App() {
  const { checkAuth, isLoading } = useAuthStore();
  const { initializeUserId } = useCartStore();

  // Check authentication and initialize cart on app load
  useEffect(() => {
    checkAuth();
    initializeUserId();
  }, []);

  // Show loading while checking authentication
  if (isLoading) {
    return (
      <div className="app-loading">
        <Spinner size="large" centered text="Cargando aplicación..." />
      </div>
    );
  }

  return (
    <Router>
      <div className="app">
        <Header />
        <main className="app-main">
          <AppRouter />
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
