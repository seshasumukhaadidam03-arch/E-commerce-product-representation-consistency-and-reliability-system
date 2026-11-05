"""
pipeline.py - The Master Pipeline
==================================
Connects: Claim Extractor -> Review Preprocessor -> Retriever -> NLI Scorer

Key Design:
  - BOTH seller claims and customer reviews are cleaned and filtered
  - Gemini extracts facts from seller side (with cache + fallback)
  - Fact vs Opinion filter on customer review side
  - Amazon webpage noise (UI elements, metadata, ads) is stripped from both sides
"""

import json
import os
import re
from claim_extractor import extract_claims
from retriever import ReviewRetriever
from nli_scorer import NLIScorer
import warnings

warnings.filterwarnings("ignore")

CACHE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "sample", "cached_claims.json"
)


class ReliabilityPipeline:
    def __init__(self):
        print("--- INITIALIZING PIPELINE ---")
        self.retriever = ReviewRetriever()
        self.scorer = NLIScorer()
        self._load_claim_cache()
        print("--- PIPELINE READY ---\n")

    def _load_claim_cache(self):
        self.claim_cache = {}
        if os.path.exists(CACHE_PATH):
            with open(CACHE_PATH, "r", encoding="utf-8") as f:
                self.claim_cache = json.load(f)
            print(f"Loaded cached claims for {len(self.claim_cache)} products.")

    # ==================================================================
    # CLEANING: Strip Amazon webpage noise from pasted text
    # ==================================================================
    def _clean_seller_input(self, features):
        """
        Filters out Amazon metadata, UI elements, and non-claim lines
        from the seller's description. Keeps only actual product claims.
        """
        # Lines that are metadata or UI noise, NOT product claims
        noise_patterns = [
            "about this item", "additional information", "see less",
            "see more", "product description", "product details",
            "manufacturer", "packer", "importer", "asin",
            "item weight", "item dimensions", "item model",
            "net quantity", "generic name", "country of origin",
            "department", "date first available", "best sellers rank",
            "customer reviews:", "out of 5 stars", "global ratings",
            "product dimensions", "feedback", "report",
        ]

        clean_claims = []
        for line in features:
            line_lower = line.strip().lower()

            # Skip empty or very short lines
            if len(line.strip()) < 10:
                continue

            # Skip metadata/noise
            is_noise = False
            for pattern in noise_patterns:
                if pattern in line_lower:
                    is_noise = True
                    break
            if is_noise:
                continue

            # Skip lines that are just codes/numbers
            if re.match(r'^[A-Z0-9\s\-:]+$', line.strip()) and len(line.strip()) < 30:
                continue

            clean_claims.append(line.strip())

        return clean_claims[:5]  # Max 5 claims to keep analysis focused

    def _clean_review_input(self, review_texts):
        """
        Strips Amazon UI elements, reviewer info, star ratings, and
        navigation text from pasted review content. Keeps only actual
        customer sentences about the product.
        """
        # Amazon UI noise patterns
        noise_patterns = [
            "verified purchase", "helpful", "report",
            "reviewed in india", "reviewed in", "out of 5 star",
            "customer image", "click to open", "see all photo",
            "previous slide", "next slide", "previous page", "next page",
            "top reviews", "global ratings", "how are ratings",
            "write a product review", "share your thoughts",
            "sponsored", "related products", "brands in this category",
            "customers who viewed", "also viewed", "free delivery",
            "limited time deal", "m.r.p:", "get it by",
            "delivery by amazon", "you pay", "coupon",
            "shop ", "page 1 of", "previous set", "next set",
            "ai generated", "generated from the text",
            "select to learn more",
            "person found this helpful",
        ]

        # Patterns for reviewer metadata lines
        meta_patterns = [
            r'^size:\s', r'^colour:\s', r'^color:\s',
            r'^\d+ out of 5', r'^\d+\.\d+ out of',
            r'^[A-Za-z]+ [A-Za-z]+$',  # Just a name like "Ayush" or "Bina Vora"
            r'^\d{1,2}\s\w+\s\d{4}',  # Dates like "2 September 2026"
            r'^size:\s?\w+colour:', # Combined size/colour
        ]

        clean_sentences = []
        for text in review_texts:
            # Clean HTML
            text = text.replace("<br />", " ").replace("<br>", " ")
            text = text.replace("&amp;", "&").replace("&quot;", '"')

            # Split into sentences
            for delimiter in ['!', '?']:
                text = text.replace(delimiter, '.')
            sentences = text.split('.')

            for s in sentences:
                clean = s.strip()
                if len(clean) < 15:
                    continue

                clean_lower = clean.lower()

                # Skip UI noise
                is_noise = False
                for pattern in noise_patterns:
                    if pattern in clean_lower:
                        is_noise = True
                        break
                if is_noise:
                    continue

                # Skip metadata patterns
                is_meta = False
                for pat in meta_patterns:
                    if re.match(pat, clean, re.IGNORECASE):
                        is_meta = True
                        break
                if is_meta:
                    continue

                # Skip price/rating lines
                if re.match(r'^[\-\d%₹$€£,.]+$', clean.strip()):
                    continue

                # Apply fact vs opinion filter
                if self._is_factual(clean):
                    clean_sentences.append(clean)

        return clean_sentences

    def _is_factual(self, sentence):
        """
        Fact vs Opinion classifier. Zero extra RAM.
        Returns True if sentence has verifiable content, False if pure opinion.
        """
        s = sentence.lower()

        # Pure opinion patterns (skip if short)
        opinion_patterns = [
            "i love", "i hate", "i like", "i dislike",
            "highly recommend", "would recommend", "don't recommend",
            "best purchase", "worst purchase", "great product",
            "awesome product", "terrible product", "amazing product",
            "five stars", "one star", "waste of money",
            "can't go wrong", "a must have", "must buy",
            "glad i bought", "very happy with", "so happy",
            "nice jacket", "nice product", "best jacket",
        ]
        for phrase in opinion_patterns:
            if phrase in s and len(s) < 50:
                return False

        # Factual words (verifiable attributes)
        fact_words = [
            # Physical
            "fit", "fits", "fitting", "size", "sizes",
            "broke", "break", "broken", "crack", "tear", "torn",
            "dry", "wet", "leak", "water", "waterproof", "resistant",
            "sharp", "dull", "cut", "cutting",
            "thick", "thin", "durable", "flimsy", "sturdy", "fragile",
            "comfortable", "uncomfortable", "soft", "hard", "rigid",
            "color", "colour", "material", "fabric", "plastic", "nylon", "polyester",
            "heavy", "light", "lightweight", "weight",
            "small", "big", "large", "tight", "loose",
            "hot", "cold", "warm", "cool", "heat", "winter", "wind",
            # Clothing specific
            "stitch", "stitching", "zipper", "zip", "pocket", "sleeve",
            "collar", "neck", "button", "lining", "padding",
            "wear", "wearing", "worn",
            # Beauty/grooming specific
            "cap", "hair", "shower", "elastic", "band", "headband",
            "lock", "handle", "brush", "divider", "tray",
            "silk", "nail", "wrap", "strength",
            "pattern", "design", "edge",
            "case", "bag", "space", "compartment",
            "shear", "scissor", "blade", "steel",
            "season", "spice", "flavor", "taste", "cook",
            # Performance
            "hour", "day", "week", "month", "year", "lasted", "last",
            "works", "worked", "doesn't work", "stopped",
            "battery", "charge", "screen", "camera",
            "price", "worth", "expensive", "cheap", "cost", "value",
            "quality", "premium", "finish",
            "smell", "odor", "look", "feel",
            # Negative indicators (important for contradiction detection)
            "don't", "doesn't", "not", "never", "poor", "bad",
            "wrong", "fake", "false", "different", "doesn't match",
        ]

        for word in fact_words:
            if word in s:
                return True

        # Long sentences usually have factual content
        if len(s) > 60:
            return True

        return False

    # ==================================================================
    # CLAIM EXTRACTION
    # ==================================================================
    def _extract_claims(self, product_data):
        """Priority: Cache -> Gemini API -> Rule-based fallback"""
        product_id = product_data.get("product_id", "")
        title = product_data.get("title", "")
        features = product_data.get("features", [])

        # Priority 1: Cached claims
        if product_id in self.claim_cache:
            print("  -> Using cached claims.")
            return self.claim_cache[product_id]

        # Priority 2: For manual input, clean the pasted claims
        if product_id == "manual":
            print("  -> Cleaning manual input claims.")
            return self._clean_seller_input(features)

        # Priority 3: Gemini API
        print("  -> Calling Gemini API...")
        claims = extract_claims(title, features)
        if claims:
            return claims

        # Priority 4: Rule-based fallback
        print("  -> API failed. Using rule-based fallback.")
        return self._clean_seller_input(features)

    # ==================================================================
    # REVIEW PREPROCESSING
    # ==================================================================
    def _preprocess_reviews(self, product_data):
        """Cleans, chunks, and filters customer reviews."""
        raw_reviews = [r["text"] for r in product_data.get("reviews", [])]
        return self._clean_review_input(raw_reviews)

    # ==================================================================
    # MAIN ANALYSIS
    # ==================================================================
    def analyze_product(self, product_data):
        title = product_data.get("title", "")
        print(f"Analyzing: {title[:60]}...")

        # STEP 0: Preprocess reviews
        reviews = self._preprocess_reviews(product_data)
        print(f"  -> {len(reviews)} factual review sentences extracted.")

        # STEP 1: Extract claims
        print("Step 1: Extracting seller claims...")
        claims = self._extract_claims(product_data)
        print(f"  -> {len(claims)} claims to verify.")

        if not claims or not reviews:
            return {"overall_pri": 0, "claim_details": []}

        # STEP 2 & 3: Retrieve and Score
        print("Step 2 & 3: Retrieving evidence and scoring...")
        claim_results = []

        for i, claim in enumerate(claims, 1):
            relevant = self.retriever.find_relevant_reviews(claim, reviews, top_k=5)

            # CONTRADICTION-DETECTOR APPROACH:
            # NLI models are excellent at detecting contradictions (87-99% confidence)
            # but weak at detecting support/entailment (0-3% for valid support).
            # So we use NLI as a contradiction detector:
            #   - Review CONTRADICTS claim (Contradiction > 50%) -> negative evidence
            #   - Review does NOT contradict (Support or Neutral) -> consistent evidence
            # This maps to human logic: "How many reviewers complained about this?"

            consistent_count = 0  # Reviews that don't contradict the claim
            contradict_count = 0  # Reviews that explicitly contradict
            evidence_list = []

            for review_data in relevant:
                evidence_text = review_data["review_text"]
                nli_result = self.scorer.check_consistency(claim, evidence_text)

                verdict = nli_result["winner"]
                conf = nli_result["scores"]

                # Classify: is this review contradicting the claim?
                if verdict == "Contradiction" and conf["Contradiction"] > 50:
                    contradict_count += 1
                    display_verdict = "Contradiction"
                elif verdict == "Support" and conf["Support"] > 30:
                    consistent_count += 1
                    display_verdict = "Support"
                else:
                    # Neutral = review discusses topic but doesn't contradict
                    # This is CONSISTENT with the claim (implicit support)
                    consistent_count += 1
                    display_verdict = "Consistent"

                evidence_list.append({
                    "text": evidence_text,
                    "verdict": display_verdict,
                    "confidence": conf,
                    "relevance": review_data["relevance_score"]
                })

            total_evidence = consistent_count + contradict_count
            if total_evidence > 0:
                # What % of relevant evidence is consistent with this claim?
                claim_consistency = (consistent_count / total_evidence) * 100
            else:
                claim_consistency = 50.0  # No evidence = uncertain

            claim_results.append({
                "claim": claim,
                "support": round(claim_consistency, 1),
                "contradict": round(100 - claim_consistency, 1),
                "consistent_count": consistent_count,
                "contradict_count": contradict_count,
                "total_evidence": total_evidence,
                "evidence": evidence_list
            })

            print(f"  Claim {i}: {consistent_count} consistent, {contradict_count} contradict -> {round(claim_consistency, 1)}%")

        # =========================================================
        # STEP 4: Calculate PRI (Product Reliability Index)
        # =========================================================
        # PRI = weighted average of all claim consistency ratios
        # Claims with MORE evidence get MORE weight (more data = more trust)

        total_weighted = 0
        total_weight = 0

        for cd in claim_results:
            # Weight = number of evidence items (more evidence = more reliable)
            weight = max(cd["total_evidence"], 1)
            total_weighted += cd["support"] * weight
            total_weight += weight

        if total_weight > 0:
            pri_score = total_weighted / total_weight
        else:
            pri_score = 50.0

        pri_score = max(0, min(100, round(pri_score, 1)))

        print(f"  -> PRI Score: {pri_score}/100")

        return {
            "overall_pri": pri_score,
            "claim_details": claim_results
        }


if __name__ == "__main__":
    pipeline = ReliabilityPipeline()

    with open("../data/sample/sample_products.json", "r", encoding="utf-8") as f:
        products = json.load(f)

    results = pipeline.analyze_product(products[0])

    print("\n" + "=" * 50)
    print(f"PRI: {results['overall_pri']}/100")
    print("=" * 50)
    for i, res in enumerate(results["claim_details"], 1):
        print(f"\nClaim {i}: {res['claim'][:60]}...")
        print(f"  Support: {res['support']}% | Contradict: {res['contradict']}%")
        for ev in res["evidence"]:
            print(f"  [{ev['verdict']}] {ev['text'][:80]}...")
