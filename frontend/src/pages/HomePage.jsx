import React from 'react';
import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useProductStore } from '../store/useProductStore';
import { useCartStore } from '../store/useCartStore';
import { useAuthStore } from '../store/useAuthStore';
import { formatPrice } from '../utils/formatters';
import Button from '../components/common/Button';
import Card from '../components/common/Card';
import Spinner from '../components/common/Spinner';
import './HomePage.css';

/**
 * Home page with featured products
 */
function HomePage() {
  const navigate = useNavigate();
  const { products, loading, fetchProducts } = useProductStore();
  const { addItem, loading: cartLoading } = useCartStore();
  const { isAuthenticated } = useAuthStore();
  const [addingProductId, setAddingProductId] = useState(null);

  useEffect(() => {
    if (products.length === 0) {
      fetchProducts({ limit: 6 });
    }
  }, []);

  const featuredProducts = products.slice(0, 6);

  const handleAddToCart = async (e, product) => {
    e.preventDefault(); // Prevenir navegación del Link
    e.stopPropagation();

    // Si no está autenticado, redirigir a login
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    try {
      setAddingProductId(product.id);
      await addItem(product.id, 1);
    } catch (error) {
      console.error('Error adding to cart:', error);
    } finally {
      setAddingProductId(null);
    }
  };

  return (
    <div className="home-page">
      {/* Hero section */}
      <section className="home-hero">
        <div className="home-hero-content">
          <h1 className="home-hero-title">Bienvenido a Asia Market</h1>
          <p className="home-hero-description">
            Descubre los mejores productos asiáticos. Auténticos, frescos y de la mejor calidad.
          </p>
          <Link to="/products">
            <Button variant="primary" size="large">
              Ver productos
            </Button>
          </Link>
        </div>
      </section>

      {/* Featured products */}
      <section className="home-featured">
        <div className="home-featured-container">
          <div className="home-featured-header">
            <h2 className="home-featured-title">Productos Destacados</h2>
            <Link to="/products" className="home-featured-link">
              Ver todos →
            </Link>
          </div>

          {loading ? (
            <div className="home-featured-loading">
              <Spinner size="large" centered text="Cargando productos..." />
            </div>
          ) : (
            <div className="home-featured-grid">
              {featuredProducts.map((product) => (
                <Card key={product.id} hoverable className="home-product-card">
                  <Link
                    to={`/products/${product.id}`}
                    className="home-product-link"
                  >
                    <div className="home-product-image-wrapper">
                      <img
                        src={product.image_url || '/placeholder-product.png'}
                        alt={product.name}
                        className="home-product-image"
                        onError={(e) => {
                          e.target.src = '/placeholder-product.png';
                        }}
                      />
                    </div>
                    <div className="home-product-content">
                      <h3 className="home-product-name">{product.name}</h3>
                      <p className="home-product-price">{formatPrice(product.price)}</p>
                      {product.stock === 0 && (
                        <span className="home-product-stock-badge out-of-stock">
                          Sin stock
                        </span>
                      )}
                    </div>
                  </Link>
                  <div className="home-product-actions">
                    <Button
                      variant="primary"
                      fullWidth
                      onClick={(e) => handleAddToCart(e, product)}
                      disabled={product.stock === 0 || addingProductId === product.id}
                    >
                      {addingProductId === product.id ? '...' : '🛒 Añadir al carrito'}
                    </Button>
                  </div>
                </Card>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* Features section */}
      <section className="home-features">
        <div className="home-features-container">
          <div className="home-feature">
            <div className="home-feature-icon">🚚</div>
            <h3 className="home-feature-title">Envío Rápido</h3>
            <p className="home-feature-description">
              Entrega en 24-48h en toda España
            </p>
          </div>
          <div className="home-feature">
            <div className="home-feature-icon">✨</div>
            <h3 className="home-feature-title">Productos Auténticos</h3>
            <p className="home-feature-description">
              Importados directamente desde Asia
            </p>
          </div>
          <div className="home-feature">
            <div className="home-feature-icon">💳</div>
            <h3 className="home-feature-title">Pago Seguro</h3>
            <p className="home-feature-description">
              Transacciones 100% seguras
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}

export default HomePage;
