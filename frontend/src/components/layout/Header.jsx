import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../../store/useAuthStore';
import { useCartStore } from '../../store/useCartStore';
import Button from '../common/Button';
import './Header.css';

/**
 * Main header component with navigation and user menu
 */
function Header() {
  const navigate = useNavigate();
  const { user, isAuthenticated, logout } = useAuthStore();
  const { totalItems } = useCartStore();

  const handleLogout = async () => {
    await logout();
    navigate('/');
  };

  return (
    <header className="header">
      <div className="header-container">
        {/* Logo */}
        <Link to="/" className="header-logo">
          <span className="header-logo-icon">🍜</span>
          <span className="header-logo-text">Asia Market</span>
        </Link>

        {/* Navigation */}
        <nav className="header-nav">
          <Link to="/" className="header-nav-link">
            Inicio
          </Link>
          <Link to="/products" className="header-nav-link">
            Productos
          </Link>
          {isAuthenticated && user?.role === 'admin' && (
            <Link to="/admin" className="header-nav-link">
              Admin
            </Link>
          )}
        </nav>

        {/* Actions */}
        <div className="header-actions">
          {/* Cart */}
          <Link to="/cart" className="header-cart-btn">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <circle cx="9" cy="21" r="1"></circle>
              <circle cx="20" cy="21" r="1"></circle>
              <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
            </svg>
            {totalItems > 0 && <span className="header-cart-badge">{totalItems}</span>}
          </Link>

          {/* User menu */}
          {isAuthenticated ? (
            <div className="header-user-menu">
              <button className="header-user-btn">
                <span className="header-user-icon">
                  {user?.full_name?.charAt(0).toUpperCase() || user?.email?.charAt(0).toUpperCase() || 'U'}
                </span>
                <span className="header-user-name">
                  {user?.full_name || user?.email?.split('@')[0] || 'Usuario'}
                </span>
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <polyline points="6 9 12 15 18 9"></polyline>
                </svg>
              </button>

              <div className="header-dropdown">
                <Link to="/orders" className="header-dropdown-item">
                  Mis Pedidos
                </Link>
                {user?.role === 'admin' && (
                  <>
                    <hr className="header-dropdown-divider" />
                    <Link to="/admin" className="header-dropdown-item">
                      Panel Admin
                    </Link>
                    <Link to="/admin/products" className="header-dropdown-item">
                      Gestión de Productos
                    </Link>
                    <Link to="/admin/categories" className="header-dropdown-item">
                      Gestión de Categorías
                    </Link>
                    <Link to="/admin/orders" className="header-dropdown-item">
                      Gestión de Pedidos
                    </Link>
                  </>
                )}
                <hr className="header-dropdown-divider" />
                <button onClick={handleLogout} className="header-dropdown-item header-dropdown-logout">
                  Cerrar Sesión
                </button>
              </div>
            </div>
          ) : (
            <div className="header-auth-buttons">
              <Button variant="ghost" size="small" onClick={() => navigate('/login')}>
                Iniciar Sesión
              </Button>
              <Button variant="primary" size="small" onClick={() => navigate('/register')}>
                Registrarse
              </Button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}

export default Header;
