import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { productService } from '../../services/productService';
import './SearchAutocomplete.css';

/**
 * SearchAutocomplete Component
 *
 * Componente de búsqueda con autocompletado en tiempo real.
 * Muestra sugerencias de productos mientras el usuario escribe.
 *
 * @param {Object} props
 * @param {string} props.placeholder - Placeholder del input
 * @param {Function} props.onSearch - Callback cuando se hace una búsqueda
 * @param {Function} props.onClear - Callback cuando se limpia la búsqueda
 * @param {string} props.initialValue - Valor inicial del input
 */
const SearchAutocomplete = ({
  placeholder = 'Buscar productos...',
  onSearch,
  onClear,
  initialValue = ''
}) => {
  const [query, setQuery] = useState(initialValue);
  const [suggestions, setSuggestions] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(-1);

  const navigate = useNavigate();
  const inputRef = useRef(null);
  const suggestionsRef = useRef(null);
  const debounceTimer = useRef(null);

  // Fetch suggestions con debounce
  const fetchSuggestions = useCallback(async (searchQuery) => {
    if (!searchQuery || searchQuery.length < 2) {
      setSuggestions([]);
      return;
    }

    setIsLoading(true);
    try {
      const results = await productService.autocomplete(searchQuery, 5);
      setSuggestions(results);
      setShowSuggestions(true);
    } catch (error) {
      console.error('Error fetching suggestions:', error);
      setSuggestions([]);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Handle input change con debounce
  const handleInputChange = (e) => {
    const value = e.target.value;
    setQuery(value);
    setSelectedIndex(-1);

    // Clear previous timer
    if (debounceTimer.current) {
      clearTimeout(debounceTimer.current);
    }

    // Set new timer (300ms debounce)
    debounceTimer.current = setTimeout(() => {
      fetchSuggestions(value);
    }, 300);
  };

  // Handle search submit
  const handleSearch = (e) => {
    e.preventDefault();
    if (query.trim()) {
      setShowSuggestions(false);
      if (onSearch) {
        onSearch(query.trim());
      }
      inputRef.current?.blur();
    }
  };

  // Handle clear
  const handleClear = () => {
    setQuery('');
    setSuggestions([]);
    setShowSuggestions(false);
    setSelectedIndex(-1);
    if (onClear) {
      onClear();
    }
    inputRef.current?.focus();
  };

  // Handle suggestion click
  const handleSuggestionClick = (product) => {
    setQuery(product.name);
    setShowSuggestions(false);
    navigate(`/products/${product.id}`);
  };

  // Handle keyboard navigation
  const handleKeyDown = (e) => {
    if (!showSuggestions || suggestions.length === 0) {
      return;
    }

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setSelectedIndex((prev) =>
          prev < suggestions.length - 1 ? prev + 1 : prev
        );
        break;

      case 'ArrowUp':
        e.preventDefault();
        setSelectedIndex((prev) => (prev > 0 ? prev - 1 : -1));
        break;

      case 'Enter':
        if (selectedIndex >= 0 && selectedIndex < suggestions.length) {
          e.preventDefault();
          handleSuggestionClick(suggestions[selectedIndex]);
        }
        break;

      case 'Escape':
        setShowSuggestions(false);
        setSelectedIndex(-1);
        break;

      default:
        break;
    }
  };

  // Close suggestions when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        suggestionsRef.current &&
        !suggestionsRef.current.contains(event.target) &&
        !inputRef.current.contains(event.target)
      ) {
        setShowSuggestions(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Clean up debounce timer on unmount
  useEffect(() => {
    return () => {
      if (debounceTimer.current) {
        clearTimeout(debounceTimer.current);
      }
    };
  }, []);

  // Highlight matching text
  const highlightText = (text, highlight) => {
    if (!highlight.trim()) {
      return text;
    }

    const regex = new RegExp(`(${highlight})`, 'gi');
    const parts = text.split(regex);

    return parts.map((part, index) =>
      regex.test(part) ? (
        <mark key={index} className="search-highlight">{part}</mark>
      ) : (
        part
      )
    );
  };

  return (
    <div className="search-autocomplete">
      <form className="search-form" onSubmit={handleSearch}>
        <div className="search-input-wrapper">
          <span className="search-icon">🔍</span>
          <input
            ref={inputRef}
            type="text"
            className="search-input"
            placeholder={placeholder}
            value={query}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            onFocus={() => query.length >= 2 && setShowSuggestions(true)}
            autoComplete="off"
          />
          {query && (
            <button
              type="button"
              className="search-clear"
              onClick={handleClear}
              aria-label="Limpiar búsqueda"
            >
              ✕
            </button>
          )}
          {isLoading && (
            <div className="search-loader">
              <div className="spinner-small"></div>
            </div>
          )}
        </div>

        <button type="submit" className="search-button">
          Buscar
        </button>
      </form>

      {/* Suggestions dropdown */}
      {showSuggestions && suggestions.length > 0 && (
        <div ref={suggestionsRef} className="search-suggestions">
          {suggestions.map((product, index) => (
            <button
              key={product.id}
              className={`search-suggestion-item ${
                index === selectedIndex ? 'selected' : ''
              }`}
              onClick={() => handleSuggestionClick(product)}
              onMouseEnter={() => setSelectedIndex(index)}
            >
              <div className="suggestion-image">
                {product.image_url ? (
                  <img src={product.image_url} alt={product.name} />
                ) : (
                  <div className="suggestion-image-placeholder">📦</div>
                )}
              </div>
              <div className="suggestion-content">
                <div className="suggestion-name">
                  {highlightText(product.name, query)}
                </div>
                <div className="suggestion-price">
                  {product.price.toFixed(2)} €
                </div>
              </div>
              {product.stock === 0 && (
                <span className="suggestion-badge">Agotado</span>
              )}
            </button>
          ))}
        </div>
      )}

      {/* No results message */}
      {showSuggestions && query.length >= 2 && !isLoading && suggestions.length === 0 && (
        <div ref={suggestionsRef} className="search-suggestions">
          <div className="search-no-results">
            No se encontraron productos
          </div>
        </div>
      )}
    </div>
  );
};

export default SearchAutocomplete;
