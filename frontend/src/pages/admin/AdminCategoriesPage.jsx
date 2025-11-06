import React, { useState, useEffect } from 'react';
import toast from 'react-hot-toast';
import { categoryService } from '../../services/categoryService';
import AdminCategoryTable from '../../components/admin/AdminCategoryTable';
import CategoryFormModal from '../../components/admin/CategoryFormModal';
import BulkActionsToolbar from '../../components/admin/BulkActionsToolbar';
import Modal from '../../components/common/Modal';
import Button from '../../components/common/Button';
import './AdminCategoriesPage.css';

/**
 * Página de gestión de categorías para administradores
 */
const AdminCategoriesPage = () => {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isFormModalOpen, setIsFormModalOpen] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [categoryToDelete, setCategoryToDelete] = useState(null);
  const [formLoading, setFormLoading] = useState(false);

  // Bulk operations state
  const [selectedIds, setSelectedIds] = useState([]);

  // Cargar categorías
  const fetchCategories = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await categoryService.getCategories();
      setCategories(data);
    } catch (err) {
      console.error('Error al cargar categorías:', err);
      setError(err.response?.data?.detail || 'Error al cargar las categorías');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCategories();
  }, []);

  // Selection handlers
  const handleSelectAll = (checked) => {
    if (checked) {
      setSelectedIds(categories.map((cat) => cat.id));
    } else {
      setSelectedIds([]);
    }
  };

  const handleSelectOne = (id, checked) => {
    if (checked) {
      setSelectedIds((prev) => [...prev, id]);
    } else {
      setSelectedIds((prev) => prev.filter((selectedId) => selectedId !== id));
    }
  };

  const handleClearSelection = () => {
    setSelectedIds([]);
  };

  // Bulk delete handler
  const handleBulkDelete = async () => {
    if (selectedIds.length === 0) return;

    const confirmed = window.confirm(
      `¿Estás seguro de que quieres eliminar ${selectedIds.length} categoría(s)?\n\n⚠️ Esta acción no se puede deshacer. Los productos asociados a estas categorías quedarán sin categoría.`
    );

    if (!confirmed) return;

    const loadingToast = toast.loading(`Eliminando ${selectedIds.length} categoría(s)...`);

    try {
      const result = await categoryService.bulkDeleteCategories(selectedIds);

      toast.dismiss(loadingToast);

      if (result.error_count > 0) {
        toast.error(
          `Eliminadas ${result.success_count} de ${result.total} categorías. ${result.error_count} errores.`,
          { duration: 5000 }
        );
      } else {
        toast.success(`${result.success_count} categoría(s) eliminadas exitosamente`, {
          icon: '🗑️',
        });
      }

      setSelectedIds([]);
      await fetchCategories();
    } catch (error) {
      toast.dismiss(loadingToast);
      console.error('Error en eliminación masiva:', error);
      toast.error(error.response?.data?.detail || 'Error al eliminar las categorías');
    }
  };

  // Abrir modal para crear
  const handleCreate = () => {
    setSelectedCategory(null);
    setIsFormModalOpen(true);
  };

  // Abrir modal para editar
  const handleEdit = (category) => {
    setSelectedCategory(category);
    setIsFormModalOpen(true);
  };

  // Crear o actualizar categoría
  const handleSubmit = async (formData) => {
    setFormLoading(true);
    try {
      if (selectedCategory) {
        // Actualizar
        await categoryService.updateCategory(selectedCategory.id, formData);
      } else {
        // Crear
        await categoryService.createCategory(formData);
      }
      await fetchCategories();
      setIsFormModalOpen(false);
      setSelectedCategory(null);
    } catch (err) {
      console.error('Error al guardar categoría:', err);
      alert(err.response?.data?.detail || 'Error al guardar la categoría');
    } finally {
      setFormLoading(false);
    }
  };

  // Confirmar eliminación
  const handleDeleteClick = (category) => {
    setCategoryToDelete(category);
  };

  // Eliminar categoría
  const handleDeleteConfirm = async () => {
    if (!categoryToDelete) return;

    try {
      await categoryService.deleteCategory(categoryToDelete.id);
      await fetchCategories();
      setCategoryToDelete(null);
    } catch (err) {
      console.error('Error al eliminar categoría:', err);
      alert(err.response?.data?.detail || 'Error al eliminar la categoría');
    }
  };

  return (
    <div className="admin-categories-page">
      <div className="page-header">
        <div className="header-content">
          <h1>Gestión de Categorías</h1>
          <p className="subtitle">Administra las categorías de productos de la tienda</p>
        </div>
        <div className="header-actions">
          <Button onClick={fetchCategories} variant="ghost" disabled={loading}>
            {loading ? 'Actualizando...' : 'Actualizar'}
          </Button>
          <Button onClick={handleCreate} variant="primary">
            Nueva Categoría
          </Button>
        </div>
      </div>

      {/* Estadísticas */}
      <div className="categories-stats">
        <div className="stat-card">
          <div className="stat-value">{categories.length}</div>
          <div className="stat-label">Total Categorías</div>
        </div>
        <div className="stat-card stat-blue">
          <div className="stat-value">
            {categories.filter((c) => c.description).length}
          </div>
          <div className="stat-label">Con Descripción</div>
        </div>
        <div className="stat-card stat-gray">
          <div className="stat-value">
            {categories.filter((c) => !c.description).length}
          </div>
          <div className="stat-label">Sin Descripción</div>
        </div>
      </div>

      {/* Bulk Actions Toolbar */}
      {selectedIds.length > 0 && (
        <BulkActionsToolbar
          selectedCount={selectedIds.length}
          onBulkDelete={handleBulkDelete}
          onClearSelection={handleClearSelection}
          showUpdateButton={false}
        />
      )}

      {/* Error */}
      {error && (
        <div className="error-message">
          <p>{error}</p>
          <Button onClick={fetchCategories}>Reintentar</Button>
        </div>
      )}

      {/* Tabla de categorías */}
      {!error && (
        <AdminCategoryTable
          categories={categories}
          onEdit={handleEdit}
          onDelete={handleDeleteClick}
          loading={loading}
          selectedIds={selectedIds}
          onSelectAll={handleSelectAll}
          onSelectOne={handleSelectOne}
        />
      )}

      {/* Modal de formulario */}
      <CategoryFormModal
        isOpen={isFormModalOpen}
        onClose={() => {
          setIsFormModalOpen(false);
          setSelectedCategory(null);
        }}
        category={selectedCategory}
        onSubmit={handleSubmit}
        loading={formLoading}
      />

      {/* Modal de confirmación de eliminación */}
      {categoryToDelete && (
        <Modal
          isOpen={!!categoryToDelete}
          onClose={() => setCategoryToDelete(null)}
          title="Confirmar Eliminación"
        >
          <div className="delete-confirmation">
            <p>
              ¿Estás seguro de que quieres eliminar la categoría{' '}
              <strong>{categoryToDelete.name}</strong>?
            </p>
            <p className="warning-text">
              ⚠️ Esta acción no se puede deshacer. Los productos asociados a esta categoría
              quedarán sin categoría.
            </p>
            <div className="modal-actions">
              <Button variant="ghost" onClick={() => setCategoryToDelete(null)}>
                Cancelar
              </Button>
              <Button variant="danger" onClick={handleDeleteConfirm}>
                Eliminar
              </Button>
            </div>
          </div>
        </Modal>
      )}
    </div>
  );
};

export default AdminCategoriesPage;
