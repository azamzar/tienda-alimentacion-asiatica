import React from 'react';
import './Card.css';

/**
 * Reusable Card component
 * A flexible container for content with optional header and footer
 *
 * @param {Object} props
 * @param {React.ReactNode} props.children - Card content
 * @param {string} props.title - Optional card title
 * @param {React.ReactNode} props.header - Optional custom header
 * @param {React.ReactNode} props.footer - Optional footer content
 * @param {boolean} props.hoverable - Add hover effect
 * @param {Function} props.onClick - Click handler (makes card clickable)
 * @param {string} props.className - Additional CSS classes
 */
function Card({
  children,
  title,
  header,
  footer,
  hoverable = false,
  onClick,
  className = '',
  ...rest
}) {
  const classes = [
    'card',
    hoverable && 'card-hoverable',
    onClick && 'card-clickable',
    className,
  ]
    .filter(Boolean)
    .join(' ');

  return (
    <div className={classes} onClick={onClick} {...rest}>
      {(title || header) && (
        <div className="card-header">
          {header || <h3 className="card-title">{title}</h3>}
        </div>
      )}

      <div className="card-body">{children}</div>

      {footer && <div className="card-footer">{footer}</div>}
    </div>
  );
}

export default Card;
