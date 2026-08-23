"""
Image validation service.

Validates uploaded images for format, size, dimensions, and basic quality.
"""

import io
import struct
from pathlib import Path

from PIL import Image

from app.core import settings


# Supported MIME types and their magic bytes
SUPPORTED_TYPES = {
    "image/jpeg": [b"\xff\xd8\xff"],
    "image/png": [b"\x89PNG\r\n\x1a\n"],
}

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

MIN_DIMENSION = 224  # Minimum width/height in pixels
MAX_DIMENSION = 8192  # Maximum width/height


class ImageValidationError(Exception):
    """Raised when image validation fails."""

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(message)


def validate_image(file_bytes: bytes, filename: str, content_type: str) -> Image.Image:
    """
    Validate an uploaded image file.

    Checks: file size, extension, magic bytes, dimensions, corruption.
    Returns a PIL Image object if valid.
    Raises ImageValidationError with specific code and message on failure.
    """
    # 1. Check file size
    if len(file_bytes) > settings.max_upload_bytes:
        raise ImageValidationError(
            "FILE_TOO_LARGE",
            f"Image exceeds maximum size of {settings.MAX_UPLOAD_SIZE_MB} MB.",
        )

    if len(file_bytes) == 0:
        raise ImageValidationError("EMPTY_FILE", "The uploaded file is empty.")

    # 2. Check file extension
    ext = Path(filename).suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise ImageValidationError(
            "UNSUPPORTED_FORMAT",
            f"Unsupported image format '{ext}'. Please upload a JPEG or PNG file.",
        )

    # 3. Verify magic bytes match claimed content type
    if not _verify_magic_bytes(file_bytes, content_type):
        raise ImageValidationError(
            "INVALID_CONTENT",
            "File content does not match the expected image format.",
        )

    # 4. Try opening with PIL to check for corruption
    try:
        image = Image.open(io.BytesIO(file_bytes))
        image.verify()
        # Re-open after verify (verify closes the image)
        image = Image.open(io.BytesIO(file_bytes))
    except Exception:
        raise ImageValidationError(
            "CORRUPTED_IMAGE", "The image file appears to be corrupted."
        )

    # 5. Check dimensions
    width, height = image.size
    if width < MIN_DIMENSION or height < MIN_DIMENSION:
        raise ImageValidationError(
            "IMAGE_TOO_SMALL",
            f"Image is too small ({width}×{height}). Minimum size is {MIN_DIMENSION}×{MIN_DIMENSION} pixels.",
        )

    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        raise ImageValidationError(
            "IMAGE_TOO_LARGE",
            f"Image dimensions are too large ({width}×{height}). Maximum is {MAX_DIMENSION}×{MAX_DIMENSION} pixels.",
        )

    # 6. Check for blank/solid color images
    if _is_blank_image(image):
        raise ImageValidationError(
            "BLANK_IMAGE",
            "The image appears to be blank or a solid color. Please upload a photo of food.",
        )

    return image


def _verify_magic_bytes(file_bytes: bytes, content_type: str) -> bool:
    """Check if file magic bytes match the claimed content type."""
    # Accept any supported type if content-type is generic
    if content_type in ("application/octet-stream", ""):
        for magic_list in SUPPORTED_TYPES.values():
            for magic in magic_list:
                if file_bytes[:len(magic)] == magic:
                    return True
        return False

    magic_list = SUPPORTED_TYPES.get(content_type, [])
    if not magic_list:
        # Check if it matches any supported type
        for supported_magic_list in SUPPORTED_TYPES.values():
            for magic in supported_magic_list:
                if file_bytes[:len(magic)] == magic:
                    return True
        return False

    return any(file_bytes[:len(m)] == m for m in magic_list)


def _is_blank_image(image: Image.Image, threshold: float = 0.05) -> bool:
    """
    Detect if an image is predominantly a single color (blank).
    Uses standard deviation of pixel values.
    """
    try:
        # Convert to RGB if not already
        rgb = image.convert("RGB")
        # Sample a subset for performance
        small = rgb.resize((50, 50))
        import numpy as np

        pixels = np.array(small, dtype=np.float32)
        std = pixels.std()
        # Very low std means very uniform (blank) image
        return std < (255 * threshold)
    except Exception:
        return False
