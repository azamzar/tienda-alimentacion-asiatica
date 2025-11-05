import React from 'react';
import './BulkActionsToolbar.css';

const BulkActionsToolbar = ({ selectedCount, onBulkDelete, onBulkUpdate, onClearSelection }) => {
  if (selectedCount === 0) {
    return null;
  }

  return (
    <div className="bulk-actions-toolbar">
      <div className="bulk-actions-info">
        <span className="selection-count">
          {selectedCount} {selectedCount === 1 ? 'producto seleccionado' : 'productos seleccionados'}
        </span>
      </div>

      <div className="bulk-actions-buttons">
        <button
          className="bulk-action-btn bulk-update-btn"
          onClick={onBulkUpdate}
          title="Actualizar productos seleccionados"
        >
          Actualizar en lote
        </button>

        <button
          className="bulk-action-btn bulk-delete-btn"
          onClick={onBulkDelete}
          title="Eliminar productos seleccionados"
        >
          Eliminar seleccionados
        </button>

        <button
          className="bulk-action-btn bulk-clear-btn"
          onClick={onClearSelection}
          title="Limpiar selección"
        >
          Limpiar selección
        </button>
      </div>
    </div>
  );
};

export default BulkActionsToolbar;
