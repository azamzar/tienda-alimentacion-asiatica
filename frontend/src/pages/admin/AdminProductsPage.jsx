import React, { useState, useEffect } from 'react';
import { useProductStore } from '../../store/useProductStore';
import ProductTable from '../../components/admin/ProductTable';
import ProductFormModal from '../../components/admin/ProductFormModal';
import Button from '../../components/common/Button';
import Input from '../../components/common/Input';
import Spinner from '../../components/common/Spinner';
import './AdminProductsPage.css';

/**
 * Admin Products Management Page
 * Allows admins to view, create, edit, and delete products
 */
function AdminProductsPage() {
  const {
    products,
    categories,
    loading,
    error,
    fetchProducts,
    fetchCategories,
    searchProducts,
    clearFilters,
  } = useProductStore();

  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingProduct, setEditingProduct] = useState(null);

  // Load products and categories on mount
  useEffect(() => {
    fetchProducts();
    fetchCategories();
  }, []);

  // Handle search
  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      searchProducts(searchQuery);
    } else {
      fetchProducts();
    }
  };

  // Handle category filter
  const handleCategoryFilter = (categoryId) => {
    setSelectedCategory(categoryId);
    if (categoryId) {
      fetchProducts({ category_id: categoryId });
    } else {
      fetchProducts();
    }
  };

  // Handle clear filters
  const handleClearFilters = () => {
    setSearchQuery('');
    setSelectedCategory('');
    clearFilters();
    fetchProducts();
  };

  // Handle create new product
  const handleCreateProduct = () => {
    setEditingProduct(null);
    setIsModalOpen(true);
  };

  // Handle edit product
  const handleEditProduct = (product) => {
    setEditingProduct(product);
    setIsModalOpen(true);
  };

  // Handle modal close
  const handleModalClose = () => {
    setIsModalOpen(false);
    setEditingProduct(null);
  };

  // Handle product saved (created or updated)
  const handleProductSaved = () => {
    setIsModalOpen(false);
    setEditingProduct(null);
    // Refresh products list
    if (selectedCategory) {
      fetchProducts({ category_id: selectedCategory });
    } else if (searchQuery) {
      searchProducts(searchQuery);
    } else {
      fetchProducts();
    }
  };

  return (
    <div className="admin-products-page">
      <div className="admin-products-header">
        <h1>Gestión de Productos</h1>
        <Button variant="primary" onClick={handleCreateProduct}>
          + Nuevo Producto
        </Button>
      </div>

      {/* Filters Section */}
      <div className="admin-products-filters">
        <form onSubmit={handleSearch} className="search-form">
          <Input
            type="text"
            placeholder="Buscar productos..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          <Button type="submit" variant="secondary">
            Buscar
          </Button>
        </form>

        <div className="category-filter">
          <label htmlFor="category-select">Categoría:</label>
          <select
            id="category-select"
            value={selectedCategory}
            onChange={(e) => handleCategoryFilter(e.target.value)}
            className="category-select"
          >
            <option value="">Todas las categorías</option>
            {categories.map((category) => (
              <option key={category.id} value={category.id}>
                {category.name}
              </option>
            ))}
          </select>
        </div>

        {(searchQuery || selectedCategory) && (
          <Button variant="ghost" onClick={handleClearFilters}>
            Limpiar filtros
          </Button>
        )}
      </div>

      {/* Error Message */}
      {error && (
        <div className="error-message">
          <p>{error}</p>
        </div>
      )}

      {/* Loading State */}
      {loading && (
        <div className="loading-container">
          <Spinner size="large" centered text="Cargando productos..." />
        </div>
      )}

      {/* Products Table */}
      {!loading && !error && (
        <ProductTable
          products={products}
          onEdit={handleEditProduct}
          onRefresh={() => fetchProducts()}
        />
      )}

      {/* Empty State */}
      {!loading && !error && products.length === 0 && (
        <div className="empty-state">
          <p>No se encontraron productos</p>
          <Button variant="primary" onClick={handleCreateProduct}>
            Crear primer producto
          </Button>
        </div>
      )}

      {/* Product Form Modal */}
      {isModalOpen && (
        <ProductFormModal
          product={editingProduct}
          categories={categories}
          onClose={handleModalClose}
          onSave={handleProductSaved}
        />
      )}
    </div>
  );
}

export default AdminProductsPage;
