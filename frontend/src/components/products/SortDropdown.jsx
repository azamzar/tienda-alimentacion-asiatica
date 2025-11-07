import React from 'react';
import './SortDropdown.css';

/**
 * SortDropdown Component
 *
 * Dropdown para ordenar productos por diferentes criterios.
 *
 * @param {Object} props
 * @param {string} props.sortBy - Campo por el que se ordena (name, price, created_at, rating)
 * @param {string} props.sortOrder - Orden (asc o desc)
 * @param {Function} props.onChange - Callback cuando cambia el ordenamiento
 */
const SortDropdown = ({ sortBy = 'created_at', sortOrder = 'desc', onChange }) => {
  const sortOptions = [
    { value: 'created_at-desc', label: 'Más recientes', sortBy: 'created_at', sortOrder: 'desc', icon: '🆕' },
    { value: 'created_at-asc', label: 'Más antiguos', sortBy: 'created_at', sortOrder: 'asc', icon: '📅' },
    { value: 'name-asc', label: 'Nombre (A-Z)', sortBy: 'name', sortOrder: 'asc', icon: '🔤' },
    { value: 'name-desc', label: 'Nombre (Z-A)', sortBy: 'name', sortOrder: 'desc', icon: '🔠' },
    { value: 'price-asc', label: 'Precio: Menor a Mayor', sortBy: 'price', sortOrder: 'asc', icon: '💰' },
    { value: 'price-desc', label: 'Precio: Mayor a Menor', sortBy: 'price', sortOrder: 'desc', icon: '💎' },
    { value: 'rating-desc', label: 'Mejor valorados', sortBy: 'rating', sortOrder: 'desc', icon: '⭐' },
    { value: 'rating-asc', label: 'Peor valorados', sortBy: 'rating', sortOrder: 'asc', icon: '📉' },
  ];

  const currentValue = `${sortBy}-${sortOrder}`;
  const currentOption = sortOptions.find(opt => opt.value === currentValue) || sortOptions[0];

  const handleChange = (e) => {
    const selectedOption = sortOptions.find(opt => opt.value === e.target.value);
    if (selectedOption && onChange) {
      onChange({
        sortBy: selectedOption.sortBy,
        sortOrder: selectedOption.sortOrder
      });
    }
  };

  return (
    <div className="sort-dropdown">
      <label htmlFor="sort-select" className="sort-label">
        <span className="sort-icon">🔄</span>
        Ordenar por:
      </label>
      <div className="sort-select-wrapper">
        <select
          id="sort-select"
          className="sort-select"
          value={currentValue}
          onChange={handleChange}
        >
          {sortOptions.map((option) => (
            <option key={option.value} value={option.value}>
              {option.icon} {option.label}
            </option>
          ))}
        </select>
        <span className="sort-arrow">▼</span>
      </div>
    </div>
  );
};

export default SortDropdown;
