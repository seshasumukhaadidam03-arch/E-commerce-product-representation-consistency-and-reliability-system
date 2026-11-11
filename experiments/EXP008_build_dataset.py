# =====================================================================
# EXP-008: Product-level feasibility scan + candidate dataset builder
# Project: AI-Based E-Commerce Product Representation Consistency (A10)
# Data:    Amazon Reviews 2023 (Hou et al., 2024), McAuley Lab, HF hub
#
# Run in Google Colab, one section at a time (each "# %%" = one cell).
# It does NOT repeat EXP-001..007B. It answers the open questions:
#   - How many products have enough reviews / photo reviews / seller bullets?
#   - What does the per-product evidence distribution look like?
# and it saves a reproducible candidate pool + a stratified sample for
# human annotation.
# =====================================================================

# %% [1] Configuration -------------------------------------------------
import json, os, random, collections, statistics, time
import requests

CATEGORY      = "Amazon_Fashion"   # start small; later e.g. "Electronics"
BASE          = "https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023/resolve/main/"
META_SRC      = BASE + f"raw/meta_categories/meta_{CATEGORY}.jsonl"
REVIEW_SRC    = BASE + f"raw/review_categories/{CATEGORY}.jsonl"
OUT_DIR       = f"/content/drive/MyDrive/A10_datasets/{CATEGORY}"   # or a local folder
SEED          = 42

MIN_FEATURES      = 3    # seller bullets needed to extract claims
MIN_REVIEWS       = 20   # text evidence needed per product
MIN_PHOTO_REVIEWS = 3    # for the visual sub-study (C5)
SAMPLE_PER_STRATUM = 20  # products per rating stratum for annotation
MAX_REVIEWS_KEPT   = 200 # cap per sampled product (keeps annotation sane)
MAX_LINES = None         # set e.g. 200_000 for a quick dry run; None = full file

os.makedirs(OUT_DIR, exist_ok=True)
random.seed(SEED)


def stream_jsonl(src, max_lines=None):
    """Yield dicts from a local path or an HTTP(S) URL, line by line."""
    if src.startswith("http"):
        with requests.get(src, stream=True, timeout=120) as r:
            r.raise_for_status()
            for i, line in enumerate(r.iter_lines()):
                if max_lines and i >= max_lines:
                    break
                if line:
                    yield json.loads(line)
    else:
        with open(src, encoding="utf-8") as f:
            for i, line in enumerate(f):
                if max_lines and i >= max_lines:
                    break
                if line.strip():
                    yield json.loads(line)


# %% [2] Pass 1 - catalogue metadata (seller side) ----------------------
t0 = time.time()
meta = {}            # parent_asin -> compact seller record
n_meta = 0
for rec in stream_jsonl(META_SRC, MAX_LINES):
    n_meta += 1
    feats = rec.get("features") or []
    if len(feats) < MIN_FEATURES:
        continue
    meta[rec["parent_asin"]] = {
        "parent_asin": rec["parent_asin"],
        "title": rec.get("title"),
        "features": feats,
        "description": rec.get("description") or [],
        "details": rec.get("details") or {},
        "catalogue_images": [im.get("large") or im.get("hi_res") or im.get("thumb")
                             for im in (rec.get("images") or [])],
        "average_rating": rec.get("average_rating"),
        "rating_number": rec.get("rating_number"),
        "main_category": rec.get("main_category"),
    }
print(f"Metadata records read: {n_meta:,}")
print(f"Products with >= {MIN_FEATURES} bullets: {len(meta):,}  ({time.time()-t0:.0f}s)")


# %% [3] Pass 2 - count evidence per product (reviews side) -------------
t0 = time.time()
stats = collections.defaultdict(lambda: {"reviews": 0, "photo_reviews": 0,
                                         "verified": 0, "low_rating": 0})
n_rev = 0
for rv in stream_jsonl(REVIEW_SRC, MAX_LINES):
    n_rev += 1
    pid = rv.get("parent_asin")
    if pid not in meta:
        continue
    s = stats[pid]
    s["reviews"] += 1
    s["photo_reviews"] += int(bool(rv.get("images")))
    s["verified"] += int(bool(rv.get("verified_purchase")))
    s["low_rating"] += int((rv.get("rating") or 5) <= 2)
