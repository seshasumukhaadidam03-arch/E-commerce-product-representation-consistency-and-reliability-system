"""
download_sample_v3.py
---------------------
Downloads a small sample of REAL Amazon products WITH reviews.
Uses Hugging Face Hub to stream JSONL files line by line.
Only downloads what we need - stops after finding good products.
"""

import json
import os
import urllib.request

BASE = "https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023/resolve/main/raw"

def stream_jsonl_lines(url, max_lines=5000):
    """Read a JSONL file from a URL, line by line, up to max_lines.
    This avoids downloading the entire multi-GB file."""
    print(f"  Streaming from: ...{url[-60:]}")
    count = 0
    req = urllib.request.Request(url, headers={"User-Agent": "Python/3"})
    with urllib.request.urlopen(req) as response:
        for line_bytes in response:
            if count >= max_lines:
                break
            line = line_bytes.decode("utf-8").strip()
            if line:
                try:
                    yield json.loads(line)
                    count += 1
                except json.JSONDecodeError:
                    continue
            if count % 1000 == 0 and count > 0:
                print(f"    ...streamed {count} lines so far")
    print(f"  Done. Read {count} lines total.")


def download():
    print("=" * 60)
    print("Downloading sample Amazon products WITH reviews")
    print("Category: All_Beauty (smaller file, faster download)")
    print("=" * 60)
    
    # --- Using All_Beauty category because it's small (213 MB meta, 326 MB reviews) ---
    # Electronics is 5GB + 22GB = too slow for a sample download
    
    # Step 1: Get product metadata
    print("\n[Step 1/3] Reading product metadata...")
    meta_url = f"{BASE}/meta_categories/meta_All_Beauty.jsonl"
    
    products = {}
    for item in stream_jsonl_lines(meta_url, max_lines=2000):
        parent_asin = item.get("parent_asin", "")
        title = (item.get("title") or "").strip()
        features = item.get("features") or []
        description = item.get("description") or []
        images = item.get("images") or []
        
        # Ensure features is a list of strings
        if isinstance(features, str):
            features = [features]
        if isinstance(description, str):
            description = [description]
            
        # We want products with at least 2 feature bullets
        if title and len(features) >= 2 and parent_asin:
            # Extract image URLs
            img_urls = []
            for img in (images if isinstance(images, list) else []):
                if isinstance(img, dict):
                    url = img.get("large") or img.get("hi_res") or img.get("thumb") or ""
                    if url:
                        img_urls.append(url)
                elif isinstance(img, str) and img.startswith("http"):
                    img_urls.append(img)
            
            products[parent_asin] = {
                "product_id": parent_asin,
                "title": title,
                "description": [d for d in description if isinstance(d, str) and d.strip()],
                "features": [f for f in features if isinstance(f, str) and f.strip()],
                "images": img_urls[:5],
                "reviews": []
            }
    
    print(f"\n  Found {len(products)} products with feature bullets.")
    
    if len(products) == 0:
        print("  ERROR: No suitable products found. Exiting.")
        return
    
    # Step 2: Get reviews for these products
    print("\n[Step 2/3] Reading customer reviews...")
    review_url = f"{BASE}/review_categories/All_Beauty.jsonl"
    
    product_ids = set(products.keys())
    review_count = 0
    
    for review in stream_jsonl_lines(review_url, max_lines=20000):
        parent_asin = review.get("parent_asin", "")
        text = (review.get("text") or "").strip()
        rating = review.get("rating", 0)
        title_r = (review.get("title") or "").strip()
        verified = review.get("verified_purchase", False)
        
        if parent_asin in product_ids and len(text) > 15:
            products[parent_asin]["reviews"].append({
                "rating": float(rating) if rating else 0.0,
                "title": title_r,
                "text": text,
                "verified": bool(verified)
            })
            review_count += 1
    
    print(f"\n  Collected {review_count} reviews for {len(product_ids)} candidate products.")
    
    # Step 3: Select the best 5 products (most reviews)
    print("\n[Step 3/3] Selecting products with the most reviews...")
    
    all_products = list(products.values())
    # Sort by review count
    all_products.sort(key=lambda p: len(p["reviews"]), reverse=True)
    
    # Take top 5 that have at least 3 reviews
    final = [p for p in all_products if len(p["reviews"]) >= 3][:5]
    
    if len(final) < 3:
        print("  Warning: Few products with 3+ reviews. Taking what we have.")
        final = all_products[:5]
    
    # Cap reviews at 15 per product, keeping a mix of ratings
    for p in final:
        if len(p["reviews"]) > 15:
            revs = p["reviews"]
            positive = [r for r in revs if r["rating"] >= 4][:6]
            negative = [r for r in revs if r["rating"] <= 2][:5]
            mixed = [r for r in revs if r["rating"] == 3][:4]
            p["reviews"] = (positive + negative + mixed)[:15]
    
    # Save
    out_dir = os.path.join("data", "sample")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "sample_products.json")
    
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(final, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'=' * 60}")
    print(f"SUCCESS! Saved {len(final)} products to: {out_path}")
    print(f"{'=' * 60}")
    
    for i, p in enumerate(final, 1):
        rev_count = len(p["reviews"])
        feat_count = len(p["features"])
        img_count = len(p["images"])
        print(f"\n  Product {i}: {p['title'][:75]}")
        print(f"    Features: {feat_count} bullet points")
        print(f"    Reviews:  {rev_count} customer reviews")
        print(f"    Images:   {img_count} image URLs")
        if p["features"]:
            print(f"    Sample feature: \"{p['features'][0][:80]}\"")
        if p["reviews"]:
            r = p["reviews"][0]
            print(f"    Sample review ({r['rating']}*): \"{r['text'][:80]}...\"")


if __name__ == "__main__":
    download()
