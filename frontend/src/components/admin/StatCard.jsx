import React from 'react';
import './StatCard.css';

/**
 * Componente de tarjeta de estadística para el dashboard
 * Muestra una métrica con título, valor, icono y tendencia opcional
 */
function StatCard({ title, value, icon, color = 'blue', trend, subtitle }) {
  return (
    <div className={`stat-card stat-card-${color}`}>
      <div className="stat-card-header">
        <div className="stat-card-info">
          <p className="stat-card-title">{title}</p>
          <h3 className="stat-card-value">{value}</h3>
          {subtitle && <p className="stat-card-subtitle">{subtitle}</p>}
        </div>
        {icon && (
          <div className="stat-card-icon">
            {icon}
          </div>
        )}
      </div>
      {trend && (
        <div className={`stat-card-trend stat-card-trend-${trend.type}`}>
          <span className="stat-card-trend-icon">
            {trend.type === 'up' ? '↑' : trend.type === 'down' ? '↓' : '→'}
          </span>
          <span className="stat-card-trend-text">{trend.text}</span>
        </div>
      )}
    </div>
  );
}

export default StatCard;
