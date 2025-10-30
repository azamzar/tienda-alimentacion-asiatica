import React, { useState, useEffect } from 'react';
import Modal from '../common/Modal';
import Button from '../common/Button';
import Input from '../common/Input';
import './UserFormModal.css';

/**
 * Modal para editar usuarios (Admin)
 * Solo permite editar: email, nombre completo y estado activo
 */
const UserFormModal = ({ isOpen, onClose, user, onSubmit, loading }) => {
  const [formData, setFormData] = useState({
    email: '',
    full_name: '',
    is_active: true,
  });
  const [errors, setErrors] = useState({});

  // Cargar datos del usuario
  useEffect(() => {
    if (user) {
      setFormData({
        email: user.email || '',
        full_name: user.full_name || '',
        is_active: user.is_active !== undefined ? user.is_active : true,
      });
    } else {
      setFormData({
        email: '',
        full_name: '',
        is_active: true,
      });
    }
    setErrors({});
  }, [user, isOpen]);

  const validateForm = () => {
    const newErrors = {};

    // Validar email
    if (!formData.email.trim()) {
      newErrors.email = 'El email es obligatorio';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Email inválido';
    }

    // Validar nombre (opcional pero si se proporciona debe tener al menos 2 caracteres)
    if (formData.full_name.trim() && formData.full_name.trim().length < 2) {
      newErrors.full_name = 'El nombre debe tener al menos 2 caracteres';
    } else if (formData.full_name.length > 255) {
      newErrors.full_name = 'El nombre no puede exceder 255 caracteres';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    // Preparar datos a enviar (solo campos que han cambiado)
    const dataToSubmit = {};

    if (formData.email !== user.email) {
      dataToSubmit.email = formData.email;
    }

    if (formData.full_name !== (user.full_name || '')) {
      dataToSubmit.full_name = formData.full_name || null;
    }

    if (formData.is_active !== user.is_active) {
      dataToSubmit.is_active = formData.is_active;
    }

    // Si no hay cambios, cerrar modal
    if (Object.keys(dataToSubmit).length === 0) {
      onClose();
      return;
    }

    onSubmit(dataToSubmit);
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
    // Limpiar error del campo al escribir
    if (errors[name]) {
      setErrors((prev) => ({
        ...prev,
        [name]: null,
      }));
    }
  };

  if (!user) return null;

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={`Editar Usuario #${user.id}`}
    >
      <form onSubmit={handleSubmit} className="user-form">
        {/* Info del usuario */}
        <div className="user-info-section">
          <div className="info-row">
            <span className="info-label">ID:</span>
            <span className="info-value">#{user.id}</span>
          </div>
          <div className="info-row">
            <span className="info-label">Rol:</span>
            <span className={`info-value role-${user.role}`}>
              {user.role === 'admin' ? 'Administrador' : 'Cliente'}
            </span>
          </div>
          <div className="info-row">
            <span className="info-label">Fecha de registro:</span>
            <span className="info-value">
              {new Date(user.created_at).toLocaleDateString('es-ES')}
            </span>
          </div>
        </div>

        <hr className="form-divider" />

        {/* Campos editables */}
        <Input
          label="Email"
          name="email"
          type="email"
          value={formData.email}
          onChange={handleChange}
          error={errors.email}
          placeholder="usuario@ejemplo.com"
          required
        />

        <Input
          label="Nombre completo"
          name="full_name"
          type="text"
          value={formData.full_name}
          onChange={handleChange}
          error={errors.full_name}
          placeholder="Nombre del usuario"
        />

        {/* Estado activo */}
        <div className="form-group checkbox-group">
          <label className="checkbox-label">
            <input
              type="checkbox"
              name="is_active"
              checked={formData.is_active}
              onChange={handleChange}
              disabled={user.role === 'admin'}
            />
            <span>Usuario activo</span>
          </label>
          {user.role === 'admin' && (
            <p className="help-text">Los usuarios administradores no pueden ser desactivados</p>
          )}
          {!formData.is_active && (
            <p className="warning-text">
              El usuario no podrá iniciar sesión mientras esté desactivado
            </p>
          )}
        </div>

        <div className="modal-actions">
          <Button type="button" variant="ghost" onClick={onClose} disabled={loading}>
            Cancelar
          </Button>
          <Button type="submit" variant="primary" disabled={loading}>
            {loading ? 'Guardando...' : 'Actualizar'}
          </Button>
        </div>
      </form>
    </Modal>
  );
};

export default UserFormModal;
