"""
pri_calculator.py - Mathematically Defensible PRI Engine
========================================================
Formulates a transparent Product Reliability Index (0 - 100).

Mathematical Definition:
-------------------------
1. Claim-Level Consistency:
   For each claim c_i:
   Score(c_i) = (Support + Consistent) / (Support + Consistent + (Contradiction * Penalty)) * 100

2. Textual PRI (PRI_text):
   Weighted average across claims:
   PRI_text = sum(Score(c_i) * w_i) / sum(w_i)
   where w_i = log2(1 + EvidenceCount(c_i)) + 1 (claims with more evidence have higher statistical weight).

3. Multimodal PRI (PRI_final):
   If visual evidence is present:
   PRI_final = (PRI_text * w_text) + (VisualScore * w_visual)
   If visual evidence is absent:
   PRI_final = PRI_text

4. Evidence Coverage:
   Coverage = (Claims with active evidence) / (Total extracted claims)
"""

import math
from typing import List, Dict, Any, Tuple
from config.settings import (
    PRI_TEXT_WEIGHT,
    PRI_VISUAL_WEIGHT,
    CONTRADICTION_PENALTY_FACTOR
)
from modules.product_input.schema import ClaimAssessment, VisualObservation

class PRICalculator:
    def __init__(
        self,
        text_weight: float = PRI_TEXT_WEIGHT,
        visual_weight: float = PRI_VISUAL_WEIGHT,
        penalty_factor: float = CONTRADICTION_PENALTY_FACTOR
    ):
        self.text_weight = text_weight
        self.visual_weight = visual_weight
        self.penalty_factor = penalty_factor

    def calculate_pri(
        self,
        claims: List[ClaimAssessment],
        visual_obs: VisualObservation
    ) -> Dict[str, Any]:
        """
        Computes composite PRI, text PRI, visual contribution, and detailed breakdown.
        """
        if not claims:
            return {
                "overall_pri": 50.0,
                "text_pri": 50.0,
                "visual_pri": None,
                "coverage": 0.0,
                "total_claims": 0,
                "evaluated_claims": 0,
                "breakdown": []
            }

        total_claims = len(claims)
        evaluated_claims = 0
        total_weighted_score = 0.0
        total_weight = 0.0

        claim_breakdowns = []

        for c in claims:
            s = c.support_count
            n = c.neutral_count
            contra = c.contradict_count
            total_ev = s + n + contra

            if total_ev > 0:
                evaluated_claims += 1
                # Non-contradictory support vs penalized contradiction
                consistent_ev = s + n
                penalized_contra = contra * self.penalty_factor

                denominator = consistent_ev + penalized_contra
                claim_score = (consistent_ev / denominator) * 100.0 if denominator > 0 else 50.0

                # Weight is logarithmically scaled with evidence count to avoid skew from 1 random review
                weight = math.log2(1 + total_ev) + 1.0
            else:
                claim_score = 50.0
                weight = 0.5  # Baseline prior weight for unverified claims

            total_weighted_score += claim_score * weight
            total_weight += weight

            claim_breakdowns.append({
                "claim_id": c.claim.claim_id,
                "claim_text": c.claim.text,
                "attribute": c.claim.attribute,
                "score": round(claim_score, 1),
                "weight": round(weight, 2),
                "evidence_count": total_ev,
                "contradictions": contra
            })

        text_pri = total_weighted_score / total_weight if total_weight > 0 else 50.0
        text_pri = max(0.0, min(100.0, text_pri))

        # Visual blending if visual evidence was provided and computed
        if visual_obs.available and visual_obs.visual_consistency_score is not None:
            visual_pri = visual_obs.visual_consistency_score
            overall_pri = (text_pri * self.text_weight) + (visual_pri * self.visual_weight)
        else:
            visual_pri = None
            overall_pri = text_pri

        overall_pri = max(0.0, min(100.0, overall_pri))
        coverage = evaluated_claims / total_claims if total_claims > 0 else 0.0

        return {
            "overall_pri": round(overall_pri, 1),
            "text_pri": round(text_pri, 1),
            "visual_pri": round(visual_pri, 1) if visual_pri is not None else None,
            "coverage": round(coverage, 2),
            "total_claims": total_claims,
            "evaluated_claims": evaluated_claims,
            "breakdown": claim_breakdowns
        }
