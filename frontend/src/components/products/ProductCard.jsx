import React from 'react';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCartStore } from '../../store/useCartStore';
import { formatPrice, getImageUrl } from '../../utils/formatters';
import Button from '../common/Button';
import Card from '../common/Card';
import './ProductCard.css';

/**
 * Product card component
 * Displays product information with add to cart functionality
 *
 * @param {Object} props
 * @param {Object} props.product - Product data
 */
function ProductCard({ product }) {
  const navigate = useNavigate();
  const { addItem } = useCartStore();
  const [isAdding, setIsAdding] = useState(false);

  const handleAddToCart = async (e) => {
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
  };

  const handleCardClick = () => {
    navigate(`/products/${product.id}`);
  };

  const isOutOfStock = product.stock === 0;
  const isLowStock = product.stock > 0 && product.stock <= 10;

  return (
    <Card hoverable onClick={handleCardClick} className="product-card">
      {/* Image */}
      <div className="product-card-image-wrapper">
        {isOutOfStock && <div className="product-card-badge product-card-badge-out">Agotado</div>}
        {isLowStock && !isOutOfStock && (
          <div className="product-card-badge product-card-badge-low">¡Últimas unidades!</div>
        )}
        <img
          src={getImageUrl(product.image_url)}
          alt={product.name}
          className="product-card-image"
          onError={(e) => {
            // Prevent infinite loop by checking if we've already set the placeholder
            if (!e.target.src.includes('placehold.co')) {
              e.target.src = 'https://placehold.co/400x300/f0f0f0/666?text=Producto';
            }
          }}
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
}

export default ProductCard;
