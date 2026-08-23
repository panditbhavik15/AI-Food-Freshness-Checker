/**
 * HomePage — Landing page with hero, how-it-works, and CTA.
 */

import { Link } from 'react-router-dom';
import './HomePage.css';

const SUPPORTED_FOODS = [
  { emoji: '🍎', name: 'Apple' },
  { emoji: '🍌', name: 'Banana' },
  { emoji: '🍅', name: 'Tomato' },
  { emoji: '🥔', name: 'Potato' },
  { emoji: '🍊', name: 'Orange' },
  { emoji: '🥕', name: 'Carrot' },
  { emoji: '🥒', name: 'Cucumber' },
  { emoji: '🍓', name: 'Strawberry' },
];

const STEPS = [
  {
    icon: '📸',
    title: 'Upload or Capture',
    description: 'Take a photo or upload an image of your food item.',
  },
  {
    icon: '🤖',
    title: 'AI Analysis',
    description: 'Our AI visually analyzes freshness indicators in seconds.',
  },
  {
    icon: '📊',
    title: 'Get Results',
    description: 'Receive freshness classification, observations, and recommendations.',
  },
];

export default function HomePage() {
  return (
    <div className="home">
      {/* Hero Section */}
      <section className="hero" id="hero-section">
        <div className="hero__glow"></div>
        <div className="hero__glow hero__glow--blue"></div>
        <div className="hero__content container">
          <div className="hero__badge animate-fade-in-up">
            <span className="badge badge--fresh">✨ AI-Powered Visual Analysis</span>
          </div>

          <h1 className="hero__title animate-fade-in-up stagger-1">
            AI Food<br />
            <span className="gradient-text">Freshness Checker</span>
          </h1>

          <p className="hero__subtitle animate-fade-in-up stagger-2">
            Check visible freshness indicators before you waste food.
            Upload a photo and get an instant AI-powered visual estimate.
          </p>

          <div className="hero__cta animate-fade-in-up stagger-3">
            <Link to="/analyze" className="btn btn--primary btn--large" id="cta-check-food">
              🔍 Check Food Now
            </Link>
            <Link to="/analyze" className="btn btn--secondary btn--large" id="cta-upload">
              📤 Upload Image
            </Link>
          </div>

          <p className="hero__disclaimer animate-fade-in-up stagger-4">
            Visual AI estimate only — not a food safety test.
          </p>
        </div>
      </section>

      {/* How It Works */}
      <section className="how-it-works container" id="how-it-works">
        <h2 className="section-title">How It Works</h2>
        <p className="section-subtitle">Three simple steps to check your food</p>

        <div className="steps">
          {STEPS.map((step, i) => (
            <div key={i} className="step glass-card animate-fade-in-up" style={{ animationDelay: `${i * 0.15}s` }}>
              <div className="step__number">{i + 1}</div>
              <div className="step__icon">{step.icon}</div>
              <h3 className="step__title">{step.title}</h3>
              <p className="step__desc">{step.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Supported Foods */}
      <section className="supported container" id="supported-foods">
        <h2 className="section-title">Supported Foods</h2>
        <p className="section-subtitle">Currently analyzing freshness for these categories</p>

        <div className="food-grid">
          {SUPPORTED_FOODS.map((food, i) => (
            <div
              key={food.name}
              className="food-item glass-card animate-fade-in-up"
              style={{ animationDelay: `${i * 0.08}s` }}
            >
              <span className="food-item__emoji">{food.emoji}</span>
              <span className="food-item__name">{food.name}</span>
            </div>
          ))}
        </div>
      </section>

      {/* Freshness Classes */}
      <section className="classes container" id="freshness-classes">
        <h2 className="section-title">Freshness Classifications</h2>
        <p className="section-subtitle">Our AI detects three levels of visual freshness</p>

        <div className="class-cards">
          <div className="class-card glass-card">
            <div className="class-card__indicator class-card__indicator--fresh"></div>
            <h3 className="class-card__title">Fresh</h3>
            <p className="class-card__desc">No obvious visual spoilage detected. Food appears vibrant and firm.</p>
          </div>
          <div className="class-card glass-card">
            <div className="class-card__indicator class-card__indicator--aging"></div>
            <h3 className="class-card__title">Aging</h3>
            <p className="class-card__desc">Visible signs of aging. Consider using soon and inspect carefully.</p>
          </div>
          <div className="class-card glass-card">
            <div className="class-card__indicator class-card__indicator--spoiled"></div>
            <h3 className="class-card__title">High Visible Spoilage Risk</h3>
            <p className="class-card__desc">Significant visual degradation. Exercise caution before consuming.</p>
          </div>
        </div>
      </section>

      {/* Footer CTA */}
      <section className="footer-cta container">
        <div className="footer-cta__card glass-card">
          <h2>Ready to check your food?</h2>
          <p>Upload a photo and get an instant visual freshness estimate.</p>
          <Link to="/analyze" className="btn btn--primary btn--large">
            🍃 Start Checking
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        <div className="container">
          <p className="footer__text">
            © 2026 FreshCheck — AI Food Freshness Checker.
            Visual AI estimate only. Not a food safety test.
          </p>
        </div>
      </footer>
    </div>
  );
}
