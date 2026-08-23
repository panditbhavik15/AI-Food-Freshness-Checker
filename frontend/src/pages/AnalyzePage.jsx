/**
 * AnalyzePage — Upload or capture food image for analysis.
 */

import { useState, useRef, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { analysisAPI } from '../services/api';
import CameraCapture from '../components/CameraCapture';
import './AnalyzePage.css';

export default function AnalyzePage() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [error, setError] = useState(null);
  const [cameraActive, setCameraActive] = useState(false);

  const fileInputRef = useRef(null);
  const navigate = useNavigate();

  const handleFileSelect = useCallback((file) => {
    if (!file) return;

    // Client-side validation
    const validTypes = ['image/jpeg', 'image/png', 'image/jpg'];
    if (!validTypes.includes(file.type)) {
      setError('Please upload a JPEG or PNG image.');
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      setError('Image must be under 10 MB.');
      return;
    }

    setError(null);
    setSelectedFile(file);
    setPreview(URL.createObjectURL(file));
  }, []);

  const handleInputChange = (e) => {
    handleFileSelect(e.target.files[0]);
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleCameraCapture = (file, previewUrl) => {
    setSelectedFile(file);
    setPreview(previewUrl);
    setCameraActive(false);
    setError(null);
  };

  const clearSelection = () => {
    setSelectedFile(null);
    setPreview(null);
    setError(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  const analyzeImage = async () => {
    if (!selectedFile) return;

    setAnalyzing(true);
    setError(null);

    try {
      const res = await analysisAPI.analyze(selectedFile);
      const data = res.data;

      if (data?.success && data?.data) {
        // Navigate to result page with analysis data
        navigate('/result', { state: { result: data.data } });
      } else {
        setError(data?.error?.message || 'Analysis failed. Please try again.');
        setAnalyzing(false);
      }
    } catch (err) {
      const message = err.response?.data?.error?.message
        || err.response?.data?.detail
        || 'Unable to connect to the analysis server. Please ensure the backend is running.';
      setError(message);
      setAnalyzing(false);
    }
  };

  return (
    <div className="analyze-page">
      <div className="container">
        <div className="analyze-page__header">
          <h1 className="analyze-page__title">
            Check Your <span className="gradient-text">Food</span>
          </h1>
          <p className="analyze-page__subtitle">
            Upload a photo or use your camera to analyze freshness
          </p>
        </div>

        {/* Dev mode banner */}
        <div className="dev-banner">
          <span>🧪</span> Running in development mode — AI model training in progress
        </div>

        {analyzing ? (
          <div className="analyzing" id="analyzing-state">
            <div className="analyzing__visual">
              <div className="analyzing__ring">
                <div className="analyzing__ring-inner"></div>
              </div>
              {preview && <img src={preview} alt="Analyzing" className="analyzing__image" />}
            </div>
            <h2 className="analyzing__title">Analyzing Your Food...</h2>
            <p className="analyzing__subtitle">Our AI is examining visual freshness indicators</p>
            <div className="analyzing__steps">
              <div className="analyzing__step analyzing__step--done">✓ Image validated</div>
              <div className="analyzing__step analyzing__step--active">⟳ Identifying food category</div>
              <div className="analyzing__step">○ Running freshness analysis</div>
              <div className="analyzing__step">○ Generating recommendations</div>
            </div>
          </div>
        ) : (
          <>
            {!preview ? (
              <div className="upload-area">
                {/* Camera mode */}
                {cameraActive ? (
                  <CameraCapture
                    onCapture={handleCameraCapture}
                    onClose={() => setCameraActive(false)}
                    onError={(err) => setError(err)}
                  />
                ) : (
                  <>
                    {/* Drop zone */}
                    <div
                      className={`dropzone glass-card ${dragActive ? 'dropzone--active' : ''}`}
                      onDragEnter={handleDrag}
                      onDragLeave={handleDrag}
                      onDragOver={handleDrag}
                      onDrop={handleDrop}
                      onClick={() => fileInputRef.current?.click()}
                      id="dropzone"
                    >
                      <input
                        ref={fileInputRef}
                        type="file"
                        accept="image/jpeg,image/png,image/jpg"
                        onChange={handleInputChange}
                        className="dropzone__input"
                        id="file-input"
                      />
                      <div className="dropzone__icon">📤</div>
                      <h3 className="dropzone__title">
                        Drop your food image here
                      </h3>
                      <p className="dropzone__subtitle">
                        or click to browse • JPEG, PNG • Max 10 MB
                      </p>
                    </div>

                    {/* Camera button */}
                    <button className="btn btn--secondary btn--large camera-btn" onClick={() => setCameraActive(true)} id="camera-open-btn">
                      📷 Use Camera
                    </button>
                  </>
                )}
              </div>
            ) : (
              /* Preview mode */
              <div className="preview glass-card" id="image-preview">
                <img src={preview} alt="Selected food" className="preview__image" />
                <div className="preview__actions">
                  <button className="btn btn--secondary" onClick={clearSelection}>
                    ✕ Change Image
                  </button>
                  <button className="btn btn--primary btn--large" onClick={analyzeImage} id="analyze-btn">
                    🔍 Analyze Freshness
                  </button>
                </div>
              </div>
            )}
          </>
        )}

        {error && (
          <div className="analyze-error" id="analyze-error" role="alert">
            <span>⚠️</span> {error}
          </div>
        )}

        {/* Supported foods info */}
        <div className="analyze-info glass-card">
          <h3>Supported Foods</h3>
          <div className="analyze-info__foods">
            {['🍎 Apple', '🍌 Banana', '🍅 Tomato', '🥔 Potato', '🍊 Orange', '🥕 Carrot', '🥒 Cucumber', '🍓 Strawberry'].map((f) => (
              <span key={f} className="analyze-info__food">{f}</span>
            ))}
          </div>
          <p className="analyze-info__tip">
            For best results, photograph a single food item with good lighting.
          </p>
        </div>
      </div>
    </div>
  );
}
