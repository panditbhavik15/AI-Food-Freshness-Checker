"""
Image utility functions.

EXIF stripping, thumbnail creation, and file storage.
"""

import io
import uuid
from pathlib import Path

from PIL import Image, ExifTags

from app.core import settings


def strip_exif(image: Image.Image) -> Image.Image:
    """
    Remove EXIF metadata from an image to prevent location leakage.

    Creates a clean copy without any metadata.
    """
    clean = Image.new(image.mode, image.size)
    clean.putdata(list(image.getdata()))
    return clean


def create_thumbnail(image: Image.Image, image_id: str, size: tuple = (200, 200)) -> Path | None:
    """
    Create a thumbnail version of the image for history display.

    Args:
        image: Source PIL Image
        image_id: Unique identifier for file naming
        size: Thumbnail dimensions (default 200×200)

    Returns:
        Path to saved thumbnail, or None if creation fails
    """
    try:
        thumb = image.copy()
        thumb.thumbnail(size, Image.Resampling.LANCZOS)

        thumb_dir = settings.upload_path / "thumbnails"
        thumb_dir.mkdir(parents=True, exist_ok=True)
        thumb_path = thumb_dir / f"{image_id}_thumb.jpg"

        thumb.convert("RGB").save(thumb_path, "JPEG", quality=80)
        return thumb_path
    except Exception:
        return None


def save_image(file_bytes: bytes, image_id: str) -> Path:
    """
    Save uploaded image to the configured upload directory.

    Args:
        file_bytes: Raw image file bytes
        image_id: Unique identifier for file naming

    Returns:
        Path to saved image
    """
    upload_dir = settings.upload_path / "images"
    upload_dir.mkdir(parents=True, exist_ok=True)

    # Detect format from bytes
    if file_bytes[:4] == b"\x89PNG":
        ext = ".png"
    else:
        ext = ".jpg"

    image_path = upload_dir / f"{image_id}{ext}"
    image_path.write_bytes(file_bytes)

    return image_path
