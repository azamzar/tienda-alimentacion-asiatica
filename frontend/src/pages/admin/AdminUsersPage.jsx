import React, { useState, useEffect } from 'react';
import { userService } from '../../services/userService';
import AdminUserTable from '../../components/admin/AdminUserTable';
import UserFormModal from '../../components/admin/UserFormModal';
import Modal from '../../components/common/Modal';
import Button from '../../components/common/Button';
import './AdminUsersPage.css';

/**
 * Página de gestión de usuarios para administradores
 */
const AdminUsersPage = () => {
  const [users, setUsers] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isFormModalOpen, setIsFormModalOpen] = useState(false);
  const [selectedUser, setSelectedUser] = useState(null);
  const [userToDelete, setUserToDelete] = useState(null);
  const [formLoading, setFormLoading] = useState(false);
  const [filterRole, setFilterRole] = useState('all');
  const [filterStatus, setFilterStatus] = useState('all');

  // Cargar usuarios y estadísticas
  const fetchUsers = async () => {
    setLoading(true);
    setError(null);
    try {
      const params = {};
      if (filterRole !== 'all') params.role = filterRole;
      if (filterStatus !== 'all') params.is_active = filterStatus === 'active';

      const [usersData, statsData] = await Promise.all([
        userService.getUsers(params),
        userService.getUserStats(),
      ]);

      setUsers(usersData);
      setStats(statsData);
    } catch (err) {
      console.error('Error al cargar usuarios:', err);
      setError(err.response?.data?.detail || 'Error al cargar los usuarios');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, [filterRole, filterStatus]);

  // Abrir modal para editar
  const handleEdit = (user) => {
    setSelectedUser(user);
    setIsFormModalOpen(true);
  };

  // Actualizar usuario
  const handleSubmit = async (formData) => {
    setFormLoading(true);
    try {
      await userService.updateUser(selectedUser.id, formData);
      await fetchUsers();
      setIsFormModalOpen(false);
      setSelectedUser(null);
    } catch (err) {
      console.error('Error al actualizar usuario:', err);
      alert(err.response?.data?.detail || 'Error al actualizar el usuario');
    } finally {
      setFormLoading(false);
    }
  };

  // Confirmar desactivación
  const handleDeleteClick = (user) => {
    setUserToDelete(user);
  };

  // Desactivar usuario
  const handleDeleteConfirm = async () => {
    if (!userToDelete) return;

    try {
      await userService.deleteUser(userToDelete.id);
      await fetchUsers();
      setUserToDelete(null);
    } catch (err) {
      console.error('Error al desactivar usuario:', err);
      alert(err.response?.data?.detail || 'Error al desactivar el usuario');
    }
  };

  return (
    <div className="admin-users-page">
      <div className="page-header">
        <div className="header-content">
          <h1>Gestión de Usuarios</h1>
          <p className="subtitle">Administra los usuarios registrados en la tienda</p>
        </div>
        <div className="header-actions">
          <Button onClick={fetchUsers} variant="ghost" disabled={loading}>
            {loading ? 'Actualizando...' : 'Actualizar'}
          </Button>
        </div>
      </div>

      {/* Estadísticas */}
      {stats && (
        <div className="users-stats">
          <div className="stat-card stat-primary">
            <div className="stat-value">{stats.total}</div>
            <div className="stat-label">Total Usuarios</div>
          </div>
          <div className="stat-card stat-green">
            <div className="stat-value">{stats.active}</div>
            <div className="stat-label">Activos</div>
          </div>
          <div className="stat-card stat-red">
            <div className="stat-value">{stats.inactive}</div>
            <div className="stat-label">Inactivos</div>
          </div>
          <div className="stat-card stat-purple">
            <div className="stat-value">{stats.admins}</div>
            <div className="stat-label">Administradores</div>
          </div>
          <div className="stat-card stat-blue">
            <div className="stat-value">{stats.customers}</div>
            <div className="stat-label">Clientes</div>
          </div>
        </div>
      )}

      {/* Filtros */}
      <div className="users-filters">
        <div className="filter-group">
          <label htmlFor="filterRole">Rol:</label>
          <select
            id="filterRole"
            value={filterRole}
            onChange={(e) => setFilterRole(e.target.value)}
            disabled={loading}
          >
            <option value="all">Todos</option>
            <option value="customer">Clientes</option>
            <option value="admin">Administradores</option>
          </select>
        </div>

        <div className="filter-group">
          <label htmlFor="filterStatus">Estado:</label>
          <select
            id="filterStatus"
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            disabled={loading}
          >
            <option value="all">Todos</option>
            <option value="active">Activos</option>
            <option value="inactive">Inactivos</option>
          </select>
        </div>
      </div>

      {/* Error */}
      {error && (
        <div className="error-message">
          <p>{error}</p>
          <Button onClick={fetchUsers}>Reintentar</Button>
        </div>
      )}

      {/* Tabla de usuarios */}
      {!error && (
        <AdminUserTable
          users={users}
          onEdit={handleEdit}
          onDelete={handleDeleteClick}
          loading={loading}
        />
      )}

      {/* Modal de formulario */}
      <UserFormModal
        isOpen={isFormModalOpen}
        onClose={() => {
          setIsFormModalOpen(false);
          setSelectedUser(null);
        }}
        user={selectedUser}
        onSubmit={handleSubmit}
        loading={formLoading}
      />

      {/* Modal de confirmación de desactivación */}
      {userToDelete && (
        <Modal
          isOpen={!!userToDelete}
          onClose={() => setUserToDelete(null)}
          title="Confirmar Desactivación"
        >
          <div className="delete-confirmation">
            <p>
              ¿Estás seguro de que quieres desactivar al usuario{' '}
              <strong>{userToDelete.email}</strong>?
            </p>
            <p className="warning-text">
              ⚠️ El usuario no podrá iniciar sesión hasta que sea reactivado. Los datos y pedidos
              del usuario se mantendrán intactos.
            </p>
            <div className="modal-actions">
              <Button variant="ghost" onClick={() => setUserToDelete(null)}>
                Cancelar
              </Button>
              <Button variant="danger" onClick={handleDeleteConfirm}>
                Desactivar
              </Button>
            </div>
          </div>
        </Modal>
      )}
    </div>
  );
};

export default AdminUsersPage;
