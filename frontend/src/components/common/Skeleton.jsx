import React from 'react';
import './Skeleton.css';

/**
 * Generic Skeleton component for loading states
 *
 * @param {Object} props
 * @param {string} props.variant - Variant type: 'text' | 'circular' | 'rectangular' (default: 'text')
 * @param {string} props.width - Width of skeleton (e.g., '100%', '200px')
 * @param {string} props.height - Height of skeleton (e.g., '20px', '100%')
 * @param {string} props.className - Additional CSS classes
 * @param {boolean} props.animation - Enable animation (default: true)
 */
const Skeleton = ({
  variant = 'text',
  width = '100%',
  height = '20px',
  className = '',
  animation = true
}) => {
  const skeletonClass = `skeleton skeleton--${variant} ${
    animation ? 'skeleton--animated' : ''
  } ${className}`;

  const style = {
    width,
    height: variant === 'text' ? '1em' : height
  };

  return <div className={skeletonClass} style={style} />;
};

export default Skeleton;
