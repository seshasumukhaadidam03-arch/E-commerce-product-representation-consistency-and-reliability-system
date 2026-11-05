"""
Unit tests for the rebuilt modules: URL parser, Rule extractor, Text Cleaner, PRI engine.
"""

import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import unittest
from modules.product_input.schema import (
    AtomicClaim,
    ClaimAssessment,
    VisualObservation,
    FinalClassification,
    UnifiedProductInput
)
from modules.product_input.url_parser import ProductURLExtractor
from modules.preprocessing.text_cleaner import TextCleaner
from modules.claim_extraction.rule_extractor import RuleBasedClaimExtractor
from modules.pri_engine.pri_calculator import PRICalculator
from modules.classification.decision_rules import AssessmentClassifier

class TestReliabilitySystem(unittest.TestCase):
    def setUp(self):
        self.url_parser = ProductURLExtractor()
        self.cleaner = TextCleaner()
        self.rule_extractor = RuleBasedClaimExtractor()
        self.pri_calculator = PRICalculator()
        self.classifier = AssessmentClassifier()

    def test_url_validation(self):
        self.assertTrue(self.url_parser.validate_url("https://www.amazon.in/dp/B08Z387RXH"))
        self.assertTrue(self.url_parser.validate_url("http://example.com/item/1"))
        self.assertFalse(self.url_parser.validate_url("not_a_url"))
        self.assertFalse(self.url_parser.validate_url("ftp://server/file"))

    def test_text_cleaner_factual_filtering(self):
        # Pure opinions should be filtered out
        self.assertFalse(self.cleaner.is_factual_sentence("Awesome product."))
        self.assertFalse(self.cleaner.is_factual_sentence("I really love this."))
        self.assertFalse(self.cleaner.is_factual_sentence("Superb!"))

        # Verifiable physical attributes should be retained
        self.assertTrue(self.cleaner.is_factual_sentence("The wallet is made of synthetic leather not genuine."))
        self.assertTrue(self.cleaner.is_factual_sentence("The zipper broke after two days of light use."))
        self.assertTrue(self.cleaner.is_factual_sentence("Has 7 card slots and fits easily in my back pocket."))

    def test_rule_based_claim_extraction(self):
        title = "Rigohill Olive Green Genuine Leather Wallet for Men"
        features = [
            "Made of high quality natural genuine leather.",
            "Equipped with RFID blocking technology.",
            "Features 7 credit card slots and 2 secret compartments.",
            "Sturdy construction with durable stitching."
        ]
        claims = self.rule_extractor.extract_atomic_claims(title, features)
        self.assertGreater(len(claims), 0)
        attributes = [c.attribute for c in claims]
        self.assertIn("material", attributes)
        self.assertIn("security", attributes)
        self.assertIn("capacity", attributes)

    def test_pri_calculation_consistent_case(self):
        claims = [
            ClaimAssessment(
                claim=AtomicClaim(claim_id="c1", attribute="material", text="Genuine leather"),
                status="Verified",
                support_count=4,
                neutral_count=1,
                contradict_count=0
            ),
            ClaimAssessment(
                claim=AtomicClaim(claim_id="c2", attribute="capacity", text="7 card slots"),
                status="Verified",
                support_count=3,
                neutral_count=0,
                contradict_count=0
            )
        ]
        visual = VisualObservation(available=False)
        result = self.pri_calculator.calculate_pri(claims, visual)
        self.assertGreaterEqual(result["overall_pri"], 80.0)
        self.assertEqual(result["coverage"], 1.0)

    def test_pri_calculation_contradictory_case(self):
        claims = [
            ClaimAssessment(
                claim=AtomicClaim(claim_id="c1", attribute="material", text="Genuine leather"),
                status="Contradicted",
                support_count=0,
                neutral_count=0,
                contradict_count=3
            ),
            ClaimAssessment(
                claim=AtomicClaim(claim_id="c2", attribute="durability", text="Durable zipper"),
                status="Contradicted",
                support_count=0,
                neutral_count=0,
                contradict_count=2
            )
        ]
        visual = VisualObservation(available=False)
        result = self.pri_calculator.calculate_pri(claims, visual)
        self.assertLessEqual(result["overall_pri"], 30.0)

    def test_classification_logic(self):
        # 1. High PRI with 0 contradictions -> CONSISTENT
        c_claims = [
            ClaimAssessment(
                claim=AtomicClaim(claim_id="c1", attribute="material", text="Genuine leather"),
                status="Verified",
                support_count=2,
                neutral_count=0,
                contradict_count=0
            )
        ]
        cls, _, _ = self.classifier.classify(85.0, 1.0, c_claims, VisualObservation(available=False))
        self.assertEqual(cls, FinalClassification.CONSISTENT)

        # 2. Low coverage -> INSUFFICIENT EVIDENCE
        cls, _, _ = self.classifier.classify(50.0, 0.20, c_claims, VisualObservation(available=False))
        self.assertEqual(cls, FinalClassification.INSUFFICIENT_EVIDENCE)

if __name__ == "__main__":
    unittest.main()
