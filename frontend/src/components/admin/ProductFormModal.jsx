import React, { useState, useEffect } from 'react';
import { productService } from '../../services/productService';
import { getImageUrl } from '../../utils/formatters';
import Modal from '../common/Modal';
import Input from '../common/Input';
import Button from '../common/Button';
import ImageUpload from '../common/ImageUpload';
import './ProductFormModal.css';

/**
 * Product Form Modal Component
 * Modal form for creating and editing products
 */
function ProductFormModal({ product, categories, onClose, onSave }) {
  const isEditMode = Boolean(product);

  // Form state
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    price: '',
    stock: '',
    category_id: '',
    image_url: '',
  });

  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState(null);
  const [imageFile, setImageFile] = useState(null);
  const [uploadMode, setUploadMode] = useState('file'); // 'file' or 'url'

  // Initialize form with product data if editing
  useEffect(() => {
    if (product) {
      setFormData({
        name: product.name || '',
        description: product.description || '',
        price: product.price?.toString() || '',
        stock: product.stock?.toString() || '',
        category_id: product.category_id?.toString() || '',
        image_url: product.image_url || '',
      });
    }
  }, [product]);

  // Handle input change
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
    // Clear error for this field
    if (errors[name]) {
      setErrors((prev) => ({
        ...prev,
        [name]: null,
      }));
    }
  };

  // Validate form
  const validateForm = () => {
    const newErrors = {};

    if (!formData.name.trim()) {
      newErrors.name = 'El nombre es obligatorio';
    }

    if (!formData.price || parseFloat(formData.price) <= 0) {
      newErrors.price = 'El precio debe ser mayor a 0';
    }

    if (!formData.stock || parseInt(formData.stock) < 0) {
      newErrors.stock = 'El stock no puede ser negativo';
    }

    if (!formData.category_id) {
      newErrors.category_id = 'Debes seleccionar una categoría';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Handle image upload
  const handleImageChange = (file) => {
    setImageFile(file);
  };

  // Handle image delete
  const handleImageDelete = async () => {
    if (isEditMode && product.image_url) {
      try {
        await productService.deleteProductImage(product.id);
        setImageFile(null);
        onSave(); // Refresh product data
      } catch (error) {
        console.error('Error deleting image:', error);
        setSubmitError('Error al eliminar la imagen');
      }
    } else {
      setImageFile(null);
    }
  };

  // Handle form submit
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);
    setSubmitError(null);

    try {
      // Prepare data for API
      const productData = {
        name: formData.name.trim(),
        description: formData.description.trim() || null,
        price: parseFloat(formData.price),
        stock: parseInt(formData.stock),
        category_id: parseInt(formData.category_id),
        image_url: uploadMode === 'url' ? formData.image_url.trim() || null : null,
      };

      let savedProduct;

      if (isEditMode) {
        // Update existing product
        savedProduct = await productService.updateProduct(product.id, productData);
      } else {
        // Create new product
        savedProduct = await productService.createProduct(productData);
      }

      // Upload image if file selected
      if (imageFile && uploadMode === 'file') {
        await productService.uploadProductImage(savedProduct.id, imageFile);
      }

      onSave(); // Callback to parent
    } catch (error) {
      console.error('Error saving product:', error);
      setSubmitError(
        error.response?.data?.detail ||
          `Error al ${isEditMode ? 'actualizar' : 'crear'} el producto`
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Modal
      isOpen={true}
      onClose={onClose}
      title={isEditMode ? 'Editar Producto' : 'Nuevo Producto'}
      size="large"
    >
      <form onSubmit={handleSubmit} className="product-form">
        {/* Product Name */}
        <div className="form-group">
          <label htmlFor="name">
            Nombre <span className="required">*</span>
          </label>
          <Input
            id="name"
            name="name"
            type="text"
            value={formData.name}
            onChange={handleChange}
            error={errors.name}
            placeholder="Ej: Ramen Miso"
            disabled={isSubmitting}
          />
          {errors.name && <span className="error-text">{errors.name}</span>}
        </div>

        {/* Description */}
        <div className="form-group">
          <label htmlFor="description">Descripción</label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            placeholder="Descripción del producto..."
            rows="3"
            disabled={isSubmitting}
            className="form-textarea"
          />
        </div>

        {/* Price and Stock */}
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="price">
              Precio (€) <span className="required">*</span>
            </label>
            <Input
              id="price"
              name="price"
              type="number"
              step="0.01"
              min="0"
              value={formData.price}
              onChange={handleChange}
              error={errors.price}
              placeholder="0.00"
              disabled={isSubmitting}
            />
            {errors.price && <span className="error-text">{errors.price}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="stock">
              Stock <span className="required">*</span>
            </label>
            <Input
              id="stock"
              name="stock"
              type="number"
              min="0"
              value={formData.stock}
              onChange={handleChange}
              error={errors.stock}
              placeholder="0"
              disabled={isSubmitting}
            />
            {errors.stock && <span className="error-text">{errors.stock}</span>}
          </div>
        </div>

        {/* Category */}
        <div className="form-group">
          <label htmlFor="category_id">
            Categoría <span className="required">*</span>
          </label>
          <select
            id="category_id"
            name="category_id"
            value={formData.category_id}
            onChange={handleChange}
            disabled={isSubmitting}
            className={`form-select ${errors.category_id ? 'error' : ''}`}
          >
            <option value="">Selecciona una categoría</option>
            {categories.map((category) => (
              <option key={category.id} value={category.id}>
                {category.name}
              </option>
            ))}
          </select>
          {errors.category_id && (
            <span className="error-text">{errors.category_id}</span>
          )}
        </div>

        {/* Image Upload */}
        <div className="form-group">
          <label>Imagen del Producto</label>

          {/* Toggle between file upload and URL */}
          <div className="upload-mode-toggle">
            <button
              type="button"
              className={`toggle-btn ${uploadMode === 'file' ? 'active' : ''}`}
              onClick={() => setUploadMode('file')}
              disabled={isSubmitting}
            >
              Subir Archivo
            </button>
            <button
              type="button"
              className={`toggle-btn ${uploadMode === 'url' ? 'active' : ''}`}
              onClick={() => setUploadMode('url')}
              disabled={isSubmitting}
            >
              URL Externa
            </button>
          </div>

          {uploadMode === 'file' ? (
            <ImageUpload
              value={imageFile}
              currentImageUrl={product?.image_url ? getImageUrl(product.image_url) : null}
              onChange={handleImageChange}
              onDelete={handleImageDelete}
              disabled={isSubmitting}
            />
          ) : (
            <>
              <Input
                id="image_url"
                name="image_url"
                type="url"
                value={formData.image_url}
                onChange={handleChange}
                placeholder="https://ejemplo.com/imagen.jpg"
                disabled={isSubmitting}
              />
              <span className="helper-text">
                Opcional. URL de la imagen del producto.
              </span>
            </>
          )}
        </div>

        {/* Submit Error */}
        {submitError && (
          <div className="submit-error">
            <p>{submitError}</p>
          </div>
        )}

        {/* Form Actions */}
        <div className="form-actions">
          <Button
            type="button"
            variant="ghost"
            onClick={onClose}
            disabled={isSubmitting}
          >
            Cancelar
          </Button>
          <Button type="submit" variant="primary" disabled={isSubmitting}>
            {isSubmitting
              ? isEditMode
                ? 'Actualizando...'
                : 'Creando...'
              : isEditMode
              ? 'Actualizar Producto'
              : 'Crear Producto'}
          </Button>
        </div>
      </form>
    </Modal>
  );
}

export default ProductFormModal;
