import React from 'react';
import './Spinner.css';

/**
 * Loading spinner component
 *
 * @param {Object} props
 * @param {string} props.size - 'small', 'medium', 'large'
 * @param {string} props.color - Spinner color
 * @param {boolean} props.centered - Center spinner in container
 * @param {string} props.text - Optional loading text
 */
function Spinner({
  size = 'medium',
  color = '#3b82f6',
  centered = false,
  text,
  className = '',
}) {
  const containerClasses = [
    'spinner-container',
    centered && 'spinner-centered',
    className,
  ]
    .filter(Boolean)
    .join(' ');

  const spinnerClasses = ['spinner', `spinner-${size}`].filter(Boolean).join(' ');

  return (
    <div className={containerClasses}>
      <div className={spinnerClasses} style={{ borderTopColor: color }}></div>
      {text && <p className="spinner-text">{text}</p>}
    </div>
  );
}

export default Spinner;
