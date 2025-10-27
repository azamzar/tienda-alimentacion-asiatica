import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuthStore } from '../store';

/**
 * Componente para proteger rutas que requieren rol de administrador
 * Redirige a /login si no está autenticado
 * Redirige a / si no es administrador
 */
function AdminRoute({ children }) {
  const { isAuthenticated, isAdmin } = useAuthStore();

  if (!isAuthenticated) {
    // Redirigir a login si no está autenticado
    return <Navigate to="/login" replace />;
  }

  if (!isAdmin()) {
    // Redirigir al home si no es administrador
    return <Navigate to="/" replace />;
  }

  // Si es admin, renderizar el contenido
  return children;
}

export default AdminRoute;
