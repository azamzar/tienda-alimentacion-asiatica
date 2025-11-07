import React, { useState, useEffect, useRef } from 'react';
import './PriceRangeSlider.css';

/**
 * PriceRangeSlider Component
 *
 * Slider de doble rango para filtrar productos por precio.
 * Permite seleccionar un rango mínimo y máximo.
 *
 * @param {Object} props
 * @param {number} props.min - Precio mínimo disponible
 * @param {number} props.max - Precio máximo disponible
 * @param {number} props.minValue - Valor mínimo seleccionado
 * @param {number} props.maxValue - Valor máximo seleccionado
 * @param {Function} props.onChange - Callback cuando cambia el rango
 * @param {string} props.currency - Símbolo de moneda (default: '€')
 */
const PriceRangeSlider = ({
  min = 0,
  max = 100,
  minValue: initialMinValue,
  maxValue: initialMaxValue,
  onChange,
  currency = '€'
}) => {
  const [minValue, setMinValue] = useState(initialMinValue || min);
  const [maxValue, setMaxValue] = useState(initialMaxValue || max);
  const minRangeRef = useRef(null);
  const maxRangeRef = useRef(null);
  const rangeTrackRef = useRef(null);

  // Update local state when props change
  useEffect(() => {
    if (initialMinValue !== undefined) {
      setMinValue(initialMinValue);
    }
  }, [initialMinValue]);

  useEffect(() => {
    if (initialMaxValue !== undefined) {
      setMaxValue(initialMaxValue);
    }
  }, [initialMaxValue]);

  // Calculate percentage for styling
  const getPercentage = (value) => {
    return ((value - min) / (max - min)) * 100;
  };

  // Update range track visual
  useEffect(() => {
    if (rangeTrackRef.current) {
      const minPercent = getPercentage(minValue);
      const maxPercent = getPercentage(maxValue);

      rangeTrackRef.current.style.left = `${minPercent}%`;
      rangeTrackRef.current.style.width = `${maxPercent - minPercent}%`;
    }
  }, [minValue, maxValue, min, max]);

  // Handle min value change
  const handleMinChange = (e) => {
    const value = Math.min(Number(e.target.value), maxValue - 1);
    setMinValue(value);
    if (onChange) {
      onChange({ min: value, max: maxValue });
    }
  };

  // Handle max value change
  const handleMaxChange = (e) => {
    const value = Math.max(Number(e.target.value), minValue + 1);
    setMaxValue(value);
    if (onChange) {
      onChange({ min: minValue, max: value });
    }
  };

  // Reset to default range
  const handleReset = () => {
    setMinValue(min);
    setMaxValue(max);
    if (onChange) {
      onChange({ min, max });
    }
  };

  const isDefaultRange = minValue === min && maxValue === max;

  return (
    <div className="price-range-slider">
      <div className="price-range-header">
        <h4 className="price-range-title">Rango de Precio</h4>
        {!isDefaultRange && (
          <button
            className="price-range-reset"
            onClick={handleReset}
            aria-label="Restablecer rango"
          >
            ✕
          </button>
        )}
      </div>

      <div className="price-range-values">
        <div className="price-value">
          <span className="price-label">Mínimo:</span>
          <span className="price-amount">
            {minValue.toFixed(2)} {currency}
          </span>
        </div>
        <div className="price-value">
          <span className="price-label">Máximo:</span>
          <span className="price-amount">
            {maxValue.toFixed(2)} {currency}
          </span>
        </div>
      </div>

      <div className="price-range-slider-container">
        {/* Track background */}
        <div className="price-range-track">
          {/* Active track (selected range) */}
          <div
            ref={rangeTrackRef}
            className="price-range-track-active"
          />
        </div>

        {/* Min range input */}
        <input
          ref={minRangeRef}
          type="range"
          min={min}
          max={max}
          step="0.01"
          value={minValue}
          onChange={handleMinChange}
          className="price-range-input price-range-input-min"
          aria-label="Precio mínimo"
        />

        {/* Max range input */}
        <input
          ref={maxRangeRef}
          type="range"
          min={min}
          max={max}
          step="0.01"
          value={maxValue}
          onChange={handleMaxChange}
          className="price-range-input price-range-input-max"
          aria-label="Precio máximo"
        />
      </div>

      <div className="price-range-limits">
        <span>{min.toFixed(2)} {currency}</span>
        <span>{max.toFixed(2)} {currency}</span>
      </div>
    </div>
  );
};

export default PriceRangeSlider;
