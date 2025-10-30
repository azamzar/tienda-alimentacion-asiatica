import React from 'react';
import Button from '../common/Button';
import { formatDate } from '../../utils/formatters';
import './AdminUserTable.css';

/**
 * Tabla de usuarios para administradores
 */
const AdminUserTable = ({ users, onEdit, onDelete, loading }) => {
  if (loading) {
    return (
      <div className="admin-user-table-loading">
        <div className="spinner"></div>
        <p>Cargando usuarios...</p>
      </div>
    );
  }

  if (!users || users.length === 0) {
    return (
      <div className="admin-user-table-empty">
        <p>No hay usuarios registrados</p>
        <p className="empty-subtitle">Los usuarios aparecerán aquí cuando se registren</p>
      </div>
    );
  }

  const getRoleBadgeClass = (role) => {
    return role === 'admin' ? 'role-badge role-admin' : 'role-badge role-customer';
  };

  const getStatusBadgeClass = (isActive) => {
    return isActive ? 'status-badge status-active' : 'status-badge status-inactive';
  };

  return (
    <div className="admin-user-table-container">
      {/* Desktop table */}
      <div className="admin-user-table-wrapper">
        <table className="admin-user-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Email</th>
              <th>Nombre</th>
              <th>Rol</th>
              <th>Estado</th>
              <th>Fecha de Registro</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {users.map((user) => (
              <tr key={user.id}>
                <td className="user-id">#{user.id}</td>
                <td className="user-email">{user.email}</td>
                <td className="user-name">{user.full_name || <span className="no-name">Sin nombre</span>}</td>
                <td className="user-role">
                  <span className={getRoleBadgeClass(user.role)}>
                    {user.role === 'admin' ? 'Administrador' : 'Cliente'}
                  </span>
                </td>
                <td className="user-status">
                  <span className={getStatusBadgeClass(user.is_active)}>
                    {user.is_active ? 'Activo' : 'Inactivo'}
                  </span>
                </td>
                <td className="user-date">{formatDate(user.created_at)}</td>
                <td className="user-actions">
                  <div className="action-buttons">
                    <Button variant="ghost" size="sm" onClick={() => onEdit(user)}>
                      Editar
                    </Button>
                    {user.role !== 'admin' && (
                      <Button
                        variant="danger"
                        size="sm"
                        onClick={() => onDelete(user)}
                        disabled={!user.is_active}
                      >
                        {user.is_active ? 'Desactivar' : 'Desactivado'}
                      </Button>
                    )}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Mobile cards */}
      <div className="admin-user-cards">
        {users.map((user) => (
          <div key={user.id} className="admin-user-card">
            <div className="user-card-header">
              <div className="user-card-title">
                <span className="user-card-id">#{user.id}</span>
                <h3 className="user-card-email">{user.email}</h3>
              </div>
              <div className="user-card-badges">
                <span className={getRoleBadgeClass(user.role)}>
                  {user.role === 'admin' ? 'Admin' : 'Cliente'}
                </span>
                <span className={getStatusBadgeClass(user.is_active)}>
                  {user.is_active ? 'Activo' : 'Inactivo'}
                </span>
              </div>
            </div>

            <div className="user-card-body">
              <div className="user-card-row">
                <span className="label">Nombre:</span>
                <span className="value">
                  {user.full_name || <span className="no-name">Sin nombre</span>}
                </span>
              </div>
              <div className="user-card-row">
                <span className="label">Fecha de registro:</span>
                <span className="value">{formatDate(user.created_at)}</span>
              </div>
            </div>

            <div className="user-card-actions">
              <Button variant="ghost" onClick={() => onEdit(user)}>
                Editar
              </Button>
              {user.role !== 'admin' && (
                <Button
                  variant="danger"
                  onClick={() => onDelete(user)}
                  disabled={!user.is_active}
                >
                  {user.is_active ? 'Desactivar' : 'Desactivado'}
                </Button>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AdminUserTable;
