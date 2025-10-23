import { Navigate } from 'react-router-dom';
import { useAuthStore } from '../store';

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

export default ProtectedRoute;
