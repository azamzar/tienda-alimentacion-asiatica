import React from 'react';
import ProductCardSkeleton from './ProductCardSkeleton';
import './ProductGridSkeleton.css';

/**
 * Skeleton loader for ProductGrid component
 * Displays a grid of placeholder cards while products are loading
 *
 * @param {Object} props
 * @param {number} props.count - Number of skeleton cards to display (default: 8)
 */
const ProductGridSkeleton = ({ count = 8 }) => {
  return (
    <div className="product-grid-skeleton">
      {Array.from({ length: count }).map((_, index) => (
        <ProductCardSkeleton key={index} />
      ))}
    </div>
  );
};

export default ProductGridSkeleton;
