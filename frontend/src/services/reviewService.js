/**
 * Review Service - API calls for product reviews
 */
import api from './api';

const reviewService = {
  /**
   * Get all reviews for a product (public)
   * @param {number} productId - Product ID
   * @param {number} skip - Number of reviews to skip (pagination)
   * @param {number} limit - Maximum number of reviews to return
   * @returns {Promise<Array>} Array of reviews
   */
  getProductReviews: async (productId, skip = 0, limit = 100) => {
    const { data } = await api.get(`/reviews/products/${productId}`, {
      params: { skip, limit }
    });
    return data;
  },

  /**
   * Get review statistics for a product (public)
   * @param {number} productId - Product ID
   * @returns {Promise<Object>} Review statistics (total_reviews, average_rating, rating_distribution)
   */
  getProductStats: async (productId) => {
    const { data } = await api.get(`/reviews/products/${productId}/stats`);
    return data;
  },

  /**
   * Get current user's review for a product (authenticated)
   * @param {number} productId - Product ID
   * @returns {Promise<Object|null>} User's review or null if not found
   */
  getMyReviewForProduct: async (productId) => {
    try {
      const { data } = await api.get(`/reviews/products/${productId}/me`);
      return data;
    } catch (error) {
      if (error.response && error.response.status === 404) {
        return null;
      }
      throw error;
    }
  },

  /**
   * Get all reviews by current user (authenticated)
   * @param {number} skip - Number of reviews to skip
   * @param {number} limit - Maximum number of reviews to return
   * @returns {Promise<Array>} Array of user's reviews
   */
  getMyReviews: async (skip = 0, limit = 100) => {
    const { data } = await api.get('/reviews/me', {
      params: { skip, limit }
    });
    return data;
  },

  /**
   * Create a new review (authenticated)
   * @param {Object} reviewData - Review data (product_id, rating, title, comment)
   * @returns {Promise<Object>} Created review
   */
  createReview: async (reviewData) => {
    const { data } = await api.post('/reviews/', reviewData);
    return data;
  },

  /**
   * Update an existing review (authenticated)
   * @param {number} reviewId - Review ID
   * @param {Object} reviewData - Updated review data (rating, title, comment)
   * @returns {Promise<Object>} Updated review
   */
  updateReview: async (reviewId, reviewData) => {
    const { data } = await api.put(`/reviews/${reviewId}`, reviewData);
    return data;
  },

  /**
   * Delete a review (authenticated)
   * @param {number} reviewId - Review ID
   * @returns {Promise<void>}
   */
  deleteReview: async (reviewId) => {
    await api.delete(`/reviews/${reviewId}`);
  }
};

export default reviewService;
