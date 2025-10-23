import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store';

/**
 * Página principal (Home)
 */
function HomePage() {
  const navigate = useNavigate();
  const { user, logout, isAdmin } = useAuthStore();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1 style={styles.title}>Tienda de Alimentación Asiática</h1>
        <div style={styles.userInfo}>
          <p style={styles.welcome}>
            Bienvenido, <strong>{user?.full_name || user?.email}</strong>
          </p>
          <p style={styles.role}>
            Rol: <span style={styles.badge}>{isAdmin() ? 'Administrador' : 'Cliente'}</span>
          </p>
          <button onClick={handleLogout} style={styles.logoutButton}>
            Cerrar Sesión
          </button>
        </div>
      </div>

      <div style={styles.content}>
        <h2>Contenido de la aplicación</h2>
        <p>Aquí irá el catálogo de productos, carrito, etc.</p>

        {isAdmin() && (
          <div style={styles.adminSection}>
            <h3>Panel de Administrador</h3>
            <p>Como administrador, puedes gestionar productos y categorías.</p>
          </div>
        )}
      </div>
    </div>
  );
}

const styles = {
  container: {
    minHeight: '100vh',
    backgroundColor: '#f5f5f5'
  },
  header: {
    backgroundColor: 'white',
    padding: '20px',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
    marginBottom: '20px'
  },
  title: {
    margin: '0 0 20px 0',
    fontSize: '28px',
    color: '#333'
  },
  userInfo: {
    display: 'flex',
    alignItems: 'center',
    gap: '20px',
    flexWrap: 'wrap'
  },
  welcome: {
    margin: 0,
    fontSize: '16px',
    color: '#666'
  },
  role: {
    margin: 0,
    fontSize: '14px',
    color: '#666'
  },
  badge: {
    padding: '4px 8px',
    backgroundColor: '#007bff',
    color: 'white',
    borderRadius: '4px',
    fontSize: '12px',
    fontWeight: 'bold'
  },
  logoutButton: {
    padding: '8px 16px',
    fontSize: '14px',
    color: 'white',
    backgroundColor: '#dc3545',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    marginLeft: 'auto'
  },
  content: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '20px',
    backgroundColor: 'white',
    borderRadius: '8px',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
  },
  adminSection: {
    marginTop: '30px',
    padding: '20px',
    backgroundColor: '#e7f3ff',
    borderLeft: '4px solid #007bff',
    borderRadius: '4px'
  }
};

export default HomePage;
