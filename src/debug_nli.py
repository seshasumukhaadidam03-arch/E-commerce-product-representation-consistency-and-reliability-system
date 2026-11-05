import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from pipeline import ReliabilityPipeline

with open("../data/sample/sample_products.json", "r", encoding="utf-8") as f:
    products = json.load(f)

pipeline = ReliabilityPipeline()
results = pipeline.analyze_product(products[0])

print("\n--- DEBUG OUTPUT ---")
for claim_data in results['claim_details']:
    print(f"\nCLAIM: {claim_data['claim'][:60]}...")
    for ev in claim_data['evidence']:
        print(f"  [{ev['verdict']}] {ev['text']}")
        print(f"      Scores: {ev['confidence']}")
