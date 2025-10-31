import React, { useState, useRef } from 'react';
import Button from './Button';
import './ImageUpload.css';

/**
 * ImageUpload Component
 * Allows users to upload images with preview and validation
 *
 * @param {Object} props
 * @param {File|null} props.value - Current image file
 * @param {string} props.currentImageUrl - URL of current image (if exists)
 * @param {Function} props.onChange - Callback when image changes
 * @param {Function} props.onDelete - Callback when image is deleted
 * @param {string} props.label - Label for the upload button
 * @param {string} props.accept - Accepted file types
 * @param {number} props.maxSize - Max file size in bytes (default: 5MB)
 * @param {boolean} props.disabled - Disable upload
 */
function ImageUpload({
  value,
  currentImageUrl,
  onChange,
  onDelete,
  label = 'Seleccionar imagen',
  accept = 'image/jpeg,image/png,image/gif,image/webp',
  maxSize = 5 * 1024 * 1024, // 5MB
  disabled = false
}) {
  const [preview, setPreview] = useState(currentImageUrl || null);
  const [error, setError] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);

  const validateFile = (file) => {
    // Check file type
    const acceptedTypes = accept.split(',').map(type => type.trim());
    const fileType = file.type;
    const isValidType = acceptedTypes.some(type => {
      if (type.endsWith('/*')) {
        return fileType.startsWith(type.replace('/*', '/'));
      }
      return fileType === type;
    });

    if (!isValidType) {
      setError('Formato de archivo no válido. Use JPG, PNG, GIF o WEBP');
      return false;
    }

    // Check file size
    if (file.size > maxSize) {
      setError(`El archivo es demasiado grande. Máximo ${(maxSize / 1024 / 1024).toFixed(1)}MB`);
      return false;
    }

    setError(null);
    return true;
  };

  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (validateFile(file)) {
      // Create preview
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result);
      };
      reader.readAsDataURL(file);

      // Call onChange callback
      onChange(file);
    } else {
      // Clear input
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);

    const file = e.dataTransfer.files?.[0];
    if (!file) return;

    if (validateFile(file)) {
      // Create preview
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result);
      };
      reader.readAsDataURL(file);

      // Call onChange callback
      onChange(file);
    }
  };

  const handleDelete = () => {
    setPreview(null);
    setError(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
    if (onDelete) {
      onDelete();
    } else {
      onChange(null);
    }
  };

  const handleClick = () => {
    if (!disabled) {
      fileInputRef.current?.click();
    }
  };

  return (
    <div className="image-upload">
      <input
        ref={fileInputRef}
        type="file"
        accept={accept}
        onChange={handleFileChange}
        disabled={disabled}
        className="image-upload-input"
      />

      {preview ? (
        <div className="image-upload-preview">
          <img src={preview} alt="Preview" className="image-upload-preview-img" />
          <div className="image-upload-preview-actions">
            <Button
              variant="ghost"
              size="small"
              onClick={handleClick}
              disabled={disabled}
            >
              Cambiar
            </Button>
            <Button
              variant="danger"
              size="small"
              onClick={handleDelete}
              disabled={disabled}
            >
              Eliminar
            </Button>
          </div>
        </div>
      ) : (
        <div
          className={`image-upload-dropzone ${isDragging ? 'dragging' : ''} ${disabled ? 'disabled' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={handleClick}
        >
          <svg
            className="image-upload-icon"
            xmlns="http://www.w3.org/2000/svg"
            width="48"
            height="48"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <circle cx="8.5" cy="8.5" r="1.5"></circle>
            <polyline points="21 15 16 10 5 21"></polyline>
          </svg>
          <p className="image-upload-text">{label}</p>
          <p className="image-upload-hint">o arrastra y suelta aquí</p>
          <p className="image-upload-limit">
            Formatos: JPG, PNG, GIF, WEBP (máx. {(maxSize / 1024 / 1024).toFixed(1)}MB)
          </p>
        </div>
      )}

      {error && (
        <p className="image-upload-error">{error}</p>
      )}
    </div>
  );
}

export default ImageUpload;
