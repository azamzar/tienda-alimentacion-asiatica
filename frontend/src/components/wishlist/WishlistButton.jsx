import React, { useState, useEffect } from 'react';
import toast from 'react-hot-toast';
import { useNavigate } from 'react-router-dom';
import { useWishlistStore } from '../../store/useWishlistStore';
import { useAuthStore } from '../../store/useAuthStore';
import './WishlistButton.css';

/**
 * WishlistButton Component - Toggle button for adding/removing from wishlist
 * @param {number} productId - ID of the product
 * @param {string} size - Size of the button ('small', 'medium', 'large')
 * @param {boolean} showLabel - Whether to show text label
 * @param {string} className - Additional CSS classes
 */
const WishlistButton = ({
  productId,
  size = 'medium',
  showLabel = false,
  className = ''
}) => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuthStore();
  const { isInWishlist, toggleWishlist, loading } = useWishlistStore();
  const [isInList, setIsInList] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (isAuthenticated) {
      setIsInList(isInWishlist(productId));
    }
  }, [productId, isAuthenticated, isInWishlist]);

  const handleClick = async (e) => {
    e.preventDefault();
    e.stopPropagation();

    if (!isAuthenticated) {
      toast.error('Debes iniciar sesión para agregar favoritos');
      setTimeout(() => navigate('/login'), 1000);
      return;
    }

    setIsLoading(true);

    try {
      const wasAdded = await toggleWishlist(productId);

      if (wasAdded) {
        setIsInList(true);
        toast.success('Agregado a favoritos', {
          icon: '❤️',
          duration: 2000
        });
      } else {
        setIsInList(false);
        toast.success('Quitado de favoritos', {
          icon: '💔',
          duration: 2000
        });
      }
    } catch (error) {
      console.error('Error toggling wishlist:', error);
      toast.error(error.response?.data?.detail || 'Error al actualizar favoritos');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <button
      onClick={handleClick}
      disabled={isLoading}
      className={`wishlist-button wishlist-button--${size} ${isInList ? 'wishlist-button--active' : ''} ${className}`}
      aria-label={isInList ? 'Quitar de favoritos' : 'Agregar a favoritos'}
      title={isInList ? 'Quitar de favoritos' : 'Agregar a favoritos'}
    >
      <svg
        className="wishlist-button__icon"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        fill={isInList ? 'currentColor' : 'none'}
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
      </svg>
      {showLabel && (
        <span className="wishlist-button__label">
          {isInList ? 'En favoritos' : 'Favorito'}
        </span>
      )}
    </button>
  );
};

export default WishlistButton;
