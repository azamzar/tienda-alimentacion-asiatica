import React, { useState, useEffect } from 'react';
import RatingStars from './RatingStars';
import './ReviewForm.css';

/**
 * ReviewForm Component - Form for creating/editing reviews
 * @param {Object} initialData - Initial review data (for editing)
 * @param {function} onSubmit - Callback when form is submitted
 * @param {function} onCancel - Callback when form is cancelled
 * @param {boolean} loading - Whether form is submitting
 */
const ReviewForm = ({
  initialData = null,
  onSubmit,
  onCancel,
  loading = false
}) => {
  const [rating, setRating] = useState(initialData?.rating || 0);
  const [title, setTitle] = useState(initialData?.title || '');
  const [comment, setComment] = useState(initialData?.comment || '');
  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (initialData) {
      setRating(initialData.rating || 0);
      setTitle(initialData.title || '');
      setComment(initialData.comment || '');
    }
  }, [initialData]);

  const validate = () => {
    const newErrors = {};

    if (rating === 0) {
      newErrors.rating = 'Por favor selecciona una calificación';
    }

    if (title && title.length > 200) {
      newErrors.title = 'El título no puede tener más de 200 caracteres';
    }

    if (comment && comment.length > 2000) {
      newErrors.comment = 'El comentario no puede tener más de 2000 caracteres';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!validate()) {
      return;
    }

    const reviewData = {
      rating,
      title: title.trim() || undefined,
      comment: comment.trim() || undefined
    };

    onSubmit(reviewData);
  };

  const handleReset = () => {
    setRating(initialData?.rating || 0);
    setTitle(initialData?.title || '');
    setComment(initialData?.comment || '');
    setErrors({});
  };

  return (
    <form className="review-form" onSubmit={handleSubmit}>
      <div className="review-form__header">
        <h3 className="review-form__title">
          {initialData ? 'Editar reseña' : 'Escribir reseña'}
        </h3>
      </div>

      {/* Rating */}
      <div className="review-form__field">
        <label className="review-form__label">
          Calificación <span className="review-form__required">*</span>
        </label>
        <RatingStars
          rating={rating}
          interactive={true}
          onRatingChange={setRating}
          size="large"
        />
        {errors.rating && (
          <span className="review-form__error">{errors.rating}</span>
        )}
      </div>

      {/* Title */}
      <div className="review-form__field">
        <label htmlFor="review-title" className="review-form__label">
          Título (opcional)
        </label>
        <input
          id="review-title"
          type="text"
          className="review-form__input"
          placeholder="Resume tu opinión en pocas palabras"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          maxLength={200}
          disabled={loading}
        />
        <span className="review-form__char-count">
          {title.length}/200
        </span>
        {errors.title && (
          <span className="review-form__error">{errors.title}</span>
        )}
      </div>

      {/* Comment */}
      <div className="review-form__field">
        <label htmlFor="review-comment" className="review-form__label">
          Comentario (opcional)
        </label>
        <textarea
          id="review-comment"
          className="review-form__textarea"
          placeholder="Cuéntanos tu experiencia con este producto"
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          maxLength={2000}
          rows={5}
          disabled={loading}
        />
        <span className="review-form__char-count">
          {comment.length}/2000
        </span>
        {errors.comment && (
          <span className="review-form__error">{errors.comment}</span>
        )}
      </div>

      {/* Actions */}
      <div className="review-form__actions">
        <button
          type="button"
          className="review-form__btn review-form__btn--secondary"
          onClick={onCancel}
          disabled={loading}
        >
          Cancelar
        </button>
        <button
          type="button"
          className="review-form__btn review-form__btn--ghost"
          onClick={handleReset}
          disabled={loading}
        >
          Limpiar
        </button>
        <button
          type="submit"
          className="review-form__btn review-form__btn--primary"
          disabled={loading || rating === 0}
        >
          {loading ? 'Guardando...' : initialData ? 'Actualizar' : 'Publicar'}
        </button>
      </div>
    </form>
  );
};

export default ReviewForm;
