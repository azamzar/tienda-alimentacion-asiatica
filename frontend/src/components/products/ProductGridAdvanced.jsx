import React, { useEffect, useState, useCallback, useMemo } from 'react';
import { productService } from '../../services/productService';
import { categoryService } from '../../services/categoryService';
import ProductCard from './ProductCard';
import ProductGridSkeleton from './ProductGridSkeleton';
import SearchAutocomplete from '../common/SearchAutocomplete';
import PriceRangeSlider from './PriceRangeSlider';
import RatingFilter from './RatingFilter';
import SortDropdown from './SortDropdown';
import './ProductGrid.css';

/**
 * ProductGridAdvanced - Product grid with advanced filters
 *
 * Features:
 * - Search with autocomplete
 * - Price range filter
 * - Rating filter
 * - Stock availability filter
 * - Sorting options
 * - Category filter
 */
const ProductGridAdvanced = () => {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Filter states
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [priceRange, setPriceRange] = useState({ min: 0, max: 100 });
  const [globalPriceRange, setGlobalPriceRange] = useState({ min: 0, max: 100 });
  const [selectedRating, setSelectedRating] = useState(null);
  const [inStockOnly, setInStockOnly] = useState(false);
  const [sortBy, setSortBy] = useState('created_at');
  const [sortOrder, setSortOrder] = useState('desc');

  // Fetch price range on mount
  useEffect(() => {
    const fetchPriceRange = async () => {
      try {
        const range = await productService.getPriceRange();
        setGlobalPriceRange(range);
        setPriceRange(range);
      } catch (error) {
        console.error('Error fetching price range:', error);
      }
    };
    fetchPriceRange();
  }, []);

  // Fetch categories
  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const data = await categoryService.getCategories();
        setCategories(data);
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    };
    fetchCategories();
  }, []);

  // Fetch products with all filters
  const fetchProducts = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const params = {
        search_query: searchQuery || undefined,
        category_id: selectedCategory || undefined,
        min_price: priceRange.min !== globalPriceRange.min ? priceRange.min : undefined,
        max_price: priceRange.max !== globalPriceRange.max ? priceRange.max : undefined,
        min_rating: selectedRating || undefined,
        in_stock_only: inStockOnly || undefined,
        sort_by: sortBy,
        sort_order: sortOrder,
        limit: 100
      };

      const data = await productService.advancedSearch(params);
      setProducts(data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al cargar productos');
    } finally {
      setLoading(false);
    }
  }, [searchQuery, selectedCategory, priceRange, selectedRating, inStockOnly, sortBy, sortOrder, globalPriceRange]);

  // Fetch products when filters change
  useEffect(() => {
    fetchProducts();
  }, [fetchProducts]);

  // Clear all filters
  const handleClearFilters = () => {
    setSearchQuery('');
    setSelectedCategory(null);
    setPriceRange(globalPriceRange);
    setSelectedRating(null);
    setInStockOnly(false);
    setSortBy('created_at');
    setSortOrder('desc');
  };

  // Check if any filter is active
  const hasActiveFilters = useMemo(() => {
    return !!(
      searchQuery ||
      selectedCategory ||
      priceRange.min !== globalPriceRange.min ||
      priceRange.max !== globalPriceRange.max ||
      selectedRating ||
      inStockOnly
    );
  }, [searchQuery, selectedCategory, priceRange, globalPriceRange, selectedRating, inStockOnly]);

  return (
    <div className="product-grid-wrapper">
      {/* Sidebar with filters */}
      <aside className="product-grid-filters">
        <div className="product-grid-filters-header">
          <h2 className="product-grid-filters-title">Filtros</h2>
          {hasActiveFilters && (
            <button
              onClick={handleClearFilters}
              className="product-grid-filters-clear"
            >
              Limpiar
            </button>
          )}
        </div>

        {/* Search with autocomplete */}
        <div className="product-grid-filter-section">
          <SearchAutocomplete
            initialValue={searchQuery}
            onSearch={setSearchQuery}
            onClear={() => setSearchQuery('')}
            placeholder="Buscar productos..."
          />
        </div>

        {/* Categories */}
        <div className="product-grid-filter-section">
          <h3 className="product-grid-filter-title">Categorías</h3>
          <div className="product-grid-categories">
            <button
              className={`product-grid-category ${!selectedCategory ? 'active' : ''}`}
              onClick={() => setSelectedCategory(null)}
            >
              <span className="product-grid-category-name">Todas</span>
            </button>
            {categories.map((category) => (
              <button
                key={category.id}
                className={`product-grid-category ${
                  selectedCategory === category.id ? 'active' : ''
                }`}
                onClick={() => setSelectedCategory(category.id)}
              >
                <span className="product-grid-category-name">{category.name}</span>
                {category.product_count !== undefined && (
                  <span className="product-grid-category-count">
                    {category.product_count}
                  </span>
                )}
              </button>
            ))}
          </div>
        </div>

        {/* Price Range Slider */}
        <div className="product-grid-filter-section">
          <PriceRangeSlider
            min={globalPriceRange.min}
            max={globalPriceRange.max}
            minValue={priceRange.min}
            maxValue={priceRange.max}
            onChange={setPriceRange}
          />
        </div>

        {/* Rating Filter */}
        <div className="product-grid-filter-section">
          <RatingFilter
            selectedRating={selectedRating}
            onChange={setSelectedRating}
          />
        </div>

        {/* Stock Filter */}
        <div className="product-grid-filter-section">
          <div className="product-grid-stock-filter">
            <label className="product-grid-checkbox-label">
              <input
                type="checkbox"
                checked={inStockOnly}
                onChange={(e) => setInStockOnly(e.target.checked)}
              />
              <span>Solo productos disponibles</span>
            </label>
          </div>
        </div>
      </aside>

      {/* Main content */}
      <div className="product-grid-content">
        {/* Header with sort */}
        <div className="product-grid-header">
          <div className="product-grid-header-info">
            <h1 className="product-grid-title">
              {selectedCategory
                ? categories.find((c) => c.id === selectedCategory)?.name
                : 'Todos los Productos'}
            </h1>
            <p className="product-grid-count">
              {products.length} {products.length === 1 ? 'producto' : 'productos'}
            </p>
          </div>

          <div className="product-grid-sort">
            <SortDropdown
              sortBy={sortBy}
              sortOrder={sortOrder}
              onChange={({ sortBy: newSortBy, sortOrder: newSortOrder }) => {
                setSortBy(newSortBy);
                setSortOrder(newSortOrder);
              }}
            />
          </div>
        </div>

        {/* Loading skeleton */}
        {loading && <ProductGridSkeleton count={8} />}

        {/* Error */}
        {error && !loading && (
          <div className="product-grid-error">
            <p>{error}</p>
            <button onClick={fetchProducts} className="product-grid-retry-button">
              Reintentar
            </button>
          </div>
        )}

        {/* Empty state */}
        {!loading && !error && products.length === 0 && (
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
        {!loading && !error && products.length > 0 && (
          <div className="product-grid">
            {products.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default ProductGridAdvanced;
