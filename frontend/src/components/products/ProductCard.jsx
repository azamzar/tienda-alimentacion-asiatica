import React, { useState, useCallback, memo } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCartStore } from '../../store/useCartStore';
import { formatPrice } from '../../utils/formatters';
import Button from '../common/Button';
import Card from '../common/Card';
import OptimizedImage from '../common/OptimizedImage';
import './ProductCard.css';

/**
 * Product card component (optimized with React.memo)
 * Displays product information with add to cart functionality
 *
 * Optimizations:
 * - React.memo to prevent unnecessary re-renders
 * - useCallback for stable function references
 * - OptimizedImage with lazy loading
 * - Memoized computed values
 *
 * @param {Object} props
 * @param {Object} props.product - Product data
 */
const ProductCard = memo(({ product }) => {
  const navigate = useNavigate();
  const { addItem } = useCartStore();
  const [isAdding, setIsAdding] = useState(false);

  // Memoize handlers with useCallback to prevent re-renders
  const handleAddToCart = useCallback(async (e) => {
    e.stopPropagation(); // Prevent card click
    setIsAdding(true);
    try {
      await addItem(product.id, 1);
      // Success - could show a toast notification here
    } catch (error) {
      console.error('Error adding to cart:', error);
      // If not authenticated, redirect to login
      if (error.response?.status === 401) {
        alert('Debes iniciar sesión para agregar productos al carrito');
        navigate('/login');
      } else {
        alert(error.response?.data?.detail || 'Error al agregar al carrito');
      }
    } finally {
      setIsAdding(false);
    }
  }, [addItem, product.id, navigate]);

  const handleCardClick = useCallback(() => {
    navigate(`/products/${product.id}`);
  }, [navigate, product.id]);

  // Compute stock status
  const isOutOfStock = product.stock === 0;
  const isLowStock = product.stock > 0 && product.stock <= 10;

  return (
    <Card hoverable onClick={handleCardClick} className="product-card">
      {/* Image with lazy loading and optimized thumbnails */}
      <div className="product-card-image-wrapper">
        {isOutOfStock && <div className="product-card-badge product-card-badge-out">Agotado</div>}
        {isLowStock && !isOutOfStock && (
          <div className="product-card-badge product-card-badge-low">¡Últimas unidades!</div>
        )}
        <OptimizedImage
          src={product.image_url}
          productId={product.id}
          alt={product.name}
          size="medium"
          className="product-card-image"
          lazy={true}
          fallback="https://placehold.co/400x300/f0f0f0/666?text=Producto"
        />
      </div>

      {/* Content */}
      <div className="product-card-content">
        {/* Category */}
        {product.category && (
          <span className="product-card-category">{product.category.name}</span>
        )}

        {/* Name */}
        <h3 className="product-card-name">{product.name}</h3>

        {/* Description */}
        {product.description && (
          <p className="product-card-description">{product.description}</p>
        )}

        {/* Price and stock */}
        <div className="product-card-footer">
          <div className="product-card-price-wrapper">
            <span className="product-card-price">{formatPrice(product.price)}</span>
            <span className="product-card-stock">
              Stock: <strong>{product.stock}</strong>
            </span>
          </div>

          {/* Add to cart button */}
          <Button
            variant="primary"
            size="small"
            onClick={handleAddToCart}
            disabled={isOutOfStock || isAdding}
            loading={isAdding}
            className="product-card-btn"
          >
            {isOutOfStock ? 'Agotado' : 'Añadir'}
          </Button>
        </div>
      </div>
    </Card>
  );
});

// Display name for debugging
ProductCard.displayName = 'ProductCard';

export default ProductCard;
