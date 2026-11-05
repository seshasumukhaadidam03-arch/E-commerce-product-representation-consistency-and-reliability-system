"""
text_cleaner.py - Intelligent Review and Seller Text Preprocessing
==================================================================
Performs review sentence segmentation, empty/duplicate detection,
and filters out non-factual subjective opinions before NLI inference.
"""

import re
from typing import List, Dict, Any, Set

class TextCleaner:
    def __init__(self):
        # Known marketing & web junk substrings to discard
        self.junk_patterns = [
            r"make sure this fits by entering your model number",
            r"sponsored ad",
            r"customer reviews",
            r"all rights reserved",
            r"visit the .* store",
            r"asin\s*:\s*[a-z0-9]{10}",
            r"best sellers rank"
        ]

        # Factual keywords indicating testable product attributes
        self.fact_keywords = {
            "fit", "size", "dimension", "broken", "tear", "torn", "leak", "waterproof",
            "water", "resistant", "sharp", "durable", "flimsy", "sturdy", "fragile",
            "comfortable", "soft", "hard", "color", "colour", "material", "fabric",
            "plastic", "leather", "polyester", "cotton", "zipper", "zip", "pocket",
            "compartment", "slot", "stitching", "stitch", "battery", "charge", "screen",
            "works", "worked", "stopped", "smell", "odor", "weight", "heavy", "light",
            "rfid", "shade", "washed", "stain", "faded", "peeling"
        }

        # Strong opinion/sentiment starters that contain zero physical facts
        self.pure_opinion_patterns = [
            r"^i (really )?(love|like|hate|dislike) this( product)?\.?$",
            r"^awesome product\.?$",
            r"^very good\.?$",
            r"^worst purchase ever\.?$",
            r"^value for money\.?$",
            r"^superb!?$",
            r"^nice product\.?$",
            r"^good delivery time\.?$"
        ]

    def clean_seller_feature(self, text: str) -> str:
        """Cleans bullet point text and removes web metadata artifacts."""
        s = text.strip()
        for pattern in self.junk_patterns:
            s = re.sub(pattern, "", s, flags=re.IGNORECASE)
        s = re.sub(r"\s+", " ", s).strip()
        return s

    def is_factual_sentence(self, sentence: str) -> bool:
        """
        Determines whether a sentence expresses an objectively verifiable product attribute
        or just pure subjective sentiment.
        """
        s_lower = sentence.lower().strip()

        # Reject tiny sentence fragments
        if len(s_lower.split()) < 3:
            return False

        # Reject pure opinion templates
        for op in self.pure_opinion_patterns:
            if re.match(op, s_lower):
                return False

        # If it mentions any specific physical/functional attribute -> Factual
        words = set(re.findall(r"\b[a-z]{3,}\b", s_lower))
        if bool(words.intersection(self.fact_keywords)):
            return True

        # Informative sentences with descriptive adjectives and nouns (length > 40 chars)
        if len(s_lower) > 45:
            return True

        return False

    def segment_reviews(self, raw_reviews: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """
        Segments review paragraphs into discrete sentences, filters opinions,
        deduplicates, and retains provenance tracking (review_id).
        """
        segmented_evidence: List[Dict[str, str]] = []
        seen_texts: Set[str] = set()

        for idx, rev in enumerate(raw_reviews):
            raw_text = rev.get("text", "")
            rev_id = rev.get("id", f"rev_{idx+1}")

            # Split on standard punctuation (. ! ?)
            sentences = re.split(r"[.!?]+", raw_text)
            for s in sentences:
                clean_s = s.strip()
                if not clean_s or len(clean_s) < 12:
                    continue

                clean_s = re.sub(r"\s+", " ", clean_s)

                if self.is_factual_sentence(clean_s):
                    normalized_key = clean_s.lower()
                    if normalized_key not in seen_texts:
                        seen_texts.add(normalized_key)
                        segmented_evidence.append({
                            "sentence": clean_s,
                            "review_id": rev_id
                        })

        return segmented_evidence
