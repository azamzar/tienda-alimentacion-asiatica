import React from 'react';
import './Input.css';

/**
 * Reusable Input component
 *
 * @param {Object} props
 * @param {string} props.label - Input label
 * @param {string} props.type - Input type (text, email, password, number, etc.)
 * @param {string} props.placeholder - Placeholder text
 * @param {string} props.error - Error message
 * @param {string} props.helperText - Helper text below input
 * @param {boolean} props.required - Mark as required
 * @param {boolean} props.disabled - Disable input
 * @param {boolean} props.fullWidth - Make input full width
 * @param {string} props.value - Input value
 * @param {Function} props.onChange - Change handler
 * @param {string} props.name - Input name
 * @param {string} props.id - Input id
 */
function Input({
  label,
  type = 'text',
  placeholder,
  error,
  helperText,
  required = false,
  disabled = false,
  fullWidth = true,
  value,
  onChange,
  name,
  id,
  className = '',
  ...rest
}) {
  const inputId = id || name || `input-${Math.random().toString(36).substr(2, 9)}`;

  const inputClasses = [
    'input',
    error && 'input-error',
    disabled && 'input-disabled',
    fullWidth && 'input-full-width',
    className,
  ]
    .filter(Boolean)
    .join(' ');

  return (
    <div className="input-wrapper">
      {label && (
        <label htmlFor={inputId} className="input-label">
          {label}
          {required && <span className="input-required"> *</span>}
        </label>
      )}

      <input
        id={inputId}
        type={type}
        name={name}
        className={inputClasses}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        disabled={disabled}
        required={required}
        {...rest}
      />

      {error && <p className="input-error-message">{error}</p>}
      {helperText && !error && <p className="input-helper-text">{helperText}</p>}
    </div>
  );
}

export default Input;
