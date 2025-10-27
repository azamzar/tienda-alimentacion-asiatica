import React from 'react';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCartStore } from '../../store/useCartStore';
import { formatPrice } from '../../utils/formatters';
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
    } catch (error) {
      console.error('Error adding to cart:', error);
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
          src={product.image_url || '/placeholder-product.png'}
          alt={product.name}
          className="product-card-image"
          onError={(e) => {
            e.target.src = '/placeholder-product.png';
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
