import React, { useState } from 'react';
import './RatingStars.css';

/**
 * RatingStars Component - Display or input star ratings
 * @param {number} rating - Current rating (1-5)
 * @param {number} maxRating - Maximum rating (default: 5)
 * @param {boolean} interactive - Whether stars are clickable
 * @param {function} onRatingChange - Callback when rating changes (interactive mode)
 * @param {string} size - Size of stars ('small', 'medium', 'large')
 */
const RatingStars = ({
  rating = 0,
  maxRating = 5,
  interactive = false,
  onRatingChange = null,
  size = 'medium'
}) => {
  const [hoverRating, setHoverRating] = useState(0);

  const handleClick = (newRating) => {
    if (interactive && onRatingChange) {
      onRatingChange(newRating);
    }
  };

  const handleMouseEnter = (star) => {
    if (interactive) {
      setHoverRating(star);
    }
  };

  const handleMouseLeave = () => {
    if (interactive) {
      setHoverRating(0);
    }
  };

  const getStarType = (star) => {
    const effectiveRating = hoverRating || rating;

    if (effectiveRating >= star) {
      return 'full';
    } else if (effectiveRating >= star - 0.5) {
      return 'half';
    }
    return 'empty';
  };

  return (
    <div className={`rating-stars rating-stars--${size} ${interactive ? 'rating-stars--interactive' : ''}`}>
      {[...Array(maxRating)].map((_, index) => {
        const star = index + 1;
        const starType = getStarType(star);

        return (
          <span
            key={star}
            className={`star star--${starType}`}
            onClick={() => handleClick(star)}
            onMouseEnter={() => handleMouseEnter(star)}
            onMouseLeave={handleMouseLeave}
            role={interactive ? 'button' : 'img'}
            aria-label={`${star} ${star === 1 ? 'star' : 'stars'}`}
            tabIndex={interactive ? 0 : -1}
          >
            {starType === 'full' && '★'}
            {starType === 'half' && '⯨'}
            {starType === 'empty' && '☆'}
          </span>
        );
      })}
      {rating > 0 && (
        <span className="rating-value" aria-label={`Rating: ${rating} out of ${maxRating}`}>
          {rating.toFixed(1)}
        </span>
      )}
    </div>
  );
};

export default RatingStars;
