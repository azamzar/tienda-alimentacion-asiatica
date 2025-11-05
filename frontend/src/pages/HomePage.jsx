import React from 'react';
import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';
import { useProductStore } from '../store/useProductStore';
import { useCartStore } from '../store/useCartStore';
import { useAuthStore } from '../store/useAuthStore';
import { formatPrice } from '../utils/formatters';
import Button from '../components/common/Button';
import Card from '../components/common/Card';
import Spinner from '../components/common/Spinner';
import PageTransition from '../components/common/PageTransition';
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

    // Si no está autenticado, mostrar mensaje y redirigir
    if (!isAuthenticated) {
      toast.error('Debes iniciar sesión para agregar productos al carrito', {
        duration: 4000,
      });
      setTimeout(() => navigate('/login'), 1500);
      return;
    }

    try {
      setAddingProductId(product.id);
      await addItem(product.id, 1);
      toast.success(`${product.name} añadido al carrito`, {
        icon: '🛒',
      });
    } catch (error) {
      console.error('Error adding to cart:', error);
      toast.error(error.response?.data?.detail || 'Error al agregar al carrito');
    } finally {
      setAddingProductId(null);
    }
  };

  return (
    <PageTransition>
      <div className="home-page">
        {/* Hero section */}
        <motion.section
          className="home-hero"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
        >
          <div className="home-hero-content">
            <motion.h1
              className="home-hero-title"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
            >
              Bienvenido a Asia Market
            </motion.h1>
            <motion.p
              className="home-hero-description"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.3 }}
            >
              Descubre los mejores productos asiáticos. Auténticos, frescos y de la mejor calidad.
            </motion.p>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.4 }}
            >
              <Link to="/products">
                <Button variant="primary" size="large">
                  Ver productos
                </Button>
              </Link>
            </motion.div>
          </div>
        </motion.section>

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
            <motion.div
              className="home-featured-grid"
              initial="hidden"
              animate="visible"
              variants={{
                visible: {
                  transition: {
                    staggerChildren: 0.1,
                  },
                },
              }}
            >
              {featuredProducts.map((product, index) => (
                <motion.div
                  key={product.id}
                  variants={{
                    hidden: { opacity: 0, y: 30 },
                    visible: {
                      opacity: 1,
                      y: 0,
                      transition: {
                        duration: 0.5,
                        ease: [0.4, 0, 0.2, 1],
                      },
                    },
                  }}
                  whileHover={{
                    y: -8,
                    transition: { duration: 0.3 },
                  }}
                >
                  <Card hoverable className="home-product-card">
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
                </motion.div>
              ))}
            </motion.div>
          )}
        </div>
      </section>

        {/* Features section */}
        <motion.section
          className="home-features"
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          variants={{
            visible: {
              transition: {
                staggerChildren: 0.15,
              },
            },
          }}
        >
          <div className="home-features-container">
            <motion.div
              className="home-feature"
              variants={{
                hidden: { opacity: 0, y: 30 },
                visible: {
                  opacity: 1,
                  y: 0,
                  transition: { duration: 0.5 },
                },
              }}
            >
              <div className="home-feature-icon">🚚</div>
              <h3 className="home-feature-title">Envío Rápido</h3>
              <p className="home-feature-description">
                Entrega en 24-48h en toda España
              </p>
            </motion.div>
            <motion.div
              className="home-feature"
              variants={{
                hidden: { opacity: 0, y: 30 },
                visible: {
                  opacity: 1,
                  y: 0,
                  transition: { duration: 0.5 },
                },
              }}
            >
              <div className="home-feature-icon">✨</div>
              <h3 className="home-feature-title">Productos Auténticos</h3>
              <p className="home-feature-description">
                Importados directamente desde Asia
              </p>
            </motion.div>
            <motion.div
              className="home-feature"
              variants={{
                hidden: { opacity: 0, y: 30 },
                visible: {
                  opacity: 1,
                  y: 0,
                  transition: { duration: 0.5 },
                },
              }}
            >
              <div className="home-feature-icon">💳</div>
              <h3 className="home-feature-title">Pago Seguro</h3>
              <p className="home-feature-description">
                Transacciones 100% seguras
              </p>
            </motion.div>
          </div>
        </motion.section>
      </div>
    </PageTransition>
  );
}

export default HomePage;
