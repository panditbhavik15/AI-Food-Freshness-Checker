/**
 * DashboardPage — User analytics overview.
 */

import { useState, useEffect } from 'react';
import { dashboardAPI } from '../services/api';
import './DashboardPage.css';

const FRESHNESS_COLORS = {
  'FRESH': '#22c55e',
  'AGING': '#f59e0b',
  'HIGH VISIBLE SPOILAGE RISK': '#ef4444',
};

export default function DashboardPage() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    dashboardAPI.getStats()
      .then((res) => {
        if (res.data?.success) setStats(res.data.data);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="dashboard-page">
        <div className="container">
          <div className="history-loading">
            <div className="spinner"></div>
            <p>Loading dashboard...</p>
          </div>
        </div>
      </div>
    );
  }

  const total = stats?.total_scans || 0;
  const distribution = stats?.freshness_distribution || {};
  const topFoods = stats?.top_foods || [];
  const recent = stats?.recent_analyses || [];

  // Calculate percentages for chart
  const distributionEntries = Object.entries(distribution);
  const chartTotal = distributionEntries.reduce((sum, [, count]) => sum + count, 0) || 1;

  return (
    <div className="dashboard-page">
      <div className="container">
        <h1 className="dashboard-page__title">
          Your <span className="gradient-text">Dashboard</span>
        </h1>

        {/* Stat Cards */}
        <div className="stat-cards">
          <div className="stat-card glass-card animate-fade-in-up">
            <div className="stat-card__icon">📊</div>
            <div className="stat-card__value">{total}</div>
            <div className="stat-card__label">Total Scans</div>
          </div>
          <div className="stat-card glass-card animate-fade-in-up stagger-1">
            <div className="stat-card__icon">🟢</div>
            <div className="stat-card__value">{distribution['FRESH'] || 0}</div>
            <div className="stat-card__label">Fresh</div>
          </div>
          <div className="stat-card glass-card animate-fade-in-up stagger-2">
            <div className="stat-card__icon">🟡</div>
            <div className="stat-card__value">{distribution['AGING'] || 0}</div>
            <div className="stat-card__label">Aging</div>
          </div>
          <div className="stat-card glass-card animate-fade-in-up stagger-3">
            <div className="stat-card__icon">🔴</div>
            <div className="stat-card__value">{distribution['HIGH VISIBLE SPOILAGE RISK'] || 0}</div>
            <div className="stat-card__label">Spoilage Risk</div>
          </div>
        </div>

        <div className="dashboard-grid">
          {/* Freshness Distribution */}
          <div className="dashboard-card glass-card animate-fade-in-up">
            <h3>Freshness Distribution</h3>
            <div className="chart-bar-container">
              {distributionEntries.map(([label, count]) => (
                <div key={label} className="chart-bar-row">
                  <span className="chart-bar-label">{label}</span>
                  <div className="chart-bar-track">
                    <div
                      className="chart-bar-fill"
                      style={{
                        width: `${(count / chartTotal) * 100}%`,
                        background: FRESHNESS_COLORS[label] || '#64748b',
                      }}
                    ></div>
                  </div>
                  <span className="chart-bar-count">{count}</span>
                </div>
              ))}
              {distributionEntries.length === 0 && (
                <p className="chart-empty">No data yet. Start checking food!</p>
              )}
            </div>
          </div>

          {/* Top Foods */}
          <div className="dashboard-card glass-card animate-fade-in-up stagger-1">
            <h3>Most Checked Foods</h3>
            <div className="top-foods">
              {topFoods.map((food, i) => (
                <div key={food.name} className="top-food-row">
                  <span className="top-food-rank">#{i + 1}</span>
                  <span className="top-food-name">{food.name}</span>
                  <span className="top-food-count">{food.count} scans</span>
                </div>
              ))}
              {topFoods.length === 0 && (
                <p className="chart-empty">No data yet.</p>
              )}
            </div>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="dashboard-card glass-card animate-fade-in-up stagger-2">
          <h3>Recent Activity</h3>
          {recent.length === 0 ? (
            <p className="chart-empty">No recent analyses.</p>
          ) : (
            <div className="recent-list">
              {recent.map((item) => (
                <div key={item.id} className="recent-item">
                  <span className="recent-item__food">{item.food_category}</span>
                  <span className={`badge badge--${
                    item.freshness_class === 'FRESH' ? 'fresh'
                    : item.freshness_class === 'AGING' ? 'aging' : 'spoiled'
                  }`}>
                    {item.freshness_class}
                  </span>
                  <span className="recent-item__confidence">{Math.round(item.confidence * 100)}%</span>
                  <span className="recent-item__date">
                    {new Date(item.created_at).toLocaleDateString()}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
