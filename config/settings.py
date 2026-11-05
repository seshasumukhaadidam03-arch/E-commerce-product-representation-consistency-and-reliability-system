"""
settings.py - Centralized Configuration for Product Reliability Assessment System
================================================================================
Defines models, paths, thresholds, scoring weights, and environment settings.
"""

import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
SAMPLE_DATA_DIR = DATA_DIR / "sample"
BENCHMARK_DATA_DIR = DATA_DIR / "benchmark"
BENCHMARK_DATA_DIR.mkdir(parents=True, exist_ok=True)

REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# NLP Models
# all-MiniLM-L6-v2: 384-dimensional dense embeddings, 80MB RAM footprint, runs fast on CPU
SBERT_MODEL_NAME = "all-MiniLM-L6-v2"

# cross-encoder/nli-MiniLM2-L6-H768: 3-class NLI (Contradiction, Entailment, Neutral), 220MB RAM
NLI_MODEL_NAME = "cross-encoder/nli-MiniLM2-L6-H768"

# LLM Extraction Model
GEMINI_MODEL_NAME = "gemini-3.8-flash"

# Algorithmic Thresholds
SBERT_SIMILARITY_THRESHOLD = 0.28   # Minimum cosine similarity to consider review evidence relevant
NLI_CONTRADICTION_THRESHOLD = 50.0  # Confidence percentage above which evidence is flagged contradictory
NLI_SUPPORT_THRESHOLD = 40.0        # Confidence percentage above which evidence is flagged supporting
TOP_K_EVIDENCE_PER_CLAIM = 5        # Number of candidate evidence sentences to retrieve per claim

# Visual Comparison Settings
IMAGE_SIZE = (256, 256)
COLOR_DELTA_E_THRESHOLD = 25.0      # CIE-Lab Delta E threshold for perceptible color mismatch
SSIM_SIMILARITY_WEIGHT = 0.60       # Weight given to structural similarity
COLOR_SIMILARITY_WEIGHT = 0.40      # Weight given to color consistency

# PRI Engine Weights & Balances
PRI_TEXT_WEIGHT = 0.75              # Overall PRI weight allocated to textual claim verification
PRI_VISUAL_WEIGHT = 0.25            # Overall PRI weight allocated to visual photo consistency
CONTRADICTION_PENALTY_FACTOR = 1.35 # Mathematical penalty multiplier applied to contradictory evidence

# Classification Boundaries
PRI_CONSISTENT_THRESHOLD = 65.0     # PRI >= 65 with high coverage -> CONSISTENT
PRI_CONTRADICTORY_THRESHOLD = 35.0  # PRI < 35 with clear contradictions -> CONTRADICTORY
MIN_COVERAGE_REQUIRED = 0.40        # Fraction of claims with active evidence needed to avoid INSUFFICIENT
