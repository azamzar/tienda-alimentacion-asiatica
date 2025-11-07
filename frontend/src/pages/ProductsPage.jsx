import React from 'react';
import ProductGridAdvanced from '../components/products/ProductGridAdvanced';
import './ProductsPage.css';

/**
 * Products page with advanced filters
 * Displays all products with search, filters, and sorting
 *
 * Features:
 * - Search with autocomplete
 * - Price range filter
 * - Rating filter
 * - Stock availability filter
 * - Category filter
 * - Multiple sorting options
 */
function ProductsPage() {
  return (
    <div className="products-page">
      <ProductGridAdvanced />
    </div>
  );
}

export default ProductsPage;
