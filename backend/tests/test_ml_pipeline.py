"""
Tests for ML inference engine and image preprocessing.
"""

from PIL import Image
from app.ml.preprocessor import preprocess_image
from app.ml.inference import get_inference_engine, PredictionResult


def test_image_preprocessing():
    img = Image.new("RGB", (500, 400), color=(150, 75, 50))
    tensor = preprocess_image(img)
    assert tensor.shape == (1, 224, 224, 3)
    assert tensor.dtype.name.startswith("float")


def test_inference_engine_prediction():
    engine = get_inference_engine()
    # Yellow green color resembling a fresh banana / fruit
    img = Image.new("RGB", (300, 300), color=(210, 190, 60))
    result = engine.predict(img)

    assert isinstance(result, PredictionResult)
    assert hasattr(result, "food_category")
    assert hasattr(result, "freshness_class")
    assert hasattr(result, "confidence")
    assert 0.0 <= result.confidence <= 1.0
    assert result.freshness_class in ["FRESH", "AGING", "HIGH VISIBLE SPOILAGE RISK", "UNKNOWN"]
