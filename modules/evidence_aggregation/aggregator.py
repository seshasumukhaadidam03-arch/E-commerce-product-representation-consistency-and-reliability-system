"""
aggregator.py - Evidence Aggregation & Provenance Synthesis
==========================================================
Synthesizes retrieved customer review sentences, NLI verdicts,
and confidence scores into claim-level assessments with transparent tracking.
"""

from typing import List, Dict, Any
from modules.product_input.schema import AtomicClaim, ReviewEvidence, ClaimAssessment, EvidenceVerdict

class EvidenceAggregator:
    def __init__(self):
        pass

    def aggregate_claim_evidence(
        self,
        claims: List[AtomicClaim],
        retrieved_evidence_map: Dict[str, List[Dict[str, Any]]],
        nli_verifier
    ) -> List[ClaimAssessment]:
        """
        Processes each claim, evaluates each retrieved evidence sentence with NLI,
        and computes claim-level consistency ratios and status.
        """
        assessments: List[ClaimAssessment] = []

        for claim in claims:
            candidates = retrieved_evidence_map.get(claim.claim_id, [])
            evidence_list: List[ReviewEvidence] = []

            support_count = 0
            contradict_count = 0
            neutral_count = 0

            for cand in candidates:
                sentence_text = cand["sentence"]
                nli_res = nli_verifier.verify_claim_evidence(claim.text, sentence_text)

                verdict = nli_res["verdict"]
                scores = nli_res["scores"]

                if verdict == EvidenceVerdict.CONTRADICTION:
                    contradict_count += 1
                elif verdict == EvidenceVerdict.SUPPORT:
                    support_count += 1
                else:
                    neutral_count += 1

                evidence_list.append(ReviewEvidence(
                    sentence=sentence_text,
                    review_id=cand.get("review_id", ""),
                    relevance_score=cand.get("relevance_score", 0.0),
                    verdict=verdict,
                    confidence_scores=scores
                ))

            # Calculate claim-level consistency
            # Contradiction is negative evidence; Support and Neutral/Consistent are non-contradictory
            total_active = support_count + contradict_count + neutral_count

            if total_active > 0:
                # Direct ratio: non-contradictory evidence over total relevant evidence
                consistent_count = support_count + neutral_count
                consistency_pct = (consistent_count / total_active) * 100.0

                if contradict_count > 0 and support_count == 0 and neutral_count <= 1:
                    status = "Contradicted"
                elif contradict_count > 0 and consistent_count > 0:
                    status = "Mixed Evidence"
                else:
                    status = "Verified"
            else:
                consistency_pct = 50.0  # Inconclusive/Neutral baseline
                status = "Unverified (No Direct Evidence)"

            assessments.append(ClaimAssessment(
                claim=claim,
                status=status,
                support_count=support_count,
                contradict_count=contradict_count,
                neutral_count=neutral_count,
                consistency_percentage=round(consistency_pct, 1),
                evidence=evidence_list
            ))

        return assessments
