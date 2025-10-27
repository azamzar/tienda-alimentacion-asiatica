import React from 'react';
import { Link } from 'react-router-dom';
import './Footer.css';

/**
 * Footer component with links and information
 */
function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="footer">
      <div className="footer-container">
        {/* Brand section */}
        <div className="footer-section">
          <div className="footer-brand">
            <span className="footer-brand-icon">🍜</span>
            <span className="footer-brand-text">Asia Market</span>
          </div>
          <p className="footer-description">
            Tu tienda online de confianza para productos de alimentación asiática.
            Calidad y autenticidad garantizadas.
          </p>
        </div>

        {/* Quick links */}
        <div className="footer-section">
          <h3 className="footer-title">Enlaces Rápidos</h3>
          <ul className="footer-links">
            <li>
              <Link to="/" className="footer-link">
                Inicio
              </Link>
            </li>
            <li>
              <Link to="/products" className="footer-link">
                Productos
              </Link>
            </li>
            <li>
              <Link to="/cart" className="footer-link">
                Carrito
              </Link>
            </li>
            <li>
              <Link to="/orders" className="footer-link">
                Mis Pedidos
              </Link>
            </li>
          </ul>
        </div>

        {/* Customer service */}
        <div className="footer-section">
          <h3 className="footer-title">Atención al Cliente</h3>
          <ul className="footer-links">
            <li>
              <a href="#" className="footer-link">
                Preguntas Frecuentes
              </a>
            </li>
            <li>
              <a href="#" className="footer-link">
                Envíos y Devoluciones
              </a>
            </li>
            <li>
              <a href="#" className="footer-link">
                Política de Privacidad
              </a>
            </li>
            <li>
              <a href="#" className="footer-link">
                Términos y Condiciones
              </a>
            </li>
          </ul>
        </div>

        {/* Contact */}
        <div className="footer-section">
          <h3 className="footer-title">Contacto</h3>
          <ul className="footer-contact">
            <li className="footer-contact-item">
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
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                <polyline points="22,6 12,13 2,6"></polyline>
              </svg>
              <span>info@asiamarket.com</span>
            </li>
            <li className="footer-contact-item">
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
                <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
              </svg>
              <span>+34 912 345 678</span>
            </li>
            <li className="footer-contact-item">
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
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                <circle cx="12" cy="10" r="3"></circle>
              </svg>
              <span>Madrid, España</span>
            </li>
          </ul>
        </div>
      </div>

      {/* Copyright */}
      <div className="footer-bottom">
        <div className="footer-container">
          <p className="footer-copyright">
            © {currentYear} Asia Market. Todos los derechos reservados.
          </p>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
