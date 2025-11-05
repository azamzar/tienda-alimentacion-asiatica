import React, { useState, useEffect } from 'react';
import Modal from '../common/Modal';
import Input from '../common/Input';
import Button from '../common/Button';
import './BulkUpdateModal.css';

const BulkUpdateModal = ({ isOpen, onClose, onConfirm, selectedCount, categories = [] }) => {
  const [formData, setFormData] = useState({
    stock: '',
    price: '',
    category_id: ''
  });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!isOpen) {
      // Reset form when modal closes
      setFormData({
        stock: '',
        price: '',
        category_id: ''
      });
    }
  }, [isOpen]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Filtrar solo los campos que tienen valor
    const updateData = {};
    if (formData.stock !== '') {
      updateData.stock = parseInt(formData.stock);
    }
    if (formData.price !== '') {
      updateData.price = parseFloat(formData.price);
    }
    if (formData.category_id !== '') {
      updateData.category_id = parseInt(formData.category_id);
    }

    // Validar que al menos un campo tenga valor
    if (Object.keys(updateData).length === 0) {
      alert('Debes ingresar al menos un campo para actualizar');
      return;
    }

    setLoading(true);
    try {
      await onConfirm(updateData);
      onClose();
    } catch (error) {
      console.error('Error al actualizar productos:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Actualizar productos en lote">
      <div className="bulk-update-modal">
        <div className="bulk-update-info">
          <p>
            Actualizarás <strong>{selectedCount}</strong> {selectedCount === 1 ? 'producto' : 'productos'}.
          </p>
          <p className="bulk-update-hint">
            Completa solo los campos que deseas actualizar. Los demás permanecerán sin cambios.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="bulk-update-form">
          <div className="form-group">
            <label htmlFor="stock">Stock</label>
            <Input
              id="stock"
              name="stock"
              type="number"
              min="0"
              placeholder="Nuevo stock (opcional)"
              value={formData.stock}
              onChange={handleChange}
            />
          </div>

          <div className="form-group">
            <label htmlFor="price">Precio (€)</label>
            <Input
              id="price"
              name="price"
              type="number"
              min="0"
              step="0.01"
              placeholder="Nuevo precio (opcional)"
              value={formData.price}
              onChange={handleChange}
            />
          </div>

          <div className="form-group">
            <label htmlFor="category_id">Categoría</label>
            <select
              id="category_id"
              name="category_id"
              value={formData.category_id}
              onChange={handleChange}
              className="bulk-update-select"
            >
              <option value="">Sin cambiar</option>
              {categories.map((category) => (
                <option key={category.id} value={category.id}>
                  {category.name}
                </option>
              ))}
            </select>
          </div>

          <div className="modal-actions">
            <Button
              type="button"
              variant="secondary"
              onClick={onClose}
              disabled={loading}
            >
              Cancelar
            </Button>
            <Button
              type="submit"
              variant="primary"
              loading={loading}
            >
              {loading ? 'Actualizando...' : 'Actualizar productos'}
            </Button>
          </div>
        </form>
      </div>
    </Modal>
  );
};

export default BulkUpdateModal;
