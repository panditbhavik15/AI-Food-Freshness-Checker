"""
ML Inference Engine.

Provides food classification and freshness prediction.
Supports two modes:
  1. Production mode: Uses a trained TensorFlow/Keras MobileNetV3 model
  2. Development mode: Uses color/texture heuristics (clearly labeled)

Per project rules: Never fabricate predictions. Dev mode is explicitly labeled.
"""

import logging
from dataclasses import dataclass
from typing import Optional

import numpy as np
from PIL import Image

from app.core import settings
from app.ml.preprocessor import get_color_statistics

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# Supported food categories
# ─────────────────────────────────────────────

SUPPORTED_FOODS = [
    "apple", "banana", "tomato", "potato",
    "orange", "carrot", "cucumber", "strawberry",
]

FRESHNESS_CLASSES = ["FRESH", "AGING", "HIGH VISIBLE SPOILAGE RISK"]

DEV_MODEL_VERSION = "dev-heuristic-v0.1"


@dataclass
class PredictionResult:
    """Structured ML prediction output."""
    food_category: str
    freshness_class: str
    confidence: float
    model_version: str
    is_food: bool = True
    is_supported: bool = True
    raw_scores: Optional[dict] = None


class FreshnessInferenceEngine:
    """
    Runs food identification and freshness classification.

    In development mode, uses color/texture heuristics on the image.
    In production mode, loads and runs the trained neural network.
    """

    def __init__(self):
        self.model = None
        self.dev_mode = settings.ML_DEV_MODE
        self.model_version = DEV_MODEL_VERSION

        if not self.dev_mode:
            self._load_model()

    def _load_model(self):
        """Load the trained TensorFlow model."""
        try:
            import tensorflow as tf
            self.model = tf.keras.models.load_model(settings.ML_MODEL_PATH)
            self.model_version = f"mobilenetv3-v1.0"
            logger.info(f"Loaded ML model from {settings.ML_MODEL_PATH}")
        except Exception as e:
            logger.warning(
                f"Failed to load ML model: {e}. Falling back to development mode."
            )
            self.dev_mode = True
            self.model_version = DEV_MODEL_VERSION

    def predict(self, image: Image.Image) -> PredictionResult:
        """
        Run food identification and freshness classification on an image.

        Args:
            image: Validated PIL Image object

        Returns:
            PredictionResult with food category, freshness class, and confidence
        """
        if self.dev_mode:
            return self._predict_heuristic(image)
        else:
            return self._predict_model(image)

    def _predict_model(self, image: Image.Image) -> PredictionResult:
        """Run prediction using the trained neural network."""
        from app.ml.preprocessor import preprocess_image

        input_array = preprocess_image(image)
        predictions = self.model.predict(input_array, verbose=0)

        # Interpret model output (depends on training setup)
        # Assuming combined classification: 8 foods × 3 freshness = 24 + 1 not-food
        top_idx = int(np.argmax(predictions[0]))
        confidence = float(np.max(predictions[0]))

        if top_idx >= len(SUPPORTED_FOODS) * len(FRESHNESS_CLASSES):
            return PredictionResult(
                food_category="unknown",
                freshness_class="UNKNOWN",
                confidence=confidence,
                model_version=self.model_version,
                is_food=False,
                is_supported=False,
            )

        food_idx = top_idx // len(FRESHNESS_CLASSES)
        freshness_idx = top_idx % len(FRESHNESS_CLASSES)

        return PredictionResult(
            food_category=SUPPORTED_FOODS[food_idx],
            freshness_class=FRESHNESS_CLASSES[freshness_idx],
            confidence=confidence,
            model_version=self.model_version,
        )

    def _predict_heuristic(self, image: Image.Image) -> PredictionResult:
        """
        Development mode: Use color/texture heuristics for prediction.

        IMPORTANT: This is NOT a real ML prediction. It is a clearly labeled
        development heuristic used for testing the application pipeline.
        All responses are tagged with model_version="dev-heuristic-v0.1".
        """
        stats = get_color_statistics(image)

        # ── Step 1: Determine most likely food based on dominant color ──
        food_category = self._identify_food_heuristic(stats)

        if food_category is None:
            return PredictionResult(
                food_category="unknown",
                freshness_class="UNKNOWN",
                confidence=0.0,
                model_version=DEV_MODEL_VERSION,
                is_food=False,
                is_supported=False,
            )

        # ── Step 2: Estimate freshness based on color degradation indicators ──
        freshness_class, confidence = self._estimate_freshness_heuristic(stats, food_category)

        return PredictionResult(
            food_category=food_category,
            freshness_class=freshness_class,
            confidence=confidence,
            model_version=DEV_MODEL_VERSION,
            raw_scores={
                "dark_ratio": stats["dark_ratio"],
                "brown_ratio": stats["brown_ratio"],
                "avg_saturation": stats["avg_saturation"],
            },
        )

    def _identify_food_heuristic(self, stats: dict) -> Optional[str]:
        """
        Simple heuristic food identification based on dominant color.

        NOTE: This is highly approximate and for development/demo only.
        It maps dominant color regions to likely food categories.
        """
        r, g, b = stats["r_mean"], stats["g_mean"], stats["b_mean"]
        sat = stats["avg_saturation"]
        brightness = stats["avg_brightness"]

        # Very low saturation or extreme brightness → likely not food
        if sat < 0.05 or brightness < 20 or brightness > 245:
            return None

        # Color-based heuristic identification
        scores = {}

        # Banana: high yellow (R≈G >> B)
        scores["banana"] = self._color_similarity(r, g, b, 210, 190, 60) * 0.8

        # Orange: orange color (R >> G > B)
        scores["orange"] = self._color_similarity(r, g, b, 230, 140, 40) * 0.8

        # Tomato: red (R >> G, B)
        scores["tomato"] = self._color_similarity(r, g, b, 200, 60, 50) * 0.8

        # Apple: red or green
        apple_red = self._color_similarity(r, g, b, 190, 50, 50)
        apple_green = self._color_similarity(r, g, b, 100, 170, 60)
        scores["apple"] = max(apple_red, apple_green) * 0.8

        # Strawberry: deep red
        scores["strawberry"] = self._color_similarity(r, g, b, 180, 40, 50) * 0.75

        # Carrot: orange (similar to orange fruit)
        scores["carrot"] = self._color_similarity(r, g, b, 240, 130, 30) * 0.75

        # Cucumber: green
        scores["cucumber"] = self._color_similarity(r, g, b, 80, 150, 60) * 0.8

        # Potato: brown/tan
        scores["potato"] = self._color_similarity(r, g, b, 180, 150, 100) * 0.7

        # Get best match
        best_food = max(scores, key=scores.get)
        best_score = scores[best_food]

        # Threshold: if no good match, return None (not food / not supported)
        if best_score < 0.15:
            return None

        return best_food

    @staticmethod
    def _color_similarity(r: float, g: float, b: float, tr: float, tg: float, tb: float) -> float:
        """Calculate color similarity (0–1) using normalized Euclidean distance."""
        dist = ((r - tr) ** 2 + (g - tg) ** 2 + (b - tb) ** 2) ** 0.5
        max_dist = (255**2 * 3) ** 0.5  # ~441
        return max(0, 1 - dist / max_dist)

    @staticmethod
    def _estimate_freshness_heuristic(stats: dict, food: str) -> tuple[str, float]:
        """
        Estimate freshness based on color degradation indicators.

        Higher dark_ratio, brown_ratio → more likely spoiled.
        Higher saturation, avg_brightness → more likely fresh.
        """
        dark = stats["dark_ratio"]
        brown = stats["brown_ratio"]
        sat = stats["avg_saturation"]
        brightness = stats["avg_brightness"]

        # Spoilage score: higher = more degraded
        spoilage_score = (dark * 0.3 + brown * 0.4 + (1 - sat) * 0.15 + max(0, (100 - brightness) / 255) * 0.15)

        # Banana is a special case: brown spots are expected during aging
        if food == "banana":
            spoilage_score *= 0.8  # Slightly more tolerant of brown

        # Potato: brown is natural color
        if food == "potato":
            spoilage_score = spoilage_score * 0.6

        # Classify
        if spoilage_score < 0.20:
            freshness = "FRESH"
            # Confidence inversely related to spoilage score
            confidence = 0.70 + (0.20 - spoilage_score) * 1.0
        elif spoilage_score < 0.45:
            freshness = "AGING"
            confidence = 0.55 + abs(0.325 - spoilage_score) * 0.8
        else:
            freshness = "HIGH VISIBLE SPOILAGE RISK"
            confidence = 0.55 + min(0.35, (spoilage_score - 0.45) * 0.7)

        # Clamp confidence
        confidence = max(0.35, min(0.95, confidence))

        return freshness, round(confidence, 2)


# ─────────────────────────────────────────────
# Singleton engine instance
# ─────────────────────────────────────────────

_engine: Optional[FreshnessInferenceEngine] = None


def get_inference_engine() -> FreshnessInferenceEngine:
    """Get or create the singleton inference engine."""
    global _engine
    if _engine is None:
        _engine = FreshnessInferenceEngine()
    return _engine
