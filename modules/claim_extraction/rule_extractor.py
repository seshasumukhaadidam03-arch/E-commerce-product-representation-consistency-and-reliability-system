"""
rule_extractor.py - Deterministic Rule-Based Atomic Claim Extractor
==================================================================
Identifies product attributes (material, dimensions, capacity, features, color)
from seller bullet points using linguistic patterns and entity-attribute heuristics.
Serves as an instant, zero-cost, reliable fallback when LLM API is unavailable.
"""

import re
from typing import List, Dict
from modules.product_input.schema import AtomicClaim

class RuleBasedClaimExtractor:
    def __init__(self):
        # Attribute category patterns
        self.attribute_patterns: Dict[str, List[str]] = {
            "material": [
                r"\b(leather|synthetic|polyester|cotton|plastic|silicone|stainless steel|nylon|ceramic|wood|denim)\b",
                r"\bmade of [a-z\s]+",
                r"\bcrafted (?:from|with) [a-z\s]+"
            ],
            "security": [
                r"\b(rfid(?:\s*blocking|\s*protection)?|anti-theft|tamper proof|secure lock)\b"
            ],
            "capacity": [
                r"\b(\d+)\s*(?:credit\s*)?(?:card\s*)?(?:slots?|compartments?|pockets?)\b",
                r"\bholds up to \d+\b",
                r"\b\d+\s*(?:liters?|litres?|ml|gb|tb|mah)\b",
                r"\b(?:multiple|several)\s*(?:card slots|compartments)\b"
            ],
            "durability": [
                r"\b(waterproof|water resistant|leakproof|sturdy|durable|scratch resistant|weatherproof)\b",
                r"\breinforced stitching\b"
            ],
            "dimension": [
                r"\b\d+(?:\.\d+)?\s*(?:cm|mm|inches|inch|kg|grams|g|lbs)\b",
                r"\bcompact (?:size|design)\b",
                r"\blightweight\b"
            ],
            "color": [
                r"\b(olive green|black|brown|tan|navy blue|red|grey|gray|white|beige)\b"
            ]
        }

    def extract_claims(self, title: str, features: List[str]) -> List[AtomicClaim]:
        """Unified interface method identical to LLMClaimExtractor."""
        return self.extract_atomic_claims(title, features)

    def extract_atomic_claims(self, title: str, features: List[str]) -> List[AtomicClaim]:
        """
        Extracts discrete, verifiable atomic claims from title and bullet features.
        """
        claims: List[AtomicClaim] = []
        claim_counter = 1
        seen_texts = set()

        # Focus claim extraction on discrete bullet features
        # Only use title if features list is empty
        all_text_units = features if features else [title]

        for unit in all_text_units:
            # Segment clauses by semicolons, commas separating specs, or pipes
            clauses = re.split(r"[;|\n•]+|\.\s+", unit)
            for clause in clauses:
                clean_clause = clause.strip()
                if len(clean_clause) < 8 or len(clean_clause) > 120:
                    continue

                # Clean leading bullet dashes or markers
                clean_clause = re.sub(r"^[-–—*#\d.]+\s*", "", clean_clause).strip()

                matched_attribute = "feature"
                matched_val = None

                # Detect attribute class
                for attr, patterns in self.attribute_patterns.items():
                    for pat in patterns:
                        match = re.search(pat, clean_clause, flags=re.IGNORECASE)
                        if match:
                            matched_attribute = attr
                            matched_val = match.group(0)
                            break
                    if matched_attribute != "feature":
                        break

                # Ignore fluff that matched nothing informative
                if matched_attribute == "feature" and not any(k in clean_clause.lower() for k in ["has", "with", "includes", "equipped", "features"]):
                    continue

                norm_key = clean_clause.lower()
                if norm_key not in seen_texts:
                    seen_texts.add(norm_key)
                    claims.append(AtomicClaim(
                        claim_id=f"claim_{claim_counter}",
                        attribute=matched_attribute,
                        text=clean_clause,
                        value=matched_val,
                        confidence=0.85,
                        source="rule_extractor"
                    ))
                    claim_counter += 1

        return claims[:8]  # Bound to top 8 meaningful claims
