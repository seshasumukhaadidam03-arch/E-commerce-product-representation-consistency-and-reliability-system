"""
schema.py - Structured Data Models for Product Reliability System
==================================================================
Defines validated Pydantic models for product ingestion, claims, evidence,
visual observations, and final assessment results.
"""

from typing import List, Dict, Optional, Any
from enum import Enum
from pydantic import BaseModel, Field

class FinalClassification(str, Enum):
    CONSISTENT = "CONSISTENT"
    CONTRADICTORY = "CONTRADICTORY"
    MIXED_EVIDENCE = "MIXED EVIDENCE"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT EVIDENCE"

class EvidenceVerdict(str, Enum):
    SUPPORT = "Support"
    CONTRADICTION = "Contradiction"
    NEUTRAL = "Neutral"
    CONSISTENT = "Consistent"

class AtomicClaim(BaseModel):
    claim_id: str = Field(description="Unique identifier for the claim (e.g. claim_1)")
    attribute: str = Field(description="Normalized attribute name: material, capacity, durability, color, feature")
    text: str = Field(description="The discrete, testable atomic assertion")
    value: Optional[str] = Field(default=None, description="Quantified value or spec if present")
    confidence: float = Field(default=1.0, description="Extraction confidence score (0.0 - 1.0)")
    source: str = Field(default="seller_text", description="Provenance source: seller_text, specifications, image_ocr")

class ReviewEvidence(BaseModel):
    sentence: str = Field(description="The specific factual sentence from the customer review")
    review_id: str = Field(default="", description="Identifier of the source review")
    relevance_score: float = Field(description="S-BERT semantic similarity score with the claim")
    verdict: EvidenceVerdict = Field(description="NLI logical relationship")
    confidence_scores: Dict[str, float] = Field(description="Probabilities: Support, Contradiction, Neutral")

class VisualObservation(BaseModel):
    seller_image_url: Optional[str] = None
    customer_image_url: Optional[str] = None
    color_similarity: float = Field(default=0.0, description="Color match score (0-100) via CIE-Lab")
    structural_similarity: float = Field(default=0.0, description="Structural match score (0-100) via SSIM")
    visual_consistency_score: float = Field(default=0.0, description="Weighted composite visual score")
    observations: List[str] = Field(default_factory=list, description="Factual notes on visible differences")
    available: bool = Field(default=False, description="Whether visual evidence was provided and evaluated")

class ClaimAssessment(BaseModel):
    claim: AtomicClaim
    status: str = Field(description="Claim-level outcome: Verified, Contradicted, Mixed, Unverified")
    support_count: int = 0
    contradict_count: int = 0
    neutral_count: int = 0
    consistency_percentage: float = 0.0
    evidence: List[ReviewEvidence] = Field(default_factory=list)

class UnifiedProductInput(BaseModel):
    product_id: str = "custom"
    title: str
    description: Optional[str] = ""
    features: List[str] = Field(default_factory=list)
    specifications: Dict[str, str] = Field(default_factory=dict)
    seller_images: List[str] = Field(default_factory=list)
    customer_reviews: List[Dict[str, Any]] = Field(default_factory=list)
    customer_images: List[str] = Field(default_factory=list)
    source_url: Optional[str] = None
    source_type: str = "manual"  # 'url', 'image', 'manual', 'sample'

class FinalAssessmentReport(BaseModel):
    product_id: str
    title: str
    overall_pri: float
    text_pri: float
    visual_pri: Optional[float] = None
    classification: FinalClassification
    coverage: float
    total_claims: int
    evaluated_claims: int
    claims: List[ClaimAssessment]
    visual_assessment: VisualObservation
    key_discrepancies: List[str]
    supporting_reasons: List[str]
    provenance_metadata: Dict[str, Any] = Field(default_factory=dict)
