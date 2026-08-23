/**
 * Safety Disclaimer component — always displayed on results.
 */

import './SafetyDisclaimer.css';

export default function SafetyDisclaimer({ notice }) {
  const text = notice || (
    "This is a visual AI estimate only. It is not a laboratory food-safety test. " +
    "Visual analysis cannot detect bacteria, toxins, or internal spoilage. " +
    "Always use your own judgement and follow food-safety guidelines."
  );

  return (
    <div className="disclaimer" role="alert" id="safety-disclaimer">
      <div className="disclaimer__icon">⚠️</div>
      <div className="disclaimer__content">
        <h4 className="disclaimer__title">Important Safety Notice</h4>
        <p className="disclaimer__text">{text}</p>
      </div>
    </div>
  );
}
