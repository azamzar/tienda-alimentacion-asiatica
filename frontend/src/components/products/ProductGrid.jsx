import React, { useEffect, useState, useMemo, useCallback } from 'react';
import { useProductStore } from '../../store/useProductStore';
import ProductCard from './ProductCard';
import ProductGridSkeleton from './ProductGridSkeleton';
import Spinner from '../common/Spinner';
import Input from '../common/Input';
import './ProductGrid.css';

/**
 * Product grid with filters and search (optimized)
 * Displays products in a responsive grid layout
 *
 * Optimizations:
 * - useMemo for expensive filtering operations
 * - useCallback for stable function references
 * - ProductGridSkeleton for better loading UX
 * - Debounced search to reduce re-renders
 */
function ProductGrid() {
  const {
    products,
    categories,
    selectedCategory,
    searchQuery,
    loading,
    error,
    fetchProducts,
    fetchCategories,
    setSelectedCategory,
    setSearchQuery,
  } = useProductStore();

  const [localSearchQuery, setLocalSearchQuery] = useState('');

  useEffect(() => {
    fetchProducts();
    fetchCategories();
  }, [fetchProducts, fetchCategories]);

  // Debounced search
  useEffect(() => {
    const timer = setTimeout(() => {
      setSearchQuery(localSearchQuery);
    }, 300);

    return () => clearTimeout(timer);
  }, [localSearchQuery, setSearchQuery]);

  // Memoize handlers with useCallback
  const handleCategoryChange = useCallback((categoryId) => {
    setSelectedCategory(categoryId);
  }, [setSelectedCategory]);

  const handleClearFilters = useCallback(() => {
    setSelectedCategory(null);
    setLocalSearchQuery('');
    setSearchQuery('');
  }, [setSelectedCategory, setSearchQuery]);

  // Memoize filtered products to avoid re-computing on every render
  const filteredProducts = useMemo(() => {
    return products.filter((product) => {
      const matchesCategory = !selectedCategory || product.category_id === selectedCategory;
      const matchesSearch =
        !searchQuery ||
        product.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        product.description?.toLowerCase().includes(searchQuery.toLowerCase());
      return matchesCategory && matchesSearch;
    });
  }, [products, selectedCategory, searchQuery]);

  // Memoize category counts to avoid recalculating on every render
  const categoryCounts = useMemo(() => {
    const counts = new Map();
    products.forEach((product) => {
      const count = counts.get(product.category_id) || 0;
      counts.set(product.category_id, count + 1);
    });
    return counts;
  }, [products]);

  // Memoize active filters check
  const hasActiveFilters = useMemo(() => {
    return !!(selectedCategory || searchQuery);
  }, [selectedCategory, searchQuery]);

  return (
    <div className="product-grid-wrapper">
      {/* Filters */}
      <aside className="product-grid-filters">
        <div className="product-grid-filters-header">
          <h2 className="product-grid-filters-title">Filtros</h2>
          {hasActiveFilters && (
            <button onClick={handleClearFilters} className="product-grid-filters-clear">
              Limpiar
            </button>
          )}
        </div>

        {/* Search */}
        <div className="product-grid-filter-section">
          <Input
            type="text"
            placeholder="Buscar productos..."
            value={localSearchQuery}
            onChange={(e) => setLocalSearchQuery(e.target.value)}
          />
        </div>

        {/* Categories */}
        <div className="product-grid-filter-section">
          <h3 className="product-grid-filter-title">Categorías</h3>
          <div className="product-grid-categories">
            <button
              className={`product-grid-category ${!selectedCategory ? 'active' : ''}`}
              onClick={() => handleCategoryChange(null)}
            >
              <span className="product-grid-category-name">Todas</span>
              <span className="product-grid-category-count">{products.length}</span>
            </button>
            {categories.map((category) => {
              const count = categoryCounts.get(category.id) || 0;
              return (
                <button
                  key={category.id}
                  className={`product-grid-category ${
                    selectedCategory === category.id ? 'active' : ''
                  }`}
                  onClick={() => handleCategoryChange(category.id)}
                >
                  <span className="product-grid-category-name">{category.name}</span>
                  <span className="product-grid-category-count">{count}</span>
                </button>
              );
            })}
          </div>
        </div>
      </aside>

      {/* Products */}
      <div className="product-grid-content">
        {/* Header */}
        <div className="product-grid-header">
          <h1 className="product-grid-title">
            {selectedCategory
              ? categories.find((c) => c.id === selectedCategory)?.name
              : 'Todos los Productos'}
          </h1>
          <p className="product-grid-count">
            {filteredProducts.length} {filteredProducts.length === 1 ? 'producto' : 'productos'}
          </p>
        </div>

        {/* Loading with skeleton */}
        {loading && <ProductGridSkeleton count={8} />}

        {/* Error */}
        {error && !loading && (
          <div className="product-grid-error">
            <p>{error}</p>
          </div>
        )}

        {/* Empty state */}
        {!loading && !error && filteredProducts.length === 0 && (
          <div className="product-grid-empty">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="64"
              height="64"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="1"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <circle cx="11" cy="11" r="8"></circle>
              <path d="m21 21-4.35-4.35"></path>
            </svg>
            <h3>No se encontraron productos</h3>
            <p>Intenta cambiar los filtros de búsqueda</p>
            {hasActiveFilters && (
              <button onClick={handleClearFilters} className="product-grid-empty-button">
                Limpiar filtros
              </button>
            )}
          </div>
        )}

        {/* Products grid */}
        {!loading && !error && filteredProducts.length > 0 && (
          <div className="product-grid">
            {filteredProducts.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default ProductGrid;
