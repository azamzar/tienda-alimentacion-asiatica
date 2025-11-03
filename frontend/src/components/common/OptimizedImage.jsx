import React, { useState, useEffect, useRef } from 'react';
import './OptimizedImage.css';

/**
 * OptimizedImage component with lazy loading and progressive enhancement
 *
 * Features:
 * - Lazy loading with Intersection Observer
 * - Progressive image loading (thumbnail -> full)
 * - WebP support with fallback
 * - Responsive images with srcset
 * - Blur-up placeholder effect
 * - Error handling with fallback image
 *
 * @param {Object} props
 * @param {string} props.src - Image source URL (can be external URL or path to uploaded image)
 * @param {number} props.productId - Product ID (for accessing optimized thumbnails)
 * @param {string} props.alt - Alt text for accessibility
 * @param {string} props.size - Image size variant: 'thumbnail' | 'medium' | 'large' (default: 'medium')
 * @param {string} props.className - Additional CSS classes
 * @param {boolean} props.lazy - Enable lazy loading (default: true)
 * @param {string} props.fallback - Fallback image URL if loading fails
 */
const OptimizedImage = ({
  src,
  productId,
  alt = 'Product image',
  size = 'medium',
  className = '',
  lazy = true,
  fallback = '/placeholder-product.png'
}) => {
  const [isLoaded, setIsLoaded] = useState(false);
  const [isInView, setIsInView] = useState(!lazy);
  const [hasError, setHasError] = useState(false);
  const [currentSrc, setCurrentSrc] = useState(null);
  const imgRef = useRef(null);

  // Determine the image source based on whether it's uploaded or external
  const getImageUrl = (imageSize) => {
    // If no src provided, use fallback
    if (!src) return fallback;

    // If it's an external URL (starts with http), use it directly
    if (src.startsWith('http://') || src.startsWith('https://')) {
      return src;
    }

    // If productId is provided, try to use optimized versions
    if (productId) {
      // Check if src already points to an optimized version
      if (src.includes('/products/') && src.includes('/')) {
        // Extract just the product ID folder path
        const baseUrl = `http://localhost:8000/uploads/products/${productId}`;
        return `${baseUrl}/${imageSize}.webp`;
      }
    }

    // Default: use the provided src with base URL
    if (src.startsWith('/uploads/')) {
      return `http://localhost:8000${src}`;
    }

    return src;
  };

  // Lazy loading with Intersection Observer
  useEffect(() => {
    if (!lazy || isInView) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setIsInView(true);
            observer.disconnect();
          }
        });
      },
      {
        rootMargin: '50px', // Start loading 50px before image enters viewport
        threshold: 0.01
      }
    );

    if (imgRef.current) {
      observer.observe(imgRef.current);
    }

    return () => {
      if (imgRef.current) {
        observer.unobserve(imgRef.current);
      }
    };
  }, [lazy, isInView]);

  // Progressive loading: load thumbnail first, then full size
  useEffect(() => {
    if (!isInView || hasError) return;

    // Start with thumbnail for progressive loading
    if (size !== 'thumbnail' && productId) {
      const thumbnailUrl = getImageUrl('thumbnail');
      const img = new Image();
      img.src = thumbnailUrl;
      img.onload = () => {
        setCurrentSrc(thumbnailUrl);
      };
    }

    // Then load the full size image
    const fullSizeUrl = getImageUrl(size);
    const img = new Image();
    img.src = fullSizeUrl;

    img.onload = () => {
      setCurrentSrc(fullSizeUrl);
      setIsLoaded(true);
    };

    img.onerror = () => {
      setHasError(true);
      setCurrentSrc(fallback);
    };
  }, [isInView, size, productId, hasError]);

  // Handle image load error
  const handleError = () => {
    if (!hasError) {
      setHasError(true);
      setCurrentSrc(fallback);
    }
  };

  // Generate srcset for responsive images
  const getSrcSet = () => {
    if (!productId || hasError) return '';

    return [
      `${getImageUrl('thumbnail')} 150w`,
      `${getImageUrl('medium')} 300w`,
      `${getImageUrl('large')} 600w`
    ].join(', ');
  };

  // Generate sizes attribute
  const getSizes = () => {
    switch (size) {
      case 'thumbnail':
        return '150px';
      case 'medium':
        return '(max-width: 768px) 100vw, 300px';
      case 'large':
        return '(max-width: 768px) 100vw, 600px';
      default:
        return '300px';
    }
  };

  return (
    <div
      ref={imgRef}
      className={`optimized-image ${className} ${isLoaded ? 'loaded' : 'loading'}`}
    >
      {!isInView ? (
        // Placeholder while not in viewport
        <div className="optimized-image__placeholder" />
      ) : (
        <>
          {currentSrc && (
            <img
              src={currentSrc}
              srcSet={productId && !hasError ? getSrcSet() : undefined}
              sizes={productId && !hasError ? getSizes() : undefined}
              alt={alt}
              onError={handleError}
              loading={lazy ? 'lazy' : 'eager'}
              className={`optimized-image__img ${isLoaded ? 'fade-in' : ''}`}
            />
          )}
          {!isLoaded && !hasError && (
            <div className="optimized-image__loader">
              <div className="spinner-small" />
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default OptimizedImage;
