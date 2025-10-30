import React from 'react';
import Button from '../common/Button';
import { formatDate } from '../../utils/formatters';
import './AdminCategoryTable.css';

/**
 * Tabla de categorías para administradores
 */
const AdminCategoryTable = ({ categories, onEdit, onDelete, loading }) => {
  if (loading) {
    return (
      <div className="admin-category-table-loading">
        <div className="spinner"></div>
        <p>Cargando categorías...</p>
      </div>
    );
  }

  if (!categories || categories.length === 0) {
    return (
      <div className="admin-category-table-empty">
        <p>No hay categorías registradas</p>
        <p className="empty-subtitle">Crea la primera categoría para comenzar</p>
      </div>
    );
  }

  return (
    <div className="admin-category-table-container">
      {/* Desktop table */}
      <div className="admin-category-table-wrapper">
        <table className="admin-category-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Nombre</th>
              <th>Descripción</th>
              <th>Fecha de Creación</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {categories.map((category) => (
              <tr key={category.id}>
                <td className="category-id">#{category.id}</td>
                <td className="category-name">{category.name}</td>
                <td className="category-description">
                  {category.description || <span className="no-description">Sin descripción</span>}
                </td>
                <td className="category-date">{formatDate(category.created_at)}</td>
                <td className="category-actions">
                  <div className="action-buttons">
                    <Button variant="ghost" size="sm" onClick={() => onEdit(category)}>
                      Editar
                    </Button>
                    <Button variant="danger" size="sm" onClick={() => onDelete(category)}>
                      Eliminar
                    </Button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Mobile cards */}
      <div className="admin-category-cards">
        {categories.map((category) => (
          <div key={category.id} className="admin-category-card">
            <div className="category-card-header">
              <div className="category-card-title">
                <span className="category-card-id">#{category.id}</span>
                <h3 className="category-card-name">{category.name}</h3>
              </div>
            </div>

            <div className="category-card-body">
              <div className="category-card-row">
                <span className="label">Descripción:</span>
                <span className="value">
                  {category.description || (
                    <span className="no-description">Sin descripción</span>
                  )}
                </span>
              </div>
              <div className="category-card-row">
                <span className="label">Fecha de creación:</span>
                <span className="value">{formatDate(category.created_at)}</span>
              </div>
            </div>

            <div className="category-card-actions">
              <Button variant="ghost" onClick={() => onEdit(category)}>
                Editar
              </Button>
              <Button variant="danger" onClick={() => onDelete(category)}>
                Eliminar
              </Button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AdminCategoryTable;
