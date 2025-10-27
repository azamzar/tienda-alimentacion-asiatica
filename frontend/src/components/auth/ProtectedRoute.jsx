import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuthStore } from '../../store/useAuthStore';

/**
 * Componente para proteger rutas que requieren autenticación
 * Redirige a /login si el usuario no está autenticado
 */
function ProtectedRoute({ children }) {
  const { isAuthenticated } = useAuthStore();

  if (!isAuthenticated) {
    // Redirigir a login si no está autenticado
    return <Navigate to="/login" replace />;
  }

  // Si está autenticado, renderizar el contenido
  return children;
}

/**
 * Componente para proteger rutas que requieren rol de administrador
 * Redirige a / si el usuario no es admin
 */
function AdminRoute({ children }) {
  const { isAuthenticated, user } = useAuthStore();

  if (!isAuthenticated) {
    // Redirigir a login si no está autenticado
    return <Navigate to="/login" replace />;
  }

  if (user?.role !== 'admin') {
    // Redirigir a home si no es admin
    return <Navigate to="/" replace />;
  }

  // Si es admin, renderizar el contenido
  return children;
}

export { ProtectedRoute, AdminRoute };
export default ProtectedRoute;
