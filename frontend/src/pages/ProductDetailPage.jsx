import React from 'react';
import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { productService } from '../services/productService';
import reviewService from '../services/reviewService';
import { useCartStore } from '../store/useCartStore';
import { useAuthStore } from '../store/useAuthStore';
import { formatPrice, getImageUrl } from '../utils/formatters';
import Button from '../components/common/Button';
import Card from '../components/common/Card';
import Spinner from '../components/common/Spinner';
import RatingStars from '../components/reviews/RatingStars';
import ReviewCard from '../components/reviews/ReviewCard';
import ReviewForm from '../components/reviews/ReviewForm';
import './ProductDetailPage.css';

/**
 * Product detail page
 * Shows detailed information about a single product
 */
function ProductDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { addItem } = useCartStore();
  const { user, isAuthenticated } = useAuthStore();

  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [quantity, setQuantity] = useState(1);
  const [isAdding, setIsAdding] = useState(false);

  // Reviews state
  const [reviews, setReviews] = useState([]);
  const [reviewStats, setReviewStats] = useState(null);
  const [myReview, setMyReview] = useState(null);
  const [loadingReviews, setLoadingReviews] = useState(false);
  const [showReviewForm, setShowReviewForm] = useState(false);
  const [editingReview, setEditingReview] = useState(null);
  const [submittingReview, setSubmittingReview] = useState(false);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        setLoading(true);
        const data = await productService.getProductById(id);
        setProduct(data);
      } catch (err) {
        setError(err.message || 'Error al cargar el producto');
      } finally {
        setLoading(false);
      }
    };

    fetchProduct();
  }, [id]);

  // Load reviews and stats
  useEffect(() => {
    const loadReviews = async () => {
      if (!id) return;

      try {
        setLoadingReviews(true);

        // Load reviews and stats in parallel
        const [reviewsData, statsData, myReviewData] = await Promise.all([
          reviewService.getProductReviews(id),
          reviewService.getProductStats(id),
          isAuthenticated
            ? reviewService.getMyReviewForProduct(id).catch(() => null)
            : Promise.resolve(null)
        ]);

        setReviews(reviewsData);
        setReviewStats(statsData);
        setMyReview(myReviewData);
      } catch (err) {
        console.error('Error loading reviews:', err);
      } finally {
        setLoadingReviews(false);
      }
    };

    loadReviews();
  }, [id, isAuthenticated]);

  const handleAddToCart = async () => {
    setIsAdding(true);
    try {
      await addItem(product.id, quantity);
      // Success notification
      toast.success(
        `${quantity} ${quantity === 1 ? 'producto agregado' : 'productos agregados'} al carrito`,
        {
          icon: '🛒',
        }
      );
      // Reset quantity after adding
      setQuantity(1);
    } catch (error) {
      console.error('Error adding to cart:', error);
      // If not authenticated, redirect to login
      if (error.response?.status === 401) {
        toast.error('Debes iniciar sesión para agregar productos al carrito', {
          duration: 4000,
        });
        setTimeout(() => navigate('/login'), 1500);
      } else {
        toast.error(error.response?.data?.detail || 'Error al agregar al carrito');
      }
    } finally {
      setIsAdding(false);
    }
  };

  const handleQuantityChange = (delta) => {
    const newQuantity = quantity + delta;
    if (newQuantity >= 1 && newQuantity <= product.stock) {
      setQuantity(newQuantity);
    }
  };

  // Review handlers
  const handleSubmitReview = async (reviewData) => {
    if (!isAuthenticated) {
      toast.error('Debes iniciar sesión para escribir una reseña');
      navigate('/login');
      return;
    }

    setSubmittingReview(true);
    try {
      if (editingReview) {
        // Update existing review
        await reviewService.updateReview(editingReview.id, reviewData);
        toast.success('Reseña actualizada correctamente');
      } else {
        // Create new review
        await reviewService.createReview({
          product_id: parseInt(id),
          ...reviewData
        });
        toast.success('Reseña publicada correctamente');
      }

      // Reload reviews
      const [reviewsData, statsData, myReviewData] = await Promise.all([
        reviewService.getProductReviews(id),
        reviewService.getProductStats(id),
        reviewService.getMyReviewForProduct(id).catch(() => null)
      ]);

      setReviews(reviewsData);
      setReviewStats(statsData);
      setMyReview(myReviewData);

      // Reset form
      setShowReviewForm(false);
      setEditingReview(null);
    } catch (error) {
      console.error('Error submitting review:', error);
      const errorMsg = error.response?.data?.detail || 'Error al guardar la reseña';
      toast.error(errorMsg);
    } finally {
      setSubmittingReview(false);
    }
  };

  const handleEditReview = (review) => {
    setEditingReview(review);
    setShowReviewForm(true);
  };

  const handleDeleteReview = async (reviewId) => {
    if (!window.confirm('¿Estás seguro de que deseas eliminar tu reseña?')) {
      return;
    }

    try {
      await reviewService.deleteReview(reviewId);
      toast.success('Reseña eliminada correctamente');

      // Reload reviews
      const [reviewsData, statsData] = await Promise.all([
        reviewService.getProductReviews(id),
        reviewService.getProductStats(id)
      ]);

      setReviews(reviewsData);
      setReviewStats(statsData);
      setMyReview(null);
    } catch (error) {
      console.error('Error deleting review:', error);
      toast.error('Error al eliminar la reseña');
    }
  };

  const handleCancelReview = () => {
    setShowReviewForm(false);
    setEditingReview(null);
  };

  if (loading) {
    return (
      <div className="product-detail-page">
        <div className="product-detail-loading">
          <Spinner size="large" centered text="Cargando producto..." />
        </div>
      </div>
    );
  }

  if (error || !product) {
    return (
      <div className="product-detail-page">
        <div className="product-detail-error">
          <Card>
            <h2>Error</h2>
            <p>{error || 'Producto no encontrado'}</p>
            <Button onClick={() => navigate('/products')}>Volver a productos</Button>
          </Card>
        </div>
      </div>
    );
  }

  const isOutOfStock = product.stock === 0;
  const isLowStock = product.stock > 0 && product.stock <= 10;

  return (
    <div className="product-detail-page">
      <div className="product-detail-container">
        {/* Back button */}
        <button className="product-detail-back" onClick={() => navigate('/products')}>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <line x1="19" y1="12" x2="5" y2="12"></line>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
          Volver a productos
        </button>

        {/* Product detail */}
        <div className="product-detail-content">
          {/* Image */}
          <div className="product-detail-image-wrapper">
            <img
              src={getImageUrl(product.image_url)}
              alt={product.name}
              className="product-detail-image"
              onError={(e) => {
                // Prevent infinite loop by checking if we've already set the placeholder
                if (!e.target.src.includes('placehold.co')) {
                  e.target.src = 'https://placehold.co/600x450/f0f0f0/666?text=Producto';
                }
              }}
            />
            {isOutOfStock && (
              <div className="product-detail-badge product-detail-badge-out">Agotado</div>
            )}
            {isLowStock && !isOutOfStock && (
              <div className="product-detail-badge product-detail-badge-low">
                ¡Últimas unidades!
              </div>
            )}
          </div>

          {/* Info */}
          <div className="product-detail-info">
            {/* Category */}
            {product.category && (
              <span className="product-detail-category">{product.category.name}</span>
            )}

            {/* Name */}
            <h1 className="product-detail-name">{product.name}</h1>

            {/* Price */}
            <div className="product-detail-price">{formatPrice(product.price)}</div>

            {/* Stock */}
            <div className="product-detail-stock">
              <strong>Stock disponible:</strong>{' '}
              <span className={isLowStock ? 'text-warning' : ''}>{product.stock} unidades</span>
            </div>

            {/* Description */}
            {product.description && (
              <div className="product-detail-description">
                <h2>Descripción</h2>
                <p>{product.description}</p>
              </div>
            )}

            {/* Quantity selector */}
            {!isOutOfStock && (
              <div className="product-detail-quantity">
                <label className="product-detail-quantity-label">Cantidad:</label>
                <div className="product-detail-quantity-controls">
                  <button
                    className="product-detail-quantity-btn"
                    onClick={() => handleQuantityChange(-1)}
                    disabled={quantity <= 1}
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="20"
                      height="20"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    >
                      <line x1="5" y1="12" x2="19" y2="12"></line>
                    </svg>
                  </button>
                  <input
                    type="number"
                    className="product-detail-quantity-input"
                    value={quantity}
                    onChange={(e) => {
                      const val = parseInt(e.target.value);
                      if (val >= 1 && val <= product.stock) {
                        setQuantity(val);
                      }
                    }}
                    min="1"
                    max={product.stock}
                  />
                  <button
                    className="product-detail-quantity-btn"
                    onClick={() => handleQuantityChange(1)}
                    disabled={quantity >= product.stock}
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="20"
                      height="20"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    >
                      <line x1="12" y1="5" x2="12" y2="19"></line>
                      <line x1="5" y1="12" x2="19" y2="12"></line>
                    </svg>
                  </button>
                </div>
              </div>
            )}

            {/* Add to cart button */}
            <div className="product-detail-actions">
              <Button
                variant="primary"
                size="large"
                fullWidth
                onClick={handleAddToCart}
                disabled={isOutOfStock || isAdding}
                loading={isAdding}
              >
                {isOutOfStock ? 'Producto agotado' : 'Añadir al carrito'}
              </Button>
            </div>
          </div>
        </div>

        {/* Reviews Section */}
        <div className="product-detail-reviews">
          <div className="reviews-header">
            <h2 className="reviews-title">Reseñas y valoraciones</h2>
            {reviewStats && (
              <div className="reviews-summary">
                <div className="reviews-summary-rating">
                  <RatingStars rating={reviewStats.average_rating} size="large" />
                  <p className="reviews-summary-text">
                    {reviewStats.total_reviews} {reviewStats.total_reviews === 1 ? 'reseña' : 'reseñas'}
                  </p>
                </div>
                {reviewStats.total_reviews > 0 && (
                  <div className="reviews-distribution">
                    {[5, 4, 3, 2, 1].map((stars) => {
                      const count = reviewStats.rating_distribution[stars] || 0;
                      const percentage = reviewStats.total_reviews > 0
                        ? (count / reviewStats.total_reviews) * 100
                        : 0;

                      return (
                        <div key={stars} className="reviews-distribution-row">
                          <span className="reviews-distribution-stars">{stars} ★</span>
                          <div className="reviews-distribution-bar">
                            <div
                              className="reviews-distribution-fill"
                              style={{ width: `${percentage}%` }}
                            />
                          </div>
                          <span className="reviews-distribution-count">{count}</span>
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>
            )}
          </div>

          {/* My Review or Write Review Button */}
          {isAuthenticated && !myReview && !showReviewForm && (
            <div className="reviews-write-prompt">
              <Button onClick={() => setShowReviewForm(true)}>
                Escribir reseña
              </Button>
            </div>
          )}

          {/* Review Form */}
          {showReviewForm && (
            <ReviewForm
              initialData={editingReview}
              onSubmit={handleSubmitReview}
              onCancel={handleCancelReview}
              loading={submittingReview}
            />
          )}

          {/* My Review */}
          {myReview && !showReviewForm && (
            <div className="reviews-my-review">
              <h3 className="reviews-section-title">Tu reseña</h3>
              <ReviewCard
                review={myReview}
                isOwner={true}
                onEdit={handleEditReview}
                onDelete={handleDeleteReview}
              />
            </div>
          )}

          {/* All Reviews */}
          {loadingReviews ? (
            <div className="reviews-loading">
              <Spinner text="Cargando reseñas..." />
            </div>
          ) : (
            <>
              {reviews.length > 0 ? (
                <div className="reviews-list">
                  <h3 className="reviews-section-title">
                    Todas las reseñas ({reviews.length})
                  </h3>
                  {reviews.map((review) => (
                    <ReviewCard
                      key={review.id}
                      review={review}
                      isOwner={user?.id === review.user_id}
                      onEdit={user?.id === review.user_id ? handleEditReview : null}
                      onDelete={user?.id === review.user_id ? handleDeleteReview : null}
                    />
                  ))}
                </div>
              ) : (
                !myReview && (
                  <div className="reviews-empty">
                    <p>Aún no hay reseñas para este producto.</p>
                    {isAuthenticated ? (
                      <Button onClick={() => setShowReviewForm(true)}>
                        Sé el primero en opinar
                      </Button>
                    ) : (
                      <p>
                        <Button onClick={() => navigate('/login')}>Inicia sesión</Button> para
                        escribir la primera reseña.
                      </p>
                    )}
                  </div>
                )
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default ProductDetailPage;
