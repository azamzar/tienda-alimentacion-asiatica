import React, { useState } from 'react';
import { validateCheckoutForm } from '../../utils/validators';
import Input from '../common/Input';
import Button from '../common/Button';
import './CheckoutForm.css';

/**
 * Formulario de checkout para crear un pedido
 * @param {Function} onSubmit - Callback al enviar el formulario
 * @param {boolean} loading - Estado de carga
 */
const CheckoutForm = ({ onSubmit, loading }) => {
  const [formData, setFormData] = useState({
    customer_name: '',
    customer_email: '',
    customer_phone: '',
    shipping_address: '',
    notes: ''
  });

  const [errors, setErrors] = useState({});
  const [touched, setTouched] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));

    // Limpiar error del campo al escribir
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const handleBlur = (e) => {
    const { name } = e.target;
    setTouched(prev => ({
      ...prev,
      [name]: true
    }));

    // Validar campo individual
    const fieldErrors = validateCheckoutForm(formData);
    if (fieldErrors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: fieldErrors[name]
      }));
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Marcar todos los campos como tocados
    setTouched({
      customer_name: true,
      customer_email: true,
      customer_phone: true,
      shipping_address: true,
      notes: true
    });

    // Validar formulario completo
    const validationErrors = validateCheckoutForm(formData);

    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    // Enviar datos
    onSubmit(formData);
  };

  return (
    <form className="checkout-form" onSubmit={handleSubmit} noValidate>
      <div className="checkout-form__section">
        <h3 className="checkout-form__section-title">Datos de Contacto</h3>

        {/* Nombre completo */}
        <div className="checkout-form__field">
          <Input
            label="Nombre Completo *"
            name="customer_name"
            value={formData.customer_name}
            onChange={handleChange}
            onBlur={handleBlur}
            error={touched.customer_name && errors.customer_name}
            placeholder="Juan Pérez"
            disabled={loading}
            required
          />
        </div>

        {/* Email */}
        <div className="checkout-form__field">
          <Input
            label="Email *"
            type="email"
            name="customer_email"
            value={formData.customer_email}
            onChange={handleChange}
            onBlur={handleBlur}
            error={touched.customer_email && errors.customer_email}
            placeholder="tu@email.com"
            disabled={loading}
            required
          />
        </div>

        {/* Teléfono */}
        <div className="checkout-form__field">
          <Input
            label="Teléfono *"
            type="tel"
            name="customer_phone"
            value={formData.customer_phone}
            onChange={handleChange}
            onBlur={handleBlur}
            error={touched.customer_phone && errors.customer_phone}
            placeholder="+34 612 345 678"
            disabled={loading}
            required
          />
        </div>
      </div>

      <div className="checkout-form__section">
        <h3 className="checkout-form__section-title">Dirección de Envío</h3>

        {/* Dirección */}
        <div className="checkout-form__field">
          <label className="checkout-form__label">
            Dirección Completa *
            <textarea
              className={`checkout-form__textarea ${
                touched.shipping_address && errors.shipping_address ? 'checkout-form__textarea--error' : ''
              }`}
              name="shipping_address"
              value={formData.shipping_address}
              onChange={handleChange}
              onBlur={handleBlur}
              placeholder="Calle, número, piso, código postal, ciudad"
              rows="3"
              disabled={loading}
              required
            />
          </label>
          {touched.shipping_address && errors.shipping_address && (
            <span className="checkout-form__error">{errors.shipping_address}</span>
          )}
        </div>
      </div>

      <div className="checkout-form__section">
        <h3 className="checkout-form__section-title">Notas Adicionales</h3>

        {/* Notas */}
        <div className="checkout-form__field">
          <label className="checkout-form__label">
            Instrucciones de entrega (opcional)
            <textarea
              className="checkout-form__textarea"
              name="notes"
              value={formData.notes}
              onChange={handleChange}
              placeholder="Ej: Llamar antes de entregar, dejar en portería, etc."
              rows="3"
              disabled={loading}
            />
          </label>
        </div>
      </div>

      {/* Botón de envío */}
      <div className="checkout-form__actions">
        <Button
          type="submit"
          variant="primary"
          size="large"
          fullWidth
          disabled={loading}
          loading={loading}
        >
          {loading ? 'Procesando...' : 'Confirmar Pedido'}
        </Button>
      </div>

      <p className="checkout-form__note">
        * Campos obligatorios
      </p>
    </form>
  );
};

export default CheckoutForm;
