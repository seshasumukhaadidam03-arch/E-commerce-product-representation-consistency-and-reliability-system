"""Quick NLI diagnostic - tests raw confidence scores for wallet reviews vs claims"""
import sys
sys.path.insert(0, 'src')
from nli_scorer import NLIScorer

scorer = NLIScorer()

# The 5 cached claims for Rigohill Wallet
claims = [
    "The wallet is made of high quality natural genuine leather",
    "Features multiple compartments including credit card slots, cash pockets, zip compartment and coin pocket",
    "Equipped with advanced RFID blocking technology for card protection",
    "Constructed with sturdy craftsmanship, durable stitching and premium finish",
    "The color and finish match the advertised olive green leather appearance"
]

# The 6 actual reviews (key sentences)
reviews = [
    "Good product, many pockets, genuine leather material, separate credit card pocket",
    "Not sturdy wallet material, bad, will get damaged easily",
    "Leather quality not good at all, feels very cheap",
    "The leather quality feels good and the finishing is neat",
    "The stitching and overall build quality are also impressive for the price",
    "Poor quality zipper, lots of stains, color washed off, uneven color",
    "It has enough space for cards, cash and coins, while still being comfortable to carry",
    "I particularly like the multiple card slots and zip compartment, which make it easy to organize"
]

print("\n" + "=" * 80)
print("RAW NLI CONFIDENCE SCORES")
print("=" * 80)

# Test just claim 1 (leather) against all reviews
claim = claims[0]
print(f"\nCLAIM: {claim}")
print("-" * 80)

for rev in reviews:
    result = scorer.check_consistency(claim, rev)
    s = result["scores"]
    v = result["winner"]
    print(f"  [{v:13s}] S:{s['Support']:5.1f}% C:{s['Contradiction']:5.1f}% N:{s['Neutral']:5.1f}%  | {rev[:65]}")

# Test claim 4 (sturdy/stitching) 
claim = claims[3]
print(f"\nCLAIM: {claim}")
print("-" * 80)

for rev in reviews:
    result = scorer.check_consistency(claim, rev)
    s = result["scores"]
    v = result["winner"]
    print(f"  [{v:13s}] S:{s['Support']:5.1f}% C:{s['Contradiction']:5.1f}% N:{s['Neutral']:5.1f}%  | {rev[:65]}")
