/**
 * ResultPage — Displays food freshness analysis results.
 */

import { useLocation, Link, useNavigate } from 'react-router-dom';
import SafetyDisclaimer from '../components/SafetyDisclaimer';
import './ResultPage.css';

const FRESHNESS_CONFIG = {
  'FRESH': {
    color: 'fresh',
    icon: '🟢',
    label: 'Fresh',
  },
  'AGING': {
    color: 'aging',
    icon: '🟡',
    label: 'Aging',
  },
  'HIGH VISIBLE SPOILAGE RISK': {
    color: 'spoiled',
    icon: '🔴',
    label: 'High Visible Spoilage Risk',
  },
};

const FOOD_EMOJIS = {
  apple: '🍎', banana: '🍌', tomato: '🍅', potato: '🥔',
  orange: '🍊', carrot: '🥕', cucumber: '🥒', strawberry: '🍓',
};

export default function ResultPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const result = location.state?.result;

  if (!result) {
    return (
      <div className="result-page">
        <div className="container result-empty">
          <h2>No Analysis Result</h2>
          <p>Please upload an image to analyze first.</p>
          <Link to="/analyze" className="btn btn--primary">
            🔍 Check Food
          </Link>
        </div>
      </div>
    );
  }

  const config = FRESHNESS_CONFIG[result.freshness] || FRESHNESS_CONFIG['AGING'];
  const foodEmoji = FOOD_EMOJIS[result.food?.toLowerCase()] || '🍽️';
  const confidencePercent = Math.round(result.confidence * 100);

  return (
    <div className="result-page">
      <div className="container">
        <div className="result animate-fade-in-up">
          {/* Header */}
          <div className="result__header">
            <div className="result__food-icon">{foodEmoji}</div>
            <h1 className="result__food-name">{result.food}</h1>
          </div>

          {/* Freshness Badge */}
          <div className={`result__freshness result__freshness--${config.color}`} id="freshness-result">
            <span className="result__freshness-icon">{config.icon}</span>
            <span className="result__freshness-label">{config.label}</span>
          </div>

          {/* Confidence */}
          <div className="result__confidence glass-card" id="confidence-display">
            <div className="result__confidence-header">
              <span>Confidence</span>
              <span className="result__confidence-value">{confidencePercent}%</span>
            </div>
            <div className="result__confidence-bar">
              <div
                className={`result__confidence-fill result__confidence-fill--${config.color}`}
                style={{ width: `${confidencePercent}%` }}
              ></div>
            </div>
            {result.confidence < 0.5 && (
              <p className="result__confidence-warning">
                ⚠️ Low confidence — consider uploading a clearer image
              </p>
            )}
          </div>

          {/* Observations */}
          <div className="result__section glass-card" id="observations-list">
            <h3 className="result__section-title">Observed Visual Indicators</h3>
            <ul className="result__observations">
              {(result.observations || []).map((obs, i) => (
                <li key={i} className="result__observation animate-fade-in-up" style={{ animationDelay: `${i * 0.1}s` }}>
                  <span className={`result__obs-dot result__obs-dot--${config.color}`}></span>
                  {obs}
                </li>
              ))}
            </ul>
          </div>

          {/* Recommendation */}
          <div className="result__section glass-card" id="recommendation-display">
            <h3 className="result__section-title">Recommendation</h3>
            <p className="result__recommendation">{result.recommendation}</p>
          </div>

          {/* Safety Disclaimer */}
          <SafetyDisclaimer notice={result.safety_notice} />

          {/* Model Info */}
          <div className="result__meta">
            <span>Model: {result.model_version}</span>
            <span>•</span>
            <span>{new Date(result.created_at).toLocaleString()}</span>
          </div>

          {/* Actions */}
          <div className="result__actions">
            <button
              className="btn btn--primary btn--large"
              onClick={() => navigate('/analyze')}
              id="check-another-btn"
            >
              🔍 Check Another Food
            </button>
            <Link to="/" className="btn btn--secondary">
              ← Back to Home
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
