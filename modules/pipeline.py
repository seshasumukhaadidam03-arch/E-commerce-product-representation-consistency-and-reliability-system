"""
pipeline.py - Central Assessment Pipeline Orchestrator
======================================================
Connects all submodules:
Input Ingestion -> Text Preprocessing -> Claim Extraction ->
Semantic Evidence Retrieval -> NLI Verification -> Visual Verification ->
PRI Calculation -> 4-State Classification.
"""

from typing import Dict, Any, List, Optional
from modules.product_input.schema import (
    UnifiedProductInput,
    FinalAssessmentReport,
    VisualObservation
)
from modules.preprocessing import TextCleaner
from modules.claim_extraction import LLMClaimExtractor, RuleBasedClaimExtractor
from modules.evidence_retrieval import SemanticRetriever
from modules.nli_verification import NLIVerifier
from modules.visual_verification import VisualComparator
from modules.evidence_aggregation import EvidenceAggregator
from modules.pri_engine import PRICalculator
from modules.classification import AssessmentClassifier

class ReliabilityAssessmentPipeline:
    def __init__(self, use_llm_claims: bool = True):
        self.text_cleaner = TextCleaner()
        self.claim_extractor = LLMClaimExtractor() if use_llm_claims else RuleBasedClaimExtractor()
        self.retriever = SemanticRetriever()
        self.nli_verifier = NLIVerifier()
        self.visual_comparator = VisualComparator()
        self.aggregator = EvidenceAggregator()
        self.pri_calculator = PRICalculator()
        self.classifier = AssessmentClassifier()

    def assess_product(
        self,
        product: UnifiedProductInput,
        customer_image_url: Optional[str] = None
    ) -> FinalAssessmentReport:
        """
        Executes end-to-end reliability assessment on a unified product input.
        """
        # Step 1: Clean and segment customer reviews
        cleaned_reviews = self.text_cleaner.segment_reviews(product.customer_reviews)

        # Step 2: Extract atomic verifiable claims from seller features & title
        cleaned_features = [self.text_cleaner.clean_seller_feature(f) for f in product.features]
        atomic_claims = self.claim_extractor.extract_claims(product.title, cleaned_features)

        # Step 3: Semantic evidence retrieval per claim
        evidence_map = self.retriever.retrieve_evidence_for_claims(
            atomic_claims,
            cleaned_reviews
        )

        # Step 4: Directional NLI & Claim aggregation
        claim_assessments = self.aggregator.aggregate_claim_evidence(
            atomic_claims,
            evidence_map,
            self.nli_verifier
        )

        # Step 5: Visual consistency verification
        seller_img = product.seller_images[0] if product.seller_images else None
        cust_img = customer_image_url or (product.customer_images[0] if product.customer_images else None)

        visual_obs = self.visual_comparator.compare_images(seller_img, cust_img)

        # Step 6: PRI Engine Computation
        pri_results = self.pri_calculator.calculate_pri(claim_assessments, visual_obs)

        # Step 7: 4-State Final Decision & Explanation Rules
        classification, discrepancies, supporting_reasons = self.classifier.classify(
            overall_pri=pri_results["overall_pri"],
            coverage=pri_results["coverage"],
            claims=claim_assessments,
            visual_obs=visual_obs
        )

        # Step 8: Build Final Report
        report = FinalAssessmentReport(
            product_id=product.product_id,
            title=product.title,
            overall_pri=pri_results["overall_pri"],
            text_pri=pri_results["text_pri"],
            visual_pri=pri_results["visual_pri"],
            classification=classification,
            coverage=pri_results["coverage"],
            total_claims=pri_results["total_claims"],
            evaluated_claims=pri_results["evaluated_claims"],
            claims=claim_assessments,
            visual_assessment=visual_obs,
            key_discrepancies=discrepancies,
            supporting_reasons=supporting_reasons,
            provenance_metadata={
                "source_type": product.source_type,
                "source_url": product.source_url,
                "cleaned_reviews_count": len(cleaned_reviews),
                "extracted_claims_count": len(atomic_claims)
            }
        )

        return report
