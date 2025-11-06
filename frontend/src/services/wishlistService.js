/**
 * Wishlist Service - API calls for user's wishlist/favorites
 */
import api from './api';

const wishlistService = {
  /**
   * Get current user's wishlist
   * @param {number} skip - Number of items to skip (pagination)
   * @param {number} limit - Maximum number of items to return
   * @returns {Promise<Array>} Array of wishlist items with product details
   */
  getWishlist: async (skip = 0, limit = 100) => {
    const { data } = await api.get('/wishlist/me', {
      params: { skip, limit }
    });
    return data;
  },

  /**
   * Get count of items in wishlist
   * @returns {Promise<number>} Count of wishlist items
   */
  getWishlistCount: async () => {
    const { data } = await api.get('/wishlist/me/count');
    return data.count;
  },

  /**
   * Check if a product is in wishlist
   * @param {number} productId - Product ID
   * @returns {Promise<boolean>} True if product is in wishlist
   */
  checkInWishlist: async (productId) => {
    const { data } = await api.get(`/wishlist/me/check/${productId}`);
    return data.in_wishlist;
  },

  /**
   * Add a product to wishlist
   * @param {number} productId - Product ID
   * @returns {Promise<Object>} Created wishlist item
   */
  addToWishlist: async (productId) => {
    const { data } = await api.post('/wishlist/me', {
      product_id: productId
    });
    return data;
  },

  /**
   * Add multiple products to wishlist
   * @param {Array<number>} productIds - Array of product IDs
   * @returns {Promise<Object>} Result with added/failed items
   */
  bulkAddToWishlist: async (productIds) => {
    const { data } = await api.post('/wishlist/me/bulk', {
      product_ids: productIds
    });
    return data;
  },

  /**
   * Remove a product from wishlist
   * @param {number} productId - Product ID
   * @returns {Promise<void>}
   */
  removeFromWishlist: async (productId) => {
    await api.delete(`/wishlist/me/${productId}`);
  },

  /**
   * Clear all items from wishlist
   * @returns {Promise<void>}
   */
  clearWishlist: async () => {
    await api.delete('/wishlist/me');
  }
};

export default wishlistService;
