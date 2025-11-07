import React from 'react';
import './RatingFilter.css';

/**
 * RatingFilter Component
 *
 * Filtro de productos por rating mínimo.
 * Permite seleccionar un rating mínimo de 1-5 estrellas.
 *
 * @param {Object} props
 * @param {number} props.selectedRating - Rating seleccionado actual (null si no hay filtro)
 * @param {Function} props.onChange - Callback cuando cambia el rating
 */
const RatingFilter = ({ selectedRating, onChange }) => {
  const ratings = [5, 4, 3, 2, 1];

  const handleRatingClick = (rating) => {
    // Si se clickea el mismo rating, se deselecciona
    if (selectedRating === rating) {
      onChange(null);
    } else {
      onChange(rating);
    }
  };

  const handleClear = () => {
    onChange(null);
  };

  const renderStars = (rating) => {
    const stars = [];
    for (let i = 1; i <= 5; i++) {
      stars.push(
        <span
          key={i}
          className={`rating-star ${i <= rating ? 'filled' : 'empty'}`}
        >
          ★
        </span>
      );
    }
    return stars;
  };

  return (
    <div className="rating-filter">
      <div className="rating-filter-header">
        <h4 className="rating-filter-title">Valoración</h4>
        {selectedRating && (
          <button
            className="rating-filter-clear"
            onClick={handleClear}
            aria-label="Limpiar filtro de valoración"
          >
            ✕
          </button>
        )}
      </div>

      <div className="rating-options">
        {ratings.map((rating) => (
          <button
            key={rating}
            className={`rating-option ${selectedRating === rating ? 'active' : ''}`}
            onClick={() => handleRatingClick(rating)}
            aria-label={`Filtrar por ${rating} estrellas o más`}
          >
            <div className="rating-stars">
              {renderStars(rating)}
            </div>
            <span className="rating-text">y más</span>
          </button>
        ))}
      </div>

      {selectedRating && (
        <div className="rating-filter-selected">
          <span className="rating-filter-icon">✓</span>
          Mostrando productos con {selectedRating}+ estrellas
        </div>
      )}
    </div>
  );
};

export default RatingFilter;
