import React from 'react';
import './Button.css';

/**
 * Reusable Button component
 *
 * @param {Object} props
 * @param {string} props.variant - 'primary', 'secondary', 'danger', 'ghost'
 * @param {string} props.size - 'small', 'medium', 'large'
 * @param {boolean} props.fullWidth - Make button full width
 * @param {boolean} props.disabled - Disable button
 * @param {boolean} props.loading - Show loading state
 * @param {React.ReactNode} props.children - Button content
 * @param {Function} props.onClick - Click handler
 * @param {string} props.type - Button type (button, submit, reset)
 */
function Button({
  children,
  variant = 'primary',
  size = 'medium',
  fullWidth = false,
  disabled = false,
  loading = false,
  onClick,
  type = 'button',
  className = '',
  ...rest
}) {
  const classes = [
    'btn',
    `btn-${variant}`,
    `btn-${size}`,
    fullWidth && 'btn-full-width',
    loading && 'btn-loading',
    className,
  ]
    .filter(Boolean)
    .join(' ');

  return (
    <button
      type={type}
      className={classes}
      disabled={disabled || loading}
      onClick={onClick}
      {...rest}
    >
      {loading ? (
        <>
          <span className="btn-spinner"></span>
          <span className="btn-loading-text">Cargando...</span>
        </>
      ) : (
        children
      )}
    </button>
  );
}

export default Button;
