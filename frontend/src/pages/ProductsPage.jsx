import React from 'react';
import ProductGrid from '../components/products/ProductGrid';
import './ProductsPage.css';

/**
 * Products page
 * Displays all products with filters and search
 */
function ProductsPage() {
  return (
    <div className="products-page">
      <ProductGrid />
    </div>
  );
}

export default ProductsPage;
