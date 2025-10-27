import React from 'react';
import { Link } from 'react-router-dom';
import Button from '../components/common/Button';
import './NotFoundPage.css';

/**
 * 404 Not Found page
 */
function NotFoundPage() {
  return (
    <div className="not-found-page">
      <div className="not-found-content">
        <h1 className="not-found-title">404</h1>
        <h2 className="not-found-subtitle">Página no encontrada</h2>
        <p className="not-found-description">
          Lo sentimos, la página que buscas no existe o ha sido movida.
        </p>
        <Link to="/">
          <Button variant="primary" size="large">
            Volver al inicio
          </Button>
        </Link>
      </div>
    </div>
  );
}

export default NotFoundPage;
