"""
model_loader.py - Singleton and Cached Model Manager
====================================================
Loads Sentence-BERT and Cross-Encoder NLI models once into memory.
Configured for efficient CPU execution on 4GB RAM laptops.
"""

import os
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'
os.environ['HF_HUB_DISABLE_PROGRESS_BARS'] = '1'

from typing import Optional
from sentence_transformers import SentenceTransformer
from transformers import pipeline
from config.settings import SBERT_MODEL_NAME, NLI_MODEL_NAME

class ModelLoader:
    _instance: Optional['ModelLoader'] = None
    _sbert_model: Optional[SentenceTransformer] = None
    _nli_classifier = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelLoader, cls).__new__(cls)
        return cls._instance

    def get_sbert_model(self) -> SentenceTransformer:
        """Loads and caches SentenceTransformer model."""
        if self._sbert_model is None:
            print(f"[ModelLoader] Initializing S-BERT ({SBERT_MODEL_NAME})...", flush=True)
            self._sbert_model = SentenceTransformer(SBERT_MODEL_NAME)
            print("[ModelLoader] S-BERT ready.", flush=True)
        return self._sbert_model

    def get_nli_classifier(self):
        """Loads and caches Cross-Encoder NLI pipeline."""
        if self._nli_classifier is None:
            print(f"[ModelLoader] Initializing NLI Cross-Encoder ({NLI_MODEL_NAME})...", flush=True)
            self._nli_classifier = pipeline(
                "text-classification",
                model=NLI_MODEL_NAME,
                top_k=None
            )
            print("[ModelLoader] NLI Classifier ready.", flush=True)
        return self._nli_classifier
