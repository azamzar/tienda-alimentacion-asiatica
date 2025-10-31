import React, { useState } from 'react';
import { productService } from '../../services/productService';
import { formatPrice, getImageUrl } from '../../utils/formatters';
import Button from '../common/Button';
import Modal from '../common/Modal';
import './ProductTable.css';

/**
 * Product Table Component
 * Displays products in a table with edit and delete actions
 */
function ProductTable({ products, onEdit, onRefresh }) {
  const [deletingProduct, setDeletingProduct] = useState(null);
  const [isDeleting, setIsDeleting] = useState(false);
  const [deleteError, setDeleteError] = useState(null);

  // Handle delete confirmation
  const handleDeleteClick = (product) => {
    setDeletingProduct(product);
    setDeleteError(null);
  };

  // Handle delete cancel
  const handleDeleteCancel = () => {
    setDeletingProduct(null);
    setDeleteError(null);
  };

  // Handle delete confirm
  const handleDeleteConfirm = async () => {
    if (!deletingProduct) return;

    setIsDeleting(true);
    setDeleteError(null);

    try {
      await productService.deleteProduct(deletingProduct.id);
      setDeletingProduct(null);
      onRefresh(); // Refresh the product list
    } catch (error) {
      console.error('Error deleting product:', error);
      setDeleteError(
        error.response?.data?.detail || 'Error al eliminar el producto'
      );
    } finally {
      setIsDeleting(false);
    }
  };

  // Get stock status class
  const getStockStatusClass = (stock) => {
    if (stock === 0) return 'stock-out';
    if (stock < 10) return 'stock-low';
    return 'stock-ok';
  };

  // Get stock status text
  const getStockStatusText = (stock) => {
    if (stock === 0) return 'Sin stock';
    if (stock < 10) return 'Stock bajo';
    return 'Disponible';
  };

  if (products.length === 0) {
    return null;
  }

  return (
    <>
      <div className="product-table-container">
        <table className="product-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Imagen</th>
              <th>Nombre</th>
              <th>Categoría</th>
              <th>Precio</th>
              <th>Stock</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {products.map((product) => (
              <tr key={product.id}>
                <td className="product-id">{product.id}</td>
                <td className="product-image">
                  <img
                    src={getImageUrl(product.image_url)}
                    alt={product.name}
                    className="product-thumbnail"
                    onError={(e) => {
                      e.target.style.display = 'none';
                      e.target.nextSibling.style.display = 'flex';
                    }}
                  />
                  <div className="product-thumbnail-placeholder" style={{ display: 'none' }}>
                    Sin imagen
                  </div>
                </td>
                <td className="product-name">
                  <div className="product-name-cell">
                    <span className="name">{product.name}</span>
                    {product.description && (
                      <span className="description">
                        {product.description.length > 60
                          ? `${product.description.substring(0, 60)}...`
                          : product.description}
                      </span>
                    )}
                  </div>
                </td>
                <td className="product-category">
                  {product.category?.name || 'Sin categoría'}
                </td>
                <td className="product-price">{formatPrice(product.price)}</td>
                <td className="product-stock">
                  <span className={`stock-badge ${getStockStatusClass(product.stock)}`}>
                    {product.stock}
                  </span>
                </td>
                <td className="product-status">
                  <span className={`status-badge ${getStockStatusClass(product.stock)}`}>
                    {getStockStatusText(product.stock)}
                  </span>
                </td>
                <td className="product-actions">
                  <div className="action-buttons">
                    <Button
                      variant="secondary"
                      size="small"
                      onClick={() => onEdit(product)}
                    >
                      Editar
                    </Button>
                    <Button
                      variant="danger"
                      size="small"
                      onClick={() => handleDeleteClick(product)}
                    >
                      Eliminar
                    </Button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Delete Confirmation Modal */}
      {deletingProduct && (
        <Modal
          isOpen={true}
          onClose={handleDeleteCancel}
          title="Confirmar eliminación"
        >
          <div className="delete-confirmation">
            <p>
              ¿Estás seguro de que quieres eliminar el producto{' '}
              <strong>{deletingProduct.name}</strong>?
            </p>
            <p className="warning-text">
              Esta acción no se puede deshacer.
            </p>

            {deleteError && (
              <div className="delete-error">
                <p>{deleteError}</p>
              </div>
            )}

            <div className="modal-actions">
              <Button
                variant="ghost"
                onClick={handleDeleteCancel}
                disabled={isDeleting}
              >
                Cancelar
              </Button>
              <Button
                variant="danger"
                onClick={handleDeleteConfirm}
                disabled={isDeleting}
              >
                {isDeleting ? 'Eliminando...' : 'Eliminar'}
              </Button>
            </div>
          </div>
        </Modal>
      )}
    </>
  );
}

export default ProductTable;
