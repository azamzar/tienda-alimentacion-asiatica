import React from 'react';
import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { productService } from '../services/productService';
import { useCartStore } from '../store/useCartStore';
import { formatPrice } from '../utils/formatters';
import Button from '../components/common/Button';
import Card from '../components/common/Card';
import Spinner from '../components/common/Spinner';
import './ProductDetailPage.css';

/**
 * Product detail page
 * Shows detailed information about a single product
 */
function ProductDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { addItem } = useCartStore();

  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [quantity, setQuantity] = useState(1);
  const [isAdding, setIsAdding] = useState(false);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        setLoading(true);
        const data = await productService.getProductById(id);
        setProduct(data);
      } catch (err) {
        setError(err.message || 'Error al cargar el producto');
      } finally {
        setLoading(false);
      }
    };

    fetchProduct();
  }, [id]);

  const handleAddToCart = async () => {
    setIsAdding(true);
    try {
      await addItem(product.id, quantity);
      // Optional: Show success message
    } catch (error) {
      console.error('Error adding to cart:', error);
    } finally {
      setIsAdding(false);
    }
  };

  const handleQuantityChange = (delta) => {
    const newQuantity = quantity + delta;
    if (newQuantity >= 1 && newQuantity <= product.stock) {
      setQuantity(newQuantity);
    }
  };

  if (loading) {
    return (
      <div className="product-detail-page">
        <div className="product-detail-loading">
          <Spinner size="large" centered text="Cargando producto..." />
        </div>
      </div>
    );
  }

  if (error || !product) {
    return (
      <div className="product-detail-page">
        <div className="product-detail-error">
          <Card>
            <h2>Error</h2>
            <p>{error || 'Producto no encontrado'}</p>
            <Button onClick={() => navigate('/products')}>Volver a productos</Button>
          </Card>
        </div>
      </div>
    );
  }

  const isOutOfStock = product.stock === 0;
  const isLowStock = product.stock > 0 && product.stock <= 10;

  return (
    <div className="product-detail-page">
      <div className="product-detail-container">
        {/* Back button */}
        <button className="product-detail-back" onClick={() => navigate('/products')}>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <line x1="19" y1="12" x2="5" y2="12"></line>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
          Volver a productos
        </button>

        {/* Product detail */}
        <div className="product-detail-content">
          {/* Image */}
          <div className="product-detail-image-wrapper">
            <img
              src={product.image_url || '/placeholder-product.png'}
              alt={product.name}
              className="product-detail-image"
              onError={(e) => {
                e.target.src = '/placeholder-product.png';
              }}
            />
            {isOutOfStock && (
              <div className="product-detail-badge product-detail-badge-out">Agotado</div>
            )}
            {isLowStock && !isOutOfStock && (
              <div className="product-detail-badge product-detail-badge-low">
                ¡Últimas unidades!
              </div>
            )}
          </div>

          {/* Info */}
          <div className="product-detail-info">
            {/* Category */}
            {product.category && (
              <span className="product-detail-category">{product.category.name}</span>
            )}

            {/* Name */}
            <h1 className="product-detail-name">{product.name}</h1>

            {/* Price */}
            <div className="product-detail-price">{formatPrice(product.price)}</div>

            {/* Stock */}
            <div className="product-detail-stock">
              <strong>Stock disponible:</strong>{' '}
              <span className={isLowStock ? 'text-warning' : ''}>{product.stock} unidades</span>
            </div>

            {/* Description */}
            {product.description && (
              <div className="product-detail-description">
                <h2>Descripción</h2>
                <p>{product.description}</p>
              </div>
            )}

            {/* Quantity selector */}
            {!isOutOfStock && (
              <div className="product-detail-quantity">
                <label className="product-detail-quantity-label">Cantidad:</label>
                <div className="product-detail-quantity-controls">
                  <button
                    className="product-detail-quantity-btn"
                    onClick={() => handleQuantityChange(-1)}
                    disabled={quantity <= 1}
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="20"
                      height="20"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    >
                      <line x1="5" y1="12" x2="19" y2="12"></line>
                    </svg>
                  </button>
                  <input
                    type="number"
                    className="product-detail-quantity-input"
                    value={quantity}
                    onChange={(e) => {
                      const val = parseInt(e.target.value);
                      if (val >= 1 && val <= product.stock) {
                        setQuantity(val);
                      }
                    }}
                    min="1"
                    max={product.stock}
                  />
                  <button
                    className="product-detail-quantity-btn"
                    onClick={() => handleQuantityChange(1)}
                    disabled={quantity >= product.stock}
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="20"
                      height="20"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    >
                      <line x1="12" y1="5" x2="12" y2="19"></line>
                      <line x1="5" y1="12" x2="19" y2="12"></line>
                    </svg>
                  </button>
                </div>
              </div>
            )}

            {/* Add to cart button */}
            <div className="product-detail-actions">
              <Button
                variant="primary"
                size="large"
                fullWidth
                onClick={handleAddToCart}
                disabled={isOutOfStock || isAdding}
                loading={isAdding}
              >
                {isOutOfStock ? 'Producto agotado' : 'Añadir al carrito'}
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ProductDetailPage;
