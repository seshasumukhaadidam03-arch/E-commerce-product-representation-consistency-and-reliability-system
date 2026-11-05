"""
decision_rules.py - 4-State Final Assessment Classifier
======================================================
Assigns one of four formal research classifications:
- CONSISTENT: Evidence predominantly confirms claims with adequate coverage.
- CONTRADICTORY: Direct evidence identifies critical discrepancies between claims and experience.
- MIXED EVIDENCE: Substantial supporting and contradicting evidence co-exist across claims.
- INSUFFICIENT EVIDENCE: Evidence is inadequate to draw a statistically defensible conclusion.
"""

from typing import List, Tuple
from config.settings import (
    PRI_CONSISTENT_THRESHOLD,
    PRI_CONTRADICTORY_THRESHOLD,
    MIN_COVERAGE_REQUIRED
)
from modules.product_input.schema import FinalClassification, ClaimAssessment, VisualObservation

class AssessmentClassifier:
    def __init__(
        self,
        consistent_threshold: float = PRI_CONSISTENT_THRESHOLD,
        contradictory_threshold: float = PRI_CONTRADICTORY_THRESHOLD,
        min_coverage: float = MIN_COVERAGE_REQUIRED
    ):
        self.consistent_threshold = consistent_threshold
        self.contradictory_threshold = contradictory_threshold
        self.min_coverage = min_coverage

    def classify(
        self,
        overall_pri: float,
        coverage: float,
        claims: List[ClaimAssessment],
        visual_obs: VisualObservation
    ) -> Tuple[FinalClassification, List[str], List[str]]:
        """
        Classifies product reliability and generates explainable supporting reasons and key discrepancies.
        """
        key_discrepancies: List[str] = []
        supporting_reasons: List[str] = []

        total_claims = len(claims)
        contradicted_claims = [c for c in claims if c.contradict_count > 0]
        verified_claims = [c for c in claims if c.status == "Verified" and (c.support_count + c.neutral_count) > 0]

        # Extract discrepancies
        for c in contradicted_claims:
            for ev in c.evidence:
                if ev.verdict.value == "Contradiction":
                    key_discrepancies.append(
                        f"Claim '{c.claim.text}' contradicted by customer feedback: \"{ev.sentence}\""
                    )

        # Extract visual discrepancies
        if visual_obs.available and visual_obs.observations:
            for obs in visual_obs.observations:
                if "discrepancy" in obs.lower() or "different" in obs.lower() or "low" in obs.lower():
                    key_discrepancies.append(f"Visual discrepancy: {obs}")
                else:
                    supporting_reasons.append(f"Visual observation: {obs}")

        # Extract supporting evidence
        for c in verified_claims:
            for ev in c.evidence:
                if ev.verdict.value in ["Support", "Consistent"]:
                    supporting_reasons.append(
                        f"Claim '{c.claim.text}' corroborated by: \"{ev.sentence}\""
                    )

        # -------------------------------------------------------------
        # 4-State Explicit Classification Logic
        # -------------------------------------------------------------
        if total_claims == 0 or (coverage < self.min_coverage and len(verified_claims) == 0):
            classification = FinalClassification.INSUFFICIENT_EVIDENCE
            if not key_discrepancies:
                key_discrepancies.append(
                    f"Only {int(coverage * 100)}% of claims had relevant customer evidence. Insufficient data to conclude."
                )

        elif len(contradicted_claims) > 0 and len(verified_claims) > 0 and overall_pri >= 40.0:
            # Clear coexistence of supported attributes and contradicted attributes
            classification = FinalClassification.MIXED_EVIDENCE

        elif overall_pri <= self.contradictory_threshold or (len(contradicted_claims) >= 1 and len(verified_claims) == 0):
            # Material failure without corroborating positive evidence
            classification = FinalClassification.CONTRADICTORY

        elif overall_pri >= self.consistent_threshold and len(contradicted_claims) == 0:
            classification = FinalClassification.CONSISTENT

        else:
            classification = FinalClassification.MIXED_EVIDENCE

        return classification, key_discrepancies[:5], supporting_reasons[:5]
