"""
Tests for image_validator and recommendation services.
"""

import pytest
from PIL import Image
from app.services.image_validator import validate_image, ImageValidationError
from app.services.recommendation import get_recommendation, SAFETY_NOTICE, FreshnessResult


def test_recommendation_fresh_apple():
    res = get_recommendation("apple", "FRESH")
    assert isinstance(res, FreshnessResult)
    assert res.freshness_class == "FRESH"
    assert "No obvious visual spoilage" in res.recommendation
    assert res.safety_notice == SAFETY_NOTICE
    assert len(res.observations) > 0


def test_recommendation_spoiled_banana():
    res = get_recommendation("banana", "HIGH VISIBLE SPOILAGE RISK")
    assert res.freshness_class == "HIGH VISIBLE SPOILAGE RISK"
    assert "caution" in res.recommendation.lower() or "discard" in res.recommendation.lower()


def test_validate_image_valid_jpeg(sample_image_bytes):
    img = validate_image(sample_image_bytes, "test.jpg", "image/jpeg")
    assert isinstance(img, Image.Image)


def test_validate_image_unsupported_format():
    with pytest.raises(ImageValidationError) as excinfo:
        validate_image(b"invalid data", "file.pdf", "application/pdf")
    assert excinfo.value.code == "UNSUPPORTED_FORMAT"
