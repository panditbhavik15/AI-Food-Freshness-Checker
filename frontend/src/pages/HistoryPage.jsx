/**
 * HistoryPage — Paginated list of past analyses.
 */

import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { historyAPI } from '../services/api';
import './HistoryPage.css';

const FRESHNESS_COLORS = {
  'FRESH': 'fresh',
  'AGING': 'aging',
  'HIGH VISIBLE SPOILAGE RISK': 'spoiled',
};

const FOOD_EMOJIS = {
  Apple: '🍎', Banana: '🍌', Tomato: '🍅', Potato: '🥔',
  Orange: '🍊', Carrot: '🥕', Cucumber: '🥒', Strawberry: '🍓',
};

export default function HistoryPage() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const navigate = useNavigate();

  useEffect(() => {
    fetchHistory();
  }, [page]);

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const res = await historyAPI.getList(page, 12);
      if (res.data?.success) {
        setItems(res.data.data.items);
        setTotalPages(res.data.data.total_pages);
      }
    } catch (err) {
      setError('Unable to load history. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id, e) => {
    e.stopPropagation();
    if (!confirm('Delete this analysis?')) return;
    try {
      await historyAPI.delete(id);
      setItems((prev) => prev.filter((i) => i.id !== id));
    } catch {
      setError('Failed to delete analysis.');
    }
  };

  const viewDetail = async (id) => {
    try {
      const res = await historyAPI.getDetail(id);
      if (res.data?.success) {
        navigate('/result', { state: { result: {
          ...res.data.data,
          food: res.data.data.food_category,
          freshness: res.data.data.freshness_class,
        }}});
      }
    } catch {
      setError('Unable to load analysis details.');
    }
  };

  return (
    <div className="history-page">
      <div className="container">
        <h1 className="history-page__title">
          Analysis <span className="gradient-text">History</span>
        </h1>

        {loading ? (
          <div className="history-loading">
            <div className="spinner"></div>
            <p>Loading history...</p>
          </div>
        ) : error ? (
          <div className="analyze-error">{error}</div>
        ) : items.length === 0 ? (
          <div className="history-empty glass-card">
            <div className="history-empty__icon">📋</div>
            <h3>No analyses yet</h3>
            <p>Your food freshness checks will appear here.</p>
            <button className="btn btn--primary" onClick={() => navigate('/analyze')}>
              🔍 Check Food Now
            </button>
          </div>
        ) : (
          <>
            <div className="history-grid">
              {items.map((item, i) => (
                <div
                  key={item.id}
                  className="history-card glass-card animate-fade-in-up"
                  style={{ animationDelay: `${i * 0.05}s` }}
                  onClick={() => viewDetail(item.id)}
                >
                  <div className="history-card__top">
                    <span className="history-card__emoji">
                      {FOOD_EMOJIS[item.food_category] || '🍽️'}
                    </span>
                    <button
                      className="history-card__delete"
                      onClick={(e) => handleDelete(item.id, e)}
                      title="Delete"
                    >
                      ×
                    </button>
                  </div>
                  <h3 className="history-card__food">{item.food_category}</h3>
                  <span className={`badge badge--${FRESHNESS_COLORS[item.freshness_class] || 'aging'}`}>
                    {item.freshness_class}
                  </span>
                  <div className="history-card__meta">
                    <span>{Math.round(item.confidence * 100)}% confidence</span>
                    <span>{new Date(item.created_at).toLocaleDateString()}</span>
                  </div>
                </div>
              ))}
            </div>

            {totalPages > 1 && (
              <div className="history-pagination">
                <button
                  className="btn btn--secondary"
                  disabled={page <= 1}
                  onClick={() => setPage((p) => p - 1)}
                >
                  ← Previous
                </button>
                <span>Page {page} of {totalPages}</span>
                <button
                  className="btn btn--secondary"
                  disabled={page >= totalPages}
                  onClick={() => setPage((p) => p + 1)}
                >
                  Next →
                </button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
