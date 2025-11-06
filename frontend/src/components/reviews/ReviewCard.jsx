import React from 'react';
import RatingStars from './RatingStars';
import { formatDate } from '../../utils/formatters';
import './ReviewCard.css';

/**
 * ReviewCard Component - Display a single review
 * @param {Object} review - Review object
 * @param {boolean} isOwner - Whether current user is the review owner
 * @param {function} onEdit - Callback when edit button is clicked
 * @param {function} onDelete - Callback when delete button is clicked
 */
const ReviewCard = ({
  review,
  isOwner = false,
  onEdit = null,
  onDelete = null
}) => {
  if (!review) return null;

  const { rating, title, comment, created_at, updated_at, user } = review;
  const isEdited = updated_at && new Date(updated_at) > new Date(created_at);

  return (
    <div className="review-card">
      <div className="review-card__header">
        <div className="review-card__user">
          <div className="review-card__avatar">
            {user?.full_name?.charAt(0)?.toUpperCase() || user?.email?.charAt(0)?.toUpperCase() || 'U'}
          </div>
          <div className="review-card__user-info">
            <h4 className="review-card__username">
              {user?.full_name || user?.email || 'Anonymous'}
            </h4>
            <div className="review-card__date">
              {formatDate(created_at)}
              {isEdited && <span className="review-card__edited"> (editada)</span>}
            </div>
          </div>
        </div>

        {isOwner && (onEdit || onDelete) && (
          <div className="review-card__actions">
            {onEdit && (
              <button
                onClick={() => onEdit(review)}
                className="review-card__action-btn review-card__action-btn--edit"
                aria-label="Editar reseña"
              >
                ✏️
              </button>
            )}
            {onDelete && (
              <button
                onClick={() => onDelete(review.id)}
                className="review-card__action-btn review-card__action-btn--delete"
                aria-label="Eliminar reseña"
              >
                🗑️
              </button>
            )}
          </div>
        )}
      </div>

      <div className="review-card__rating">
        <RatingStars rating={rating} size="small" />
      </div>

      {title && (
        <h5 className="review-card__title">{title}</h5>
      )}

      {comment && (
        <p className="review-card__comment">{comment}</p>
      )}
    </div>
  );
};

export default ReviewCard;
