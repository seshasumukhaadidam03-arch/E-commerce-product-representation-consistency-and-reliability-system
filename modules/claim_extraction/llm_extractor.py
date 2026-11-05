"""
llm_extractor.py - Structured Atomic Claim Extraction using Gemini API
=====================================================================
Uses Gemini 3.8 Flash with deterministic JSON schema to extract discrete,
testable claims while discarding promotional marketing fluff.
Automatically falls back to RuleBasedClaimExtractor on API or network errors.
"""

import os
import json
from typing import List
from dotenv import load_dotenv
from config.settings import GEMINI_MODEL_NAME
from modules.product_input.schema import AtomicClaim
from .rule_extractor import RuleBasedClaimExtractor

load_dotenv()

class LLMClaimExtractor:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.fallback = RuleBasedClaimExtractor()
        self.client = None

        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"[LLMClaimExtractor] Could not initialize Gemini client: {e}")

    def extract_claims(self, title: str, features: List[str]) -> List[AtomicClaim]:
        """
        Extracts atomic claims via Gemini structured generation or falls back to rule engine.
        """
        if not self.client:
            return self.fallback.extract_atomic_claims(title, features)

        prompt = f"""
You are an expert e-commerce quality assurance auditor.
Analyze the following product title and advertised features:

Product Title: {title}
Features: {json.dumps(features)}

Extract discrete, objectively verifiable atomic claims made by the seller.
Rules:
1. Extract only testable facts (e.g. material composition, physical dimensions, compartments, battery life, color).
2. Filter out subjective marketing hype (e.g. "Best luxury gift", "Incredible comfort", "Premium style").
3. Break compound sentences into atomic single-assertion claims.
4. Categorize each attribute into one of: 'material', 'capacity', 'durability', 'security', 'dimension', 'color', 'feature'.

Output strictly a JSON list of objects matching this schema:
[
  {{"attribute": "material", "text": "Made of 100% natural genuine leather", "value": "genuine leather"}},
  {{"attribute": "capacity", "text": "Has 7 credit card slots and 2 secret compartments", "value": "7 slots, 2 compartments"}}
]
"""
        try:
            response = self.client.models.generate_content(
                model=GEMINI_MODEL_NAME,
                contents=prompt
            )
            raw = response.text.strip()
            if raw.startswith("```json"):
                raw = raw[7:-3].strip()
            elif raw.startswith("```"):
                raw = raw[3:-3].strip()

            parsed = json.loads(raw)
            claims: List[AtomicClaim] = []
            for idx, item in enumerate(parsed, 1):
                claims.append(AtomicClaim(
                    claim_id=f"claim_{idx}",
                    attribute=item.get("attribute", "feature"),
                    text=item.get("text", "").strip(),
                    value=item.get("value"),
                    confidence=0.95,
                    source="gemini_llm"
                ))
            return claims
        except Exception as e:
            print(f"[LLMClaimExtractor] API extraction failed ({e}). Falling back to rule-based engine.")
            return self.fallback.extract_atomic_claims(title, features)
