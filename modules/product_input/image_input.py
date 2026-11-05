"""
image_input.py - Advertised Image Ingestion & Feature Extraction
===============================================================
Validates uploaded seller product photos, detects dimensions, formats,
and optionally performs OCR/heuristic attribute extraction for promotional labels.
"""

from typing import Dict, Any, Optional
import numpy as np
from PIL import Image
import io

class AdvertisedImageProcessor:
    def __init__(self, max_dimension: int = 1920):
        self.max_dimension = max_dimension

    def validate_and_load(self, image_bytes_or_path) -> Image.Image:
        """Validates that image is readable and within standard color spaces."""
        try:
            if isinstance(image_bytes_or_path, (bytes, bytearray)):
                image = Image.open(io.BytesIO(image_bytes_or_path))
            else:
                image = Image.open(image_bytes_or_path)

            image = image.convert("RGB")
            
            # Downscale if excessively large to protect student laptop RAM
            if max(image.size) > self.max_dimension:
                image.thumbnail((self.max_dimension, self.max_dimension), Image.Resampling.LANCZOS)
                
            return image
        except Exception as e:
            raise ValueError(f"Invalid or corrupted image: {e}")

    def extract_image_metadata(self, image: Image.Image) -> Dict[str, Any]:
        """Extracts technical metadata: resolution, aspect ratio, dominant color tone."""
        width, height = image.size
        img_np = np.array(image.resize((64, 64)))
        avg_rgb = np.mean(img_np, axis=(0, 1)).astype(int).tolist()

        return {
            "width": width,
            "height": height,
            "aspect_ratio": round(width / max(height, 1), 2),
            "dominant_rgb": avg_rgb,
            "valid": True
        }
