import React, { useEffect } from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { useAuthStore } from './store/useAuthStore';
import { useTheme } from './hooks/useTheme';
import Header from './components/layout/Header';
import Footer from './components/layout/Footer';
import AppRouter from './routes/AppRouter';
import Spinner from './components/common/Spinner';
import './App.css';
import './styles/theme.css';

/**
 * Main App component
 * Sets up routing, layout, and initializes stores
 */
function App() {
  const { checkAuth, isLoading } = useAuthStore();
  const { isDark } = useTheme();

  // Check authentication on app load
  useEffect(() => {
    checkAuth();
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
      <Toaster
        position="top-right"
        reverseOrder={false}
        gutter={8}
        toastOptions={{
          // Default options for all toasts
          duration: 4000,
          style: {
            background: isDark ? '#1e293b' : '#fff',
            color: isDark ? '#f1f5f9' : '#333',
            padding: '16px',
            borderRadius: '8px',
            boxShadow: isDark
              ? '0 4px 12px rgba(0, 0, 0, 0.5)'
              : '0 4px 12px rgba(0, 0, 0, 0.15)',
            maxWidth: '500px',
            border: isDark ? '1px solid #334155' : 'none',
          },
          // Success toast style
          success: {
            duration: 3000,
            iconTheme: {
              primary: '#10b981',
              secondary: isDark ? '#1e293b' : '#fff',
            },
          },
          // Error toast style
          error: {
            duration: 5000,
            iconTheme: {
              primary: '#ef4444',
              secondary: isDark ? '#1e293b' : '#fff',
            },
          },
          // Loading toast style
          loading: {
            iconTheme: {
              primary: '#3b82f6',
              secondary: isDark ? '#1e293b' : '#fff',
            },
          },
        }}
      />
    </Router>
  );
}

export default App;
