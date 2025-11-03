import React from 'react';
import Skeleton from '../common/Skeleton';
import './ProductCardSkeleton.css';

/**
 * Skeleton loader for ProductCard component
 * Displays a placeholder while product data is loading
 */
const ProductCardSkeleton = () => {
  return (
    <div className="product-card-skeleton">
      <div className="product-card-skeleton__image">
        <Skeleton variant="rectangular" width="100%" height="100%" />
      </div>
      <div className="product-card-skeleton__content">
        <Skeleton variant="text" width="80%" height="20px" />
        <Skeleton variant="text" width="60%" height="16px" />
        <div className="product-card-skeleton__footer">
          <Skeleton variant="text" width="40%" height="24px" />
          <Skeleton variant="rectangular" width="100px" height="36px" />
        </div>
      </div>
    </div>
  );
};

export default ProductCardSkeleton;
