"""
cross_encoder_nli.py - Natural Language Inference Engine
========================================================
Performs cross-attention NLI classification for Claim-Evidence pairs.
Premise = Customer Review Evidence
Hypothesis = Seller Claim
Evaluates Support, Contradiction, and Neutral probabilities with calibration.
"""

from typing import Dict, Any, List
from config.settings import NLI_CONTRADICTION_THRESHOLD, NLI_SUPPORT_THRESHOLD
from models.model_loader import ModelLoader
from modules.product_input.schema import EvidenceVerdict

class NLIVerifier:
    def __init__(self):
        self.classifier = ModelLoader().get_nli_classifier()

    def verify_claim_evidence(
        self,
        claim_text: str,
        evidence_text: str
    ) -> Dict[str, Any]:
        """
        Runs cross-encoder inference with Premise = evidence_text, Hypothesis = claim_text.
        Returns parsed probabilities and assigned EvidenceVerdict.
        """
        # Directional NLI standard: Premise (known observation) -> Hypothesis (assertion tested)
        result = self.classifier({"text": evidence_text, "text_pair": claim_text})

        scores = {
            "Contradiction": 0.0,
            "Support": 0.0,
            "Neutral": 0.0
        }

        for item in result:
            label = str(item["label"]).lower()
            percentage = round(item["score"] * 100, 1)

            if "contradiction" in label or "label_0" in label:
                scores["Contradiction"] = percentage
            elif "entailment" in label or "support" in label or "label_1" in label:
                scores["Support"] = percentage
            elif "neutral" in label or "label_2" in label:
                scores["Neutral"] = percentage

        # Calibrated decision logic:
        # Pretrained cross-encoders express very high certainty on contradiction (85-99%),
        # but conservative scores on colloquial confirmation.
        if scores["Contradiction"] >= NLI_CONTRADICTION_THRESHOLD:
            verdict = EvidenceVerdict.CONTRADICTION
        elif scores["Support"] >= NLI_SUPPORT_THRESHOLD:
            verdict = EvidenceVerdict.SUPPORT
        else:
            # Consistent if the evidence discusses the attribute without contradiction
            verdict = EvidenceVerdict.CONSISTENT

        return {
            "verdict": verdict,
            "scores": scores
        }
