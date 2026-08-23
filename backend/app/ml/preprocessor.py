"""
Image preprocessor for the ML pipeline.

Handles resizing, normalization, and format conversion.
"""

import io
import numpy as np
from PIL import Image


# Model input dimensions
INPUT_SIZE = (224, 224)


def preprocess_image(image: Image.Image) -> np.ndarray:
    """
    Preprocess a PIL Image for model inference.

    Steps:
    1. Convert to RGB (handle RGBA, grayscale, etc.)
    2. Resize to 224×224
    3. Convert to float32 array
    4. Normalize pixel values to [0, 1]

    Args:
        image: PIL Image object (already validated)

    Returns:
        NumPy array of shape (1, 224, 224, 3) with float32 values in [0, 1]
    """
    # Ensure RGB mode
    if image.mode != "RGB":
        image = image.convert("RGB")

    # Resize with high-quality resampling
    image = image.resize(INPUT_SIZE, Image.Resampling.LANCZOS)

    # Convert to numpy array
    img_array = np.array(image, dtype=np.float32)

    # Normalize to [0, 1]
    img_array = img_array / 255.0

    # Add batch dimension: (224, 224, 3) → (1, 224, 224, 3)
    img_array = np.expand_dims(img_array, axis=0)

    return img_array


def get_color_statistics(image: Image.Image) -> dict:
    """
    Extract color statistics from an image for the heuristic analyzer.

    Returns HSV channel statistics and brown/dark pixel ratios.
    """
    # Resize for performance
    small = image.convert("RGB").resize((100, 100), Image.Resampling.LANCZOS)
    pixels = np.array(small, dtype=np.float32)

    # RGB statistics
    r_mean, g_mean, b_mean = pixels[:, :, 0].mean(), pixels[:, :, 1].mean(), pixels[:, :, 2].mean()

    # Convert to HSV-like analysis
    # Detect brown/dark pixels (low brightness, warm hue)
    brightness = pixels.mean(axis=2)
    dark_ratio = (brightness < 80).mean()  # Fraction of dark pixels
    very_dark_ratio = (brightness < 40).mean()

    # Detect brownish pixels (R > G > B pattern with low saturation)
    brown_mask = (
        (pixels[:, :, 0] > pixels[:, :, 1])
        & (pixels[:, :, 1] > pixels[:, :, 2])
        & (brightness < 150)
        & (brightness > 40)
    )
    brown_ratio = brown_mask.mean()

    # Detect green pixels (freshness indicator for some produce)
    green_mask = (
        (pixels[:, :, 1] > pixels[:, :, 0])
        & (pixels[:, :, 1] > pixels[:, :, 2])
    )
    green_ratio = green_mask.mean()

    # Detect vibrant/saturated colors
    max_channel = pixels.max(axis=2)
    min_channel = pixels.min(axis=2)
    saturation = np.where(max_channel > 0, (max_channel - min_channel) / max_channel, 0)
    avg_saturation = saturation.mean()

    # Color variance (uniformity)
    color_std = pixels.std()

    return {
        "r_mean": float(r_mean),
        "g_mean": float(g_mean),
        "b_mean": float(b_mean),
        "dark_ratio": float(dark_ratio),
        "very_dark_ratio": float(very_dark_ratio),
        "brown_ratio": float(brown_ratio),
        "green_ratio": float(green_ratio),
        "avg_saturation": float(avg_saturation),
        "color_std": float(color_std),
        "avg_brightness": float(brightness.mean()),
    }
