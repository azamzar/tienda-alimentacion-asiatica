import React, { useState, useEffect } from 'react';
import toast from 'react-hot-toast';
import { useProductStore } from '../../store/useProductStore';
import { productService } from '../../services/productService';
import ProductTable from '../../components/admin/ProductTable';
import ProductFormModal from '../../components/admin/ProductFormModal';
import BulkActionsToolbar from '../../components/admin/BulkActionsToolbar';
import BulkUpdateModal from '../../components/admin/BulkUpdateModal';
import Modal from '../../components/common/Modal';
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

  // Bulk operations state
  const [selectedIds, setSelectedIds] = useState([]);
  const [isBulkUpdateModalOpen, setIsBulkUpdateModalOpen] = useState(false);
  const [isBulkDeleteModalOpen, setIsBulkDeleteModalOpen] = useState(false);
  const [bulkOperationLoading, setBulkOperationLoading] = useState(false);

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

  // Handle select all products
  const handleSelectAll = (checked) => {
    if (checked) {
      setSelectedIds(products.map(p => p.id));
    } else {
      setSelectedIds([]);
    }
  };

  // Handle select one product
  const handleSelectOne = (id, checked) => {
    if (checked) {
      setSelectedIds(prev => [...prev, id]);
    } else {
      setSelectedIds(prev => prev.filter(selectedId => selectedId !== id));
    }
  };

  // Handle clear selection
  const handleClearSelection = () => {
    setSelectedIds([]);
  };

  // Handle bulk delete
  const handleBulkDelete = () => {
    setIsBulkDeleteModalOpen(true);
  };

  // Confirm bulk delete
  const confirmBulkDelete = async () => {
    setBulkOperationLoading(true);
    try {
      const result = await productService.bulkDeleteProducts(selectedIds);

      toast.success(
        `✅ ${result.success_count} productos eliminados correctamente${result.error_count > 0 ? ` (${result.error_count} errores)` : ''}`,
        { duration: 4000 }
      );

      if (result.errors && result.errors.length > 0) {
        console.error('Bulk delete errors:', result.errors);
      }

      setSelectedIds([]);
      setIsBulkDeleteModalOpen(false);

      // Refresh products
      if (selectedCategory) {
        fetchProducts({ category_id: selectedCategory });
      } else if (searchQuery) {
        searchProducts(searchQuery);
      } else {
        fetchProducts();
      }
    } catch (error) {
      console.error('Error in bulk delete:', error);
      toast.error(error.response?.data?.detail || 'Error al eliminar productos');
    } finally {
      setBulkOperationLoading(false);
    }
  };

  // Handle bulk update
  const handleBulkUpdate = () => {
    setIsBulkUpdateModalOpen(true);
  };

  // Confirm bulk update
  const confirmBulkUpdate = async (updateData) => {
    setBulkOperationLoading(true);
    try {
      const result = await productService.bulkUpdateProducts(selectedIds, updateData);

      toast.success(
        `✅ ${result.success_count} productos actualizados correctamente${result.error_count > 0 ? ` (${result.error_count} errores)` : ''}`,
        { duration: 4000 }
      );

      if (result.errors && result.errors.length > 0) {
        console.error('Bulk update errors:', result.errors);
      }

      setSelectedIds([]);
      setIsBulkUpdateModalOpen(false);

      // Refresh products
      if (selectedCategory) {
        fetchProducts({ category_id: selectedCategory });
      } else if (searchQuery) {
        searchProducts(searchQuery);
      } else {
        fetchProducts();
      }
    } catch (error) {
      console.error('Error in bulk update:', error);
      toast.error(error.response?.data?.detail || 'Error al actualizar productos');
    } finally {
      setBulkOperationLoading(false);
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

      {/* Bulk Actions Toolbar */}
      {!loading && !error && (
        <BulkActionsToolbar
          selectedCount={selectedIds.length}
          onBulkDelete={handleBulkDelete}
          onBulkUpdate={handleBulkUpdate}
          onClearSelection={handleClearSelection}
        />
      )}

      {/* Products Table */}
      {!loading && !error && (
        <ProductTable
          products={products}
          onEdit={handleEditProduct}
          onRefresh={() => fetchProducts()}
          selectedIds={selectedIds}
          onSelectAll={handleSelectAll}
          onSelectOne={handleSelectOne}
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

      {/* Bulk Update Modal */}
      <BulkUpdateModal
        isOpen={isBulkUpdateModalOpen}
        onClose={() => setIsBulkUpdateModalOpen(false)}
        onConfirm={confirmBulkUpdate}
        selectedCount={selectedIds.length}
        categories={categories}
      />

      {/* Bulk Delete Confirmation Modal */}
      {isBulkDeleteModalOpen && (
        <Modal
          isOpen={isBulkDeleteModalOpen}
          onClose={() => setIsBulkDeleteModalOpen(false)}
          title="Confirmar eliminación masiva"
        >
          <div className="bulk-delete-modal">
            <p className="bulk-delete-warning">
              ⚠️ Estás a punto de eliminar <strong>{selectedIds.length}</strong>{' '}
              {selectedIds.length === 1 ? 'producto' : 'productos'}.
            </p>
            <p>Esta acción no se puede deshacer.</p>

            <div className="modal-actions">
              <Button
                variant="secondary"
                onClick={() => setIsBulkDeleteModalOpen(false)}
                disabled={bulkOperationLoading}
              >
                Cancelar
              </Button>
              <Button
                variant="danger"
                onClick={confirmBulkDelete}
                loading={bulkOperationLoading}
              >
                {bulkOperationLoading ? 'Eliminando...' : 'Eliminar productos'}
              </Button>
            </div>
          </div>
        </Modal>
      )}
    </div>
  );
}

export default AdminProductsPage;