print(f"Review records read: {n_rev:,}  ({time.time()-t0:.0f}s)")


# %% [4] EXP-008 results - the feasibility numbers ----------------------
eligible_text  = [p for p, s in stats.items() if s["reviews"] >= MIN_REVIEWS]
eligible_photo = [p for p in eligible_text if stats[p]["photo_reviews"] >= MIN_PHOTO_REVIEWS]
all_counts = [s["reviews"] for s in stats.values()]
photo_share = (sum(s["photo_reviews"] for s in stats.values()) /
               max(1, sum(all_counts)))

summary = {
    "category": CATEGORY,
    "dry_run_max_lines": MAX_LINES,
    "metadata_records": n_meta,
    "review_records": n_rev,
    "products_with_min_features": len(meta),
    "products_with_any_review": len(stats),
    "median_reviews_per_product": statistics.median(all_counts) if all_counts else 0,
    "share_of_reviews_with_photos": round(photo_share, 4),
    f"products_ge_{MIN_REVIEWS}_reviews": len(eligible_text),
    f"products_ge_{MIN_REVIEWS}_reviews_and_ge_{MIN_PHOTO_REVIEWS}_photo_reviews": len(eligible_photo),
}
print(json.dumps(summary, indent=2))
with open(f"{OUT_DIR}/EXP008_summary.json", "w") as f:
    json.dump(summary, f, indent=2)


# %% [5] Stratified sample for human annotation -------------------------
# Strata by product average rating so the sample is not all happy products.
# NOTE: the stratum is a SAMPLING device only; labels come from annotators.
def stratum(pid):
    r = meta[pid]["average_rating"] or 0
    return "low(<3.5)" if r < 3.5 else ("mid(3.5-4.2)" if r < 4.2 else "high(>=4.2)")

pool = sorted(eligible_text)               # sorted -> reproducible with SEED
by_stratum = collections.defaultdict(list)
for p in pool:
    by_stratum[stratum(p)].append(p)

sample = []
for name, items in sorted(by_stratum.items()):
    photo_first = [p for p in items if p in set(eligible_photo)]
    rest = [p for p in items if p not in set(eligible_photo)]
    random.shuffle(photo_first); random.shuffle(rest)
    picked = (photo_first + rest)[:SAMPLE_PER_STRATUM]   # prefer photo products
    sample += picked
    print(f"{name:14s} pool={len(items):6,}  picked={len(picked)}  "
          f"with_photos={sum(p in set(eligible_photo) for p in picked)}")
sample_set = set(sample)


# %% [6] Pass 3 - collect the reviews of sampled products ---------------
kept = collections.defaultdict(list)
for rv in stream_jsonl(REVIEW_SRC, MAX_LINES):
    pid = rv.get("parent_asin")
    if pid in sample_set and len(kept[pid]) < MAX_REVIEWS_KEPT:
        kept[pid].append({
            "review_id": f"{pid}_{len(kept[pid]):04d}",   # stable provenance id
            "rating": rv.get("rating"),
            "title": rv.get("title"),
            "text": rv.get("text"),
            "verified_purchase": rv.get("verified_purchase"),
            "helpful_vote": rv.get("helpful_vote"),
            "timestamp": rv.get("timestamp"),
            "customer_images": [im.get("large_image_url") for im in (rv.get("images") or [])],
        })


# %% [7] Save the dataset ----------------------------------------------
with open(f"{OUT_DIR}/products.jsonl", "w", encoding="utf-8") as f:
    for pid in sample:
        rec = dict(meta[pid], **stats[pid], stratum=stratum(pid))
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
with open(f"{OUT_DIR}/reviews.jsonl", "w", encoding="utf-8") as f:
    for pid in sample:
        for rv in kept[pid]:
            f.write(json.dumps(dict(rv, parent_asin=pid), ensure_ascii=False) + "\n")
with open(f"{OUT_DIR}/sample_asins.txt", "w") as f:
    f.write("\n".join(sample))
print(f"Saved {len(sample)} products and "
      f"{sum(len(v) for v in kept.values()):,} reviews to {OUT_DIR}")
