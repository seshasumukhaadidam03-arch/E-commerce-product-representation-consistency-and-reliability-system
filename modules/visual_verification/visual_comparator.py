"""
visual_comparator.py - Multi-Metric Visual Consistency Engine
============================================================
Evaluates photographic consistency between seller catalog images and
customer unboxing photos using:
1. Foreground-isolated CIE-Lab color distance (Delta E)
2. Structural edge alignment and feature similarity (SSIM)
3. Quantitative perceptual observation generation
"""

import io
from typing import Optional, List, Dict, Any
import requests
import numpy as np
import cv2
from PIL import Image
from skimage.metrics import structural_similarity as ssim
from config.settings import (
    IMAGE_SIZE,
    COLOR_DELTA_E_THRESHOLD,
    SSIM_SIMILARITY_WEIGHT,
    COLOR_SIMILARITY_WEIGHT
)
from modules.preprocessing.image_preprocessor import ImagePreprocessor
from modules.product_input.schema import VisualObservation

class VisualComparator:
    def __init__(self):
        self.preprocessor = ImagePreprocessor(target_size=IMAGE_SIZE)

    def load_image_from_source(self, source: str) -> Optional[Image.Image]:
        """Loads an image from a URL or local file path."""
        try:
            if source.startswith("http://") or source.startswith("https://"):
                headers = {"User-Agent": "Mozilla/5.0"}
                resp = requests.get(source, headers=headers, timeout=6)
                resp.raise_for_status()
                return Image.open(io.BytesIO(resp.content)).convert("RGB")
            else:
                return Image.open(source).convert("RGB")
        except Exception as e:
            print(f"[VisualComparator] Failed to load image from '{source[:60]}...': {e}")
            return None

    def compare_images(
        self,
        seller_image_source: Optional[str],
        customer_image_source: Optional[str]
    ) -> VisualObservation:
        """
        Executes color and structural similarity evaluation across the two images.
        """
        if not seller_image_source or not customer_image_source:
            return VisualObservation(
                available=False,
                observations=["Insufficient visual representations provided (missing seller or customer image)."]
            )

        img_seller_pil = self.load_image_from_source(seller_image_source)
        img_cust_pil = self.load_image_from_source(customer_image_source)

        if img_seller_pil is None or img_cust_pil is None:
            return VisualObservation(
                seller_image_url=seller_image_source,
                customer_image_url=customer_image_source,
                available=False,
                observations=["Unable to download or decode one or both product images."]
            )

        # 1. Preprocess and normalize both images
        img_s_rgb = self.preprocessor.preprocess_image(img_seller_pil)
        img_c_rgb = self.preprocessor.preprocess_image(img_cust_pil)

        # 2. Extract central foreground regions (reduces studio background bias)
        fg_s = self.preprocessor.extract_central_foreground(img_s_rgb)
        fg_c = self.preprocessor.extract_central_foreground(img_c_rgb)

        observations: List[str] = []

        # =========================================================
        # METRIC A: CIE-Lab COLOR DISTANCE
        # =========================================================
        lab_s = cv2.cvtColor(fg_s, cv2.COLOR_RGB2LAB)
        lab_c = cv2.cvtColor(fg_c, cv2.COLOR_RGB2LAB)

        mean_lab_s = np.mean(lab_s, axis=(0, 1))
        mean_lab_c = np.mean(lab_c, axis=(0, 1))

        # Euclidean distance in Lab color space (Delta E approximation)
        delta_e = float(np.linalg.norm(mean_lab_s - mean_lab_c))

        # Normalize Delta E to a 0-100 color match scale
        # Delta E < 10: Barely perceptible
        # Delta E > 35: Clear color / shade discrepancy
        color_score = max(0.0, min(100.0, 100.0 - (delta_e * 2.2)))

        if delta_e > COLOR_DELTA_E_THRESHOLD:
            observations.append(
                f"Noticeable color shade discrepancy detected (Delta E: {delta_e:.1f}). "
                "Delivered product appears visibly different in tone or saturation from studio catalog."
            )
        else:
            observations.append(f"Product color tone is consistent with catalog appearance (Delta E: {delta_e:.1f}).")

        # =========================================================
        # METRIC B: STRUCTURAL SIMILARITY (SSIM)
        # =========================================================
        gray_s = cv2.cvtColor(img_s_rgb, cv2.COLOR_RGB2GRAY)
        gray_c = cv2.cvtColor(img_c_rgb, cv2.COLOR_RGB2GRAY)

        ssim_val, _ = ssim(gray_s, gray_c, full=True)
        # SSIM range is [-1, 1], normalize to [0, 100]
        structure_score = max(0.0, min(100.0, float(ssim_val * 100.0)))

        if structure_score < 30.0:
            observations.append(
                f"Low structural alignment ({structure_score:.1f}%). Possible causes: differing angle, "
                "packaging variations, or distinct physical silhouette."
            )
        else:
            observations.append(f"Structural and edge contours match reasonably ({structure_score:.1f}%).")

        # =========================================================
        # COMPOSITE VISUAL CONSISTENCY SCORE
        # =========================================================
        composite_score = round(
            (color_score * COLOR_SIMILARITY_WEIGHT) + (structure_score * SSIM_SIMILARITY_WEIGHT),
            1
        )

        return VisualObservation(
            seller_image_url=seller_image_source,
            customer_image_url=customer_image_source,
            color_similarity=round(color_score, 1),
            structural_similarity=round(structure_score, 1),
            visual_consistency_score=composite_score,
            observations=observations,
            available=True
        )
