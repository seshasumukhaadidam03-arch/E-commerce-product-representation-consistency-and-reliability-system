"""Product input package initialization."""
from .schema import UnifiedProductInput, AtomicClaim, ReviewEvidence, VisualObservation, FinalAssessmentReport, FinalClassification, EvidenceVerdict
from .url_parser import ProductURLExtractor
from .image_input import AdvertisedImageProcessor

__all__ = [
    "UnifiedProductInput",
    "AtomicClaim",
    "ReviewEvidence",
    "VisualObservation",
    "FinalAssessmentReport",
    "FinalClassification",
    "EvidenceVerdict",
    "ProductURLExtractor",
    "AdvertisedImageProcessor"
]
