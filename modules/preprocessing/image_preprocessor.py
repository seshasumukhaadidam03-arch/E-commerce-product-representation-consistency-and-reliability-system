"""
image_preprocessor.py - Image Normalization and Foreground Isolation
====================================================================
Preprocesses seller and customer images for color and structural comparison:
resizes with aspect-ratio preserving padding, and isolates central product regions.
"""

from typing import Tuple, Optional
import numpy as np
import cv2
from PIL import Image

class ImagePreprocessor:
    def __init__(self, target_size: Tuple[int, int] = (256, 256)):
        self.target_size = target_size

    def preprocess_image(self, image: Image.Image) -> np.ndarray:
        """
        Converts PIL Image to RGB numpy array, resizes to target_size with letterbox padding.
        """
        img_np = np.array(image.convert("RGB"))
        h, w = img_np.shape[:2]
        target_w, target_h = self.target_size

        scale = min(target_w / w, target_h / h)
        new_w = int(w * scale)
        new_h = int(h * scale)

        resized = cv2.resize(img_np, (new_w, new_h), interpolation=cv2.INTER_AREA)

        # Create neutral gray canvas
        canvas = np.full((target_h, target_w, 3), 128, dtype=np.uint8)
        x_offset = (target_w - new_w) // 2
        y_offset = (target_h - new_h) // 2

        canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized
        return canvas

    def extract_central_foreground(self, img_rgb: np.ndarray) -> np.ndarray:
        """
        Extracts central crop (60% region) to minimize studio or table background bias.
        """
        h, w = img_rgb.shape[:2]
        start_y = int(h * 0.20)
        end_y = int(h * 0.80)
        start_x = int(w * 0.20)
        end_x = int(w * 0.80)
        return img_rgb[start_y:end_y, start_x:end_x]
