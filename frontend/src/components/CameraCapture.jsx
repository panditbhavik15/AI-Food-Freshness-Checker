/**
 * CameraCapture — Reusable camera stream & photo capture component.
 */

import { useRef, useEffect, useCallback } from 'react';
import './CameraCapture.css';

export default function CameraCapture({ onCapture, onClose, onError }) {
  const videoRef = useRef(null);
  const streamRef = useRef(null);

  const startCamera = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'environment', width: { ideal: 1280 }, height: { ideal: 720 } },
      });
      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    } catch (err) {
      if (err.name === 'NotAllowedError') {
        onError?.('Camera access denied. Please allow camera permissions or use file upload.');
      } else {
        onError?.('Unable to access camera. Please use file upload instead.');
      }
      onClose?.();
    }
  }, [onError, onClose]);

  useEffect(() => {
    startCamera();
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop());
      }
    };
  }, [startCamera]);

  const handleCapture = () => {
    if (!videoRef.current) return;

    const canvas = document.createElement('canvas');
    canvas.width = videoRef.current.videoWidth || 640;
    canvas.height = videoRef.current.videoHeight || 480;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(videoRef.current, 0, 0);

    canvas.toBlob(
      (blob) => {
        if (blob) {
          const file = new File([blob], 'camera-capture.jpg', { type: 'image/jpeg' });
          const previewUrl = canvas.toDataURL('image/jpeg');
          onCapture(file, previewUrl);
        }
      },
      'image/jpeg',
      0.9
    );
  };

  return (
    <div className="camera glass-card" id="camera-view">
      <video ref={videoRef} autoPlay playsInline muted className="camera__video" />
      <div className="camera__controls">
        <button className="btn btn--secondary" onClick={onClose} type="button">
          Cancel
        </button>
        <button
          className="btn btn--primary camera__capture"
          onClick={handleCapture}
          id="capture-btn"
          type="button"
          aria-label="Take photo"
        >
          📸 Take Photo
        </button>
        <div style={{ width: '80px' }}></div>
      </div>
    </div>
  );
}
